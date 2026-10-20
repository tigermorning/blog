/* svg.flow-motion: 박스에 순서대로 지연값을 주고, 화면에 보일 때만 재생한다 */
(function () {
  var svgs = document.querySelectorAll('svg.flow-motion');
  if (!svgs.length) return;
  svgs.forEach(function (svg) {
    var boxes = svg.querySelectorAll('rect');
    var step = 0.9;
    svg.style.setProperty('--fm-cycle', (boxes.length * step + 2) + 's');
    boxes.forEach(function (r, i) {
      r.classList.add('fm-box');
      r.style.setProperty('--fm-delay', (i * step) + 's');
    });
    svg.querySelectorAll('line, path').forEach(function (l) {
      if (l.closest('marker')) return;
      l.classList.add('fm-line');
    });
  });
  if (!('IntersectionObserver' in window)) { svgs.forEach(function (s) { s.classList.add('fm-on'); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { e.target.classList.toggle('fm-on', e.isIntersecting); });
  }, { threshold: 0.3 });
  svgs.forEach(function (s) { io.observe(s); });
})();
