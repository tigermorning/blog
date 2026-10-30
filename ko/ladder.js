// 공부 사다리: ladder-data.js 의 관계(다음·더하기·갈래)를 그린다. 글 제목·단계는 forest-data.js 에서 가져온다.
(function () {
  var L = window.LADDERS, F = window.FOREST;
  var root = document.getElementById('ladder');
  if (!L || !F || !root) return;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var info = {};
  F.posts.forEach(function (p, i) { info[p.f] = { t: p.t, stage: F.groups[p.g].stage, i: i }; });

  function card(s, n) {
    var p = info[s.f] || { t: s.f, stage: 0 };
    var sc = p.stage ? 'var(--folder-' + p.stage + ')' : 'var(--muted)';
    return '<a class="lc" href="' + s.f + '.html" style="--sc:' + sc + '">' +
      (n ? '<span class="lc-n">' + n + '</span>' : '') +
      '<span class="lc-t">' + esc(s.title) + '</span><span class="lc-tag">' + esc(s.tag) + '</span>' +
      '<span class="lc-post">' + esc(p.t) + '</span>' + (p.stage ? '<span class="lc-st">' + p.stage + '단계 글</span>' : '') + '</a>';
  }
  function edge(e) {
    return '<span class="le le-' + e.to + '" aria-hidden="true"><span class="le-l">' + (e.to === 'add' ? '＋ ' : '') + esc(e.label || '') + '</span></span>';
  }
  function seq(items) {
    return items.map(function (x) {
      if (x.to) return edge(x);
      if (x.choose) {
        return '<div class="lch"><p class="lch-q">' + esc(x.choose) + '<small>하나를 골라요</small></p>' +
          x.options.map(function (o) {
            return '<div class="lch-o"><span class="lch-w">' + esc(o.when) + '</span><div class="lrow">' + seq(o.steps) + '</div></div>';
          }).join('') + '</div>';
      }
      return card(x);
    }).join('');
  }
  function flat(items, out) {
    items.forEach(function (x) {
      if (x.f) out.push(x);
      if (x.choose) x.options.forEach(function (o) { flat(o.steps, out); });
    });
    return out;
  }

  var view = 'rel';
  var tabs = document.createElement('div'); tabs.className = 'forest-modes';
  var chips = document.createElement('div'); chips.className = 'forest-chips ladder-chips';
  var board = document.createElement('div'); board.className = 'ladder-board';
  root.appendChild(chips); root.appendChild(tabs); root.appendChild(board);
  var cur = L[0];
  [['rel', '관계대로'], ['order', '읽는 순서대로']].forEach(function (m) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = m[1]; b.dataset.v = m[0];
    b.addEventListener('click', function () { view = m[0]; draw(); });
    tabs.appendChild(b);
  });
  function ordered(l) {
    return flat(l.flow, []).slice().sort(function (a, b) { return (info[a.f] ? info[a.f].i : 0) - (info[b.f] ? info[b.f].i : 0); });
  }
  // 갈래가 없고 칸 순서가 글 목록 순서와 같으면 두 보기가 사실상 같다 → 관계대로 하나만 보여 준다
  function same(l) {
    var rel = flat(l.flow, []).map(function (s) { return s.f; }).join();
    var plain = l.flow.every(function (x) { return !x.choose; });
    return plain && rel === ordered(l).map(function (s) { return s.f; }).join();
  }
  function draw() {
    var both = !same(cur);
    if (!both) view = 'rel';
    tabs.hidden = !both;
    [].forEach.call(tabs.children, function (b) { b.classList.toggle('on', b.dataset.v === view); });
    var h = '<p class="ladder-head">' + esc(cur.mark + ' ' + cur.name) + '</p>';
    if (view === 'rel') {
      h += '<p class="ladder-legend"><span class="lg lg-next">→ 다음</span><span class="lg lg-add">＋→ 앞 것에 더하기</span><span class="lg lg-ch">▤ 갈래: 상황에 맞게 하나</span></p>';
      h += '<div class="lrow ltop">' + seq(cur.flow) + '</div>';
    } else {
      h += '<p class="ladder-legend">같은 글들을 글 목록에 놓인 순서대로 늘어놓았어요. 처음부터 차례로 읽을 때 쓰세요.</p><ol class="lorder">' +
        ordered(cur).map(function (s) {
          var p = info[s.f] || { t: s.f, stage: 0 };
          var sc = p.stage ? 'var(--folder-' + p.stage + ')' : 'var(--muted)';
          return '<li style="--sc:' + sc + '"><a href="' + s.f + '.html"><span class="lo-t">' + esc(p.t) + '</span>' +
            '<span class="lo-tag">' + esc(s.tag) + '</span>' + (p.stage ? '<span class="lc-st">' + p.stage + '단계 글</span>' : '') + '</a></li>';
        }).join('') + '</ol>';
    }
    board.innerHTML = h;
  }
  L.forEach(function (l) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = l.mark + ' ' + l.name;
    b.addEventListener('click', function () {
      cur = l;
      [].forEach.call(chips.children, function (x) { x.classList.toggle('on', x === b); });
      draw();
    });
    chips.appendChild(b);
  });
  chips.firstChild.classList.add('on');
  draw();
})();
