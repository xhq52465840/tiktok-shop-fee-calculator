"""Written content. Every number is either taken from the rate files (src/data) or computed with markets.compute()."""
from markets import MARKETS, compute, idx
from site_helpers import money, pct, ex_table

MYO = MARKETS['tiktok-shop-my']['selector']['options']; PHO = MARKETS['tiktok-shop-ph']['selector']['options']
myr = lambda n: next(o for o in MYO if o['n'] == n)['r']
RM = lambda v: money(v, 'MYR'); PHP = lambda v: money(v, 'PHP'); USD = lambda v: money(v, 'USD'); GBP = lambda v: money(v, 'GBP')

GUIDES = [
 dict(lang='en', slug='tiktok-shop-malaysia-commission-changes-october-2026', short='Malaysia commission changes (31 Oct 2026)',
      title='TikTok Shop Malaysia Commission Changes on 31 October 2026, Explained',
      desc='What changes in TikTok Shop Malaysia commission on 31 Oct 2026: which categories go up or down, BXP vs non-BXP, worked examples in ringgit and how to reprice.',
      market='tiktok-shop-my'),
 dict(lang='en', slug='tiktok-shop-philippines-seller-growth-fee', short='Philippines Seller Growth Fee',
      title='TikTok Shop Philippines Seller Growth Fee: Rates, Categories and Real Examples',
      desc='The TikTok Shop PH Seller Growth Fee explained: 1% or 1.5% by category, how it stacks with the ₱5 processing fee, and what it costs on real orders.',
      market='tiktok-shop-ph'),
 dict(lang='en', slug='tiktok-shop-pricing-target-margin', short='Price for a target margin',
      title='How to Price Products on TikTok Shop to Hit a Target Margin',
      desc='A simple formula to set TikTok Shop prices that hit your target margin after commission, transaction and fixed per-order fees, with worked examples for MY, PH and the US.',
      market=None),
 dict(lang='en', slug='read-tiktok-shop-settlement-check-fees', short='Check your settlement',
      title='How to Read Your TikTok Shop Settlement and Check Every Fee Deduction',
      desc='Where to find order settlement details in TikTok Shop Seller Center, how each fee line is calculated, and how to spot deductions that don\'t add up.',
      market=None),
]

def ex_rows(f, cur, labels, extra_top=()):
    M = lambda v: money(v, cur)
    rows = list(extra_top)
    for k, r, a in f['rows']:
        rows.append((f"{labels[k]} ({pct(r)})" if k not in ('psf', 'opf', 'listing', 'epf') else labels[k], '−' + M(a)))
    rows.append(('Total fees', M(f['total']), True))
    rows.append(('Payout', M(f['payout']), True))
    return rows

LBL = dict(commission='Commission', tx='Transaction fee', bxp='BXP service fee', psf='Platform Support Fee', ssf='Shipping Service Fee',
           opf='Order Processing Fee', growth='Seller Growth Fee', referral='Referral fee', aff='Affiliate commission',
           listing='Listing fee', etx='Transaction fee', epp='Payment processing', epf='Payment processing (flat)')

