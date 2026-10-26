"""Build the static site: python3 src/build.py  (SITE_BASE env var overrides the canonical origin)."""
import os, re, json, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from markets import MARKETS, COMING, VERIFIED, compute
from sf_site import (page, crumbs, faq_block, sources_block, widget, AD, esc, BASE, PAGES,
                     VERIFIED_H, VFULL, VDATE, LOGO, ic, ptile, calc_name, calc_links, badge,
                     issue_url, rel as rel_, MARK)
from site_helpers import money, pct
from i18n import tr, LANGS
import content as C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def w(path, html):
    p = os.path.join(ROOT, path, 'index.html') if path.endswith('/') or path == '' else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w', encoding='utf-8').write(html)

def clean():
    for d in ['en', 'ms', 'ru', 'malaysia', 'philippines']:
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

def copy_rates():
    dst = os.path.join(ROOT, 'assets', 'rates')
    os.makedirs(dst, exist_ok=True)
    for mid, m in MARKETS.items():
        src = m['selector'].get('src')
        if not src: continue
        # src is a short key like 'ozon' — file lives at src/data/{mid}/ru.json or similar
        for cand in [os.path.join(ROOT, 'src', 'data', mid, 'ru.json'),
                     os.path.join(ROOT, 'src', 'data', mid, f'{src}.json'),
                     os.path.join(ROOT, 'assets', 'rates', f'{mid}.json')]:
            if os.path.isfile(cand):
                shutil.copy2(cand, os.path.join(dst, f'{mid}.json')); break

def toc_html(toc, lang='en'):
    return ('<aside class="toc" aria-label="On this page"><b>' + esc(tr(lang, 'on_this_page')) + '</b><div class="lst">'
            + ''.join(f'<a href="#{i}">{esc(t)}</a>' for i, t in toc) + '</div></aside>')

def rail_calcs(path, lang, mid=None):
    items = ''.join(f'<li><a href="{rel_(path)}{u}">{ptile(p, 22)}{esc(n)}</a></li>' for u, n, p, f, k in calc_links(lang) if k != mid)
    return f'<aside class="rail"><div class="card railcard"><div class="t">{esc(tr(lang, "more_calcs"))}</div><ul>{items}</ul></div></aside>'

def gcard(path, g, lang):
    cov = g.get('cov', 'cov-ink'); fig = g.get('fig', '')
    href = f'{g.get("lang","en")}/guides/{g["slug"]}/'
    words = 700
    return f'''<a class="card gcard" href="{rel_(path)}{href}">
<div class="cov {cov}"><div class="fig">{esc(fig)}</div><div class="cap">{esc(g["short"])}</div></div>
<div class="body"><span class="badge b-brand sm">{esc(tr(lang,"guide"))}</span>
<h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p>
<div class="gmeta"><span>{ic("clock",13)}{max(3, round(words/220))} {esc(tr(lang,"min_read"))}</span><span>{ic("cal",13)}{VDATE[lang]}</span></div></div></a>'''

# ---------------------------------------------------------------- calculators
def calc_page(mid, lang):
    m = MARKETS[mid]; d = C.PAGE_FN[(mid, lang)]()
    path = f'{lang}/{m["slug"]}/'
    alt = {l: f'{l}/{m["slug"]}/' for l in m['langs']} if len(m['langs']) > 1 else None
    items = [('SellerFee', f'{lang}/')]
    if m['platform'] == 'tiktok-shop' and lang == 'en': items.append(('TikTok Shop', 'en/tiktok-shop/'))
    if m['market'] == 'RU' and lang == 'en': items.append(('Russia', 'en/russia/'))
    if m['market'] == 'RU' and lang == 'ru': items.append(('Россия', 'ru/'))
    items.append((d['h1'], None))
    ch, cld = crumbs(path, items)
    fh, fld = faq_block(d['faq'], lang)
    # strip empty faq placeholder heading from body if present
    body_html = re.sub(r'<h2 id="faq"\s*>\s*</h2>', '', d['body'])
    live = badge(tr(lang, 'live'), 'live')
    verified = badge(f'{tr(lang, "verified")} {VDATE[lang]}', 'verified', 'shield')
    srcs = badge(f'{len(m["sources"])} {"official sources" if lang=="en" else ("sumber rasmi" if lang=="ms" else "офиц. источника")}', 'brand')
    langseg = ''
    if alt and len(alt) > 1:
        langseg = '<div class="langseg"><div class="seg">' + ''.join(
            f'<a href="{rel_(path)}{p}" hreflang="{l}"{" aria-current=page" if l==lang else ""}>{esc(LANGS[l]["name"])}</a>' for l, p in alt.items()) + '</div></div>'
    head = f'''<div class="phead"><div class="wrap">{ch}
<div class="titlerow">{ptile(m["platform"], 56)}<div style="flex:1;min-width:0"><h1 class="h-display">{esc(d["h1"])}</h1>
<p class="lead" style="margin-top:10px">{esc(d["lede"])}</p>
<div class="metarow">{live}{verified}{srcs}{langseg}</div></div></div></div></div>'''
    # related guides
    rel_g = [g for g in C.GUIDES if g.get('market') == mid and g.get('lang') == lang][:3]
    if not rel_g: rel_g = [g for g in C.GUIDES if g.get('market') == mid and g.get('lang') == 'en'][:2]
    guides_h = ''
    if rel_g:
        guides_h = f'<section class="blk"><div class="wrap"><div class="sh"><h2 class="h2">{esc(tr(lang,"related"))}</h2></div><div class="cards">{"".join(gcard(path,g,lang) for g in rel_g)}</div></div></section>'
    body = f'''{head}<div class="wrap">{widget(mid, lang)}</div>
{AD(mid + '-1')}
<section class="blk"><div class="wrap"><div class="contentgrid">{toc_html(d["toc"], lang)}
<article class="prose">{body_html}{fh}{sources_block(m["sources"], lang, path)}</article>
{rail_calcs(path, lang, mid)}</div></div></section>
{guides_h}'''
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": d['h1'], "url": BASE + path,
           "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "inLanguage": lang,
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "dateModified": VERIFIED,
           "publisher": {"@type": "Organization", "name": "SellerFee", "url": BASE}}
    w(path, page(path, lang, d['title'], d['desc'], body, [app, fld, cld], alt=alt,
                 scripts=f'<script src="{rel_(path)}assets/engine.js" defer></script>'))

