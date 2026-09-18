// 큰 그림 지도: 상자를 누르면 한 단계 안으로 들어가는 지도.
// 데이터는 big-map-data.js(window.BIGMAP)에 있고, 이 파일은 그리기만 한다.
// 단계: 전체(#/) → 지역(#/r) → 구역(#/r/s) → 개념 카드(#/r/s/n), 가로지르는 실(#/t/id)
(function () {
  const D = window.BIGMAP;
  const root = document.getElementById("bm-root");
  if (!D || !root) return;

  const regionById = {};
  D.regions.forEach((r, i) => { r.index = i; regionById[r.id] = r; });
  const subRegion = {};
  D.regions.forEach((r) => r.subs.forEach((s) => { subRegion[s] = r; }));

  // 글 파일 → 지도 위 자리(지역·구역·노드)
  const postHome = {};
  Object.keys(D.subs).forEach((sid) => {
    const s = D.subs[sid];
    s.flow.nodes.forEach((n) => n.posts.forEach((f) => {
      if (!postHome[f]) postHome[f] = { r: subRegion[sid].id, s: sid, n: n.id };
    }));
  });
  const postInfo = {};
  Object.keys(D.subs).forEach((sid) => D.subs[sid].posts.forEach((p) => { postInfo[p.file] = p; }));

  const esc = (t) => String(t == null ? "" : t)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  // ---------- 상자-화살표 배치 ----------
  // 화살표를 따라 층을 나누고(위→아래), 한 층이 폭을 넘으면 여러 줄로 접는다.
  function layers(nodes, edges) {
    const ids = nodes.map((n) => n.id);
    const out = {}; ids.forEach((id) => { out[id] = []; });
    edges.forEach((e) => { if (out[e[0]] && out[e[1]] !== undefined) out[e[0]].push(e[1]); });
    // 되돌아가는 화살표(순환)는 층 계산에서 뺀다
    const state = {}, back = new Set();
    function dfs(u) {
      state[u] = 1;
      out[u].forEach((v) => {
        if (state[v] === 1) back.add(u + ">" + v);
        else if (!state[v]) dfs(v);
      });
      state[u] = 2;
    }
    ids.forEach((id) => { if (!state[id]) dfs(id); });
    const layer = {}; ids.forEach((id) => { layer[id] = 0; });
    for (let k = 0; k < ids.length; k++) {
      edges.forEach((e) => {
        if (back.has(e[0] + ">" + e[1]) || layer[e[0]] === undefined || layer[e[1]] === undefined) return;
        if (layer[e[1]] < layer[e[0]] + 1) layer[e[1]] = layer[e[0]] + 1;
      });
    }
    // 들어오는 화살표가 없는 외톨이는 이어진 곳 바로 위층으로 당긴다
    edges.forEach((e) => {
      if (back.has(e[0] + ">" + e[1])) return;
      const hasIn = edges.some((f) => f[1] === e[0]);
      if (!hasIn && layer[e[1]] - layer[e[0]] > 1) layer[e[0]] = layer[e[1]] - 1;
    });
    return layer;
  }

  function drawGraph(host, nodes, edges, opts) {
    host.innerHTML = "";
    const W = host.clientWidth || 700;
    const gap = 14, vgap = opts.vgap || 58, minW = W < 480 ? 132 : 158, maxW = opts.maxW || 236;
    const perRow = Math.max(1, Math.floor((W + gap) / (minW + gap)));
    const layer = layers(nodes, edges);
    const byLayer = [];
    nodes.forEach((n) => { (byLayer[layer[n.id]] = byLayer[layer[n.id]] || []).push(n); });

    const els = {};
    nodes.forEach((n) => {
      const el = document.createElement(n.onClick ? "button" : "div");
      el.className = "bm-node" + (n.kind ? " bm-" + n.kind : "") + (n.onClick ? "" : " bm-static");
      el.style.setProperty("--nc", n.color || "var(--folder-9)");
      el.innerHTML =
        (n.step ? '<span class="bm-step">' + esc(n.step) + "</span>" : "") +
        '<span class="bm-node-title">' + esc(n.label) + "</span>" +
        (n.sub ? '<span class="bm-node-sub">' + esc(n.sub) + "</span>" : "") +
        (n.count ? '<span class="bm-node-count">' + esc(n.count) + "</span>" : "");
      if (n.onClick) el.addEventListener("click", n.onClick);
      host.appendChild(el);
      els[n.id] = el;
    });

    // 줄 단위로 자리 잡기
    const pos = {};
    let y = 4, prevCenters = {};
    byLayer.forEach((row) => {
      if (!row) return;
      // 위층과 가까운 순서로 정렬(교차 줄이기)
      row.sort((a, b) => center(a) - center(b));
      function center(n) {
        const ins = edges.filter((e) => e[1] === n.id && prevCenters[e[0]] !== undefined);
        if (!ins.length) return 1e6 + nodes.indexOf(n);
        return ins.reduce((s, e) => s + prevCenters[e[0]], 0) / ins.length;
      }
      for (let i = 0; i < row.length; i += perRow) {
        const chunk = row.slice(i, i + perRow);
        const k = chunk.length;
        const w = Math.min(maxW, (W - (Math.min(perRow, row.length) - 1) * gap) / Math.min(perRow, row.length));
        const total = k * w + (k - 1) * gap;
        let x = (W - total) / 2, h = 0;
        chunk.forEach((n) => {
          const el = els[n.id];
          el.style.width = w + "px";
          el.style.left = x + "px";
          el.style.top = y + "px";
          h = Math.max(h, el.offsetHeight);
          pos[n.id] = { x: x, y: y, w: w };
          x += w + gap;
        });
        chunk.forEach((n) => { pos[n.id].h = els[n.id].offsetHeight; prevCenters[n.id] = pos[n.id].x + w / 2; });
        y += h + vgap;
      }
    });
    const H = y - vgap + 8;
    host.style.height = H + "px";

    // 화살표
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "bm-edges");
    svg.setAttribute("width", W); svg.setAttribute("height", H);
    svg.setAttribute("aria-hidden", "true");
    const mk = document.createElementNS(NS, "marker");
    const mid = "bm-arrow-" + Math.random().toString(36).slice(2, 7);
    mk.setAttribute("id", mid); mk.setAttribute("viewBox", "0 0 10 10");
    mk.setAttribute("refX", "9"); mk.setAttribute("refY", "5");
    mk.setAttribute("markerWidth", "7"); mk.setAttribute("markerHeight", "7");
    mk.setAttribute("orient", "auto-start-reverse");
    mk.innerHTML = '<path d="M0,0 L10,5 L0,10 z" class="bm-arrowhead"/>';
    const defs = document.createElementNS(NS, "defs"); defs.appendChild(mk); svg.appendChild(defs);
    host.insertBefore(svg, host.firstChild);

    const placed = Object.keys(pos).map((k) => ({ x: pos[k].x, y: pos[k].y, w: pos[k].w, h: pos[k].h }));
    edges.forEach((e) => {
      const a = pos[e[0]], b = pos[e[1]];
      if (!a || !b) return;
      let d, lx, ly;
      if (b.y > a.y + a.h) {
        const x1 = a.x + a.w / 2, y1 = a.y + a.h, x2 = b.x + b.w / 2, y2 = b.y - 2;
        // 층을 건너뛰는 화살표가 중간 상자를 뚫지 않게 옆으로 돌린다
        const lo = Math.min(x1, x2) - 12, hi = Math.max(x1, x2) + 12;
        const blockers = Object.keys(pos).map((k) => pos[k])
          .filter((p) => p.y > y1 && p.y + p.h < y2 && p.x < hi && p.x + p.w > lo);
        if (blockers.length) {
          let xs = Math.max.apply(null, blockers.map((p) => p.x + p.w)) + 18;
          if (xs > W - 6) xs = Math.min.apply(null, blockers.map((p) => p.x)) - 18;
          const t1 = Math.min.apply(null, blockers.map((p) => p.y));
          const t2 = Math.max.apply(null, blockers.map((p) => p.y + p.h));
          d = "M" + x1 + "," + y1 + " C" + x1 + "," + (y1 + 24) + " " + xs + "," + (t1 - 24) + " " + xs + "," + t1 +
            " L" + xs + "," + t2 + " C" + xs + "," + (t2 + 24) + " " + x2 + "," + (y2 - 24) + " " + x2 + "," + y2;
          lx = xs; ly = t1 - 14;
        } else {
          const m = (y2 - y1) / 2;
          d = "M" + x1 + "," + y1 + " C" + x1 + "," + (y1 + m) + " " + x2 + "," + (y2 - m) + " " + x2 + "," + y2;
          lx = (x1 + x2) / 2; ly = (y1 + y2) / 2;
        }
      } else if (Math.abs(b.y - a.y) < 2) {
        // 같은 줄: 옆으로
        const leftToRight = b.x > a.x;
        const x1 = leftToRight ? a.x + a.w : a.x, x2 = leftToRight ? b.x - 2 : b.x + b.w + 2;
        const y1 = a.y + a.h / 2;
        d = "M" + x1 + "," + y1 + " L" + x2 + "," + y1;
        lx = (x1 + x2) / 2; ly = y1 - 12;
      } else {
        // 위로 되돌아가는 화살표: 오른쪽 바깥으로 돌린다
        const x1 = a.x + a.w, y1 = a.y + a.h / 2, x2 = b.x + b.w + 2, y2 = b.y + b.h / 2;
        const bulge = Math.min(W - 4, Math.max(x1, x2) + 34);
        d = "M" + x1 + "," + y1 + " C" + bulge + "," + y1 + " " + bulge + "," + y2 + " " + x2 + "," + y2;
        lx = bulge - 14; ly = (y1 + y2) / 2;
      }
      const p = document.createElementNS(NS, "path");
      p.setAttribute("d", d);
      p.setAttribute("class", "bm-edge");
      p.setAttribute("marker-end", "url(#" + mid + ")");
      svg.appendChild(p);
      if (e[2]) {
        const lab = document.createElement("span");
        lab.className = "bm-edge-label";
        lab.textContent = e[2];
        host.appendChild(lab);
        const lw = lab.offsetWidth, lh = lab.offsetHeight;
        // 상자나 다른 라벨과 겹치면 가까운 빈자리로 비킨다
        const clampX = (x) => Math.max(0, Math.min(W - lw, x));
        const hits = (l, t) => placed.some((r) => l < r.x + r.w + 2 && r.x < l + lw + 2 && t < r.y + r.h + 1 && r.y < t + lh + 1);
        let left = clampX(lx - lw / 2), top = ly - lh / 2;
        const tries = [];
        for (let dy = 0; dy <= 90; dy += 6) {
          [0, -(lw / 2 + 10), lw / 2 + 10].forEach((dx) => { tries.push([dx, -dy]); if (dy) tries.push([dx, dy]); });
        }
        for (const t of tries) {
          const l = clampX(lx - lw / 2 + t[0]), tp = ly - lh / 2 + t[1];
          if (!hits(l, tp)) { left = l; top = tp; break; }
        }
        placed.push({ x: left, y: top, w: lw, h: lh });
        lab.style.left = left + "px";
        lab.style.top = top + "px";
      }
    });
  }

  // ---------- 화면 ----------
  let redraw = null, current = null;

  // ---------- 크게 보기 ----------
  // 지도 그림을 화면 가득 다시 그린다. 폰에서는 720px 폭으로 그려 옆으로 밀어 보게 한다.
  const modal = document.createElement("dialog");
  modal.className = "bm-modal";
  modal.setAttribute("aria-label", "지도 크게 보기");
  modal.innerHTML = '<div class="bm-modal-bar"><p class="bm-modal-title"></p>' +
    '<button type="button" class="bm-modal-close" aria-label="닫기">×</button></div>' +
    '<div class="bm-modal-scroll"><div class="bm-graph bm-modal-graph"></div></div>';
  document.body.appendChild(modal);
  const modalGraph = modal.querySelector(".bm-modal-graph");
  function drawModal() {
    if (!current || !modal.open) return;
    const avail = modal.querySelector(".bm-modal-scroll").clientWidth - 32;
    modalGraph.style.width = Math.max(720, Math.min(1180, avail)) + "px";
    const nodes = current.nodes.map((n) => Object.assign({}, n, n.onClick ? {
      onClick: () => { modal.close(); n.onClick(); } } : {}));
    drawGraph(modalGraph, nodes, current.edges, Object.assign({}, current.opts,
      { maxW: Math.max(current.opts.maxW || 236, 260) }));
  }
  function openModal() {
    if (!current) return;
    const h = root.querySelector(".bm-h");
    modal.querySelector(".bm-modal-title").textContent = h ? h.textContent : "";
    if (typeof modal.showModal === "function") modal.showModal(); else modal.setAttribute("open", "");
    drawModal();
  }
  modal.querySelector(".bm-modal-close").addEventListener("click", () => modal.close());
  // 그림 바깥(어두운 배경)을 누르면 닫는다
  modal.addEventListener("click", (e) => { if (e.target === modal) modal.close(); });

  function show(nodes, edges, opts) {
    const host = document.getElementById("bm-g");
    current = { nodes: nodes, edges: edges, opts: opts };
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "bm-zoom-btn";
    btn.textContent = "⤢ 크게 보기";
    btn.addEventListener("click", openModal);
    host.parentNode.insertBefore(btn, host);
    // 상자가 아닌 빈 곳을 눌러도 크게 본다
    host.addEventListener("click", (e) => { if (!e.target.closest(".bm-node")) openModal(); });
    redraw = () => drawGraph(host, nodes, edges, opts);
    redraw();
  }
  function crumbs(list) {
    return '<nav class="bm-crumbs" aria-label="지도 위치">' + list.map((c, i) =>
      i === list.length - 1 ? '<span aria-current="page">' + esc(c[0]) + "</span>"
        : '<a href="' + c[1] + '">' + esc(c[0]) + "</a>").join('<span class="bm-sep">›</span>') + "</nav>";
  }
  function go(h) { location.hash = h; }
  function levelTag(n, text) {
    return '<p class="bm-level"><span class="bm-level-dots">' +
      [0, 1, 2, 3].map((i) => '<i class="' + (i <= n ? "on" : "") + '"></i>').join("") +
      "</span>" + esc(text) + "</p>";
  }

  function viewWorld() {
    root.innerHTML = crumbs([["전체 그림", "#/"]]) + levelTag(0, "전체 보기") +
      '<h3 class="bm-h">' + esc(D.world.title) + "</h3>" +
      '<p class="bm-lead">' + esc(D.world.lead) + "</p>" +
      '<div class="bm-graph" id="bm-g"></div>' +
      '<ol class="bm-steps">' + D.world.steps.map((s) =>
        '<li><strong>' + esc(s[0]) + "</strong> " + esc(s[1]) + "</li>").join("") + "</ol>" +
      '<p class="bm-threads-title">어디에나 걸쳐 있는 세 가닥</p>' +
      '<div class="bm-threads">' + D.threads.map((t) =>
        '<a class="bm-thread" href="#/t/' + t.id + '" style="--nc:' + t.color + '"><strong>' + esc(t.name) +
        "</strong><span>" + esc(t.question) + "</span></a>").join("") + "</div>";
    const nodes = D.world.nodes.map((n) => {
      const r = regionById[n.id];
      return {
        id: n.id, label: n.label, sub: n.sub, step: n.step, kind: r ? "region" : "actor",
        color: r ? r.color : "var(--muted)",
        count: r ? countRegion(r) + "편" : "",
        onClick: r ? () => go("#/" + r.id) : null,
      };
    });
    show(nodes, D.world.edges, { vgap: 62, maxW: 280 });
  }
  function countRegion(r) { return r.subs.reduce((s, sid) => s + (D.subs[sid] ? D.subs[sid].posts.length : 0), 0); }

  function viewRegion(r) {
    root.innerHTML = crumbs([["전체 그림", "#/"], [r.name, "#/" + r.id]]) + levelTag(1, "지역 확대 · 이 지역의 글 묶음") +
      '<h3 class="bm-h" style="--nc:' + r.color + '">' + esc(r.name) + "</h3>" +
      '<p class="bm-lead">' + esc(r.role) + "</p>" +
      '<div class="bm-scene" style="--nc:' + r.color + '"><p class="bm-scene-title">실전에서는</p><p>' + esc(r.scenario) + "</p></div>" +
      '<div class="bm-graph" id="bm-g"></div>' +
      '<p class="bm-hint">상자를 누르면 그 글 묶음이 어떤 순서로 돌아가는지 확대해 볼 수 있어요.</p>';
    const nodes = r.subs.filter((sid) => D.subs[sid]).map((sid) => {
      const s = D.subs[sid];
      return { id: sid, label: s.name, sub: s.role, color: r.color, kind: "sub",
        count: s.posts.length + "편", onClick: () => go("#/" + r.id + "/" + sid) };
    });
    show(nodes, r.edges, {});
  }

  function viewSub(r, sid) {
    const s = D.subs[sid];
    root.innerHTML = crumbs([["전체 그림", "#/"], [r.name, "#/" + r.id], [s.name, "#/" + r.id + "/" + sid]]) +
      levelTag(2, "묶음 확대 · 돌아가는 순서") +
      '<h3 class="bm-h" style="--nc:' + r.color + '">' + esc(s.name) + "</h3>" +
      '<p class="bm-lead">' + esc(s.role) + "</p>" +
      '<div class="bm-scene" style="--nc:' + r.color + '"><p class="bm-scene-title">실전에서는</p><p>' + esc(s.scenario) + "</p></div>" +
      '<div class="bm-graph" id="bm-g"></div>' +
      '<p class="bm-hint">상자를 누르면 그 개념을 다룬 글과, 실제로 쓰이는 순간이 나와요.</p>';
    const nodes = s.flow.nodes.map((n) => ({
      id: n.id, label: n.label, color: r.color, kind: "concept",
      count: n.posts.length + "편", onClick: () => go("#/" + r.id + "/" + sid + "/" + n.id),
    }));
    show(nodes, s.flow.edges, { vgap: 54, maxW: 200 });
  }

  function card(p, color) {
    const t = D.titles[p.file] || p.file;
    const links = (p.links || []).filter((f) => postHome[f] && f !== p.file);
    return '<article class="bm-card" style="--nc:' + color + '">' +
      '<p class="bm-card-concept">' + esc(p.concept) + "</p>" +
      '<p class="bm-card-line">' + esc(p.one_line) + "</p>" +
      (p.practice ? '<p class="bm-card-practice"><span>실전</span>' + esc(p.practice) + "</p>" : "") +
      (p.analogy ? '<p class="bm-card-analogy"><span>비유</span>' + esc(p.analogy) + "</p>" : "") +
      (p.keywords && p.keywords.length ? '<p class="bm-card-keys">' + p.keywords.map((k) => "<span>" + esc(k) + "</span>").join("") + "</p>" : "") +
      '<a class="bm-card-read" href="' + esc(p.file) + '">글 읽기 · ' + esc(t) + " →</a>" +
      (links.length ? '<p class="bm-card-links">이어지는 자리 ' + links.map((f) => {
        const h = postHome[f];
        return '<a href="#/' + h.r + "/" + h.s + "/" + h.n + '">' + esc(postInfo[f].concept) + "</a>";
      }).join("") + "</p>" : "") +
      "</article>";
  }

  function viewNode(r, sid, nid) {
    const s = D.subs[sid];
    const n = s.flow.nodes.find((x) => x.id === nid);
    if (!n) return viewSub(r, sid);
    const ins = s.flow.edges.filter((e) => e[1] === nid).map((e) => s.flow.nodes.find((x) => x.id === e[0]));
    const outs = s.flow.edges.filter((e) => e[0] === nid).map((e) => s.flow.nodes.find((x) => x.id === e[1]));
    const base = "#/" + r.id + "/" + sid + "/";
    const nb = (list, lab) => list.filter(Boolean).length ? '<p class="bm-nb"><span>' + lab + "</span>" +
      list.filter(Boolean).map((x) => '<a href="' + base + x.id + '">' + esc(x.label) + "</a>").join("") + "</p>" : "";
    root.innerHTML = crumbs([["전체 그림", "#/"], [r.name, "#/" + r.id], [s.name, "#/" + r.id + "/" + sid], [n.label, base + nid]]) +
      levelTag(3, "글 확대 · 한 편씩") +
      '<h3 class="bm-h" style="--nc:' + r.color + '">' + esc(n.label) + "</h3>" +
      nb(ins, "앞 단계") + nb(outs, "다음 단계") +
      '<div class="bm-cards">' + n.posts.map((f) => postInfo[f]).filter(Boolean).map((p) => card(p, r.color)).join("") + "</div>";
    redraw = null; current = null;
  }

  function viewThread(t) {
    root.innerHTML = crumbs([["전체 그림", "#/"], [t.name, "#/t/" + t.id]]) + levelTag(1, "가로지르는 한 가닥") +
      '<h3 class="bm-h" style="--nc:' + t.color + '">' + esc(t.name) + "</h3>" +
      '<p class="bm-lead">' + esc(t.lead) + "</p>" +
      '<div class="bm-graph" id="bm-g"></div>' +
      '<p class="bm-hint">번호는 읽기 좋은 순서예요. 상자를 누르면 그 글이 원래 있는 지도 자리로 가요. 색은 속한 지역이에요.</p>';
    const items = t.posts.filter((f) => postHome[f]);
    const nodes = items.map((f, i) => {
      const h = postHome[f], r = regionById[h.r];
      return { id: f, label: postInfo[f].concept, sub: postInfo[f].one_line, count: r.name, step: String(i + 1),
        color: r.color, kind: "concept", onClick: () => go("#/" + h.r + "/" + h.s + "/" + h.n) };
    });
    show(nodes, [], { vgap: 22, maxW: 250 });
  }

  function route() {
    if (modal.open) modal.close();
    const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    if (parts[0] === "t") {
      const t = D.threads.find((x) => x.id === parts[1]);
      if (t) viewThread(t); else viewWorld();
    } else if (!parts.length || !regionById[parts[0]]) viewWorld();
    else {
      const r = regionById[parts[0]];
      if (parts[1] && D.subs[parts[1]] && r.subs.indexOf(parts[1]) >= 0) {
        if (parts[2]) viewNode(r, parts[1], parts[2]); else viewSub(r, parts[1]);
      } else viewRegion(r);
    }
    const top = root.getBoundingClientRect().top + window.scrollY - 16;
    if (location.hash && window.scrollY > top) window.scrollTo({ top: top });
  }

  window.addEventListener("hashchange", route);
  let rt;
  window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (redraw) redraw(); drawModal(); }, 120); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { if (redraw) redraw(); });
  route();
})();
