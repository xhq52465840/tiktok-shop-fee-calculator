"""Shopee + Lazada page copy. Numbers from rate files or markets.compute()."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

SH_MY = MARKETS['shopee-my']['selector']['options']
SH_SG = MARKETS['shopee-sg']['selector']['options']
LZ_MY = MARKETS['lazada-my']['selector']['options']
RM = lambda v: money(v, 'MYR'); SGD = lambda v: money(v, 'SGD')
LBL = dict(commission='Commission', tx='Transaction fee', psf='Platform Support Fee',
           pxp_svc='PXP service fee', lz_pay='Payment / other fee', aff='Affiliate commission')

def _ex(f, cur, labels, extra_top=()):
    M = lambda v: money(v, cur)
    rows = list(extra_top)
    for k, r, a in f['rows']:
        if k in ('psf',) or (k == 'lz_pay' and a == 0):
            rows.append((labels.get(k, k), '−' + M(a)))
        else:
            rows.append((f"{labels.get(k, k)} ({pct(r)})", '−' + M(a)))
    rows.append(('Total fees', M(f['total']), True))
    rows.append(('Payout', M(f['payout']), True))
    return rows

def shopee_my_page():
    sk = 'Beauty › Skincare'
    r = next(o for o in SH_MY if o['n'] == sk)['r']
    old = compute('shopee-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('shopee-my', sel=sk, period='new', price=39.90, cost=12)
    scp = compute('shopee-my', sel=sk, period='new', tg={'scp': True}, price=39.90, cost=12)
    cam = compute('shopee-my', sel='Cameras & Drones › Cameras', period='old', store='mall', tg={'scp': True},
                  price=100, sellerDisc=30, cost=40)
    sample = ['Beauty › Skincare', 'Beauty › Makeup', 'Mobile & Gadgets › Mobile Phones',
              'Cameras & Drones › Cameras', 'Women Clothes › Dresses', 'Men Shoes › Sneakers',
              'Mom & Baby › Diapering & Potty', 'Home & Living › Furniture', 'Pets › Pet Food',
              'Books & Magazines › Books']
    def rr(o, k):
        v = o['r'].get(k); return pct(v) if v is not None else '–'
    def trow(n):
        o = next(x for x in SH_MY if x['n'] == n)
        return (f"<tr><td>{n}</td><td class='n'>{rr(o,'old.mp.non')}</td><td class='n'><b>{rr(o,'new.mp.non')}</b></td>"
                f"<td class='n'>{rr(o,'new.mp.scp')}</td><td class='n'><b>{rr(o,'new.mall.non')}</b></td></tr>")
    full = ''.join(
        f"<tr><td>{o['n']}</td>" + ''.join(f"<td class='n'>{rr(o,k)}</td>" for k in
            ['old.mp.scp','old.mp.non','old.mall.scp','old.mall.non','new.mp.scp','new.mp.non','new.mall.scp','new.mall.non']) + '</tr>'
        for o in SH_MY)
    toc = [('how', 'How Shopee Malaysia fees work'), ('examples', 'Worked examples'),
           ('changes', 'What changed in 2026'), ('rates', 'Commission rates by category'),
           ('tips', 'Protecting your margin'), ('faq', 'FAQ'), ('sources', 'Sources')]
    body = f'''
<h2 id="how">How Shopee Malaysia fees work</h2>
<p>On a completed local order, Shopee Malaysia deducts a category commission, a transaction fee and a Platform Support Fee. Commission depends on the product category, on Marketplace vs Mall, and on whether you are in the Cashback Programme (SCP). The commission percentages we load are <b>SST-inclusive</b> (official table × 1.08), matching how Shopee's own worked examples convert a 9.0% list rate into 9.72%.</p>
<h3>1. Commission fee</h3>
<p>Commission = (item price − seller-funded discount) × category rate. Platform-funded vouchers are not subtracted from the base. Marketplace and Mall publish separate tables; SCP sellers get the lower column. From 14 August 2026 the Marketplace and Mall tables were updated again.</p>
<h3>2. Transaction fee</h3>
<p>3.78% (after SST) of the final order amount paid by the buyer, including shipping, rounded to 2 decimal places. Deducted automatically on completed orders.</p>
<h3>3. Platform Support Fee</h3>
<p>RM0.54 (after SST) on every completed order, regardless of order value.</p>
<h3>4. New-seller waiver</h3>
<p>From 1 August 2026, Marketplace commission applies only after you have listed your first product for more than 120 days <b>or</b> have more than 200 completed orders, whichever comes first. Use the "New seller" toggle to model the waiver period.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: RM39.90 skincare serum, Marketplace, non-SCP</h4>
<p>Skincare commission for a non-SCP Marketplace seller stays at {pct(r['new.mp.non'])} after 14 August (SST-inclusive). Cost RM12.</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">Before 14 Aug</th><th class="n">From 14 Aug</th></tr></thead><tbody>
<tr><td>Commission</td><td class="n">−{RM(old['fee']['commission'])}</td><td class="n">−{RM(new['fee']['commission'])}</td></tr>
<tr><td>Transaction fee (3.78%)</td><td class="n">−{RM(old['fee']['tx'])}</td><td class="n">−{RM(new['fee']['tx'])}</td></tr>
<tr><td>Platform Support Fee</td><td class="n">−{RM(old['fee']['psf'])}</td><td class="n">−{RM(new['fee']['psf'])}</td></tr>
<tr><td><b>Payout</b></td><td class="n"><b>{RM(old['payout'])}</b></td><td class="n"><b>{RM(new['payout'])}</b></td></tr>
<tr><td><b>Profit after RM12 cost</b></td><td class="n"><b>{RM(old['profit'])}</b></td><td class="n"><b>{RM(new['profit'])}</b></td></tr>
</tbody></table></div></div>
<div class="example"><h4>Example 2: same serum as an SCP seller</h4>
<p>SCP drops the new skincare commission to {pct(r['new.mp.scp'])}.</p>
{ex_table(_ex(scp, 'MYR', LBL))}
<p>Profit {RM(scp['profit'])} ({scp['margin']:.1f}% margin) vs {RM(new['profit'])} outside SCP.</p></div>
<div class="example"><h4>Example 3: Shopee's Mall cameras scenario</h4>
<p>Mall SCP cameras, RM100 after a RM10 promo with a RM30 seller voucher (commission base RM70). Official example: 9.0% list × 8% SST = 9.72% → RM6.80. The calculator matches: commission {RM(cam['fee']['commission'])}.</p>
{ex_table(_ex(cam, 'MYR', LBL, extra_top=[('Item subtotal after your discount', RM(cam['b']['net']))]))}</div>

<h2 id="changes">What changed in 2026</h2>
<div class="tablewrap"><table><thead><tr><th>Effective</th><th>Change</th></tr></thead><tbody>
<tr><td>21 May 2026</td><td>Waived or reduced commission on 100+ essential categories.</td></tr>
<tr><td>1 Aug 2026</td><td>Marketplace commission starts after 120 days or 200 completed orders; more essentials added to reduced rates.</td></tr>
<tr><td>14 Aug 2026</td><td>New Marketplace and Mall commission tables (SCP / non-SCP columns).</td></tr>
</tbody></table></div>

<h2 id="rates">Commission rates by category</h2>
<p>A selection of popular sub-categories. All rates below are <b>SST-inclusive</b>. MP = Marketplace.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Sub-category</th><th class="n">MP non-SCP before</th><th class="n">MP non-SCP from 14 Aug</th><th class="n">MP SCP from 14 Aug</th><th class="n">Mall non-SCP from 14 Aug</th></tr></thead><tbody>
{''.join(trow(n) for n in sample if any(o['n']==n for o in SH_MY))}</tbody></table></div>
<details class="adv"><summary>Show all {len(SH_MY)} sub-categories</summary>
<p style="margin-top:12px"><input id="sf-filter" class="search" type="search" placeholder="Filter, e.g. skincare" aria-label="Filter categories"></p>
<div class="tablewrap tall"><table class="tbl" id="sf-rates"><thead><tr><th>Category › Sub-category</th>
<th class="n">MP SCP (old)</th><th class="n">MP non-SCP (old)</th><th class="n">Mall SCP (old)</th><th class="n">Mall non-SCP (old)</th>
<th class="n">MP SCP (new)</th><th class="n">MP non-SCP (new)</th><th class="n">Mall SCP (new)</th><th class="n">Mall non-SCP (new)</th>
</tr></thead><tbody>{full}</tbody></table></div></details>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Reprice against the 14 August table.</b> SCP and non-SCP columns moved independently; check your top SKUs with both toggles.</li>
<li><b>Bundle low-priced items.</b> The RM0.54 Platform Support Fee is per order, not per item.</li>
<li><b>Confirm Mall vs Marketplace.</b> Mall commissions are several points higher in most categories.</li>
<li><b>Edit the rate if Seller Center disagrees.</b> Category assignment can differ from the public table; every rate field is editable.</li>
</ul>
'''
    faq = [
     ("What fees does Shopee Malaysia charge local sellers?",
      "Category commission (Marketplace or Mall, SCP or non-SCP), a 3.78% transaction fee on the buyer-paid amount including shipping, and a RM0.54 Platform Support Fee per completed order. Optional programme and pre-order fees may also apply."),
     ("Are commission rates inclusive of SST?",
      "Shopee publishes list rates that are subject to 8% SST. This calculator stores SST-inclusive rates (list × 1.08), matching Shopee's own worked examples (e.g. 9.0% → 9.72%)."),
     ("When did the August 2026 commission change start?",
      "00:00 on 14 August 2026 for both Marketplace and Mall tables. Orders before that date follow the earlier columns."),
     ("Who gets the new-seller commission waiver?",
      "From 1 August 2026, Marketplace commission applies after more than 120 days since first listing or more than 200 completed orders, whichever comes first."),
     ("What is the Cashback Programme (SCP)?",
      "Sellers on Shopee's Cashback Programme pay the lower SCP commission column. Programme rules and any separate service fees are in Seller Center."),
    ]
    return dict(title='Shopee Malaysia Fee Calculator 2026 (Commission, 3.78% TX, RM0.54 PSF)',
                desc='Free Shopee Malaysia fee and profit calculator with Marketplace and Mall commission tables from 14 Aug 2026 (SST-inclusive), 3.78% transaction fee and RM0.54 Platform Support Fee.',
                h1='Shopee Malaysia Fee Calculator',
                lede='See exactly what Shopee Malaysia takes on each order — Marketplace or Mall, SCP or non-SCP — using the official 14 August 2026 commission tables, 3.78% transaction fee and RM0.54 Platform Support Fee.',
                body=body, faq=faq, toc=toc)

def shopee_sg_page():
    ph = next(o for o in SH_SG if 'Mobile Phones' in o['n'])
    base = compute('shopee-sg', sel=ph['n'], price=29.90, cost=10)
    pxp = compute('shopee-sg', sel=ph['n'], tg={'pxp': True}, rates={'pxp_svc': 5.45}, price=29.90, cost=10)
    big = compute('shopee-sg', sel=ph['n'], price=500, cost=350)
    toc = [('how', 'How Shopee Singapore fees work'), ('examples', 'Worked examples'),
           ('rates', 'Commission rates by category'), ('tips', 'Protecting your margin'),
           ('faq', 'FAQ'), ('sources', 'Sources')]
    rows = ''.join(
        f"<tr><td>{o['n']}</td><td class='n'>{pct(o['r']['nonmall_pxp'])}</td><td class='n'><b>{pct(o['r']['nonmall'])}</b></td>"
        f"<td class='n'>{pct(o['r']['mall_pxp'])}</td><td class='n'><b>{pct(o['r']['mall'])}</b></td>"
        f"<td class='n'>{('S$' + str(o['r']['cap_nonmall'])) if o['r'].get('cap_nonmall') else '–'}</td>"
        f"<td class='n'>{('S$' + str(o['r']['cap_mall'])) if o['r'].get('cap_mall') else '–'}</td></tr>"
        for o in SH_SG)
    body = f'''
<h2 id="how">How Shopee Singapore fees work</h2>
<p>Local Shopee SG sellers pay a GST-inclusive category commission and a GST-inclusive transaction fee on every successful order. Sellers in the Promo Xtra Programme (PXP) get preferential commission rates and pay a separate PXP service fee.</p>
<h3>1. Commission fee</h3>
<p>GST-inclusive percentage of the product price after seller-sponsored promotions. Mall and non-Mall (Marketplace) have different rates; PXP sellers use the preferential column. Selected electronics and fashion categories have per-item caps (e.g. S$60 non-Mall / S$120 Mall for many electronics). From 28 August 2026, selected food, home-care, books and musical-instrument categories received a 1 percentage-point reduction.</p>
<h3>2. Transaction fee</h3>
<p>3.27% (GST-inclusive) of the final payment amount, including buyer-paid shipping. SPayLater can range from 3.27% to 6.54% depending on the buyer's repayment period — the calculator defaults to 3.27%; edit the rate for longer tenures.</p>
<h3>3. PXP service fee</h3>
<p>Charged only if you join Promo Xtra. The percentage varies by category (Shopee's FAQ example uses 5.45% of gross settlement). Enter your category rate under fee rates — we do not invent a category table we have not verified.</p>
<h3>4. New-seller waiver</h3>
<p>Eligible new Mall and non-Mall sellers get 0% commission for the first 120 days of seller activity. PXP service fees have a separate 30-day waiver for new-to-Shopee sellers who join PXP.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: S$29.90 phone accessory, non-Mall, not in PXP</h4>
<p>Using the "{ph['n']}" row at {pct(ph['r']['nonmall'])} non-PXP, cost S$10.</p>
{ex_table(_ex(base, 'SGD', LBL))}
<p>Profit {SGD(base['profit'])} ({base['margin']:.1f}% margin).</p></div>
<div class="example"><h4>Example 2: same item in PXP with a 5.45% service fee</h4>
<p>Preferential commission {pct(ph['r']['nonmall_pxp'])} plus a 5.45% PXP service fee (FAQ example rate).</p>
{ex_table(_ex(pxp, 'SGD', LBL))}
<p>Profit {SGD(pxp['profit'])}. Whether PXP pays off depends on the extra orders the programme brings in.</p></div>
<div class="example"><h4>Example 3: S$500 phone, non-Mall — commission cap</h4>
<p>At {pct(ph['r']['nonmall'])} the uncapped commission would be over S$60; the published non-Mall cap is S$60 per item. Calculator commission: {SGD(big['fee']['commission'])}.</p></div>

<h2 id="rates">Commission rates by category</h2>
<p>GST-inclusive rates from the Shopee SG table in force from 28 August 2026. Caps shown where Shopee publishes them.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Category</th><th class="n">Non-Mall PXP</th><th class="n">Non-Mall</th><th class="n">Mall PXP</th><th class="n">Mall</th><th class="n">Cap non-Mall</th><th class="n">Cap Mall</th></tr></thead><tbody>{rows}</tbody></table></div>

<h2 id="tips">Protecting your margin</h2>
<ul>
<li><b>Watch the per-item caps on electronics.</b> High-ticket phones and appliances often hit the S$60 / S$120 caps, which helps margin versus an uncapped percentage.</li>
<li><b>Model SPayLater separately</b> if a large share of buyers use longer tenures (up to 6.54%).</li>
<li><b>Enter your real PXP service fee</b> from Seller Center before deciding whether the preferential commission is worth it.</li>
</ul>
'''
    faq = [
     ("What is the Shopee Singapore transaction fee?",
      "3.27% GST-inclusive of the final payment amount (including buyer-paid shipping). SPayLater can be higher, up to 6.54%."),
     ("Do commission rates include GST?",
      "Yes. Shopee SG publishes commission and transaction fees as GST-inclusive."),
     ("What changed on 28 August 2026?",
      "Shopee reduced commission by 1 percentage point for selected Food & Beverages, Home & Living (toilet paper), books and musical instruments."),
     ("How does the 120-day new-seller waiver work?",
      "Eligible new Mall and non-Mall sellers pay 0% commission for the first 120 days of seller activity. Service and transaction fees still apply."),
     ("Where do PXP service fee rates come from?",
      "They vary by category on a separate Shopee page. Enter the rate shown in your Seller Center; the FAQ example of 5.45% is only a placeholder."),
    ]
    return dict(title='Shopee Singapore Fee Calculator 2026 (GST-inclusive Commission & 3.27% TX)',
                desc='Free Shopee Singapore fee and profit calculator with GST-inclusive Mall and non-Mall commission tables from 28 Aug 2026, 3.27% transaction fee, PXP toggle and per-item caps.',
                h1='Shopee Singapore Fee Calculator',
                lede='GST-inclusive Mall and non-Mall commission from 28 August 2026, 3.27% transaction fee, PXP preferential rates and published per-item caps — so you can see payout and margin before you list.',
                body=body, faq=faq, toc=toc)

def lazada_my_page():
    g = LZ_MY[0]
    base = compute('lazada-my', sel=g['n'], price=49.90, cost=15)
    mall = compute('lazada-my', sel=g['n'], store='mall', price=49.90, cost=15)
    toc = [('how', 'How Lazada Malaysia fees work'), ('examples', 'Worked examples'),
           ('rates', 'Cluster commission ranges'), ('gaps', 'What we could not verify'),
           ('faq', 'FAQ'), ('sources', 'Sources')]
    rows = ''.join(
        f"<tr><td>{o['n']}</td><td class='n'>{pct(o['r']['mp'])} – {pct(o['r']['mp_hi'])}</td>"
        f"<td class='n'>{pct(o['r']['mall'])} – {pct(o['r']['mall_hi'])}</td></tr>"
        for o in LZ_MY)
    body = f'''
<h2 id="how">How Lazada Malaysia fees work</h2>
<p>Lazada Malaysia charges a category commission on delivered orders. From 14 August 2026 the Marketplace and LazMall tables were revised. Published rates are <b>subject to 8% SST</b>; this calculator stores SST-inclusive floors (list × 1.08) as the default and keeps the cluster ceiling in the rate table so you can edit up.</p>
<p>Lazada's public help centre serves the commission page as a JavaScript app that returned no readable table to our scraper. The cluster ranges below come from a dated BigSeller reprint of Lazada's official 14 August 2026 Marketplace and LazMall tables, cross-checked against the Seller Center path <b>Settings → Commission</b>. Every rate field is editable — paste the exact % from your Seller Center when you have it.</p>
<h3>1. Commission fee</h3>
<p>Percentage of item price after seller-funded discounts, by product cluster (General Merchandise, FMCG, Fashion, Electronics, Digital Goods). LazMall is higher than Marketplace in most clusters. New sellers typically get a 120-day commission-free window — use the toggle.</p>
<h3>2. Payment and other fees</h3>
<p>Lazada may charge payment or campaign-related fees on top of commission. We have not verified a single published payment-fee percentage for all MY sellers, so the field starts empty and is editable.</p>

<h2 id="examples">Worked examples</h2>
<div class="example"><h4>Example 1: RM49.90 general merchandise, Marketplace floor</h4>
<p>Using the SST-inclusive Marketplace floor for General Merchandise ({pct(g['r']['mp'])}), cost RM15.</p>
{ex_table(_ex(base, 'MYR', LBL))}
<p>Profit {RM(base['profit'])}. Edit the commission up toward {pct(g['r']['mp_hi'])} if your sub-category sits at the top of the cluster.</p></div>
<div class="example"><h4>Example 2: same item on LazMall</h4>
<p>LazMall floor {pct(g['r']['mall'])}.</p>
{ex_table(_ex(mall, 'MYR', LBL))}
<p>Profit {RM(mall['profit'])}.</p></div>

<h2 id="rates">Cluster commission ranges (from 14 Aug 2026, SST-inclusive)</h2>
<p>Defaults in the calculator use the <b>floor</b> of each range. Ceilings are shown so you can edit upward to match Seller Center.</p>
<div class="tablewrap"><table class="tbl"><thead><tr><th>Cluster</th><th class="n">Marketplace</th><th class="n">LazMall</th></tr></thead><tbody>{rows}</tbody></table></div>

<h2 id="gaps">What we could not verify</h2>
<ul>
<li><b>Per-sub-category rates</b> inside each cluster — only cluster ranges are published in the secondary reprint we could read.</li>
<li><b>A single official payment-fee %</b> for all MY sellers — enter yours from the fee statement.</li>
<li><b>Live scrape of sellercenter.lazada.com.my</b> — the commission FAQ is a client-rendered page that returned an empty body to automation.</li>
</ul>
<p>When Lazada publishes a stable public HTML or PDF table, we will replace cluster floors with per-category rows.</p>
'''
    faq = [
     ("Where do these Lazada MY rates come from?",
      "Cluster ranges effective 14 August 2026, subject to 8% SST, as reprinted by BigSeller from Lazada's Marketplace and LazMall commission tables. Confirm the exact % under Seller Center → Settings → Commission."),
     ("Why only cluster ranges, not every sub-category?",
      "Lazada's public help page did not expose a readable per-category table to our scraper. We refuse to invent rows, so the calculator uses verified cluster floors with editable rates."),
     ("Are rates inclusive of SST?",
      "Lazada labels the tables 'subject to 8% SST'. We multiply by 1.08 so the default matches an all-in deduction; edit if your statement shows the ex-SST figure."),
     ("Is there a new-seller waiver?",
      "Lazada commonly offers about 120 commission-free days for new sellers. Use the toggle; confirm the exact window in your onboarding email or Seller Center."),
    ]
    return dict(title='Lazada Malaysia Fee Calculator 2026 (Commission from 14 Aug)',
                desc='Free Lazada Malaysia fee and profit calculator with Marketplace and LazMall cluster commission ranges from 14 August 2026 (SST-inclusive floors), editable to match Seller Center.',
                h1='Lazada Malaysia Fee Calculator',
                lede='Marketplace and LazMall cluster commission floors from 14 August 2026 (SST-inclusive), editable to the exact % in your Seller Center — plus payout and margin on every order.',
                body=body, faq=faq, toc=toc)

GUIDES_SEA = [
 dict(lang='en', slug='shopee-malaysia-fees-august-2026', short='Shopee MY fees (14 Aug 2026)',
      title='Shopee Malaysia Seller Fees after 14 August 2026: Commission, 3.78% TX and RM0.54 PSF',
      desc='How Shopee Malaysia Marketplace and Mall commission changed on 14 August 2026, how SST applies, and worked examples with the 3.78% transaction fee and RM0.54 Platform Support Fee.',
      market='shopee-my', cov='cov-ink', fig='Shopee MY'),
 dict(lang='en', slug='shopee-singapore-commission-gst', short='Shopee SG GST-inclusive fees',
      title='Shopee Singapore Commission and Transaction Fees (GST-inclusive), Explained',
      desc='Shopee SG Mall vs non-Mall commission from 28 August 2026, the 3.27% GST-inclusive transaction fee, PXP preferential rates and per-item caps.',
      market='shopee-sg', cov='cov-ink', fig='Shopee SG'),
]

def g_shopee_my():
    return shopee_my_page()['body']  # reuse page body sections via guide wrapper in build — provide focused guide
def g_shopee_sg():
    return shopee_sg_page()['body']

# Slimmer guide bodies: point at calculator, expand changes
def g_shopee_my_guide():
    sk='Beauty › Skincare'; r=next(o for o in SH_MY if o['n']==sk)['r']
    new=compute('shopee-my', sel=sk, period='new', price=39.90, cost=12)
    old=compute('shopee-my', sel=sk, period='old', price=39.90, cost=12)
    return f'''
<p>Shopee Malaysia updated Marketplace and Mall commission on <b>14 August 2026</b>. This guide summarises what changed and links every number to the <a href="../../shopee/malaysia/">Shopee Malaysia fee calculator</a>.</p>
<h2 id="fees">The three fees on a normal order</h2>
<ul>
<li><b>Commission</b> — category × Marketplace/Mall × SCP/non-SCP. We store SST-inclusive rates (official list × 1.08).</li>
<li><b>Transaction fee</b> — 3.78% after SST on the buyer-paid amount including shipping.</li>
<li><b>Platform Support Fee</b> — RM0.54 after SST per completed order.</li>
</ul>
<h2 id="aug">What the 14 August table did to skincare</h2>
<p>Beauty › Skincare, Marketplace non-SCP: {pct(r['old.mp.non'])} before → {pct(r['new.mp.non'])} from 14 August (SST-inclusive). On a RM39.90 serum with RM12 cost, profit moves from {RM(old['profit'])} to {RM(new['profit'])}.</p>
<p>Open the calculator, switch the rate period, and compare your own top SKUs before the next campaign.</p>
<h2 id="scp">SCP vs non-SCP</h2>
<p>Cashback Programme sellers use the SCP column (lower commission). Confirm you are actually enrolled before pricing on that column.</p>
'''

def g_shopee_sg_guide():
    return f'''
<p>Shopee Singapore publishes <b>GST-inclusive</b> commission and a <b>3.27% GST-inclusive</b> transaction fee. Preferential PXP commission sits beside a separate PXP service fee. Use the <a href="../../shopee/singapore/">Shopee Singapore fee calculator</a> for payout and margin.</p>
<h2 id="aug">28 August 2026 reduction</h2>
<p>Selected Food &amp; Beverages, toilet paper, books and musical instruments dropped by 1 percentage point. Electronics keep per-item caps (commonly S$60 non-Mall / S$120 Mall).</p>
<h2 id="pxp">PXP in one line</h2>
<p>Lower commission column + category service fee (enter yours; FAQ example 5.45%). Run both sides in the calculator before joining.</p>
'''

GUIDE_BODY_SEA = {
 'shopee-malaysia-fees-august-2026': g_shopee_my_guide,
 'shopee-singapore-commission-gst': g_shopee_sg_guide,
}
GUIDE_SOURCES_SEA = {
 'shopee-malaysia-fees-august-2026': MARKETS['shopee-my']['sources'],
 'shopee-singapore-commission-gst': MARKETS['shopee-sg']['sources'],
}
PAGE_FN_SEA = {
 ('shopee-my', 'en'): shopee_my_page,
 ('shopee-sg', 'en'): shopee_sg_page,
 ('lazada-my', 'en'): lazada_my_page,
}
