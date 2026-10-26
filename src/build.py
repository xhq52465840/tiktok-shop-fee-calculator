"""Build the static site: python3 src/build.py  (SITE_BASE env var overrides the canonical origin)."""
import os, re, json, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from markets import MARKETS, COMING, VERIFIED, compute
from sf_site import page, crumbs, faq_block, sources_block, widget, AD, esc, BASE, PAGES, VERIFIED_H, money, pct, LOGO
from i18n import tr
import content as C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def w(path, html):
    p = os.path.join(ROOT, path, 'index.html') if path.endswith('/') or path == '' else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(html)

def clean():
    for d in ['en', 'ms', 'malaysia', 'philippines']:
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

def toc_html(toc, lang='en'):
    return f'<aside class="aside"><div class="sticky"><p class="eyebrow">{esc(tr(lang, "on_this_page"))}</p><nav class="toc">' + ''.join(f'<a href="#{i}">{esc(t)}</a>' for i, t in toc) + '</nav></div></aside>'

def related(path, items):
    return '<div class="cards" style="margin-top:12px">' + ''.join(f'<a class="card" href="{rel_(path)}{u}"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for u, t, d in items) + '</div>'

from sf_site import rel as rel_

GUIDE_CARDS = [(f'en/guides/{g["slug"]}/', g['title'], g['desc']) for g in C.GUIDES]

# ---------------------------------------------------------------- calculators
def calc_page(mid, lang):
    m = MARKETS[mid]; d = C.PAGE_FN[(mid, lang)]()
    path = f'{lang}/{m["slug"]}/'
    alt = {l: f'{l}/{m["slug"]}/' for l in m['langs']} if len(m['langs']) > 1 else None
    plat = 'Etsy' if m['platform'] == 'etsy' else 'TikTok Shop'
    items = [('SellerFee', f'{lang}/')]
    if m['platform'] == 'tiktok-shop' and lang == 'en': items.append(('TikTok Shop', 'en/tiktok-shop/'))
    items.append((d['h1'], None))
    ch, cld = crumbs(path, items)
    fh, fld = faq_block(d['faq'], lang)
    vh = VERIFIED_H if lang == 'en' else '26 Oktober 2026'
    badges = f'<div class="badges"><span class="badge ok">✓ {esc(tr(lang, "verified"))} {vh}</span><span class="badge">{len(m["sources"])} {"official sources" if lang == "en" else "sumber rasmi"}</span><span class="badge">{"Free · no sign-up" if lang == "en" else "Percuma · tanpa daftar"}</span></div>'
    rel_guides = [g for g in GUIDE_CARDS if (m['platform'] == 'tiktok-shop')][:3] if lang == 'en' else []
    others = [(f'en/{x["slug"]}/', f'{x["platformName"]} {x["marketName"]}' if x['market'] != 'GLOBAL' else x['platformName'] + ' fee calculator', f'{x["platformName"]} fees and profit, {x["marketName"]}.') for k, x in MARKETS.items() if k != mid]
    body = f'''<div class="wrap">{ch}
<header class="pagehead"><h1>{esc(d["h1"])}</h1><p class="lede">{esc(d["lede"])}</p>{badges}</header>
{widget(mid, lang)}
{AD(mid + '-1')}
<div class="layout"><article class="prose">{d["body"]}{fh}{sources_block(m["sources"], lang)}</article>{toc_html(d["toc"], lang)}</div>
{('<h2>' + esc(tr(lang, "related")) + '</h2>' + related(path, rel_guides)) if rel_guides else ''}
<h2>{"More calculators" if lang == "en" else "Kalkulator lain"}</h2>{related(path, others)}
</div>'''
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": d['h1'], "url": BASE + path, "applicationCategory": "FinanceApplication",
           "operatingSystem": "Any", "inLanguage": lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "dateModified": VERIFIED,
           "publisher": {"@type": "Organization", "name": "SellerFee", "url": BASE}}
    w(path, page(path, lang, d['title'], d['desc'], body, [app, fld, cld], alt=alt,
                 scripts=f'<script src="{rel_(path)}assets/engine.js" defer></script>'))

