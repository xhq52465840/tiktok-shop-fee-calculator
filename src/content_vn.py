"""TikTok Shop Vietnam (and later Indonesia / Shopee ID & VN) page copy and guides. Every number comes from markets.compute() or the rate files."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

VN = MARKETS['tiktok-shop-vn']['selector']['options']
VND = lambda v: money(v, 'VND')
E = lambda s: f'<span lang="en">{s}</span>'

LBL = dict(commission='Commission fee', tx='Transaction fee', opf='Order Processing Fee', wht='Withheld VAT + personal income tax',
           dcf='Dynamic Commission Fee', mallsf='Mall Service Fee', lsf='Logistics Service Fee', preorder='Pre-order service fee', gxp='Growth Xtra Program fee')
PCT_ROWS = {'commission', 'tx', 'wht', 'dcf', 'mallsf', 'preorder', 'gxp'}
ID = MARKETS['tiktok-shop-id']['selector']['options']
IDR = lambda v: money(v, 'IDR')

def _ex(f, cur):
    M = lambda v: money(v, cur); rows = []
    for k, r, a in f['rows']:
        if k == 'gxp' and not a: continue
        lab = f"{LBL[k]} ({pct(r)})" if k in PCT_ROWS and r else LBL[k]
        rows.append((lab, ('+' + M(-a)) if a < 0 else ('−' + M(a))))
    rows.append(('Total fees', M(f['total']), True))
    rows.append(('Payout', M(f['payout']), True))
    return rows

def _vn(n):
    return next(o for o in VN if o['n'] == n)

# ---------------------------------------------------------------- TikTok Shop VN
VN_SAMPLE = ['Skincare › Serums & Essences', 'Makeup › Lipstick & Lip Gloss', "Women's Tops › Women's T-shirts", "Men's Tops › T-shirts",
             'Phones & Tablets › Mobile Phones', 'Desktop Computers, Laptops & Tablets › Laptops', 'Pantry Food › Instant Noodles',
             'Formula Milk & Baby Food › Growth Milk Formula', 'Dog & Cat Food › Dog Food', 'Nutrition & Wellness › Vitamins, Minerals & Wellness Supplements',
             'Gold › Gold Bracelets & Anklets']
SK = 'Skincare › Serums & Essences'

def _vn_rows():
    rows = ''
    for n in VN_SAMPLE:
        o = _vn(n)
        rows += (f"<tr><td>{E(o['g'] + ' › ' + n)}</td><td class='n'>{pct(o['r']['mp'])}</td><td class='n'>{pct(o['r']['mall'])}</td></tr>")
    return rows

def tiktok_vn_page():
    o = _vn(SK)['r']
    a = compute('tiktok-shop-vn', sel=SK, price=199000, cost=60000)
    m = compute('tiktok-shop-vn', sel=SK, store='mall', price=199000, cost=60000)
    s = compute('tiktok-shop-vn', sel=SK, price=199000, cost=60000, x={'txs': 't10'})
    h = compute('tiktok-shop-vn', sel=SK, price=199000, cost=60000, tg={'vnWht': True})
    ph = 'Phones & Tablets › Mobile Phones'
    p = compute('tiktok-shop-vn', sel=ph, price=5990000, cost=5300000)
    toc = [('how', 'How TikTok Shop Vietnam fees work'), ('examples', 'Worked examples'), ('rates', 'Sample commission rates'),
           ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How TikTok Shop Vietnam fees work</h2>
<p>TikTok Shop Vietnam charges three fees on a normal delivered order. TikTok’s own fees already include Vietnamese tax for sellers without a verified company tax code.</p>
<h3>1. Platform commission fee</h3>
<p>The commission depends on the category and on whether you sell as a Marketplace or a Mall shop. Marketplace rates are from the table effective <b>3 July 2026</b>; Mall rates are from the table effective <b>20 October 2026</b>, which also cut Mall book categories from 15% to 12.5%. The table has more than 2,000 categories, from 1.5% to {pct(max(x['r']['mp'] for x in VN))} for Marketplace and 1.5% to {pct(max(x['r']['mall'] for x in VN))} for Mall. Categories not in the table pay the default 14% (Marketplace) or 16% (Mall). Commission is charged on the item price after seller discounts. Shipping is not included.</p>
<h3>2. Transaction fee</h3>
<p>6% for orders created from 9 May 2026, on the amount the customer paid plus any platform discount, less refunds. In practice that is the item price after seller discounts plus the shipping the buyer paid. From <b>21 October 2026</b>, shops that spend on ads get a lower transaction fee, based on their ads take rate over the last 30 days: 0.5 percentage points off at 4% to under 7%, 0.7 at 7% to under 10%, 1.0 at 10% to under 15%, 1.2 at 15% to under 20%, and 1.5 at 20% or more.</p>
<h3>3. Order Processing Fee</h3>
<p>{VND(3000)} per delivered order, since 27 October 2025.</p>
<h3>4. Tax withheld for individual and household sellers</h3>
<p>Since 1 July 2025, TikTok Shop withholds 1% VAT and 0.5% personal income tax from individual and business household sellers, on the item price after seller discount. Tick the option in the calculator if this applies to you. Registered companies declare their own tax instead.</p>
<h3>What is not included</h3>
<p>From 12 October 2026 there is also a logistics service fee for parcels over 10 kg, from {VND(3000)} and capped at {VND(65000)} per parcel. Affiliate commission and ads are optional. Add affiliate commission in its field, and any other cost under other costs.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: {VND(199000)} serum, Marketplace shop</h4>
<p>Serums &amp; Essences at {pct(o['mp'])}, product cost {VND(60000)}, free shipping for the buyer.</p>
{ex_table(_ex(a, 'VND'))}
<p>Profit {VND(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same serum in a Mall shop</h4>
<p>The Mall rate is {pct(o['mall'])}: total fees {VND(m['total'])}, profit {VND(m['profit'])}.</p></div>
<div class="example"><h4>Example 3: with a 10% ads take rate</h4>
<p>A Marketplace shop whose ads take rate is between 10% and 15% gets 1.0 point off the transaction fee from 21 October 2026. The fee falls to {pct(s['rate']['tx'])} ({VND(s['fee']['tx'])}) and total fees to {VND(s['total'])}.</p></div>
<div class="example"><h4>Example 4: individual seller</h4>
<p>As an individual or household seller, {VND(h['fee']['wht'])} of tax is also withheld, so the payout is {VND(h['payout'])}.</p></div>
<div class="example"><h4>Example 5: {VND(5990000)} mobile phone</h4>
<p>Mobile phones pay {pct(_vn(ph)['r']['mp'])} on Marketplace. Fees: {VND(p['total'])}, profit {VND(p['profit'])} on a {VND(5300000)} cost.</p></div>

<h2 id="rates">Sample commission rates</h2>
<p>Marketplace rates effective 3 July 2026 and Mall rates effective 20 October 2026. The calculator has all categories.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Marketplace</th><th class="n">Mall</th></tr></thead><tbody>{_vn_rows()}</tbody></table></div>
<p>Read the full picture in our guide to <a href="../../guides/tiktok-shop-vietnam-fees-2026/">TikTok Shop Vietnam seller fees in 2026</a>.</p>
'''
    faq = [
     ('How much is the TikTok Shop Vietnam commission?', 'It depends on the category. Marketplace rates run from 1.5% to 16% and Mall rates from 1.5% to 19.8%. Categories that are not listed pay 14% (Marketplace) or 16% (Mall).'),
     ('What is the TikTok Shop Vietnam transaction fee?', '6% from 9 May 2026, on the item price after seller discounts plus the shipping the buyer paid. From 21 October 2026, shops that spend on ads can get 0.5 to 1.5 points off.'),
     ('Is there a fixed fee per order?', 'Yes. The Order Processing Fee is 3,000 ₫ per delivered order.'),
     ('Does TikTok Shop withhold tax in Vietnam?', 'Yes. Since 1 July 2025 it withholds 1% VAT and 0.5% personal income tax from individual and business household sellers.'),
    ]
    return dict(title='TikTok Shop Vietnam Fee Calculator 2026 (Commission, 6% Transaction Fee)',
                desc='Free TikTok Shop Vietnam fee and profit calculator: Marketplace and Mall commission for 2,000+ categories, the 6% transaction fee with the new ads savings, 3,000 ₫ per order and withheld tax.',
                h1='TikTok Shop Vietnam Fee Calculator',
                lede='Marketplace and Mall commission for every category, the 6% transaction fee and its new ads-based savings from 21 October 2026, 3,000 ₫ per order and the 1.5% tax withheld from individual sellers.',
                body=body, faq=faq, toc=toc)

# ---------------------------------------------------------------- TikTok Shop ID
def _id(n):
    return next(o for o in ID if o['n'] == n)
ID_SAMPLE = ['Skincare › Serums & Essences', "Women's Tops", "Men's Tops", 'Hijabs', "Women's Islamic Clothing › Abayas", 'Phones & Tablets',
             'Desktop Computers, Laptops & Tablets', 'Instant Food › Instant Noodles', 'Formula Milk & Baby Food › Growth Milk Formula',
             'Baby Care & Health › Diapers', 'Gold']
SAV = [('none', 'Default rate'), ('gmo', 'GMV Max order, shop under 3%'), ('gx', 'Growth Xtra, non-GMV Max order'), ('gxgmo', 'Growth Xtra + GMV Max order'),
       ('s3', 'Shop GMV Max spend 3% or more'), ('s3gx', 'Shop GMV Max spend 3% or more + Growth Xtra')]

def _id_rows():
    rows = ''
    for n in ID_SAMPLE:
        o = _id(n); r = o['r']
        rows += (f"<tr><td>{E(o['g'] + ' › ' + n)}</td><td class='n'>{pct(r['mp.none'])}</td><td class='n'>{pct(r['mall.none'])}</td>"
                 f"<td class='n'>{pct(r['mp.s3gx'])}</td><td class='n'>{pct(r['dcf'])}</td></tr>")
    return rows

def tiktok_id_page():
    o = _id(SK)['r']
    a = compute('tiktok-shop-id', sel=SK, price=89000, cost=30000)
    m = compute('tiktok-shop-id', sel=SK, store='mall', price=89000, cost=30000)
    s = compute('tiktok-shop-id', sel=SK, price=89000, cost=30000, x={'sav': 's3gx'})
    ph = 'Phones & Tablets'
    p = compute('tiktok-shop-id', sel=ph, price=3499000, cost=3100000)
    toc = [('how', 'How TikTok Shop Indonesia fees work'), ('examples', 'Worked examples'), ('rates', 'Sample commission rates'),
           ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f"""
