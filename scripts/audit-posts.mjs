// ko/*.html 글을 WRAP UP 과제의 "블로그 작성 시 주의할 점" 기준으로 잰다.
//
//   node scripts/audit-posts.mjs            표 출력 (본문 길이 순)
//   node scripts/audit-posts.mjs --csv      CSV 출력
//
// 재는 것 (판정은 사람이 한다 — 숫자는 후보를 고르는 용도):
//   chars     <main> 본문 글자 수 (build-search-data.mjs와 같은 추출 규칙)
//   visuals   표·그림·SVG·이미지·코드·퀴즈/박스 등 줄글이 아닌 블록 수
//   maxRun    시각 요소 없이 연속된 <p> 문단의 최대 개수 (줄글만 이어지는 구간)
//   pPerVis   문단 수 / (visuals+1)
//   lockedOrNoMain  <main>이 없음 (암호 글 등) — 손대지 말 것
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const POSTS_DIR = path.join(ROOT, "ko");
const SKIP = new Set([
  "index.html",
  "posts.html",
  "start.html",
  "topic-map.html",
  "big-map.html",
  "_sidebar.html",
]);

const VISUAL = /<(table|figure|svg|img|pre|details|ol|ul|blockquote)\b|class="[^"]*(box|quiz|card|diagram|stepper|callout)[^"]*"/gi;

function measure(html) {
  const main = html.match(/<main>([\s\S]*?)<\/main>/);
  if (!main) return null;
  const body = main[1];
  const text = body.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const visuals = (body.match(VISUAL) || []).length;
  const paras = (body.match(/<p\b/gi) || []).length;
  // 최상위 흐름에서 <p>가 시각 요소 없이 몇 번 연속되는지
  const tokens = body.match(/<p\b|<(table|figure|svg|img|pre|details|ol|ul|blockquote|h2|h3)\b|class="[^"]*(box|quiz|card|diagram|stepper|callout)[^"]*"/gi) || [];
  let run = 0;
  let maxRun = 0;
  for (const t of tokens) {
    if (/^<p\b/i.test(t)) {
      run++;
      maxRun = Math.max(maxRun, run);
    } else run = 0;
  }
  return { chars: text.length, visuals, paras, maxRun, pPerVis: +(paras / (visuals + 1)).toFixed(1) };
}

const rows = [];
for (const f of fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith(".html") && !SKIP.has(f)).sort()) {
  const html = fs.readFileSync(path.join(POSTS_DIR, f), "utf8");
  const m = measure(html);
  const title = (html.match(/<title>([\s\S]*?)<\/title>/) || [, ""])[1].trim();
  rows.push(m ? { file: f, title, ...m } : { file: f, title, lockedOrNoMain: true });
}

rows.sort((a, b) => (b.chars || 0) - (a.chars || 0));
if (process.argv.includes("--csv")) {
  console.log("file,chars,visuals,paras,maxRun,pPerVis,lockedOrNoMain,title");
  for (const r of rows)
    console.log([r.file, r.chars ?? "", r.visuals ?? "", r.paras ?? "", r.maxRun ?? "", r.pPerVis ?? "", r.lockedOrNoMain ? 1 : "", JSON.stringify(r.title)].join(","));
} else {
  for (const r of rows)
    console.log(r.lockedOrNoMain ? `LOCKED  ${r.file}` : `${String(r.chars).padStart(6)}  vis=${String(r.visuals).padStart(3)}  p=${String(r.paras).padStart(3)}  run=${String(r.maxRun).padStart(2)}  ${r.file}`);
}