# ======================================================================= MALAYSIA
def my_page():
    sk = 'Beauty & Personal Care › Skincare'; r = myr(sk)
    old = compute('tiktok-shop-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('tiktok-shop-my', sel=sk, period='new', price=39.90, cost=12)
    bxp = compute('tiktok-shop-my', sel=sk, period='new', tg={'bxp': True}, price=39.90, cost=12)
    bxpc = compute('tiktok-shop-my', sel=sk, period='new', tg={'bxp': True, 'campaign': True}, price=39.90, cost=12)
    g = compute('tiktok-shop-my', sel='Toys & Hobbies › Musical Instruments & Accessories', price=1000, sellerDisc=100)
    wt = "Womenswear & Underwear › Women's Tops"
    pl = compute('tiktok-shop-my', sel=wt, store='mall', tg={'paylater': True}, price=60, qty=2, sellerDisc=10, buyerShip=6, cost=22)
    rows_up = sorted(((o['r']['new.mp.non'] - o['r']['old.mp.non'], o) for o in MYO if o['r']['old.mp.non'] is not None), key=lambda x: -x[0])
    n_up = sum(1 for d, _ in rows_up if d > 0.001); n_dn = sum(1 for d, _ in rows_up if d < -0.001); n_eq = len(rows_up) - n_up - n_dn
    downs = [o for d, o in rows_up if d < -0.001]
    def rr(o, k): return pct(o['r'][k]) if o['r'][k] is not None else '–'
    sample = ['Beauty & Personal Care › Skincare', 'Beauty & Personal Care › Makeup', "Womenswear & Underwear › Women's Dresses", 'Muslim Fashion › Hijabs',
              'Phones & Electronics › Mobile Phone Accessories', 'Phones & Electronics › Phones & Tablets', 'Home Supplies › Home Decor', 'Food & Beverages › Snacks',
              'Food & Beverages › Fresh & Frozen Food', 'Health › Nutrition & Wellness', 'Baby & Maternity › Nursing & Feeding', 'Sports & Outdoor › Water Sports']
    def trow(n):
        o = next(x for x in MYO if x['n'] == n)
        return f"<tr><td>{n}</td><td class='n'>{rr(o,'old.mp.non')}</td><td class='n'><b>{rr(o,'new.mp.non')}</b></td><td class='n'>{rr(o,'old.mp.bxp')}</td><td class='n'><b>{rr(o,'new.mp.bxp')}</b></td><td class='n'><b>{rr(o,'new.mall.non')}</b></td></tr>"
    full = ''.join(f"<tr><td>{o['n']}</td>" + ''.join(f"<td class='n'>{rr(o,k)}</td>" for k in ['old.mp.bxp','old.mp.non','old.mall.bxp','old.mall.non','new.mp.bxp','new.mp.non','new.mall.bxp','new.mall.non']) + '</tr>' for o in MYO)
    toc = [('how', 'How TikTok Shop Malaysia fees work'), ('examples', 'Worked examples'), ('changes', 'What changed in 2026'), ('rates', 'Commission rates by category'), ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How TikTok Shop Malaysia fees work</h2>
<p>On an ordinary delivered order, TikTok Shop Malaysia deducts three fees from your settlement. If you are in the Bonus Extra Program (BXP), there is a fourth. Every rate TikTok publishes for Malaysia already includes 8% SST, so you don't add tax on top.</p>
<h3>1. Commission fee</h3>
<p>Commission depends on the product's sub-category, on whether you sell as a Marketplace or Mall seller, and on whether you joined BXP. It is charged on the item price minus your own (seller-funded) discount: <b>Commission = (item price − seller discount) × rate</b>. Shipping and TikTok's platform-funded discounts are not part of the base. From 31 October 2026 the rates range from 0% (fresh and frozen food, baking, dairy, staples) up to 20.52% (non-BXP Mall fragrance, makeup and similar beauty lines).</p>
<h3>2. Transaction fee</h3>
<p>The transaction fee is 3.78%. Since 15 February 2026 it has been charged on <b>original item price − seller discount + shipping paid by the buyer</b>, and platform discounts are no longer deducted from that base. From 00:00 on 16 October 2026, orders the buyer pays with TikTok PayLater are charged 4.86% instead. You don't choose the payment method, so for pricing it is safer to assume part of your orders will carry the higher rate.</p>
<h3>3. Platform Support Fee</h3>
<p>A flat RM0.50 plus SST, which is RM0.54, on every successfully delivered order regardless of order value or quantity. It started on 15 February 2026. It is not refunded if a delivered order is later returned. Because it is flat, it hurts small baskets most: it is 0.54% of a RM100 order but 2.7% of a RM20 order.</p>
<h3>4. BXP service fee (BXP sellers only)</h3>
<p>BXP sellers get lower commission rates and access to platform vouchers such as Bonus Cashback, Voucher Xtra, LIVE Specials and Limited-time Vouchers. In exchange they pay a BXP service fee of 4.86% on every completed order, whether or not the buyer used a BXP voucher. From 7 October 2026 the fee is 7.02% on campaign days (Double Day and Payday windows). It is capped at RM54 per item.</p>

<h2 id="examples">Worked examples</h2>
<p>All examples use the official rate tables and the same formulas as the calculator above.</p>
<div class="example"><h4>Example 1: a RM39.90 skincare serum, Marketplace, not in BXP</h4>
<p>Skincare commission for a non-BXP Marketplace seller goes from {pct(r['old.mp.non'])} to {pct(r['new.mp.non'])} on 31 October. Product cost RM12, no discount, free shipping funded by the platform.</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">Before 31 Oct</th><th class="n">From 31 Oct</th></tr></thead><tbody>
<tr><td>Commission</td><td class="n">−{RM(old['fee']['commission'])}</td><td class="n">−{RM(new['fee']['commission'])}</td></tr>
<tr><td>Transaction fee (3.78%)</td><td class="n">−{RM(old['fee']['tx'])}</td><td class="n">−{RM(new['fee']['tx'])}</td></tr>
<tr><td>Platform Support Fee</td><td class="n">−{RM(old['fee']['psf'])}</td><td class="n">−{RM(new['fee']['psf'])}</td></tr>
<tr><td><b>Payout</b></td><td class="n"><b>{RM(old['payout'])}</b></td><td class="n"><b>{RM(new['payout'])}</b></td></tr>
<tr><td><b>Profit after RM12 cost</b></td><td class="n"><b>{RM(old['profit'])}</b></td><td class="n"><b>{RM(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>The new table costs this seller {RM(old['profit'] - new['profit'])} per order, and margin drops from {old['margin']:.1f}% to {new['margin']:.1f}%.</p></div>
<div class="example"><h4>Example 2: the same serum as a BXP seller</h4>
<p>As a BXP seller the new skincare commission is {pct(r['new.mp.bxp'])}, but the BXP service fee is added.</p>
{ex_table(ex_rows(bxp, 'MYR', LBL))}
<p>Profit is {RM(bxp['profit'])} on a normal day ({bxp['margin']:.1f}% margin) and {RM(bxpc['profit'])} on a campaign day, when the BXP fee is 7.02%. Compared with {RM(new['profit'])} outside BXP, joining only pays off here if the vouchers bring in enough extra orders. Use the calculator's BXP switch to test your own numbers.</p></div>
<div class="example"><h4>Example 3: TikTok's own worked example</h4>
<p>TikTok's Seller University uses a RM1,000 guitar with a RM100 seller discount, sold by a non-BXP Marketplace seller at 12.96%. The calculator reproduces it exactly: commission {RM(g['fee']['commission'])}, transaction fee {RM(g['fee']['tx'])}, plus the Platform Support Fee. (TikTok's example shows that fee as RM0.50, before SST; the fee page sets it at RM0.54 including SST, which is what we use.)</p></div>
<div class="example"><h4>Example 4: a Mall order paid with PayLater</h4>
<p>Two women's tops at RM60 each, a RM10 shop voucher, RM6 shipping paid by the buyer, Mall seller outside BXP, paid with TikTok PayLater.</p>
{ex_table(ex_rows(pl, 'MYR', LBL, extra_top=[('Item subtotal after your discount', RM(pl['b']['net'])), ('Shipping paid by buyer', '+' + RM(6))]))}
<p>The transaction fee is charged on {RM(pl['b']['net_ship'])} (subtotal plus buyer-paid shipping) at 4.86%, while commission is charged only on {RM(pl['b']['net'])}.</p></div>

<h2 id="changes">What changed in 2026</h2>
<div class="tablewrap"><table><thead><tr><th>Effective</th><th>Change</th></tr></thead><tbody>
<tr><td>15 Feb 2026</td><td>New Platform Support Fee of RM0.54 per delivered order. Transaction fee base changes to item price − seller discount + buyer-paid shipping.</td></tr>
<tr><td>7 Oct 2026</td><td>BXP campaign-day fee rises from 4.86% to 7.02%. The non-campaign rate and the RM54 per-item cap are unchanged.</td></tr>
<tr><td>16 Oct 2026</td><td>Transaction fee for TikTok PayLater orders rises to 4.86%. Other payment methods stay at 3.78%.</td></tr>
<tr><td>31 Oct 2026</td><td>New Marketplace and Mall commission table. Orders placed before this date follow the old rates.</td></tr>
</tbody></table></div>
<p>For non-BXP Marketplace sellers, {n_up} of the {len(rows_up)} sub-categories with an earlier rate go up on 31 October, {n_dn} go down and {n_eq} stay the same. The decreases are concentrated in essentials: {", ".join(o["n"] for o in downs)}. The biggest increases are in water and winter sports (up {rows_up[0][0]:.2f} percentage points) and baby care &amp; health (up {next(d for d,o in rows_up if o["n"]=="Baby & Maternity › Baby Care & Health"):.2f} points). Read the full analysis in <a href="../../guides/tiktok-shop-malaysia-commission-changes-october-2026/">our guide to the 31 October changes</a>.</p>
<p>BXP campaign days for the rest of 2026, per TikTok: Double Day 8–11 November and 9–12 December; Payday 24–25 November and 20–21 December.</p>

<h2 id="rates">Commission rates by category</h2>
<p>A selection of popular sub-categories. MP = Marketplace. All rates include SST.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Sub-category</th><th class="n">MP non-BXP before</th><th class="n">MP non-BXP from 31 Oct</th><th class="n">MP BXP before</th><th class="n">MP BXP from 31 Oct</th><th class="n">Mall non-BXP from 31 Oct</th></tr></thead><tbody>{"".join(trow(n) for n in sample)}</tbody></table></div>
<details class="adv"><summary>Show all {len(MYO)} sub-categories</summary>
<p style="margin-top:12px"><input id="sf-filter" class="search" type="search" placeholder="Filter, e.g. skincare" aria-label="Filter categories"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates"><thead><tr><th>Category › Sub-category</th><th class="n">MP BXP (old)</th><th class="n">MP non-BXP (old)</th><th class="n">Mall BXP (old)</th><th class="n">Mall non-BXP (old)</th><th class="n">MP BXP (new)</th><th class="n">MP non-BXP (new)</th><th class="n">Mall BXP (new)</th><th class="n">Mall non-BXP (new)</th></tr></thead><tbody>{full}</tbody></table></div></details>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Reprice before 31 October.</b> The new table applies to orders placed from 00:00 on 31 October 2026. Check your top SKUs in the calculator with "Orders from 31 Oct 2026" selected and adjust prices or bundles before your next campaign.</li>
<li><b>Bundle low-priced items.</b> The RM0.54 Platform Support Fee is charged per order, not per item. Two items in one order pay it once.</li>
<li><b>Price for PayLater.</b> If a meaningful share of your buyers use PayLater, the extra 1.08 percentage points on those orders comes straight out of margin.</li>
<li><b>Run the BXP numbers per category.</b> In most categories BXP lowers commission by 2.17 to 2.70 points but adds a 4.86% fee, so you pay more per order and need the vouchers to lift sales. Baby Care &amp; Health is the exception: BXP commission is 7.78% against 13.82% outside BXP, so BXP is cheaper even before any extra sales.</li>
<li><b>Fund discounts carefully.</b> Seller-funded discounts lower the base for commission and transaction fees, but every ringgit of discount still comes out of your payout. Platform-funded vouchers cost you nothing and don't change your fees.</li>
<li><b>Include affiliate commission.</b> Creator commission is charged on top of TikTok's fees. Enter your rate in the calculator so the margin you see is the margin you get.</li>
</ul>
<p>For a step-by-step pricing method, see <a href="../../guides/tiktok-shop-pricing-target-margin/">how to price for a target margin</a>.</p>
'''
    faq = [
     ("What are TikTok Shop Malaysia's seller fees in 2026?", "A commission fee by product category (different for Marketplace and Mall, and lower if you join BXP), a 3.78% transaction fee (4.86% on TikTok PayLater orders from 16 October 2026) and a flat RM0.54 Platform Support Fee per delivered order. BXP sellers also pay a 4.86% BXP service fee, or 7.02% on campaign days. All rates include 8% SST."),
     ("When do the new commission rates start?", "At 00:00 on 31 October 2026, Malaysia time. Orders placed before then are charged the old rates."),
     ("How is commission calculated?", "Commission = (item price − seller discount) × the category rate. Shipping and platform-funded discounts are not included."),
     ("Is the transaction fee charged on shipping?", "Yes. Since 15 February 2026 it is charged on the original item price minus your discount plus the shipping fee the buyer paid."),
     ("Is the RM0.54 Platform Support Fee refunded on returns?", "Only if the order was never delivered. Once an order is delivered, the fee is not refunded even if the buyer later returns it."),
     ("Is BXP worth it after 31 October?", "It depends on the category and on how many extra orders the vouchers bring. In most categories BXP saves 2.17 to 2.70 commission points but costs 4.86% (7.02% on campaign days), so total fees per order are higher. Compare both in the calculator."),
     ("Do the rates include SST?", "Yes. TikTok publishes commission, transaction, BXP and Platform Support Fee rates inclusive of 8% SST."),
    ]
    return dict(
     title='TikTok Shop Fee Calculator Malaysia 2026 (New 31 Oct Commission Rates)',
     desc='Free TikTok Shop Malaysia fee and profit calculator with the new commission table from 31 October 2026, 3.78%/4.86% transaction fee, RM0.54 Platform Support Fee and BXP.',
     h1='TikTok Shop Fee Calculator Malaysia',
     lede='See exactly what TikTok Shop Malaysia deducts from each order and what you keep, using the official commission table for orders from 31 October 2026.',
     body=body, faq=faq, toc=toc)

# ======================================================================= PHILIPPINES
def ph_page():
    top = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=499, cost=180)
    top_old = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=499, cost=180, rates={'opf': 3, 'growth': 0})
    ph = compute('tiktok-shop-ph', sel='Phones & Electronics › Phones & Tablets', store='mall', price=8000, cost=6900)
    cheap = compute('tiktok-shop-ph', sel='Kitchenware', price=149, cost=60)
    shoes = compute('tiktok-shop-ph', sel='Shoes', store='mall', price=1900, sellerDisc=120)
    toc = [('how', 'How TikTok Shop Philippines fees work'), ('examples', 'Worked examples'), ('changes', 'What changed in 2026'), ('rates', 'Commission and growth fee by category'), ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    rows = ''.join(f"<tr><td>{o['g']}</td><td>{o['n']}</td><td class='n'>{pct(o['r']['mp'])}</td><td class='n'>{pct(o['r']['mall'])}</td><td class='n'>{pct(o['r']['growth'])}{'*' if o['note'] else ''}</td></tr>" for o in PHO)
    body = f'''
<h2 id="how">How TikTok Shop Philippines fees work</h2>
<p>TikTok Shop Philippines deducts five fees from each successfully delivered order. Every rate below is VAT inclusive, as TikTok publishes it.</p>
<h3>1. Commission fee</h3>
<p>Charged on <b>item price − seller discount</b> at a rate set by product category. Since 15 January 2025 Marketplace and Mall sellers have different rates: Marketplace ranges from 5% to 7.3%, Mall from 5% to 9.1%. New sellers pay 0% commission for their first 90 days. If TikTok hasn't assigned a rate to a new category yet, the default is 6.7% for Marketplace and 7.7% for Mall.</p>
<h3>2. Transaction fee</h3>
<p>2.24% on every successful order. The calculator applies it to the item subtotal after your discount plus the shipping fee paid by the buyer, the base TikTok introduced in July 2026. You can edit the rate under "Fee rates used" if your settlement shows otherwise.</p>
<h3>3. Shipping Service Fee</h3>
<p>Charged on delivered orders to fund platform-wide free shipping incentives and visibility boosts: 5.5% for Marketplace sellers and 5% for Mall sellers, on item price − seller discount, capped at ₱100 per item.</p>
<h3>4. Order Processing Fee</h3>
<p>A fixed ₱5 (tax inclusive) per successfully delivered order, whatever the order value or number of items. TikTok charged a discounted ₱3 from 1 December 2025 and ended the discount at 00:00 on 1 September 2026. It is not refunded if a delivered order is later returned. New sellers (first product listed within the last 90 days) are exempt for the following month, and existing sellers' first 50 orders each month are exempt.</p>
<h3>5. Seller Growth Fee</h3>
<p>A per-order fee that funds platform-wide growth incentives, including making the Bonus Cashback Program free for eligible sellers. It is 1% for Electronics, Grocery and Large Appliances, and 1.5% for Beauty &amp; Personal Care, Fashion, Mom &amp; Baby, Health and Lifestyle (except Large Appliances). Seller reports date it from 27 April 2026. Read more in our <a href="../../guides/tiktok-shop-philippines-seller-growth-fee/">Seller Growth Fee guide</a>.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: a ₱499 women's top, Marketplace</h4>
<p>Womenswear commission is {pct(top['rate']['commission'])} for Marketplace sellers and the growth fee is 1.5%. Product cost ₱180.</p>
{ex_table(ex_rows(top, 'PHP', LBL))}
<p>TikTok keeps {PHP(top['total'])}, or {top['total']/499*100:.1f}% of the price. Profit is {PHP(top['profit'])} ({top['margin']:.1f}% margin). In January–April 2026, with the ₱3 processing fee and no growth fee, the same order would have left {PHP(top_old['profit'])}.</p></div>
<div class="example"><h4>Example 2: an ₱8,000 phone, Mall seller</h4>
<p>Phones &amp; Tablets commission is {pct(ph['rate']['commission'])} for Mall, and electronics pay a 1% growth fee. The Shipping Service Fee would be 5% × ₱8,000 = ₱400, but the cap limits it to ₱100.</p>
{ex_table(ex_rows(ph, 'PHP', LBL))}
<p>On high-value items the ₱100 cap matters a lot: the effective fee rate here is {ph['total']/8000*100:.2f}% instead of {(6+2.24+5+1):.2f}% uncapped.</p></div>
<div class="example"><h4>Example 3: a ₱149 kitchen gadget</h4>
<p>Low prices feel the flat ₱5 fee most. Kitchenware is {pct(cheap['rate']['commission'])} for Marketplace.</p>
{ex_table(ex_rows(cheap, 'PHP', LBL))}
<p>The ₱5 Order Processing Fee alone is {5/149*100:.2f}% of the price. Total fees are {cheap['total']/149*100:.1f}% of the sale, against {top['total']/499*100:.1f}% on the ₱499 top.</p></div>
<div class="example"><h4>Example 4: TikTok's own commission example</h4>
<p>TikTok's Seller University uses grey shoes at ₱1,900 with a ₱120 seller discount, at the 7.9% Mall rate for shoes. The calculator gives the same commission: {PHP(shoes['fee']['commission'])}.</p></div>

<h2 id="changes">What changed in 2026</h2>
<div class="tablewrap"><table><thead><tr><th>Effective</th><th>Change</th></tr></thead><tbody>
<tr><td>27 Apr 2026 (reported)</td><td>Seller Growth Fee of 1% or 1.5% per order introduced; Bonus Cashback becomes free for eligible sellers.</td></tr>
<tr><td>1 Sep 2026</td><td>Order Processing Fee discount ends: ₱3 → ₱5 per delivered order. Exemptions for new sellers and the first 50 orders a month remain.</td></tr>
<tr><td>Unchanged</td><td>Commission (15 January 2025 table), 2.24% transaction fee, 5.5%/5% Shipping Service Fee capped at ₱100 per item.</td></tr>
</tbody></table></div>

<h2 id="rates">Commission and growth fee by category</h2>
<p><input id="sf-filter" class="search" type="search" placeholder="Filter, e.g. shoes" aria-label="Filter categories"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates"><thead><tr><th>Cluster</th><th>Category</th><th class="n">Marketplace</th><th class="n">Mall</th><th class="n">Growth fee</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted">* Kids' Fashion and Pet Supplies are not named in TikTok's Seller Growth Fee list; 1.5% is assumed. The growth fee base (item price − seller discount) is our assumption, because TikTok's overview page gives the rate but not the base.</p>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Raise the floor price, not every price.</b> On items under about ₱200 the fixed ₱5 fee is several percent of the sale. Bundles and minimum-spend vouchers spread it across more value.</li>
<li><b>Use your 50 exempt orders.</b> Existing sellers don't pay the Order Processing Fee on their first 50 orders each month. Count them in your monthly average, not per order.</li>
<li><b>Mind the ₱100 cap.</b> The Shipping Service Fee stops at ₱100 per item, so high-value items carry a lower fee rate than cheap ones.</li>
<li><b>Mall vs Marketplace.</b> Mall commission is higher in most categories but the Shipping Service Fee is 0.5 points lower. Compare both with the store type switch.</li>
<li><b>Price for the growth fee.</b> Fashion, beauty, health and lifestyle pay 1.5%. That is ₱7.49 on a ₱499 item, every order.</li>
</ul>
<p>See also: <a href="../../guides/tiktok-shop-pricing-target-margin/">pricing for a target margin</a> and <a href="../../guides/read-tiktok-shop-settlement-check-fees/">checking your settlement</a>.</p>
'''
    faq = [
     ("What are TikTok Shop Philippines seller fees in 2026?", "Commission by category (Marketplace 5%–7.3%, Mall 5%–9.1%), a 2.24% transaction fee, a Shipping Service Fee of 5.5% (Marketplace) or 5% (Mall) capped at ₱100 per item, a ₱5 Order Processing Fee per delivered order and a Seller Growth Fee of 1% or 1.5%. All VAT inclusive."),
     ("Is the order processing fee ₱3 or ₱5?", "₱5 since 00:00 on 1 September 2026. It was ₱3 from 1 December 2025 to 31 August 2026."),
     ("Who doesn't pay the ₱5 fee?", "New sellers whose first product was listed within the last 90 days are exempt for the following month. Existing sellers' first 50 orders each month are exempt."),
     ("What is the Seller Growth Fee?", "A 1% (Electronics, Grocery, Large Appliances) or 1.5% (Beauty & Personal Care, Fashion, Mom & Baby, Health, Lifestyle) fee per successful order that funds platform growth incentives, including free Bonus Cashback for eligible sellers."),
     ("Do new sellers pay commission?", "No. New sellers get 0% commission for 90 days. The other fees still apply."),
     ("Are these fees VAT inclusive?", "Yes. TikTok publishes all Philippine seller fee rates inclusive of VAT."),
    ]
    return dict(
     title='TikTok Shop Philippines Seller Fee Calculator 2026 (₱5 Fee + Growth Fee)',
     desc='Free TikTok Shop Philippines fee and profit calculator with the ₱5 Order Processing Fee, 1%–1.5% Seller Growth Fee, 2.24% transaction fee and Shipping Service Fee.',
     h1='TikTok Shop Seller Fee Calculator Philippines',
     lede='Every fee TikTok Shop PH deducts from an order, including the ₱5 Order Processing Fee and the Seller Growth Fee that many calculators still leave out.',
     body=body, faq=faq, toc=toc)

# ======================================================================= UNITED STATES
def us_page():
    UO = MARKETS['tiktok-shop-us']['selector']['options']
    tee = compute('tiktok-shop-us', price=24.99, buyerShip=4.99, cost=7, shipCost=4.5)
    aff = compute('tiktok-shop-us', price=24.99, buyerShip=4.99, cost=7, shipCost=4.5, affPct=15)
    card = compute('tiktok-shop-us', sel='Collectibles › Trading Cards & Accessories', price=12000)
    gold = compute('tiktok-shop-us', sel='Jewelry Accessories & Derivatives › Gold', price=450, cost=260)
    five = [o['n'] for o in UO if o['r']['rate'] == 5]
    groups = {}
    for o in UO: groups.setdefault(o['g'], set()).add(o['r']['rate'])
    grow = ''.join(f"<tr><td>{g}</td><td class='n'>{' / '.join(pct(x) for x in sorted(v))}</td><td>{'3% on the portion of a sale over $10,000' if any('over' in o['r'] for o in UO if o['g']==g) else ''}</td></tr>" for g, v in groups.items())
    toc = [('how', 'How the referral fee works'), ('examples', 'Worked examples'), ('rates', 'Rates by category'), ('tips', 'Pricing tips'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How the TikTok Shop US referral fee works</h2>
<p>In the United States TikTok Shop charges one main platform fee, the <b>referral fee</b>. TikTok's formula is <b>referral fee = rate × (customer payment + platform discount − tax)</b>. In practice that is the item price after your own discount plus the shipping the customer paid. Platform-funded discounts are added back, so they don't lower your fee, and sales tax is excluded.</p>
<p>The rate is 6% for almost every category. Five fine-jewelry sub-categories (Diamond, Gold, Jade, Platinum/Carat Gold, and Ruby, Sapphire &amp; Emerald) have been 5% since 31 October 2024, and every Pre-Owned sub-category is 5%. Collectibles and Pre-Owned sales pay only 3% on the part of a sale above $10,000.</p>
<p>The referral fee is not the whole picture. If you sell through creators, the affiliate commission you set is charged on top, and it is often larger than TikTok's own fee. Add it in the calculator.</p>
<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: a $24.99 T-shirt with $4.99 buyer-paid shipping</h4>
<p>The referral fee is charged on {USD(tee['b']['net_ship'])}, including the shipping the buyer paid. Product cost $7, label cost $4.50.</p>
{ex_table(ex_rows(tee, 'USD', LBL))}
<p>Profit is {USD(tee['profit'])} ({tee['margin']:.1f}% of the item price). With a 15% creator commission it falls to {USD(aff['profit'])}.</p></div>
<div class="example"><h4>Example 2: a $12,000 trading card</h4>
<p>Collectibles pay 6% on the first $10,000 and 3% on the rest: 6% × $10,000 + 3% × $2,000 = {USD(card['total'])}, an effective {card['total']/12000*100:.2f}%.</p></div>
<div class="example"><h4>Example 3: a $450 gold necklace</h4>
<p>Gold jewelry is one of the 5% sub-categories, so the referral fee is {USD(gold['total'])} rather than $27.00 at 6%.</p></div>
<h2 id="rates">Referral fee rates by category</h2>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Rate</th><th>Notes</th></tr></thead><tbody>{grow}</tbody></table></div>
<p class="muted">5% sub-categories: {", ".join(five)}.</p>
<h2 id="tips">Pricing tips</h2>
<ul><li><b>Charge shipping knowingly.</b> Buyer-paid shipping is part of the referral fee base, so a $5 shipping charge costs you $0.30 in fees.</li>
<li><b>Budget for creators.</b> Affiliate commission usually outweighs the 6% referral fee. Set a commission you can afford at your target margin.</li>
<li><b>Check your category.</b> Jewelry in the five fine-jewelry sub-categories pays 5%; other jewelry pays 6%. Make sure listings are categorized correctly.</li></ul>
<p>Read <a href="../../guides/tiktok-shop-pricing-target-margin/">how to price for a target margin</a>.</p>
'''
    faq = [("What is the TikTok Shop US referral fee in 2026?", "6% for most categories; 5% for five fine-jewelry sub-categories and all Pre-Owned categories. Collectibles and Pre-Owned pay 3% on the portion of a sale over $10,000."),
           ("Is the referral fee charged on shipping?", "Yes. The base includes the shipping fee paid by the customer. Sales tax is excluded."),
           ("Do platform discounts reduce the fee?", "No. TikTok adds platform discounts back into the base, so the fee is calculated as if the buyer paid the full price."),
           ("Is affiliate commission included?", "No. Creator commission is set by you and charged separately. Enter it in the calculator to see your real margin.")]
    return dict(title='TikTok Shop US Fee Calculator 2026: Referral Fee & Profit', desc='Free TikTok Shop US fee calculator: 6% referral fee (5% fine jewelry and Pre-Owned), shipping in the base, the $10K tier for collectibles, plus affiliate commission and profit.',
                h1='TikTok Shop Fee Calculator United States', lede='Work out the TikTok Shop US referral fee, your payout and your profit, using the official category rates.', body=body, faq=faq, toc=toc)

# ======================================================================= UNITED KINGDOM
def uk_page():
    dress = compute('tiktok-shop-uk', price=22, buyerShip=3.49, cost=7, shipCost=3.2)
    elec = compute('tiktok-shop-uk', sel=1, price=60, cost=30)
    toc = [('how', 'How the commission works'), ('examples', 'Worked examples'), ('tips', 'Pricing tips'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How TikTok Shop UK commission works</h2>
<p>TikTok Shop UK charges a commission on every sale. The standard rate is <b>9%</b>, including VAT, before any reductions. TikTok's formula is <b>commission = ((net sales + customer-paid shipping + platform discount) − (net sales refund + platform discount refund)) × rate</b>. So shipping the buyer pays is included, platform discounts are added back, and refunds are taken off.</p>
<p>Products in specified Electronics and Beauty &amp; Personal Care categories automatically get a 4-point category-level reduction, an effective <b>5%</b>. TikTok can also offer reductions through Seller Centre missions. Only one reduction applies to a product at a time; they don't stack.</p>
<p>If an order is fully returned, the full commission is refunded. If part of an order is refunded, only the commission on the refunded items comes back.</p>
<div class="callout warn"><p>Which sub-categories qualify for 5% is listed in TikTok's "Commission Rate by Product Categories" document linked from the policy. Check that your product is categorised correctly: if TikTok re-categorises it during listing review, the reduced rate no longer applies.</p></div>
<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: a £22 dress with £3.49 buyer-paid shipping</h4>
{ex_table(ex_rows(dress, 'GBP', LBL))}
<p>Commission is charged on {GBP(dress['b']['net_ship'])}. After a £7 product cost and £3.20 postage, profit is {GBP(dress['profit'])}.</p></div>
<div class="example"><h4>Example 2: a £60 item in an eligible electronics category</h4>
<p>At the reduced 5% rate, commission is {GBP(elec['total'])} instead of £5.40 at 9%.</p></div>
<h2 id="tips">Pricing tips</h2>
<ul><li><b>Shipping is in the base.</b> A £3.49 postage charge adds about £0.31 in commission at 9%.</li>
<li><b>Look for missions.</b> TikTok offers commission reductions through Seller Centre missions, especially for new sellers. They don't stack with category reductions.</li>
<li><b>Add creator commission.</b> Affiliate commission is on top of TikTok's 9%.</li></ul>
'''
    faq = [("What is TikTok Shop UK's commission rate?", "9% including VAT for most categories. Specified Electronics and Beauty & Personal Care categories get an effective 5%."),
           ("Is commission charged on postage?", "Yes. Customer-paid shipping is part of the commission base."),
           ("Can reductions stack?", "No. Only one commission reduction applies to a product at a time."),
           ("Is commission refunded on returns?", "Yes. A full return refunds the full commission; a partial refund returns the commission on the refunded items.")]
    return dict(title='TikTok Shop UK Fee Calculator 2026: 9% Commission & Profit', desc='Free TikTok Shop UK commission and profit calculator: 9% standard rate, 5% for eligible electronics and beauty, postage in the base, plus affiliate commission.',
                h1='TikTok Shop Fee Calculator United Kingdom', lede='Estimate TikTok Shop UK commission and what you keep per order, based on the official commission policy.', body=body, faq=faq, toc=toc)

# ======================================================================= ETSY
def etsy_page():
    ET = MARKETS['etsy']['selector']['options']
    us = compute('etsy', price=30, buyerShip=5, tax=2.4, cost=9, shipCost=4.8)
    uk = compute('etsy', sel='United Kingdom', price=25, buyerShip=4, cost=8, shipCost=3.6, rates={'listing': 0})
    my = compute('etsy', sel='Malaysia', price=80, buyerShip=25, cost=25, shipCost=22, rates={'listing': 0})
    rows = ''.join(f"<tr><td>{o['n']}</td><td class='n'>{pct(o['r']['pp'])} + {o['r']['pf']:g} {o['cur']}</td></tr>" for o in ET)
    toc = [('how', 'How Etsy fees work'), ('examples', 'Worked examples'), ('rates', 'Processing fees by country'), ('tips', 'Pricing tips'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Etsy fees work</h2>
<p>Most Etsy sales carry three fees:</p>
<ul><li><b>Listing fee:</b> US$0.20 per listing when you publish it. If a listing auto-renews after a sale, or a buyer purchases more than one item from a listing, another US$0.20 is charged for each additional item. The calculator charges US$0.20 per item sold.</li>
<li><b>Transaction fee:</b> 6.5% of the item price plus the shipping and gift wrap you charge. If you sell from the US, it doesn't apply to sales tax. Outside the US it applies to the listing price, which should include any taxes you are responsible for.</li>
<li><b>Payment processing fee:</b> a percentage plus a flat amount per order, set by the country of your bank account, charged on the total sale including shipping and any applicable sales tax. For example 3% + $0.25 in the United States, 4% + £0.20 in the UK and 4.5% + RM2 in Malaysia.</li></ul>
<p>Etsy Ads, Offsite Ads and shipping labels bought on Etsy are extra and depend on how you use them. Add them under "Other costs".</p>
<div class="callout"><p><b>Selling from the UK?</b> UK shops also pay Etsy's 0.48% regulatory operating fee and, without a VAT number, 20% VAT on Etsy's fees. The <a href="/en/etsy/uk/">Etsy UK fee calculator</a> includes both, in pounds.</p></div>
<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: a US seller, $30 item, $5 shipping, $2.40 sales tax</h4>
{ex_table(ex_rows(us, 'USD', LBL))}
<p>The transaction fee is on {USD(us['b']['net_ship'])}; payment processing is on {USD(us['b']['gross'])} including tax, plus $0.25. Etsy keeps {USD(us['total'])}. After a $9 cost and a $4.80 label, profit is {USD(us['profit'])}.</p></div>
<div class="example"><h4>Example 2: a UK seller, £25 item, £4 postage</h4>
<p>Transaction fee {GBP(uk['fee']['etx'])} and payment processing {GBP(uk['fee']['epp'] + uk['fee']['epf'])} (4% + £0.20), {GBP(uk['total'])} in total, plus the US$0.20 listing fee charged in US dollars.</p></div>
<div class="example"><h4>Example 3: a Malaysian seller, RM80 item, RM25 shipping</h4>
<p>Transaction fee {RM(my['fee']['etx'])} and payment processing {RM(my['fee']['epp'] + my['fee']['epf'])} (4.5% + RM2), {RM(my['total'])} before the US$0.20 listing fee.</p></div>
<h2 id="rates">Payment processing fees by bank-account location</h2>
<p><input id="sf-filter" class="search" type="search" placeholder="Filter countries" aria-label="Filter countries"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates"><thead><tr><th>Bank account location</th><th class="n">Fee (% of total + flat per order)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted">Etsy Payments processing fees are subject to VAT in some locations; VAT appears on your Etsy VAT invoice.</p>
<h2 id="tips">Pricing tips</h2>
<ul><li><b>Shipping is taxed by fees too.</b> Both the 6.5% transaction fee and processing apply to shipping you charge.</li>
<li><b>Small orders pay more.</b> The flat processing fee and the listing fee weigh more on cheap items. Consider bundles or a higher minimum price.</li>
<li><b>Refunds return part of the processing fee.</b> Etsy credits the processing fee proportionally to the refunded amount.</li></ul>
'''
    faq = [("What are Etsy's fees in 2026?", "A US$0.20 listing fee, a 6.5% transaction fee on item price plus shipping and gift wrap, and a payment processing fee that depends on your bank country, such as 3% + $0.25 in the US."),
           ("Is the transaction fee charged on shipping?", "Yes. It applies to the item price plus the shipping and gift wrap you charge."),
           ("Is payment processing charged on sales tax?", "Yes. It is charged on the total sale price including shipping and any applicable sales tax."),
           ("Are fees refunded if I refund a buyer?", "Etsy credits the payment processing fee proportionally to the refund amount.")]
    return dict(title='Etsy Fee Calculator 2026: Listing, Transaction & Processing Fees by Country', desc='Free Etsy fee and profit calculator with the 6.5% transaction fee, US$0.20 listing fee and official payment processing fees for 60+ bank-account countries.',
                h1='Etsy Fee Calculator', lede='See Etsy\'s listing, transaction and payment processing fees for your country and what you keep from each sale.', body=body, faq=faq, toc=toc)

# ======================================================================= GUIDES
def g_my():
    ch = []
    for o in MYO:
        if o['r']['old.mp.non'] is None: continue
        ch.append((round(o['r']['new.mp.non'] - o['r']['old.mp.non'], 2), o))
    ch.sort(key=lambda x: -x[0])
    up = [c for c in ch if c[0] > 0]; dn = [c for c in ch if c[0] < 0]; eq = [c for c in ch if c[0] == 0]
    from collections import Counter
    cnt = Counter(c[0] for c in up)
    common = cnt.most_common(3)
    zero = [o['n'] for o in MYO if o['r']['new.mp.non'] == 0]
    t = lambda lst: ''.join(f"<tr><td>{o['n']}</td><td class='n'>{pct(o['r']['old.mp.non'])}</td><td class='n'><b>{pct(o['r']['new.mp.non'])}</b></td><td class='n'>{d:+.2f}</td><td class='n'>{pct(o['r']['old.mp.bxp'])} → {pct(o['r']['new.mp.bxp'])}</td></tr>" for d, o in lst)
    hj = compute('tiktok-shop-my', sel='Muslim Fashion › Hijabs', period='old', price=35, cost=11)
    hj2 = compute('tiktok-shop-my', sel='Muslim Fashion › Hijabs', period='new', price=35, cost=11)
    ph1 = compute('tiktok-shop-my', sel='Phones & Electronics › Mobile Phone Accessories', period='old', price=29.90, cost=8)
    ph2 = compute('tiktok-shop-my', sel='Phones & Electronics › Mobile Phone Accessories', period='new', price=29.90, cost=8)
    nf1 = compute('tiktok-shop-my', sel='Baby & Maternity › Nursing & Feeding', period='old', price=89, cost=40)
    nf2 = compute('tiktok-shop-my', sel='Baby & Maternity › Nursing & Feeding', period='new', price=89, cost=40)
    def keep_price(f_new, target_profit, sk):
        p = 1.0
        while compute('tiktok-shop-my', sel=sk, period='new', price=p, cost=11)['profit'] < target_profit: p = round(p + 0.1, 2)
        return p
    hp = keep_price(hj2, hj['profit'], 'Muslim Fashion › Hijabs')
    body = f'''
<p>TikTok Shop Malaysia published a new commission table on 16 October 2026. It applies to orders placed from <b>00:00 on 31 October 2026, Malaysia time (UTC+8)</b>. Orders placed before that follow the current rates. Nothing else changes on that date: the 3.78% transaction fee, the RM0.54 Platform Support Fee and the BXP service fee stay as they are, and TikTok says there are no new flat, listing or monthly charges.</p>
<h2 id="summary">The change in numbers</h2>
<p>Looking at non-BXP Marketplace rates across the {len(ch)} sub-categories that had a rate before:</p>
<ul><li><b>{len(up)} go up.</b> The most common increases are {", ".join(f"+{d:.2f} points ({n} sub-categories)" for d, n in common)}.</li>
<li><b>{len(dn)} go down</b>, all in essentials and vouchers.</li>
<li><b>{len(eq)} stay the same</b>, including the Pre-Owned fashion lines and the {len(zero)} categories at 0%: {", ".join(zero)}.</li>
<li>One new category, Beer, Wine &amp; Spirits, gets a rate for the first time ({pct(myr("Food & Beverages › Beer, Wine & Spirits")["new.mp.non"])} for non-BXP Marketplace).</li></ul>
<p>The highest rate in the new table is 20.52% (non-BXP Mall fragrance, makeup, men's care, nail care and hand &amp; foot care), up from 18.90%.</p>
<h2 id="up">Biggest increases</h2>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Sub-category</th><th class="n">MP non-BXP before</th><th class="n">From 31 Oct</th><th class="n">Change (pts)</th><th class="n">MP BXP</th></tr></thead><tbody>{t(up[:10])}</tbody></table></div>
<h2 id="down">Categories that get cheaper</h2>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Sub-category</th><th class="n">MP non-BXP before</th><th class="n">From 31 Oct</th><th class="n">Change (pts)</th><th class="n">MP BXP</th></tr></thead><tbody>{t(dn)}</tbody></table></div>
<p>TikTok describes these as "essential categories protected": selected daily necessities whose rates are reduced or held.</p>
<h2 id="bxp">BXP vs non-BXP after the change</h2>
<p>BXP sellers still pay lower commission, but in most categories the gap narrows. Before 31 October a BXP seller paid 4.32 points less than a non-BXP seller in almost every category. From 31 October the gap is 2.70 points in most categories and 2.17 points in most clothing and bag categories. Since BXP sellers also pay the 4.86% BXP fee (7.02% on campaign days), being in BXP now costs more per order in most categories than before. The exception is Baby Care &amp; Health, where BXP commission falls to 7.78% while the non-BXP rate rises to 13.82%.</p>
<h2 id="examples">What it means per order</h2>
<div class="example"><h4>RM35 hijab, non-BXP Marketplace, cost RM11</h4>
<p>Commission goes from {pct(hj['rate']['commission'])} to {pct(hj2['rate']['commission'])}. Payout falls from {RM(hj['payout'])} to {RM(hj2['payout'])}, profit from {RM(hj['profit'])} to {RM(hj2['profit'])}. To keep the old profit you would need to charge about {RM(hp)}.</p></div>
<div class="example"><h4>RM29.90 phone case, non-BXP Marketplace, cost RM8</h4>
<p>Mobile phone accessories go from {pct(ph1['rate']['commission'])} to {pct(ph2['rate']['commission'])}. Profit per order goes from {RM(ph1['profit'])} to {RM(ph2['profit'])}.</p></div>
<div class="example"><h4>RM89 breast pump accessory set (Nursing &amp; Feeding), cost RM40</h4>
<p>One of the categories that gets cheaper: {pct(nf1['rate']['commission'])} → {pct(nf2['rate']['commission'])}. Profit rises from {RM(nf1['profit'])} to {RM(nf2['profit'])}.</p></div>
<h2 id="todo">What to do before 31 October</h2>
<ol><li>List your top 20 SKUs by revenue and check each one's sub-category in the <a href="../../tiktok-shop/malaysia/">Malaysia calculator</a>, with "Orders from 31 Oct 2026" selected.</li>
<li>Decide per SKU whether to absorb the increase, raise the price or bundle. For low-priced items, bundling also spreads the RM0.54 Platform Support Fee.</li>
<li>If you are in BXP, compare your fees with BXP switched on and off. Remember the campaign-day rate of 7.02% on Double Day 8–11 November and Payday 24–25 November.</li>
<li>After 31 October, check your first settlements against the new rates. Our <a href="../read-tiktok-shop-settlement-check-fees/">settlement guide</a> shows where to look.</li></ol>
'''
    return body

def g_ph():
    ex = [('Fashion', 'Womenswear & Underwear', 299), ('Beauty', 'Beauty & Personal Care', 399), ('Electronics', 'Phones & Electronics › Phone Accessories', 249), ('Grocery', 'Food & Beverages', 180)]
    rows = ''
    for lab, cat, p in ex:
        f = compute('tiktok-shop-ph', sel=cat, price=p); o = compute('tiktok-shop-ph', sel=cat, price=p, rates={'opf': 3, 'growth': 0})
        rows += f"<tr><td>{lab}: {cat}</td><td class='n'>{PHP(p)}</td><td class='n'>{pct(f['rate']['growth'])}</td><td class='n'>{PHP(f['fee']['growth'])}</td><td class='n'>{PHP(o['total'])}</td><td class='n'><b>{PHP(f['total'])}</b></td></tr>"
    m1 = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=299, qty=1)
    month = 1000; base_m = 299 * month
    body = f'''
<p>TikTok Shop Philippines charges a <b>Seller Growth Fee</b> on every successful order. TikTok says it funds platform-wide growth incentives, including offering the Bonus Cashback Program to all eligible sellers for free, with more platform subsidies and support promised for the future.</p>
<h2 id="rates">Seller Growth Fee rates</h2>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Product group</th><th class="n">Rate (VAT inclusive)</th></tr></thead><tbody>
<tr><td>Electronics, Grocery, Large Appliances</td><td class="n">1%</td></tr>
<tr><td>Beauty &amp; Personal Care, Fashion, Mom &amp; Baby, Health, Lifestyle (except Large Appliances)</td><td class="n">1.5%</td></tr></tbody></table></div>
<p>TikTok's list uses broad groups rather than its commission sub-categories. Two commission categories aren't clearly covered: Kids' Fashion and Pet Supplies. Our <a href="../../tiktok-shop/philippines/">Philippines calculator</a> assumes 1.5% for both and lets you edit the rate.</p>
<h2 id="when">When did it start?</h2>
<p>Seller news reports put the start at 27 April 2026, when TikTok expanded Bonus Cashback to all eligible sellers and cut its service fee from 2% to 0%. We couldn't read an official page that states the date, so treat it as reported rather than confirmed. TikTok's current fee overview, updated 13 October 2026, lists the growth fee as a standard seller fee.</p>
<p>Bonus Cashback benefits only apply to eligible sellers: TikTok's overview says a Seller Shop Experience Score of at least 2.8 or fewer than 36 violation points. The growth fee itself is charged to all sellers.</p>
<h2 id="stack">How it stacks with the other fees</h2>
<p>The growth fee comes on top of commission (5%–7.3% Marketplace), the 2.24% transaction fee, the 5.5% Shipping Service Fee (5% Mall, capped at ₱100 per item) and the ₱5 Order Processing Fee, which rose from ₱3 on 1 September 2026. The table compares total fees per order now with January–April 2026 (₱3 processing fee, no growth fee), for Marketplace sellers with no discount and no buyer-paid shipping:</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Example</th><th class="n">Price</th><th class="n">Growth rate</th><th class="n">Growth fee</th><th class="n">All fees, Jan–Apr 2026</th><th class="n">All fees now</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>At 1,000 orders a month of a ₱299 fashion item, the growth fee alone is {PHP(r_ := m1['fee']['growth'] * month)} a month.</p>
<h2 id="base">What is it charged on?</h2>
<p>TikTok's overview gives the rate but not the base. We assume it works like commission and the Shipping Service Fee, on item price minus seller discount. Check one order's settlement detail to confirm: divide the Seller Growth Fee line by the item subtotal after your discount and you should get 1% or 1.5%.</p>
<h2 id="reduce">Can you reduce it?</h2>
<p>There is no published exemption. What you can control is pricing: the growth fee is a percentage, so it scales with price, while the ₱5 processing fee is flat. Use the <a href="../tiktok-shop-pricing-target-margin/">target-margin pricing method</a> with all five fees included.</p>
'''
    return body

def solve_price(mid, cost, target, step=0.01, **kw):
    lo, hi = 0.0, 100000.0
    for _ in range(60):
        mid_p = (lo + hi) / 2
        f = compute(mid, price=mid_p, cost=cost, **kw)
        if f['margin'] >= target: hi = mid_p
        else: lo = mid_p
    import math
    p = math.ceil(hi * 100) / 100
    return p, compute(mid, price=p, cost=cost, **kw)

def g_price():
    wt = "Womenswear & Underwear › Women's Tops"
    v_my = myr(wt)['new.mp.non'] + 3.78
    p1, f1 = solve_price('tiktok-shop-my', 20, 25, sel=wt)
    p1a, f1a = solve_price('tiktok-shop-my', 20, 25, sel=wt, affPct=10)
    p2, f2 = solve_price('tiktok-shop-ph', 200, 25, sel='Womenswear & Underwear')
    v_ph = 7.3 + 2.24 + 5.5 + 1.5
    p3, f3 = solve_price('tiktok-shop-us', 8, 25, shipCost=4)
    body = f'''
<p>Most sellers price by adding a markup to cost and hoping fees don't eat it. On TikTok Shop that rarely works, because some fees are percentages of the price and some are flat per order. The reliable way is to start from the margin you want and solve for the price.</p>
<h2 id="formula">The formula</h2>
<p>Split your costs into two groups:</p>
<ul><li><b>Fixed costs per order (F):</b> product cost, your shipping cost, packaging, and flat platform fees such as the RM0.54 Platform Support Fee (Malaysia) or the ₱5 Order Processing Fee (Philippines).</li>
<li><b>Percentage fees (v):</b> commission, transaction fee and any other fee charged as a percentage of the price, plus affiliate commission if you use creators.</li></ul>
<p>If m is your target margin as a share of the price, then:</p>
<div class="callout"><p><b>Price = F ÷ (1 − v − m)</b></p></div>
<p>For example, with 18% percentage fees and a 25% target margin, divide your fixed costs by 0.57. If v + m reaches 100%, no price works: you need to lower costs, fees or your target.</p>
<h2 id="my">Example: Malaysia</h2>
<p>A women's top costing RM20, non-BXP Marketplace, from 31 October 2026. Commission is {pct(myr(wt)['new.mp.non'])} and the transaction fee 3.78%, so v = {v_my:.2f}%. F = RM20 + RM0.54 = RM20.54. For a 25% margin:</p>
<p>Price = 20.54 ÷ (1 − {v_my/100:.4f} − 0.25) ≈ <b>{RM(p1)}</b>. Check in the calculator: fees {RM(f1['total'])}, profit {RM(f1['profit'])}, margin {f1['margin']:.1f}%.</p>
<p>Add a 10% creator commission and the price for the same margin rises to <b>{RM(p1a)}</b> (margin {f1a['margin']:.1f}%). Creator commission is often the biggest single lever on price.</p>
<h2 id="ph">Example: Philippines</h2>
<p>A ₱200 womenswear item, Marketplace. Percentage fees: 7.3% commission + 2.24% transaction + 5.5% Shipping Service Fee + 1.5% Seller Growth Fee = {v_ph:.2f}%. F = ₱200 + ₱5 = ₱205.</p>
<p>Price = 205 ÷ (1 − {v_ph/100:.4f} − 0.25) ≈ <b>{PHP(p2)}</b>, giving fees of {PHP(f2['total'])} and a {f2['margin']:.1f}% margin. This works while the Shipping Service Fee stays under its ₱100 per item cap; above that, treat it as a fixed ₱100.</p>
<h2 id="us">Example: United States</h2>
<p>An item costing $8 with a $4 shipping label, buyer pays no shipping, 6% referral fee. Price = 12 ÷ (1 − 0.06 − 0.25) ≈ <b>{USD(p3)}</b>, for a referral fee of {USD(f3['total'])} and a {f3['margin']:.1f}% margin.</p>
<h2 id="pitfalls">Common pitfalls</h2>
<ul><li><b>Margin vs markup.</b> A 25% margin is profit equal to 25% of the price. It is a 33% markup on cost-plus-fees. Mixing them up is the most common pricing mistake.</li>
<li><b>Discounts change the base.</b> Seller-funded discounts reduce the price the percentages apply to, but your fixed costs stay. Solve the formula at the discounted price you actually expect to sell at.</li>
<li><b>Campaign fees.</b> In Malaysia, BXP sellers pay 7.02% instead of 4.86% on campaign days. Price your campaign offers with the campaign rate.</li>
<li><b>Returns.</b> Some flat fees aren't refunded on returns after delivery (the Malaysian Platform Support Fee and the Philippine Order Processing Fee). If your return rate is high, add a return allowance to F.</li></ul>
<p>Use the <a href="../../tiktok-shop/malaysia/">Malaysia</a>, <a href="../../tiktok-shop/philippines/">Philippines</a> or <a href="../../tiktok-shop/united-states/">US</a> calculator to check any price you get from the formula.</p>
'''
    return body

def g_settle():
    g = compute('tiktok-shop-my', sel='Toys & Hobbies › Musical Instruments & Accessories', price=1000, sellerDisc=100)
    body = f'''
<p>TikTok Shop deducts its fees from each order's settlement before paying you, so you never see an invoice line by line unless you look for it. Checking a handful of orders each month is the fastest way to catch a wrong category, a fee you didn't expect or a rate change you missed.</p>
<h2 id="where">Where to find the numbers</h2>
<ul><li><b>Orders not settled yet:</b> Seller Center → Finance → Transactions → To settle → View Details. This shows the estimated settlement and each fee.</li>
<li><b>Settled orders:</b> Seller Center → Finance → Withdrawals → Settled → View Details (Earning Details).</li>
<li><b>Monthly invoices:</b> in the Philippines, Finance → Invoice Center → Platform Service Fee has an invoice for the previous month's commission.</li>
<li><b>BXP fees (Malaysia):</b> Finance → Settled records → View Details. The BXP program fee appears as two components, the BCP service fee and the VXP service fee. Add them together.</li></ul>
<h2 id="lines">How each line should be calculated</h2>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Market</th><th>Fee line</th><th>Formula</th></tr></thead><tbody>
<tr><td>MY</td><td>Commission</td><td>(item price − seller discount) × category rate</td></tr>
<tr><td>MY</td><td>Transaction fee</td><td>(item price − seller discount + buyer-paid shipping) × 3.78% (4.86% for PayLater)</td></tr>
<tr><td>MY</td><td>Platform Support Fee</td><td>RM0.54 per delivered order</td></tr>
<tr><td>MY</td><td>BXP (BCP + VXP)</td><td>(item price − seller discount) × 4.86% (7.02% campaign days), max RM54 per item</td></tr>
<tr><td>PH</td><td>Commission</td><td>(item price − seller discount) × category rate</td></tr>
<tr><td>PH</td><td>Transaction fee</td><td>2.24%</td></tr>
<tr><td>PH</td><td>Shipping Service Fee</td><td>(item price − seller discount) × 5.5% Marketplace / 5% Mall, max ₱100 per item</td></tr>
<tr><td>PH</td><td>Order Processing Fee</td><td>₱5 per delivered order (unless exempt)</td></tr>
<tr><td>PH</td><td>Seller Growth Fee</td><td>1% or 1.5% by category</td></tr>
<tr><td>US</td><td>Referral fee</td><td>(customer payment + platform discount − tax) × rate</td></tr>
<tr><td>UK</td><td>Commission</td><td>(net sales + customer-paid shipping + platform discount − refunds) × 9% or 5%</td></tr>
</tbody></table></div>
<h2 id="check">A five-minute check</h2>
<ol><li>Pick three recent settled orders in different categories.</li>
<li>For each, note the item price, your seller discount, buyer-paid shipping and the fee lines.</li>
<li>Enter the same order in the calculator for your market, with the right store type and program settings.</li>
<li>Compare line by line. Differences of a cent come from rounding. Bigger differences usually mean one of the issues below.</li></ol>
<p>As a reference point, TikTok Malaysia's own example (a RM1,000 guitar with a RM100 seller discount, non-BXP Marketplace at 12.96%) gives commission {RM(g['fee']['commission'])} and transaction fee {RM(g['fee']['tx'])}, which our calculator matches.</p>
<h2 id="mismatch">Why a fee might not match</h2>
<ul><li><b>Wrong category.</b> Commission depends on the sub-category TikTok assigned, which may not be the one you chose. In the UK, re-categorised products lose the reduced 5% rate.</li>
<li><b>Platform discounts.</b> Platform-funded vouchers are not subtracted from the commission base, and since 15 February 2026 not from the Malaysian transaction fee base either. The fee is calculated as if the buyer paid full price.</li>
<li><b>Payment method.</b> In Malaysia, PayLater orders from 16 October 2026 carry a 4.86% transaction fee.</li>
<li><b>Order date.</b> Malaysia's new commission table applies to orders placed from 31 October 2026, not to the settlement date.</li>
<li><b>Waivers.</b> New-seller commission waivers, Platform Support Fee rebates and the Philippine Order Processing Fee exemption for the first 50 orders a month all change the numbers.</li></ul>
<h2 id="returns">What happens on returns</h2>
<ul><li><b>Commission and transaction fee:</b> refunded in full if the whole order is returned, and for the refunded items on a partial refund (Malaysia, Philippines, UK).</li>
<li><b>Malaysia Platform Support Fee:</b> not refunded once the order was delivered. Refunded only if the whole order is cancelled before delivery.</li>
<li><b>Philippines Order Processing Fee:</b> not refunded once the order was delivered. On undelivered orders it is refunded only if the whole order is refunded.</li></ul>
<p>If a deduction still doesn't add up, raise a ticket in Seller Center → Help Center with the order ID and your calculation.</p>
'''
    return body

GUIDE_BODY = {GUIDES[0]['slug']: g_my, GUIDES[1]['slug']: g_ph, GUIDES[2]['slug']: g_price, GUIDES[3]['slug']: g_settle}
GUIDE_SOURCES = {
 GUIDES[0]['slug']: MARKETS['tiktok-shop-my']['sources'],
 GUIDES[1]['slug']: MARKETS['tiktok-shop-ph']['sources'],
 GUIDES[2]['slug']: MARKETS['tiktok-shop-my']['sources'][:3] + MARKETS['tiktok-shop-ph']['sources'][:3] + MARKETS['tiktok-shop-us']['sources'],
 GUIDES[3]['slug']: MARKETS['tiktok-shop-my']['sources'] + MARKETS['tiktok-shop-ph']['sources'][:3] + MARKETS['tiktok-shop-us']['sources'] + MARKETS['tiktok-shop-uk']['sources'],
}

# ======================================================================= MALAY: Malaysia calculator
def my_page_ms():
    sk = 'Beauty & Personal Care › Skincare'; r = myr(sk)
    old = compute('tiktok-shop-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('tiktok-shop-my', sel=sk, period='new', price=39.90, cost=12)
    toc = [('yuran', 'Cara yuran TikTok Shop Malaysia dikira'), ('contoh', 'Contoh pengiraan'), ('perubahan', 'Perubahan pada 2026'), ('faq', 'Soalan lazim'), ('sources', 'Sumber rasmi')]
    body = f'''
<h2 id="yuran">Cara yuran TikTok Shop Malaysia dikira</h2>
<p>Bagi setiap pesanan yang berjaya dihantar, TikTok Shop Malaysia menolak tiga yuran daripada penyelesaian anda, dan satu lagi jika anda menyertai Bonus Extra Program (BXP). Semua kadar yang diterbitkan oleh TikTok sudah termasuk SST 8%.</p>
<ul>
<li><b>Yuran komisen:</b> bergantung pada subkategori produk, jenis kedai (Marketplace atau Mall) dan sama ada anda penjual BXP. Komisen = (harga item − diskaun penjual) × kadar. Caj penghantaran dan diskaun tajaan platform tidak termasuk dalam asas pengiraan.</li>
<li><b>Yuran transaksi:</b> 3.78% atas (harga asal item − diskaun penjual + caj penghantaran yang dibayar pembeli). Mulai 16 Oktober 2026, pesanan yang dibayar dengan TikTok PayLater dikenakan 4.86%.</li>
<li><b>Yuran Sokongan Platform:</b> RM0.54 (RM0.50 + SST) bagi setiap pesanan yang berjaya dihantar, tanpa mengira nilai atau kuantiti. Yuran ini tidak dipulangkan jika pesanan yang telah dihantar kemudiannya dipulangkan.</li>
<li><b>Yuran perkhidmatan BXP:</b> 4.86% bagi setiap pesanan yang selesai, atau 7.02% pada hari kempen (Double Day dan Payday) mulai 7 Oktober 2026, dihadkan kepada RM54 seunit.</li>
</ul>
<h2 id="contoh">Contoh pengiraan</h2>
<div class="example"><h4>Serum penjagaan kulit RM39.90, Marketplace, bukan BXP, kos RM12</h4>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">Sebelum 31 Okt</th><th class="n">Mulai 31 Okt</th></tr></thead><tbody>
<tr><td>Komisen</td><td class="n">{pct(r['old.mp.non'])} = −{RM(old['fee']['commission'])}</td><td class="n">{pct(r['new.mp.non'])} = −{RM(new['fee']['commission'])}</td></tr>
<tr><td>Yuran transaksi (3.78%)</td><td class="n">−{RM(old['fee']['tx'])}</td><td class="n">−{RM(new['fee']['tx'])}</td></tr>
<tr><td>Yuran Sokongan Platform</td><td class="n">−{RM(old['fee']['psf'])}</td><td class="n">−{RM(new['fee']['psf'])}</td></tr>
<tr><td><b>Bayaran</b></td><td class="n"><b>{RM(old['payout'])}</b></td><td class="n"><b>{RM(new['payout'])}</b></td></tr>
<tr><td><b>Untung</b></td><td class="n"><b>{RM(old['profit'])}</b></td><td class="n"><b>{RM(new['profit'])}</b></td></tr></tbody></table></div>
<p>Jadual komisen baharu mengurangkan untung sebanyak {RM(old['profit'] - new['profit'])} bagi setiap pesanan.</p></div>
<h2 id="perubahan">Perubahan pada 2026</h2>
<div class="tablewrap"><table><thead><tr><th>Berkuat kuasa</th><th>Perubahan</th></tr></thead><tbody>
<tr><td>15 Feb 2026</td><td>Yuran Sokongan Platform RM0.54 diperkenalkan. Asas yuran transaksi menjadi harga item − diskaun penjual + caj penghantaran pembeli.</td></tr>
<tr><td>7 Okt 2026</td><td>Yuran BXP pada hari kempen naik daripada 4.86% kepada 7.02%.</td></tr>
<tr><td>16 Okt 2026</td><td>Yuran transaksi bagi pesanan TikTok PayLater naik kepada 4.86%.</td></tr>
<tr><td>31 Okt 2026</td><td>Jadual komisen Marketplace dan Mall baharu. Pesanan yang dibuat sebelum tarikh ini mengikut kadar lama.</td></tr></tbody></table></div>
<p>Panduan penuh dan jadual semua {len(MYO)} subkategori tersedia dalam <a href="../../../en/tiktok-shop/malaysia/">versi bahasa Inggeris</a>.</p>
'''
    faq = [
     ("Apakah yuran penjual TikTok Shop Malaysia pada 2026?", "Yuran komisen mengikut kategori produk, yuran transaksi 3.78% (4.86% untuk pesanan TikTok PayLater mulai 16 Oktober 2026) dan Yuran Sokongan Platform RM0.54 bagi setiap pesanan yang dihantar. Penjual BXP juga membayar yuran perkhidmatan BXP 4.86%, atau 7.02% pada hari kempen. Semua kadar termasuk SST 8%."),
     ("Bilakah kadar komisen baharu bermula?", "Pada 00:00, 31 Oktober 2026, waktu Malaysia. Pesanan yang dibuat sebelum itu dikenakan kadar lama."),
     ("Bagaimanakah komisen dikira?", "Komisen = (harga item − diskaun penjual) × kadar kategori. Caj penghantaran dan diskaun tajaan platform tidak termasuk."),
     ("Adakah Yuran Sokongan Platform dipulangkan jika pesanan dipulangkan?", "Tidak, jika pesanan telah berjaya dihantar. Yuran hanya dipulangkan jika keseluruhan pesanan dibatalkan sebelum penghantaran."),
     ("Adakah kadar ini termasuk SST?", "Ya. TikTok menerbitkan kadar komisen, transaksi, BXP dan Yuran Sokongan Platform termasuk SST 8%."),
    ]
    return dict(title='Kalkulator Yuran TikTok Shop Malaysia 2026 (Kadar Komisen Baharu 31 Okt)',
                desc='Kalkulator yuran dan untung TikTok Shop Malaysia percuma dengan jadual komisen baharu mulai 31 Oktober 2026, yuran transaksi 3.78%/4.86%, Yuran Sokongan Platform RM0.54 dan BXP.',
                h1='Kalkulator Yuran TikTok Shop Malaysia', lede='Lihat dengan tepat berapa yang ditolak oleh TikTok Shop Malaysia bagi setiap pesanan dan berapa yang anda simpan, berdasarkan jadual komisen rasmi untuk pesanan mulai 31 Oktober 2026.',
                body=body, faq=faq, toc=toc)

PAGE_FN = {('tiktok-shop-my', 'en'): my_page, ('tiktok-shop-my', 'ms'): my_page_ms, ('tiktok-shop-ph', 'en'): ph_page,
           ('tiktok-shop-us', 'en'): us_page, ('tiktok-shop-uk', 'en'): uk_page, ('etsy', 'en'): etsy_page}

# Russia (Ozon, Wildberries, Yandex Market) — EN + RU
from content_ru import PAGE_FN_RU, GUIDES_RU
PAGE_FN.update(PAGE_FN_RU)
GUIDES.extend(GUIDES_RU)

# Shopee + Lazada
from content_sea import PAGE_FN_SEA, GUIDES_SEA, GUIDE_BODY_SEA, GUIDE_SOURCES_SEA
PAGE_FN.update(PAGE_FN_SEA)
GUIDES.extend(GUIDES_SEA)
GUIDE_BODY.update(GUIDE_BODY_SEA)
GUIDE_SOURCES.update(GUIDE_SOURCES_SEA)

# Simplified Chinese
from content_zh import PAGE_FN_ZH, GUIDES_ZH
PAGE_FN.update(PAGE_FN_ZH)
GUIDES.extend(GUIDES_ZH)

# TikTok Shop Singapore & Thailand, Etsy UK — EN + ZH
from content_new import PAGE_FN_NEW, GUIDES_NEW, GUIDE_BODY_NEW, GUIDE_SOURCES_NEW
from content_new_zh import PAGE_FN_NEW_ZH, GUIDES_NEW_ZH
PAGE_FN.update(PAGE_FN_NEW); PAGE_FN.update(PAGE_FN_NEW_ZH)
GUIDES.extend(GUIDES_NEW); GUIDES.extend(GUIDES_NEW_ZH)
GUIDE_BODY.update(GUIDE_BODY_NEW); GUIDE_SOURCES.update(GUIDE_SOURCES_NEW)

