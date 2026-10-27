/* SellerFee calculator engine. Reads a market definition (window.SF_MARKET) and UI strings (window.SF_T).
   A market lists its inputs, selectors, toggles and fee components; adding a market needs only a new data file.
   Supported per component: pct / fixed / vol (stepped per-litre logistics) types, rates from the selected option
   (optionally by store, price band, extra select or "_" fallback), caps, rate adjustments, conditional tariffs. */
(function () {
  'use strict';
  var M = window.SF_MARKET, T = window.SF_T || {};
  if (!M) return;
  var $ = function (id) { return document.getElementById(id); };
  var root = $('sf-calc');
  var num = function (id) { var e = $(id); if (!e) return 0; var v = parseFloat(String(e.value).replace(',', '.')); return isFinite(v) ? v : 0; };
  var r2 = function (n) { return Math.round(parseFloat((n * 100).toPrecision(12))) / 100; };
  var r4 = function (n) { return Math.round(parseFloat((n * 10000).toPrecision(12))) / 10000; }; // rates keep up to 4 decimals (e.g. 7.085%)
  var t = function (k, d) { return T[k] || d; };
  var cur = M.currency, opts = [], touched = {};
  function money(n) {
    var dec = M.decimals === undefined ? 2 : M.decimals;
    var s = Math.abs(n).toLocaleString(M.locale || 'en', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    var sym = M.symbols && M.symbols[cur] || cur + ' ';
    return (n < 0 ? '\u2212' : '') + (M.symbolAfter ? s + '\u00A0' + sym : sym + s);
  }
  function fmt1(x) { return x.toLocaleString(M.locale || 'en', { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }
  function fmtPct(r) { return (Math.round(r * 1000) / 1000).toLocaleString(M.locale || 'en', { maximumFractionDigits: 3 }) + '%'; }
  function label(o) { return (o.g ? o.g + ' \u203A ' : '') + o.n; }

  // ----- state
  function state() {
    var s = { sel: +($('sf-sel').value || 0), period: $('sf-period') ? $('sf-period').value : null, store: null, tg: {}, x: {} };
    var st = root.querySelector('input[name=sf-store]:checked'); s.store = st ? st.value : null;
    (M.toggles || []).forEach(function (g) { var e = $('sf-t-' + g.id); s.tg[g.id] = !!(e && e.checked && !e.disabled); });
    (M.selects || []).forEach(function (x) { var e = $('sf-x-' + x.id); s.x[x.id] = e ? e.value : x.def; });
    return s;
  }
  function keyFor(tpl, s) {
    return tpl.replace('{period}', s.period).replace('{store}', s.store).replace(/\{x:(\w+)\}/g, function (_, id) { return s.x[id]; })
      .replace(/\{(\w+)\}/g, function (_, id) {
        var g = (M.toggles || []).filter(function (x) { return x.id === id; })[0];
        return g ? g.vals[s.tg[id] ? 1 : 0] : '';
      });
  }
  function inList(v, l) { return l === undefined || (Array.isArray(l) ? l.indexOf(v) >= 0 : l === v); }
  function active(c, s) {
    if (c.when && !s.tg[c.when]) return false;
    if (!inList(s.store, c.whenStore)) return false;
    if (c.whenX && s.x[c.whenX[0]] !== c.whenX[1]) return false;
    return true;
  }
  function unit(o) { var b = bases(o); return o.qty ? b.net / o.qty : 0; }
  function band(o) { var u = unit(o), i = 0; (M.bands || []).forEach(function (th) { if (u > th) i++; }); return i; }
  function condOn(name, s, o) {
    var c = (M.conds || {})[name]; if (!c) return false;
    if (!inList(s.store, c.stores)) return false;
    if (c.maxUnit !== undefined && unit(o) > c.maxUnit) return false;
    if (c.maxVol !== undefined && o.vol > c.maxVol) return false;
    return true;
  }
  function conds(s, o) { var r = {}; Object.keys(M.conds || {}).forEach(function (k) { r[k] = condOn(k, s, o); }); return r; }
  // default rate for a component in a given state (null = not published)
  function defRate(c, s, o) {
    if (!active(c, s)) return 0;
    if (c.zeroIf && s.tg[c.zeroIf]) return 0;
    var r = c.rate, cd = conds(s, o);
    if (typeof r === 'string' && r.indexOf('opt:') === 0) {
      var R = (opts[s.sel] || {}).r || {}, k = keyFor(r.slice(4), s);
      r = R[k] !== undefined ? R[k] : R._;
    }
    if (r && typeof r === 'object' && !Array.isArray(r)) r = r[c.by ? s.x[c.by] : s.store];
    if (Array.isArray(r)) r = r[Math.min(band(o), r.length - 1)];
    (c.rateIf || []).forEach(function (x) { if (s.tg[x.t]) r = x.rate; });
    var replaced = false;
    Object.keys(c.condRate || {}).forEach(function (k) { if (cd[k]) { r = c.condRate[k]; replaced = true; } });
    if (r === undefined || r === null) return null;
    if (!replaced) (c.adj || []).forEach(function (a) { if (a.t ? s.tg[a.t] : s.x[a.x] === a.v) r += a.d; });
    if (c.minRate !== undefined) r = Math.max(r, c.minRate);
    return r4(r);
  }
  function defaults(s, o) { var d = {}; M.components.forEach(function (c) { d[c.id] = defRate(c, s, o); }); return d; }

  function readInputs() {
    return { price: num('sf-price'), qty: Math.max(1, Math.round(num('sf-qty')) || 1), sellerDisc: num('sf-sellerDisc'),
      buyerShip: num('sf-buyerShip'), shipCost: num('sf-shipCost'), cost: num('sf-cost'), other: num('sf-other'),
      affPct: num('sf-affPct'), tax: num('sf-tax'), taxPct: num('sf-taxPct'), vol: num('sf-vol'), coef: $('sf-coef') ? num('sf-coef') : 100 };
  }
  function bases(o) {
    var net = Math.max(0, o.price * o.qty - o.sellerDisc);
    return { net: net, net_ship: net + o.buyerShip, gross: net + o.buyerShip + o.tax };
  }
  // per-item cost of a volume-based (per-litre) service
  function volCost(v, L) {
    if (!(L > 0)) return 0;
    if (v.ceil) L = Math.ceil(L - 1e-9);
    var p, tb = v.table || [];
    if (tb.length && L <= tb[tb.length - 1][0]) { for (var i = 0; i < tb.length; i++) if (L <= tb[i][0] + 1e-9) { p = tb[i][1]; break; } }
    else {
      p = v.first + v.per * Math.max(0, L - 1);
      (v.steps || []).forEach(function (st) { if (L > st[0]) p += (L - st[0]) * st[1]; });
    }
    if (v.cap !== undefined) p = Math.min(p, v.cap);
    return p;
  }
  function compute(o, rates, s) {
    var b = bases(o), rows = [], cd = conds(s, o);
    M.components.forEach(function (c) {
      if (!active(c, s)) return;
      var zeroCond = (c.condZero || []).filter(function (k) { return cd[k]; })[0];
      if (zeroCond) { rows.push({ id: c.id, label: c.label, how: t('cond_' + zeroCond + '_incl', 'Included'), amt: 0, color: c.color }); return; }
      var raw = rates[c.id], r = raw; if (r === null || r === undefined || isNaN(r)) r = 0;
      var amt, how, n;
      if (c.type === 'voltab') {
        var tb = (M.tables || {})[c.table], L = o.vol, bi = 0;
        if (!tb || !(L > 0)) { amt = 0; how = t('noVol', 'Enter the volume'); }
        else {
          while (bi < tb.upper.length - 1 && L > tb.upper[bi] + 1e-9) bi++;
          var fr = s.x[c.from], to = s.x[c.to], key = fr + '-' + to, arr = (fr !== '' && to !== '' && tb.routes[key]) || tb['default'];
          var routed = arr !== tb['default'], col = unit(o) > tb.bands[0] ? 1 : 0, pv = arr[bi][col];
          amt = pv * o.qty;
          var bl = (M.locale || '').indexOf('ru') === 0 ? tb.labels[bi] : '\u2264\u00A0' + tb.upper[bi].toLocaleString(M.locale || 'en') + '\u00A0' + t('litre', 'L');
          how = bl + ', ' + (routed ? tb.clusters[fr] + ' → ' + tb.clusters[to] : t('universal', 'universal tariff')) + ' → ' + money(pv) + (o.qty > 1 ? ' × ' + o.qty : '');
          if (!routed && fr !== '' && to !== '') how += ' (' + t('noRoute', 'no tariff for this route') + ')';
        }
      } else if (c.type === 'vol') {
        var per = volCost(c.vol, o.vol), mult = c.vol.mult ? o[c.vol.mult] / 100 : 1;
        amt = per * mult * o.qty;
        how = (o.vol > 0 ? (o.vol.toLocaleString(M.locale || 'en') + ' ' + t('litre', 'L') + ' \u2192 ' + money(per)) : t('noVol', 'Enter the volume')) +
          (c.vol.mult ? ' \u00D7 ' + fmtPct(o[c.vol.mult]) : '') + (o.qty > 1 ? ' \u00D7 ' + o.qty : '');
      } else if (c.type === 'fixed') {
        n = c.per === 'item' ? o.qty : 1;
        amt = r * n; how = c.per === 'item' ? money(r) + ' \u00D7 ' + o.qty : t('flat', 'Flat per order');
        if (r === 0) how = (raw === null || raw === undefined || isNaN(raw)) ? t('notSet', 'Not set, see note above') : (c.manual ? t('enterIt', 'Enter your amount') : t('waived', 'Waived'));
      } else {
        // base 'fees' = sum of the fee rows above (e.g. VAT charged on the platform's own fees)
        var base = c.base === 'fees' ? rows.reduce(function (x, q) { return x + q.amt; }, 0) : b[c.base || 'net'];
        amt = base * r / 100; how = fmtPct(r) + ' \u00D7 ' + money(base);
        if (c.tier) {
          var over = (opts[s.sel] || {}).r[c.tier.key];
          if (over !== undefined && base > c.tier.threshold) {
            amt = c.tier.threshold * r / 100 + (base - c.tier.threshold) * over / 100;
            how += ' (' + fmtPct(over) + ' ' + t('above', 'above') + ' ' + money(c.tier.threshold) + ')';
          }
        }
        if (c.capPerItem) {
          var capV = c.capPerItem;
          if (typeof capV === 'string' && capV.indexOf('opt:') === 0) {
            var RR = (opts[s.sel] || {}).r || {};
            capV = RR[keyFor(capV.slice(4), s)];
          }
          if (capV) {
            var cap = capV * o.qty;
            if (amt > cap) { amt = cap; how += ' \u2192 ' + t('capped', 'capped at') + ' ' + money(capV) + '/' + t('item', 'item'); }
          }
        }
        if (c.capPerOrder && amt > c.capPerOrder) { amt = c.capPerOrder; how += ' \u2192 ' + t('capped', 'capped at') + ' ' + money(c.capPerOrder) + '/' + t('order', 'order'); }
        if (raw === null || raw === undefined || isNaN(raw)) how = t('notSet', 'Not set, see note above');
        Object.keys(c.condRate || {}).forEach(function (k) { if (cd[k]) how += ' \u00B7 ' + t('cond_' + k, k); });
      }
      rows.push({ id: c.id, label: c.label, how: how, amt: r2(amt), color: c.color });
    });
    if (o.affPct > 0) rows.push({ id: 'aff', label: t('aff', 'Affiliate creator commission'), how: fmtPct(o.affPct) + ' \u00D7 ' + money(b.net), amt: r2(b.net * o.affPct / 100), color: '#a78bfa' });
    var total = r2(rows.reduce(function (x, r) { return x + r.amt; }, 0));
    var payout = r2(b.net_ship - o.shipCost - total);
    var goods = r2(o.cost * o.qty + o.other);
    var taxAmt = r2(b.net * o.taxPct / 100);
    var profit = r2(payout - goods - taxAmt);
    return { b: b, rows: rows, total: total, payout: payout, goods: goods, taxAmt: taxAmt, profit: profit, margin: b.net > 0 ? profit / b.net * 100 : 0, cond: cd };
  }

  function refreshRates(s, o, reset) {
    if (reset) Object.keys(touched).forEach(function (k) { if (!(M.components.filter(function (c) { return c.id === k; })[0] || {}).manual) delete touched[k]; });
    var d = defaults(s, o);
    M.components.forEach(function (c) {
      var e = $('sf-r-' + c.id); if (!e) return;
      if (!touched[c.id]) e.value = d[c.id] === null ? '' : d[c.id];
      var w = e.closest('.sf-rate'); if (w) w.hidden = !active(c, s);
    });
    return d;
  }
  function fill() {
    var s = state(), o = readInputs(), d = refreshRates(s, o, true);
    var opt = opts[s.sel] || {};
    if (M.currencyFromOption) { cur = opt.cur; root.querySelectorAll('.sf-cur').forEach(function (x) { x.textContent = cur; }); }
    var note = '';
    M.components.forEach(function (c) { if (active(c, s) && d[c.id] === null && !c.manual) note = t('noRate', 'No published rate for this selection. Enter the rate from your Seller Center.'); });
    if (opt.note && T['note_' + opt.note]) note = T['note_' + opt.note];
    $('sf-selnote').textContent = note;
    (M.toggles || []).forEach(function (g) {
      var e = $('sf-t-' + g.id); if (!e) return;
      var off = (g.requires && !s.tg[g.requires]) || !inList(s.store, g.stores);
      e.disabled = off; if (off) e.checked = false;
      if (g.stores) { var w = e.closest('.tg'); if (w) w.hidden = off; }
    });
    (M.selects || []).forEach(function (x) { var e = $('sf-x-' + x.id); if (e && x.stores) { var w = e.closest('.field'); if (w) w.hidden = !inList(s.store, x.stores); } });
    root.querySelectorAll('[data-stores]').forEach(function (el) { el.hidden = !inList(s.store, el.getAttribute('data-stores').split(' ')); });
    calc();
  }
  function readRates() { var o = {}; M.components.forEach(function (c) { var e = $('sf-r-' + c.id); o[c.id] = e && e.value !== '' ? parseFloat(String(e.value).replace(',', '.')) : (c.type === 'vol' || c.type === 'voltab' ? 0 : null); }); return o; }

  function calc() {
    var s = state(), o = readInputs();
    refreshRates(s, o, false);
    var f = compute(o, readRates(), s);
    $('sf-k-profit').textContent = money(f.profit);
    $('sf-k-profit').className = f.profit < 0 ? 'neg' : 'pos';
    $('sf-k-margin').textContent = fmt1(f.margin) + '%';
    $('sf-k-margin').className = f.profit < 0 ? 'neg' : f.margin < 10 ? 'warn' : 'pos';
    $('sf-k-fees').textContent = money(f.total);
    $('sf-k-feespct').textContent = f.b.net > 0 ? fmt1(f.total / f.b.net * 100) + '% ' + t('ofSub', 'of item subtotal') : '';
    $('sf-k-payout').textContent = money(f.payout);
    $('sf-k-payout').className = 'big' + (f.payout < 0 ? ' neg' : '');
    last = { o: o, f: f };
    var be = $('sf-be'), p30 = $('sf-p30');
    if (be) { var x = solve(0, s, o), y = solve(30, s, o); be.textContent = x === null ? t('na', 'n/a') : money(x); p30.textContent = y === null ? t('na', 'n/a') : money(y); }
    var cn = $('sf-condnote');
    if (cn) { var on = Object.keys(f.cond).filter(function (k) { return f.cond[k]; }); cn.hidden = !on.length; cn.textContent = on.map(function (k) { return t('condnote_' + k, ''); }).join(' '); }
    // bar
    var parts = [];
    f.rows.forEach(function (r) { if (r.amt) parts.push([r.label, r.amt, r.color || '#f97316']); });
    if (o.shipCost) parts.push([t('shipCost', 'Shipping you pay'), o.shipCost, 'var(--cost)']);
    if (f.goods) parts.push([t('goods', 'Product & other costs'), f.goods, 'var(--ink-700)']);
    if (f.taxAmt) parts.push([t('taxp', 'Your income tax'), f.taxAmt, 'var(--ink-500)']);
    if (f.profit > 0) parts.push([t('profit', 'Profit'), f.profit, 'var(--profit)']);
    var tot = parts.reduce(function (x, p) { return x + p[1]; }, 0) || 1;
    $('sf-bar').innerHTML = parts.map(function (p) { return '<i style="width:' + (p[1] / tot * 100).toFixed(2) + '%;background:' + p[2] + '" title="' + p[0] + ': ' + money(p[1]) + '"></i>'; }).join('');
    $('sf-legend').innerHTML = parts.map(function (p) { return '<li><i style="background:' + p[2] + '"></i>' + p[0] + ' <b>' + fmt1(p[1] / tot * 100) + '%</b></li>'; }).join('');
    // breakdown
    var h = '<tr><td>' + t('subtotal', 'Item subtotal after your discount') + '<small>' + money(o.price) + ' \u00D7 ' + o.qty + (o.sellerDisc ? ' \u2212 ' + money(o.sellerDisc) : '') + '</small></td><td class="n">' + money(f.b.net) + '</td></tr>';
    if (o.buyerShip) h += '<tr><td>' + t('buyerShip', 'Shipping paid by buyer') + '</td><td class="n">+' + money(o.buyerShip) + '</td></tr>';
    f.rows.forEach(function (r) { h += '<tr><td><i class="dot" style="background:' + (r.color || '#f97316') + '"></i>' + r.label + '<small>' + r.how + '</small></td><td class="n neg">\u2212' + money(r.amt) + '</td></tr>'; });
    if (o.shipCost) h += '<tr><td>' + t('shipCost', 'Shipping you pay') + '</td><td class="n neg">\u2212' + money(o.shipCost) + '</td></tr>';
    h += '<tr class="tot"><td>' + t('payout', 'Estimated payout') + '</td><td class="n">' + money(f.payout) + '</td></tr>';
    h += '<tr><td>' + t('goods', 'Product & other costs') + '</td><td class="n neg">\u2212' + money(f.goods) + '</td></tr>';
    if (f.taxAmt) h += '<tr><td>' + t('taxp', 'Your income tax') + '<small>' + fmtPct(o.taxPct) + ' \u00D7 ' + money(f.b.net) + '</small></td><td class="n neg">\u2212' + money(f.taxAmt) + '</td></tr>';
    h += '<tr class="tot"><td>' + t('profit', 'Profit') + '</td><td class="n ' + (f.profit < 0 ? 'neg' : 'pos') + '">' + money(f.profit) + '</td></tr>';
    $('sf-breakdown').innerHTML = h;
    compare(o, s);
  }

  // price per item at which margin (profit / item subtotal) reaches target %, with the current settings; null if unreachable
  function ratesAt(s, o) { var d = defaults(s, o), r = readRates(); M.components.forEach(function (c) { if (!touched[c.id]) r[c.id] = d[c.id]; }); return r; }
  function solve(target, s, o) {
    var f = function (p) { var o2 = Object.assign({}, o, { price: p }), x = compute(o2, ratesAt(s, o2), s); return x.profit - target / 100 * x.b.net; };
    var hi = Math.max(10, o.price * 4, (o.cost * o.qty + o.other + o.shipCost) * 20 + 100);
    for (var k = 0; k < 6 && f(hi) < 0; k++) hi *= 4;
    if (f(hi) < 0) return null;
    // scan from below so that price bands (cheaper tiers) are found first
    var steps = 400, lo = 0, prev = 0;
    for (var i = 1; i <= steps; i++) { var p = hi * i / steps; if (f(p) >= 0) { lo = prev; hi = p; break; } prev = p; }
    for (var j = 0; j < 50; j++) { var mid = (lo + hi) / 2; if (f(mid) >= 0) hi = mid; else lo = mid; }
    return Math.ceil(hi * 100 - 1e-6) / 100;
  }
  var last = null;
  function plain() {
    if (!last) return '';
    var lines = [document.title.split(' | ')[0], label(opts[state().sel] || {})];
    lines.push(t('subtotal', 'Item subtotal') + ': ' + money(last.f.b.net));
    last.f.rows.forEach(function (r) { lines.push(r.label + ' (' + r.how + '): −' + money(r.amt)); });
    lines.push(t('ui_res_fees', 'Total fees') + ': ' + money(last.f.total));
    lines.push(t('ui_res_payout', 'Payout') + ': ' + money(last.f.payout));
    lines.push(t('ui_res_profit', 'Profit') + ': ' + money(last.f.profit) + ' (' + fmt1(last.f.margin) + '%)');
    lines.push(location.href.split('#')[0]);
    return lines.join('\n');
  }
  function stateToQuery() {
    var q = new URLSearchParams();
    root.querySelectorAll('input[id^=sf-],select[id^=sf-]').forEach(function (e) {
      if (e.id === 'sf-selq' || e.id === 'sf-grp' || e.disabled) return;
      if (e.type === 'checkbox') { if (e.checked) q.set(e.id.slice(3), '1'); return; }
      if (e.id.indexOf('sf-r-') === 0 && !touched[e.id.slice(5)]) return;
      if (e.value !== '') q.set(e.id.slice(3), e.value);
    });
    var st = root.querySelector('input[name=sf-store]:checked'); if (st) q.set('store', st.value);
    return q.toString();
  }
  function applyQuery() {
    var q = new URLSearchParams(location.search); if (!q.toString()) return;
    if (q.has('store')) { var r = root.querySelector('input[name=sf-store][value="' + q.get('store') + '"]'); if (r) r.checked = true; }
    if (q.has('sel') && opts[+q.get('sel')]) { if (grp) { grp.value = opts[+q.get('sel')].g; showGroup(grp.value); } s0.value = q.get('sel'); }
    q.forEach(function (v, k) {
      if (k === 'store' || k === 'sel') return;
      var e = $('sf-' + k); if (!e) return;
      if (e.type === 'checkbox') e.checked = v === '1'; else e.value = v;
      if (k.indexOf('r-') === 0) touched[k.slice(2)] = 1;
    });
  }
  function flash(btn, msg) { var o = btn.innerHTML; btn.textContent = msg; setTimeout(function () { btn.innerHTML = o; }, 1600); }
  function copyText(txt, btn, msg) {
    var done = function () { flash(btn, msg); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(txt).then(done, function () { fallback(); });
    else fallback();
    function fallback() { var a = document.createElement('textarea'); a.value = txt; document.body.appendChild(a); a.select(); try { document.execCommand('copy'); done(); } catch (e) {} a.remove(); }
  }

  function compare(o, s) {
    var box = $('sf-compare'); if (!box || !M.compare) return;
    var C = M.compare;
    function side(x) {
      var s2 = JSON.parse(JSON.stringify(s)); if (x.state) Object.keys(x.state).forEach(function (k) { s2[k] = x.state[k]; });
      var r = readRates(), d = defaults(s2, o), na = false;
      (C.vary || []).forEach(function (k) { r[k] = d[k]; if (d[k] === null) na = true; });
      if (x.rates) Object.keys(x.rates).forEach(function (k) { if (r[k]) r[k] = x.rates[k]; });
      return { f: compute(o, r, s2), na: na };
    }
    var a = side(C.a), b = side(C.b);
    if (a.na || b.na) { box.innerHTML = '<p class="muted">' + t('cmpNa', 'No earlier rate is published for this selection.') + '</p>'; return; }
    var d = r2(b.f.profit - a.f.profit);
    box.innerHTML = '<table class="sf-cmp"><thead><tr><th></th><th class="n">' + C.a.label + '</th><th class="n">' + C.b.label + '</th></tr></thead><tbody>' +
      '<tr><td>' + t('fees', 'Platform fees') + '</td><td class="n">' + money(a.f.total) + '</td><td class="n">' + money(b.f.total) + '</td></tr>' +
      '<tr><td>' + t('payout', 'Estimated payout') + '</td><td class="n">' + money(a.f.payout) + '</td><td class="n">' + money(b.f.payout) + '</td></tr>' +
      '<tr class="tot"><td>' + t('profit', 'Profit') + '</td><td class="n">' + money(a.f.profit) + '</td><td class="n">' + money(b.f.profit) + '</td></tr></tbody></table>' +
      '<p class="sf-delta ' + (d < 0 ? 'neg' : 'pos') + '">' + t('change', 'Change per order') + ': <b>' + (d > 0 ? '+' : '') + money(d) + '</b></p>' +
      (C.note ? '<p class="muted">' + C.note + '</p>' : '');
  }

  // ----- category picker: plain select, or group select + search for long lists
  var s0 = $('sf-sel'), grp = $('sf-grp'), q = $('sf-selq');
  function addOpt(sel, v, txt) { var e = document.createElement('option'); e.value = v; e.textContent = txt; sel.appendChild(e); }
  function showGroup(g, keep) {
    s0.innerHTML = '';
    opts.forEach(function (o, i) { if (o.g === g) addOpt(s0, i, o.n); });
    if (keep !== undefined) s0.value = keep;
  }
  function search(v) {
    v = v.trim().toLowerCase();
    if (!v) { grp.disabled = false; showGroup(grp.value, s0.value); fill(); return; }
    var hits = [];
    for (var i = 0; i < opts.length && hits.length < 300; i++) if (label(opts[i]).toLowerCase().indexOf(v) >= 0) hits.push(i);
    s0.innerHTML = '';
    if (!hits.length) { addOpt(s0, '', t('noMatch', 'No matching category')); s0.disabled = true; $('sf-selnote').textContent = ''; return; }
    s0.disabled = false; grp.disabled = true;
    hits.forEach(function (i) { addOpt(s0, i, label(opts[i])); });
    fill();
  }
  function init() {
    (M.selects || []).forEach(function (x) {
      if (!x.fromTable) return;
      var e = $('sf-x-' + x.id), list = M.tables[x.fromTable[0]][x.fromTable[1]];
      list.forEach(function (n, i) { addOpt(e, i, n); });
      if (x.defIndex !== undefined) e.value = x.defIndex;
    });
    if (grp) {
      var groups = []; opts.forEach(function (o) { if (groups.indexOf(o.g) < 0) groups.push(o.g); });
      grp.innerHTML = ''; groups.forEach(function (g) { addOpt(grp, g, g); });
      var d0 = opts[M.defaultOption || 0]; grp.value = d0.g; showGroup(d0.g, M.defaultOption || 0);
      var cnt = $('sf-selcount'); if (cnt) cnt.textContent = opts.length.toLocaleString(M.locale || 'en');
    } else {
      opts.forEach(function (c, i) { addOpt(s0, i, c.n); });
      s0.value = M.defaultOption || 0;
    }
    root.classList.remove('loading');
    root.addEventListener('change', function (e) {
      var id = e.target.id || '';
      if (id.indexOf('sf-r-') === 0) { touched[id.slice(5)] = 1; calc(); return; }
      if (id === 'sf-grp') { showGroup(grp.value); s0.selectedIndex = 0; }
      if (id === 'sf-selq') return;
      fill();
    });
    root.addEventListener('input', function (e) {
      var id = e.target.id || '';
      if (id === 'sf-selq') { search(e.target.value); return; }
      if (id.indexOf('sf-r-') === 0) touched[id.slice(5)] = 1;
      if (e.target.type === 'number') calc();
    });
    applyQuery();
    fill();
    var cb = $('sf-copy'), sb = $('sf-share');
    if (cb) cb.addEventListener('click', function () { copyText(plain(), cb, t('ui_copied', 'Copied')); });
    if (sb) sb.addEventListener('click', function () {
      var url = location.href.split('?')[0].split('#')[0] + '?' + stateToQuery();
      if (history.replaceState) history.replaceState(null, '', url);
      if (navigator.share && /Mobi|Android/i.test(navigator.userAgent)) navigator.share({ title: document.title, url: url }).catch(function () {});
      else copyText(url, sb, t('ui_link_copied', 'Link copied'));
    });
    window.SF_compute = function (inputs, selIndex, extra) { // used by tests; no args → current UI state
      var s = state();
      if (selIndex !== undefined && selIndex !== null) s.sel = selIndex;
      if (extra) {
        if (extra.store) s.store = extra.store;
        if (extra.period) s.period = extra.period;
        if (extra.tg) Object.assign(s.tg, extra.tg);
        if (extra.x) Object.assign(s.x, extra.x);
      }
      var o = inputs ? Object.assign({ price: 0, qty: 1, sellerDisc: 0, buyerShip: 0, shipCost: 0, cost: 0, other: 0, affPct: 0, tax: 0, taxPct: 0, vol: 0, coef: 100 }, inputs) : readInputs();
      var rates = defaults(s, o);
      var f = compute(o, rates, s);
      f.fee = {}; f.rate = rates; f.rows.forEach(function (r) { f.fee[r.id] = r.amt; });
      return f;
    };
    window.SF_ready = true;
  }
  function expand(d) { return d.o ? d.o.map(function (x) { return { g: d.groups[x[0]], n: x[1], r: x[2] }; }) : d; }
  if (M.selector.src) {
    root.classList.add('loading');
    fetch(M.selector.src).then(function (r) { return r.json(); }).then(function (d) { opts = expand(d); M.tables = d.tables || {}; init(); })
      .catch(function () { $('sf-selnote').textContent = t('loadErr', 'Could not load the rate table. Please reload the page.'); });
  } else { opts = expand(M.selector.options); init(); }

  // searchable rate table
  var fq = $('sf-filter');
  if (fq) fq.addEventListener('input', function () { var v = fq.value.toLowerCase(); document.querySelectorAll('#sf-rates tbody tr').forEach(function (tr) { tr.hidden = tr.textContent.toLowerCase().indexOf(v) < 0; }); });
})();
