// 핵심 요약 영역(한 줄 정의 .one-liner, 이 글을 읽기 전에 .why-read, meta/og description, «핵심 한 줄»)에 비유·감정 표현이 들어갔는지 검사한다.
// 사용: node scripts/check-summary-wording.mjs [파일...]   (인자가 없으면 ko·en·zh 의 모든 글)
// 걸리면 종료 코드 1. 정말 문제없는 관용 표현은 아래 ALLOW 에 «파일:문구»로 적고 이유를 남긴다(2026-11-09 사용자 지정 규칙).
import fs from 'fs';
import path from 'path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1')), '..');
const BAN = [
  [/아프게|아프고|아픈 |아픔|아파요/, '몸·감정 비유(아프다)는 «영향이 크다» 같은 직설로'],
  [/겹의 체|체로 거르/, '«체» 비유 대신 «단계의 검사»처럼'],
  [/문을 (닫|열|잠)|입구를 열|잠근다/, '문 비유 대신 실제 동작(막는다·허용한다)으로'],
  [/열쇠/, '«열쇠» 비유 대신 키·개인키·비밀 문자열처럼(한 줄 정의·description 에서만 검사)', ['한 줄 정의', 'description']],
  [/시간표에 올|예선|쥔 관리자|먹일수록|밑바닥/, '비유 대신 실제 동작으로'],
  [/손님|사장님|요리사|주방|요리|셰프|레시피|주문서|공정표|동선표|밀키트|조리|(?<![가-힣])도마|부엌|시식/, '요약 영역에는 비유 무대(식당)를 쓰지 않고 실제 대상(사용자·개발자·서버)으로'],
  [/세 겹|일곱 겹/, '«겹» 비유 대신 «단계»로'],
];
const ALLOW = [
  // 'domain-expertise-ai-era-asset.html:진짜 아픈 문제' — 사업 용어 «아픈 문제(pain point)»를 풀어 쓴 관용 표현이라 허용
  'domain-expertise-ai-era-asset.html:아픈 문제',
];
const clean = (t) => t.replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, ' ').replace(/\s+/g, ' ').trim();
const files = process.argv.slice(2).length ? process.argv.slice(2)
  : ['ko', 'en', 'zh'].flatMap((d) => fs.readdirSync(path.join(root, d)).filter((f) => f.endsWith('.html')).map((f) => path.join(root, d, f)));
let bad = 0;
for (const f of files) {
  const s = fs.readFileSync(f, 'utf8');
  const parts = [];
  for (const m of s.matchAll(/<p class="one-liner"[^>]*>([\s\S]*?)<\/p>/g)) parts.push(['한 줄 정의', clean(m[1])]);
  for (const m of s.matchAll(/<div class="why-read">([\s\S]*?)<\/div>/g)) for (const li of m[1].matchAll(/<li[^>]*>([\s\S]*?)<\/li>/g)) parts.push(['읽기 전에 박스', clean(li[1])]);
  // «핵심 한 줄»(비유 절 끝 문단)도 직설로 — 파이썬 스터디(beginner-python-*)는 건드리지 않기로 한 방침이라 제외
  if (!/beginner-python/.test(f)) for (const m of s.matchAll(/<p><strong>핵심 한 줄:?<\/strong>:?([\s\S]*?)<\/p>/g)) parts.push(['핵심 한 줄', clean(m[1])]);
  for (const m of s.matchAll(/<meta (?:name="description"|property="og:description") content="([^"]*)"/g)) parts.push(['description', clean(m[1])]);
  for (const [where, text] of parts) for (const [re, why, only] of BAN) {
    if (only && !only.includes(where)) continue;
    const hit = text.match(re);
    if (hit && !ALLOW.some((a) => { const [fn, sn] = a.split(':'); return f.endsWith(fn) && text.includes(sn); })) {
      bad++; console.log(`${path.relative(root, f)} [${where}] «${hit[0]}» — ${why}\n    ${text.slice(0, 120)}`);
    }
  }
}
// 본문 어디서든: 오해 근거 없는 부정 머리말
for (const f of files) { const s = fs.readFileSync(f, 'utf8'); if (/서로 바꿔 쓰는 (방법|방식)이 아니라/.test(s)) { bad++; console.log(`${path.relative(root, f)} [본문] «서로 바꿔 쓰는 … 아니라» — 긍정문으로(순서·단계를 직접 말한다)`); } }
console.log(bad ? `\n${bad}건 걸림` : '통과: 핵심 요약 영역에 금지 표현 없음');
process.exit(bad ? 1 : 0);
