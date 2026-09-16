// 잠긴 독서 노트의 비밀번호를 찾아 온다.
//
//   1) --password <값>        — 그때만 쓰는 값. 가장 우선.
//   2) 환경변수 BOOK_PASSWORD  — CI나 한 번짜리 실행용.
//   3) 저장소 루트의 .env      — 평소 쓰는 경로. .gitignore에 있어 커밋되지 않는다.
//
// .env는 평문이다. 원본은 비밀번호 관리자에 따로 두고, 이 파일은 매번 타이핑하지
// 않으려는 편의 장치로만 쓴다.
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..", "..");
const ENV_FILE = path.join(ROOT, ".env");
const ENV_KEY = "BOOK_PASSWORD";

function fromEnvFile() {
  if (!fs.existsSync(ENV_FILE)) return null;
  for (const line of fs.readFileSync(ENV_FILE, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    if (trimmed.slice(0, eq).trim() !== ENV_KEY) continue;
    let value = trimmed.slice(eq + 1).trim();
    // 따옴표로 감싼 값도 받는다 — 비밀번호에 공백이나 #이 들어가면 감싸야 한다.
    if (value.length >= 2 && (value[0] === '"' || value[0] === "'") && value.at(-1) === value[0]) {
      value = value.slice(1, -1);
    }
    return value || null;
  }
  return null;
}

/**
 * argv에서 --password와 그 값을 떼어 내고, 없으면 환경변수·.env 순으로 찾는다.
 * 반환: { password, rest } — rest는 --password 쌍을 제거한 나머지 인자.
 */
export function resolvePassword(argv, usage) {
  const rest = argv.slice();
  let password = null;
  let source = null;

  const flag = rest.indexOf("--password");
  if (flag !== -1) {
    password = rest[flag + 1];
    if (!password) {
      console.error(usage);
      process.exit(1);
    }
    rest.splice(flag, 2);
    source = "--password";
  }

  if (!password && process.env[ENV_KEY]) {
    password = process.env[ENV_KEY];
    source = `환경변수 ${ENV_KEY}`;
  }
  if (!password) {
    const fromFile = fromEnvFile();
    if (fromFile) {
      password = fromFile;
      source = ".env";
    }
  }

  if (!password) {
    console.error(usage);
    console.error(`\n비밀번호를 못 찾았습니다. .env에 ${ENV_KEY}=... 를 넣거나 --password로 넘기세요.`);
    console.error("(.env.example을 복사해 쓰면 됩니다. .env는 커밋되지 않습니다.)");
    process.exit(1);
  }

  return { password, rest, source };
}
