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

# ---------------------------------------------------------------- Shopee Vietnam
SVN = MARKETS['shopee-vn']['selector']['options']
VND = lambda v: money(v, 'VND')
V = lambda s: f'<span lang="vi">{s}</span>'
LBLV = dict(fixedfee='Fixed fee', tx='Transaction processing fee', infra='Infrastructure fee', vxtra='Voucher Xtra service fee',
            piship='PiShip service fee', wht='Withheld VAT + personal income tax')
def _exv(f):
    rows = [((f"{LBLV[k]} ({pct(r)})" if k in ('fixedfee', 'tx', 'vxtra', 'wht') and r else LBLV[k]), '−' + VND(a)) for k, r, a in f['rows']]
    rows.append(('Total fees', VND(f['total']), True)); rows.append(('Payout', VND(f['payout']), True))
    return rows
def _ov(g, n):
    return next(o for o in SVN if o['g'] == g and o['n'] == n)
SR = ('Sắc Đẹp', 'Chăm sóc da mặt › Tinh chất dưỡng')
VSAMPLE = [SR, ('Thời Trang Nữ', 'Đầm'), ('Thời Trang Nam', 'Quần jean'), ('Điện Thoại & Phụ Kiện', 'Điện thoại'), ('Máy tính & Laptop', 'Laptop'),
           ('Mẹ & Bé', 'Tã & bô em bé › Tã dùng một lần'), ('Thực phẩm và đồ uống', 'Đồ chế biến sẵn › Mì ăn liền'), ('Nhà cửa & Đời sống', 'Dụng cụ chăm sóc nhà cửa › Chổi'),
           ('Sách & Tạp Chí', 'Sách › Truyện Tranh')]
VRNG = lambda k: (min(o['r'][k] for o in SVN if o['r'].get(k) is not None), max(o['r'][k] for o in SVN if o['r'].get(k) is not None))

def _vrows():
    out = ''
    for g, n in VSAMPLE:
        try: r = _ov(g, n)['r']
        except StopIteration: continue
        out += f"<tr><td>{V(g + ' › ' + n)}</td><td class='n'>{pct(r['mp']) if r['mp'] is not None else '–'}</td><td class='n'>{pct(r['mall']) if r['mall'] is not None else '–'}</td></tr>"
    return out

