# Builds the static pages. Run: python3 src/build.py
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.environ.get('SITE_BASE', 'https://xhq52465840.github.io/tiktok-shop-fee-calculator/')
VERIFIED = '2026-10-26'
VERIFIED_H = '26 October 2026'
AD = '<div class="ad-slot" data-ad-slot="{}"><!-- Ad placeholder: no ad code yet --></div>'

def head(title, desc, path, faq=None, extra=''):
    url = BASE + path
    ld = [{"@context":"https://schema.org","@type":"WebApplication","name":title,"url":url,"applicationCategory":"BusinessApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0"},"dateModified":VERIFIED}]
    if faq:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    rel = '../' if path else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Ctext y=%22.9em%22 font-size=%2290%22%3E%F0%9F%A7%AE%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{rel}assets/style.css">
{extra}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
'''

def header(rel):
    return f'''<header class="site"><div class="in"><a href="{rel or './'}">TikTok Shop Fee Calculator</a>
<nav><a href="{rel}malaysia/">Malaysia</a><a href="{rel}philippines/">Philippines</a></nav></div></header>
'''

def footer(rel):
    return f'''<footer><div class="in">
<p>Independent tool, not affiliated with TikTok or ByteDance. Rates come from official TikTok Shop Seller University pages (last checked {VERIFIED_H}). Fees can change and your shop may have waivers or program fees not shown here, so always confirm in Seller Center before pricing.</p>
<p><a href="{rel}">Home</a> · <a href="{rel}malaysia/">Malaysia calculator</a> · <a href="{rel}philippines/">Philippines calculator</a></p>
</div></footer>
'''

def faq_html(faq):
    return '<h2 id="faq">FAQ</h2>\n' + '\n'.join(f'<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>' for q,a in faq)

def sources_html(src):
    return '<h2 id="sources">Sources</h2>\n<ul>' + ''.join(f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{html.escape(t)}</a>{(" — " + html.escape(n)) if n else ""}</li>' for t,u,n in src) + f'</ul>\n<p class="note">Last verified: <time datetime="{VERIFIED}">{VERIFIED_H}</time>.</p>'

COMMON_INPUTS = '''
<div class="full"><label for="cat">Product category</label><select id="cat"></select><p class="note" id="catNote"></p></div>
<div class="full"><label>Store type</label><div class="seg"><label><input type="radio" name="store" value="mp" checked>Marketplace</label><label><input type="radio" name="store" value="mall">Mall</label></div></div>
<div><label for="price">Selling price per item <small>({cur})</small></label><input id="price" type="number" inputmode="decimal" min="0" step="0.01" value="{price}"></div>
<div><label for="qty">Quantity in order</label><input id="qty" type="number" inputmode="numeric" min="1" step="1" value="1"></div>
<div><label for="sellerDisc">Seller-funded discount / voucher <small>(order total)</small></label><input id="sellerDisc" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
<div><label for="cost">Product cost per item</label><input id="cost" type="number" inputmode="decimal" min="0" step="0.01" value="{cost}"></div>
<div><label for="buyerShip">Shipping paid by buyer</label><input id="buyerShip" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
<div><label for="shipCost">Shipping cost you pay</label><input id="shipCost" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
<div><label for="affPct">Affiliate creator commission <small>(%)</small></label><input id="affPct" type="number" inputmode="decimal" min="0" step="0.1" value="0"></div>
<div><label for="other">Other costs <small>(packaging, ads…)</small></label><input id="other" type="number" inputmode="decimal" min="0" step="0.01" value="0"></div>
'''

RESULTS = '''<div class="card" aria-live="polite">
<h2 style="margin-top:0">Result</h2>
<div class="big"><div><span>TikTok fees</span><b id="kFees">–</b><span id="kFeesPct"></span></div><div><span>Payout</span><b id="kPayout">–</b></div><div><span>Profit</span><b id="kProfit">–</b><span id="kMargin"></span></div></div>
<div class="tablewrap" id="breakdown"></div>
<p class="note">Platform-funded vouchers don't reduce your fees or payout, so they aren't an input. Margin = profit ÷ item subtotal after your discount.</p>
</div>'''

# ---------------- Malaysia ----------------
MY_FAQ = [
 ("What are TikTok Shop Malaysia's seller fees in 2026?", "On a normal delivered order you pay a commission fee by product category (different for Marketplace and Mall, and lower if you join the Bonus Extra Program), a 3.78% transaction fee (4.86% on TikTok PayLater orders from 16 October 2026), and a flat RM0.54 Platform Support Fee per order. BXP sellers also pay a 4.86% BXP service fee, or 7.02% on campaign days. All rates include 8% SST."),
 ("What changes on 31 October 2026?", "TikTok Shop Malaysia revises Marketplace and Mall commission rates for orders placed from 00:00 on 31 October 2026, Malaysia time. Orders placed before that date follow the old rates. Most categories go up (for example non-BXP Marketplace skincare moves from 15.12% to 16.74%), while some essentials such as feminine care, medical supplies, OTC medicine and nursing & feeding go down, and fresh food, baking, dairy and staples stay at 0%."),
 ("How is the TikTok Shop commission fee calculated in Malaysia?", "Commission = (item price − seller discount) × the category rate. Shipping and TikTok platform discounts are not part of the base. The published rates already include SST."),
 ("How is the transaction fee calculated?", "Since 15 February 2026 the transaction fee is (original item price − seller discount + shipping paid by the buyer) × 3.78%. From 16 October 2026 orders paid with TikTok PayLater are charged 4.86% instead. Platform discounts are not deducted from the base."),
 ("What is the RM0.54 Platform Support Fee?", "A flat fee of RM0.50 plus 8% SST (RM0.54) per successfully delivered order, regardless of order value or quantity, introduced on 15 February 2026. It is not refunded if a delivered order is later returned. Some categories and eligible new or small sellers can get it rebated or waived."),
 ("Is joining BXP worth it after the new rates?", "From 31 October 2026, BXP lowers your commission by roughly 2.2 to 6 percentage points depending on category (2.70 points for many categories, such as skincare), but adds a 4.86% BXP service fee (7.02% on campaign days, capped at RM54 per item) on every completed order. Tick and untick 'Bonus Extra Program' in the calculator to compare your own numbers."),
 ("Are TikTok Shop Malaysia fees inclusive of SST?", "Yes. TikTok publishes the commission, transaction, BXP and Platform Support Fee rates inclusive of 8% SST, and this calculator uses those SST-inclusive figures."),
]
MY_SRC = [
 ("Commission Fee & Seller Fees Calculations (TikTok Shop MY Seller University, updated 16 Oct 2026)", "https://seller-my.tiktok.com/university/essay?knowledge_id=6907739532281602&lang=en", "full before/after 31 Oct 2026 commission table, formula"),
 ("Transaction Fee (TikTok Shop MY Seller University)", "https://seller-my.tiktok.com/university/essay?knowledge_id=10013511&lang=en", "3.78%, PayLater 4.86% from 16 Oct 2026, fee base"),
 ("Platform Support Fee (TikTok Shop MY Seller University)", "https://seller-my.tiktok.com/university/essay?knowledge_id=7992113007347457&lang=en", "RM0.50 + SST = RM0.54 per delivered order"),
 ("Bonus Extra Program (BXP) (TikTok Shop MY Seller University, 22 Sep 2026)", "https://seller-my.tiktok.com/university/essay?knowledge_id=8969995510564625&lang=en", "4.86% / 7.02% campaign-day fee, RM54 per-item cap"),
]

def my_page():
    title = "TikTok Shop Fee Calculator Malaysia 2026 (New 31 Oct Rates)"
    desc = "Free TikTok Shop Malaysia fee and profit calculator with the new commission rates from 31 October 2026, 3.78%/4.86% transaction fee, RM0.54 support fee and BXP. Old vs new comparison."
    inputs = COMMON_INPUTS.format(cur='RM', price='50', cost='20') + '''
