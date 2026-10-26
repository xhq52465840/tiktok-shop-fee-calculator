"""Page shell, calculator widget and shared helpers."""
import json, html, os
from markets import MARKETS, VERIFIED, compute
from site_helpers import money, pct, ex_table
from i18n import S, tr, LANGS
BASE = os.environ.get('SITE_BASE', 'https://sellerfee.app/')
VERIFIED_H = '26 October 2026'
VERIFIED_MS = '26 Oktober 2026'
esc = html.escape
PAGES = []  # (path, lang, alternates{lang:path}, lastmod)

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#0d9488"/><path d="M9 7h14v18l-2.3-1.6L18.4 25l-2.4-1.6L13.6 25l-2.3-1.6L9 25z" fill="#fff"/><circle cx="13.2" cy="12.2" r="1.7" fill="#0d9488"/><circle cx="18.8" cy="18.4" r="1.7" fill="#0d9488"/><path d="M19.6 10.8l-7.2 8.8" stroke="#0d9488" stroke-width="1.8" stroke-linecap="round"/></svg>'

def _unused_money(v, cur="RM", dec=2):
    s = f"{abs(v):,.{dec}f}"
    sym = {'MYR': 'RM', 'PHP': '₱', 'USD': '$', 'GBP': '£'}.get(cur, cur)
    return ('−' if v < 0 else '') + sym + s

def _unused_pct(v):
    s = f"{v:.2f}".rstrip('0').rstrip('.')
    return s + '%'

def rel(path):
    depth = path.strip('/').count('/') + 1 if path.strip('/') else 0
    return '../' * depth

def link(frm, to):
    return rel(frm) + to

def header(lang, path, alt=None):
    r = rel(path); L = lambda k: tr(lang, k)
    nav = [((f'{lang}/tiktok-shop/' if lang == 'en' else 'ms/tiktok-shop/malaysia/'), L('nav_tiktok')), ('en/etsy/', L('nav_etsy')), ('en/guides/', L('nav_guides')), ('en/about/', L('nav_about'))]
    items = ''.join(f'<a href="{r}{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{esc(t)}</a>' for u, t in nav)
    sw = ''
    if alt:
        other = [l for l in alt if l != lang][0]
        sw = f'<a class="lang" href="{r}{alt[other]}" hreflang="{other}" lang="{other}">{esc(LANGS[other]["name"])}</a>'
    return f'''<header class="hdr"><div class="wrap"><a class="logo" href="{r}{lang}/" aria-label="SellerFee home">{LOGO}<span>Seller<b>Fee</b></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">{esc(L('menu'))}</button>
<nav class="nav" id="nav">{items}{sw}</nav></div></header>
'''

def footer(lang, path):
    r = rel(path); L = lambda k: tr(lang, k)
    calcs = ''.join(f'<a href="{r}en/{m["slug"]}/">{esc(m["platformName"])} {esc(m["marketName"]) if m["market"]!="GLOBAL" else ""}</a>' for m in MARKETS.values())
    from content import GUIDES
    guides = ''.join(f'<a href="{r}en/guides/{g["slug"]}/">{esc(g["short"])}</a>' for g in GUIDES[:4])
    return f'''<footer class="ftr"><div class="wrap"><div class="cols">
<div><a class="logo" href="{r}{lang}/">{LOGO}<span>Seller<b>Fee</b></span></a><p style="margin-top:12px">{esc(L('f_tag'))}</p></div>
<div><h4>{esc(L('f_tools'))}</h4>{calcs}</div>
<div><h4>{esc(L('f_guides'))}</h4>{guides}<a href="{r}en/guides/">All guides →</a></div>
<div><h4>{esc(L('f_company'))}</h4><a href="{r}en/about/">{esc(L('f_about'))}</a><a href="{r}en/contact/">{esc(L('f_contact'))}</a><a href="{r}en/privacy/">{esc(L('f_privacy'))}</a><a href="{r}en/terms/">{esc(L('f_terms'))}</a></div>
</div><p class="fine">{esc(L('disclaimer'))} {"Rates last verified" if lang=="en" else "Kadar terakhir disahkan"} {VERIFIED_H if lang=="en" else VERIFIED_MS}. © 2026 SellerFee.</p></div></footer>
'''

