"""Guide: Amazon US FBM prepaid return label rule from 18 Dec 2026, with a return-vs-returnless break-even calculator."""

def _net(price, label, handling, fee, out, sell):
    return sell / 100 * (price * (1 - fee / 100) - out) - label - handling

def _be(label, handling, fee, out, sell):
    return ((label + handling) / (sell / 100) + out) / (1 - fee / 100)

def usd(v): return ('−' if v < 0 else '') + f'${abs(v):,.2f}'

CALC = '''
<div class="card" id="rr-calc" style="padding:20px;margin:18px 0">
<div class="g2" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">
<div class="field"><label class="label" for="rr-price">Resale price if the item comes back</label><div class="input"><span class="pre">$</span><input id="rr-price" type="number" inputmode="decimal" min="0" step="0.01" value="25"></div></div>
<div class="field"><label class="label" for="rr-label">Prepaid return label cost</label><div class="input"><span class="pre">$</span><input id="rr-label" type="number" inputmode="decimal" min="0" step="0.01" value="8"></div></div>
<div class="field"><label class="label" for="rr-handling">Inspection, repacking and labour</label><div class="input"><span class="pre">$</span><input id="rr-handling" type="number" inputmode="decimal" min="0" step="0.01" value="2"></div></div>
<div class="field"><label class="label" for="rr-fee">Selling fees when you resell it</label><div class="input"><input id="rr-fee" type="number" inputmode="decimal" min="0" max="99" step="0.1" value="15"><span class="suf">%</span></div></div>
<div class="field"><label class="label" for="rr-out">Shipping cost to the next buyer</label><div class="input"><span class="pre">$</span><input id="rr-out" type="number" inputmode="decimal" min="0" step="0.01" value="5"></div></div>
<div class="field"><label class="label" for="rr-sell">Chance the return can be resold as new</label><div class="input"><input id="rr-sell" type="number" inputmode="decimal" min="1" max="100" step="1" value="80"><span class="suf">%</span></div></div>
</div>
<div style="margin-top:16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">
<div><span class="small muted">Expected gain from return and resell</span><div class="h-display" style="font-size:28px" id="rr-net" aria-live="polite">$3.00</div></div>
<div><span class="small muted">Break-even resale price</span><div class="h-display" style="font-size:28px" id="rr-be">$20.59</div></div>
</div>
<p id="rr-yes" style="margin-top:12px"><b>Return and resell.</b> The item is worth more back than the label and handling cost. Upload the prepaid label in Manage Seller-Fulfilled Returns within 7 days.</p>
<p id="rr-no" style="margin-top:12px" hidden><b>Returnless refund.</b> Getting the item back costs more than it is worth. Issue a full refund without requiring the return.</p>
<p class="small muted">Both options refund the buyer in full, so the refund itself is left out. The example values are illustrative: enter your own label cost and fees.</p>
</div>
<script>(function(){var f=function(i){return parseFloat(document.getElementById(i).value)||0};var lg=document.documentElement.lang||'en';var nf=new Intl.NumberFormat(lg,{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2});
function run(){var p=f('rr-price'),l=f('rr-label'),h=f('rr-handling'),fee=Math.min(f('rr-fee'),99),o=f('rr-out'),s=Math.max(Math.min(f('rr-sell'),100),1);
var net=s/100*(p*(1-fee/100)-o)-l-h,be=((l+h)/(s/100)+o)/(1-fee/100);
document.getElementById('rr-net').textContent=nf.format(net);document.getElementById('rr-be').textContent=nf.format(be);
document.getElementById('rr-yes').hidden=!(net>=0);document.getElementById('rr-no').hidden=net>=0;}
document.querySelectorAll('#rr-calc input').forEach(function(e){e.addEventListener('input',run)});run();})();</script>
'''

