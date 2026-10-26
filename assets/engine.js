/* SellerFee calculator engine. Reads a market definition (window.SF_MARKET) and UI strings (window.SF_T).
   A market lists its inputs, selectors, toggles and fee components; adding a market needs only a new data file. */
(function () {
  'use strict';
  var M = window.SF_MARKET, T = window.SF_T || {};
  if (!M) return;
  var $ = function (id) { return document.getElementById(id); };
  var root = $('sf-calc');
  var num = function (id) { var e = $(id); if (!e) return 0; var v = parseFloat(e.value); return isFinite(v) ? v : 0; };
  var r2 = function (n) { return Math.round(parseFloat((n * 100).toPrecision(12))) / 100; };
  var t = function (k, d) { return T[k] || d; };
  var cur = M.currency;
  function money(n) {
    var dec = M.decimals === undefined ? 2 : M.decimals;
    var s = Math.abs(n).toLocaleString(M.locale || 'en', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    return (n < 0 ? '\u2212' : '') + (M.symbols && M.symbols[cur] || cur + ' ') + s;
  }
  var sel = M.selector, opts = sel.options;

  // ----- state
  function state() {
    var s = { sel: +$('sf-sel').value, period: $('sf-period') ? $('sf-period').value : null, store: null, tg: {} };
    var st = root.querySelector('input[name=sf-store]:checked'); s.store = st ? st.value : null;
    (M.toggles || []).forEach(function (g) { var e = $('sf-t-' + g.id); s.tg[g.id] = !!(e && e.checked); });
    return s;
  }
  function keyFor(tpl, s) {
    return tpl.replace('{period}', s.period).replace('{store}', s.store).replace(/\{(\w+)\}/g, function (_, id) {
      var g = (M.toggles || []).filter(function (x) { return x.id === id; })[0];
      return g ? g.vals[s.tg[id] ? 1 : 0] : '';
    });
  }
  function active(c, s) {
    if (c.when && !s.tg[c.when]) return false;
    if (c.whenStore && c.whenStore !== s.store) return false;
    return true;
  }
  // default rate for a component in a given state (null = not published)
  function defRate(c, s) {
    if (!active(c, s)) return 0;
    if (c.zeroIf && s.tg[c.zeroIf]) return 0;
    var r = c.rate;
    if (typeof r === 'string' && r.indexOf('opt:') === 0) r = opts[s.sel].r[keyFor(r.slice(4), s)];
    if (r && typeof r === 'object') r = r[s.store];
    (c.rateIf || []).forEach(function (x) { if (s.tg[x.t]) r = x.rate; });
    return r === undefined ? null : r;
  }
  function defaults(s) { var o = {}; M.components.forEach(function (c) { o[c.id] = defRate(c, s); }); return o; }

  function readInputs() {
    var o = { price: num('sf-price'), qty: Math.max(1, Math.round(num('sf-qty')) || 1), sellerDisc: num('sf-sellerDisc'),
      buyerShip: num('sf-buyerShip'), shipCost: num('sf-shipCost'), cost: num('sf-cost'), other: num('sf-other'),
      affPct: num('sf-affPct'), tax: num('sf-tax') };
    return o;
  }
  function bases(o) {
    var net = Math.max(0, o.price * o.qty - o.sellerDisc);
    return { net: net, net_ship: net + o.buyerShip, gross: net + o.buyerShip + o.tax };
  }
  // compute fees for inputs o, rates map, state s
  function compute(o, rates, s) {
    var b = bases(o), rows = [];
    M.components.forEach(function (c) {
      if (!active(c, s)) return;
      var raw = rates[c.id], r = raw; if (r === null || r === undefined || isNaN(r)) r = 0;
      var amt, how;
      if (c.type === 'fixed') {
        var n = c.per === 'item' ? o.qty : 1;
        amt = r * n; how = c.per === 'item' ? money(r) + ' \u00D7 ' + o.qty : t('flat', 'Flat per order');
      } else {
        var base = b[c.base || 'net'];
        amt = base * r / 100; how = fmtPct(r) + ' \u00D7 ' + money(base);
        if (c.tier) {
          var over = opts[s.sel].r[c.tier.key];
          if (over !== undefined && base > c.tier.threshold) {
            amt = c.tier.threshold * r / 100 + (base - c.tier.threshold) * over / 100;
            how += ' (' + fmtPct(over) + ' ' + t('above', 'above') + ' ' + money(c.tier.threshold) + ')';
          }
        }
        if (c.capPerItem) {
          var cap = c.capPerItem * o.qty;
          if (amt > cap) { amt = cap; how += ' \u2192 ' + t('capped', 'capped at') + ' ' + money(c.capPerItem) + '/' + t('item', 'item'); }
        }
      }
      if (c.type === 'fixed' && r === 0) how = (raw === null || raw === undefined || isNaN(raw)) ? t('notSet', 'Not set, see note above') : t('waived', 'Waived');
      rows.push({ id: c.id, label: c.label, how: how, amt: r2(amt), color: c.color });
    });
    if (o.affPct > 0) rows.push({ id: 'aff', label: t('aff', 'Affiliate creator commission'), how: fmtPct(o.affPct) + ' \u00D7 ' + money(b.net), amt: r2(b.net * o.affPct / 100), color: '#a78bfa' });
    var total = r2(rows.reduce(function (x, r) { return x + r.amt; }, 0));
    var payout = r2(b.net_ship - o.shipCost - total);
    var goods = r2(o.cost * o.qty + o.other);
    var profit = r2(payout - goods);
    return { b: b, rows: rows, total: total, payout: payout, goods: goods, profit: profit, margin: b.net > 0 ? profit / b.net * 100 : 0 };
  }
  function fmtPct(r) { return (Math.round(r * 100) / 100) + '%'; }

  function fill() {
    var s = state(), d = defaults(s);
    M.components.forEach(function (c) {
      var e = $('sf-r-' + c.id); if (!e) return;
      e.value = d[c.id] === null ? '' : d[c.id];
      e.closest('.sf-rate').hidden = !active(c, s);
    });
    var opt = opts[s.sel];
    if (M.currencyFromOption) { cur = opt.cur; root.querySelectorAll('.sf-cur').forEach(function (x) { x.textContent = cur; }); }
    var note = '';
    M.components.forEach(function (c) { if (active(c, s) && d[c.id] === null) note = t('noRate', 'No published rate for this selection. Enter the rate from your Seller Center.'); });
    if (opt.note && T['note_' + opt.note]) note = T['note_' + opt.note];
    $('sf-selnote').textContent = note;
    (M.toggles || []).forEach(function (g) { if (g.requires) { var e = $('sf-t-' + g.id); e.disabled = !s.tg[g.requires]; if (e.disabled) e.checked = false; } });
    calc();
  }
  function readRates() { var o = {}; M.components.forEach(function (c) { var e = $('sf-r-' + c.id); o[c.id] = e && e.value !== '' ? parseFloat(e.value) : null; }); return o; }

  function calc() {
    var s = state(), o = readInputs(), f = compute(o, readRates(), s);
    $('sf-k-profit').textContent = money(f.profit);
    $('sf-k-profit').className = 'sf-big ' + (f.profit < 0 ? 'neg' : 'pos');
    $('sf-k-margin').textContent = t('margin', 'Margin') + ' ' + f.margin.toFixed(1) + '%';
    $('sf-k-margin').className = 'sf-pill ' + (f.profit < 0 ? 'neg' : f.margin < 10 ? 'warn' : 'pos');
    $('sf-k-fees').textContent = money(f.total);
    $('sf-k-feespct').textContent = f.b.net > 0 ? (f.total / f.b.net * 100).toFixed(1) + '% ' + t('ofSub', 'of item subtotal') : '';
    $('sf-k-payout').textContent = money(f.payout);
    // bar
    var gross = Math.max(f.b.net_ship, 0.0001), parts = [];
    f.rows.forEach(function (r) { parts.push([r.label, r.amt, r.color || '#f97316']); });
    if (o.shipCost) parts.push([t('shipCost', 'Shipping you pay'), o.shipCost, '#94a3b8']);
    if (f.goods) parts.push([t('goods', 'Product & other costs'), f.goods, '#475569']);
    if (f.profit > 0) parts.push([t('profit', 'Profit'), f.profit, '#10b981']);
    var tot = parts.reduce(function (x, p) { return x + p[1]; }, 0) || 1;
    $('sf-bar').innerHTML = parts.map(function (p) { return '<span style="width:' + (p[1] / tot * 100).toFixed(2) + '%;background:' + p[2] + '" title="' + p[0] + ': ' + money(p[1]) + '"></span>'; }).join('');
    $('sf-legend').innerHTML = parts.map(function (p) { return '<li><i style="background:' + p[2] + '"></i>' + p[0] + ' <b>' + (p[1] / tot * 100).toFixed(1) + '%</b></li>'; }).join('');
    // breakdown
    var h = '<tr><td>' + t('subtotal', 'Item subtotal after your discount') + '<small>' + money(o.price) + ' \u00D7 ' + o.qty + (o.sellerDisc ? ' \u2212 ' + money(o.sellerDisc) : '') + '</small></td><td class="n">' + money(f.b.net) + '</td></tr>';
    if (o.buyerShip) h += '<tr><td>' + t('buyerShip', 'Shipping paid by buyer') + '</td><td class="n">+' + money(o.buyerShip) + '</td></tr>';
    f.rows.forEach(function (r) { h += '<tr><td><i class="dot" style="background:' + (r.color || '#f97316') + '"></i>' + r.label + '<small>' + r.how + '</small></td><td class="n neg">\u2212' + money(r.amt) + '</td></tr>'; });
    if (o.shipCost) h += '<tr><td>' + t('shipCost', 'Shipping you pay') + '</td><td class="n neg">\u2212' + money(o.shipCost) + '</td></tr>';
    h += '<tr class="tot"><td>' + t('payout', 'Estimated payout') + '</td><td class="n">' + money(f.payout) + '</td></tr>';
    h += '<tr><td>' + t('goods', 'Product & other costs') + '</td><td class="n neg">\u2212' + money(f.goods) + '</td></tr>';
    h += '<tr class="tot"><td>' + t('profit', 'Profit') + '</td><td class="n ' + (f.profit < 0 ? 'neg' : 'pos') + '">' + money(f.profit) + '</td></tr>';
    $('sf-breakdown').innerHTML = h;
    compare(o, s);
  }

  function compare(o, s) {
    var box = $('sf-compare'); if (!box || !M.compare) return;
    var C = M.compare;
    function side(x) {
      var s2 = JSON.parse(JSON.stringify(s)); if (x.state) Object.keys(x.state).forEach(function (k) { s2[k] = x.state[k]; });
      var r = readRates(), d = defaults(s2), na = false;
      (C.vary || []).forEach(function (k) { r[k] = d[k]; if (d[k] === null) na = true; });
      if (x.rates) Object.keys(x.rates).forEach(function (k) { if (r[k]) r[k] = x.rates[k]; });
      return { f: compute(o, r, s2), na: na };
    }
    var a = side(C.a), b = side(C.b);
    if (a.na || b.na) { box.innerHTML = '<p class="muted">' + t('cmpNa', 'No earlier rate is published for this selection.') + '</p>'; return; }
    var d = r2(b.f.profit - a.f.profit);
    box.innerHTML = '<table class="sf-cmp"><thead><tr><th></th><th class="n">' + C.a.label + '</th><th class="n">' + C.b.label + '</th></tr></thead><tbody>' +
      '<tr><td>' + t('fees', 'TikTok fees') + '</td><td class="n">' + money(a.f.total) + '</td><td class="n">' + money(b.f.total) + '</td></tr>' +
      '<tr><td>' + t('payout', 'Estimated payout') + '</td><td class="n">' + money(a.f.payout) + '</td><td class="n">' + money(b.f.payout) + '</td></tr>' +
      '<tr class="tot"><td>' + t('profit', 'Profit') + '</td><td class="n">' + money(a.f.profit) + '</td><td class="n">' + money(b.f.profit) + '</td></tr></tbody></table>' +
      '<p class="sf-delta ' + (d < 0 ? 'neg' : 'pos') + '">' + t('change', 'Change per order') + ': <b>' + (d > 0 ? '+' : '') + money(d) + '</b></p>' +
      (C.note ? '<p class="muted">' + C.note + '</p>' : '');
  }

  // ----- init
  var s0 = $('sf-sel');
  opts.forEach(function (c, i) { var e = document.createElement('option'); e.value = i; e.textContent = c.n; s0.appendChild(e); });
  s0.value = M.defaultOption || 0;
  root.addEventListener('change', function (e) { if (e.target.id && e.target.id.indexOf('sf-r-') === 0) calc(); else fill(); });
  root.addEventListener('input', function (e) { if (e.target.type === 'number') calc(); });
  fill();
  window.SF_compute = function (inputs, selIndex, extra) { // used by tests
    var s = state(); s.sel = selIndex; Object.assign(s, extra || {});
    var o = Object.assign({ price: 0, qty: 1, sellerDisc: 0, buyerShip: 0, shipCost: 0, cost: 0, other: 0, affPct: 0, tax: 0 }, inputs);
    return compute(o, defaults(s), s);
  };

  // searchable rate table
  var q = $('sf-filter');
  if (q) q.addEventListener('input', function () { var v = q.value.toLowerCase(); document.querySelectorAll('#sf-rates tbody tr').forEach(function (tr) { tr.hidden = tr.textContent.toLowerCase().indexOf(v) < 0; }); });
})();
