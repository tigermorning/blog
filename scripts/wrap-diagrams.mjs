/**
 * 본문 인라인 SVG를 .diagram-scroll 로 감싸고 폰용 최소 폭을 계산해 붙인다.
 *
 *   node scripts/wrap-diagrams.mjs ko en zh        # 감싸고 값 갱신
 *   node scripts/wrap-diagrams.mjs --check ko      # 바꿀 게 있는지만 확인
 *
 * SVG는 width/height 없이 viewBox만 주기 때문에 컨테이너 폭에 맞춰 줄어든다.
 * 데스크톱에선 그게 맞지만, 폰에서는 본문이 340px 남짓이라 viewBox 640~1150
 * 짜리 그림이 절반 이하로 찌그러지고 그림 안 글자가 6~8px가 되어 못 읽는다.
 *
 * 그래서 그림마다 "글자가 11px 밑으로 안 내려가는 최소 폭"을 계산해
 * --diagram-min 으로 박아 두고, style.css가 폰에서 그만큼 폭을 확보한 뒤
 * 넘치는 만큼 옆으로 밀어서 보게 한다.
 *
 * 새 글을 쓰고 나면 그냥 다시 돌리면 된다 — 이미 감싼 그림은 값만 다시
 * 맞추고, 안 바뀌면 파일을 건드리지 않는다.
 */
import fs from "node:fs";
import path from "node:path";

const TARGET_FS = 11;   // 폰에서 보장할 그림 속 최소 글자 크기(px)
const MIN_W = 480;      // 이보다 좁게는 안 잡는다
const MAX_W = 960;      // 이보다 넓으면 미는 거리가 너무 길어진다

const args = process.argv.slice(2);
const check = args.includes("--check");
const dirs = args.filter((a) => !a.startsWith("--"));
if (!dirs.length) {
  console.error("사용법: node scripts/wrap-diagrams.mjs [--check] <폴더...>");
  process.exit(1);
}

/** 파일 전체의 <style> 블록에서 `.클래스 { font-size: N }` 을 모은다.
    SVG 안에서 쓰는 클래스가 페이지 <style>에 정의된 경우가 있어서,
    SVG 블록만 훑으면 실제보다 큰 글자 크기로 잘못 계산하게 된다. */
function classFontSizes(html) {
  const sizes = new Map();
  for (const style of html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
    for (const rule of style[1].matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
      const fs = rule[2].match(/font-size\s*:\s*([\d.]+)px/);
      if (!fs) continue;
      for (const sel of rule[1].split(",")) {
        const cls = sel.trim().match(/\.([A-Za-z0-9_-]+)$/);
        if (cls) sizes.set(cls[1], Math.min(sizes.get(cls[1]) ?? Infinity, parseFloat(fs[1])));
      }
    }
  }
  return sizes;
}

/** 그림 하나가 폰에서 필요로 하는 최소 폭 */
function minWidthFor(svg, pageClassSizes) {
  const vb = svg.match(/viewBox="([\d.\s,-]+)"/);
  if (!vb) return null;
  const vbw = parseFloat(vb[1].trim().split(/[\s,]+/)[2]);
  if (!vbw) return null;

  const found = [...svg.matchAll(/font-size\s*[:=]\s*"?([\d.]+)/g)].map((m) => parseFloat(m[1]));
  for (const text of svg.matchAll(/<text\b[^>]*class="([^"]+)"/g)) {
    for (const cls of text[1].split(/\s+/)) {
      if (pageClassSizes.has(cls)) found.push(pageClassSizes.get(cls));
    }
  }
  const minFs = found.length ? Math.min(...found) : 12;
  return Math.round(Math.min(MAX_W, Math.max(MIN_W, vbw * (TARGET_FS / minFs))));
}

let wrapped = 0, retuned = 0, touched = 0;

for (const dir of dirs) {
  for (const name of fs.readdirSync(dir).filter((f) => f.endsWith(".html"))) {
    const file = path.join(dir, name);
    const original = fs.readFileSync(file, "utf8");

    // 본문만 건드린다. <main>이 없는 예전 글은 <body> 전체를 본문으로 본다.
    const start = original.indexOf("<main") !== -1 ? original.indexOf("<main") : original.indexOf("<body");
    const end = original.lastIndexOf("</main>") !== -1 ? original.lastIndexOf("</main>") : original.lastIndexOf("</body>");
    if (start === -1 || end === -1 || end < start) continue;

    const classSizes = classFontSizes(original);
    let body = original.slice(start, end);
    let localWrapped = 0, localRetuned = 0;

    // 1) 아직 안 감싼 그림 감싸기
    body = body.replace(/([ \t]*)(<svg\b[\s\S]*?<\/svg>)/g, (m, indent, svg, offset) => {
      if (body.slice(Math.max(0, offset - 400), offset).includes("diagram-scroll")) return m;
      const need = minWidthFor(svg, classSizes);
      if (need === null) return m;
      localWrapped++;
      return `${indent}<div class="diagram-scroll" style="--diagram-min: ${need}px">\n${indent}${svg}\n${indent}</div>`;
    });

    // 2) 이미 감싼 그림은 값만 다시 맞추기(그림을 고쳤을 수 있으므로)
    body = body.replace(
      /(<div class="diagram-scroll" style="--diagram-min: )(\d+)(px">\s*)(<svg\b[\s\S]*?<\/svg>)/g,
      (m, head, cur, mid, svg) => {
        const need = minWidthFor(svg, classSizes);
        if (need === null || String(need) === cur) return m;
        localRetuned++;
        return head + need + mid + svg;
      }
    );

    const next = original.slice(0, start) + body + original.slice(end);
    if (next === original) continue;
    wrapped += localWrapped;
    retuned += localRetuned;
    touched++;
    if (!check) fs.writeFileSync(file, next);
    if (check) console.log(`${file}: 감쌀 그림 ${localWrapped}개, 값 갱신 ${localRetuned}개`);
  }
}

console.log(
  check
    ? `확인만 함 — 파일 ${touched}개에서 감쌀 그림 ${wrapped}개, 값 갱신 ${retuned}개`
    : `그림 ${wrapped}개를 감싸고 ${retuned}개의 최소 폭을 갱신했습니다 (파일 ${touched}개)`
);