# ---------------------------------------------------------------- guides
def guide_page(g):
    lang = g.get('lang', 'en')
    path = f'{lang}/guides/{g["slug"]}/'
    body_html = g['body']() if callable(g.get('body')) else C.GUIDE_BODY[g['slug']]()
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    toc = [(i, re.sub('<[^>]+>', '', t).replace('&amp;', '&')) for i, t in toc] + [('sources', tr(lang, 'sources'))]
    words = len(re.sub('<[^>]+>', ' ', body_html).split())
    hub = f'{lang}/guides/'
    ch, cld = crumbs(path, [('SellerFee', f'{lang}/'), (tr(lang, 'nav_guides'), hub), (g['short'], None)])
    src = g.get('sources') or C.GUIDE_SOURCES.get(g['slug'], [])
    # related calcs
    calcs = []
    if g.get('market') and g['market'] in MARKETS:
        m = MARKETS[g['market']]; l = lang if lang in m['langs'] else 'en'
        calcs = [(f'{l}/{m["slug"]}/', calc_name(m, lang), '')]
    elif g.get('market') == 'tiktok-shop-my':
        calcs = [('en/tiktok-shop/malaysia/', 'TikTok Shop Malaysia', '')]
    more = [x for x in C.GUIDES if x.get('lang') == lang and x['slug'] != g['slug']][:3]
    byline = f'''<div class="byline"><span class="who"><b>SellerFee</b></span><span class="sep"></span>
<span>{ic("cal",14)}<time datetime="{VERIFIED}">{VFULL[lang]}</time></span>
<span>{ic("clock",14)}{max(3, round(words/220))} {esc(tr(lang,"min_read"))}</span>
<span class="act"><button type="button" class="btn btn-secondary btn-sm" data-copy-link="{esc(tr(lang,"link_copied"))}">{ic("link",14)}{esc(tr(lang,"share_calc"))}</button></span></div>'''
    rail = f'<aside class="rail"><div class="card railcard"><div class="t">{esc(tr(lang,"open_calc"))}</div><ul>' + ''.join(
        f'<li><a href="{rel_(path)}{u}">{esc(t)} {ic("arrow",13)}</a></li>' for u, t, _ in calcs) + '</ul></div></aside>' if calcs else ''
    body = f'''<div class="ahead"><div class="wrap">{ch}
<span class="badge b-brand">{esc(tr(lang,"guide"))}</span>
<h1 class="h-display">{esc(g["title"])}</h1>
<p class="lead">{esc(g["desc"])}</p>{byline}</div></div>
<div class="wrap alayout"><div class="contentgrid">{toc_html(toc, lang)}
<article class="prose">{body_html}{sources_block(src, lang, path)}</article>{rail}</div>
{('<section class="blk"><div class="sh"><h2 class="h2">' + esc(tr(lang,"related")) + '</h2></div><div class="cards">' + ''.join(gcard(path,x,lang) for x in more) + '</div></section>') if more else ''}
</div>'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "description": g['desc'],
           "datePublished": VERIFIED, "dateModified": VERIFIED, "inLanguage": lang, "mainEntityOfPage": BASE + path,
           "image": BASE + "assets/og.png", "author": {"@type": "Organization", "name": "SellerFee", "url": BASE},
           "publisher": {"@type": "Organization", "name": "SellerFee", "logo": {"@type": "ImageObject", "url": BASE + "assets/favicon.svg"}}}
    w(path, page(path, lang, g['title'] + ' | SellerFee', g['desc'], body, [art, cld], og_type='article'))

def guides_index(lang='en'):
    path = f'{lang}/guides/'
    ch, cld = crumbs(path, [('SellerFee', f'{lang}/'), (tr(lang, 'nav_guides'), None)])
    guides = [g for g in C.GUIDES if g.get('lang') == lang]
    if lang == 'ru' and not guides: guides = [g for g in C.GUIDES if g.get('lang') == 'en']
    title = {'en': 'Seller fee guides', 'ms': 'Panduan yuran penjual', 'ru': 'Гайды по комиссиям маркетплейсов'}[lang]
    lede = {'en': 'Plain-English explanations of marketplace fee changes, with worked examples computed from the official rate cards.',
            'ms': 'Penjelasan yuran marketplace dengan contoh dikira daripada kad kadar rasmi.',
            'ru': 'Разборы комиссий маркетплейсов с примерами, посчитанными по официальным тарифам.'}[lang]
    body = f'''<div class="phead"><div class="wrap">{ch}<h1 class="h-display" style="margin-top:18px">{esc(title)}</h1>
