(function(){
  'use strict';
  var M = document.body.getAttribute('data-market');
  if (!M) return;
  var $ = function(id){ return document.getElementById(id); };
  var num = function(id){ var v = parseFloat($(id).value); return isFinite(v) ? v : 0; };
  var CUR = M === 'MY' ? 'RM' : '\u20B1';
  var LOC = M === 'MY' ? 'en-MY' : 'en-PH';
  var money = function(n){ var s = Math.abs(n).toLocaleString(LOC,{minimumFractionDigits:2,maximumFractionDigits:2}); return (n < 0 ? '\u2212' : '') + CUR + s; };
  var r2 = function(n){ return Math.round(n*100)/100; };
  var CATS = M === 'MY' ? window.MY_CATS : window.PH_CATS;
  var sel = $('cat');
  CATS.forEach(function(c, i){ var o = document.createElement('option'); o.value = i; o.textContent = c.n; sel.appendChild(o); });
  // sensible default
  var def = CATS.findIndex(function(c){ return /Women.s Tops|Womenswear/.test(c.n); });
  if (def >= 0) sel.value = def;

  function store(){ var r = document.querySelector('input[name=store]:checked'); return r ? r.value : 'mp'; }

  // MY commission rate columns: [oldMpBxp, oldMpNon, oldMallBxp, oldMallNon, newMpBxp, newMpNon, newMallBxp, newMallNon]
  function myRate(c, period, st, bxp){
    var idx = (period === 'new' ? 4 : 0) + (st === 'mall' ? 2 : 0) + (bxp ? 0 : 1);
    return c.r[idx];
  }

  function fillDefaults(){
    var c = CATS[+sel.value];
    var st = store();
    if (M === 'MY'){
      var period = $('period').value, bxp = $('bxp').checked;
      var rate = myRate(c, period, st, bxp);
      $('commRate').value = rate === null ? '' : rate;
      $('catNote').textContent = rate === null ? 'TikTok lists no rate for this category before 31 Oct 2026. Enter your rate manually.' : '';
      $('txRate').value = $('paylater').checked ? 4.86 : 3.78;
      $('bxpRate').value = bxp ? ($('campaign').checked ? 7.02 : 4.86) : 0;
      $('campaign').disabled = !bxp;
      $('psf').value = $('psfWaived').checked ? 0 : 0.54;
    } else {
      var comm = st === 'mall' ? c.mall : c.mp;
      $('commRate').value = $('newSeller').checked ? 0 : comm;
      $('txRate').value = 2.24;
      $('ssfRate').value = st === 'mall' ? 5 : 5.5;
      $('ssfCap').value = 100;
      $('opf').value = $('opfExempt').checked ? 0 : 5;
      $('growthRate').value = c.g;
      $('catNote').textContent = c.gn || '';
    }
    calc();
  }

  function fees(o){
    // o: inputs + rates. Returns breakdown array and totals.
    var base = Math.max(0, o.price*o.qty - o.sellerDisc);
    var rows = [];
    var comm = r2(base * o.commRate/100);
    rows.push(['Commission fee', o.commRate + '% \u00D7 ' + money(base), comm]);
    var tx = r2((base + o.buyerShip) * o.txRate/100);
    rows.push(['Transaction fee', o.txRate + '% \u00D7 ' + money(base + o.buyerShip), tx]);
    if (M === 'MY'){
      if (o.bxpRate > 0){
        var b = Math.min(base * o.bxpRate/100, 54*o.qty);
        rows.push(['BXP service fee', o.bxpRate + '% \u00D7 ' + money(base) + ' (cap RM54/item)', r2(b)]);
      }
      rows.push(['Platform Support Fee', 'flat per delivered order', r2(o.psf)]);
    } else {
      var ssf = Math.min(base * o.ssfRate/100, o.ssfCap*o.qty);
      rows.push(['Shipping Service Fee', o.ssfRate + '% \u00D7 ' + money(base) + ' (cap ' + money(o.ssfCap) + '/item)', r2(ssf)]);
      rows.push(['Order Processing Fee', 'flat per delivered order', r2(o.opf)]);
      if (o.growthRate > 0) rows.push(['Seller Growth Fee', o.growthRate + '% \u00D7 ' + money(base), r2(base*o.growthRate/100)]);
    }
    if (o.affPct > 0) rows.push(['Affiliate creator commission', o.affPct + '% \u00D7 ' + money(base) + ' (your setting)', r2(base*o.affPct/100)]);
    var total = rows.reduce(function(s,r){ return s + r[2]; }, 0);
    var payout = base + o.buyerShip - o.shipCost - total;
    var profit = payout - o.cost*o.qty - o.other;
    return {base:base, rows:rows, total:r2(total), payout:r2(payout), profit:r2(profit), margin: base > 0 ? profit/base*100 : 0};
  }

  function readInputs(){
    var o = {price:num('price'), qty:Math.max(1, Math.round(num('qty'))||1), sellerDisc:num('sellerDisc'), buyerShip:num('buyerShip'), shipCost:num('shipCost'),
      cost:num('cost'), other:num('other'), affPct:num('affPct'), commRate:num('commRate'), txRate:num('txRate')};
    if (M === 'MY'){ o.bxpRate = num('bxpRate'); o.psf = num('psf'); }
    else { o.ssfRate = num('ssfRate'); o.ssfCap = num('ssfCap'); o.opf = num('opf'); o.growthRate = num('growthRate'); }
    return o;
  }

  function calc(){
    var o = readInputs();
    var f = fees(o);
    var html = '<table><thead><tr><th>Item</th><th>How</th><th class="n">Amount</th></tr></thead><tbody>';
    html += '<tr><td>Item subtotal after your discount</td><td>' + money(o.price) + ' \u00D7 ' + o.qty + ' \u2212 ' + money(o.sellerDisc) + '</td><td class="n">' + money(f.base) + '</td></tr>';
    if (o.buyerShip) html += '<tr><td>Shipping paid by buyer</td><td></td><td class="n">' + money(o.buyerShip) + '</td></tr>';
    f.rows.forEach(function(r){ html += '<tr><td>' + r[0] + '</td><td class="note">' + r[1] + '</td><td class="n neg">\u2212' + money(r[2]) + '</td></tr>'; });
    if (o.shipCost) html += '<tr><td>Shipping cost you pay</td><td></td><td class="n neg">\u2212' + money(o.shipCost) + '</td></tr>';
    html += '<tr class="tot"><td>Estimated payout</td><td></td><td class="n">' + money(f.payout) + '</td></tr>';
    html += '<tr><td>Product cost</td><td>' + money(o.cost) + ' \u00D7 ' + o.qty + '</td><td class="n neg">\u2212' + money(o.cost*o.qty) + '</td></tr>';
    if (o.other) html += '<tr><td>Other costs</td><td></td><td class="n neg">\u2212' + money(o.other) + '</td></tr>';
    html += '<tr class="tot"><td>Profit</td><td></td><td class="n ' + (f.profit < 0 ? 'neg' : 'pos') + '">' + money(f.profit) + '</td></tr></tbody></table>';
    $('breakdown').innerHTML = html;
    $('kFees').textContent = money(f.total);
    $('kFeesPct').textContent = f.base > 0 ? (f.total/f.base*100).toFixed(2) + '% of subtotal' : '';
    $('kPayout').textContent = money(f.payout);
    $('kProfit').textContent = money(f.profit);
    $('kProfit').className = f.profit < 0 ? 'neg' : 'pos';
    $('kMargin').textContent = 'Margin ' + f.margin.toFixed(1) + '%';
    compare(o, f);
  }

  function compare(o, fNow){
    var c = CATS[+sel.value], a, b, la, lb, note = '';
    if (M === 'MY'){
      var st = store(), bxp = $('bxp').checked;
      var oldR = myRate(c, 'old', st, bxp), newR = myRate(c, 'new', st, bxp);
      la = 'Before 31 Oct 2026'; lb = 'From 31 Oct 2026';
      if (oldR === null){ $('compare').innerHTML = '<p class="note">No pre-31 October rate is published for this category.</p>'; return; }
      a = fees(Object.assign({}, o, {commRate: oldR}));
      b = fees(Object.assign({}, o, {commRate: newR}));
      note = 'Only the commission rate differs between the columns; your other settings (transaction, BXP, support fee) are kept the same.';
    } else {
      la = 'Early 2026 (\u20B13 fee, no growth fee)'; lb = 'Now (\u20B15 fee + growth fee)';
      a = fees(Object.assign({}, o, {opf: o.opf > 0 ? 3 : 0, growthRate: 0}));
      b = fees(Object.assign({}, o, {opf: o.opf > 0 ? 5 : 0}));
      note = 'The \u20B13 processing fee applied from 1 Dec 2025 to 31 Aug 2026; the Seller Growth Fee started 27 Apr 2026. Commission is unchanged (15 Jan 2025 table).';
    }
    var d = r2(b.profit - a.profit);
    $('compare').innerHTML = '<table><thead><tr><th></th><th class="n">' + la + '</th><th class="n">' + lb + '</th></tr></thead><tbody>' +
      '<tr><td>Total TikTok fees</td><td class="n">' + money(a.total) + '</td><td class="n">' + money(b.total) + '</td></tr>' +
      '<tr><td>Payout</td><td class="n">' + money(a.payout) + '</td><td class="n">' + money(b.payout) + '</td></tr>' +
      '<tr class="tot"><td>Profit</td><td class="n">' + money(a.profit) + '</td><td class="n">' + money(b.profit) + '</td></tr>' +
      '<tr><td>Change per order</td><td></td><td class="n ' + (d < 0 ? 'neg' : 'pos') + '">' + (d > 0 ? '+' : '') + money(d) + '</td></tr></tbody></table><p class="note">' + note + '</p>';
  }

  var drivers = M === 'MY' ? ['cat','period','bxp','campaign','paylater','psfWaived'] : ['cat','newSeller','opfExempt'];
  drivers.forEach(function(id){ $(id).addEventListener('change', fillDefaults); });
  document.querySelectorAll('input[name=store]').forEach(function(e){ e.addEventListener('change', fillDefaults); });
  document.querySelectorAll('#calc input[type=number]').forEach(function(e){ e.addEventListener('input', calc); });
  fillDefaults();

  // Rate table
  var tb = $('rateBody');
  if (tb){
    var h = '';
    CATS.forEach(function(c){
      if (M === 'MY'){
        h += '<tr><td>' + c.n + '</td>' + c.r.map(function(v, i){ return '<td class="n' + (i >= 4 ? ' new' : '') + '">' + (v === null ? '\u2013' : v.toFixed(2) + '%') + '</td>'; }).join('') + '</tr>';
      } else {
        h += '<tr><td>' + c.cl + '</td><td>' + c.n + '</td><td class="n">' + c.mp.toFixed(2) + '%</td><td class="n">' + c.mall.toFixed(2) + '%</td><td class="n">' + c.g + '%' + (c.gn ? '*' : '') + '</td></tr>';
      }
    });
    tb.innerHTML = h;
    var q = $('rateFilter');
    if (q) q.addEventListener('input', function(){ var t = q.value.toLowerCase(); tb.querySelectorAll('tr').forEach(function(tr){ tr.style.display = tr.textContent.toLowerCase().indexOf(t) >= 0 ? '' : 'none'; }); });
  }
})();