# ---------------------------------------------------------------- guides
def guide_page(g):
    path = f'en/guides/{g["slug"]}/'
    body_html = C.GUIDE_BODY[g['slug']]()
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    toc = [(i, re.sub('<[^>]+>', '', t).replace('&amp;', '&')) for i, t in toc] + [('sources', 'Sources')]
    words = len(re.sub('<[^>]+>', ' ', body_html).split())
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('Guides', 'en/guides/'), (g['short'], None)])
    calcs = [(f'en/{MARKETS[k]["slug"]}/', f'TikTok Shop {MARKETS[k]["marketName"]} calculator', 'Check your own numbers with the official rates.') for k in ['tiktok-shop-my', 'tiktok-shop-ph', 'tiktok-shop-us']]
    more = [x for x in GUIDE_CARDS if g['slug'] not in x[0]]
    body = f'''<div class="wrap">{ch}
<div class="layout"><article class="prose"><header class="pagehead"><p class="eyebrow">Guide</p><h1>{esc(g["title"])}</h1>
<p class="muted">Updated <time datetime="{VERIFIED}">{VERIFIED_H}</time> · {max(2, round(words / 220))} min read · Figures from official TikTok Shop Seller University pages</p></header>
{body_html}{sources_block(C.GUIDE_SOURCES[g["slug"]])}</article>{toc_html(toc)}</div>
{AD('guide')}
<h2>Calculators</h2>{related(path, calcs)}<h2>More guides</h2>{related(path, more)}</div>'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "description": g['desc'], "datePublished": VERIFIED, "dateModified": VERIFIED,
           "inLanguage": "en", "mainEntityOfPage": BASE + path, "image": BASE + "assets/og.png",
           "author": {"@type": "Organization", "name": "SellerFee", "url": BASE}, "publisher": {"@type": "Organization", "name": "SellerFee", "logo": {"@type": "ImageObject", "url": BASE + "assets/favicon.svg"}}}
    w(path, page(path, 'en', g['title'] + ' | SellerFee', g['desc'], body, [art, cld], og_type='article'))

def guides_index():
    path = 'en/guides/'
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('Guides', None)])
    body = f'''<div class="wrap">{ch}<header class="pagehead"><h1>Seller fee guides</h1><p class="lede">Plain-English explanations of marketplace fee changes, with worked examples computed from the official rate cards.</p></header>
{related(path, GUIDE_CARDS)}</div>'''
    w(path, page(path, 'en', 'Seller Fee Guides for TikTok Shop and Etsy Sellers | SellerFee', 'Guides to TikTok Shop fee changes in Malaysia and the Philippines, pricing for a target margin and checking your settlement, with real worked examples.', body, [cld]))

# ---------------------------------------------------------------- hubs & home
def live_cards(path):
    return ''.join(f'<a class="card" href="{rel_(path)}en/{m["slug"]}/"><span class="flag">{m["flag"]}</span><h3>{esc(m["platformName"])} {esc(m["marketName"]) if m["market"] != "GLOBAL" else "fee calculator"}</h3><p>{esc(C_SUM[k])}</p><div class="meta"><span class="tag">Live</span><span>Verified {VERIFIED_H}</span></div></a>' for k, m in MARKETS.items())
def soon_cards():
    return ''.join(f'<div class="card soon"><span class="flag">{f}</span><h3>{esc(p)} {esc(mk)}</h3><p>Rates will be added once they can be verified against official sources.</p><div class="meta"><span class="tag soon">Coming soon</span></div></div>' for p, mk, f in COMING)
C_SUM = {'tiktok-shop-my': 'New commission table from 31 Oct 2026, 3.78%/4.86% transaction fee, RM0.54 support fee, BXP.',
         'tiktok-shop-ph': '₱5 Order Processing Fee, 1%–1.5% Seller Growth Fee, 2.24% transaction fee, Shipping Service Fee.',
         'tiktok-shop-us': '6% referral fee by category, 5% fine jewelry and Pre-Owned, 3% over $10K.',
         'tiktok-shop-uk': '9% commission, 5% for specified electronics and beauty categories.',
         'etsy': '6.5% transaction fee, US$0.20 listing fee and payment processing for 60+ bank countries.'}

def home():
    path = 'en/'
    pv = compute('tiktok-shop-my', sel='Beauty & Personal Care › Skincare', period='new', price=39.90, cost=12)
    RM = lambda v: money(v, 'MYR')
    preview = f'''<div class="preview" aria-label="Example result"><p class="eyebrow" style="margin:0">Example · TikTok Shop Malaysia</p><h3>RM39.90 skincare serum, Marketplace, from 31 Oct 2026</h3>
