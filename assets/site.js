/* Site chrome: close menus on outside click / Escape, highlight the current TOC entry, copy-link buttons. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    document.querySelectorAll('details.dd[open]').forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute('open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.querySelectorAll('details.dd[open]').forEach(function (d) { d.removeAttribute('open'); });
  });
  var toc = document.querySelectorAll('.toc a[href^="#"]');
  if (toc.length && 'IntersectionObserver' in window) {
    var map = {};
    toc.forEach(function (a) { var el = document.getElementById(a.getAttribute('href').slice(1)); if (el) map[el.id] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { toc.forEach(function (a) { a.classList.remove('on'); }); if (map[en.target.id]) map[en.target.id].classList.add('on'); } });
    }, { rootMargin: '0px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }
  document.querySelectorAll('[data-copy-link]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = location.href.split('#')[0], msg = b.getAttribute('data-copy-link'), o = b.innerHTML;
      var done = function () { b.textContent = msg; setTimeout(function () { b.innerHTML = o; }, 1600); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(url).then(done); else { var t = document.createElement('textarea'); t.value = url; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); done(); } catch (e) {} t.remove(); }
    });
  });
})();