<div class="full"><label for="period">Rate period</label><select id="period"><option value="new" selected>Orders from 31 Oct 2026 (new rates)</option><option value="old">Orders before 31 Oct 2026</option></select></div>
<div class="full"><label class="chk"><input type="checkbox" id="bxp"> Bonus Extra Program (BXP) seller</label>
<label class="chk"><input type="checkbox" id="campaign"> BXP campaign day (Double Day / Payday, 7.02%)</label>
<label class="chk"><input type="checkbox" id="paylater"> Buyer paid with TikTok PayLater (4.86% transaction fee)</label>
<label class="chk"><input type="checkbox" id="psfWaived"> Platform Support Fee waived or rebated for this order</label></div>
<div class="full"><details><summary>Edit the fee rates</summary><p class="note">These fill in from the official tables. Change them if your Seller Center shows something different.</p><div class="grid">
<div><label for="commRate">Commission rate (%)</label><input id="commRate" type="number" step="0.01" min="0"></div>
<div><label for="txRate">Transaction fee (%)</label><input id="txRate" type="number" step="0.01" min="0"></div>
<div><label for="bxpRate">BXP service fee (%)</label><input id="bxpRate" type="number" step="0.01" min="0"></div>
<div><label for="psf">Platform Support Fee (RM per order)</label><input id="psf" type="number" step="0.01" min="0"></div>
</div></details></div>'''
    body = f'''<body data-market="MY">
{header('../')}<main>
<h1>TikTok Shop Fee Calculator Malaysia (31 Oct 2026 rates)</h1>
<p class="lead">Work out what TikTok Shop Malaysia takes from each order and what you keep, using the commission table that applies to orders from 31 October 2026, plus the transaction fee, Platform Support Fee and BXP fee.</p>
<p><span class="badge">Rates last verified {VERIFIED_H} from TikTok Seller University</span></p>
{AD.format('my-top')}
<div class="calc" id="calc">
<div class="card"><div class="grid">{inputs}</div></div>
{RESULTS}
</div>
<div class="card"><h2 style="margin-top:0">Old vs new: before and after 31 October 2026</h2><div class="tablewrap" id="compare"></div></div>
{AD.format('my-mid')}
<h2>TikTok Shop Malaysia fees at a glance</h2>
<div class="tablewrap"><table>
<thead><tr><th>Fee</th><th>Rate (SST inclusive)</th><th>Charged on</th><th>Since</th></tr></thead>
<tbody>
<tr><td>Commission</td><td>0% – 20.52% by category, Marketplace/Mall, BXP</td><td>Item price − seller discount</td><td>New table from 31 Oct 2026</td></tr>
<tr><td>Transaction fee</td><td>3.78%; 4.86% for TikTok PayLater</td><td>Item price − seller discount + buyer-paid shipping</td><td>PayLater rate from 16 Oct 2026</td></tr>
<tr><td>Platform Support Fee</td><td>RM0.54 per delivered order</td><td>Flat</td><td>15 Feb 2026</td></tr>
<tr><td>BXP service fee (BXP sellers only)</td><td>4.86%; 7.02% on campaign days; cap RM54/item</td><td>Item price − seller discount</td><td>Campaign-day rate from 7 Oct 2026</td></tr>
</tbody></table></div>
<p class="note">BXP campaign days in the rest of 2026 per TikTok: Double Day 8–11 Nov and 9–12 Dec; Payday 24–25 Nov and 20–21 Dec. TikTok's own worked example shows the Platform Support Fee as RM0.50 (before SST); the fee page says RM0.54 including SST, which is what we use.</p>
<h2 id="rates">Full commission rate table (Malaysia)</h2>
<p>Every sub-category from TikTok's official table. MP = Marketplace. Columns 5–8 are the rates for orders from 31 October 2026.</p>
<p><input id="rateFilter" type="search" placeholder="Filter categories, e.g. skincare" style="width:100%;padding:9px;border:1px solid #c9ced6;border-radius:8px;font-size:16px"></p>
<div class="tablewrap"><table class="ratetable"><thead><tr><th rowspan="2">Category › Sub-category</th><th colspan="4">Before 31 Oct 2026</th><th colspan="4">From 31 Oct 2026</th></tr>
<tr><th class="n">MP BXP</th><th class="n">MP non-BXP</th><th class="n">Mall BXP</th><th class="n">Mall non-BXP</th><th class="n">MP BXP</th><th class="n">MP non-BXP</th><th class="n">Mall BXP</th><th class="n">Mall non-BXP</th></tr></thead><tbody id="rateBody"></tbody></table></div>
{faq_html(MY_FAQ)}
{AD.format('my-bottom')}
{sources_html(MY_SRC)}
</main>
{footer('../')}<script src="../assets/data.js"></script><script src="../assets/calc.js"></script>
</body></html>
'''
    return head(title, desc, 'malaysia/', MY_FAQ) + body

# ---------------- Philippines ----------------
PH_FAQ = [
 ("What are TikTok Shop Philippines seller fees in 2026?", "Each delivered order is charged a commission fee by category (Marketplace 5%–7.3%, Mall 5%–9.1%), a 2.24% transaction fee, a Shipping Service Fee of 5.5% (Marketplace) or 5% (Mall) capped at ₱100 per item, a fixed ₱5 Order Processing Fee per order, and a Seller Growth Fee of 1% or 1.5% depending on category. All rates are VAT inclusive."),
 ("What is the TikTok Shop Seller Growth Fee?", "A per-order fee TikTok Shop Philippines charges all sellers to fund platform-wide growth incentives, including making the Bonus Cashback Program free for eligible sellers. It is 1% for Electronics, Grocery and Large Appliances, and 1.5% for Beauty & Personal Care, Fashion, Mom & Baby, Health and Lifestyle (except Large Appliances), VAT inclusive. Seller reports date it from 27 April 2026."),
 ("Is the TikTok Shop order processing fee ₱3 or ₱5?", "₱5. TikTok charged a discounted ₱3 from 1 December 2025, then ended the discount from 00:00 on 1 September 2026 (Philippine time). The fee is now a fixed ₱5 (tax inclusive) per successfully delivered order, regardless of order value or number of items."),
 ("Who doesn't pay the ₱5 order processing fee?", "TikTok waives it for new sellers (first product listed within the last 90 days) for the following month, and existing sellers get their first 50 orders each month free. Tick 'Order Processing Fee exempt' in the calculator for those orders."),
 ("How is the TikTok Shop Philippines commission calculated?", "Commission = (item price − seller discount) × the sub-category rate. Shipping and TikTok platform discounts are excluded. New sellers get 0% commission for their first 90 days."),
 ("Is the Shipping Service Fee charged on every order?", "TikTok's seller fee overview says it is charged to all sellers on successfully delivered orders: 5.5% for Marketplace and 5% for Mall, capped at ₱100 per item, and not refunded if the order is later returned."),
 ("Are TikTok Shop PH fees VAT inclusive?", "Yes. TikTok publishes all of these Philippine fee rates inclusive of VAT, and the calculator uses them as published."),
]
PH_SRC = [
 ("Introduction to Seller Fees (TikTok Shop PH Seller University, updated 13 Oct 2026)", "https://seller-ph.tiktok.com/university/essay?knowledge_id=2675772847064834&lang=en", "transaction 2.24%, Shipping Service Fee, ₱5 processing fee, Seller Growth Fee rates"),
 ("Platform Commission Fee (TikTok Shop PH Seller University)", "https://seller-ph.tiktok.com/university/essay?knowledge_id=3157977859229442&lang=en", "commission table effective 15 Jan 2025, formula, new-seller waiver"),
 ("[Philippines] Order Processing Fee (TikTok Shop Academy, 18 Aug 2026)", "https://seller.tiktokglobalshop.com/university/essay?knowledge_id=6361124523788048", "₱5 from 1 Sep 2026, exemptions"),
 ("Report on the Seller Growth Fee start date (Baijing, secondary source)", "https://www.baijing.cn/article/55291", "27 Apr 2026 start date; not confirmed on an official page we could read"),
]

def ph_page():
    title = "TikTok Shop Philippines Seller Fee Calculator 2026 (₱5 + Growth Fee)"
    desc = "Free TikTok Shop Philippines fee and profit calculator with the ₱5 order processing fee, the new 1%–1.5% Seller Growth Fee, 2.24% transaction fee and Shipping Service Fee. Updated October 2026."
    inputs = COMMON_INPUTS.format(cur='₱', price='499', cost='200') + '''
