const assert = require('node:assert/strict');
const { join } = require('node:path');
const { pathToFileURL } = require('node:url');
const { test } = require('node:test');

const edgeFunction = import(pathToFileURL(join(__dirname, '..', 'netlify/edge-functions/markdown.js')));

// Stand in for the site's static files; record which URLs the function reads.
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

function negotiate(path) {
  return edgeFunction.then(({ default: handler }) =>
    handler(new Request('https://kubescape.io' + path, { headers: { Accept: 'text/markdown' } })));
}

test('runs only for requests that accept text/markdown, and fails open', async () => {
  const { config } = await edgeFunction;
  assert.equal(config.path, '/*');
  assert.deepEqual(config.header, { accept: 'text/markdown' });
  assert.equal(config.onError, 'bypass');
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

test('falls back to HTML when a page has no Markdown copy', async () => {
  serve({});
  assert.equal(await negotiate('/blog/archive/2024/08/'), undefined);
});

test('leaves files and non-directory URLs alone', async () => {
  const requested = serve({});
  for (const path of ['/llms.txt', '/docs/getting-started/index.md', '/assets/favicon.svg']) {
    assert.equal(await negotiate(path), undefined);
  }
  assert.deepEqual(requested, []);
});
