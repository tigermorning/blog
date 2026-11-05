// 교안 시각화(HTML)를 헤드리스 Chrome으로 열어 조작하며 화면을 찍고 mp4로 만든다. 설치 없이 CDP(WebSocket)만 쓴다.
// 사용: node record_frames.mjs <step03|step05|step07> <html 경로> <출력 mp4>
import { spawn, execFileSync } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';

const [, , name, htmlPath, outMp4] = process.argv;
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9333 + Math.floor(Math.random() * 300);
const W = 1000, H = Number(process.env.H || 860);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'rec-'));
const profile = path.join(tmp, 'profile');
const framesDir = path.join(tmp, 'frames');
fs.mkdirSync(framesDir);

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', `--window-size=${W},${H}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let target;
for (let i = 0; i < 60 && !target; i++) {
  try { const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); target = list.find(t => t.type === 'page'); } catch {}
  if (!target) await sleep(300);
}
if (!target) { chrome.kill(); throw new Error('chrome did not start'); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let seq = 0; const pending = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise(res => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result && r.result.result && r.result.result.value; };

await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
await send('Page.enable');
await send('Page.navigate', { url: 'file:///' + htmlPath.replace(/\\/g, '/') });
await sleep(2500);

// 화면 찍기 루프
const stamps = []; let recording = true; let n = 0; let lastB64 = '', sameSince = Date.now();
const cap = (async () => {
  while (recording) {
    const t = Date.now();
    const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 82 });
    const b64 = r.result && r.result.data;
    if (b64) {
      if (b64 !== lastB64) { lastB64 = b64; sameSince = Date.now(); }
      const f = path.join(framesDir, `f${String(n).padStart(5, '0')}.jpg`);
      fs.writeFileSync(f, Buffer.from(b64, 'base64')); stamps.push([f, t]); n++;
    }
    await sleep(Math.max(0, 100 - (Date.now() - t)));
  }
})();
const hold = ms => sleep(ms);
// 화면이 stableMs 동안 안 바뀌면 끝난 것으로 본다(최대 maxMs)
const settle = async (stableMs = 2200, maxMs = 40000) => { const t0 = Date.now(); while (Date.now() - t0 < maxMs) { if (Date.now() - sameSince > stableMs) return; await sleep(200); } };
const click = sel => ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});if(!e)return 'nf';e.click();return 'ok'})()`);
const setRange = async (id, from, to, step, gap = 90) => {
  const dir = to >= from ? 1 : -1;
  for (let v = from; dir * (to - v) >= 0; v += dir * step) {
    await ev(`(()=>{const e=document.getElementById(${JSON.stringify(id)});const set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;set.call(e,${v});e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}))})()`);
    await sleep(gap);
  }
};

const scenarios = {
  async step03() {
    await hold(2500);
    await setRange('free', 10, 3, 1); await hold(2500);
    await setRange('free', 3, 1, 1); await hold(2500);
    await setRange('free', 1, 10, 1); await hold(1200);
    await setRange('price', 1000, 2000, 100); await hold(2500);
    await setRange('price', 2000, 1000, 100); await hold(1200);
    await setRange('conv', 5, 12, 1); await hold(2500);
  },
  async step05() {
    await hold(2000);
    await click('#play'); await sleep(800); await settle();
    await click('[data-s="tamper"]'); await hold(1500);
    await click('#reset'); await hold(500);
    await click('#play'); await sleep(800); await settle();
    await hold(1500);
  },
  async step07() {
    await hold(2000);
    for (const s of ['refresh', 'lost', 'race']) {
      await click(`[data-s="${s}"]`); await hold(1000);
      await click('#play'); await sleep(800); await settle();
      await hold(1200);
    }
    // 장치를 끄고 다시: 동시 도착에서 관문 ①②를 끄면 어떻게 되는지
    await click('[data-s="race"]'); await hold(800);
    await click('#t-status'); await hold(600); await click('#t-ledger'); await hold(1000);
    await click('#play'); await sleep(800); await settle(); await hold(1500);
  },
};
await scenarios[name]();
recording = false; await cap;
ws.close(); chrome.kill();

// 프레임 → mp4 (찍은 시각 간격 그대로)
let list = '';
for (let i = 0; i < stamps.length; i++) {
  const d = i < stamps.length - 1 ? (stamps[i + 1][1] - stamps[i][1]) / 1000 : 2.0;
  list += `file '${stamps[i][0].replace(/\\/g, '/')}'\nduration ${d.toFixed(3)}\n`;
}
list += `file '${stamps[stamps.length - 1][0].replace(/\\/g, '/')}'\n`;
const lf = path.join(tmp, 'list.txt'); fs.writeFileSync(lf, list);
execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lf, '-vf', `fps=10,scale=${W}:${H - (H % 2)},format=yuv420p`, '-c:v', 'libx264', '-crf', '29', '-movflags', '+faststart', outMp4]);
console.log(name, 'frames', n, 'out', outMp4, fs.statSync(outMp4).size);
// 임시 폴더는 시스템 임시 위치라 그대로 둔다
