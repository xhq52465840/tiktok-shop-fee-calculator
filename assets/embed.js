/* SellerFee embed loader: https://sellerfee.app/en/embed/ */
(function () {
  'use strict';
  var me = document.currentScript, m = me && me.src.match(/^https?:\/\/[^\/]+/), origin = m ? m[0] : 'https://sellerfee.app';
  var frames = [];
  function mount(el) {
    if (el.getAttribute('data-sf-done')) return;
    var calc = (el.getAttribute('data-calc') || '').replace(/^\/+|\/+$/g, ''), lang = el.getAttribute('data-lang') || 'en';
    if (!/^[a-z0-9-]+(\/[a-z0-9-]+)?$/.test(calc)) return;
    if (!/^(en|zh|ru|ms)$/.test(lang)) lang = 'en';
    el.setAttribute('data-sf-done', '1');
    var f = document.createElement('iframe');
    f.src = origin + '/' + lang + '/embed/' + calc + '/';
    f.title = el.getAttribute('data-title') || 'Seller fee calculator by sellerfee.app';
    f.setAttribute('loading', 'lazy'); f.setAttribute('allow', 'clipboard-write');
    f.style.cssText = 'display:block;width:100%;max-width:100%;border:0;overflow:hidden;color-scheme:light;height:' + (parseInt(el.getAttribute('data-height'), 10) || 1900) + 'px';
    el.insertBefore(f, el.firstChild); frames.push(f);
  }
  window.addEventListener('message', function (e) {
    if (e.origin !== origin || !e.data || e.data.sellerfee !== 'height') return;
    for (var i = 0; i < frames.length; i++) if (frames[i].contentWindow === e.source) frames[i].style.height = Math.max(200, e.data.h | 0) + 'px';
  });
  function run() { var l = document.querySelectorAll('.sellerfee-embed[data-calc]'); for (var i = 0; i < l.length; i++) mount(l[i]); }
  run();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  window.SellerFeeEmbed = { mount: run };
})();
