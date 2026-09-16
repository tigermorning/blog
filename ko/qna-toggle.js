(function () {
  // 질문 하나하나를 <details class="qna">로 접어 둔 글에서 쓴다.
  // 목차 링크(#q3)나 본문 안 앵커(#q3-power)로 들어오면 감싼 질문을 먼저 펼친 뒤 그 자리로 옮긴다.
  var items = document.querySelectorAll('details.qna');
  if (!items.length) return;

  function reveal(hash) {
    if (!hash || hash.length < 2) return;
    var target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!target) return;
    for (var el = target; el; el = el.parentElement) {
      if (el.tagName === 'DETAILS') el.open = true;
    }
    target.scrollIntoView();
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (a) {
      // 같은 해시를 다시 누르면 hashchange가 안 생기므로 여기서 직접 펼친다
      reveal(a.getAttribute('href'));
      return;
    }
    var btn = e.target.closest('[data-qna]');
    if (!btn) return;
    var open = btn.getAttribute('data-qna') === 'open';
    for (var i = 0; i < items.length; i++) items[i].open = open;
  });

  window.addEventListener('hashchange', function () { reveal(location.hash); });
  reveal(location.hash);

  // 인쇄할 때는 접힌 내용이 빠지지 않게 전부 펼친다
  window.addEventListener('beforeprint', function () {
    for (var i = 0; i < items.length; i++) items[i].open = true;
  });
})();
