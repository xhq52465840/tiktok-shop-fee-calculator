"""TikTok Shop Singapore & Thailand, Etsy UK — English page copy and guides.
Every number comes from the rate files (src/data) or markets.compute(); nothing is typed in by hand
except rates quoted from the official pages cited in each market's sources."""
from collections import Counter
from markets import MARKETS, compute, USD_GBP
from site_helpers import money, pct, ex_table

SGO = MARKETS['tiktok-shop-sg']['selector']['options']
THO = MARKETS['tiktok-shop-th']['selector']['options']
SGD = lambda v: money(v, 'SGD'); THB = lambda v: money(v, 'THB'); GBP = lambda v: money(v, 'GBP')
FIXED = ('pif', 'listing', 'epf', 'psf')
LBL = dict(commission='Commission', tx='Transaction fee', bxp='BXP service fee', cgf='Commerce Growth Fee', pif='Platform Infrastructure Fee',
           listing='Listing fee (US$0.20 converted)', etx='Transaction fee', epp='Payment processing', epf='Payment processing (flat)',
           rof='Regulatory operating fee', offads='Offsite Ads fee', feevat='VAT on Etsy fees', aff='Affiliate commission')

def ex_rows(f, cur, labels=LBL, extra_top=(), tot='Total fees', pay='Payout'):
    M = lambda v: money(v, cur)
    rows = list(extra_top)
    for k, r, a in f['rows']:
        rows.append((labels[k] if k in FIXED else f"{labels[k]} ({pct(r)})", '−' + M(a)))
    rows.append((tot, M(f['total']), True))
    rows.append((pay, M(f['payout']), True))
    return rows

def opt(opts, g, n):
    return next(o for o in opts if o['g'] == g and o['n'] == n)

def label(o):
    return f"{o['g']} › {o['n']}"

def grouped(opts, keys):
    """Collapse sub-categories that share identical rates within the same L1 › L2 into one row (keeps the page light);
    L2 groups with mixed rates are listed sub-category by sub-category."""
    from itertools import groupby
    out = []
    for (g, l2), items in groupby(opts, key=lambda o: (o['g'], o['n'].split(' › ')[0])):
        items = list(items)
        sig = {tuple(o['r'].get(k) for k in keys) for o in items}
        if len(sig) == 1 and len(items) > 1: out.append((f"{g} › {l2} <span class='muted'>(all {len(items)})</span>", items[0]['r']))
        else: out.extend((label(o), o['r']) for o in items)
    return out

# ------------------------------------------------------------------ shared stats (computed from the rate files)
def sg_stats():
    old_non = Counter(o['r']['old.non'] for o in SGO); new_non = Counter(o['r']['new.non'] for o in SGO)
    moved = Counter((o['r']['old.non'], o['r']['new.non']) for o in SGO)
    cap_new = sum(1 for o in SGO if o['r'].get('cap_new')); cap_old = sum(1 for o in SGO if o['r'].get('cap_old'))
    low = sum(1 for o in SGO if o['r']['bxpfee'] == 3.27)
    return dict(old_non=old_non, new_non=new_non, moved=moved, cap_new=cap_new, cap_old=cap_old, low=low, n=len(SGO))

def th_stats():
    nm = Counter(o['r']['new.mp'] for o in THO)
    up = Counter(round(o['r']['new.mp'] - o['r']['old.mp'], 2) for o in THO if 'old.mp' in o['r'])
    upm = Counter(round(o['r']['new.mall'] - o['r']['old.mall'], 2) for o in THO if 'old.mall' in o['r'])
    el = sum(1 for o in THO if o['r']['cgf'] == 6.96)
    return dict(nm=nm, up=up, upm=upm, el=el, n=len(THO), new_only=sum(1 for o in THO if 'old.mp' not in o['r']))

# ================================================================== TikTok Shop Singapore
SG_SAMPLE = [('Beauty & Personal Care', 'Skincare › Serums & Essences'), ('Beauty & Personal Care', 'Makeup › Lipstick & Lip Gloss'),
             ('Womenswear & Underwear', "Women's Tops › Women's T-shirts"), ('Food & Beverages', 'Snacks › Crisps & Puffed Snacks'),
             ('Phones & Electronics', 'Phones & Tablets › Mobile Phones'), ('Phones & Electronics', 'Audio & Video › Headphones, Earphones & Accessories'),
             ('Phones & Electronics', 'Phones & Tablets › Tablets'), ('Household Appliances', 'Kitchen Appliances › Fryers'),
             ('Computers & Office Equipment', 'Desktop Computers, Laptops & Tablets › Laptops'), ('Baby & Maternity', 'Formula Milk & Baby Food › Infant Formula'),
             ('Toys & Hobbies', 'Classic & Novelty Toys › Building Toys'), ('Home Supplies', 'Home Organizers › Storage Boxes & Bins')]

def _sg_sample():
    out = []
    for g, n in SG_SAMPLE:
        try: out.append(opt(SGO, g, n))
        except StopIteration: pass
    return out

def _cap(v): return f'S${v:g}' if v else '–'