<div class="row"><span>Commission ({pct(pv['rate']['commission'])})</span><span>−{RM(pv['fee']['commission'])}</span></div>
<div class="row"><span>Transaction fee (3.78%)</span><span>−{RM(pv['fee']['tx'])}</span></div>
<div class="row"><span>Platform Support Fee</span><span>−{RM(pv['fee']['psf'])}</span></div>
<div class="row"><span>Product cost</span><span>−RM12.00</span></div>
<div class="row t"><span>Profit</span><span class="pos">{RM(pv['profit'])} · {pv['margin']:.1f}%</span></div></div>'''
    gl = ''.join(f'<a class="card" href="guides/{g["slug"]}/"><p class="eyebrow">Guide</p><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p></a>' for g in C.GUIDES)
    body = f'''<section class="hero"><div class="wrap grid"><div>
<p class="eyebrow" style="color:#5eead4">Fee &amp; profit calculators for cross-border sellers</p>
<h1>Know exactly what every marketplace takes from your sale.</h1>
<p class="lede">SellerFee turns official marketplace rate cards into fast calculators. Pick your platform and market, enter a price, and see every fee, your payout and your real margin.</p>
<div class="cta"><a class="btn" href="tiktok-shop/malaysia/">TikTok Shop Malaysia</a><a class="btn ghost" href="tiktok-shop/philippines/">Philippines</a><a class="btn ghost" href="tiktok-shop/">All TikTok Shop markets</a></div>
<ul class="trust"><li>Rates from official seller help pages</li><li>Last verified {VERIFIED_H}</li><li>Free, no sign-up</li></ul></div>
{preview}</div></section>
<section class="section"><div class="wrap"><p class="eyebrow">Calculators</p><h2 style="margin-top:.2em">Live now</h2><div class="cards">{live_cards(path)}</div>
<h2>Coming next</h2><div class="cards">{soon_cards()}</div></div></section>
<section class="section alt"><div class="wrap"><p class="eyebrow">Why sellers use SellerFee</p><h2 style="margin-top:.2em">Numbers you can check</h2><div class="features">
<div class="feature"><div class="ic">1</div><h3>Official sources only</h3><p>Every rate comes from the platform's own seller help pages, linked on each calculator. If a rate can't be verified, we don't publish the calculator.</p></div>
<div class="feature"><div class="ic">2</div><h3>Dated and re-checked</h3><p>Each page shows when its rates were last verified. When a platform changes fees, the calculator shows old and new side by side.</p></div>
<div class="feature"><div class="ic">3</div><h3>Every fee, not just commission</h3><p>Transaction, processing, per-order and program fees, caps and tiers are all included, and you can edit any rate to match your account.</p></div>
</div></div></section>
<section class="section"><div class="wrap"><p class="eyebrow">Guides</p><h2 style="margin-top:.2em">Latest guides</h2><div class="cards">{gl}</div></div></section>
{AD('home')}'''
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "SellerFee", "url": BASE, "inLanguage": "en"}
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "SellerFee", "url": BASE, "logo": BASE + "assets/favicon.svg"}
    w(path, page(path, 'en', 'SellerFee: Fee & Profit Calculators for TikTok Shop, Etsy and More', 'Free fee and profit calculators for cross-border e-commerce sellers: TikTok Shop Malaysia, Philippines, US and UK, and Etsy. Official rates, dated and sourced.', body, [site, org], alt={'en': 'en/', 'ms': 'ms/'}))

def home_ms():
    path = 'ms/'
    body = f'''<section class="hero"><div class="wrap"><p class="eyebrow" style="color:#5eead4">Kalkulator yuran &amp; untung untuk penjual</p>
