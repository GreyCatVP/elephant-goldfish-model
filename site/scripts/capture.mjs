// Copyright 2026 Google LLC.
// SPDX-License-Identifier: Apache-2.0

// Regenerates every committed site image: public/og.png and screenshots/*.png.
// Usage: npm run capture   (builds first, then serves dist/ and drives Chrome).
// Uses puppeteer-core, so it needs a local Chrome: set CHROME_PATH if it is not found.

import { createServer } from 'node:http';
import { existsSync } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const site = fileURLToPath(new URL('..', import.meta.url));
const dist = join(site, 'dist');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };

// /src/** and /scripts/** come from the site source (for the og template); everything else from dist/.
const server = createServer(async (req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname));
  const root = /^\/(src|scripts)\//.test(path) ? site : dist;
  const file = join(root, path.endsWith('/') ? `${path}index.html` : path);
  try {
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': types[extname(file)] ?? 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404).end();
  }
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}`;

const chrome = [
  process.env.CHROME_PATH,
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].find((p) => p && existsSync(p));
if (!chrome) throw new Error('Chrome not found. Set CHROME_PATH.');
const browser = await puppeteer.launch({ executablePath: chrome, args: ['--no-sandbox'] });

async function capture({ url, out, width, height, scheme = 'light', fullPage = false }) {
  const page = await browser.newPage();
  await page.setViewport({ width, height });
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: scheme }]);
  await page.goto(base + url, { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(site, out), fullPage });
  await page.close();
  console.log(`wrote ${out}`);
}

try {
  await capture({ url: '/scripts/og.html', out: 'public/og.png', width: 1200, height: 630 });
  await capture({ url: '/', out: 'screenshots/hero-light.png', width: 1200, height: 600 });
  await capture({ url: '/', out: 'screenshots/hero-dark.png', width: 1200, height: 600, scheme: 'dark' });
  await capture({ url: '/', out: 'screenshots/full-light.png', width: 1000, height: 800, fullPage: true });
  await capture({ url: '/', out: 'screenshots/mobile.png', width: 375, height: 812 });
} finally {
  await browser.close();
  server.close();
}