def sg_page():
    sk = ('Beauty & Personal Care', 'Skincare › Serums & Essences'); ph = 'Phones & Tablets › Mobile Phones'
    new = compute('tiktok-shop-sg', price=29.90, cost=9); old = compute('tiktok-shop-sg', period='old', price=29.90, cost=9)
    bxp = compute('tiktok-shop-sg', tg={'bxp': True}, price=29.90, cost=9); bxpc = compute('tiktok-shop-sg', tg={'bxp': True, 'sgCampaign': True}, price=29.90, cost=9)
    pn = compute('tiktok-shop-sg', sel=ph, price=499, cost=380); po = compute('tiktok-shop-sg', sel=ph, period='old', price=499, cost=380)
    e1 = compute('tiktok-shop-sg', tg={'bxp': True}, price=160, sellerDisc=20, buyerShip=2)
    e2 = compute('tiktok-shop-sg', tg={'bxp': True}, price=600, sellerDisc=10, buyerShip=2)
    t1 = compute('tiktok-shop-sg', price=1000, buyerShip=10)
    st = sg_stats()
    rows = ''.join(f"<tr><td>{label(o)}</td><td class='n'><b>{pct(o['r']['new.non'])}</b></td><td class='n'>{pct(o['r']['new.bxp'])}</td><td class='n'>{_cap(o['r'].get('cap_new'))}</td>"
                   f"<td class='n'>{pct(o['r']['old.non'])}</td><td class='n'>{pct(o['r']['old.bxp'])}</td><td class='n'>{_cap(o['r'].get('cap_old'))}</td><td class='n'>{pct(o['r']['bxpfee'])}</td></tr>" for o in _sg_sample())
    full = ''.join(f"<tr><td>{n}</td><td class='n'>{pct(r['new.non'])}</td><td class='n'>{pct(r['new.bxp'])}</td><td class='n'>{_cap(r.get('cap_new'))}</td>"
                   f"<td class='n'>{pct(r['old.non'])}</td><td class='n'>{pct(r['old.bxp'])}</td><td class='n'>{_cap(r.get('cap_old'))}</td><td class='n'>{pct(r['bxpfee'])}</td></tr>"
                   for n, r in grouped(SGO, ['new.non', 'new.bxp', 'cap_new', 'old.non', 'old.bxp', 'cap_old', 'bxpfee']))
    thead = "<thead><tr><th>Category</th><th class='n'>Non-BXP from 1 Sep</th><th class='n'>BXP from 1 Sep</th><th class='n'>Cap from 1 Sep</th><th class='n'>Non-BXP 27 Jul</th><th class='n'>BXP 27 Jul</th><th class='n'>Cap 27 Jul</th><th class='n'>BXP service fee</th></tr></thead>"
    toc = [('how', 'How TikTok Shop Singapore fees work'), ('examples', 'Worked examples'), ('changes', 'What changed on 1 September 2026'),
           ('rates', 'Commission rates by category'), ('limits', 'What the calculator assumes'), ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How TikTok Shop Singapore fees work</h2>
<p>TikTok Shop Singapore's own fee overview lists two seller fees on a delivered order: a <b>Platform Commission Fee</b> and a <b>Transaction Fee</b>. Sellers in the Bonus Extra Program (BXP) pay a third, the BXP service fee. Every rate TikTok publishes for Singapore already includes 9% GST, so nothing is added on top.</p>
<h3>1. Platform Commission Fee</h3>
<p>From 00:00 on 1 September 2026 (GMT+8), the official table charges <b>9.810%</b> to standard sellers and <b>7.085%</b> to BXP sellers in every category. Rows in the "EL, Toys &amp; Collectibles" industry — electronics, appliances, computers, toys, collectibles, vouchers and similar — carry a <b>S$30 fee cap</b>; every other row has no cap. The base is <b>(item price − seller discount) × rate</b>. Shipping and TikTok-funded discounts are not part of it.</p>
<h3>2. Transaction Fee</h3>
<p><b>3.27%</b> (GST-inclusive) since 1 October 2025, up from 2.18%. Since 1 April 2026 it is charged on what the customer paid (including shipping) plus TikTok's platform discount, minus any refunds. TikTok's example: S$1,010 × 3.27% = S$33.027. It is refunded proportionally when an order is returned.</p>
<h3>3. BXP service fee (BXP sellers only)</h3>
<p>BXP gives your products Bonus Cashback, LIVE Specials and Voucher Xtra vouchers in exchange for a service fee on <b>every</b> completed order, voucher or not: <b>3.27%</b> in listed electronics, baby-care and appliance sub-categories and <b>5.45%</b> in all others, on (net product price − seller-funded discounts), capped at <b>S$30 per item</b>. During double-digit and Payday campaigns it rises by 1.09 points (4.36% / 6.54%). The calculator applies the right rate to each of the {st['n']:,} categories ({st['low']} sit in the 3.27% group).</p>

<h2 id="examples">Worked examples</h2>
<p>All examples use the official tables and the same formulas as the calculator above.</p>
<div class="example"><h4>Example 1: a S$29.90 serum, not in BXP, before and after 1 September</h4>
<p>Product cost S$9, no discount, free shipping funded by the platform.</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">27 Jul – 31 Aug</th><th class="n">From 1 Sep</th></tr></thead><tbody>
<tr><td>Commission</td><td class="n">{pct(old['rate']['commission'])} = −{SGD(old['fee']['commission'])}</td><td class="n">{pct(new['rate']['commission'])} = −{SGD(new['fee']['commission'])}</td></tr>
<tr><td>Transaction fee (3.27%)</td><td class="n">−{SGD(old['fee']['tx'])}</td><td class="n">−{SGD(new['fee']['tx'])}</td></tr>
<tr><td><b>Payout</b></td><td class="n"><b>{SGD(old['payout'])}</b></td><td class="n"><b>{SGD(new['payout'])}</b></td></tr>
<tr><td><b>Profit after S$9 cost</b></td><td class="n"><b>{SGD(old['profit'])}</b></td><td class="n"><b>{SGD(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>The 1 September table costs this seller {SGD(old['profit'] - new['profit'])} per order; margin moves from {old['margin']:.1f}% to {new['margin']:.1f}%.</p></div>
<div class="example"><h4>Example 2: the same serum as a BXP seller</h4>
{ex_table(ex_rows(bxp, 'SGD'))}
<p>Profit {SGD(bxp['profit'])} on a normal day and {SGD(bxpc['profit'])} on a campaign day (BXP fee 6.54%), against {SGD(new['profit'])} outside BXP. BXP only pays for itself if its vouchers bring in extra orders.</p></div>
<div class="example"><h4>Example 3: a S$499 phone — the new S$30 cap</h4>
<p>Mobile phones sit in the capped electronics group. Uncapped, 9.81% would be {SGD(499 * 0.0981)}.</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">27 Jul – 31 Aug</th><th class="n">From 1 Sep</th></tr></thead><tbody>
<tr><td>Commission</td><td class="n">{pct(po['rate']['commission'])} = −{SGD(po['fee']['commission'])}</td><td class="n">capped −{SGD(pn['fee']['commission'])}</td></tr>
<tr><td>Transaction fee (3.27%)</td><td class="n">−{SGD(po['fee']['tx'])}</td><td class="n">−{SGD(pn['fee']['tx'])}</td></tr>
<tr><td><b>Profit after S$380 cost</b></td><td class="n"><b>{SGD(po['profit'])}</b></td><td class="n"><b>{SGD(pn['profit'])}</b></td></tr>
</tbody></table></div>
<p>For high-ticket electronics the new table is cheaper: the cap fell from S$50 to S$30 per item, so this phone keeps {SGD(pn['profit'] - po['profit'])} more per order.</p></div>
<div class="example"><h4>Example 4: TikTok's own BXP examples</h4>
<p>TikTok's BXP page uses two orders at 5.45%. The calculator reproduces both: S$160 with a S$20 seller discount gives a BXP fee of <b>{SGD(e1['fee']['bxp'])}</b> ((160 − 20) × 5.45%), and S$600 with a S$10 discount gives {SGD(590 * 0.0545)} before the cap, charged as <b>{SGD(e2['fee']['bxp'])}</b>. The transaction-fee example (S$1,010 × 3.27%) comes out at {SGD(t1['fee']['tx'])} after rounding.</p></div>

<h2 id="changes">What changed on 1 September 2026</h2>
<p>TikTok replaced the 27 July 2026 table with a single flat structure:</p>
<div class="tablewrap"><table><thead><tr><th></th><th>27 Jul – 31 Aug 2026</th><th>From 1 Sep 2026</th></tr></thead><tbody>
<tr><td>Standard (non-BXP)</td><td>8.175% in most categories; 6.54% in {st['old_non'].get(6.54, 0)} electronics and appliance categories</td><td>9.810% everywhere</td></tr>
<tr><td>BXP</td><td>7.085%; 5.45% in the same electronics and appliance categories</td><td>7.085% everywhere</td></tr>
<tr><td>Fee cap</td><td>S$50 in {st['cap_old']} categories</td><td>S$30 in {st['cap_new']} categories ("EL, Toys &amp; Collectibles")</td></tr>
</tbody></table></div>
<p>For a standard seller that is +{9.81 - 8.175:.3f} points in {st['moved'].get((8.175, 9.81), 0):,} of {st['n']:,} categories and +{9.81 - 6.54:.2f} points in {st['moved'].get((6.54, 9.81), 0)}. In capped categories, any item priced above about {SGD(30 / 0.0981)} (standard) or {SGD(30 / 0.07085)} (BXP) hits the S$30 ceiling. Full analysis: <a href="/en/guides/tiktok-shop-singapore-commission-september-2026/">our guide to the 1 September change</a>.</p>
<p>Earlier tables on TikTok's page took effect on 1 October 2025, 1 April 2026 and 27 July 2026. The calculator keeps the 27 July table so you can compare.</p>

<h2 id="rates">Commission rates by category</h2>
<p>Popular categories. All rates include GST.</p>
<div class="tablewrap"><table class="tbl">{thead}<tbody>{rows}</tbody></table></div>
<details class="adv"><summary>Show all {st['n']:,} categories</summary>
<p class="muted small" style="margin-top:12px">Sub-categories with identical rates are grouped under their parent; mixed groups are listed one by one.</p>
<p style="margin-top:12px"><input id="sf-filter" class="search" type="search" placeholder="Filter, e.g. skincare" aria-label="Filter categories"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates">{thead}<tbody>{full}</tbody></table></div></details>

<h2 id="limits">What the calculator assumes</h2>
<ul>
<li><b>Local sellers.</b> The tables are TikTok Shop Singapore's local-seller tables. Cross-border sellers are billed under the Global Seller programme, and its 3 September 2026 notice shows different rates in its examples — check your Global Seller Center.</li>
<li><b>Marketplace and Mall.</b> TikTok's page says Marketplace and Mall rates can differ, but the 1 September PDF publishes a single set of rates. If your Mall contract shows something else, edit the commission rate.</li>
<li><b>Cap per item.</b> TikTok labels the S$30 as a "fee upper cap"; we apply it per item, the same way TikTok words the BXP cap.</li>
<li><b>BXP-restricted products.</b> Virtual products, infant formula and gold can't use BXP and are charged the standard rate, so leave the BXP switch off for them.</li>
<li><b>Not included:</b> the 1.09% pre-order service fee, affiliate partner fees, shipping adjustments and penalties. Add any that apply under "Other costs".</li>
</ul>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Reprice everyday items.</b> Low-ticket beauty, fashion and food took the full increase to 9.81%. On a S$20 item the extra 1.635 points cost about S$0.33 per order.</li>
<li><b>Check BXP category by category.</b> BXP saves 2.725 commission points but costs 3.27% or 5.45% more, so per-order fees go up. It is worth it only if the vouchers lift sales.</li>
<li><b>Use the cap.</b> Bundles of capped electronics above about S$306 pay no more commission per item, which can make premium bundles more attractive.</li>
<li><b>Fund discounts carefully.</b> Seller discounts reduce the commission base, but every dollar still comes out of your payout. Platform-funded discounts don't reduce commission; they are part of the transaction-fee base.</li>
</ul>
'''
    faq = [
     ("What are TikTok Shop Singapore's seller fees in 2026?", "A Platform Commission Fee of 9.810% (7.085% for BXP sellers) on orders from 1 September 2026, capped at S$30 in electronics, toys and collectibles categories, and a 3.27% Transaction Fee. BXP sellers also pay a 3.27% or 5.45% BXP service fee (capped at S$30 per item). All rates include 9% GST."),
     ("Is TikTok Shop Singapore commission the same for every category?", "Since 1 September 2026, yes: 9.810% standard and 7.085% BXP in every category of the official table. What differs is the S$30 cap, which only applies to the 'EL, Toys & Collectibles' industry."),
     ("How is commission calculated?", "(Item price − seller discount) × rate. Shipping and TikTok's platform discounts are excluded."),
     ("How is the 3.27% transaction fee calculated?", "On the customer's payment, including shipping, plus TikTok's platform discount, minus refunds. It is refunded proportionally on returns."),
     ("When does the BXP service fee go up?", "During double-digit and Payday campaigns it is 1.09 points higher: 4.36% instead of 3.27%, or 6.54% instead of 5.45%."),
     ("Do the rates include GST?", "Yes. TikTok publishes the commission, transaction and BXP service fees for Singapore inclusive of 9% GST."),
     ("Does this calculator work for cross-border sellers?", "It uses the local-seller tables. TikTok's Global Seller notice from 3 September 2026 shows different rates in its examples, so cross-border sellers should check their own Seller Center and edit the rates."),
    ]
    return dict(title='TikTok Shop Singapore Fee Calculator 2026 (9.81% Commission from 1 Sep)',
                desc='Free TikTok Shop Singapore fee and profit calculator: 9.81% / 7.085% BXP commission from 1 Sep 2026 with the S$30 electronics cap, 3.27% transaction fee and BXP service fee. GST-inclusive.',
                h1='TikTok Shop Fee Calculator Singapore',
                lede='See what TikTok Shop Singapore deducts from each order and what you keep, using the official GST-inclusive commission table for orders from 1 September 2026.',
                body=body, faq=faq, toc=toc)

# ================================================================== TikTok Shop Thailand
TH_SAMPLE = [('Beauty & Personal Care', 'Skincare › Serums & Essences'), ('Beauty & Personal Care', 'Makeup › Lipstick & Lip Gloss'),
             ('Womenswear & Underwear', "Women's Tops › Women's T-shirts"), ('Food & Beverages', 'Snacks › Crisps & Puffed Snacks'),
             ('Phones & Electronics', 'Phones & Tablets › Mobile Phones'), ('Phones & Electronics', 'Audio & Video › Headphones, Earphones & Accessories'),
             ('Household Appliances', 'Kitchen Appliances › Fryers'), ('Baby & Maternity', 'Formula Milk & Baby Food › Infant Formula'),
             ('Health', 'Nutrition & Wellness › Beauty Supplement'), ('Home Supplies', 'Home Organizers › Storage Boxes & Bins'),
             ('Pet Supplies', 'Dog & Cat Food › Dog Food'), ('Kitchenware', 'Cookware › Pots')]

def _th_sample():
    out = []
    for g, n in TH_SAMPLE:
        try: out.append(opt(THO, g, n))
        except StopIteration: pass
    return out

def _p(r, k): return pct(r[k]) if k in r else '–'

def th_page():
    sk = 'Skincare › Serums & Essences'; hp = 'Audio & Video › Headphones, Earphones & Accessories'
    new = compute('tiktok-shop-th', price=299, cost=90); old = compute('tiktok-shop-th', period='old', price=299, cost=90)
    mall = compute('tiktok-shop-th', store='mall', price=299, cost=90); combo = compute('tiktok-shop-th', store='mall', tg={'combo': True}, price=299, cost=90)
    hm = compute('tiktok-shop-th', sel=hp, store='mall', price=2000, cost=1100)
    g1 = compute('tiktok-shop-th', price=1000, sellerDisc=100)
    cap = compute('tiktok-shop-th', price=3000, cost=1500)
    sm = compute('tiktok-shop-th', tg={'gmvMax': True, 'smallSeller': True}, price=299, cost=90)
    st = th_stats()
    rows = ''.join(f"<tr><td>{label(o)}</td><td class='n'><b>{_p(o['r'],'new.mp')}</b></td><td class='n'><b>{_p(o['r'],'new.mall')}</b></td><td class='n'>{_p(o['r'],'new.mall_combo')}</td>"
                   f"<td class='n'>{_p(o['r'],'old.mp')}</td><td class='n'>{_p(o['r'],'old.mall')}</td><td class='n'>{_p(o['r'],'cgf')}</td></tr>" for o in _th_sample())
    full = ''.join(f"<tr><td>{n}</td><td class='n'>{_p(r,'new.mp')}</td><td class='n'>{_p(r,'new.mall')}</td><td class='n'>{_p(r,'new.mall_combo')}</td>"
                   f"<td class='n'>{_p(r,'old.mp')}</td><td class='n'>{_p(r,'old.mall')}</td><td class='n'>{_p(r,'cgf')}</td></tr>"
                   for n, r in grouped(THO, ['new.mp', 'new.mall', 'new.mall_combo', 'old.mp', 'old.mall', 'cgf']))
    thead = "<thead><tr><th>Category</th><th class='n'>Marketplace from 5 Jul</th><th class='n'>Mall from 5 Jul</th><th class='n'>Mall Combo from 5 Jul</th><th class='n'>Marketplace 6 May</th><th class='n'>Mall 6 May</th><th class='n'>Commerce Growth Fee</th></tr></thead>"
    top = st['up'].most_common(1)[0]
    toc = [('how', 'How TikTok Shop Thailand fees work'), ('examples', 'Worked examples'), ('changes', 'What changed in 2026'),
           ('rates', 'Commission rates by category'), ('limits', 'What the calculator assumes'), ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How TikTok Shop Thailand fees work</h2>
<p>A delivered order on TikTok Shop Thailand carries four platform fees. TikTok publishes every rate <b>including tax</b> (VAT), so nothing is added on top.</p>
<h3>1. Platform Commission Fee</h3>
<p>Set per sub-category, with separate tables for Marketplace (non-Mall) and Mall sellers. From 00:00 on 5 July 2026 (GMT+7) most Marketplace categories pay <b>10.70%</b> and most Mall categories <b>13.91%</b>; the full range runs from 5.35% to 13.91%. Mall sellers in the <b>Mall Combo Package</b> (enrolled in both Mall Live Specials and Brands Crazy Deals) pay a lower Combo column, usually 10.70%. Formula: <b>(item price − seller discount) × rate</b>; shipping and TikTok's platform discounts are excluded. Marketplace sellers whose GMV Max ad spend exceeds 3% of revenue over the last 30 days get 1.07 points off (since 1 April 2026).</p>
<h3>2. Transaction Fee</h3>
<p><b>3.21%</b>. Since 21 March 2026 it is charged on the customer's payment plus TikTok's platform discount, which includes shipping the buyer pays. It is not refunded if a delivered order is returned. TikTok's example: THB 900 × 3.21% = THB 28.89.</p>
<h3>3. Commerce Growth Fee (CGF)</h3>
<p>From 6 May 2026: <b>6.96%</b> for the Electronics industry ({st['el']} sub-categories) and <b>8.03%</b> for everything else, on (item price − seller discount), capped at <b>฿199 per item</b>. Marketplace sellers with under ฿10,000 GMV in the last 30 days pay 6.42% / 7.49%. New sellers don't pay it for their first 30 days (capped at ฿1,000 in waived fees for sellers onboarded after 16 July 2026), and it isn't charged to sellers who ship only with their own fleet. Not refunded on returns.</p>
<h3>4. Platform Infrastructure Fee</h3>
<p>A flat <b>฿1.07 per delivered order</b> since 1 October 2025, not refunded on returns. Sellers with 1–100 orders in the previous 30 days (window ending on the 20th) have it waived the following month.</p>

<h2 id="examples">Worked examples</h2>
<p>All examples use the official tables and the same formulas as the calculator above.</p>
<div class="example"><h4>Example 1: a ฿299 serum, Marketplace, before and after 5 July</h4>
<p>Product cost ฿90, no discount, free shipping funded by the platform.</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">6 May – 4 Jul</th><th class="n">From 5 Jul</th></tr></thead><tbody>
<tr><td>Commission</td><td class="n">{pct(old['rate']['commission'])} = −{THB(old['fee']['commission'])}</td><td class="n">{pct(new['rate']['commission'])} = −{THB(new['fee']['commission'])}</td></tr>
<tr><td>Transaction fee (3.21%)</td><td class="n">−{THB(old['fee']['tx'])}</td><td class="n">−{THB(new['fee']['tx'])}</td></tr>
<tr><td>Commerce Growth Fee (8.03%)</td><td class="n">−{THB(old['fee']['cgf'])}</td><td class="n">−{THB(new['fee']['cgf'])}</td></tr>
<tr><td>Platform Infrastructure Fee</td><td class="n">−{THB(old['fee']['pif'])}</td><td class="n">−{THB(new['fee']['pif'])}</td></tr>
<tr><td><b>Payout</b></td><td class="n"><b>{THB(old['payout'])}</b></td><td class="n"><b>{THB(new['payout'])}</b></td></tr>
<tr><td><b>Profit after ฿90 cost</b></td><td class="n"><b>{THB(old['profit'])}</b></td><td class="n"><b>{THB(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>Fees now take {THB(new['total'])}, or {new['total'] / 299 * 100:.1f}% of the price. The 5 July table costs {THB(old['profit'] - new['profit'])} per order.</p></div>
<div class="example"><h4>Example 2: the same serum as a Mall seller</h4>
<p>Standard Mall commission is {pct(mall['rate']['commission'])}: total fees {THB(mall['total'])}, profit {THB(mall['profit'])}. In the Mall Combo Package it drops to {pct(combo['rate']['commission'])}: fees {THB(combo['total'])}, profit {THB(combo['profit'])}.</p>
{ex_table(ex_rows(mall, 'THB'))}</div>
<div class="example"><h4>Example 3: TikTok's own examples</h4>
<p>A ฿1,000 item with a ฿100 seller discount, Marketplace, 10.70%: commission <b>{THB(g1['fee']['commission'])}</b>, transaction fee <b>{THB(g1['fee']['tx'])}</b> and Commerce Growth Fee <b>{THB(g1['fee']['cgf'])}</b> (8.03%) — matching TikTok's worked figures of 96.3, 28.89 and 72.27. A ฿2,000 pair of headphones on Mall: commission <b>{THB(hm['fee']['commission'])}</b> (11.77%) and CGF <b>{THB(hm['fee']['cgf'])}</b> (6.96%, Electronics), as in TikTok's examples.</p></div>
<div class="example"><h4>Example 4: the ฿199 Commerce Growth Fee cap</h4>
<p>A ฿3,000 item outside Electronics would owe {THB(3000 * 0.0803)} at 8.03%; the calculator charges the capped <b>{THB(cap['fee']['cgf'])}</b>. The cap kicks in above about {THB(199 / 0.0803)} (or {THB(199 / 0.0696)} for Electronics).</p></div>
<div class="example"><h4>Example 5: a small Marketplace seller using GMV Max</h4>
<p>With both reductions (commission −1.07, CGF −0.54) the serum's fees fall from {THB(new['total'])} to {THB(sm['total'])}.</p></div>

<h2 id="changes">What changed in 2026</h2>
<div class="tablewrap"><table><thead><tr><th>Effective</th><th>Change</th></tr></thead><tbody>
<tr><td>21 Mar 2026</td><td>Transaction fee base becomes customer payment + platform discount (3.21%).</td></tr>
<tr><td>1 Apr 2026</td><td>Marketplace sellers spending over 3% of revenue on GMV Max get commission −1.07 points.</td></tr>
<tr><td>6 May 2026</td><td>New commission tables. Commerce Growth Fee rises from 5.89% / 6.96% to 6.96% / 8.03%, capped at ฿199 per item.</td></tr>
<tr><td>5 Jul 2026</td><td>New Marketplace and Mall commission tables: most Marketplace categories go from 8.56% to 10.70%, most Mall categories from 11.77% to 13.91%.</td></tr>
<tr><td>16 Jul 2026</td><td>New sellers' 30-day CGF waiver capped at ฿1,000.</td></tr>
</tbody></table></div>
<p>Across the {st['n'] - st['new_only']:,} Marketplace sub-categories in both tables, the most common change on 5 July was <b>+{top[0]:.2f} points</b> ({top[1]:,} sub-categories). {st['new_only']} sub-categories appear only in the new table. Full analysis: <a href="/en/guides/tiktok-shop-thailand-seller-fees-2026/">our guide to Thailand seller fees in 2026</a>.</p>

<h2 id="rates">Commission rates by category</h2>
<p>Popular categories. All rates include tax.</p>
<div class="tablewrap"><table class="tbl">{thead}<tbody>{rows}</tbody></table></div>
<details class="adv"><summary>Show all {st['n']:,} sub-categories</summary>
<p class="muted small" style="margin-top:12px">Sub-categories with identical rates are grouped under their parent; mixed groups are listed one by one.</p>
<p style="margin-top:12px"><input id="sf-filter" class="search" type="search" placeholder="Filter, e.g. skincare" aria-label="Filter categories"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates">{thead}<tbody>{full}</tbody></table></div></details>

<h2 id="limits">What the calculator assumes</h2>
<ul>
<li><b>Local sellers</b> on TikTok Shop Thailand. Cross-border sellers are billed under the Global Seller programme.</li>
<li><b>Mall programme fees.</b> Mall Live Specials and Brands Crazy Deals may carry their own fees; the Combo switch only changes the commission rate.</li>
<li><b>Earlier table.</b> The comparison uses the 6 May 2026 table. No 6 May Mall Combo column is loaded, so it shows "not published" if you combine the two.</li>
<li><b>Not included:</b> the 2.14% pre-order service fee, affiliate partner fees and ads. Add them under "Other costs" if they apply.</li>
</ul>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Count all four fees.</b> On a typical non-Electronics Marketplace order, commission + transaction + CGF is about 21.9% before the ฿1.07 flat fee. Many sellers still price as if only commission applies.</li>
<li><b>Use the CGF cap on premium items.</b> Above about ฿2,478 the CGF is fixed at ฿199 per item.</li>
<li><b>Bundle cheap items.</b> The ฿1.07 infrastructure fee is per order.</li>
<li><b>Returns cost more than they look.</b> The transaction fee, CGF and infrastructure fee are not refunded after delivery.</li>
</ul>
'''
    faq = [
     ("What are TikTok Shop Thailand's seller fees in 2026?", "A commission by category (most Marketplace categories 10.70%, most Mall 13.91% from 5 July 2026), a 3.21% transaction fee, a Commerce Growth Fee of 6.96% (Electronics) or 8.03% capped at ฿199 per item, and a ฿1.07 Platform Infrastructure Fee per delivered order. All rates include tax."),
     ("When did the new commission rates start?", "At 00:00 on 5 July 2026, Thailand time (GMT+7), for both Marketplace and Mall."),
     ("What is the Commerce Growth Fee?", "A per-order fee on (item price − seller discount): 6.96% for the Electronics industry and 8.03% for others since 6 May 2026, capped at ฿199 per item. It is waived for new sellers' first 30 days and isn't charged to sellers who ship only with their own fleet."),
     ("What is the Mall Combo Package?", "A lower Mall commission for Mall sellers enrolled in both Mall Live Specials and Brands Crazy Deals who register for the package."),
     ("Are fees refunded when a buyer returns an order?", "Commission is refunded on returned items. The transaction fee, Commerce Growth Fee and Platform Infrastructure Fee are not refunded after delivery."),
     ("Do the rates include VAT?", "Yes. TikTok Shop Thailand publishes all of these rates inclusive of tax."),
    ]
    return dict(title='TikTok Shop Thailand Fee Calculator 2026 (Commission, CGF & ฿1.07 Fee)',
                desc='Free TikTok Shop Thailand fee and profit calculator: Marketplace and Mall commission from 5 Jul 2026, 3.21% transaction fee, 6.96%/8.03% Commerce Growth Fee (฿199 cap) and ฿1.07 infrastructure fee.',
                h1='TikTok Shop Fee Calculator Thailand',
                lede='See what TikTok Shop Thailand deducts from each order — commission, transaction fee, Commerce Growth Fee and the ฿1.07 infrastructure fee — using the official tables from 5 July 2026.',
                body=body, faq=faq, toc=toc)

# ================================================================== Etsy UK
LIST_GBP = round(0.20 * USD_GBP, 2); CAP_GBP = round(100 * USD_GBP, 2)

def etsy_uk_page():
    a = compute('etsy-uk', price=25, buyerShip=4, cost=8, shipCost=3.6)
    v = compute('etsy-uk', sel=1, price=25, buyerShip=4, cost=8, shipCost=3.6, taxPct=16.67)
    o = compute('etsy-uk', tg={'offsite': True}, price=25, buyerShip=4, cost=8, shipCost=3.6)
    big = compute('etsy-uk', tg={'offsite': True}, price=800, cost=300)
    pre = round(sum(x[2] for x in a['rows'] if x[0] != 'feevat'), 2)
    toc = [('how', 'How Etsy fees work for UK sellers'), ('vat', 'VAT on Etsy fees'), ('examples', 'Worked examples'),
           ('limits', 'What the calculator assumes'), ('tips', 'Pricing tips'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Etsy fees work for UK sellers</h2>
<p>A UK shop paid through Etsy Payments to a UK bank account pays these fees on a normal sale:</p>
<ul>
<li><b>Listing fee:</b> US$0.20 per listing, charged again for each extra item sold from a multi-quantity listing and when a sold listing auto-renews. Etsy bills it in US dollars; the calculator converts it to <b>{GBP(LIST_GBP)}</b> at the ECB reference rate of 26 October 2026 (1 USD = {USD_GBP} GBP). Edit it under "Fee rates used" if your statement differs.</li>
<li><b>Transaction fee:</b> 6.5% of the order total in your listing currency — item price plus the postage and gift wrap you charge.</li>
<li><b>Payment processing fee:</b> 4% + £0.20 per order for a UK bank account, on the total sale price including postage and any sales tax Etsy collects.</li>
<li><b>Regulatory operating fee:</b> <b>0.48%</b> of the order total (item price, postage, gift wrap and personalisation) since <b>22 June 2026</b>, up from 0.32%. Etsy charges it in some markets, including the UK, to cover the cost of complying with local regulation.</li>
<li><b>Offsite Ads fee</b> (only on orders from an Offsite Ad): 15% of the order total, or 12% once your shop has made US$10,000 in any 365 days, never more than US$100 per order ({GBP(CAP_GBP)} at the same rate).</li>
</ul>
<p>Etsy Ads, postage labels bought on Etsy and Etsy Plus are separate. Add them under "Other costs".</p>

<h2 id="vat">VAT on Etsy fees</h2>
<p>The UK is one of the countries where Etsy charges VAT on its seller fees. Etsy's help article says that if you <b>haven't</b> added a VAT number, VAT is charged on your seller fees, and on Etsy Payments processing fees where required; if you add a valid VAT number, Etsy doesn't charge VAT and your monthly invoice shows no VAT was charged. The calculator uses the UK standard rate of <b>20%</b> on all Etsy fees in the first option of "Your VAT status on Etsy" and 0% in the second.</p>
<p>If you are VAT-registered you also owe VAT on your own sales. Enter 16.67 under "VAT you owe on your sales" to take the VAT out of a VAT-inclusive price. How you account for VAT on Etsy's fees once Etsy stops charging it is a question for your accountant or HMRC guidance.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: a £25 item with £4 postage, not VAT-registered</h4>
<p>Product cost £8, a £3.60 postage label bought elsewhere.</p>
{ex_table(ex_rows(a, 'GBP'))}
<p>Etsy's fees before VAT come to {GBP(pre)}; 20% VAT adds {GBP(a['fee']['feevat'])}. You keep {GBP(a['payout'])}, and profit after cost and postage is <b>{GBP(a['profit'])}</b> ({a['margin']:.1f}% of the item price). The global Etsy calculator, which leaves out the regulatory fee and VAT, would show {GBP(a['total'] - a['fee']['rof'] - a['fee']['feevat'] - a['fee']['listing'])} in fees before the listing fee.</p></div>
<div class="example"><h4>Example 2: the same order, VAT-registered with a VAT number on Etsy</h4>
<p>No VAT on fees, so fees fall to {GBP(v['total'])}. But the £25 price now contains {GBP(v['tax'])} of VAT you owe HMRC, so profit is <b>{GBP(v['profit'])}</b>.</p></div>
<div class="example"><h4>Example 3: the same order from an Offsite Ad</h4>
{ex_table(ex_rows(o, 'GBP'))}
<p>The 15% Offsite Ads fee ({GBP(o['fee']['offads'])}) also attracts VAT, so fees jump to {GBP(o['total'])} and profit to {GBP(o['profit'])}.</p></div>
<div class="example"><h4>Example 4: an £800 order from an Offsite Ad — the US$100 cap</h4>
<p>15% would be {GBP(120)}; the fee is capped at <b>{GBP(big['fee']['offads'])}</b> (US$100). Total fees {GBP(big['total'])}.</p></div>

<h2 id="limits">What the calculator assumes</h2>
<ul>
<li><b>UK shop, UK bank account, listing in GBP.</b> If you list in another currency Etsy adds a 2.5% currency conversion fee — add it under "Other costs".</li>
<li><b>US-dollar amounts</b> (listing fee and the Offsite Ads cap) are converted at the ECB reference rate of 26 October 2026. Etsy converts at its own rate on the day.</li>
<li><b>VAT at 20%.</b> Etsy's article says it charges the applicable VAT; we use the UK standard rate.</li>
<li><b>One listing fee per item sold.</b> Etsy charges US$0.20 at publication and again on each renewal and multi-quantity sale.</li>
</ul>

<h2 id="tips">Pricing tips</h2>
<ul>
<li><b>Plan for about 12–14% of the order total</b> in Etsy fees on a typical £20–£50 order when you're not VAT-registered, before any Offsite Ads.</li>
<li><b>Postage is charged fees too.</b> Transaction, processing and regulatory fees all apply to the postage you charge.</li>
<li><b>Price Offsite Ads into your margin.</b> Once your shop passes US$10,000 in 365 days, you can't opt out.</li>
<li><b>Refunds return the processing fee proportionally.</b> Etsy credits it against the refunded amount.</li>
</ul>
<p>Selling from another country? Use the <a href="/en/etsy/">global Etsy fee calculator</a> with payment processing for 60+ bank countries.</p>
'''
    faq = [
     ("What are Etsy's fees for UK sellers in 2026?", f"A US$0.20 listing fee (about {GBP(LIST_GBP)}), a 6.5% transaction fee on item price plus postage and gift wrap, payment processing of 4% + £0.20 per order, a 0.48% regulatory operating fee since 22 June 2026, and 20% VAT on those fees if you haven't added a UK VAT number. Offsite Ads add 15% or 12% on orders they bring in, capped at US$100."),
     ("What is Etsy's regulatory operating fee in the UK?", "0.48% of the order total — item price, postage, gift wrap and personalisation — since 22 June 2026. It was 0.32% before."),
     ("Does Etsy charge VAT on fees in the UK?", "Yes, unless you add a valid VAT number in your Etsy account. Then Etsy stops charging VAT on its fees and your monthly invoice shows no VAT charged."),
     ("Is the transaction fee charged on postage?", "Yes. The 6.5% applies to the item price plus the postage and gift wrap you charge."),
     ("How much is the Etsy listing fee in pounds?", f"Etsy bills US$0.20, so the pound amount moves with the exchange rate. At the ECB rate on 26 October 2026 it was {GBP(LIST_GBP)}."),
     ("Can I opt out of Offsite Ads?", "Only while your shop has always made under US$10,000 in any 365 days. After that, Offsite Ads are mandatory and the fee is 12%."),
    ]
    return dict(title='Etsy Fee Calculator UK 2026: Fees, 0.48% Regulatory Fee & VAT',
                desc='Free Etsy UK fee and profit calculator: 6.5% transaction fee, 4% + £0.20 processing, 0.48% regulatory operating fee from 22 Jun 2026, VAT on Etsy fees and Offsite Ads, in pounds.',
                h1='Etsy Fee Calculator UK',
                lede='Every fee Etsy takes from a UK sale — listing, transaction, processing, the 0.48% regulatory operating fee and VAT on fees — and what you keep, in pounds.',
                body=body, faq=faq, toc=toc)

# ================================================================== Guides (en)
def g_sg():
    st = sg_stats()
    new = compute('tiktok-shop-sg', price=29.90, cost=9); old = compute('tiktok-shop-sg', period='old', price=29.90, cost=9)
    tab_o = compute('tiktok-shop-sg', sel='Phones & Tablets › Tablets', period='old', price=399, cost=300)
    tab_n = compute('tiktok-shop-sg', sel='Phones & Tablets › Tablets', price=399, cost=300)
    pn = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', price=499, cost=380); po = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', period='old', price=499, cost=380)
    return f'''
<p>On <b>1 September 2026</b> TikTok Shop Singapore replaced its category commission table with one flat rate: <b>9.810%</b> for standard sellers and <b>7.085%</b> for BXP sellers, GST included, with a <b>S$30 fee cap</b> on electronics, toys and collectibles. This guide shows who pays more, who pays less, and what it does to real orders. Every number links back to the <a href="/en/tiktok-shop/singapore/">TikTok Shop Singapore fee calculator</a>.</p>
<h2 id="what">What changed</h2>
<div class="tablewrap"><table><thead><tr><th></th><th>27 Jul – 31 Aug 2026</th><th>From 1 Sep 2026</th></tr></thead><tbody>
<tr><td>Standard commission</td><td>8.175% (6.54% in {st['old_non'].get(6.54, 0)} electronics &amp; appliance categories)</td><td>9.810% in all {st['n']:,} categories</td></tr>
<tr><td>BXP commission</td><td>7.085% (5.45% in the same group)</td><td>7.085% everywhere</td></tr>
<tr><td>Cap</td><td>S$50 in {st['cap_old']} categories</td><td>S$30 in {st['cap_new']} categories</td></tr>
</tbody></table></div>
<p>The 3.27% transaction fee and the BXP service fee (3.27% / 5.45%, capped at S$30 per item) did not change.</p>
<h2 id="everyday">Everyday products pay more</h2>
<p>{st['moved'].get((8.175, 9.81), 0):,} categories went from 8.175% to 9.81%, a 1.635-point rise for standard sellers. A S$29.90 serum (cost S$9) now pays {SGD(new['fee']['commission'])} commission instead of {SGD(old['fee']['commission'])}; profit falls from {SGD(old['profit'])} to {SGD(new['profit'])}. BXP sellers in these categories see no change at 7.085%.</p>
<h2 id="electronics">Electronics: higher rate, lower cap</h2>
<p>The {st['moved'].get((6.54, 9.81), 0)} categories that paid 6.54% jumped by 3.27 points, but most are now capped at S$30. Which effect wins depends on price:</p>
<ul>
<li>A S$399 tablet (previously 6.54%, uncapped): commission {SGD(tab_o['fee']['commission'])} → {SGD(tab_n['fee']['commission'])}, profit {SGD(tab_o['profit'])} → {SGD(tab_n['profit'])}.</li>
<li>A S$499 phone (previously 8.175%, S$50 cap): commission {SGD(po['fee']['commission'])} → {SGD(pn['fee']['commission'])}, profit {SGD(po['profit'])} → {SGD(pn['profit'])}.</li>
</ul>
<p>At 9.81% the cap binds from about {SGD(30 / 0.0981)}, so premium electronics are often cheaper to sell than before.</p>
<h2 id="bxp">Is BXP still worth it?</h2>
<p>BXP lowers commission by 2.725 points but adds a 3.27% or 5.45% service fee on every completed order (+1.09 during campaigns). Per order BXP costs more in almost every category, so it only pays if the vouchers bring extra sales. Toggle BXP in the calculator with your own price to see the gap.</p>
<h2 id="action">What to do now</h2>
<ul>
<li>Recheck prices on low-ticket items in beauty, fashion and food, where the whole 1.635-point rise lands.</li>
<li>For electronics above S$306, the cap makes bundles and premium models relatively cheaper to sell.</li>
<li>Cross-border sellers: TikTok's Global Seller notice uses different rates — check your own Seller Center.</li>
</ul>
'''

def g_th():
    st = th_stats()
    new = compute('tiktok-shop-th', price=299, cost=90); old = compute('tiktok-shop-th', period='old', price=299, cost=90)
    mall = compute('tiktok-shop-th', store='mall', price=299, cost=90); combo = compute('tiktok-shop-th', store='mall', tg={'combo': True}, price=299, cost=90)
    top = st['up'].most_common(1)[0]; topm = st['upm'].most_common(1)[0]
    return f'''
<p>TikTok Shop Thailand now takes four separate fees from each delivered order, and two of them changed in the middle of 2026. This guide lays out the full fee stack, what changed on 6 May and 5 July, and what it costs on real orders, using the <a href="/en/tiktok-shop/thailand/">TikTok Shop Thailand fee calculator</a>.</p>
<h2 id="stack">The four fees</h2>
<div class="tablewrap"><table><thead><tr><th>Fee</th><th>Rate (tax-inclusive)</th><th>Base</th><th>Refunded on return?</th></tr></thead><tbody>
<tr><td>Platform Commission Fee</td><td>By category: Marketplace mostly 10.70%, Mall mostly 13.91% (from 5 Jul 2026)</td><td>Item price − seller discount</td><td>Yes</td></tr>
<tr><td>Transaction Fee</td><td>3.21%</td><td>Customer payment + platform discount</td><td>No, after delivery</td></tr>
<tr><td>Commerce Growth Fee</td><td>6.96% Electronics / 8.03% other, max ฿199 per item</td><td>Item price − seller discount</td><td>No</td></tr>
<tr><td>Platform Infrastructure Fee</td><td>฿1.07 per order</td><td>Flat</td><td>No</td></tr>
</tbody></table></div>
<h2 id="july">The 5 July commission increase</h2>
<p>The most common Marketplace change was <b>+{top[0]:.2f} points</b> ({top[1]:,} sub-categories, mostly 8.56% → 10.70%); on Mall the most common change was +{topm[0]:.2f} points ({topm[1]:,} sub-categories, mostly 11.77% → 13.91%). On a ฿299 serum (cost ฿90) sold on Marketplace, total fees go from {THB(old['total'])} to {THB(new['total'])} and profit from {THB(old['profit'])} to {THB(new['profit'])}.</p>
<h2 id="cgf">The Commerce Growth Fee</h2>
<p>Since 6 May 2026 the CGF is 6.96% for Electronics and 8.03% for everything else (up from 5.89% / 6.96%), capped at ฿199 per item. It is waived for a new seller's first 30 days (up to ฿1,000 for sellers onboarded after 16 July 2026), reduced by 0.54 points for Marketplace sellers under ฿10,000 GMV in 30 days, and not charged to sellers who deliver only with their own fleet. For most sellers it is now the second-largest fee after commission.</p>
<h2 id="mall">Mall vs Mall Combo</h2>
<p>The same serum on Mall pays {pct(mall['rate']['commission'])} commission (fees {THB(mall['total'])}). In the Mall Combo Package — Mall Live Specials plus Brands Crazy Deals — it pays {pct(combo['rate']['commission'])} (fees {THB(combo['total'])}). The difference is {THB(mall['total'] - combo['total'])} per order, before any costs of the two programmes.</p>
<h2 id="action">What to do now</h2>
<ul>
<li>Price with all four fees: about 21.9% of the price for a typical non-Electronics Marketplace item, plus ฿1.07.</li>
<li>If you spend on GMV Max, check whether you clear the 3%-of-revenue threshold for the 1.07-point discount.</li>
<li>Remember that returns don't give back the transaction fee, CGF or infrastructure fee.</li>
</ul>
'''

def g_etsy_uk():
    a = compute('etsy-uk', price=25, buyerShip=4, cost=8, shipCost=3.6)
    s = compute('etsy-uk', price=12, buyerShip=3, cost=4, shipCost=2.7)
    l = compute('etsy-uk', price=60, buyerShip=5, cost=20, shipCost=4.5)
    def r(f, p): return f"<tr><td>{GBP(p)} + postage</td><td class='n'>{GBP(f['total'])}</td><td class='n'>{f['total'] / f['b']['net_ship'] * 100:.1f}%</td><td class='n'>{GBP(f['profit'])}</td></tr>"
    return f'''
<p>Etsy's fees for UK sellers changed twice in a way most fee calculators miss: the <b>regulatory operating fee</b> rose to <b>0.48%</b> on 22 June 2026, and Etsy adds <b>VAT</b> to its fees unless you've given it a VAT number. Here is the full list and what it costs, with the <a href="/en/etsy/uk/">Etsy UK fee calculator</a>.</p>
<h2 id="list">Every Etsy fee for a UK shop</h2>
<ul>
<li>Listing fee US$0.20 (about {GBP(LIST_GBP)} at the 26 Oct 2026 ECB rate).</li>
<li>Transaction fee 6.5% of item price + postage + gift wrap.</li>
<li>Payment processing 4% + £0.20 per order (UK bank account).</li>
<li>Regulatory operating fee 0.48% of the order total (0.32% until 21 June 2026).</li>
<li>VAT at 20% on those fees if you haven't added a VAT number.</li>
<li>Offsite Ads 15% or 12% on attributed orders, max US$100 per order.</li>
</ul>
<h2 id="vat">Who pays VAT on Etsy fees</h2>
<p>Etsy charges VAT on seller fees for UK sellers who haven't submitted a VAT number, and on Etsy Payments processing fees where required. Add a valid VAT number in your account and Etsy stops charging it; your monthly invoice then states that no VAT was charged. For a seller below the VAT threshold, this VAT is simply a cost — on a £25 order it adds {GBP(a['fee']['feevat'])}.</p>
<h2 id="real">What it costs on real orders</h2>
<div class="tablewrap"><table><thead><tr><th>Order</th><th class="n">Etsy fees</th><th class="n">% of order</th><th class="n">Profit</th></tr></thead><tbody>
{r(s, 12)}{r(a, 25)}{r(l, 60)}
</tbody></table></div>
<p>Not VAT-registered, no Offsite Ads; product costs £4 / £8 / £20 and postage labels £2.70 / £3.60 / £4.50 against £3 / £4 / £5 charged. Smaller orders lose a bigger share to the fixed £0.20 processing fee and the listing fee.</p>
<h2 id="action">How to price for it</h2>
<ul>
<li>Budget roughly 12–14% of the order total for Etsy fees, more on cheap items.</li>
<li>Build Offsite Ads into the price of bestsellers: a 15% fee plus VAT on it can halve the margin on that order.</li>
<li>If you become VAT-registered, add your VAT number to Etsy promptly so fees stop carrying VAT.</li>
</ul>
'''

GUIDES_NEW = [
 dict(lang='en', slug='tiktok-shop-singapore-commission-september-2026', short='Singapore commission (1 Sep 2026)',
      title='TikTok Shop Singapore Commission Change on 1 September 2026: 9.81% Flat Rate and S$30 Cap',
      desc='TikTok Shop Singapore moved to a flat 9.81% (7.085% BXP) commission on 1 Sep 2026 with a S$30 cap on electronics. Who pays more, who pays less, with worked examples.',
      market='tiktok-shop-sg', cov='cov-ink', fig='9.81%'),
 dict(lang='en', slug='tiktok-shop-thailand-seller-fees-2026', short='Thailand seller fees 2026',
      title='TikTok Shop Thailand Seller Fees in 2026: Commission, 3.21% Transaction Fee, CGF and ฿1.07 Fee',
      desc='The four fees on every TikTok Shop Thailand order, the 5 July 2026 commission increase, the Commerce Growth Fee and Mall Combo — with worked examples in baht.',
      market='tiktok-shop-th', cov='cov-amber', fig='4 fees'),
 dict(lang='en', slug='etsy-uk-fees-vat-regulatory-fee', short='Etsy UK fees & VAT',
      title='Etsy Fees for UK Sellers in 2026: 0.48% Regulatory Fee, VAT on Fees and Real Examples',
      desc='Every Etsy fee for a UK shop: 6.5% transaction, 4% + £0.20 processing, the 0.48% regulatory operating fee from 22 June 2026 and VAT on Etsy fees, with worked examples.',
      market='etsy-uk', cov='cov-green', fig='0.48%'),
]
GUIDE_BODY_NEW = {GUIDES_NEW[0]['slug']: g_sg, GUIDES_NEW[1]['slug']: g_th, GUIDES_NEW[2]['slug']: g_etsy_uk}
GUIDE_SOURCES_NEW = {GUIDES_NEW[0]['slug']: MARKETS['tiktok-shop-sg']['sources'], GUIDES_NEW[1]['slug']: MARKETS['tiktok-shop-th']['sources'],
                     GUIDES_NEW[2]['slug']: MARKETS['etsy-uk']['sources']}
PAGE_FN_NEW = {('tiktok-shop-sg', 'en'): sg_page, ('tiktok-shop-th', 'en'): th_page, ('etsy-uk', 'en'): etsy_uk_page}
