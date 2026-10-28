"""Shopee Indonesia page copy and guide. Every number comes from markets.compute() or the rate file."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

SID = MARKETS['shopee-id']['selector']['options']
IDR = lambda v: money(v, 'IDR')
I = lambda s: f'<span lang="id">{s}</span>'
LBL = dict(admin='Admin fee', mallpay='Shopee Mall payment fee', opf='Order Processing Fee', gox='Gratis Ongkir XTRA fee',
           promox='Promo XTRA fee', promoxp='Promo XTRA+ fee', livex='Live/Video XTRA fee', preorder='Pre-order service fee')
PCT = {'admin', 'mallpay', 'gox', 'promox', 'promoxp', 'livex', 'preorder'}

def _ex(f):
    rows = [((f"{LBL[k]} ({pct(r)})" if k in PCT and r else LBL[k]), '−' + IDR(a)) for k, r, a in f['rows']]
    rows.append(('Total fees', IDR(f['total']), True)); rows.append(('Payout', IDR(f['payout']), True))
    return rows

def _o(g, n):
    return next(o for o in SID if o['g'] == g and o['n'] == n)
FW = ('Perawatan & Kecantikan', 'Perawatan Wajah')
SAMPLE = [FW, ('Pakaian Wanita', 'Dress'), ('Fashion Muslim', 'Mukena & Perlengkapan Sholat'), ('Sepatu Pria', 'Sandal'),
          ('Handphone & Aksesoris', 'Handphone'), ('Komputer & Aksesoris', 'Laptop'), ('Makanan & Minuman', 'Makanan Instan'),
          ('Ibu & Bayi', 'Susu Formula & Makanan Bayi'), ('Elektronik', 'TV & Aksesoris')]
RNG = lambda k: (min(o['r'][k] for o in SID if k in o['r']), max(o['r'][k] for o in SID if k in o['r']))

def _rows():
    out = ''
    for g, n in SAMPLE:
        r = _o(g, n)['r']
        out += (f"<tr><td>{I(g + ' › ' + n)}</td><td class='n'>{pct(r['nonstar'])}</td><td class='n'>{pct(r['mall'])}</td>"
                f"<td class='n'>{pct(r['cur_reg'])}</td><td class='n'>{pct(r['new_reg'])}</td></tr>")
    return out

def shopee_id_page():
    r = _o(*FW)['r']; sel = SID.index(_o(*FW))
    a = compute('shopee-id', sel=sel, price=89000, cost=30000)
    m = compute('shopee-id', sel=sel, store='mall', price=89000, cost=30000)
    gc = compute('shopee-id', sel=sel, price=89000, cost=30000, x={'gox': 'cur_reg'})
    gn = compute('shopee-id', sel=sel, price=89000, cost=30000, x={'gox': 'new_reg'})
    lo, hi = RNG('nonstar'); mlo, mhi = RNG('mall')
    toc = [('how', 'How Shopee Indonesia fees work'), ('examples', 'Worked examples'), ('rates', 'Sample rates'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f"""
