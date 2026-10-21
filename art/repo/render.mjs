// Renders the SVGs made by make_repo_art.py to PNG with Chromium (Playwright).
// Usage: node render.mjs [file.svg ...]   (default: every *.svg in this folder)
import { createRequire } from 'node:module';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
// require() honours NODE_PATH, so a globally installed Playwright works too.
const { chromium } = createRequire(import.meta.url)('playwright');
const files = process.argv.slice(2).length ? process.argv.slice(2)
  : readdirSync(here).filter(f => f.endsWith('.svg'));
// Retina-sized PNGs for the README; the social preview stays at 1280x640.
const scale = f => (f.startsWith('social-preview') || f.startsWith('avatar') ? 1 : 2);

const browser = await chromium.launch();
for (const f of files) {
  const svg = readFileSync(join(here, f), 'utf8');
  const [, w, h] = svg.match(/width="([\d.]+)" height="([\d.]+)"/);
  const page = await browser.newPage({ viewport: { width: Math.ceil(+w), height: Math.ceil(+h) }, deviceScaleFactor: scale(f) });
  await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await page.locator('svg').first().screenshot({ path: join(here, f.replace(/\.svg$/, '.png')), omitBackground: true });
  await page.close();
  console.log(f.replace(/\.svg$/, '.png'));
}
await browser.close();