<h1>Ketahui dengan tepat berapa yang diambil oleh marketplace daripada jualan anda.</h1>
<p class="lede">SellerFee menukar kad kadar rasmi marketplace kepada kalkulator yang pantas. Masukkan harga dan lihat setiap yuran, bayaran dan margin sebenar anda.</p>
<div class="cta"><a class="btn" href="tiktok-shop/malaysia/">Kalkulator TikTok Shop Malaysia</a><a class="btn ghost" href="../en/">Semua kalkulator (English)</a></div>
<ul class="trust"><li>Kadar daripada halaman rasmi Seller University</li><li>Terakhir disahkan 26 Oktober 2026</li><li>Percuma, tanpa daftar</li></ul></div></section>
<section class="section"><div class="wrap"><h2 style="margin-top:0">Kalkulator dalam Bahasa Melayu</h2><div class="cards">
<a class="card" href="tiktok-shop/malaysia/"><span class="flag">🇲🇾</span><h3>TikTok Shop Malaysia</h3><p>Jadual komisen baharu mulai 31 Okt 2026, yuran transaksi 3.78%/4.86%, Yuran Sokongan Platform RM0.54 dan BXP.</p><div class="meta"><span class="tag">Aktif</span></div></a></div>
<p class="muted" style="margin-top:18px">Kalkulator untuk Filipina, Amerika Syarikat, United Kingdom dan Etsy tersedia dalam bahasa Inggeris.</p></div></section>'''
    w(path, page(path, 'ms', 'SellerFee: Kalkulator Yuran & Untung untuk Penjual TikTok Shop', 'Kalkulator yuran dan untung percuma untuk penjual e-dagang, bermula dengan TikTok Shop Malaysia. Kadar rasmi, bertarikh dan bersumber.', body, alt={'en': 'en/', 'ms': 'ms/'}))

def tiktok_hub():
    path = 'en/tiktok-shop/'
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('TikTok Shop', None)])
    tt = [m for m in MARKETS.values() if m['platform'] == 'tiktok-shop']
    rows = ''.join(f'<tr><td>{m["flag"]} <a href="{m["slug"].split("/")[1]}/">{m["marketName"]}</a></td><td>{esc(C_SUM[k])}</td></tr>' for k, m in MARKETS.items() if m['platform'] == 'tiktok-shop')
    cards = ''.join(f'<a class="card" href="{m["slug"].split("/")[1]}/"><span class="flag">{m["flag"]}</span><h3>TikTok Shop {m["marketName"]}</h3><p>{esc(C_SUM[k])}</p><div class="meta"><span class="tag">Live</span><span>Verified {VERIFIED_H}</span></div></a>' for k, m in MARKETS.items() if m['platform'] == 'tiktok-shop')
    soon = ''.join(f'<div class="card soon"><span class="flag">{f}</span><h3>TikTok Shop {mk}</h3><p>We publish a market only after verifying its rates on TikTok\'s own Seller University pages.</p><div class="meta"><span class="tag soon">Coming soon</span></div></div>' for p, mk, f in COMING if p == 'TikTok Shop')
    body = f'''<div class="wrap">{ch}<header class="pagehead"><h1>TikTok Shop fee calculators by country</h1>
<p class="lede">TikTok Shop charges different fees in every market: category commission in Southeast Asia, a flat referral fee in the US and a single commission rate in the UK. Pick your market.</p></header>
<div class="cards">{cards}{soon}</div>
<h2>How TikTok Shop fees differ by market</h2><div class="tablewrap"><table class="tbl"><thead><tr><th>Market</th><th>Main fees</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Guides</h2>{related(path, GUIDE_CARDS)}</div>'''
    w(path, page(path, 'en', 'TikTok Shop Fee Calculators: Malaysia, Philippines, US & UK | SellerFee', 'Free TikTok Shop seller fee calculators for Malaysia, the Philippines, the United States and the United Kingdom, built on the official Seller University rate cards.', body, [cld]))

# ---------------------------------------------------------------- company pages
REPO = 'https://github.com/xhq52465840/tiktok-shop-fee-calculator'
def static_pages():
    P = {
     'about': ('About SellerFee', 'About SellerFee: who we are, how we verify marketplace fee rates and how the calculators work.', f'''