<p class="lead" style="margin-top:12px">{esc(lede)}</p></div></div>
<section class="s"><div class="wrap"><div class="cards">{''.join(gcard(path, g, lang) for g in guides)}</div></div></section>'''
    w(path, page(path, lang,
                 {'en': 'Seller Fee Guides for TikTok Shop, Ozon, Wildberries & More | SellerFee',
                  'ms': 'Panduan Yuran Penjual | SellerFee',
                  'ru': 'Гайды по комиссиям Ozon, Wildberries, Яндекс Маркет | SellerFee'}[lang],
                 {'en': 'Guides to marketplace fee changes with real worked examples from official rate cards.',
                  'ms': 'Panduan perubahan yuran marketplace dengan contoh sebenar.',
                  'ru': 'Гайды по изменению комиссий с примерами из официальных тарифов.'}[lang],
                 body, [cld]))

# ---------------------------------------------------------------- hubs & home
C_SUM = {
 'tiktok-shop-my': 'New commission table from 31 Oct 2026, 3.78%/4.86% transaction fee, RM0.54 support fee, BXP.',
 'tiktok-shop-ph': '₱5 Order Processing Fee, 1%–1.5% Seller Growth Fee, 2.24% transaction fee, Shipping Service Fee.',
 'tiktok-shop-us': '6% referral fee by category, 5% fine jewelry and Pre-Owned, 3% over $10K.',
 'tiktok-shop-uk': '9% commission, 5% for specified electronics and beauty categories.',
 'etsy': '6.5% transaction fee, US$0.20 listing fee and payment processing for 60+ bank countries.',
 'ozon': 'FBO/FBS/realFBS commission by category & price band, logistics from 30 Oct 2026, last-mile 25 ₽.',
 'wildberries': 'КВВ by subject (FBW/FBS/DBS), logistics 46+14 ₽/L × warehouse coefficient.',
 'yandex-market': 'Placement by category, 42% low-price tariff, delivery 5%, middle mile, payment transfer.',
}
C_SUM_RU = {
 'ozon': 'Вознаграждение FBO/FBS/realFBS по категориям и ценам, логистика с 30 окт. 2026, последняя миля 25 ₽.',
 'wildberries': 'КВВ по предметам (FBW/FBS/DBS), логистика 46+14 ₽/л × коэффициент склада.',
 'yandex-market': 'Размещение по категориям, тариф 42%, доставка 5%, средняя миля, перевод платежа.',
}

def home():
    path = 'en/'
    # Quick-calc: real links to live calculators (not a fake widget)
    tabs = [('en/tiktok-shop/malaysia/', 'tiktok-shop', 'TikTok MY', True),
            ('en/ozon/', 'ozon', 'Ozon', True),
            ('en/wildberries/', 'wildberries', 'Wildberries', True),
            ('en/yandex-market/', 'yandex-market', 'Yandex Market', True),
            ('en/etsy/', 'etsy', 'Etsy', True)]
    qc_tabs = ''.join(f'<a class="{"on" if i==0 else ""}" href="{u}">{ptile(p,18)}{esc(n)}</a>' for i,(u,p,n,_) in enumerate(tabs))
    pv = compute('tiktok-shop-my', sel='Beauty & Personal Care › Skincare', period='new', price=39.90, cost=12)
    RM = lambda v: money(v, 'MYR')
    qc = f'''<div class="card qc"><div class="qc-tabs">{qc_tabs}</div>
<div class="body"><div class="eyebrow">Example · TikTok Shop Malaysia · from 31 Oct 2026</div>
<div class="chips"><a class="chip on" href="tiktok-shop/malaysia/">Skincare</a>
<a class="chip" href="tiktok-shop/malaysia/">Marketplace</a>
<a class="chip" href="tiktok-shop/malaysia/">RM 39.90</a>
<a class="chip" href="tiktok-shop/malaysia/">Open →</a></div></div>
<div class="qres"><div class="row"><div><span class="small muted">Estimated profit</span><div class="v h-display pos">{RM(pv['profit'])}</div>
<span class="small muted">{pv['margin']:.1f}% margin · fees {RM(pv['total'])}</span></div>
<a class="btn btn-brand" href="tiktok-shop/malaysia/">Open calculator {ic("arrow",15)}</a></div></div></div>'''
    # platform grid
    def prow(mid):
        m = MARKETS[mid]
        note = 'New rates 31 Oct' if mid == 'tiktok-shop-my' else f'Verified {VDATE["en"]}'
        nb = f'<span class="badge b-new" style="height:22px;font-size:12px">{note}</span>' if mid == 'tiktok-shop-my' else f'<span class="r">{note}</span>'
        return f'<a class="mrow" href="{m["slug"]}/"><span class="flag" style="font-size:18px">{m["flag"]}</span><span class="nm">{esc(m["marketName"] if m["market"]!="GLOBAL" else "Global")}</span>{nb}{badge("Live","live")}</a>'
    tt = ''.join(prow(k) for k in MARKETS if MARKETS[k]['platform']=='tiktok-shop')
    for p, mk, f in COMING:
        if p == 'TikTok Shop':
            tt += f'<div class="mrow off"><span class="flag" style="font-size:18px">{f}</span><span class="nm">{esc(mk)}</span>{badge("Coming soon","soon")}</div>'
    ru = ''.join(f'<a class="mrow" href="{MARKETS[k]["slug"]}/"><span class="flag" style="font-size:18px">{MARKETS[k]["flag"]}</span><span class="nm">{esc(MARKETS[k]["platformName"])}</span><span class="r">Verified {VDATE["en"]}</span>{badge("Live","live")}</a>' for k in ('ozon','wildberries','yandex-market'))
    others = [('etsy', True), ('shopee', False), ('lazada', False), ('amazon', False), ('ebay', False)]
    ohtml = ''
    for name, live in others:
        if live:
            m = MARKETS['etsy']
            ohtml += f'''<a class="card ccard" href="{m["slug"]}/"><div class="top">{ptile("etsy",40)}{badge("Live","live")}</div>