def page(path, lang, title, desc, body, schema=None, alt=None, og_type='website', scripts=''):
    url = BASE + path
    alts = ''
    if alt:
        alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in alt.items())
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt["en"]}">'
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (schema or []))
    r = rel(path)
    PAGES.append((path, alt))
    return f'''<!doctype html>
<html lang="{LANGS[lang]['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">{alts}
<meta property="og:site_name" content="SellerFee"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og.png"><meta property="og:locale" content="{'ms_MY' if lang=='ms' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0b1324">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(lang, path, alt)}<main id="main">
{body}
</main>
{footer(lang, path)}{scripts}</body>
</html>
'''

def crumbs(path, items):
    r = rel(path)
    h = '<nav class="crumbs" aria-label="Breadcrumb">' + ' / '.join(f'<a href="{r}{u}">{esc(t)}</a>' if u is not None else esc(t) for t, u in items) + '</nav>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": BASE + u} if u is not None else {})} for i, (t, u) in enumerate(items)]}
    return h, ld

def faq_block(faq, lang='en'):
    h = f'<h2 id="faq">{esc(tr(lang, "faq"))}</h2><div class="faq">' + ''.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in faq) + '</div>'
    import re
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faq]}
    return h, ld

def sources_block(src, lang='en'):
    return (f'<h2 id="sources">{esc(tr(lang, "sources"))}</h2><ul class="sources">' +
            ''.join(f'<li><a href="{u}" rel="nofollow noopener" target="_blank">{esc(t)}</a></li>' for t, u in src) +
            f'</ul><p class="muted">{esc(tr(lang, "verified"))}: <time datetime="{VERIFIED}">{VERIFIED_H if lang=="en" else VERIFIED_MS}</time>.</p>')

AD = lambda slot: f'<div class="ad" data-ad-slot="{slot}"></div>'

# ---------------- calculator widget
def fld(lang, id, cur_html, value, hint=None, suffix=None, step='0.01', mode='decimal'):
    pre = f'<span class="sf-cur">{cur_html}</span>' if cur_html else ''
    suf = f'<span class="suf">{suffix}</span>' if suffix else ''
    h = f'<p class="hint">{esc(hint)}</p>' if hint else ''
    return f'<div class="fld"><label for="sf-{id}">{esc(tr(lang, id))}</label><div class="in">{pre}<input id="sf-{id}" type="number" inputmode="{mode}" min="0" step="{step}" value="{value}">{suf}</div>{h}</div>'

