"""Guide: Seller Growth Fees compared across TikTok Shop, Shopee and Lazada (MY/PH/SG/TH). Numbers from markets.compute()."""
from markets import MARKETS, compute
from site_helpers import money

PHP = lambda v: money(v, 'PHP'); THB = lambda v: money(v, 'THB')
SPH = MARKETS['shopee-ph']['selector']['options']
TTH = MARKETS['tiktok-shop-th']['selector']['options']

def _gi(opts, g): return next(i for i, o in enumerate(opts) if o.get('g') == g)

def g_growth_compare():
    tt_f = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=499)['fee']['growth']
    sh_f = compute('shopee-ph', sel=_gi(SPH, 'Women Clothes'), price=499)['fee']['sgsf']
    sh_h = compute('shopee-ph', sel=_gi(SPH, 'Home & Living'), price=499)['fee']['sgsf']
    th_s = compute('tiktok-shop-th', price=299)['fee']['cgf']
    th_e_i = next(i for i, o in enumerate(TTH) if o.get('r', {}).get('cgf') == 6.96)
    th_e = compute('tiktok-shop-th', sel=th_e_i, price=5000)['fee']['cgf']
    return f'''
<p>TikTok Shop and Shopee now both charge a per-order “growth” fee in some Southeast Asian markets, on top of commission and the transaction fee. The names are similar but the rates, categories and caps are not. This page compares them market by market, using each platform’s own seller centre pages, and links to the calculator that includes each fee.</p>
<h2 id="table">Growth fees by market</h2>
<div class="tablewrap"><table><thead><tr><th>Market</th><th>TikTok Shop</th><th>Shopee</th></tr></thead><tbody>
<tr><td><b>Philippines</b></td><td><b>Seller Growth Fee</b>: 1% for Electronics, Grocery and Large Appliances; 1.5% for Beauty &amp; Personal Care, Fashion, Mom &amp; Baby, Health and Lifestyle (except Large Appliances). VAT inclusive, every successful order.</td><td><b>Seller Growth Support Fee</b>: 1.00% or 1.50% of the item price after discounts, by category (list updated 22 October 2026). New sellers are exempt for their first 90 days.</td></tr>
<tr><td><b>Thailand</b></td><td><b>Commerce Growth Fee</b>: 6.96% for Electronics, 8.03% for everything else, capped at ฿199 per item, tax inclusive, from 6 May 2026. Small Marketplace sellers (under ฿10,000 GMV in the last 30 days) pay 0.54% less.</td><td>No separate growth fee. Shopee raised its sale transaction fee (commission) by 1 or 2 points before VAT on 4 August 2026 and says the increase supports seller growth.</td></tr>
<tr><td><b>Malaysia</b></td><td>No growth fee. Fees are commission, the 3.78% transaction fee, the RM0.54 Platform Support Fee and, for Bonus Extra Program sellers, a 4.86% BXP fee.</td><td>No growth fee. Fees for local sellers are commission, the 3.78% transaction fee and the RM0.54 Platform Support Fee.</td></tr>
<tr><td><b>Singapore</b></td><td>No growth fee. TikTok lists commission and the 3.27% transaction fee; the Bonus Extra Program fee applies only if you join.</td><td>No growth fee. Shopee lists commission, transaction, service and shipping fees; service fees apply to programmes you join.</td></tr>
</tbody></table></div>
<p><b>Lazada is not in the table.</b> The secondary sources we checked list no Lazada growth fee in Malaysia, the Philippines, Singapore or Thailand, but Lazada’s full fee schedules for these markets sit behind Seller Center login or are published as images, so we could not verify them from an official page. We will add Lazada once we can.</p>
<h2 id="ph">Philippines: two fees with the same idea, different categories</h2>
<p>Both platforms charge 1% or 1.5%, but they sort categories differently. On TikTok Shop fashion pays 1.5%; on Shopee, women’s clothes pay 1.00%. On a ₱499 top the TikTok Shop growth fee is {PHP(tt_f)} and Shopee’s is {PHP(sh_f)} (Shopee rounds fees to the peso). Home items pay 1.5% on both: {PHP(sh_h)} on Shopee for a ₱499 home item.</p>
<p>AMZ123 reported on 27 October 2026 that TikTok Shop Philippines has announced a change from 1 November 2026: the growth fee is charged on every successful order for all sellers, and Lifestyle products (except Large Appliances) go from 1% to 1.5%. See our <a href="../tiktok-shop-philippines-seller-growth-fee/">TikTok Shop Philippines Seller Growth Fee guide</a> for the details.</p>
<h2 id="th">Thailand: the biggest growth fee by far</h2>
<p>TikTok Shop Thailand’s Commerce Growth Fee is several times larger than the Philippine fees. A ฿299 skincare item pays {THB(th_s)} (8.03%). The ฿199 cap matters on expensive items: a ฿5,000 electronics item would pay ฿348 at 6.96%, but the cap limits it to {THB(th_e)}. New sellers do not pay it for their first 30 days (capped at ฿1,000 for sellers who joined after 16 July 2026), and sellers who ship only with their own fleet are not charged.</p>
<h2 id="calc">Calculators that include these fees</h2>
<ul>
<li><a href="../../tiktok-shop/philippines/">TikTok Shop Philippines fee calculator</a> (Seller Growth Fee by category)</li>
<li><a href="../../shopee/philippines/">Shopee Philippines fee calculator</a> (Seller Growth Support Fee by category)</li>
<li><a href="../../tiktok-shop/thailand/">TikTok Shop Thailand fee calculator</a> (Commerce Growth Fee with the ฿199 cap and small-seller discount)</li>
<li><a href="../../shopee/thailand/">Shopee Thailand fee calculator</a>, <a href="../../tiktok-shop/malaysia/">TikTok Shop Malaysia</a>, <a href="../../shopee/malaysia/">Shopee Malaysia</a>, <a href="../../tiktok-shop/singapore/">TikTok Shop Singapore</a> and <a href="../../shopee/singapore/">Shopee Singapore</a></li>
</ul>
<h2 id="tips">What to do about it</h2>
<ul>
<li><b>Check your category on each platform.</b> The same product can pay 1% on one platform and 1.5% on the other.</li>
<li><b>Price for the fee, not around it.</b> None of these fees has a general exemption beyond the new-seller windows, so build them into your price.</li>
<li><b>Watch the cap in Thailand.</b> Above about ฿2,480 per item, TikTok Shop Thailand’s fee stops growing.</li>
</ul>
'''

