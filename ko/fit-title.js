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
  // 그림을 가로 스크롤 상자에 담고, 가장 작은 글자가 최소 10px로 보이는 폭을 그림마다 계산해
  // --fig-min 으로 넘긴다. 실제 적용은 style.css 의 좁은 화면 규칙이 한다.
  var TARGET_PX = 10;   // 이 크기보다 작게는 안 줄인다
  var MAX_WIDTH = 1100; // 너무 넓어져 한없이 밀지 않도록 상한

  function needWidth(svg, viewBoxWidth) {
    var texts = svg.querySelectorAll('text');
    var smallest = Infinity;
    for (var i = 0; i < texts.length; i++) {
      var px = parseFloat(getComputedStyle(texts[i]).fontSize);
      if (px > 0 && px < smallest) smallest = px;
    }
    if (!isFinite(smallest)) return 0;
    // viewBox 안의 글자 크기가 smallest 이므로, 그림 폭이 W 일 때 화면에 보이는 크기는
    // smallest * (W / viewBoxWidth) 다. 이것이 TARGET_PX 가 되는 W 를 구한다.
    return Math.min(viewBoxWidth * (TARGET_PX / smallest), MAX_WIDTH);
  }

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
    var need = needWidth(svg, w);
    if (need > 0) box.style.setProperty('--fig-min', Math.round(need) + 'px');
  }
})();