def widget(mid, lang):
    m = MARKETS[mid]; L = lambda k: tr(lang, k); d = m['defaults']
    cur = m['symbols'].get(m['currency'], m['currency'])
    curh = cur if not m.get('currencyFromOption') else m['currency']
    inp = m['inputs']
    prod = [f'<div class="fld full"><label for="sf-sel">{esc(L(m["selector"]["label"]))}</label><div class="in"><select id="sf-sel"></select></div><p class="hint" id="sf-selnote"></p></div>']
    prod.append(fld(lang, 'price', curh, d.get('price', 0)))
    prod.append(fld(lang, 'qty', None, 1, step='1', mode='numeric'))
    prod.append(fld(lang, 'sellerDisc', curh, 0, hint=L('sellerDisc_h')))
    prod.append(fld(lang, 'buyerShip', curh, d.get('buyerShip', 0)))
    if 'tax' in inp: prod.append(fld(lang, 'tax', curh, 0, hint=L('tax_h')))
    shop = []
    if m['store']:
        shop.append(f'<div class="fld"><label>{esc(L("store"))}</label><div class="seg" role="radiogroup">' + ''.join(
            f'<label><input type="radio" name="sf-store" value="{v}"{" checked" if i == 0 else ""}><span>{esc(L(k))}</span></label>' for i, (v, k) in enumerate(m['store'])) + '</div></div>')
    if m['periods']:
        shop.append(f'<div class="fld"><label for="sf-period">{esc(L("period"))}</label><div class="in"><select id="sf-period">' + ''.join(
            f'<option value="{v}">{esc(L(k))}</option>' for v, k in m['periods']) + '</select></div></div>')
    for g in m['toggles']:
        shop.append(f'<label class="tg"><input type="checkbox" id="sf-t-{g["id"]}"><span><b>{esc(L("t_" + g["id"]))}</b><small>{esc(L("t_" + g["id"] + "_h"))}</small></span></label>')
    costs = [fld(lang, 'cost', curh, d.get('cost', 0)), fld(lang, 'shipCost', curh, 0)]
    if 'affPct' in inp: costs.append(fld(lang, 'affPct', None, 0, suffix='%', step='0.1'))
    costs.append(fld(lang, 'other', curh, 0, hint=L('other_h')))
    rates = []
    for c in m['components']:
        unit = '%' if c['type'] == 'pct' else (curh + ' ' + (L('u_item') if c.get('per') == 'item' else L('u_order')))
        rates.append(f'<div class="fld sf-rate"><label for="sf-r-{c["id"]}">{esc(L("c_" + c["id"]))}</label><div class="in"><input id="sf-r-{c["id"]}" type="number" step="0.01" min="0"><span class="suf">{esc(unit)}</span></div></div>')
    shop_sec = f'<div class="sec"><h2>{esc(L("sec_shop"))}</h2><div class="fields"><div class="full">{"".join(shop)}</div></div></div>' if shop else ''
    cmp = f'<div class="sec"><h2>{esc(L("cmp_title"))}</h2><div id="sf-compare"></div></div>' if m['compare'] else ''
    cfg = {k: m[k] for k in ('currency', 'symbols', 'locale', 'components', 'toggles', 'defaultOption') if k in m}
    cfg['currencyFromOption'] = m.get('currencyFromOption', False)
    cfg['selector'] = {'options': m['selector']['options']}
    comps = []
    for c in m['components']:
        c2 = dict(c); c2['label'] = L('c_' + c['id']); comps.append(c2)
    cfg['components'] = comps
    if m['compare']:
        C = m['compare']; cfg['compare'] = {'vary': C['vary'], 'a': dict(C['a'], label=L(C['a']['label'])), 'b': dict(C['b'], label=L(C['b']['label'])), 'note': L(C['note'])}
    js = dict(S['en']['js']); js.update(S[lang].get('js', {}))
    return f'''<div class="calc" id="sf-calc">
<div class="panel">
<div class="sec"><h2>{esc(L("sec_product"))}</h2><div class="fields">{"".join(prod)}</div></div>
{shop_sec}
<div class="sec"><h2>{esc(L("sec_costs"))}</h2><div class="fields">{"".join(costs)}</div></div>
<div class="sec"><details class="adv"><summary>{esc(L("sec_rates"))}</summary><p class="hint" style="margin:10px 0 0">{esc(L("rates_h"))}</p><div class="fields">{"".join(rates)}</div></details></div>
</div>
<div class="panel result" aria-live="polite">
<div class="top"><span class="lbl">{esc(L("res_profit"))}</span><b id="sf-k-profit" class="sf-big">–</b><span id="sf-k-margin" class="sf-pill"></span>
<div class="kpis"><div><span>{esc(L("res_fees"))}</span><b id="sf-k-fees">–</b><span id="sf-k-feespct"></span></div><div><span>{esc(L("res_payout"))}</span><b id="sf-k-payout">–</b></div></div></div>
<div class="sec"><h2>{esc(L("res_where"))}</h2><div class="bar" id="sf-bar"></div><ul class="legend" id="sf-legend"></ul></div>
<div class="sec"><h2>{esc(L("res_breakdown"))}</h2><table class="bk"><tbody id="sf-breakdown"></tbody></table></div>
{cmp}
</div>
</div>
<script>window.SF_MARKET={json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))};window.SF_T={json.dumps(js, ensure_ascii=False)};</script>'''