def shopee_vn_page():
    r = _ov(*SR)['r']; sel = SVN.index(_ov(*SR))
    a = compute('shopee-vn', sel=sel, price=199000, cost=60000)
    m = compute('shopee-vn', sel=sel, store='mall', price=199000, cost=60000)
    x = compute('shopee-vn', sel=sel, price=199000, cost=60000, tg={'vXtra': 1, 'svWht': 1})
    lo, hi = VRNG('mp'); mlo, mhi = VRNG('mall')
    toc = [('how', 'How Shopee Vietnam fees work'), ('examples', 'Worked examples'), ('rates', 'Sample rates'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f"""
<h2 id="how">How Shopee Vietnam fees work</h2>
<p>Every delivered Shopee Vietnam order pays three fees. All rates include VAT.</p>
<h3>1. Fixed fee (commission)</h3>
<p>The fixed fee (Phí Cố Định) is Shopee’s commission, a percentage by level-3 category, charged on each item’s value: {pct(lo)} to {pct(hi)} for non-Mall shops from the table effective <b>23 May 2026</b>, and {pct(mlo)} to {pct(mhi)} for Shopee Mall from the table effective <b>4 October 2026</b>. New non-Mall shops pay no fixed fee for the first 30 days after their first product goes live.</p>
<h3>2. Transaction processing fee</h3>
<p>6% for every payment method (Phí Xử Lý Giao Dịch, renamed from Phí Thanh Toán in April 2026). It is charged on the item price plus the shipping the buyer paid, minus seller promotions.</p>
<h3>3. Infrastructure fee</h3>
<p>{VND(3000)} per delivered order (Phí Hạ Tầng).</p>
<h3>Optional fees and tax</h3>
<p>Voucher Xtra costs 5.5% of each item, capped at {VND(50000)} per item, and PiShip {VND(2700)} per order. For individual and business household sellers Shopee also withholds 1% VAT and 0.5% personal income tax on the item price after seller discount.</p>
<p>A few vehicle-parts categories are named differently in the non-Mall and Mall tables, so they show a rate for one shop type only.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: {VND(199000)} serum, non-Mall</h4>
<p>Serums pay a {pct(r['mp'])} fixed fee. Product cost {VND(60000)}, free shipping for the buyer.</p>
{ex_table(_exv(a))}
<p>Profit {VND(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same serum in Shopee Mall</h4>
<p>The Mall fixed fee is {pct(r['mall'])}: total fees {VND(m['total'])}, profit {VND(m['profit'])}.</p></div>
<div class="example"><h4>Example 3: household seller with Voucher Xtra</h4>
<p>Add Voucher Xtra and the withheld tax: total {VND(x['total'])}, profit {VND(x['profit'])}.</p></div>

<h2 id="rates">Sample rates</h2>
<p>Fixed fee by category. The calculator has all {len(SVN):,} categories.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Non-Mall (23 May 2026)</th><th class="n">Mall (4 Oct 2026)</th></tr></thead><tbody>{_vrows()}</tbody></table></div>
<p>Read the full picture in our guide to <a href="../../guides/shopee-vietnam-fees-2026/">Shopee Vietnam seller fees in 2026</a>.</p>
"""
    faq = [
     ('How much is the Shopee Vietnam commission?', f'The fixed fee is {pct(lo)} to {pct(hi)} for non-Mall shops and {pct(mlo)} to {pct(mhi)} for Shopee Mall, by category. On top of that there is a 6% transaction processing fee and {VND(3000)} per order.'),
     ('Is the Shopee Vietnam payment fee 6%?', 'Yes. Since 1 May 2026 (non-Mall) and 8 May 2026 (Mall) the transaction processing fee is 6% for every payment method, including COD. It includes the shipping the buyer paid.'),
     ('Does Shopee withhold tax?', 'For individual and business household sellers, yes: 1% VAT and 0.5% personal income tax on goods, since 1 July 2025. Registered companies declare their own tax.'),
     ('Do new shops pay the fixed fee?', 'New non-Mall shops pay no fixed fee for 30 days after their first product goes live. The other fees still apply.'),
    ]
    return dict(title='Shopee Vietnam Fee Calculator 2026 (Fixed Fee, 6% Transaction Fee, Mall)',
                desc='Free Shopee Vietnam fee and profit calculator: non-Mall and Mall fixed fee for 1,500+ categories, the 6% transaction processing fee, 3,000 ₫ per order, Voucher Xtra, PiShip and the withheld tax for household sellers.',
                h1='Shopee Vietnam Fee Calculator',
                lede='Non-Mall fixed fee from 23 May 2026 and Mall fixed fee from 4 October 2026 for every category, the 6% transaction processing fee, the 3,000 ₫ infrastructure fee, Voucher Xtra, PiShip and the withheld tax.',
                body=body, faq=faq, toc=toc)

def g_shopee_vn():
    r = _ov(*SR)['r']; sel = SVN.index(_ov(*SR))
    a = compute('shopee-vn', sel=sel, price=199000, cost=60000)
    big = compute('shopee-vn', sel=sel, price=1500000, cost=600000, tg={'vXtra': 1})
    return f"""
<p>Shopee Vietnam raised most of its fees in 2026: a 6% transaction processing fee for every payment method from May, a new non-Mall fixed fee table on <b>23 May 2026</b>, and Voucher Xtra going from 4% to 5.5%. This guide lists every fee and works through an example. All the numbers come from the <a href="../../shopee/vietnam/">Shopee Vietnam fee calculator</a>.</p>
<h2 id="fees">The fees on every order</h2>
<div class="tablewrap"><table><thead><tr><th>Fee</th><th>Rate</th><th>Charged on</th></tr></thead><tbody>
<tr><td>Fixed fee</td><td>{pct(VRNG('mp')[0])} to {pct(VRNG('mp')[1])} (non-Mall), {pct(VRNG('mall')[0])} to {pct(VRNG('mall')[1])} (Mall) by category</td><td>Each item’s value</td></tr>
<tr><td>Transaction processing fee</td><td>6%</td><td>Item price + buyer shipping − seller promotions</td></tr>
<tr><td>Infrastructure fee</td><td>{VND(3000)} per order</td><td>Each delivered order</td></tr>
<tr><td>Withheld VAT + personal income tax</td><td>1% + 0.5% (individual and household sellers only)</td><td>Item price after seller discounts</td></tr>
</tbody></table></div>
<h2 id="example">Worked example</h2>
<p>A {VND(199000)} serum from a non-Mall shop, product cost {VND(60000)}, free shipping for the buyer.</p>
{ex_table(_exv(a))}
<p>Profit is {VND(a['profit'])}, a {a['margin']:.1f}% margin. The fixed fee and the transaction fee together take {pct(r['mp'] + 6)} of the price.</p>
<h2 id="changes">What changed in 2026</h2>
<ul>
<li><b>1 May 2026</b> (non-Mall) and <b>8 May 2026</b> (Mall): the transaction processing fee became 6% for every payment method.</li>
<li><b>23 May 2026</b>: new non-Mall fixed fee table. Beauty went from 14% to 17%, fashion from 12.5–13.5% to 13.5–16.5%. Voucher Xtra went from 4% to 5.5% (still capped at {VND(50000)} per item) and PiShip from {VND(1620)} to {VND(2700)} per order.</li>
<li><b>29 May 2026</b>: new Mall fixed fee table, updated again for books and magazines on <b>4 October 2026</b>.</li>
</ul>
<h2 id="vxtra">Voucher Xtra</h2>
<p>Voucher Xtra sends your shop’s vouchers to buyers every week. Its 5.5% fee is capped at {VND(50000)} per item, so it costs less in percentage terms on expensive items: on a {VND(1500000)} serum the fee is {VND(50000)} instead of {VND(82500)}, and total fees are {VND(big['total'])}.</p>
<h2 id="tax">Tax for individual and household sellers</h2>
<p>Since 1 July 2025, Shopee withholds tax from individual and business household sellers under Decree 117/2025: 1% VAT and 0.5% personal income tax on goods (5% and 2% on services), on the item price after seller discount. On the serum that is {VND(round(199000 * 0.015))}.</p>
"""
GUIDES_SID.append(dict(lang='en', slug='shopee-vietnam-fees-2026', short='Shopee Vietnam fees 2026',
      title='Shopee Vietnam Seller Fees 2026: Fixed Fee by Category, the 6% Transaction Fee and Voucher Xtra',
      desc='Every Shopee Vietnam seller fee in 2026: non-Mall and Mall fixed fee by category, the 6% transaction processing fee, 3,000 ₫ per order, Voucher Xtra 5.5%, withheld tax and a worked example.',
      market='shopee-vn', cov='cov-amber', fig='6%'))
GUIDE_BODY_SID['shopee-vietnam-fees-2026'] = g_shopee_vn
GUIDE_SOURCES_SID['shopee-vietnam-fees-2026'] = MARKETS['shopee-vn']['sources']
PAGE_FN_SID[('shopee-vn', 'en')] = shopee_vn_page