GUIDES_GROWTH = [
 dict(lang='en', slug='seller-growth-fee-tiktok-shopee-lazada', short='Growth fees compared: TikTok Shop vs Shopee',
      title='TikTok Shop vs Shopee vs Lazada Seller Growth Fees 2026: Malaysia, Philippines, Singapore, Thailand',
      desc='Which platforms charge a seller growth fee in Southeast Asia, at what rate: TikTok Shop’s Seller Growth Fee and Commerce Growth Fee, Shopee’s Seller Growth Support Fee, and what Lazada charges, by country.',
      market='tiktok-shop-ph', cov='cov-amber', fig='1%–8.03%'),
]
GUIDE_BODY_GROWTH = {'seller-growth-fee-tiktok-shopee-lazada': g_growth_compare}
GUIDE_SOURCES_GROWTH = {'seller-growth-fee-tiktok-shopee-lazada': [
 MARKETS['tiktok-shop-ph']['sources'][0],
 MARKETS['tiktok-shop-ph']['sources'][-1],
 ('Commerce Growth Fee — TikTok Shop TH Seller University (21 Sep 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=4831419884979969&lang=en'),
 MARKETS['tiktok-shop-my']['sources'][0],
 ('Introduction to Seller Fees — TikTok Shop SG Seller University (13 Mar 2026)', 'https://seller-sg.tiktok.com/university/essay?knowledge_id=113323786536705&lang=en'),
 ('Seller Growth Support Fee (updated 22 Oct 2026) — Shopee PH Seller Education Hub', 'https://seller.shopee.ph/edu/article/27461'),
 ('Fees for Local Shopee Sellers — Shopee MY Seller Education Hub', 'https://seller.shopee.com.my/edu/article/3503'),
 ('About Commission, Service, and Transaction Fees — Shopee SG Seller Education Hub (19 Oct 2026)', 'https://seller.shopee.sg/edu/article/13107'),
 ('นโยบายค่าธรรมเนียม (Fee Policy, from 4 Aug 2026) — Shopee TH Help Centre', 'https://help.shopee.co.th/portal/4/article/77254')]}