<h3>Etsy</h3><p>{esc(C_SUM["etsy"])}</p><div class="go">Open calculator {ic("arrow",14)}</div></a>'''
        else:
            req = issue_url(f'Calculator request: {name.title()}', f'Please add a fee calculator for {name.title()}.')
            ohtml += f'''<a class="card ccard" href="{req}" rel="noopener"><div class="top">{ptile(name,40)}{badge("Coming soon","soon")}</div>
<h3>{name.title()}</h3><p>Rates will be added once they can be verified against official sources.</p>
<div class="go soon">{ic("bell",14)} Request this calculator</div></a>'''
    # source register
    srcs = [
     ('🇲🇾', 'TikTok Shop MY', 'Commission Fee & Seller Fees', 'Updated 16 Oct 2026', 'en/tiktok-shop/malaysia/#sources'),
     ('🇵🇭', 'TikTok Shop PH', 'Introduction to Seller Fees', 'Updated 13 Oct 2026', 'en/tiktok-shop/philippines/#sources'),
     ('🇺🇸', 'TikTok Shop US', 'Referral Fees by Category', 'Revised 8 Oct 2026', 'en/tiktok-shop/us/#sources'),
     ('🇬🇧', 'TikTok Shop UK', 'Commission Rate Policy', 'Dated 18 Sep 2025', 'en/tiktok-shop/uk/#sources'),
     ('🌐', 'Etsy', 'Fee Basics · Payment Processing', 'Etsy Help Center', 'en/etsy/#sources'),
     ('🇷🇺', 'Ozon', 'Commissions XLSX 28 Aug · Logistics 30 Oct', 'Seller Edu', 'en/ozon/#sources'),
     ('🇷🇺', 'Wildberries', 'КВВ PDF 7 Jul · Logistics instructions', 'Updated 19 Oct 2026', 'en/wildberries/#sources'),
     ('🇷🇺', 'Yandex Market', 'Placement · FBY/FBS · Acquiring', 'As published 26 Oct 2026', 'en/yandex-market/#sources'),
    ]
    srows = ''.join(f'<tr><td><span class="flag">{f}</span> <b>{esc(m)}</b></td><td><a href="{u}">{esc(d)} {ic("ext",13)}</a><span class="sub">{esc(note)}</span></td><td>{badge("Checked "+VDATE["en"],"verified","shield")}</td></tr>' for f,m,d,note,u in srcs)
    guides = [g for g in C.GUIDES if g.get('lang') == 'en'][:6]
    body = f'''<section class="hero"><div class="wrap">
<div><div class="announce">{badge("New","new")}<span>Russia live: Ozon, Wildberries, Yandex Market · <a href="russia/">See calculators {ic("arrow",13)}</a></span></div>
<h1 class="h-display">Know exactly what every marketplace takes from your sale.</h1>
<p class="lead">SellerFee turns official marketplace rate cards into fast calculators. Pick your platform, enter a price, and see every fee, your payout and your real margin.</p>
<div class="ctas"><a class="btn btn-primary btn-lg" href="tiktok-shop/malaysia/">{ic("calc",16)} TikTok Shop Malaysia</a>
<a class="btn btn-secondary btn-lg" href="russia/">Russia marketplaces</a></div>
<div class="checks"><span>{ic("check",15)} Official sources only</span><span>{ic("check",15)} Verified {VDATE["en"]}</span><span>{ic("check",15)} Free, no sign-up</span></div></div>
{qc}</div></section>
<div class="stats"><div class="wrap" style="display:contents">
<div><b>8</b><span>Live calculators</span></div>
<div><b>3</b><span>Russia marketplaces</span></div>
<div><b>16k+</b><span>Category rates loaded</span></div>
<div><b>0</b><span>Invented figures</span></div>
</div></div>
<section class="s" id="calculators"><div class="wrap">
<div class="sh"><div><p class="eyebrow">Calculators</p><h2 class="h2">Platforms &amp; markets</h2></div>
<a class="btn btn-link" href="rate-changes/">Rate changes {ic("arrow",14)}</a></div>
<div class="pgrid">
<div class="card pcard"><div class="ph">{ptile("tiktok-shop",40)}<div><b>TikTok Shop</b><div class="small muted">4 live markets</div></div></div>{tt}
<a class="mrow" href="tiktok-shop/" style="border-top:1px solid var(--line);margin-top:4px"><span class="nm" style="color:var(--brand-600)">All TikTok Shop markets</span>{ic("arrow",14)}</a></div>
<div class="card pcard"><div class="ph">{ptile("ozon",40)}<div><b>Russia</b><div class="small muted">Ozon · WB · Yandex</div></div></div>{ru}
<a class="mrow" href="russia/" style="border-top:1px solid var(--line);margin-top:4px"><span class="nm" style="color:var(--brand-600)">Russia hub</span>{ic("arrow",14)}</a></div>
<div class="stackcol">{ohtml}</div>
</div></div></section>
<section class="s trust"><div class="wrap"><div class="tgrid">
<div><p class="eyebrow">Trust</p><h2 class="h2">Numbers you can check</h2>
<div class="step"><span class="n">1</span><div><b>Official sources only</b><p>Every rate comes from the platform’s own seller help. If we can’t verify it, we don’t publish the calculator.</p></div></div>
<div class="step"><span class="n">2</span><div><b>Dated and re-checked</b><p>Each page shows when its rates were last verified. Old and new rates sit side by side when fees change.</p></div></div>
<div class="step"><span class="n">3</span><div><b>Every fee, not just commission</b><p>Transaction, processing, logistics, caps and tiers — and you can edit any rate to match your account.</p></div></div></div>
<div class="card reg"><div class="hd"><b>Source register</b><span class="small muted">Checked {VDATE["en"]}</span></div>
<div class="tscroll"><table class="t"><thead><tr><th>Market</th><th>Source</th><th>Status</th></tr></thead><tbody>{srows}</tbody></table></div></div>
</div></div></section>
<section class="s"><div class="wrap"><div class="sh"><div><p class="eyebrow">Guides</p><h2 class="h2">Latest guides</h2></div>
<a class="btn btn-link" href="guides/">All guides {ic("arrow",14)}</a></div>
<div class="cards">{''.join(gcard(path, g, 'en') for g in guides)}</div>
<div class="cta"><div><h2 class="h-display">Need a market we don’t cover yet?</h2>
<p>Open a GitHub issue with the platform and the official rate page. We only publish after we can verify the numbers.</p></div>
<div class="btns"><a class="btn btn-secondary btn-lg" href="{issue_url("Calculator request: ", "Platform:\nMarket:\nLink to official rates:")}" rel="noopener">{ic("bell",16)} Request a calculator</a>
<a class="btn btn-brand btn-lg" href="about/">How we verify rates</a></div></div>
</div></section>'''
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "SellerFee", "url": BASE, "inLanguage": "en"}
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "SellerFee", "url": BASE, "logo": BASE + "assets/favicon.svg"}
    w(path, page(path, 'en', 'SellerFee: Fee & Profit Calculators for TikTok Shop, Ozon, Wildberries & More',
                 'Free fee and profit calculators for cross-border sellers: TikTok Shop, Ozon, Wildberries, Yandex Market and Etsy. Official rates, dated and sourced.',
                 body, [site, org], alt={'en': 'en/', 'ms': 'ms/', 'ru': 'ru/'}))

def home_ms():
    path = 'ms/'
    body = f'''<section class="hero"><div class="wrap" style="grid-template-columns:1fr">
