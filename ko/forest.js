// 전체 지도(숲): 글 하나 = 점 하나. 데이터는 forest-data.js (scripts/build-forest-data.mjs 로 생성)
(function () {
  var F = window.FOREST;
  var root = document.getElementById('forest');
  if (!F || !root) return;
  var NS = 'http://www.w3.org/2000/svg';
  var W = 1000, H = 560, C = 6.4, R = 4.4;
  var STAGE_POS = { 1: [95, 170], 2: [215, 330], 3: [320, 130], 4: [445, 320], 5: [550, 125], 6: [650, 315], 7: [745, 135], 8: [865, 305], 9: [948, 115] };
  var SHELF_POS = [[300, 500], [520, 505], [660, 510]];
  var SHORT = { 1: '웹과 컴퓨터', 2: 'AI 도구 써보기', 3: 'AI 작동 원리', 4: '보고 듣고 그리는 AI', 5: '공간과 자연', 6: '지시·컨텍스트·도구', 7: '내 도구 만들기', 8: '오케스트레이션', 9: '서비스로 내놓기' };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function gColor(g) {
    var grp = F.groups[g];
    if (grp.stage) return 'var(--folder-' + grp.stage + ')';
    return ['var(--folder-10)', 'var(--folder-6)', 'var(--muted)'][g - 9] || 'var(--muted)';
  }

  // 그룹 중심
  var shelfIdx = 0;
  F.groups.forEach(function (g, i) {
    g.idx = i;
    g.c = g.stage ? STAGE_POS[g.stage] : SHELF_POS[shelfIdx++] || [500, 600];
    g.label = g.stage ? g.stage + ' ' + SHORT[g.stage] : (g.locked ? '🔒 ' : '') + g.short;
  });
  // 점 위치: 그룹마다 해바라기 배열(가운데가 첫 글)
  var count = {};
  F.posts.forEach(function (p) {
    var k = count[p.g] = (count[p.g] || 0);
    count[p.g]++;
    var g = F.groups[p.g];
    var rr = C * Math.sqrt(k + 0.5), th = k * 2.39996;
    p.x = g.c[0] + rr * Math.cos(th);
    p.y = g.c[1] + rr * Math.sin(th);
    p.k = k;
  });

  var wrap = document.createElement('div'); wrap.className = 'forest-wrap';
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'forest-svg', role: 'img', 'aria-label': '이 블로그의 글을 점으로 그린 전체 지도. 1단계부터 9단계까지 점선 길로 이어지고, 아래에 책장 묶음이 있다' });
  var tip = document.createElement('div'); tip.className = 'forest-tip';
  wrap.appendChild(svg); wrap.appendChild(tip);

  // 막(幕) 띠
  var acts = [['기초', 30, 375], ['넓히기', 385, 600], ['만들기', 610, 990]];
  acts.forEach(function (a) {
    el('rect', { x: a[1], y: 30, width: a[2] - a[1], height: 380, rx: 22, fill: 'var(--border)', opacity: .28 }, svg);
    var t = el('text', { x: (a[1] + a[2]) / 2, y: 22, 'text-anchor': 'middle', class: 'glabel', 'font-size': 18, fill: 'var(--muted)' }, svg);
    t.textContent = a[0];
  });
  el('rect', { x: 200, y: 430, width: 560, height: 124, rx: 22, fill: 'var(--border)', opacity: .18 }, svg);

  // 길(1→9단계)
  var stages = F.groups.filter(function (g) { return g.stage; }).sort(function (a, b) { return a.stage - b.stage; });
  var d = 'M' + stages[0].c[0] + ',' + stages[0].c[1];
  for (var i = 1; i < stages.length; i++) {
    var a = stages[i - 1].c, b = stages[i].c, mx = (a[0] + b[0]) / 2;
    d += ' C' + mx + ',' + a[1] + ' ' + mx + ',' + b[1] + ' ' + b[0] + ',' + b[1];
  }
  var road = el('path', { d: d, class: 'road' }, svg);

  // 그룹 배경과 이름
  var halos = [];
  F.groups.forEach(function (g) {
    var rad = C * Math.sqrt(g.n + 0.5) + 12;
    g.rad = rad;
    var h = el('circle', { cx: g.c[0], cy: g.c[1], r: rad, fill: gColor(g.idx), opacity: .12, class: 'halo' }, svg);
    h.dataset.g = g.idx; halos.push(h);
    var ty = g.stage ? (g.c[1] < 220 ? g.c[1] - rad - 22 : g.c[1] + rad + 22) : g.c[1] - rad - 20;
    var t = el('text', { x: g.c[0], y: ty, 'text-anchor': 'middle', class: 'glabel', 'font-size': g.stage ? 17 : 15, fill: 'var(--ink)' }, svg);
    t.textContent = g.label;
    var n = el('text', { x: g.c[0], y: ty + 17, 'text-anchor': 'middle', class: 'glabel', 'font-size': 13, fill: 'var(--muted)' }, svg);
    n.textContent = g.n + '편';
  });

  var trail = el('path', { class: 'trail', d: '', opacity: 0 }, svg);
  var numLayer = el('g', {}, svg);

  // 점
  var dots = F.posts.map(function (p) {
    var c = el('circle', { r: R, cx: 0, cy: 0, class: 'dot', fill: gColor(p.g) }, svg);
    c.style.transform = 'translate(' + W / 2 + 'px,' + H / 2 + 'px)';
    c.style.opacity = 0;
    c.dataset.i = F.posts.indexOf(p);
    c.addEventListener('mouseenter', function (e) { showTip(p, e); });
    c.addEventListener('mousemove', function (e) { moveTip(e); });
    c.addEventListener('mouseleave', function () { tip.style.opacity = 0; });
    c.addEventListener('click', function () { location.href = p.f + '.html'; });
    return c;
  });
  function place() {
    if (placed) return; placed = true;
    F.posts.forEach(function (p, i) {
      var c = dots[i];
      c.style.transitionDelay = reduce ? '0s' : (p.g * 0.06 + p.k * 0.008) + 's';
      c.style.transform = 'translate(' + p.x + 'px,' + p.y + 'px)';
      c.style.opacity = c.dataset.dim === '1' ? .12 : 1;
    });
  }
  // 길 그리기
  var len = road.getTotalLength ? road.getTotalLength() : 0;
  if (len && !reduce) {
    road.style.strokeDasharray = len; road.style.strokeDashoffset = len;
    road.style.transition = 'stroke-dashoffset 2.2s ease .6s';
  }

  function subName(p) {
    var g = F.groups[p.g];
    var s = g.subs.filter(function (x) { return x.id === p.s; })[0];
    return s && s.name !== g.name ? s.name : '';
  }
  function showTip(p, e) {
    var g = F.groups[p.g];
    tip.innerHTML = '<strong>' + esc(p.t) + '</strong><br><span style="opacity:.75">' + esc(g.label) + (subName(p) ? ' · ' + esc(subName(p)) : '') + '</span>';
    tip.style.opacity = 1; moveTip(e);
  }
  function moveTip(e) {
    var r = wrap.getBoundingClientRect();
    var x = e.clientX - r.left + 14, y = e.clientY - r.top + 14;
    if (x > r.width - 290) x = e.clientX - r.left - 290;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // 보기 바꾸기
  var modes = document.createElement('div'); modes.className = 'forest-modes';
  var chips = document.createElement('div'); chips.className = 'forest-chips';
  var panel = document.createElement('div'); panel.className = 'forest-panel';
  var MODES = [['stage', '단계별로 보기'], ['region', '주제 영역별로 보기'], ['path', '공부 길로 보기']];
  MODES.forEach(function (m) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = m[1]; b.dataset.m = m[0];
    b.addEventListener('click', function () { setMode(m[0]); });
    modes.appendChild(b);
  });
  root.appendChild(modes); root.appendChild(chips); root.appendChild(wrap); root.appendChild(panel);

  function dim(pred) {
    dots.forEach(function (c, i) { var on = pred(F.posts[i]); c.dataset.dim = on ? '0' : '1'; if (placed) c.style.opacity = on ? 1 : .12; c.setAttribute('r', R); });
  }
  function clearTrail() { trail.setAttribute('opacity', 0); numLayer.innerHTML = ''; }

  var mode = null;
  function setMode(m) {
    mode = m;
    [].forEach.call(modes.children, function (b) { b.classList.toggle('on', b.dataset.m === m); });
    chips.innerHTML = ''; clearTrail();
    if (m === 'stage') {
      dots.forEach(function (c, i) { c.style.fill = gColor(F.posts[i].g); });
      dim(function () { return true; });
      panel.innerHTML = '<p>점에 마우스를 대면 제목, 누르면 그 글로 가요. 색 동그라미에 대면 소분류가 보여요.</p>';
    } else if (m === 'region') {
      var col = {}; F.regions.forEach(function (r) { col[r.id] = r.color; });
      dots.forEach(function (c, i) { var r = F.posts[i].r; c.style.fill = r ? col[r] : 'var(--muted)'; });
      dim(function () { return true; });
      F.regions.forEach(function (r) {
        var b = document.createElement('button'); b.type = 'button';
        b.innerHTML = '<span class="sw" style="background:' + r.color + '"></span>' + esc(r.name);
        var n = F.posts.filter(function (p) { return p.r === r.id; }).length;
        b.addEventListener('mouseenter', function () { dim(function (p) { return p.r === r.id; }); panel.innerHTML = '<p><strong>' + esc(r.name) + '</strong> — ' + n + '편</p>'; });
        b.addEventListener('mouseleave', function () { dim(function () { return true; }); });
        chips.appendChild(b);
      });
      panel.innerHTML = '<p>같은 점을 «무엇을 다루는 글인가»로 칠했어요. 이름에 마우스를 대면 그 영역만 남아요.</p>';
    } else {
      dots.forEach(function (c, i) { c.style.fill = gColor(F.posts[i].g); });
      dim(function () { return false; });
      F.ladders.forEach(function (l, li) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = l.mark + ' ' + l.name;
        b.addEventListener('click', function () {
          [].forEach.call(chips.children, function (x) { x.classList.toggle('on', x === b); });
          showLadder(l);
        });
        chips.appendChild(b);
        if (li === 0) setTimeout(function () { b.click(); }, 50);
      });
    }
  }
  function showLadder(l) {
    var idx = l.posts.map(function (f) { for (var i = 0; i < F.posts.length; i++) if (F.posts[i].f === f) return i; return -1; }).filter(function (i) { return i >= 0; });
    dim(function (p) { return l.posts.indexOf(p.f) >= 0; });
    idx.forEach(function (i) { dots[i].setAttribute('r', R + 3); });
    var pts = idx.map(function (i) { return [F.posts[i].x, F.posts[i].y]; });
    if (pts.length) {
      var d2 = 'M' + pts.map(function (q) { return q[0] + ',' + q[1]; }).join(' L');
      trail.setAttribute('d', d2); trail.setAttribute('opacity', .85);
      var L = trail.getTotalLength();
      trail.style.transition = 'none'; trail.style.strokeDasharray = L; trail.style.strokeDashoffset = reduce ? 0 : L;
      trail.getBoundingClientRect();
      trail.style.transition = reduce ? 'none' : 'stroke-dashoffset 1.6s ease';
      trail.style.strokeDashoffset = 0;
    }
    numLayer.innerHTML = '';
    pts.forEach(function (q, k) {
      var t = el('text', { x: q[0] + 9, y: q[1] - 8, class: 'num' }, numLayer); t.textContent = k + 1;
    });
    panel.innerHTML = '<p><strong>' + esc(l.mark + ' ' + l.name) + '</strong> — 이 순서로 읽어요.</p><ol>' +
      idx.map(function (i) { return '<li><a href="' + F.posts[i].f + '.html">' + esc(F.posts[i].t) + '</a></li>'; }).join('') + '</ol>';
  }

  // 그룹에 마우스를 대면 소분류
  halos.forEach(function (h) {
    var g = F.groups[+h.dataset.g];
    h.addEventListener('mouseenter', function () {
      if (mode !== 'stage') return;
      h.setAttribute('opacity', .26);
      panel.innerHTML = '<p><strong>' + esc(g.name) + '</strong> — ' + g.n + '편 · <a href="posts.html#' + g.id + '">목록에서 보기</a></p><p>' +
        g.subs.map(function (s) { return esc(s.name) + ' <span style="color:var(--muted)">' + s.n + '</span>'; }).join(' · ') + '</p>';
    });
    h.addEventListener('mouseleave', function () { h.setAttribute('opacity', .12); });
  });

  var placed = false;
  var start = root.getAttribute('data-mode') || 'stage';
  setMode(start);
  requestAnimationFrame(function () { requestAnimationFrame(function () {
    place();
    if (len && !reduce) road.style.strokeDashoffset = 0;
    if (start === 'path') setTimeout(function () { var b = chips.querySelector('button'); if (b) b.click(); }, 900);
  }); });
  setTimeout(function () { place(); if (len && !reduce) road.style.strokeDashoffset = 0; }, 400);
})();
