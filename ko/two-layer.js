(function () {
  var all = document.querySelectorAll('details.deep');
  function openFor(id) {
    var t = id && document.getElementById(id);
    if (!t) return;
    var d = t.closest('details.deep');
    if (!d) { d = t.nextElementSibling; while (d && d.tagName !== 'DETAILS' && d.tagName !== 'H2') d = d.nextElementSibling; if (d && d.tagName !== 'DETAILS') d = null; }
    if (d) { d.open = true; t.scrollIntoView(); }
  }
  window.addEventListener('hashchange', function () { openFor(location.hash.slice(1)); });
  openFor(location.hash.slice(1));
  var b = document.getElementById('deep-all');
  if (b) b.addEventListener('click', function () {
    var open = b.textContent === '모두 펼치기';
    all.forEach(function (d) { d.open = open; });
    b.textContent = open ? '모두 접기' : '모두 펼치기';
  });
})();
