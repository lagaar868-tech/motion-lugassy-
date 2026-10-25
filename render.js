#!/usr/bin/env node
/*
 * Export MP4 de l'animation, image par image (rendu parfait, sans saccades).
 *
 *   node render.js                 -> out/lugassy-16x9.mp4 + out/lugassy-9x16.mp4
 *   node render.js --format 916    -> uniquement le 9:16
 *   node render.js --fps 60
 *
 * Utilise Puppeteer s'il est installé, sinon Playwright. Nécessite ffmpeg dans le PATH.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const args = process.argv.slice(2);
const arg = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const FPS = +arg('fps', 30);
const FORMATS = arg('format') ? [arg('format')] : ['169', '916'];
const ROOT = __dirname;
const OUT = path.join(ROOT, 'out');

const SIZES = { '169': [1920, 1080, 'lugassy-16x9.mp4'], '916': [1080, 1920, 'lugassy-9x16.mp4'] };
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.png': 'image/png', '.svg': 'image/svg+xml',
               '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.css': 'text/css' };

// Petit serveur local : nécessaire pour lire la couleur du logo (canvas bloqué en file://)
function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { rsp.writeHead(404); return rsp.end(); }
      rsp.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(rsp);
    }).listen(0, '127.0.0.1', () => res(srv));
  });
}

async function launch() {
  try {
    const puppeteer = require('puppeteer');
    const b = await puppeteer.launch({ headless: true });
    return { browser: b, newPage: async (w, h) => { const p = await b.newPage(); await p.setViewport({ width: w, height: h, deviceScaleFactor: 1 }); return p; } };
  } catch (e) {
    const { chromium } = require('playwright');
    const b = await chromium.launch();
    return { browser: b, newPage: (w, h) => b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 }) };
  }
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const srv = await serve();
  const port = srv.address().port;
  const { browser, newPage } = await launch();

  for (const f of FORMATS) {
    const [w, h, name] = SIZES[f];
    const page = await newPage(w, h);
    await page.goto(`http://127.0.0.1:${port}/index.html?render=1&format=${f}`, { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => window.__ready);
    const [dur, red] = await page.evaluate(() => [window.DURATION, window.__RED]);
    const frames = Math.round(dur * FPS);
    console.log(`\n▶ ${name}  ${w}x${h}  ${dur}s @ ${FPS} fps  (${frames} images)  rouge: ${red}`);

    // Voix off ajoutée automatiquement si audio/voix-off.wav existe
    const VOICE = path.join(ROOT, 'audio', 'voix-off.wav');
    const audioIn = fs.existsSync(VOICE) ? ['-i', VOICE] : [];
    const audioOut = audioIn.length ? ['-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-shortest'] : [];
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', ...audioIn,
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', ...audioOut, '-movflags', '+faststart',
      path.join(OUT, name)], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((ok, ko) => ff.on('close', c => c === 0 ? ok() : ko(new Error('ffmpeg ' + c))));

    for (let i = 0; i < frames; i++) {
      await page.evaluate(t => window.seek(t), i / FPS);
      const buf = await page.screenshot({ type: 'png' });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % FPS === 0) process.stdout.write(`\r  ${Math.round((i / frames) * 100)} %`);
    }
    ff.stdin.end();
    await done;
    process.stdout.write(`\r  100 %  → out/${name}\n`);
    await page.close();
  }

  await browser.close();
  srv.close();
})().catch(e => { console.error(e); process.exit(1); });