<div><p class="eyebrow">Kalkulator yuran &amp; untung untuk penjual</p>
<h1 class="h-display">Ketahui dengan tepat berapa yang diambil oleh marketplace daripada jualan anda.</h1>
<p class="lead">SellerFee menukar kad kadar rasmi marketplace kepada kalkulator yang pantas.</p>
<div class="ctas"><a class="btn btn-primary btn-lg" href="tiktok-shop/malaysia/">Kalkulator TikTok Shop Malaysia</a>
<a class="btn btn-secondary btn-lg" href="../en/">Semua kalkulator (English)</a></div>
<div class="checks"><span>{ic("check",15)} Kadar rasmi Seller University</span><span>{ic("check",15)} Disahkan {VDATE["ms"]}</span><span>{ic("check",15)} Percuma</span></div></div></div></section>
<section class="s"><div class="wrap"><h2 class="h2">Kalkulator dalam Bahasa Melayu</h2>
<div class="cards"><a class="card ccard" href="tiktok-shop/malaysia/"><div class="top">{ptile("tiktok-shop",40)}{badge("Aktif","live")}</div>
<h3>TikTok Shop Malaysia</h3><p>Jadual komisen baharu mulai 31 Okt 2026, yuran transaksi 3.78%/4.86%, Yuran Sokongan Platform RM0.54 dan BXP.</p>
<div class="go">Buka kalkulator {ic("arrow",14)}</div></a></div>
<p class="muted" style="margin-top:18px">Kalkulator untuk Filipina, AS, UK, Etsy dan Rusia tersedia dalam bahasa Inggeris (dan Rusia).</p></div></section>'''
    w(path, page(path, 'ms', 'SellerFee: Kalkulator Yuran & Untung untuk Penjual TikTok Shop',
                 'Kalkulator yuran dan untung percuma untuk penjual e-dagang, bermula dengan TikTok Shop Malaysia. Kadar rasmi, bertarikh dan bersumber.',
                 body, alt={'en': 'en/', 'ms': 'ms/', 'ru': 'ru/'}))

def home_ru():
    path = 'ru/'
    tabs = ''.join(f'<a class="{"on" if i==0 else ""}" href="{u}">{ptile(p,18)}{esc(n)}</a>' for i,(u,p,n) in enumerate([
        ('ozon/', 'ozon', 'Ozon'), ('wildberries/', 'wildberries', 'Wildberries'), ('yandex-market/', 'yandex-market', 'Яндекс Маркет')]))
    oz = compute('ozon', price=1500, cost=450, vol=1.5)
    qc = f'''<div class="card qc"><div class="qc-tabs">{tabs}</div>
<div class="body"><div class="eyebrow">Пример · Ozon FBO · косметика</div>
<div class="chips"><a class="chip on" href="ozon/">FBO</a><a class="chip" href="ozon/">1 500 ₽</a><a class="chip" href="ozon/">1,5 л</a><a class="chip" href="ozon/">Открыть →</a></div></div>
<div class="qres"><div class="row"><div><span class="small muted">Оценка прибыли</span><div class="v h-display pos">{money(oz['profit'],'RUB',lang='ru')}</div>
<span class="small muted">{oz['margin']:.1f}% маржа · комиссии {money(oz['total'],'RUB',lang='ru')}</span></div>
<a class="btn btn-brand" href="ozon/">Открыть калькулятор {ic("arrow",15)}</a></div></div></div>'''
    cards = ''.join(f'''<a class="card ccard" href="{MARKETS[k]["slug"]}/"><div class="top">{ptile(k,40)}{badge("Актуально","live")}</div>
<h3>{esc({"ozon":"Ozon","wildberries":"Wildberries","yandex-market":"Яндекс Маркет"}[k])}</h3>
<p>{esc(C_SUM_RU[k])}</p><div class="go">Открыть калькулятор {ic("arrow",14)}</div></a>''' for k in ('ozon','wildberries','yandex-market'))
    guides = [g for g in C.GUIDES if g.get('lang') == 'ru']
    body = f'''<section class="hero"><div class="wrap">
