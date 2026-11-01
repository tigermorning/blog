// figure.motion 이 화면에 절반쯤 들어오면 한 번 재생하고, 누르면 처음부터 다시 재생한다.
(function () {
  var figs = document.querySelectorAll('figure.motion');
  if (!figs.length) return;
  document.documentElement.classList.add('mo-js');
  function play(fig) {
    fig.classList.remove('is-on');
    void fig.getBoundingClientRect();
    fig.classList.add('is-on');
  }
  figs.forEach(function (fig) {
    var cap = fig.querySelector('figcaption');
    if (cap && !fig.querySelector('.mo-replay')) {
      var hint = document.createElement('span');
      hint.className = 'mo-replay';
      hint.textContent = '↻ 그림을 누르면 다시 재생돼요';
      cap.appendChild(hint);
    }
    fig.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      play(fig);
    });
  });
  if (!('IntersectionObserver' in window)) {
    figs.forEach(play);
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { play(en.target); io.unobserve(en.target); }
    });
  }, { threshold: 0.45 });
  figs.forEach(function (fig) { io.observe(fig); });
})();