<p>SellerFee is an independent website that publishes free fee and profit calculators for people who sell on online marketplaces, especially sellers working across borders. We started with TikTok Shop in Malaysia and the Philippines, where fees changed several times in 2026, and are adding more platforms and markets.</p>
<h2>How we source rates</h2>
<p>Every rate in our calculators comes from the platform's own seller help pages, such as TikTok Shop Seller University or the Etsy Help Center. Each calculator links its sources and shows the date we last checked them. When a platform publishes only a rate but not how it is calculated, we say so on the page and make the rate editable. We don't publish a calculator for a market until its rates can be verified from an official source.</p>
<h2>How we keep them current</h2>
<p>We re-check the source pages regularly and whenever a platform announces a change. When fees change, we keep the old rates alongside the new ones so you can compare, and we note the effective date.</p>
<h2>How the calculators work</h2>
<p>The calculators run entirely in your browser. Nothing you type is sent to us. Results are estimates based on the published rates; your own account may have waivers, program fees or promotions that change the numbers, so your Seller Center is always the final word.</p>
<h2>Independence</h2>
<p>SellerFee is not affiliated with, endorsed by or sponsored by TikTok, ByteDance, Etsy, Shopee, Lazada, Amazon, eBay or any other marketplace. Product and company names are trademarks of their owners.</p>
<h2>Get in touch</h2><p>Spotted a rate that has changed, or want a market added? See our <a href="../contact/">contact page</a>.</p>'''),
     'contact': ('Contact SellerFee', 'How to contact SellerFee, report a fee change or request a new marketplace calculator.', f'''
<p>We'd like to hear from you, especially if a platform has changed its fees and we haven't caught it yet.</p>
<h2>Report a rate change or an error</h2>
<p>Open an issue on our public project page: <a href="{REPO}/issues" rel="noopener">{REPO.replace("https://", "")}/issues</a>. Please include the platform, the market, the fee that looks wrong and, if you can, a link to the official page that shows the current rate.</p>
<h2>Request a calculator</h2>
<p>Use the same page to request a platform or market. We add markets once their rates can be verified from official sources.</p>
<h2>What we can't help with</h2>
<p>We can't see or change anything in your marketplace account. For questions about a specific order or deduction, contact the platform's seller support, for example through Seller Center → Help Center on TikTok Shop.</p>'''),
     'privacy': ('Privacy Policy', 'SellerFee privacy policy: what data the site collects, cookies, advertising and your choices.', f'''
<p><i>Last updated {VERIFIED_H}.</i></p>
<p>This policy explains what information SellerFee ("we") collects when you use this website and how it is used.</p>
<h2>Information you enter in calculators</h2>
<p>The calculators run in your browser. Prices, costs and other numbers you enter are not sent to or stored on our servers.</p>
<h2>Information collected automatically</h2>
<p>The site is hosted on GitHub Pages. Like most web hosts, GitHub may log technical information such as your IP address, browser type and the pages requested, for security and operational purposes. See GitHub's privacy statement for details. We do not currently run our own analytics.</p>
<h2>Cookies</h2>
<p>SellerFee itself does not set cookies today. If we add analytics or advertising, the third-party services described below may use cookies or similar technologies, and we will update this policy before doing so.</p>
<h2>Advertising</h2>
<p>We may show ads served by third-party vendors, including Google. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" rel="noopener">www.aboutads.info</a>. Where required by law, we will ask for your consent before personalised ads are shown.</p>
<h2>Links to other sites</h2>
<p>Our pages link to official marketplace help pages and other sites. Their privacy practices are their own.</p>
<h2>Children</h2>
<p>The site is intended for adults running a business and is not directed at children under 13.</p>
<h2>Changes and contact</h2>
<p>We will post any changes on this page with a new date. Questions can be raised through our <a href="../contact/">contact page</a>.</p>'''),
     'terms': ('Terms of Use', 'Terms of use for SellerFee calculators and content.', f'''
