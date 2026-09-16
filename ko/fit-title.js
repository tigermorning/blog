(function () {
  var h1 = document.querySelector('main h1');
  if (!h1 || h1.classList.contains('greeting')) return;
  var container = h1.parentElement;

  function shrinkToFit() {
    h1.style.whiteSpace = 'nowrap';
    var size = parseFloat(getComputedStyle(h1).fontSize);
    var minSize = 20;
    while (h1.scrollWidth > container.clientWidth && size > minSize) {
      size -= 1;
      h1.style.fontSize = size + 'px';
    }
    if (h1.scrollWidth > container.clientWidth) {
      // 그래도 한 줄에 안 들어가면 억지로 구겨넣지 않고 줄바꿈을 허용한다
      h1.style.whiteSpace = 'normal';
    }
  }

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(shrinkToFit);
  } else {
    shrinkToFit();
  }
})();

(function () {
  // 좁은 화면에서 인라인 다이어그램이 통째로 줄어들면 글자가 5px까지 작아져 못 읽는다.
  // 그림을 가로 스크롤 상자에 담아, 화면이 좁을 때는 최소 폭을 지키고 옆으로 밀어 보게 한다.
  var MIN_WIDTH = 640;   // 이 폭 아래로는 줄이지 않는다
  var svgs = document.querySelectorAll('main svg');
  for (var i = 0; i < svgs.length; i++) {
    var svg = svgs[i];
    var vb = svg.getAttribute('viewBox');
    if (!vb) continue;                                  // 뷰박스 없는 장식용은 건너뛴다
    var w = parseFloat(vb.split(/[\s,]+/)[2]);
    if (!(w >= 400)) continue;                          // 원래 작은 그림은 그대로 둔다
    if (svg.parentNode && svg.parentNode.className === 'fig-scroll') continue;
    var box = document.createElement('div');
    box.className = 'fig-scroll';
    box.setAttribute('tabindex', '0');                  // 키보드로도 밀어 볼 수 있게
    svg.parentNode.insertBefore(box, svg);
    box.appendChild(svg);
  }
})();