def g_amazon_returns():
    a = _net(25, 8, 2, 15, 5, 80); be = _be(8, 2, 15, 5, 80); b = _net(12, 8, 2, 15, 5, 80)
    return f'''
<p>From <b>18 December 2026</b>, Amazon will require a prepaid return label on almost every US return of a seller-fulfilled (FBM) order. Sellers who give buyers only a return address, and let the buyer pay postage, will no longer meet the rule. This guide explains the change and includes a calculator to decide, return by return, whether to pay for the label or refund without getting the item back.</p>
<p class="muted">Amazon announced the change in an email to sellers, reported by PPC Land and Seller Essentials. We could not find a public Amazon page with the new rule: Seller Central help pages require a login, and PPC Land reports that the help page it reviewed on 19 October 2026 did not mention it yet. Check the notice in your Seller Central account.</p>
<h2 id="rule">What changes on 18 December 2026</h2>
<ul>
<li>All US returns for seller-fulfilled orders need a <b>prepaid return shipping label</b>. Address-only labels, where the customer arranges and pays for the return, no longer count.</li>
<li><b>Heavy and bulky items</b> are excluded for now. Amazon calls this temporary and has not defined the category or given an end date.</li>
<li>Within <b>7 calendar days</b> of each return request you must either upload a prepaid label against the request in <b>Manage Seller-Fulfilled Returns</b>, or issue a full refund without requiring the item back.</li>
<li>If you do neither, Amazon may issue a <b>returnless refund automatically</b> and deduct it from your selling account. The buyer keeps the item.</li>
<li>Labels sent through Buyer-Seller Messaging or any other channel outside the Manage Returns workflow <b>do not count</b>.</li>
</ul>
<p>Fulfillment by Amazon (FBA) orders are not affected. Amazon already enrolls US sellers in prepaid returns through Buy Shipping; the new rule removes the address-only option that remained. Who finally pays for a label can still depend on the return reason, so check how Amazon treats seller-fault and buyer-remorse returns for your account.</p>
<h2 id="calculator">Return or returnless refund? Break-even calculator</h2>
<p>When a return comes in, you refund the buyer either way. The question is whether getting the item back is worth the label, the handling and the cost of selling it again.</p>
{CALC}
<h2 id="example">Worked examples</h2>
<p>With a $8 label, $2 of handling, 15% selling fees, $5 to ship it again and an 80% chance it can be resold, a $25 item is worth getting back: the expected gain is {usd(a)}. The break-even resale price is {usd(be)}. Below that, a returnless refund costs you less. The same item at $12 would lose {usd(-b)} on average if you paid for the return, so refund it without a return.</p>
<p>The formula: expected gain = chance of resale × (resale price × (1 − selling fees) − shipping to the next buyer) − label cost − handling.</p>
<h2 id="deadline">Do not let the deadline decide for you</h2>
<p>A returnless refund you choose for a cheap item is a sensible business decision. One that Amazon issues because nobody uploaded the label in 7 days can cost you an expensive item as well as the sale. Check open return requests every day, give the queue an owner and a backup, and set a price limit under which your team refunds without a return.</p>
<h2 id="checklist">Checklist before 18 December</h2>
<ul>
<li>Find the products and procedures that still use address-only labels or send labels by message.</li>
<li>Make sure every label is uploaded in Manage Seller-Fulfilled Returns.</li>
<li>Work out your break-even resale price per product with the calculator above.</li>
<li>Check how Amazon classifies any products you think are heavy and bulky.</li>
</ul>
'''

GUIDES_AMAZON = [
 dict(lang='en', slug='amazon-fbm-prepaid-return-label-2026', short='Amazon FBM prepaid return labels (18 Dec 2026)',
      title='Amazon FBM Prepaid Return Label Rule from 18 December 2026: 7-Day Deadline and Return vs Returnless Refund Calculator',
      desc='From 18 Dec 2026 Amazon US sellers who fulfil their own orders must upload a prepaid return label within 7 days or Amazon may auto-refund the buyer. What changes, and a break-even calculator for return vs returnless refund.',
      market=None, cov='cov-ink', fig='7 days'),
]
GUIDE_BODY_AMAZON = {'amazon-fbm-prepaid-return-label-2026': g_amazon_returns}
GUIDE_SOURCES_AMAZON = {'amazon-fbm-prepaid-return-label-2026': [
 ('Amazon forces prepaid return labels on US seller orders from December 18 — PPC Land (19 Oct 2026), reports the Amazon Services email', 'https://ppc.land/amazon-forces-prepaid-return-labels-on-us-seller-orders-from-december-18/'),
 ('Amazon’s December 18 Return Label Change: What FBM Sellers Need to Know — Seller Essentials (Oct 2026)', 'https://selleressentials.com/amazon-fbm-prepaid-return-labels/')]}
