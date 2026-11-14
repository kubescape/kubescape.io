const assert = require('node:assert/strict');
const { join } = require('node:path');
const { pathToFileURL } = require('node:url');
const { test } = require('node:test');

const edgeFunction = import(pathToFileURL(join(__dirname, '..', 'netlify/edge-functions/markdown.js')));

function serve(files) {
  const requested = [];
  global.fetch = async (url) => {
    requested.push(String(url));
    const path = new URL(url).pathname;
    if (!(path in files)) return new Response('Not found', { status: 404 });
    return new Response(files[path], {
      headers: { 'Content-Type': 'application/octet-stream', 'Cache-Control': 'public,max-age=0,must-revalidate', ETag: '"abc"' }
    });
  };
  return requested;
}

function createMockContext(html = '<!doctype html><html></html>', initialVary = 'Accept-Encoding') {
  return {
    next: async () => new Response(html, {
      status: 200,
      headers: new Headers({
        'Content-Type': 'text/html; charset=utf-8',
        ...(initialVary ? { 'Vary': initialVary } : {}),
      }),
    }),
  };
}

function negotiate(path, { accept = 'text/markdown', context = createMockContext() } = {}) {
  const headers = accept !== null ? { Accept: accept } : {};
  return edgeFunction.then(({ default: handler }) =>
    handler(new Request('https://kubescape.io' + path, { headers }), context));
}

test('runs on all paths without header filter, and fails open', async () => {
  const { config } = await edgeFunction;
  assert.equal(config.path, '/*');
  assert.equal(config.header, undefined);
  assert.equal(config.onError, 'bypass');
});

test('adds Vary: Accept to HTML responses for standard browser requests', async () => {
  const response = await negotiate('/docs/getting-started/', {
    accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  });
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(response.headers.get('Vary'), 'Accept-Encoding, Accept');
  assert.equal(await response.text(), '<!doctype html><html></html>');
});

test('adds Vary: Accept to HTML responses when Accept header is omitted', async () => {
  const response = await negotiate('/docs/getting-started/', {
    accept: null,
  });
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(response.headers.get('Vary'), 'Accept-Encoding, Accept');
});

test('serves the Markdown copy with its own content type and cache headers', async () => {
  const requested = serve({ '/docs/getting-started/index.md': '# Getting started\n' });
  const response = await negotiate('/docs/getting-started/');
  assert.deepEqual(requested, ['https://kubescape.io/docs/getting-started/index.md']);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Content-Type'), 'text/markdown; charset=utf-8');
  assert.equal(response.headers.get('Vary'), 'Accept');
  assert.equal(response.headers.get('Cache-Control'), 'public,max-age=0,must-revalidate');
  assert.equal(response.headers.get('ETag'), '"abc"');
  assert.equal(await response.text(), '# Getting started\n');
});

test('falls back to HTML with Vary: Accept when a page has no Markdown copy', async () => {
  serve({});
  const response = await negotiate('/blog/archive/2024/08/');
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(response.headers.get('Vary'), 'Accept-Encoding, Accept');
  assert.equal(await response.text(), '<!doctype html><html></html>');

  assert.equal(await negotiate('/blog/archive/2024/08/', { context: null }), undefined);
});

test('falls back to HTML when Markdown is forbidden or less preferred', async () => {
  const requested = serve({ '/docs/getting-started/index.md': '# Getting started\n' });

  const forbidden = await negotiate('/docs/getting-started/', {
    accept: 'text/html, text/markdown;q=0',
  });
  assert.equal(forbidden.status, 200);
  assert.equal(forbidden.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(forbidden.headers.get('Vary'), 'Accept-Encoding, Accept');

  const htmlPreferred = await negotiate('/docs/getting-started/', {
    accept: 'text/html, text/markdown;q=0.1',
  });
  assert.equal(htmlPreferred.status, 200);
  assert.equal(htmlPreferred.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(htmlPreferred.headers.get('Vary'), 'Accept-Encoding, Accept');

  const htmlFirst = await negotiate('/docs/getting-started/', {
    accept: 'text/html, text/markdown',
  });
  assert.equal(htmlFirst.status, 200);
  assert.equal(htmlFirst.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.equal(htmlFirst.headers.get('Vary'), 'Accept-Encoding, Accept');

  assert.deepEqual(requested, []);
});

test('serves Markdown when Markdown is preferred or requested with higher specificity', async () => {
  const requested = serve({ '/docs/getting-started/index.md': '# Getting started\n' });

  const mdPreferred = await negotiate('/docs/getting-started/', {
    accept: 'text/html;q=0.5, text/markdown;q=0.8',
  });
  assert.equal(mdPreferred.status, 200);
  assert.equal(mdPreferred.headers.get('Content-Type'), 'text/markdown; charset=utf-8');
  assert.equal(mdPreferred.headers.get('Vary'), 'Accept');

  const mdFirst = await negotiate('/docs/getting-started/', {
    accept: 'text/markdown, text/html',
  });
  assert.equal(mdFirst.status, 200);
  assert.equal(mdFirst.headers.get('Content-Type'), 'text/markdown; charset=utf-8');
  assert.equal(mdFirst.headers.get('Vary'), 'Accept');

  const wildcard = await negotiate('/docs/getting-started/', {
    accept: 'text/markdown, */*',
  });
  assert.equal(wildcard.status, 200);
  assert.equal(wildcard.headers.get('Content-Type'), 'text/markdown; charset=utf-8');
  assert.equal(wildcard.headers.get('Vary'), 'Accept');

  assert.equal(requested.length, 3);
});

test('leaves files and non-directory URLs alone', async () => {
  const requested = serve({});
  for (const path of ['/llms.txt', '/docs/getting-started/index.md', '/assets/favicon.svg']) {
    assert.equal(await negotiate(path, { context: null }), undefined);
  }
  assert.deepEqual(requested, []);
});
