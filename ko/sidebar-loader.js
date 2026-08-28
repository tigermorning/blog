(function () {
  var mount = document.getElementById('sidebar-mount');
  if (!mount) return;
  fetch('_sidebar.html')
    .then(function (r) { return r.text(); })
    .then(function (html) { mount.outerHTML = html; })
    .catch(function () {});
})();
