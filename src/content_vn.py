"""TikTok Shop Vietnam (and later Indonesia / Shopee ID & VN) page copy and guides. Every number comes from markets.compute() or the rate files."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

VN = MARKETS['tiktok-shop-vn']['selector']['options']
VND = lambda v: money(v, 'VND')
E = lambda s: f'<span lang="en">{s}</span>'

LBL = dict(commission='Commission fee', tx='Transaction fee', opf='Order Processing Fee', wht='Withheld VAT + personal income tax')
PCT_ROWS = {'commission', 'tx', 'wht'}

def _ex(f, cur):
    M = lambda v: money(v, cur); rows = []
    for k, r, a in f['rows']:
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

# ---------------------------------------------------------------- guide
GUIDES_VN = [
 dict(lang='en', slug='tiktok-shop-vietnam-fees-2026', short='TikTok Shop Vietnam fees 2026',
      title='TikTok Shop Vietnam Seller Fees 2026: Commission, 6% Transaction Fee and the New Ads Savings',
      desc='Every TikTok Shop Vietnam seller fee in 2026: category commission for Marketplace and Mall, the 6% transaction fee and its savings tiers from 21 October, 3,000 ₫ per order, withheld tax and a worked example.',
      market='tiktok-shop-vn', cov='cov-ink', fig='6%'),
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

GUIDE_BODY_VN = {'tiktok-shop-vietnam-fees-2026': g_tiktok_vn}
GUIDE_SOURCES_VN = {'tiktok-shop-vietnam-fees-2026': MARKETS['tiktok-shop-vn']['sources']}
PAGE_FN_VN = {('tiktok-shop-vn', 'en'): tiktok_vn_page}