<div><div class="announce">{badge("Новое","new")}<span>Логистика Ozon FBO/FBS с 30 октября 2026 · <a href="ozon/">Посчитать {ic("arrow",13)}</a></span></div>
<h1 class="h-display">Считайте комиссии Ozon, Wildberries и Яндекс Маркета по официальным тарифам.</h1>
<p class="lead">SellerFee загружает актуальные ставки из Seller Edu, PDF КВВ и справки Маркета. Укажите цену — получите каждую комиссию, выплату и маржу.</p>
<div class="ctas"><a class="btn btn-primary btn-lg" href="ozon/">{ic("calc",16)} Ozon</a>
<a class="btn btn-secondary btn-lg" href="wildberries/">Wildberries</a>
<a class="btn btn-secondary btn-lg" href="yandex-market/">Яндекс Маркет</a></div>
<div class="checks"><span>{ic("check",15)} Только официальные источники</span><span>{ic("check",15)} Проверено {VDATE["ru"]}</span><span>{ic("check",15)} Бесплатно</span></div></div>
{qc}</div></section>
<section class="s" id="calculators"><div class="wrap"><div class="sh"><div><p class="eyebrow">Калькуляторы</p><h2 class="h2">Российские маркетплейсы</h2></div></div>
<div class="cards">{cards}</div></div></section>
<section class="s"><div class="wrap"><div class="sh"><div><p class="eyebrow">Гайды</p><h2 class="h2">Разборы тарифов</h2></div>
<a class="btn btn-link" href="guides/">Все гайды {ic("arrow",14)}</a></div>
<div class="cards">{''.join(gcard(path, g, 'ru') for g in guides)}</div></div></section>'''
    w(path, page(path, 'ru', 'SellerFee: калькуляторы комиссий Ozon, Wildberries и Яндекс Маркета',
                 'Бесплатные калькуляторы комиссий и прибыли для продавцов Ozon, Wildberries и Яндекс Маркета. Официальные тарифы, с датой проверки.',
                 body, alt={'en': 'en/', 'ms': 'ms/', 'ru': 'ru/'}))

def tiktok_hub():
    path = 'en/tiktok-shop/'
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('TikTok Shop', None)])
    cards = ''.join(f'''<a class="card ccard" href="{m["slug"].split("/")[1]}/"><div class="top"><span class="flag" style="font-size:28px">{m["flag"]}</span>{badge("Live","live")}</div>
<h3>TikTok Shop {m["marketName"]}</h3><p>{esc(C_SUM[k])}</p><div class="go">Open calculator {ic("arrow",14)}</div></a>'''
                    for k, m in MARKETS.items() if m['platform'] == 'tiktok-shop')
    soon = ''.join(f'''<div class="card ccard"><div class="top"><span class="flag" style="font-size:28px">{f}</span>{badge("Coming soon","soon")}</div>
<h3>TikTok Shop {esc(mk)}</h3><p>Published only after rates are verified on TikTok Seller University.</p>
<div class="go soon">{ic("bell",14)} Request</div></div>''' for p, mk, f in COMING if p == 'TikTok Shop')
    rows = ''.join(f'<tr><td>{m["flag"]} <a href="{m["slug"].split("/")[1]}/">{m["marketName"]}</a></td><td>{esc(C_SUM[k])}</td></tr>'
                   for k, m in MARKETS.items() if m['platform'] == 'tiktok-shop')
    guides = [g for g in C.GUIDES if g.get('lang') == 'en' and (g.get('market') or '').startswith('tiktok')]
    body = f'''<div class="phead"><div class="wrap">{ch}
<h1 class="h-display" style="margin-top:18px">TikTok Shop fee calculators by country</h1>
<p class="lead" style="margin-top:12px">Different fees in every market: category commission in Southeast Asia, a flat referral fee in the US and a single commission rate in the UK.</p></div></div>
<section class="s"><div class="wrap"><div class="cards">{cards}{soon}</div>
<h2 class="h2" style="margin-top:48px">How fees differ by market</h2>
<div class="tablewrap"><table><thead><tr><th>Market</th><th>Main fees</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="sh" style="margin-top:48px"><h2 class="h2">Guides</h2></div>
<div class="cards">{''.join(gcard(path, g, 'en') for g in guides)}</div></div></section>'''
    w(path, page(path, 'en', 'TikTok Shop Fee Calculators: Malaysia, Philippines, US & UK | SellerFee',
                 'Free TikTok Shop seller fee calculators for Malaysia, the Philippines, the United States and the United Kingdom, built on official Seller University rate cards.',
                 body, [cld]))

def russia_hub():
    path = 'en/russia/'
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('Russia', None)])
    cards = ''.join(f'''<a class="card ccard" href="../{MARKETS[k]["slug"]}/"><div class="top">{ptile(k,40)}{badge("Live","live")}</div>
<h3>{esc(MARKETS[k]["platformName"])}</h3><p>{esc(C_SUM[k])}</p><div class="go">Open calculator {ic("arrow",14)}</div></a>'''
                    for k in ('ozon', 'wildberries', 'yandex-market'))
    guides = [g for g in C.GUIDES if g.get('lang') == 'en' and g.get('market') in ('ozon', 'wildberries', 'yandex-market')]
    body = f'''<div class="phead"><div class="wrap">{ch}
