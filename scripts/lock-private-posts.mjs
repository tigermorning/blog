/**
 * 비공개 독서노트의 본문을 AES-GCM으로 암호화해 HTML에 넣는다.
 *
 *   node scripts/lock-private-posts.mjs <파일...> --password <비밀번호>
 *
 * <div class="page" id="pageContent"> 부터 </body> 직전까지를 통째로 암호화한다.
 * 본문에 딸린 <script>(사이드 목차·슬라이더·복사 버튼 등)도 함께 들어가므로,
 * 복호화 뒤 다시 실행해 준다.
 *
 * 비밀번호는 파일에 저장하지 않는다. 틀린 비밀번호는 AES-GCM 인증 태그가
 * 검증에 실패하면서 걸러진다 — 별도 검증값을 둘 필요가 없다.
 */
import fs from "node:fs";
import { webcrypto as crypto } from "node:crypto";

const PBKDF2_ITERATIONS = 250000;
const START_MARK = '<div class="page" id="pageContent"';
const END_MARK = "</body>";

const args = process.argv.slice(2);
const passIndex = args.indexOf("--password");
if (passIndex === -1 || !args[passIndex + 1]) {
  console.error("사용법: node scripts/lock-private-posts.mjs <파일...> --password <비밀번호>");
  process.exit(1);
}
const password = args[passIndex + 1];
const files = args.slice(0, passIndex);
if (!files.length) {
  console.error("암호화할 파일이 없습니다.");
  process.exit(1);
}

const b64 = (buf) => Buffer.from(buf).toString("base64");

async function encrypt(plaintext) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const baseKey = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveKey"]
  );
  const key = await crypto.subtle.deriveKey(
    { name: "PBKDF2", salt, iterations: PBKDF2_ITERATIONS, hash: "SHA-256" },
    baseKey,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt"]
  );
  const cipher = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    key,
    new TextEncoder().encode(plaintext)
  );
  return { salt: b64(salt), iv: b64(iv), data: b64(cipher) };
}

function unlockScript(payload) {
  return `
  <script id="lockedPayload" type="application/json">${JSON.stringify(payload)}</script>
  <script>
  (function(){
    var KEY = "unlocked-book-agent-era-ai-system-design"; // 이 책 전체가 공유하는 키 — 장마다 다시 안 물어봄
    var ITER = ${PBKDF2_ITERATIONS};
    var payload = JSON.parse(document.getElementById("lockedPayload").textContent);
    var opened = false;

    function bytes(b64){
      var bin = atob(b64), out = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
      return out;
    }

    function decrypt(pass){
      var enc = new TextEncoder();
      return crypto.subtle.importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"])
        .then(function(base){
          return crypto.subtle.deriveKey(
            { name: "PBKDF2", salt: bytes(payload.salt), iterations: ITER, hash: "SHA-256" },
            base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
        })
        .then(function(key){
          return crypto.subtle.decrypt(
            { name: "AES-GCM", iv: bytes(payload.iv) }, key, bytes(payload.data));
        })
        .then(function(buf){ return new TextDecoder().decode(buf); });
    }

    // innerHTML로 넣은 <script>는 실행되지 않으므로 다시 만들어 붙인다.
    function runScripts(root){
      var list = Array.prototype.slice.call(root.querySelectorAll("script"));
      list.forEach(function(old){
        var s = document.createElement("script");
        if (old.src) { s.src = old.src; } else { s.textContent = old.textContent; }
        old.parentNode.replaceChild(s, old);
      });
    }

    function reveal(html){
      if (opened) return;
      opened = true;
      var holder = document.createElement("div");
      holder.innerHTML = html;
      var page = holder.querySelector("#pageContent");
      if (page) page.style.display = "";
      while (holder.firstChild) document.body.appendChild(holder.firstChild);
      runScripts(document.body);
      var gate = document.getElementById("lockGate");
      if (gate) gate.parentNode.removeChild(gate);
    }

    function tryPass(pass, onFail){
      decrypt(pass).then(function(html){
        try { sessionStorage.setItem(KEY, pass); } catch(e){}
        reveal(html);
      }).catch(function(){ if (onFail) onFail(); });
    }

    document.addEventListener("DOMContentLoaded", function(){
      var saved = null;
      try { saved = sessionStorage.getItem(KEY); } catch(e){}
      if (saved) tryPass(saved);

      function submit(){
        var v = document.getElementById("lockInput").value;
        tryPass(v, function(){
          document.getElementById("lockError").style.display = "block";
        });
      }
      document.getElementById("lockBtn").addEventListener("click", submit);
      document.getElementById("lockInput").addEventListener("keydown", function(ev){
        if (ev.key === "Enter") submit();
      });
    });
  })();
  </script>
`;
}

let failed = false;
for (const file of files) {
  const html = fs.readFileSync(file, "utf8");

  if (html.includes('id="lockedPayload"')) {
    console.log(`건너뜀 (이미 암호화됨): ${file}`);
    continue;
  }

  const start = html.indexOf(START_MARK);
  const end = html.lastIndexOf(END_MARK);
  if (start === -1 || end === -1 || end < start) {
    console.error(`실패: ${file} — pageContent 또는 </body>를 찾지 못했습니다.`);
    failed = true;
    continue;
  }

  const head = html.slice(0, start);
  const body = html.slice(start, end);
  const tail = html.slice(end);

  // 기존 평문 잠금 스크립트(PASS가 그대로 적혀 있던 것)를 걷어낸다.
  const cleanedHead = head.replace(
    /\n?\s*<script>\s*\(function\(\)\{\s*var PASS = [\s\S]*?<\/script>\n?/,
    "\n"
  );
  if (cleanedHead === head) {
    console.error(`실패: ${file} — 기존 잠금 스크립트를 찾지 못했습니다.`);
    failed = true;
    continue;
  }
  if (/var PASS\s*=/.test(cleanedHead)) {
    console.error(`실패: ${file} — 평문 비밀번호가 남아 있습니다.`);
    failed = true;
    continue;
  }

  const payload = await encrypt(body);
  const out = cleanedHead + unlockScript(payload) + tail;
  fs.writeFileSync(file, out);

  console.log(
    `${file}\n   평문 ${body.length.toLocaleString()}자 → 암호문 ${payload.data.length.toLocaleString()}자` +
      `  |  파일 ${html.length.toLocaleString()} → ${out.length.toLocaleString()}바이트`
  );
}

process.exit(failed ? 1 : 0);