<p><i>Last updated {VERIFIED_H}.</i></p>
<p>By using SellerFee you agree to these terms.</p>
<h2>Estimates, not advice</h2>
<p>Our calculators and guides provide estimates based on fee rates published by each marketplace on the date shown. They are for general information only and are not financial, tax, accounting or legal advice. Your actual fees can differ because of your account type, category assignment, programs, waivers, promotions, taxes, currency conversion or changes the platform makes after our last check. Always confirm fees in your marketplace account before making pricing or business decisions.</p>
<h2>No warranty</h2>
<p>The site is provided "as is" without warranties of any kind. We do our best to keep rates accurate and current but do not guarantee that they are complete, correct or up to date.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, SellerFee is not liable for any loss arising from your use of, or reliance on, the site or its results.</p>
<h2>Trademarks</h2>
<p>TikTok, TikTok Shop, Etsy, Shopee, Lazada, Amazon and eBay are trademarks of their respective owners. SellerFee is independent and not affiliated with or endorsed by them.</p>
<h2>Acceptable use</h2>
<p>You may use the calculators freely for your own business. Please don't scrape the site at a rate that disrupts it or republish our content as your own.</p>
<h2>Changes</h2>
<p>We may update these terms; the date above shows the latest version.</p>'''),
    }
    for slug, (title, desc, html) in P.items():
        path = f'en/{slug}/'
        ch, cld = crumbs(path, [('SellerFee', 'en/'), (title, None)])
        w(path, page(path, 'en', f'{title} | SellerFee', desc, f'<div class="wrap narrow">{ch}<article class="prose"><h1>{esc(title)}</h1>{html}</article></div>', [cld]))

# ---------------------------------------------------------------- plumbing
def plumbing():
    # root: send visitors to /en/ (or /ms/ for Malay browsers)
    open(os.path.join(ROOT, 'index.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SellerFee</title>
<link rel="canonical" href="{BASE}en/"><link rel="alternate" hreflang="en" href="{BASE}en/"><link rel="alternate" hreflang="ms" href="{BASE}ms/"><link rel="alternate" hreflang="x-default" href="{BASE}en/">
<meta http-equiv="refresh" content="0; url=en/"><meta name="robots" content="noindex,follow">
<script>location.replace((navigator.language||'').toLowerCase().indexOf('ms')===0?'ms/':'en/')</script></head><body><a href="en/">SellerFee</a></body></html>''')
    for old, new in [('malaysia/', 'en/tiktok-shop/malaysia/'), ('philippines/', 'en/tiktok-shop/philippines/')]:
        w(old, f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{BASE}{new}"><meta http-equiv="refresh" content="0; url=../{new}"><meta name="robots" content="noindex"></head><body><a href="../{new}">This page has moved.</a></body></html>')
    open(os.path.join(ROOT, '404.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | SellerFee</title><meta name="robots" content="noindex">
<script>var b=location.hostname.endsWith('github.io')?'/tiktok-shop-fee-calculator/':'/';document.write('<base href="'+b+'">')</script><link rel="stylesheet" href="assets/style.css"></head>
<body><main class="wrap narrow" style="padding:80px 20px"><h1>Page not found</h1><p>The page you're looking for doesn't exist or has moved.</p><p><a class="btn" href="en/">Go to the calculators</a></p></main></body></html>''')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, alt in PAGES:
        sm.append(f'  <url><loc>{BASE}{path}</loc><lastmod>{VERIFIED}</lastmod>')
        if alt:
            for l, p in alt.items(): sm.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{p}"/>')
            sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{alt["en"]}"/>')
        sm.append('  </url>')
    sm.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(ROOT, 'assets', 'favicon.svg'), 'w').write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
    os.makedirs(os.path.join(ROOT, 'deploy'), exist_ok=True)
    open(os.path.join(ROOT, 'deploy', 'CNAME'), 'w').write('sellerfee.app\n')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')

if __name__ == '__main__':
    clean()
    home(); home_ms(); tiktok_hub()
    for mid, m in MARKETS.items():
        for lang in m['langs']: calc_page(mid, lang)
    guides_index()
    for g in C.GUIDES: guide_page(g)
    static_pages(); plumbing()
    print('built', len(PAGES), 'pages')