<h1 class="h-display" style="margin-top:18px">Russia marketplace fee calculators</h1>
<p class="lead" style="margin-top:12px">Ozon, Wildberries and Yandex Market — FBO/FBS-style models, category commission, logistics and payment fees in rubles, from official seller documents.</p>
<p class="muted" style="margin-top:8px">Also available in <a href="../../ru/">Русский</a>.</p></div></div>
<section class="s"><div class="wrap"><div class="cards">{cards}</div>
<div class="sh" style="margin-top:48px"><h2 class="h2">Guides</h2><a class="btn btn-link" href="../guides/">All guides {ic("arrow",14)}</a></div>
<div class="cards">{''.join(gcard(path, g, 'en') for g in guides)}</div></div></section>'''
    w(path, page(path, 'en', 'Russia Fee Calculators: Ozon, Wildberries & Yandex Market | SellerFee',
                 'Free fee and profit calculators for Ozon, Wildberries and Yandex Market sellers. Official category tariffs, logistics and payment fees in RUB.',
                 body, [cld], alt={'en': 'en/russia/', 'ru': 'ru/'}))

def rate_changes():
    path = 'en/rate-changes/'
    ch, cld = crumbs(path, [('SellerFee', 'en/'), ('Rate changes', None)])
    rows = [
     ('30 Oct 2026', 'Ozon', 'FBO/FBS logistics tariffs', 'New cluster × volume × price-band table', 'en/ozon/'),
     ('31 Oct 2026', 'TikTok Shop MY', 'Category commission', 'New commission table (side-by-side with old rates in the calculator)', 'en/tiktok-shop/malaysia/'),
     ('19 Oct 2026', 'Wildberries', 'Logistics instructions', 'Page updated; base tariff × coefficient unchanged since 15 Aug', 'en/wildberries/'),
     ('11 Oct – 31 Dec 2026', 'Yandex Market', 'FBY storage', 'Storage free in this window', 'en/yandex-market/'),
     ('End of 2026', 'Yandex Market', '42% low-price tariff', '≤300 ₽ and ≤5 L on FBY/FBS', 'en/yandex-market/'),
     ('7 Jul 2026', 'Wildberries', 'КВВ table', 'Subject commission PDF currently in force', 'en/wildberries/'),
     ('28 Aug 2026', 'Ozon', 'Category commission XLSX', 'Price-band rates currently loaded', 'en/ozon/'),
    ]
    trs = ''.join(f'<tr><td class="nowrap">{esc(d)}</td><td><b>{esc(p)}</b></td><td>{esc(w)}</td><td>{esc(n)}</td><td><a href="../{u.split("/",1)[1]}">Calculator {ic("arrow",13)}</a></td></tr>' for d,p,w,n,u in rows)
    body = f'''<div class="phead"><div class="wrap">{ch}
<h1 class="h-display" style="margin-top:18px">Rate changes</h1>
<p class="lead" style="margin-top:12px">Dated fee changes that affect the live calculators. Every row links to the calculator and its official sources.</p></div></div>
<section class="s"><div class="wrap"><div class="tablewrap"><table>
<thead><tr><th>When</th><th>Platform</th><th>What</th><th>Detail</th><th></th></tr></thead>
<tbody>{trs}</tbody></table></div>
<p class="muted" style="margin-top:16px">Last register check: {VFULL["en"]}. Found a change we missed? <a href="{issue_url("Rate change: ", "Platform:\nEffective date:\nLink to official source:")}">Open an issue</a>.</p></div></section>'''
    w(path, page(path, 'en', 'Marketplace Rate Changes (2026) | SellerFee',
                 'Dated marketplace fee changes for TikTok Shop, Ozon, Wildberries and Yandex Market, linked to the calculators that use them.',
                 body, [cld]))

def static_pages():
    about = f'''
<p>SellerFee is an independent website that publishes free fee and profit calculators for people who sell on online marketplaces, especially sellers working across borders. We cover TikTok Shop (MY, PH, US, UK), Etsy, and the Russian marketplaces Ozon, Wildberries and Yandex Market.</p>
<h2 id="how-we-source-rates">How we source rates</h2>
<p>Every rate comes from the platform’s own seller help — TikTok Shop Seller University, Etsy Help, Ozon Seller Edu, Wildberries instructions and КВВ PDF, Yandex Market help. Each calculator links its sources and shows the date we last checked them. When a platform publishes a rate but not the formula, we say so and make the rate editable. We don’t publish a calculator until rates can be verified from an official source.</p>
<h2>How we keep them current</h2>
<p>We re-check source pages regularly and whenever a platform announces a change. When fees change, we keep old rates alongside new ones where the platform still publishes both, and we note the effective date on <a href="../rate-changes/">Rate changes</a>.</p>
<h2>How the calculators work</h2>
<p>The calculators run entirely in your browser. Nothing you type is sent to us. Results are estimates based on published rates; your account may have waivers, program fees or promotions that change the numbers, so your seller cabinet is always the final word.</p>
<h2>Independence</h2>
<p>SellerFee is not affiliated with TikTok, Etsy, Ozon, Wildberries, Yandex or any other marketplace. We don’t take listing fees or referral kickbacks for calculator results.</p>
<p>Found a wrong rate? <a href="{issue_url("Wrong rate: ", "Page:\nWhich fee:\nOfficial source:")}">Open a GitHub issue</a> with the page and the official source.</p>
'''
    P = {
     'about': ('About SellerFee', 'About SellerFee: who we are, how we verify marketplace fee rates and how the calculators work.', about),
     'privacy': ('Privacy', 'SellerFee privacy notice: calculators run in your browser; we don’t collect the numbers you type.', f'''
<p>Last updated {VERIFIED_H}.</p>
<p>SellerFee calculators run entirely in your browser. The prices, costs and rates you enter are not sent to our servers. We don’t run an account system and we don’t sell personal data.</p>
<h2>Logs and hosting</h2>
<p>Like most static sites, our host may keep standard access logs (IP address, URL, user agent). We use them only to keep the site reliable.</p>
<h2>Cookies</h2>
<p>We don’t set analytics or advertising cookies. The language you pick is not stored as a tracking cookie.</p>
<h2>Contact</h2>
<p>Questions: use the <a href="../contact/">contact page</a> or open a GitHub issue on the project repository.</p>
'''),
     'terms': ('Terms of use', 'Terms of use for SellerFee calculators and guides.', f'''
