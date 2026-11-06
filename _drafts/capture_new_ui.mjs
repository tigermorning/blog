// 도장 최신 화면(상점·추가 대화권)을 헤드리스 Chrome(CDP)으로 찍는다. 설치 없음(Node 내장 WebSocket).
// 사용: node capture_new_ui.mjs <출력 폴더> <서버 주소>
import { spawn } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';

const [, , outDir, base = 'http://127.0.0.1:8141'] = process.argv;
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9400 + Math.floor(Math.random() * 300);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'rs-new-'));
fs.mkdirSync(outDir, { recursive: true });
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', '--window-size=480,1000', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let target;
for (let i = 0; i < 60 && !target; i++) {
  try { const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); target = list.find(t => t.type === 'page'); } catch {}
  if (!target) await sleep(300);
}
if (!target) { chrome.kill(); throw new Error('chrome did not start'); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let seq = 0; const pending = new Map(); const logs = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') logs.push('exception: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
});
const send = (method, params = {}) => new Promise(res => { const id = ++seq; pending.set(id, res); ws.send(JSON.stringify({ id, method, params })); });
const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result && r.result.result && r.result.result.value; };
const shot = async name => { const r = await send('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(outDir, name), Buffer.from(r.result.data, 'base64')); console.log('saved', name); };
const go = async url => { await send('Page.navigate', { url }); await sleep(2500); };
const size = async (w, h) => send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });

await send('Page.enable'); await send('Runtime.enable');
await size(480, 960);
await go(base + '/');
await ev(`(()=>{const b=document.getElementById('introClose');if(b&&!document.getElementById('intro').hidden)b.click();return 1})()`);
await sleep(500);
console.log('header button:', await ev(`document.getElementById('crBtn').textContent`));
await shot('new-01-home-shop-button.png');

// 상점 팝업: 위쪽(대화권)과 아래쪽(일회 구매 상품)을 한 장에 담으려고 창을 길게
await size(480, 1500);
await ev(`document.getElementById('crBtn').click()`);
await sleep(900);
console.log('shop open:', await ev(`document.getElementById('crDlg').open`), '| title:', await ev(`document.getElementById('crTitle').textContent`));
await shot('new-02-shop-dialog.png');
await ev(`document.getElementById('crList').scrollIntoView({block:'center'})`);
await sleep(500);
await shot('new-02b-shop-chat-tickets.png');

// 추가 대화 100번(1,000원)을 고르면 주문을 만들고 /pay 로 간다 → 토스 결제위젯
await size(1000, 900);
await go(base + '/');
await ev(`(()=>{const b=document.getElementById('introClose');if(b&&!document.getElementById('intro').hidden)b.click();return 1})()`);
await size(480, 1500);
await ev(`document.getElementById('crBtn').click()`);
await sleep(700);
await ev(`document.querySelector('#crList .crprod, #crList button, #crList [data-id]').click()`);
await sleep(4500);
await size(1000, 900);
await sleep(1500);
console.log('pay url:', await ev('location.pathname'), '| status:', await ev(`(document.getElementById('status')||{}).textContent`));
await shot('new-03-pay-widget-chat-tickets.png');

fs.writeFileSync(path.join(outDir, 'console-new.txt'), logs.join('\n') + '\n');
ws.close(); chrome.kill();
