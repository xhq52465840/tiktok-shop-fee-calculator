"""Walmart US, Shopee PH and Shopee TH page copy and guides. Every number comes from markets.compute() or the rate files."""
from markets import MARKETS, compute, WFS_STD
from site_helpers import money, pct, ex_table

WM = MARKETS['walmart-us']['selector']['options']
PH = MARKETS['shopee-ph']['selector']['options']
TH = MARKETS['shopee-th']['selector']['options']
USD = lambda v: money(v, 'USD'); PHP = lambda v: money(v, 'PHP'); THB = lambda v: money(v, 'THB')
E = lambda s: f'<span lang="en">{s}</span>'

LBL = dict(referral='Referral fee', nss='New-Seller Savings discount', wfs='WFS fulfillment fee', wfs_app='WFS apparel surcharge',
           wfs_haz='WFS hazmat surcharge', wfs_low='WFS surcharge, item under $10', wfs_ovr='WFS oversize surcharge',
           wfs_credit='New-Seller Savings WFS discount', commission='Commission fee', tx='Transaction fee',
           psf_ph='Platform Shipping Fee', sgsf='Seller Growth Support Fee', opf='Order Processing Fee',
           mdv='Mega Discount Voucher service fee', pif='Platform Infrastructure Fee', svc='Programme service fees')
PCT_ROWS = {'referral', 'nss', 'wfs_credit', 'commission', 'tx', 'psf_ph', 'sgsf', 'mdv'}

def _ex(f, cur, ship_label=None):
    M = lambda v: money(v, cur); rows = []
    for k, r, a in f['rows']:
        if k == 'svc' and not a: continue
        lab = f"{LBL[k]} ({pct(r)})" if k in PCT_ROWS and r else LBL[k]
        rows.append((lab, ('+' + M(-a)) if a < 0 else ('−' + M(a))))
    rows.append(('Total fees', M(f['total']), True))
    rows.append(('Payout', M(f['payout']), True))
    return rows

def _wm_rule(o):
    r = o['r']
    if 'bands' in r:
        parts, lo = [], None
        for mx, rate in r['bands']:
            parts.append(f"{pct(rate)} up to ${mx:g}"); lo = mx
        parts.append(f"{pct(r['rate'])} above ${lo:g}")
        return '; '.join(parts) + ' (whole price)'
    if 'at' in r:
        return f"{pct(r['rate'])} on the portion up to ${r['at']:,g}; {pct(r['over'])} on the portion above"
    return pct(r['rate'])

