// «맥락 없는 내용» 후보를 찾는다(후보만 알려 줌 — 사람이 글을 읽고 판단한다. 2026-11-09 사용자 지정 규칙).
//  A. 각주가 달린 용어가 각주 번호 위치보다 먼저 박스·한 줄 정의 등에서 쓰였는가(정의 전에 사용)
//  B. 비유 절(#analogy 또는 «비유» 제목) 안의 «아니/그게/그럼/그러면/그래도/그런데»로 시작하는 따옴표 대사(앞 장면 없는 대사 후보)
//  C. 독자가 못 보는 출처에 기대는 말(강의에서·가이드대로·강의 자료·교안)
// 사용: node scripts/check-context.mjs [파일...]   (인자가 없으면 ko 의 모든 글, beginner-python-* 제외)
import fs from 'fs';
import path from 'path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..');
const files = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(path.join(root, 'ko')).filter((f) => f.endsWith('.html') && !f.startsWith('beginner-python')).map((f) => path.join(root, 'ko', f));
const clean = (t) => t.replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, ' ').replace(/\s+/g, ' ').trim();
let n = 0;
const out = (f, kind, msg) => { n++; console.log(`${path.relative(root, f)} [${kind}] ${msg}`); };
for (const f of files) {
  const s = fs.readFileSync(f, 'utf8');
  const m0 = s.indexOf('<main>'); if (m0 < 0) continue;
  let body = s.slice(m0, s.indexOf('</main>'));
  const fnStart = body.indexOf('<section class="footnotes">');
  const main = fnStart > 0 ? body.slice(0, fnStart) : body;
  // A. 각주 용어의 첫 사용 위치 vs 각주 번호 위치
  for (const li of body.matchAll(/<li id="fn(\d+)">([\s\S]*?)<\/li>/g)) {
    const term = clean(li[2]).split(/ — | - /)[0].replace(/[()]/g, '').trim();
    if (term.length < 2 || term.length > 14) continue;
    const refAt = main.indexOf(`id="fnref${li[1]}"`);
    if (refAt < 0) continue;
    const pre = clean(main.slice(0, main.lastIndexOf('<sup', refAt)));
    const firstUse = pre.indexOf(term);
    if (firstUse >= 0 && firstUse < pre.length - term.length - 1) out(f, '정의 전 사용 후보', `«${term}»가 각주 ${li[1]} 앞에서 이미 쓰임: …${pre.slice(Math.max(0, firstUse - 20), firstUse + 30)}…`);
  }
  // B. 비유 절의 맥락 없는 대사 후보
  const an = main.search(/<h2[^>]*>(?:(?!<\/h2>)[\s\S])*비유(?:(?!<\/h2>)[\s\S])*<\/h2>/);
  if (an >= 0) {
    const endAt = main.indexOf('<h2', an + 10);
    const seg = clean(main.slice(an, endAt > 0 ? endAt : undefined));
    for (const q of seg.matchAll(/["“«]\s*(아니|그게|그럼|그러면|그래도|그런데)[^"”»]{0,30}["”»]/g)) out(f, '앞 장면 없는 대사 후보', q[0]);
  }
  // C. 못 보는 출처
  for (const q of clean(main).matchAll(/(강의에서|강의 자료|강의 교안|가이드대로|교안에서)/g)) out(f, '독자가 못 보는 출처', q[0]);
}
console.log(n ? `\n후보 ${n}건 — 글을 읽고 판단하세요` : '후보 없음');