<p>Last updated {VERIFIED_H}.</p>
<p>By using SellerFee you agree to these terms.</p>
<h2>Estimates, not advice</h2>
<p>Our calculators and guides provide estimates based on fee rates published by each marketplace on the date shown. They are for general information only and are not financial, tax, accounting or legal advice. Your actual fees can differ because of your account type, category assignment, programs, waivers, promotions, taxes, currency conversion or changes the platform makes after our last check. Always confirm fees in your marketplace account before making pricing or business decisions.</p>
<h2>No warranty</h2>
<p>The site is provided “as is” without warranties of any kind. We do our best to keep rates accurate and current but do not guarantee that they are complete, correct or up to date.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, SellerFee is not liable for any loss arising from your use of, or reliance on, the site or its results.</p>
<h2>Trademarks</h2>
<p>TikTok, TikTok Shop, Etsy, Shopee, Lazada, Amazon, eBay, Ozon, Wildberries and Yandex Market are trademarks of their respective owners. SellerFee is independent and not affiliated with or endorsed by them.</p>
<h2>Acceptable use</h2>
<p>You may use the calculators freely for your own business. Please don’t scrape the site at a rate that disrupts it or republish our content as your own.</p>
<h2>Changes</h2>
<p>We may update these terms; the date above shows the latest version.</p>
'''),
     'contact': ('Contact', 'Contact SellerFee about rate errors, calculator requests or the project.', f'''
<p>SellerFee is a small independent project.</p>
<ul>
<li><b>Wrong rate on a page</b> — <a href="{issue_url("Wrong rate: ", "Page:\nWhich fee looks wrong:\nLink to the official source:")}">open a GitHub issue</a> with the page URL and the official source.</li>
<li><b>Request a calculator</b> — <a href="{issue_url("Calculator request: ", "Platform:\nMarket:\nLink to official rates:")}">tell us the platform and the official rate page</a>.</li>
<li><b>Everything else</b> — open an issue on <a href="https://github.com/xhq52465840/tiktok-shop-fee-calculator">the GitHub repository</a>.</li>
</ul>
'''),
    }
    for slug, (title, desc, html) in P.items():
        path = f'en/{slug}/'
        ch, cld = crumbs(path, [('SellerFee', 'en/'), (title, None)])
        w(path, page(path, 'en', f'{title} | SellerFee', desc,
                     f'<div class="wrap narrow spage">{ch}<article class="prose"><h1>{esc(title)}</h1>{html}</article></div>', [cld]))

def plumbing():
    open(os.path.join(ROOT, 'index.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>SellerFee</title>
<link rel="canonical" href="{BASE}en/">
<link rel="alternate" hreflang="en" href="{BASE}en/"><link rel="alternate" hreflang="ms" href="{BASE}ms/"><link rel="alternate" hreflang="ru" href="{BASE}ru/"><link rel="alternate" hreflang="x-default" href="{BASE}en/">
<meta http-equiv="refresh" content="0; url=en/"><meta name="robots" content="noindex,follow">
<script>(function(){{var l=(navigator.language||'').toLowerCase();location.replace(l.indexOf('ru')===0?'ru/':l.indexOf('ms')===0?'ms/':'en/')}})()</script></head>
<body><a href="en/">SellerFee</a> · <a href="ru/">Русский</a> · <a href="ms/">Bahasa Melayu</a></body></html>''')
    for old, new in [('malaysia/', 'en/tiktok-shop/malaysia/'), ('philippines/', 'en/tiktok-shop/philippines/')]:
        w(old, f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="{BASE}{new}"><meta http-equiv="refresh" content="0; url=../{new}"><meta name="robots" content="noindex"></head><body><a href="../{new}">This page has moved.</a></body></html>')
    open(os.path.join(ROOT, '404.html'), 'w').write(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | SellerFee</title><meta name="robots" content="noindex">
<script>var b=location.hostname.endsWith('github.io')?'/tiktok-shop-fee-calculator/':'/';document.write('<base href="'+b+'">')</script><link rel="stylesheet" href="assets/style.css"></head>
<body><main class="wrap narrow spage"><h1>Page not found</h1><p>The page you’re looking for doesn’t exist or has moved.</p><p><a class="btn btn-primary" href="en/">Go to the calculators</a></p></main></body></html>''')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, alt in PAGES:
        sm.append(f'  <url><loc>{BASE}{path}</loc><lastmod>{VERIFIED}</lastmod>')
        if alt:
            for l, p in alt.items(): sm.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{p}"/>')
            sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{alt.get("en", list(alt.values())[0])}"/>')
        sm.append('  </url>')
    sm.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(ROOT, 'assets', 'favicon.svg'), 'w').write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
    os.makedirs(os.path.join(ROOT, 'deploy'), exist_ok=True)
    open(os.path.join(ROOT, 'deploy', 'CNAME'), 'w').write('sellerfee.app\n')
    open(os.path.join(ROOT, 'CNAME'), 'w').write('sellerfee.app\n')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')

if __name__ == '__main__':
    clean(); copy_rates()
    home(); home_ms(); home_ru(); tiktok_hub(); russia_hub(); rate_changes()
    for mid, m in MARKETS.items():
        for lang in m['langs']: calc_page(mid, lang)
    for lang in ('en', 'ru'): guides_index(lang)
    for g in C.GUIDES: guide_page(g)
    static_pages(); plumbing()
    print('built', len(PAGES), 'pages')
