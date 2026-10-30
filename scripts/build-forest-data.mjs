// 전체 지도(숲)용 데이터를 만든다: ko/forest-data.js
// 원천: ko/posts.html(단계·소분류·글 순서), ko/topic-map.html(사다리), ko/big-map-data.js(주제 영역)
// 실행: node scripts/build-forest-data.mjs
import fs from 'fs';
import vm from 'vm';

const posts = fs.readFileSync('ko/posts.html', 'utf8');
const strip = (h) => h.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();

// 1) 단계·책장 그룹과 소분류, 글
const groupRe = /<h3 class="post-group-title" id="([^"]+)">([^<]*)<\/h3>/g;
const marks = [];
let m;
while ((m = groupRe.exec(posts))) marks.push({ id: m[1], name: m[2].trim(), at: m.index, end: groupRe.lastIndex });
const groups = [];
const list = [];
marks.forEach((g, gi) => {
  const body = posts.slice(g.end, gi + 1 < marks.length ? marks[gi + 1].at : posts.length);
  // 글마다 바로 앞에 나온 소분류에 붙인다(소분류가 없으면 그룹 자체)
  const heads = [...body.matchAll(/<summary class="post-subcategory-title" id="([^"]+)">([\s\S]*?)<\/summary>/g)]
    .map((x) => ({ id: x[1], name: strip(x[2]), at: x.index }));
  const subs = [];
  const liRe = /<a href="([a-z0-9-]+)\.html">(?:(?!<\/a>)[\s\S])*?<span class="title-list-title">([\s\S]*?)<\/span>/g;
  let l;
  while ((l = liRe.exec(body))) {
    if (list.some((p) => p.f === l[1])) continue;
    const head = heads.filter((h) => h.at < l.index).pop() || { id: g.id, name: g.name };
    let sub = subs.find((x) => x.id === head.id);
    if (!sub) { sub = { id: head.id, name: head.name, n: 0 }; subs.push(sub); }
    sub.n++;
    list.push({ f: l[1], t: strip(l[2]), g: groups.length, s: head.id });
  }
  const stage = g.name.match(/^(\d)단계 · (.*)$/);
  groups.push({ id: g.id, name: g.name, stage: stage ? +stage[1] : 0, short: stage ? stage[2] : g.name.replace(/^🔒\s*/, ''), locked: g.name.includes('🔒'), subs });
});
groups.forEach((g, i) => { g.n = list.filter((p) => p.g === i).length; });

// 2) 사다리(주제 지도)
const tm = fs.readFileSync('ko/topic-map.html', 'utf8');
const ladders = [];
const secs = tm.split(/(?=<h2)/);
for (const sec of secs) {
  const h = sec.match(/<h2[^>]*>([\s\S]*?)<\/h2>/);
  if (!h) continue;
  const title = strip(h[1]);
  const lm = title.match(/^사다리\s*(\S+)\s*—\s*(.*)$/);
  if (!lm) continue;
  const seen = [];
  for (const x of sec.matchAll(/href="([a-z0-9-]+)\.html/g)) {
    if (!seen.includes(x[1]) && list.some((p) => p.f === x[1])) seen.push(x[1]);
  }
  ladders.push({ mark: lm[1], name: lm[2], posts: seen });
}

// 3) 주제 영역(큰 그림 데이터의 8영역)
const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync('ko/big-map-data.js', 'utf8'), ctx);
const B = ctx.window.BIGMAP;
const regions = B.regions.map((r) => ({ id: r.id, name: r.name, color: r.color }));
const regionOf = {};
for (const r of B.regions) {
  for (const sid of r.subs || []) {
    const sub = B.subs[sid];
    if (!sub) continue;
    for (const p of sub.posts || []) {
      const f = (p.file || '').replace(/\.html$/, '');
      if (f && !(f in regionOf)) regionOf[f] = r.id;
    }
  }
}
list.forEach((p) => { p.r = regionOf[p.f] || null; });

const out = { groups, posts: list, ladders, regions };
fs.writeFileSync('ko/forest-data.js',
  '// 전체 지도(숲) 데이터 — scripts/build-forest-data.mjs 가 만든다. 손으로 고치지 말 것.\nwindow.FOREST = ' + JSON.stringify(out) + ';\n');
console.log('groups', groups.map((g) => `${g.short}:${g.n}`).join(' / '));
console.log('posts', list.length, '| ladders', ladders.length, ladders.map((l) => l.posts.length).join(','), '| region 없는 글', list.filter((p) => !p.r).length);
