// search-data.js를 ko/*.html에서 다시 만든다.
//
//   node scripts/build-search-data.mjs          쓰기
//   node scripts/build-search-data.mjs --check   바뀌는 항목만 보여 주고 쓰지 않음
//
// 본문 텍스트는 scripts/extract-main-text.mjs와 같은 규칙으로 뽑는다
// (<main> 안의 태그를 공백 하나로 바꾸고 공백을 접는다).
// <main>이 없는 글(암호를 걸어 둔 비공개 글)은 기존 항목을 그대로 둔다.
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const POSTS_DIR = path.join(ROOT, "ko");
const OUT_FILE = path.join(ROOT, "search-data.js");

// 글이 아니라 목록·이동용 페이지
const SKIP = new Set([
  "index.html",
  "posts.html",
  "start.html",
  "topic-map.html",
  "_sidebar.html",
]);

function extract(html) {
  const main = html.match(/<main>([\s\S]*?)<\/main>/);
  if (!main) return null;
  const text = main[1]
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
  const title = html.match(/<title>([\s\S]*?)<\/title>/);
  return { title: title ? title[1].trim() : "", text };
}

function readExisting() {
  if (!fs.existsSync(OUT_FILE)) return {};
  const src = fs.readFileSync(OUT_FILE, "utf8");
  const body = src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1);
  return JSON.parse(body);
}

const existing = readExisting();
const files = fs
  .readdirSync(POSTS_DIR)
  .filter((f) => f.endsWith(".html") && !SKIP.has(f))
  .sort();

// 기존 순서를 먼저 지키고, 새 글은 뒤에 붙인다 (diff를 작게 유지)
const order = [
  ...Object.keys(existing).filter((k) => files.includes(k)),
  ...files.filter((k) => !(k in existing)),
];

const out = {};
const added = [];
const changed = [];
const kept = [];
const dropped = Object.keys(existing).filter((k) => !files.includes(k));

for (const name of order) {
  const entry = extract(fs.readFileSync(path.join(POSTS_DIR, name), "utf8"));
  if (!entry) {
    // <main>이 없는 글: 손으로 적어 둔 기존 항목을 그대로 둔다
    if (existing[name]) {
      out[name] = existing[name];
      kept.push(name);
    } else {
      console.warn(`건너뜀 (<main> 없음, 기존 항목도 없음): ${name}`);
    }
    continue;
  }
  out[name] = entry;
  const before = existing[name];
  if (!before) added.push(name);
  else if (before.title !== entry.title || before.text !== entry.text)
    changed.push(name);
}

const report = (label, list) =>
  list.length && console.log(`${label} ${list.length}건\n  ${list.join("\n  ")}`);
report("새로 추가:", added);
report("내용 바뀜:", changed);
report("파일이 없어져 빠짐:", dropped);
report("<main>이 없어 기존 항목 유지:", kept);
if (!added.length && !changed.length && !dropped.length)
  console.log("바뀐 항목 없음");

if (process.argv.includes("--check")) process.exit(0);

const json = JSON.stringify(out, null, 1);
const eol = fs.existsSync(OUT_FILE) && fs.readFileSync(OUT_FILE, "utf8").includes("\r\n") ? "\r\n" : "\n";
fs.writeFileSync(
  OUT_FILE,
  (`const SEARCH_DATA = ${json};\n`).split("\n").join(eol),
  "utf8"
);
console.log(`\n${Object.keys(out).length}개 항목을 search-data.js에 썼어요.`);
