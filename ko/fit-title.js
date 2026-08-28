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
