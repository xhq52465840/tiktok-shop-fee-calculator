/* Push AdSense for each manual <ins class="adsbygoogle"> once the library is ready. */
(function () {
  'use strict';
  function pushAll() {
    var nodes = document.querySelectorAll('ins.adsbygoogle');
    if (!nodes.length) return;
    window.adsbygoogle = window.adsbygoogle || [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute('data-adsbygoogle-status')) continue;
      try { window.adsbygoogle.push({}); } catch (e) {}
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pushAll);
  } else {
    pushAll();
  }
})();
