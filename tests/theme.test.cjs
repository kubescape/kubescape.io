// Run with: node --test tests/theme.test.cjs (no dependencies).
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { runInNewContext } = require('node:vm');
const { test } = require('node:test');

const root = join(__dirname, '..');
const script = readFileSync(join(root, 'docs/javascripts/theme.js'), 'utf8');
const bootstrap = readFileSync(join(root, 'overrides/partials/javascripts/palette.html'), 'utf8')
  .match(/<script>([\s\S]*?)<\/script>/)[1]
  .replace('{{ config.theme.palette | tojson }}', JSON.stringify([
    { scheme: 'default' }, { scheme: 'slate' }
  ]));

// Two independent documents share storage, as browser tabs do. The palette
// change stub mirrors Material 9.2.7's body update and __palette storage write.
function openTab(storage, dark = false) {
  const listeners = {};
  const attributes = {};
  const body = {
    dataset: {},
    setAttribute(name, value) {
      if (name === 'data-md-color-scheme') this.dataset.mdColorScheme = value;
    }
  };
  const system = {
    matches: dark,
    addEventListener(type, callback) { listeners.system = callback; }
  };
  const button = {
    setAttribute(name, value) { attributes[name] = value; },
    addEventListener(type, callback) { listeners.click = callback; }
  };
  const palette = {
    querySelector(selector) {
      const scheme = selector.match(/="(.*?)"/)[1];
      return {
        dispatchEvent() {
          body.dataset.mdColorScheme = scheme;
          storage.set('__palette', { index: scheme === 'slate' ? 1 : 0, color: { scheme } });
        }
      };
    }
  };
  const context = {
    document: {
      body,
      querySelector: selector => selector === '[data-theme-toggle]' ? button : palette,
      addEventListener(type, callback) { listeners.ready = callback; }
    },
    matchMedia: () => system,
    __md_get: key => storage.get(key) ?? null,
    __md_set: (key, value) => storage.set(key, value),
    Event: class {}
  };
  runInNewContext(bootstrap, context);
  runInNewContext(script, context);
  return {
    ready: () => listeners.ready(),
    click: () => listeners.click(),
    scheme: () => body.dataset.mdColorScheme,
    label: () => attributes['aria-label'],
    systemChange(dark) { system.matches = dark; listeners.system(); }
  };
}

for (const chosen of ['default', 'slate']) {
  test(`a stale automatic tab preserves a shared manual ${chosen} choice across refresh`, async () => {
    const storage = new Map();
    const a = openTab(storage);
    const b = openTab(storage);
    a.ready();
    b.ready();
    await b.click();
    if (chosen === 'default') await b.click();
    assert.equal(storage.get('__palette_manual'), true);
    a.systemChange(chosen === 'default');
    assert.equal(storage.get('__palette').color.scheme, chosen);
    const refreshed = openTab(storage, chosen === 'default');
    refreshed.ready();
    assert.equal(refreshed.scheme(), chosen);
    assert.equal(refreshed.label(), chosen === 'default' ? 'Switch to dark mode' : 'Switch to light mode');
  });
}

test('initial reconciliation respects a choice saved by another tab during loading', async () => {
  const storage = new Map();
  const loading = openTab(storage);
  const active = openTab(storage);
  active.ready();
  await active.click();
  loading.ready();
  assert.equal(storage.get('__palette').color.scheme, 'slate');
});

test('without a manual choice, automatic tabs still follow system changes', () => {
  const storage = new Map();
  const tab = openTab(storage);
  tab.ready();
  tab.systemChange(true);
  assert.equal(tab.scheme(), 'slate');
  tab.systemChange(false);
  assert.equal(tab.scheme(), 'default');
  assert.equal(storage.has('__palette_manual'), false);
});