<h2 id="how">How TikTok Shop Indonesia fees work</h2>
<p>TikTok Shop and Tokopedia share one seller platform and one fee schedule in Indonesia. A normal delivered order pays four core fees, plus a fifth for Mall shops. All rates include tax.</p>
<h3>1. Platform commission fee</h3>
<p>The rate depends on the category and on whether you are a Marketplace or a Mall seller: {pct(min(x['r']['mp.none'] for x in ID))} to {pct(max(x['r']['mp.none'] for x in ID))} for Marketplace and {pct(min(x['r']['mall.none'] for x in ID))} to {pct(max(x['r']['mall.none'] for x in ID))} for Mall, from the table effective <b>18 May 2026</b>. It is charged on the item price after seller discounts. Shipping and platform discounts are not included.</p>
<p>The same table lists lower rates for sellers who use GMV Max ads or join the Growth Xtra Program: per order for GMV Max orders, or for the whole shop when GMV Max spend is 3% or more of GMV over the last 30 days. With both, the saving is up to {pct(max(x['r']['mall.none'] - x['r']['mall.s3gx'] for x in ID))}. Choose your situation in the calculator.</p>
<h3>2. Dynamic Commission Fee</h3>
<p>3% to 8% by category, on the item price after seller discounts, capped at <b>{IDR(60000)} per item</b>. It funds the platform’s standard promotions such as free shipping and Bonus Cashback, and it is not refunded if a delivered order is later returned.</p>
<h3>3. Order Processing Fee</h3>
<p>{IDR(1250)} per delivered order, however many items it has. New sellers pay nothing on their first 50 orders.</p>
<h3>4. Logistics Service Fee</h3>
<p>A flat fee per order since 1 May 2026, from {IDR(540)} to {IDR(5060)} depending on the shipping service, the route and the parcel weight. The calculator starts at {IDR(690)} (standard shipping within Java to Jakarta, up to 1 kg). Change it to match your parcels.</p>
<h3>5. Mall Service Fee</h3>
<p>Mall shops pay another 1.8%, capped at {IDR(50000)} per product.</p>
<h3>Optional fees</h3>
<p>Pre-order products pay an extra 3%. The Growth Xtra Program charges its own service fee of 2% to 4% by category. Enter it in the calculator if you take part. Affiliate commission goes in its own field.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: {IDR(89000)} serum, Marketplace</h4>
<p>Serums &amp; Essences: {pct(o['mp.none'])} commission and {pct(o['dcf'])} Dynamic Commission Fee. Product cost {IDR(30000)}, free shipping for the buyer.</p>
{ex_table(_ex(a, 'IDR'))}
<p>Profit {IDR(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same serum in a Mall shop</h4>
<p>The Mall rate is {pct(o['mall.none'])}, plus the 1.8% Mall Service Fee: total fees {IDR(m['total'])}, profit {IDR(m['profit'])}.</p></div>
<div class="example"><h4>Example 3: with GMV Max and Growth Xtra</h4>
<p>A Marketplace shop with GMV Max spend of 3% or more that also joins Growth Xtra pays {pct(o['mp.s3gx'])} commission on this serum. Fees fall to {IDR(s['total'])} before the Growth Xtra fee and the ads themselves.</p></div>
<div class="example"><h4>Example 4: {IDR(3499000)} phone</h4>
<p>Phones pay {pct(_id(ph)['r']['mp.none'])} commission on Marketplace. The {pct(_id(ph)['r']['dcf'])} Dynamic Commission Fee would be {IDR(round(3499000 * 0.03))} but is capped at {IDR(60000)}. Total fees {IDR(p['total'])}, profit {IDR(p['profit'])} on a {IDR(3100000)} cost.</p></div>

<h2 id="rates">Sample commission rates</h2>
<p>Rates from the table effective 18 May 2026. The calculator has all categories and all savings columns.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Marketplace</th><th class="n">Mall</th><th class="n">Marketplace, GMV Max 3%+ and Growth Xtra</th><th class="n">Dynamic Commission Fee</th></tr></thead><tbody>{_id_rows()}</tbody></table></div>
<p>Read the full picture in our guide to <a href="../../guides/tiktok-shop-indonesia-fees-2026/">TikTok Shop Indonesia seller fees in 2026</a>.</p>
"""
    faq = [
     ('How much is the TikTok Shop Indonesia commission?', 'The platform commission fee is 2.5% to 10.2% for Marketplace and 2.5% to 12.2% for Mall, by category, from 18 May 2026. On top of that there is a Dynamic Commission Fee of 3% to 8%, capped at Rp60,000 per item.'),
     ('Are TikTok Shop and Tokopedia fees the same?', 'Yes. Since the merger they use one seller platform and one fee schedule in Indonesia.'),
     ('What is the Dynamic Commission Fee?', 'A second commission of 3% to 8% by category that pays for the platform’s standard promotions such as free shipping and Bonus Cashback. It is capped at Rp60,000 per item.'),
     ('How do the commission savings work?', 'Sellers who use GMV Max ads or join the Growth Xtra Program get lower commission rates. GMV Max orders get a per-order saving. Shops whose GMV Max spend is 3% or more of GMV get a shop-wide saving, and combining it with Growth Xtra gives the biggest saving, up to 8.18 points.'),
     ('Is there a fee per order?', 'Yes. The Order Processing Fee is Rp1,250 per delivered order (free for a new seller’s first 50 orders), and the Logistics Service Fee is Rp540 to Rp5,060 per order.'),
    ]
    return dict(title='TikTok Shop Indonesia Fee Calculator 2026 (Tokopedia, Commission + Dynamic Fee)',
                desc='Free TikTok Shop & Tokopedia Indonesia fee and profit calculator: Marketplace and Mall commission for 1,100 categories, GMV Max and Growth Xtra savings, the 3–8% Dynamic Commission Fee, Rp1,250 per order and the Logistics Service Fee.',
                h1='TikTok Shop Indonesia Fee Calculator',
                lede='Marketplace and Mall commission for every category from 18 May 2026, with GMV Max and Growth Xtra savings, the Dynamic Commission Fee capped at Rp60,000, the Mall Service Fee, Rp1,250 per order and the Logistics Service Fee.',
                body=body, faq=faq, toc=toc)

def g_tiktok_id():
    o = _id(SK)['r']
    a = compute('tiktok-shop-id', sel=SK, price=89000, cost=30000)
    trs = ''
    for k, lab in SAV:
        f = compute('tiktok-shop-id', sel=SK, price=89000, cost=30000, x={'sav': k})
        trs += f"<tr><td>{lab}</td><td class='n'>{pct(f['rate']['commission'])}</td><td class='n'>{IDR(f['total'])}</td><td class='n'>{IDR(f['profit'])}</td></tr>"
    lsf = [('Java ↔ Jakarta', 690, 890, 1620), ('Java ↔ Java (outside Jakarta)', 990, 1090, 2220), ('Java ↔ Bali', 1720, 2220, 4150),
           ('Java ↔ Sumatra', 2830, 3330, 5060), ('Java ↔ Sulawesi', 3940, 4850, 5060), ('Java ↔ Papua & Maluku', 5060, 5060, 5060),
           ('Within Bali', 540, 680, 1340), ('Within Sumatra', 750, 1090, 1880)]
    lrows = ''.join(f"<tr><td>{r}</td><td class='n'>{IDR(x)}</td><td class='n'>{IDR(y)}</td><td class='n'>{IDR(z)}</td></tr>" for r, x, y, z in lsf)
    return f"""
<p>TikTok Shop and Tokopedia now share one seller platform in Indonesia, and their fees changed on <b>18 May 2026</b>: a new commission table by category, a higher Dynamic Commission Fee, and lower rates for sellers who use GMV Max ads or the Growth Xtra Program. This guide lists every fee on a normal order and works through an example. All the numbers come from the <a href="../../tiktok-shop/indonesia/">TikTok Shop Indonesia fee calculator</a>.</p>
<h2 id="fees">The fees on every order</h2>
<div class="tablewrap"><table><thead><tr><th>Fee</th><th>Rate</th><th>Charged on</th></tr></thead><tbody>
<tr><td>Platform commission fee</td><td>2.5% to 10.2% (Marketplace), 2.5% to 12.2% (Mall) by category</td><td>Item price after seller discounts</td></tr>
<tr><td>Dynamic Commission Fee</td><td>3% to 8% by category, up to {IDR(60000)} per item</td><td>Item price after seller discounts</td></tr>
<tr><td>Order Processing Fee</td><td>{IDR(1250)} per order (first 50 orders free for new sellers)</td><td>Each delivered order</td></tr>
<tr><td>Logistics Service Fee</td><td>{IDR(540)} to {IDR(5060)} per order</td><td>Shipping service, route and parcel weight</td></tr>
<tr><td>Mall Service Fee</td><td>1.8%, up to {IDR(50000)} per product (Mall only)</td><td>Item price after seller discounts</td></tr>
</tbody></table></div>
<h2 id="example">Worked example</h2>
<p>An {IDR(89000)} serum on Marketplace, product cost {IDR(30000)}, free shipping for the buyer, no savings programme.</p>
{ex_table(_ex(a, 'IDR'))}
<p>Profit is {IDR(a['profit'])}, a {a['margin']:.1f}% margin. Commission and the Dynamic Commission Fee together take {pct(o['mp.none'] + o['dcf'])} of the price.</p>
<h2 id="savings">GMV Max and Growth Xtra savings</h2>
<p>Since 18 May 2026 the commission table has a column for each savings situation. GMV Max orders get a lower rate per order. A shop whose GMV Max spend (Product and LIVE GMV Max) is 3% or more of its GMV over the last 30 days gets a lower rate on every order. Growth Xtra members get a shop-wide saving too, and the biggest saving, up to 8.18 points, goes to shops that do both. For the same serum on Marketplace:</p>
<div class="tablewrap"><table><thead><tr><th>Situation</th><th class="n">Commission</th><th class="n">Fees</th><th class="n">Profit</th></tr></thead><tbody>{trs}</tbody></table></div>
<p>The savings are not free. GMV Max is paid advertising, and Growth Xtra has its own service fee of 2% to 4%. Check that the extra sales cover both.</p>
<h2 id="logistics">The Logistics Service Fee</h2>
<p>Since 1 May 2026 every order also pays a flat Logistics Service Fee. It depends on the shipping service, the route and the chargeable weight (the higher of actual and volumetric weight, length × width × height in cm ÷ 6,000). Standard shipping:</p>
<div class="tablewrap"><table><thead><tr><th>Route</th><th class="n">Up to 1 kg</th><th class="n">1–2 kg</th><th class="n">2–3 kg</th></tr></thead><tbody>{lrows}</tbody></table></div>
<p>Economy, cargo and instant or same-day shipping have their own rates. The fee is not refunded when a delivered order is returned.</p>
<h2 id="other">Fees that apply only sometimes</h2>
<ul>
<li><b>Pre-order service fee</b>: 3% of the item price after seller discount, on pre-order products.</li>
<li><b>Growth Xtra Program fee</b>: 2% to 4% by category for members, plus 2% (up to Rp20,000 per item) for GXP Super.</li>
<li><b>Affiliate commission</b>: the rate you set for creators, on affiliate orders only.</li>
</ul>
"""

# ---------------------------------------------------------------- guide
GUIDES_VN = [
 dict(lang='en', slug='tiktok-shop-vietnam-fees-2026', short='TikTok Shop Vietnam fees 2026',
      title='TikTok Shop Vietnam Seller Fees 2026: Commission, 6% Transaction Fee and the New Ads Savings',
      desc='Every TikTok Shop Vietnam seller fee in 2026: category commission for Marketplace and Mall, the 6% transaction fee and its savings tiers from 21 October, 3,000 ₫ per order, withheld tax and a worked example.',
      market='tiktok-shop-vn', cov='cov-ink', fig='6%'),
 dict(lang='en', slug='tiktok-shop-indonesia-fees-2026', short='TikTok Shop Indonesia fees 2026',
      title='TikTok Shop Indonesia Seller Fees 2026: Commission, Dynamic Commission Fee and GMV Max Savings',
      desc='Every TikTok Shop and Tokopedia seller fee in Indonesia in 2026: commission by category from 18 May, the 3–8% Dynamic Commission Fee, GMV Max and Growth Xtra savings, Rp1,250 per order, the Logistics Service Fee and a worked example.',
      market='tiktok-shop-id', cov='cov-amber', fig='8.18%'),
]

def g_tiktok_vn():
    o = _vn(SK)['r']
    a = compute('tiktok-shop-vn', sel=SK, price=199000, cost=60000, buyerShip=0)
    m = compute('tiktok-shop-vn', sel=SK, store='mall', price=199000, cost=60000)
    tiers = [('none', 'Under 4%'), ('t05', '4% to under 7%'), ('t07', '7% to under 10%'), ('t10', '10% to under 15%'), ('t12', '15% to under 20%'), ('t15', '20% or more')]
    trs = ''
    for k, lab in tiers:
        f = compute('tiktok-shop-vn', sel=SK, price=199000, cost=60000, x={'txs': k})
        trs += f"<tr><td>{lab}</td><td class='n'>{pct(f['rate']['tx'])}</td><td class='n'>{VND(f['fee']['tx'])}</td><td class='n'>{VND(f['profit'])}</td></tr>"
    return f'''
<p>TikTok Shop Vietnam’s fees changed several times in 2026: a new Marketplace commission table on 3 July, a new Mall table on 20 October, and transaction fee savings for shops that advertise from 21 October. This guide lists every fee on a normal order and works through an example. All the numbers come from the <a href="../../tiktok-shop/vietnam/">TikTok Shop Vietnam fee calculator</a>.</p>
<h2 id="fees">The fees on every order</h2>
<div class="tablewrap"><table><thead><tr><th>Fee</th><th>Rate</th><th>Charged on</th></tr></thead><tbody>
<tr><td>Platform commission fee</td><td>1.5% to 19.8% by category (default 14% Marketplace, 16% Mall)</td><td>Item price after seller discounts</td></tr>
<tr><td>Transaction fee</td><td>6% (less 0.5 to 1.5 points with ads savings)</td><td>Item price after seller discounts + buyer shipping</td></tr>
<tr><td>Order Processing Fee</td><td>{VND(3000)} per order</td><td>Each delivered order</td></tr>
<tr><td>Withheld VAT + personal income tax</td><td>1% + 0.5% (individual and household sellers only)</td><td>Item price after seller discounts</td></tr>
</tbody></table></div>
<h2 id="commission">Commission: Marketplace and Mall</h2>
<p>Commission depends on the category level 3 of the product. Marketplace shops use the table effective 3 July 2026 and Mall shops the table effective 20 October 2026. Mall rates are usually 2 to 4 points higher: Serums &amp; Essences pay {pct(o['mp'])} on Marketplace and {pct(o['mall'])} in Mall. Mall book categories are the exception. Since 20 October 2026 they pay 12.5%, less than the Marketplace rate. Phones and laptops are among the cheapest categories, at 2% to 3.8%.</p>
<h2 id="tx">The 6% transaction fee and the new savings</h2>
<p>The transaction fee is 6% for orders created from 9 May 2026. It is charged on what the buyer paid plus any platform discount, so it includes the shipping the buyer paid. From 21 October 2026 TikTok Shop gives a saving based on the shop’s ads take rate (ads spend as a share of GMV) over the last 30 days. For a {VND(199000)} serum on Marketplace:</p>
<div class="tablewrap"><table><thead><tr><th>Ads take rate</th><th class="n">Transaction fee</th><th class="n">Fee</th><th class="n">Profit</th></tr></thead><tbody>{trs}</tbody></table></div>
<p>The saving only pays for itself if the ads bring in the sales. At a 10% take rate you spend far more on ads than the 1 point you save.</p>
<h2 id="example">Worked example</h2>
<p>A {VND(199000)} serum on Marketplace, product cost {VND(60000)}, free shipping for the buyer and no ads savings.</p>
{ex_table(_ex(a, 'VND'))}
<p>Profit is {VND(a['profit'])}, a {a['margin']:.1f}% margin. In a Mall shop the same sale costs {VND(m['total'])} in fees, leaving {VND(m['profit'])}.</p>
<h2 id="tax">Tax for individual and household sellers</h2>
<p>Since 1 July 2025, TikTok Shop withholds tax from individual and business household sellers: 1% VAT and 0.5% personal income tax on the item price after seller discount. On the serum that is {VND(round(199000 * 0.015))}. TikTok’s own fees include Vietnamese tax unless you are a company with a verified tax code.</p>
<h2 id="other">Fees that apply only sometimes</h2>
<ul>
<li><b>Logistics service fee</b>: from 12 October 2026, for parcels over 10 kg only. It starts at {VND(3000)} and is capped at {VND(65000)} per parcel.</li>
<li><b>Affiliate commission</b>: the rate you set for creators, on affiliate orders only.</li>
</ul>
'''

GUIDE_BODY_VN = {'tiktok-shop-vietnam-fees-2026': g_tiktok_vn, 'tiktok-shop-indonesia-fees-2026': g_tiktok_id}
GUIDE_SOURCES_VN = {'tiktok-shop-vietnam-fees-2026': MARKETS['tiktok-shop-vn']['sources'], 'tiktok-shop-indonesia-fees-2026': MARKETS['tiktok-shop-id']['sources']}
PAGE_FN_VN = {('tiktok-shop-vn', 'en'): tiktok_vn_page, ('tiktok-shop-id', 'en'): tiktok_id_page}
