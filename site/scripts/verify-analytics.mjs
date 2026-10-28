// Copyright 2026 Google LLC
// SPDX-License-Identifier: Apache-2.0

// Verify built HTML with controlled Google script responses, without telemetry.
// Build once without an ID and save its HTML, then build with G-TEST:
// npm run test:browser -- /path/to/disabled-build.html
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import puppeteer from 'puppeteer-core';

const enabled = await readFile(new URL('../dist/index.html', import.meta.url), 'utf8');
assert.ok(process.argv[2], 'Pass the HTML from the build without an analytics ID');
const disabled = await readFile(process.argv[2], 'utf8');
const browser = await puppeteer.launch({ channel: 'chrome', executablePath: process.env.CHROME_PATH });
const results = [];

async function visit(host, { failed = false, html = enabled } = {}) {
  const page = await browser.newPage();
  const requests = [];
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.setRequestInterception(true);
  page.on('request', request => {
    const url = new URL(request.url());
    let body = '';
    let contentType = 'text/plain';
    if (url.hostname === 'www.gstatic.com' || url.hostname === 'www.googletagmanager.com') {
      requests.push(request.url());
      if (url.pathname.endsWith('cookienotificationbar.min.js')) {
        if (failed) return void request.abort('failed');
        contentType = 'application/javascript';
        body = `window.__cookieScriptLoaded = true;
          window.__finishConsent = () => {
            window.dataLayer.unshift(['consent', 'update', { analytics_storage: 'granted' }]);
            window.__consentInitialized = true;
            window.glueCookieNotificationBarLoaded();
          };`;
      } else if (url.hostname === 'www.googletagmanager.com') {
        contentType = 'application/javascript';
        body = `window.__gaInitializedAfterConsent = window.__consentInitialized === true;
          window.__gaCommands = Array.from(window.dataLayer, args => Array.from(args));`;
      } else {
        contentType = 'text/css';
      }
    } else if (request.isNavigationRequest() && request.frame() === page.mainFrame()) {
      contentType = 'text/html';
      body = html;
    }
    // Respond to every request; nothing reaches Google or another network host.
    void request.respond({ status: 200, contentType, body });
  });
  await page.goto(`https://${host}/?private=secret&utm_source=test#private`, { waitUntil: 'load' });
  const gaRequests = () => requests.filter(url => new URL(url).hostname === 'www.googletagmanager.com');
  return { page, requests, gaRequests, errors };
}

try {
  const delayed = await visit('egm.dev');
  assert.equal(await delayed.page.evaluate(() => window.__cookieScriptLoaded), true);
  assert.equal(delayed.gaRequests().length, 0, 'GA must not load before asynchronous configuration completes');
  assert.equal(await delayed.page.evaluate(() => window.dataLayer.some(args => args[0] === 'config')), false);
  await delayed.page.evaluate(() => window.__finishConsent());
  await delayed.page.waitForFunction(() => window.__gaCommands !== undefined);
  assert.equal(delayed.gaRequests().length, 1);
  assert.equal(await delayed.page.evaluate(() => window.__gaInitializedAfterConsent), true);
  const config = await delayed.page.evaluate(() => window.__gaCommands.find(args => args[0] === 'config')[2]);
  assert.equal(config.page_location, 'https://egm.dev/?utm_source=test');
  assert.equal(config.allow_google_signals, false);
  assert.equal(config.allow_ad_personalization_signals, false);
  results.push({ case: 'delayed configuration', pass: true, requests: [...delayed.requests] });

  await delayed.page.evaluate(() => { window.__finishConsent(); window.__finishConsent(); });
  assert.equal(await delayed.page.evaluate(() => document.querySelectorAll('script[src*="googletagmanager.com"]').length), 1);
  assert.equal(await delayed.page.evaluate(() => window.dataLayer.filter(args => args[0] === 'config').length), 1);
  assert.deepEqual(delayed.errors, []);
  results.push({ case: 'repeated callbacks', pass: true });
  await delayed.page.close();

  const failure = await visit('egm.dev', { failed: true });
  assert.equal(failure.gaRequests().length, 0);
  assert.equal(await failure.page.evaluate(() => window.dataLayer.some(args => args[0] === 'config')), false);
  assert.deepEqual(failure.errors, []);
  results.push({ case: 'cookie script failure', pass: true });
  await failure.page.close();

  for (const [host, html] of [['preview.example.com', enabled], ['localhost', enabled], ['egm.dev', disabled]]) {
    const gated = await visit(host, { html });
    assert.equal(gated.requests.length, 0);
    assert.equal(await gated.page.evaluate(() => window.dataLayer === undefined), true);
    assert.deepEqual(gated.errors, []);
    results.push({ case: host === 'egm.dev' ? 'measurement ID unset' : `noncanonical ${host}`, pass: true });
    await gated.page.close();
  }
  console.log(JSON.stringify({ browser: await browser.version(), googleResponses: 'intercepted fixtures; no live vendor verification', results }, null, 2));
} finally {
  await browser.close();
}