<h2 id="how">How Shopee Indonesia fees work</h2>
<p>Shopee Indonesia charges by seller type: Non-Star, Star/Star+ and Shopee Mall. Non-Star and Star sellers pay the same rates. All fees include VAT and are charged on the item price after seller discounts and seller vouchers, never on shipping.</p>
<h3>1. Admin fee</h3>
<p>The admin fee (Biaya Administrasi) depends on the product type: {pct(lo)} to {pct(hi)} for Non-Star and Star sellers and {pct(mlo)} to {pct(mhi)} for Shopee Mall. There is no cap per item. The 10% top rate is already 20% below the 12.5% base rate.</p>
<p>Non-Star sellers who uploaded their first product before 1 August 2026 pay no admin fee and no Order Processing Fee until they complete 50 orders or reach 6 months. Sellers who started on or after 1 August 2026 pay from the first order.</p>
<h3>2. Shopee Mall payment fee</h3>
<p>Mall sellers also pay 1.8%, capped at {IDR(50000)} per item, in every category.</p>
<h3>3. Order Processing Fee</h3>
<p>{IDR(1250)} per completed order. On a multi-product order it is split across the products by value.</p>
<h3>4. Optional programmes</h3>
<p>Gratis Ongkir XTRA (free shipping) charges a rate by product type: {pct(RNG('cur_reg')[0])} to {pct(RNG('cur_reg')[1])} for regular-size products, capped at {IDR(40000)} per item, and up to {pct(RNG('cur_spec')[1])} for special-size products, capped at {IDR(60000)}. New rates apply from <b>1 December 2026</b> for non-Mall sellers and from <b>1 January 2027</b> for Mall: up to {pct(RNG('new_reg')[1])} with a {IDR(60000)} cap for regular size and up to {pct(RNG('new_spec')[1])} with an {IDR(80000)} cap for special size. Choose the current or the new rates in the calculator.</p>
<p>Promo XTRA costs 4.5% (max {IDR(60000)} per item) and Promo XTRA+ 6.5% (max {IDR(80000)}). Orders through Shopee Live or Shopee Video pay 3%, or 2% if you are in Promo XTRA, capped at {IDR(20000)} per item. Pre-order products pay another 3%.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: {IDR(89000)} face care product, Non-Star or Star</h4>
<p>Product cost {IDR(30000)}, free shipping for the buyer, no optional programmes.</p>
{ex_table(_ex(a))}
<p>Profit {IDR(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same product in Shopee Mall</h4>
<p>The Mall admin fee is {pct(r['mall'])}, plus the 1.8% payment fee: total fees {IDR(m['total'])}, profit {IDR(m['profit'])}.</p></div>
<div class="example"><h4>Example 3: with Gratis Ongkir XTRA, now and from 1 December 2026</h4>
<p>At the current {pct(r['cur_reg'])} rate the fees are {IDR(gc['total'])}. From 1 December 2026 the rate for this product rises to {pct(r['new_reg'])} and the fees to {IDR(gn['total'])}, leaving {IDR(gn['profit'])} profit.</p></div>

<h2 id="rates">Sample rates</h2>
<p>Admin fee and the Gratis Ongkir XTRA rate for regular-size products. The calculator has all {len(SID):,} product types.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Admin fee, Non-Star &amp; Star</th><th class="n">Admin fee, Mall</th><th class="n">Gratis Ongkir XTRA now</th><th class="n">Gratis Ongkir XTRA from 1 Dec 2026</th></tr></thead><tbody>{_rows()}</tbody></table></div>
<p>Read the full picture in our guide to <a href="../../guides/shopee-indonesia-fees-2026/">Shopee Indonesia seller fees in 2026</a>.</p>
"""
    faq = [
     ('How much is the Shopee Indonesia admin fee?', f'{pct(lo)} to {pct(hi)} of the item price for Non-Star and Star/Star+ sellers and {pct(mlo)} to {pct(mhi)} for Shopee Mall, by product type, with no cap per item.'),
     ('Do Star sellers pay less than Non-Star sellers?', 'No. Non-Star and Star/Star+ sellers pay the same admin fee rates. Only new Non-Star sellers who started before 1 August 2026 still get the free period.'),
     ('Is Gratis Ongkir XTRA compulsory?', 'No. It is an optional programme. You pay its fee only if you join, and you can leave at any time.'),
     ('What changes on 1 December 2026?', 'New Gratis Ongkir XTRA rates for non-Mall sellers, with Mall following on 1 January 2027. Most regular-size rates go up by 3 to 3.5 points (special size by 3.5 to 4) and the caps rise from Rp40,000 to Rp60,000 (regular size) and from Rp60,000 to Rp80,000 (special size).'),
     ('Is there a fee per order?', 'Yes. The Order Processing Fee is Rp1,250 per completed order.'),
    ]
    return dict(title='Shopee Indonesia Fee Calculator 2026 (Admin Fee, Gratis Ongkir XTRA, Mall)',
                desc='Free Shopee Indonesia fee and profit calculator: admin fee for Non-Star, Star/Star+ and Mall by product type, the 1.8% Mall payment fee, Rp1,250 per order, Gratis Ongkir XTRA with the 1 Dec 2026 rates, Promo XTRA and Live XTRA.',
                h1='Shopee Indonesia Fee Calculator',
                lede='Admin fee for Non-Star, Star/Star+ and Shopee Mall by product type, the Mall payment fee, Rp1,250 per order, and the optional Gratis Ongkir XTRA, Promo XTRA and Live/Video XTRA fees, including the new rates from 1 December 2026.',
                body=body, faq=faq, toc=toc)

def g_shopee_id():
    r = _o(*FW)['r']; sel = SID.index(_o(*FW))
    a = compute('shopee-id', sel=sel, price=89000, cost=30000)
    trs = ''
    for k, lab in [('none', 'Not in Gratis Ongkir XTRA'), ('cur_reg', 'Gratis Ongkir XTRA, current rate'), ('new_reg', 'Gratis Ongkir XTRA from 1 Dec 2026')]:
        f = compute('shopee-id', sel=sel, price=89000, cost=30000, x={'gox': k})
        trs += f"<tr><td>{lab}</td><td class='n'>{IDR(f['total'])}</td><td class='n'>{IDR(f['profit'])}</td></tr>"
    big = compute('shopee-id', sel=sel, price=1500000, cost=600000, x={'gox': 'cur_reg'})
    bign = compute('shopee-id', sel=sel, price=1500000, cost=600000, x={'gox': 'new_reg'})
    return f"""
<p>Shopee Indonesia’s fees depend on your seller type and the product type. In 2026 the new-seller free period ended for sellers starting from 1 August, and the optional Gratis Ongkir XTRA programme gets new, higher rates from <b>1 December 2026</b> (1 January 2027 for Mall). This guide lists every fee and works through examples. All the numbers come from the <a href="../../shopee/indonesia/">Shopee Indonesia fee calculator</a>.</p>
<h2 id="fees">The fees on every order</h2>
<div class="tablewrap"><table><thead><tr><th>Fee</th><th>Non-Star and Star/Star+</th><th>Shopee Mall</th></tr></thead><tbody>
<tr><td>Admin fee</td><td>{pct(RNG('nonstar')[0])} to {pct(RNG('nonstar')[1])} by product type</td><td>{pct(RNG('mall')[0])} to {pct(RNG('mall')[1])} by product type</td></tr>
<tr><td>Payment fee</td><td>None</td><td>1.8%, up to {IDR(50000)} per item</td></tr>
<tr><td>Order Processing Fee</td><td>{IDR(1250)} per completed order</td><td>{IDR(1250)} per completed order</td></tr>
</tbody></table></div>
<p>Percentage fees are charged on the original price minus seller discounts and seller vouchers. Shipping is never included.</p>
<h2 id="example">Worked example</h2>
<p>An {IDR(89000)} face care product from a Non-Star or Star seller, product cost {IDR(30000)}, free shipping for the buyer, no optional programmes.</p>
{ex_table(_ex(a))}
<p>Profit is {IDR(a['profit'])}, a {a['margin']:.1f}% margin.</p>
<h2 id="gox">Gratis Ongkir XTRA from 1 December 2026</h2>
<p>Gratis Ongkir XTRA gives your products free-shipping vouchers in exchange for a fee by product type. From 1 December 2026 (non-Mall) and 1 January 2027 (Mall), most regular-size rates rise by 3 to 3.5 points and most special-size rates by 3.5 to 4. The cap per item goes from {IDR(40000)} to {IDR(60000)} for regular-size products and from {IDR(60000)} to {IDR(80000)} for special-size products. For the same face care product ({pct(r['cur_reg'])} now, {pct(r['new_reg'])} from December):</p>
<div class="tablewrap"><table><thead><tr><th>Situation</th><th class="n">Fees</th><th class="n">Profit</th></tr></thead><tbody>{trs}</tbody></table></div>
<p>The higher cap matters for expensive products. On a {IDR(1500000)} item the fee is capped at {IDR(40000)} now. From December it is capped at {IDR(60000)}: total fees go from {IDR(big['total'])} to {IDR(bign['total'])}.</p>
<h2 id="new">The new-seller free period</h2>
<p>Non-Star sellers who uploaded their first product before 1 August 2026 pay no admin fee and no Order Processing Fee until 50 completed orders or 6 months, whichever comes first. Sellers who start on or after 1 August 2026 pay the normal fees from the first order. Shopee runs separate support programmes for new small businesses instead.</p>
<h2 id="other">Other optional fees</h2>
<ul>
<li><b>Promo XTRA</b>: 4.5% (max {IDR(60000)} per item), or 6.5% for Promo XTRA+ (max {IDR(80000)}).</li>
<li><b>Live/Video XTRA</b>: 3% on orders through Shopee Live or Shopee Video, or 2% with Promo XTRA, max {IDR(20000)} per item.</li>
<li><b>Pre-order service fee</b>: 3% on pre-order products.</li>
<li><b>SPayLater XTRA 0%</b>: 2.5% (3-month) or 4% (6-month) on orders paid with SPayLater instalments.</li>
</ul>
"""

GUIDES_SID = [dict(lang='en', slug='shopee-indonesia-fees-2026', short='Shopee Indonesia fees 2026',
      title='Shopee Indonesia Seller Fees 2026: Admin Fee, Gratis Ongkir XTRA from 1 December and Mall Fees',
      desc='Every Shopee Indonesia seller fee in 2026: admin fee for Non-Star, Star/Star+ and Mall by product type, the 1.8% Mall payment fee, Rp1,250 per order, the new Gratis Ongkir XTRA rates from 1 December 2026 and worked examples.',
      market='shopee-id', cov='cov-ink', fig='1 Dec')]
GUIDE_BODY_SID = {'shopee-indonesia-fees-2026': g_shopee_id}
GUIDE_SOURCES_SID = {'shopee-indonesia-fees-2026': MARKETS['shopee-id']['sources']}
PAGE_FN_SID = {('shopee-id', 'en'): shopee_id_page}