# ---------------------------------------------------------------- Walmart US
def walmart_us_page():
    hk = 'Home, Kitchen, Decor & Garden'
    a = compute('walmart-us', sel=hk, price=24.99, cost=8)
    b = compute('walmart-us', sel=hk, price=24.99, cost=8, x={'nss': 't20'})
    c = compute('walmart-us', sel=hk, store='wfs', price=24.99, cost=8, wt=1.5)
    ap = compute('walmart-us', sel='Apparel & Accessories', store='wfs', price=14.99, cost=4, wt=0.6, tg={'wfsApparel': True})
    ea = compute('walmart-us', sel='Electronics Accessories', price=129, cost=60)
    nine = compute('walmart-us', sel=hk, store='wfs', price=40, wt=9)
    rows = ''.join(f"<tr><td>{E(o['n'])}</td><td>{_wm_rule(o)}</td></tr>" for o in WM)
    wfs_rows = ''.join(
        f"<tr><td>{('Up to 1 lb' if mx == 1 else (f'{mx} lb' if mx in (2, 3) else f'{frm if frm else 4}–{mx} lb'))}</td><td class='n'>{USD(base)}{(' + ' + USD(per) + ' per lb above ' + str(frm) + ' lb') if per else ''}</td></tr>"
        for mx, base, per, frm in WFS_STD)
    toc = [('how', 'How Walmart Marketplace fees work'), ('nss', 'New-Seller Savings 2026'), ('wfs', 'Walmart Fulfillment Services fees'),
           ('examples', 'Worked examples'), ('rates', 'Referral fees by category'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Walmart Marketplace fees work</h2>
<p>Walmart Marketplace (US) charges no monthly subscription and no setup fee. On each sale you pay a <b>referral fee</b>: a percentage of the total sales price, which includes the item price plus any shipping, handling and gift-wrap charges paid by the customer. Walmart deducts it from your payout. If you use Walmart Fulfillment Services (WFS), fulfillment and storage fees are added on top.</p>
<h3>1. Referral fee</h3>
<p>Most categories pay a flat rate, usually 15%. Some categories use one of two other rules, and the calculator applies both automatically:</p>
<ul>
<li><b>Whole-price bands.</b> One rate applies to the whole item, depending on its total sales price. For example, Beauty, Health &amp; Personal Care pays 8% if the item sells for $10 or less and 15% above $10.</li>
<li><b>Portion tiers.</b> One rate applies to the part of the price up to a threshold and a second rate to the part above it. For example, Electronics Accessories pays 15% on the first $100 and 8% on the rest.</li>
</ul>
<p>Some secondary sources report that Walmart lowered rates in several categories from June 2026, but Walmart’s published schedule above has not changed. Each rate in the calculator can be edited, so check the commission rate column in your Seller Center payment statements and enter your own rate if it differs.</p>

<h2 id="nss">New-Seller Savings 2026</h2>
<p>First-time sellers who go live after 1 February 2026 and opt in through the Seller Center form get a discount on referral fees. The discount depends on GMV (gross merchandise value) since launch:</p>
<div class="tablewrap"><table><thead><tr><th>GMV since launch</th><th class="n">Referral fee discount</th></tr></thead><tbody>
<tr><td>$0.01–$50,000</td><td class="n">20%</td></tr><tr><td>$50,001–$500,000</td><td class="n">30%</td></tr><tr><td>Over $500,000</td><td class="n">40%</td></tr></tbody></table></div>
<p>The program runs from 2 February 2026 to 31 January 2027. Discounts stop on 31 January 2027 or when you reach the $72,000 maximum, whichever comes first. Sellers who joined between 1 February and 27 April 2026 do not need to enroll by clicking. Eligible sellers using WFS also get 10% of their fulfillment fees back, up to $2,000. The offer includes other incentives as well (a sponsored-search ad rebate and Walmart Connect credits); they don’t change per-order fees, so the calculator leaves them out. Choose your tier in the calculator to see the discount as a separate credit line.</p>

<h2 id="wfs">Walmart Fulfillment Services fees</h2>
<p>WFS charges a fulfillment fee per unit, based on shipping weight. Under 1 lb, Walmart adds 0.25 lb for packaging to the unit weight and rounds up. From 1 lb to 150 lb, the shipping weight is the greater of the unit weight and the dimensional weight (length × width × height in inches ÷ 139), rounded up to the next whole pound. The standard base fees, in effect since April 2025, are:</p>
<div class="tablewrap"><table><thead><tr><th>Shipping weight</th><th class="n">Fee per unit</th></tr></thead><tbody>{wfs_rows}</tbody></table></div>
<p>Walmart’s published table shows a lower starting fee for 31–50 lb ($14.55) than for 21–30 lb ($15.55). The calculator uses the table exactly as published.</p>
<p>Surcharges per unit: apparel $0.50, hazardous materials $0.50, items priced under $10 $1.00, oversize $3.00 (longest side over 48 in, median side over 30 in, or longest side + girth over 105 in). Larger oversize items ($20, with weight counted as at least 90 lb) and Big &amp; Bulky items ($155 plus $0.80 for each pound above 90 lb) follow different rules and are not covered here. Storage costs $0.75 per cubic foot per month, rising after 30 days in October–December. From 30 June 2026, long-term storage is $2.25 per cubic foot for 366–450 days and $7.50 above 450 days. Enter storage under other costs.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: $24.99 home item shipped by the seller</h4>
<p>Home, Kitchen, Decor &amp; Garden at 15%, product cost $8, no shipping charged to the customer.</p>
{ex_table(_ex(a, 'USD'))}
<p>Profit {USD(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same item with New-Seller Savings (20% tier)</h4>
{ex_table(_ex(b, 'USD'))}
<p>The referral fee drops from {USD(a['total'])} to {USD(b['total'])}, so profit rises to {USD(b['profit'])}.</p></div>
<div class="example"><h4>Example 3: the same item fulfilled by WFS (1.5 lb)</h4>
<p>A 1.5 lb unit rounds up to 2 lb, so the base fee is {USD(c['fee']['wfs'])}.</p>
{ex_table(_ex(c, 'USD'))}
<p>Profit {USD(c['profit'])}. If you ship it yourself, include your own shipping cost before comparing the two.</p></div>
<div class="example"><h4>Example 4: $14.99 T-shirt fulfilled by WFS (0.6 lb)</h4>
<p>Apparel sold for $15 or less pays a 5% referral fee. 0.6 lb + 0.25 lb rounds up to 1 lb, and the apparel surcharge is added.</p>
{ex_table(_ex(ap, 'USD'))}</div>
<div class="example"><h4>Example 5: $129 electronics accessory, portion tiers</h4>
<p>15% on the first $100 ($15.00) plus 8% on the remaining $29 ($2.32) gives a referral fee of {USD(ea['fee']['referral'])}.</p></div>
<p>Check: Walmart’s pricing page works through a 9 lb item with a WFS fee of $7.75. The calculator gives {USD(nine['fee']['wfs'])}.</p>

<h2 id="rates">Referral fees by category</h2>
<p>From Walmart’s referral fee schedule for contract categories, updated 9 March 2026. Rates apply to the total sales price.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th>Referral fee</th></tr></thead><tbody>{rows}</tbody></table></div>
'''
    faq = [
     ('Does Walmart Marketplace charge a monthly fee?', 'No. Walmart Marketplace has no monthly subscription and no setup fee. You pay a referral fee on each sale, plus WFS fees if you use Walmart fulfillment.'),
     ('Is the referral fee charged on shipping?', 'Yes. Walmart calculates the referral fee on the total sales price, which includes the item price and any shipping, handling and gift-wrap charges paid by the customer.'),
     ('How does the 2026 New-Seller Savings discount work?', 'First-time sellers who go live after 1 February 2026 and opt in get 20%, 30% or 40% off referral fees depending on GMV since launch, until 31 January 2027 or a $72,000 maximum. Eligible WFS users also get 10% of fulfillment fees back, up to $2,000.'),
     ('How is the WFS shipping weight calculated?', 'Under 1 lb, Walmart adds 0.25 lb to the unit weight and rounds up. From 1 lb, it takes the greater of the unit weight and the dimensional weight (L × W × H ÷ 139) and rounds up to the next pound.'),
     ('Why does my statement show a different referral rate?', 'Some categories may be on a contract or updated rate. Every rate in the calculator can be edited, so enter the commission rate shown in your Seller Center statements.'),
    ]
    return dict(title='Walmart Marketplace Fee Calculator 2026 (Referral Fees, WFS & New-Seller Savings)',
                desc='Free Walmart Marketplace (US) fee and profit calculator with the official referral fee schedule, price bands and tiers, 2026 New-Seller Savings discounts and WFS fulfillment fees by weight.',
                h1='Walmart Marketplace Fee Calculator',
                lede='Referral fees by category with Walmart’s price bands and tiers, the 2026 New-Seller Savings discount and WFS fulfillment fees by shipping weight. See your payout and margin before you list.',
                body=body, faq=faq, toc=toc)

# ---------------------------------------------------------------- Shopee PH
def shopee_ph_page():
    off = compute('shopee-ph', sel='Mobile Phones', store='mall', tg={'mdv': True}, price=400, sellerDisc=30, buyerShip=50, shipCost=50)
    wc = compute('shopee-ph', sel='Women Clothes', price=499, cost=180)
    ns = compute('shopee-ph', sel='Women Clothes', price=499, cost=180, tg={'newSeller': True})
    ph = compute('shopee-ph', sel='Mobile Phones', price=12999, cost=10500)
    grp = {}
    for o in PH: grp.setdefault(o['g'], []).append(o)
    rows = ''
    for g, L in grp.items():
        mps = sorted({o['r']['mp'] for o in L}); malls = sorted({o['r']['mall'] for o in L})
        rng = lambda v: pct(v[0]) if len(v) == 1 else f'{pct(v[0])}–{pct(v[-1])}'
        rows += f"<tr><td>{E(g)}</td><td class='n'>{rng(mps)}</td><td class='n'>{rng(malls)}</td><td class='n'>{pct(L[0]['r']['sgsf'])}</td></tr>"
    toc = [('how', 'How Shopee Philippines fees work'), ('examples', 'Worked examples'), ('rates', 'Commission by category'),
           ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Shopee Philippines fees work</h2>
<p>Shopee PH publishes every seller fee as <b>VAT-inclusive</b> and rounds each fee to the nearest peso. The calculator does the same. These fees apply to a completed order:</p>
<h3>1. Commission fee</h3>
<p>Commission is a category rate applied to the item price after seller discounts. The Marketplace table has applied since 1 June 2025, with rates from 8.50% (mobile phones, cameras) to 10.50% (clothes, home &amp; living, sports). Mall uses a separate, more detailed table that has applied since 1 January 2025. New sellers pay no commission for their first 90 days.</p>
<h3>2. Transaction fee</h3>
<p>2.24% of the total amount the buyer pays, including shipping. If the buyer uses SPayLater instalments, an extra 3–6% applies. To model that, edit the transaction fee rate.</p>
<h3>3. Platform Shipping Fee</h3>
<p>5.6% of the item price after discounts for Marketplace sellers, or 4.48% for Mall, up to ₱100 per item. It applies to orders shipped with Shopee-supported logistics.</p>
<h3>4. Seller Growth Support Fee</h3>
<p>1.00% or 1.50% of the item price after discounts, depending on the category (list updated 22 October 2026). New sellers are exempt for their first 90 days. See how it compares with TikTok Shop’s growth fees in our <a href="../../guides/seller-growth-fee-tiktok-shopee-lazada/">growth fee comparison</a>.</p>
<h3>5. Order Processing Fee</h3>
<p>₱5 per completed order. You don’t pay it on your first 50 orders each month, or during a new seller’s first 90 days.</p>
<h3>6. Optional programmes</h3>
<p>If you join Mega Discount Voucher, it adds a 4% service fee, up to ₱200 per item, with 1% more on spike campaign days. Live Xtra (3.36%, up to ₱100) and pre-order (2%) have their own fees. Enter those under other costs or edit a rate.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: Shopee’s own sample computation (Mall, mobile phone)</h4>
<p>Price ₱400 with ₱30 in seller discounts, so the item price after discounts is ₱370. The buyer pays ₱420 including ₱50 shipping, and the seller has joined Mega Discount Voucher. Commission is 6.12%.</p>
{ex_table(_ex(off, 'PHP'))}
<p>The ₱50 shipping goes to the courier, so we enter it as shipping cost too. Net income: {PHP(off['profit'])}, matching Shopee’s published result of ₱297.</p></div>
<div class="example"><h4>Example 2: ₱499 dress, Marketplace</h4>
<p>Women Clothes at 10.50%, product cost ₱180, no shipping paid by the buyer.</p>
{ex_table(_ex(wc, 'PHP'))}
<p>Profit {PHP(wc['profit'])} ({wc['margin']:.1f}% margin). In the first 90 days the new-seller exemptions remove commission, Seller Growth Support Fee and Order Processing Fee, so fees drop to {PHP(ns['total'])}.</p></div>
<div class="example"><h4>Example 3: ₱12,999 phone, Marketplace</h4>
<p>At 8.50%, commission is {PHP(ph['fee']['commission'])}. The Platform Shipping Fee is capped at {PHP(ph['fee']['psf_ph'])}. Total fees: {PHP(ph['total'])}.</p></div>

<h2 id="rates">Commission by category</h2>
<p>VAT-inclusive rates from Shopee PH’s commission tables. Where a category’s subcategories have different rates, the table shows the range. The calculator has every subcategory.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Marketplace</th><th class="n">Mall</th><th class="n">Growth Support Fee</th></tr></thead><tbody>{rows}</tbody></table></div>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Plan for the end of the 90-day exemption.</b> When it ends, commission, the growth support fee and the order fee all start at once.</li>
<li><b>Check the ₱100 shipping-fee cap</b> on higher-priced items. Above about ₱1,786 (Marketplace) the cap applies.</li>
<li><b>Only add Mega Discount Voucher</b> if the extra orders outweigh the 4% fee.</li>
</ul>
'''
    faq = [
     ('Are Shopee Philippines fees VAT-inclusive?', 'Yes. Shopee PH publishes its commission, transaction, platform shipping and other fees as VAT-inclusive, and rounds each fee to the nearest peso.'),
     ('What is the Shopee PH transaction fee?', '2.24% of the total amount the buyer pays, including shipping. SPayLater instalment orders carry an extra 3–6%.'),
     ('What is the Platform Shipping Fee?', '5.6% of the item price after discounts for Marketplace sellers, or 4.48% for Mall, up to ₱100 per item, on orders shipped with Shopee-supported logistics.'),
     ('Do new sellers pay commission?', 'No. New sellers pay no commission, Seller Growth Support Fee or Order Processing Fee for their first 90 days. The transaction fee and Platform Shipping Fee still apply.'),
     ('When is the ₱5 Order Processing Fee waived?', 'On your first 50 orders each month, and during a new seller’s first 90 days.'),
    ]
    return dict(title='Shopee Philippines Fee Calculator 2026 (Commission, 2.24% TX, Shipping Fee)',
                desc='Free Shopee Philippines fee and profit calculator with VAT-inclusive Marketplace and Mall commission, 2.24% transaction fee, Platform Shipping Fee, Seller Growth Support Fee and ₱5 Order Processing Fee.',
                h1='Shopee Philippines Fee Calculator',
                lede='VAT-inclusive Marketplace and Mall commission, the 2.24% transaction fee, the Platform Shipping Fee capped at ₱100 per item, the Seller Growth Support Fee and the ₱5 order fee, each rounded to the peso as Shopee does.',
                body=body, faq=faq, toc=toc)

# ---------------------------------------------------------------- Shopee TH
TH_SAMPLE = ['Mobile Phones', 'Computers & Accessories › Laptops', 'Skincare › Facial Serum & Essence', 'Makeup › Lips',
             'Hair Care › Shampoo', 'Women Clothes › Dresses', 'Men Shoes › Sneakers', 'Women Bags › Tote Bags',
             'Watches › Women Watches', 'Home Appliances › Batteries', 'Motorcycles › Motorcycles']

def shopee_th_page():
    sk = 'Skincare › Facial Serum & Essence'
    a = compute('shopee-th', sel=sk, price=299, cost=90)
    s = compute('shopee-th', sel=sk, price=299, cost=90, x={'tier': 'small'})
    m = compute('shopee-th', sel=sk, store='mall', price=299, cost=90)
    p = compute('shopee-th', sel='Mobile Phones', price=8990, buyerShip=0, cost=7600)
    o = next(x for x in TH if x['n'] == sk)['r']
    rows = ''
    for n in TH_SAMPLE:
        r = next((x for x in TH if x['n'] == n), None)
        if not r: continue
        g, r = r['g'], r['r']
        rows += (f"<tr><td>{E(g + ' › ' + n)}</td><td class='n'>{pct(r['mp.std'])}</td><td class='n'>{pct(r['mp.small'])}</td>"
                 f"<td class='n'>{pct(r['mall.std'])}</td><td class='n'>{pct(r['mall.small'])}</td></tr>")
    toc = [('how', 'How Shopee Thailand fees work'), ('examples', 'Worked examples'), ('rates', 'Sample commission rates'),
           ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Shopee Thailand fees work</h2>
<p>Shopee Thailand’s fee policy covers three charges on a normal completed order. All rates below include 7% VAT.</p>
<h3>1. Sale transaction fee (commission)</h3>
<p>New category tables apply from <b>4 August 2026</b>, with separate tables for Non-Mall and Mall sellers. Each table lists more than 1,400 categories and four columns: standard, PRIME seller, small seller and small seller + PRIME. Shopee defines a small seller as one with sales of ฿10,000 or less in the previous 30 days. The rate is applied to the item price after seller discounts; shipping is not included. The calculator loads both full tables, so search for your category and choose your seller type.</p>
<h3>2. Payment transaction fee</h3>
<p>3% + VAT = 3.21% of the order amount, including shipping and any Shopee-funded discounts or coins. Instalment and some SPayLater payments cost more. To model those, edit the rate.</p>
<h3>3. Platform Infrastructure Fee</h3>
<p>฿1 + VAT = ฿1.07 per completed order.</p>
<h3>4. Programme service fees</h3>
<p>Programmes such as free-shipping or coins-cashback promotions have their own service fees. They are optional and vary by programme, so enter your total percentage in the field provided.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: ฿299 serum, Non-Mall, standard seller</h4>
<p>Facial Serum &amp; Essence at {pct(o['mp.std'])}, product cost ฿90, no shipping paid by the buyer.</p>
{ex_table(_ex(a, 'THB'))}
<p>Profit {THB(a['profit'])} ({a['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: the same serum as a small seller</h4>
<p>The small-seller column is {pct(o['mp.small'])}, so commission falls to {THB(s['fee']['commission'])} and profit rises to {THB(s['profit'])}.</p></div>
<div class="example"><h4>Example 3: the same serum in Shopee Mall</h4>
<p>The Mall rate is {pct(o['mall.std'])}: total fees {THB(m['total'])}, profit {THB(m['profit'])}.</p></div>
<div class="example"><h4>Example 4: ฿8,990 mobile phone</h4>
<p>Mobile phones pay {pct(next(x for x in TH if x['n'] == 'Mobile Phones')['r']['mp.std'])}. Fees: {THB(p['total'])}, profit {THB(p['profit'])} on a ฿7,600 cost.</p></div>

<h2 id="rates">Sample commission rates</h2>
<p>VAT-inclusive rates from the tables that apply from 4 August 2026. The calculator has all categories.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Non-Mall</th><th class="n">Non-Mall, small seller</th><th class="n">Mall</th><th class="n">Mall, small seller</th></tr></thead><tbody>{rows}</tbody></table></div>
'''
    faq = [
     ('When did the new Shopee Thailand commission start?', 'Shopee Thailand’s new Non-Mall and Mall sale transaction fee tables apply from 4 August 2026.'),
     ('Do Shopee Thailand fees include VAT?', 'Yes. The category rates include 7% VAT. The payment transaction fee is 3% + VAT (3.21%), and the Platform Infrastructure Fee is ฿1 + VAT (฿1.07) per order.'),
     ('What is a small seller?', 'Shopee’s fee tables give a lower rate to small sellers, defined as sellers with sales of ฿10,000 or less in the previous 30 days.'),
     ('Is commission charged on shipping?', 'No. Commission is charged on the item price after seller discounts. The 3.21% payment transaction fee does include shipping.'),
    ]
    return dict(title='Shopee Thailand Fee Calculator 2026 (Commission from 4 Aug, 3.21% Payment Fee)',
                desc='Free Shopee Thailand fee and profit calculator with Non-Mall and Mall commission for 1,400+ categories from 4 August 2026, small-seller rates, 3.21% payment fee and ฿1.07 per order.',
                h1='Shopee Thailand Fee Calculator',
                lede='Non-Mall and Mall commission for every category from 4 August 2026, small-seller and PRIME columns, the 3.21% payment transaction fee and ฿1.07 per order, all VAT-inclusive.',
                body=body, faq=faq, toc=toc)

# ---------------------------------------------------------------- guide
GUIDES_MORE = [
 dict(lang='en', slug='walmart-new-seller-savings-2026', short='Walmart New-Seller Savings 2026',
      title='Walmart New-Seller Savings 2026: 20–40% Off Referral Fees, Explained with Examples',
      desc='Who qualifies for Walmart Marketplace New-Seller Savings in 2026, how the 20%, 30% and 40% referral fee tiers and the $72,000 maximum work, the WFS discount, and worked examples.',
      market='walmart-us', cov='cov-ink', fig='Walmart'),
]

def g_walmart_nss():
    hk = 'Home, Kitchen, Decor & Garden'
    a = compute('walmart-us', sel=hk, price=24.99, cost=8)
    t = {k: compute('walmart-us', sel=hk, price=24.99, cost=8, x={'nss': k}) for k in ('t20', 't30', 't40')}
    w = compute('walmart-us', sel=hk, store='wfs', price=24.99, cost=8, wt=1.5, x={'nss': 't20'}, tg={'wfsCredit': True})
    trs = ''.join(f"<tr><td>{lab}</td><td class='n'>{USD(t[k]['total'])}</td><td class='n'>{USD(t[k]['profit'])}</td></tr>"
                  for k, lab in (('t20', '20% tier'), ('t30', '30% tier'), ('t40', '40% tier')))
    return f'''
<p>Walmart Marketplace’s <b>New-Seller Savings</b> programme for 2026 cuts referral fees for first-time sellers by 20%, 30% or 40%. This guide covers who qualifies, how the tiers work and what the discount is worth on a typical item. Every number links to the <a href="../../walmart/united-states/">Walmart Marketplace fee calculator</a>.</p>
<h2 id="who">Who qualifies</h2>
<ul>
<li>First-time Walmart Marketplace sellers who go live after 1 February 2026.</li>
<li>You opt in through the form in Seller Center. Sellers who joined between 1 February and 27 April 2026 do not need to enroll by clicking.</li>
<li>The programme runs from 2 February 2026 to 31 January 2027.</li>
</ul>
<h2 id="tiers">The three tiers</h2>
<p>The discount is a percentage off your referral fee. It grows with your GMV (gross merchandise value) since launch: <b>20%</b> for $0.01–$50,000, <b>30%</b> for $50,001–$500,000 and <b>40%</b> above $500,000. Discounts stop on 31 January 2027 or when the total reaches <b>$72,000</b>, whichever comes first.</p>
<h2 id="example">What it is worth on a $24.99 item</h2>
<p>A home item at a 15% referral fee, seller fulfilled, with an $8 product cost. Without the programme, fees are {USD(a['total'])} and profit is {USD(a['profit'])}.</p>
<div class="tablewrap"><table><thead><tr><th>Tier</th><th class="n">Fees</th><th class="n">Profit</th></tr></thead><tbody>{trs}</tbody></table></div>
<h2 id="wfs">The WFS discount</h2>
<p>Eligible sellers who use Walmart Fulfillment Services also get 10% of WFS fulfillment fees back, up to $2,000. On the same item fulfilled by WFS (1.5 lb, so 2 lb shipping weight), with the 20% tier and the WFS discount turned on, total fees are {USD(w['total'])} and profit is {USD(w['profit'])}.</p>
<h2 id="other">Other parts of the offer</h2>
<p>The offer also includes a rebate on sponsored-search ads and Walmart Connect advertising credits. Neither changes the fees on an order, so the calculator leaves them out. Check the official terms for the current amounts and conditions.</p>
'''

GUIDE_BODY_MORE = {'walmart-new-seller-savings-2026': g_walmart_nss}
GUIDE_SOURCES_MORE = {'walmart-new-seller-savings-2026': MARKETS['walmart-us']['sources'][2:4] + MARKETS['walmart-us']['sources'][:1]}
PAGE_FN_MORE = {('walmart-us', 'en'): walmart_us_page, ('shopee-ph', 'en'): shopee_ph_page, ('shopee-th', 'en'): shopee_th_page}
