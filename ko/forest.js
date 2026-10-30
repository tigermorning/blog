// 전체 지도(숲): 글 하나 = 점 하나. 데이터는 forest-data.js (scripts/build-forest-data.mjs 로 생성)
(function () {
  var F = window.FOREST;
  var root = document.getElementById('forest');
  if (!F || !root) return;
  var NS = 'http://www.w3.org/2000/svg';
  var W = 1000, H = 430, C = 6.4, R = 4.4;
  var STAGE_POS = { 1: [95, 170], 2: [215, 330], 3: [320, 130], 4: [445, 320], 5: [550, 125], 6: [650, 315], 7: [745, 135], 8: [865, 305], 9: [948, 115] };
  var SHORT = { 1: '웹과 컴퓨터', 2: 'AI 도구 써보기', 3: 'AI 작동 원리', 4: '보고 듣고 그리는 AI', 5: '공간과 자연', 6: '지시·컨텍스트·도구', 7: '내 도구 만들기', 8: '오케스트레이션', 9: '서비스로 내놓기' };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // 공부 사다리: 숲 대신 칸을 왼쪽→오른쪽(좁은 화면은 위→아래)으로 잇는다
  if (root.getAttribute('data-mode') === 'path') {
    var lchips = document.createElement('div'); lchips.className = 'forest-chips ladder-chips';
    var board = document.createElement('div'); board.className = 'ladder-board';
    root.appendChild(lchips); root.appendChild(board);
    var showL = function (l) {
      var h = '<p class="ladder-head">' + esc(l.mark + ' ' + l.name) + '</p><ol class="ladder-steps">';
      l.steps.forEach(function (s, k) {
        if (k) h += '<li class="ladder-cond" aria-hidden="true"><span>' + esc(l.conds[k - 1] || '') + '</span></li>';
        var sc = s.stage ? 'var(--folder-' + s.stage + ')' : 'var(--muted)';
        h += '<li class="ladder-step" style="--sc:' + sc + ';--k:' + k + '"><a href="' + s.f + '.html">' +
          '<span class="ls-n">' + (k + 1) + '</span><span class="ls-t">' + esc(s.title) + '</span><span class="ls-tag">' + esc(s.tag) + '</span>' +
          '<span class="ls-post">' + esc(s.t) + '</span>' + (s.stage ? '<span class="ls-st">' + s.stage + '단계 글</span>' : '') + '</a></li>';
      });
      board.innerHTML = h + '</ol>' + (l.note ? '<p class="ladder-note">' + esc(l.note) + '</p>' : '');
    };
    F.ladders.forEach(function (l, li) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = l.mark + ' ' + l.name;
      b.addEventListener('click', function () {
        [].forEach.call(lchips.children, function (x) { x.classList.toggle('on', x === b); });
        showL(l);
      });
      lchips.appendChild(b);
      if (li === 0) b.click();
    });
    return;
  }

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function gColor(g) { return 'var(--folder-' + F.groups[g].stage + ')'; }

  // 그룹 중심
  F.groups.forEach(function (g, i) {
    g.idx = i;
    g.c = STAGE_POS[g.stage];
    g.label = g.stage + ' ' + SHORT[g.stage];
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
  var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'forest-svg', role: 'img', 'aria-label': '바이브 코딩 단계별 글을 점으로 그린 전체 지도. 1단계부터 9단계까지 점선 길로 이어진다' });
  var tip = document.createElement('div'); tip.className = 'forest-tip';
  wrap.appendChild(svg); wrap.appendChild(tip);

  // 막(幕) 띠
  // 큰 묶음 세 개: 이름은 모두 «무엇을 + 어떻게 하기»
  var acts = [['기초 다지기', '1~3단계', 30, 372], ['분야 넓히기', '4~5단계', 388, 600], ['에이전트 만들기', '6~9단계', 616, 990]];
  acts.forEach(function (a) {
    el('rect', { x: a[2], y: 34, width: a[3] - a[2], height: 380, rx: 22, fill: 'var(--border)', 'fill-opacity': .3, stroke: 'var(--muted)', 'stroke-opacity': .55, 'stroke-width': 2, 'stroke-dasharray': '7 6' }, svg);
    var t = el('text', { x: (a[2] + a[3]) / 2, y: 24, 'text-anchor': 'middle', class: 'glabel', 'font-size': 20, 'font-weight': 700, fill: 'var(--ink)' }, svg);
    t.textContent = a[0] + ' ';
    var r = el('tspan', { 'font-size': 14, 'font-weight': 400, fill: 'var(--muted)' }, t); r.textContent = a[1];
  });

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
    var ty = g.c[1] < 220 ? g.c[1] - rad - 22 : g.c[1] + rad + 22;
    var t = el('text', { x: g.c[0], y: ty, 'text-anchor': 'middle', class: 'glabel', 'font-size': 17, fill: 'var(--ink)' }, svg);
    t.textContent = g.label;
    var n = el('text', { x: g.c[0], y: ty + 17, 'text-anchor': 'middle', class: 'glabel', 'font-size': 13, fill: 'var(--muted)' }, svg);
    n.textContent = g.n + '편';
  });

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
  // 안내 칸: 단계 동그라미에 마우스를 대면 소분류가 보인다
  var panel = document.createElement('div'); panel.className = 'forest-panel';
  root.appendChild(wrap); root.appendChild(panel);
  var HINT = '<p>점에 마우스를 대면 제목, 누르면 그 글로 가요. 색 동그라미에 대면 소분류가 보여요.</p>';
  panel.innerHTML = HINT;

  halos.forEach(function (h) {
    var g = F.groups[+h.dataset.g];
    h.addEventListener('mouseenter', function () {
      h.setAttribute('opacity', .26);
      panel.innerHTML = '<p><strong>' + esc(g.name) + '</strong> — ' + g.n + '편 · <a href="posts.html#' + g.id + '">목록에서 보기</a></p><p>' +
        g.subs.map(function (s) { return esc(s.name) + ' <span style="color:var(--muted)">' + s.n + '</span>'; }).join(' · ') + '</p>';
    });
    h.addEventListener('mouseleave', function () { h.setAttribute('opacity', .12); });
  });

  var placed = false;
  requestAnimationFrame(function () { requestAnimationFrame(function () {
    place();
    if (len && !reduce) road.style.strokeDashoffset = 0;
  }); });
  setTimeout(function () { place(); if (len && !reduce) road.style.strokeDashoffset = 0; }, 400);
})();