<div class="full"><label class="chk"><input type="checkbox" id="newSeller"> New seller in 0% commission period (first 90 days)</label>
<label class="chk"><input type="checkbox" id="opfExempt"> Order Processing Fee exempt (new seller month, or within first 50 orders this month)</label></div>
<div class="full"><details><summary>Edit the fee rates</summary><p class="note">These fill in from the official pages. Change them if your Seller Center shows something different.</p><div class="grid">
<div><label for="commRate">Commission rate (%)</label><input id="commRate" type="number" step="0.01" min="0"></div>
<div><label for="txRate">Transaction fee (%)</label><input id="txRate" type="number" step="0.01" min="0"></div>
<div><label for="ssfRate">Shipping Service Fee (%)</label><input id="ssfRate" type="number" step="0.01" min="0"></div>
<div><label for="ssfCap">Shipping Service Fee cap (₱ per item)</label><input id="ssfCap" type="number" step="1" min="0"></div>
<div><label for="opf">Order Processing Fee (₱ per order)</label><input id="opf" type="number" step="0.01" min="0"></div>
<div><label for="growthRate">Seller Growth Fee (%)</label><input id="growthRate" type="number" step="0.01" min="0"></div>
</div></details></div>'''
    body = f'''<body data-market="PH">
{header('../')}<main>
<h1>TikTok Shop Philippines Seller Fee Calculator (2026)</h1>
<p class="lead">See every fee TikTok Shop PH deducts from an order, including the ₱5 Order Processing Fee and the new Seller Growth Fee that many calculators still leave out, and what profit you keep.</p>
<p><span class="badge">Rates last verified {VERIFIED_H} from TikTok Seller University</span></p>
{AD.format('ph-top')}
<div class="calc" id="calc">
<div class="card"><div class="grid">{inputs}</div></div>
{RESULTS}
</div>
<div class="card"><h2 style="margin-top:0">Old vs new: early 2026 vs now</h2><div class="tablewrap" id="compare"></div></div>
{AD.format('ph-mid')}
<h2>TikTok Shop Philippines fees at a glance</h2>
<div class="tablewrap"><table>
<thead><tr><th>Fee</th><th>Rate (VAT inclusive)</th><th>Charged on</th><th>Since</th></tr></thead>
<tbody>
<tr><td>Commission</td><td>Marketplace 5%–7.3%, Mall 5%–9.1%</td><td>Item price − seller discount</td><td>15 Jan 2025 table</td></tr>
<tr><td>Transaction fee</td><td>2.24%</td><td>Item price − seller discount + buyer-paid shipping*</td><td>—</td></tr>
<tr><td>Shipping Service Fee</td><td>5.5% Marketplace / 5% Mall, cap ₱100 per item</td><td>Item price − seller discount</td><td>—</td></tr>
<tr><td>Order Processing Fee</td><td>₱5 per delivered order</td><td>Flat</td><td>1 Sep 2026 (₱3 before)</td></tr>
<tr><td>Seller Growth Fee</td><td>1% Electronics, Grocery, Large Appliances; 1.5% Beauty, Fashion, Mom &amp; Baby, Health, Lifestyle</td><td>Item price − seller discount*</td><td>27 Apr 2026 (reported)</td></tr>
</tbody></table></div>
<p class="note">* TikTok's overview page gives the rate but not the exact base for these two fees. The transaction fee base follows TikTok's July 2026 formula change as reported by seller news sites; the growth fee base is our assumption. Both are editable above.</p>
<h2 id="rates">Commission and growth fee by category (Philippines)</h2>
<p><input id="rateFilter" type="search" placeholder="Filter categories, e.g. shoes" style="width:100%;padding:9px;border:1px solid #c9ced6;border-radius:8px;font-size:16px"></p>
<div class="tablewrap"><table class="ratetable"><thead><tr><th>Cluster</th><th>Category</th><th class="n">Marketplace</th><th class="n">Mall</th><th class="n">Growth fee</th></tr></thead><tbody id="rateBody"></tbody></table></div>
<p class="note">* Kids' Fashion and Pet Supplies are not named in TikTok's growth fee list; 1.5% is assumed.</p>
{faq_html(PH_FAQ)}
{AD.format('ph-bottom')}
{sources_html(PH_SRC)}
</main>
{footer('../')}<script src="../assets/data.js"></script><script src="../assets/calc.js"></script>
</body></html>
'''
    return head(title, desc, 'philippines/', PH_FAQ) + body

def home():
    title = "TikTok Shop Fee Calculator for Malaysia & Philippines (Updated Oct 2026)"
    desc = "Free TikTok Shop seller fee and profit calculators for Malaysia (new 31 Oct 2026 commission rates) and the Philippines (₱5 processing fee and Seller Growth Fee). Official rates with sources."
    faq = [("Which TikTok Shop fee changes happened in 2026?", "Malaysia added a RM0.54 Platform Support Fee (15 Feb), raised the PayLater transaction fee to 4.86% (16 Oct), raised the BXP campaign-day fee to 7.02% (7 Oct) and revises commission rates from 31 Oct 2026. The Philippines added a 1%–1.5% Seller Growth Fee (from 27 Apr, as reported) and raised the Order Processing Fee from ₱3 to ₱5 on 1 Sep 2026."),
           ("Is this calculator official?", "No. It is an independent free tool. The rates are copied from TikTok's official Seller University pages, linked on each calculator page with the date we last checked them.")]
    body = f'''<body>
{header('')}<main>
<h1>TikTok Shop Fee Calculator: Malaysia &amp; Philippines</h1>
<p class="lead">TikTok Shop changed its seller fees several times in 2026, and many calculators haven't caught up. These calculators use the official rates and show the full fee breakdown, your payout and your profit.</p>
<p><span class="badge">Rates last verified {VERIFIED_H}</span></p>
<div class="cards">
<a class="card" href="malaysia/"><h2 style="margin-top:0">🇲🇾 Malaysia</h2><p>New commission rates from 31 October 2026, 3.78% / 4.86% PayLater transaction fee, RM0.54 Platform Support Fee, BXP 4.86% / 7.02%.</p><span class="btn">Open calculator</span></a>
<a class="card" href="philippines/"><h2 style="margin-top:0">🇵🇭 Philippines</h2><p>₱5 Order Processing Fee, 1%–1.5% Seller Growth Fee, 2.24% transaction fee, 5.5% / 5% Shipping Service Fee.</p><span class="btn">Open calculator</span></a>
</div>
{AD.format('home')}
{faq_html(faq)}
</main>
{footer('')}</body></html>
'''
    return head(title, desc, '', faq) + body

def w(p, s):
    p = os.path.join(ROOT, p); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(s)

w('index.html', home()); w('malaysia/index.html', my_page()); w('philippines/index.html', ph_page())
w('404.html', head('Page not found', 'Page not found', '404.html') + '<body>' + header('/tiktok-shop-fee-calculator/') + '<main><h1>Page not found</h1><p><a href="/tiktok-shop-fee-calculator/">Go to the calculators</a></p></main></body></html>')
w('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc><lastmod>{VERIFIED}</lastmod></url>\n' for p in ['', 'malaysia/', 'philippines/']) + '</urlset>\n')
w('.nojekyll', '')
print('built')
