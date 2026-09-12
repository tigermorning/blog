// 잠긴 글(본문이 암호화된 비공개 독서 노트)의 검색 항목을 만들어 search-data.js에 넣는다.
//
//   node scripts/add-locked-search-entry.mjs ko/generative-ai-design-patterns-ch3.html --password <비밀번호>
//
// 본문을 메모리에서만 풀어 <h1>~<h3> 제목만 뽑는다. 본문 문장은 저장하지 않는다
// (ch1·ch2 항목과 같은 형식: 제목 · 소제목 · 소제목 …).
// 비밀번호는 어디에도 기록하지 않는다.
import fs from "node:fs";
import path from "node:path";
import { webcrypto as crypto } from "node:crypto";

const PBKDF2_ITERATIONS = 250000;
const OUT_FILE = path.join(path.resolve(import.meta.dirname, ".."), "search-data.js");

const args = process.argv.slice(2);
const passIndex = args.indexOf("--password");
if (passIndex === -1 || !args[passIndex + 1]) {
  console.error(
    "사용법: node scripts/add-locked-search-entry.mjs <파일...> --password <비밀번호>"
  );
  process.exit(1);
}
const password = args[passIndex + 1];
const files = args.slice(0, passIndex);
if (!files.length) {
  console.error("대상 파일이 없습니다.");
  process.exit(1);
}

const bytes = (b64) => Buffer.from(b64, "base64");

async function decrypt(payload) {
  const baseKey = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveKey"]
  );
  const key = await crypto.subtle.deriveKey(
    {
      name: "PBKDF2",
      salt: bytes(payload.salt),
      iterations: PBKDF2_ITERATIONS,
      hash: "SHA-256",
    },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["decrypt"]
  );
  const buf = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: bytes(payload.iv) },
    key,
    bytes(payload.data)
  );
  return new TextDecoder().decode(buf);
}

const clean = (s) =>
  s
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();

function headings(html) {
  return [...html.matchAll(/<h[123][^>]*>([\s\S]*?)<\/h[123]>/g)]
    .map((m) => clean(m[1]))
    .filter(Boolean);
}

const src = fs.readFileSync(OUT_FILE, "utf8");
const eol = src.includes("\r\n") ? "\r\n" : "\n";
let written = false;
const data = JSON.parse(src.slice(src.indexOf("{"), src.lastIndexOf("}") + 1));

for (const file of files) {
  const html = fs.readFileSync(file, "utf8");
  const payloadMatch = html.match(
    /<script id="lockedPayload"[^>]*>([\s\S]*?)<\/script>/
  );
  if (!payloadMatch) {
    console.error(`잠긴 글이 아닙니다 (lockedPayload 없음): ${file}`);
    process.exitCode = 1;
    continue;
  }

  let body;
  try {
    body = await decrypt(JSON.parse(payloadMatch[1]));
  } catch {
    console.error(`비밀번호가 틀렸습니다: ${file}`);
    process.exitCode = 1;
    continue;
  }

  const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/);
  const title = titleMatch ? clean(titleMatch[1]) : "";
  // 잠금 화면 자체의 문구는 빼고, 겉면과 본문의 소제목만 모은다
  const outer = headings(html).filter((h) => h !== title && !/비밀번호/.test(h));
  const parts = [title, ...outer, ...headings(body)].filter(Boolean);
  const text = [...new Set(parts)].join(" · ");

  const key = path.basename(file);
  const before = data[key];
  data[key] = { title, text };
  written = true;
  console.log(
    `${before ? "갱신" : "추가"}: ${key} — 소제목 ${parts.length - 1}개, ${text.length}자`
  );
}

if (!written) {
  console.error("바뀐 항목이 없어 search-data.js를 그대로 뒀어요.");
  process.exit(process.exitCode ?? 1);
}

fs.writeFileSync(
  OUT_FILE,
  `const SEARCH_DATA = ${JSON.stringify(data, null, 1)};\n`.split("\n").join(eol),
  "utf8"
);
console.log(`search-data.js에 썼어요 (항목 ${Object.keys(data).length}개).`);
