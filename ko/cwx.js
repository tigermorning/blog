/* 코드가 실행되는 과정을 한 단계씩 보여 주는 그림(모션 그래픽) 공용 코드.
   사용: <div id="아이디"></div> 뒤에 cwx('아이디', {label, code:[...], steps:[{c, s, t, p}], stateTitle}) 를 부른다.
   steps 의 각 항목: c = 강조할 코드 줄 번호(-1 이면 없음), s = 지금 상태를 그리는 HTML, t = 설명(HTML), p = 이 단계에서 화면에 찍히는 글자(있으면 결과 칸에 쌓인다). */
(function(){
  var css = [
    '.cw{border:2px solid var(--cw-border);border-radius:14px;background:#fff;padding:.9rem;margin:1rem 0;font-size:.92rem}',
    '.cw{--cw-border:#ece4d6;--cw-muted:#8a8177;--cw-ink:#3b3630;--cw-hit-bg:#dff7ea;--cw-hit-ink:#1f7a52;color:#3b3630;line-height:1.5}',
    '.cw *{box-sizing:border-box}',
    '.cw-col{min-width:0}',
    '.cw-col h4{margin:0 0 .4rem;font-size:.8rem;color:var(--cw-muted);font-weight:400;letter-spacing:.02em}',
    ".cw-code{background:#3a3631;border-radius:10px;padding:.5rem 0;font-family:Consolas,'D2Coding',monospace;font-size:.8rem;color:#f5efe4;overflow-x:auto}",
    '.cw-code div{padding:.15rem .6rem;white-space:pre;border-left:4px solid transparent;transition:background .25s,border-color .25s}',
    '.cw-code div.on{background:#5a4a2f;border-left-color:#ffd166}',
    '.cw-chip{border:2px solid var(--cw-border);border-radius:8px;padding:.18rem .4rem;font-size:.8rem;background:#fffaf0;transition:all .25s;color:var(--cw-ink);word-break:break-all}',
    '.cw-chip mark{background:#ffd166;color:#3b3630;border-radius:3px;padding:0 1px}',
    '.cw-chip.cur{border-color:#ff9f1c;box-shadow:0 0 0 3px #ffe2a8}',
    '.cw-chip.hit{background:var(--cw-hit-bg);border-color:#9bd9b8;color:var(--cw-hit-ink)}',
    '.cw-chip.miss{background:#f3efe8;color:#a39a8c}',
    ".cw-out{background:#3a3631;color:#f5efe4;border-radius:10px;padding:.4rem .6rem;font-family:Consolas,'D2Coding',monospace;font-size:.8rem;white-space:pre;overflow-x:auto}",
    '.cw-out .last{color:#ffd166}',
    '.cw-cap{margin:.8rem 0 .5rem;padding:.55rem .75rem;border-radius:10px;background:#fff4dc;min-height:3.1rem;line-height:1.5}',
    '.cw-bar{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}',
    '.cw-bar button{font:inherit;border:2px solid var(--cw-ink);background:#fff;border-radius:999px;padding:.2rem .85rem;cursor:pointer;color:var(--cw-ink)}',
    '.cw-bar button:hover{background:#ffe2a8}',
    '.cw-prog{margin-left:auto;color:var(--cw-muted);font-size:.8rem}',
    '.cwx-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:.8rem}',
    '.cwx-state{display:flex;flex-direction:column;gap:.5rem}',
    '.cwx-box{border:2px solid var(--cw-border);border-radius:10px;background:#fffaf0;padding:.3rem .55rem;transition:background .25s,border-color .25s}',
    '.cwx-box b{display:block;font-weight:400;color:var(--cw-muted);font-size:.75rem}',
    ".cwx-txt{font-family:Consolas,'D2Coding',monospace;font-size:.8rem;white-space:pre-wrap;color:var(--cw-ink);min-height:1.2rem;word-break:break-all}",
    '.cwx-txt mark{background:#ffd166;color:#3b3630;border-radius:3px;padding:0 1px}',
    '.cwx-box.flash{border-color:#ff9f1c;background:#fff1cf}',
    '.cwx-box.warn{border-color:#ff8a8f;background:#ffe3e4}',
    '.cwx-box .empty{color:#a39a8c}',
    '.cwx-chips{display:grid;grid-template-columns:repeat(auto-fill,minmax(7.4rem,1fr));gap:.3rem}',
    '.cwx-chips.one{grid-template-columns:1fr}',
    '.cwx-out{min-height:4.2rem}',
    '@media (max-width:640px){.cwx-grid{grid-template-columns:minmax(0,1fr)}}',
    '@media (prefers-reduced-motion:reduce){.cw *{transition:none!important}}'
  ].join('\n');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  function cwx(id, o){
    var root = document.getElementById(id); if(!root) return;
    var steps = o.steps, out = [], usesOut = false;
    steps.forEach(function(s){ if(s.p !== undefined){ out.push(s.p); usesOut = true; } s.out = out.slice(); });
    root.className = 'cw'; root.setAttribute('role','group'); root.setAttribute('aria-label', o.label);
    root.innerHTML = '<div class="cwx-grid"><div class="cw-col"><h4>코드</h4><div class="cw-code"></div></div>' +
      '<div class="cw-col"><h4>' + (o.stateTitle || '지금 상태') + '</h4><div class="cwx-state"></div>' +
      (usesOut ? '<h4 style="margin-top:.6rem">화면에 찍힌 결과</h4><div class="cw-out cwx-out"></div>' : '') +
      '</div></div><div class="cw-cap"></div><div class="cw-bar"><button type="button" class="b-play"></button>' +
      '<button type="button" class="b-step" aria-label="한 단계 앞으로">한 단계 ▶</button>' +
      '<button type="button" class="b-reset" aria-label="처음부터 다시">↺ 처음부터</button><span class="cw-prog"></span></div>';
    var q = function(c){ return root.querySelector(c); }, codeEl = q('.cw-code'), rows = [];
    o.code.forEach(function(t){ var d = document.createElement('div'); d.textContent = t; codeEl.appendChild(d); rows.push(d); });
    var cur = 0, timer = null;
    function show(k){
      var s = steps[k]; cur = k;
      rows.forEach(function(r, j){ r.className = (j === s.c) ? 'on' : ''; });
      q('.cwx-state').innerHTML = s.s; q('.cw-cap').innerHTML = s.t;
      q('.cw-prog').textContent = (k+1) + ' / ' + steps.length + ' 단계';
      if(usesOut){ q('.cwx-out').innerHTML = s.out.map(function(t, j){ var e = esc(t); return j === s.out.length-1 ? '<span class="last">' + e + '</span>' : e; }).join('\n'); }
    }
    function next(){ if(cur < steps.length-1){ show(cur+1); } else { stop(); } }
    function play(){ if(timer) return; if(cur >= steps.length-1) show(0); timer = setInterval(next, 1400); q('.b-play').textContent = '⏸ 멈춤'; }
    function stop(){ if(timer){ clearInterval(timer); timer = null; } q('.b-play').textContent = (cur >= steps.length-1) ? '↻ 다시 재생' : '▶ 재생'; }
    q('.b-play').onclick = function(){ timer ? stop() : play(); };
    q('.b-step').onclick = function(){ stop(); if(cur >= steps.length-1) show(0); else show(cur+1); };
    q('.b-reset').onclick = function(){ stop(); show(0); };
    show(0); stop();
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(!reduce && 'IntersectionObserver' in window){
      var seen = false;
      new IntersectionObserver(function(es){ es.forEach(function(e){
        if(e.isIntersecting && !seen){ seen = true; play(); }
        if(!e.isIntersecting && timer){ stop(); }
      }); }, {threshold: .5}).observe(root);
    }
  }
  cwx.esc = esc;
  /* 이름표가 달린 글자 상자. text 가 null 이면 '(파일 없음)', 빈 글자면 '(비어 있음)'. cls 에 raw 가 있으면 줄 바꿈 표시(↵)를 붙이지 않는다. */
  cwx.box = function(label, text, cls){
    var t = (text === null) ? '<span class="empty">(파일 없음)</span>' : (text === '' ? '<span class="empty">(비어 있음)</span>' : esc(text).replace(/\n/g, (cls && cls.indexOf('raw') >= 0) ? '\n' : '↵\n'));
    return '<div class="cwx-box ' + (cls || '') + '"><b>' + label + '</b><div class="cwx-txt">' + t + '</div></div>';
  };
  /* html 을 그대로 넣는 상자(강조 표시용) */
  cwx.boxHtml = function(label, html, cls){
    return '<div class="cwx-box ' + (cls || '') + '"><b>' + label + '</b><div class="cwx-txt">' + html + '</div></div>';
  };
  cwx.chips = function(arr, o){
    o = o || {};
    return '<div class="cwx-chips' + (o.one ? ' one' : '') + '">' + arr.map(function(t, i){
      var c = 'cw-chip'; if(o.hi && o.hi.indexOf(i) >= 0) c += ' hit'; if(o.read !== undefined && i < o.read) c += ' hit'; if(o.cur === i) c += ' cur';
      return '<div class="' + c + '">' + (o.idx ? i + ': ' : '') + (o.ptr === i ? '▶ ' : '') + esc(t) + '</div>';
    }).join('') + '</div>';
  };
  window.cwx = cwx;
})();
