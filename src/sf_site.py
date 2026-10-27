"""Page shell (header, footer, page template), calculator widget and shared helpers. Visual design: sellerfee-design (approved 26 Oct 2026)."""
import json, html, os, re
import html as H
from markets import MARKETS, VERIFIED, compute
from site_helpers import money, pct, ex_table
from i18n import S, tr, LANGS
import l10n
GUIDES_ALL = []   # filled by build.py: every guide in every language (native or localised)
LORDER = ['en', 'zh', 'ru', 'ms']
BASE = os.environ.get('SITE_BASE', 'https://sellerfee.app/')
REPO = 'https://github.com/xhq52465840/tiktok-shop-fee-calculator'
VERIFIED_H = '26 October 2026'
VDATE = {'en': '26 Oct 2026', 'ms': '26 Okt 2026', 'ru': '26 окт. 2026', 'zh': '2026年10月26日'}
VFULL = {'en': '26 October 2026', 'ms': '26 Oktober 2026', 'ru': '26 октября 2026', 'zh': '2026年10月26日'}
VERIFIED_MS = VFULL['ms']
esc = html.escape
PAGES = []  # (path, alternates{lang:path})

MARK = '<svg class="mark" viewBox="0 0 28 28" aria-hidden="true"><rect width="28" height="28" rx="7.5" fill="#0B1220"/><path d="M19.2 7.6 8.8 20.4" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="9.3" cy="9.3" r="2.7" fill="#fff"/><circle cx="18.7" cy="18.7" r="2.7" fill="#22C58B"/></svg>'
LOGO = MARK.replace(' class="mark"', '').replace(' aria-hidden="true"', '')
P = {
 'chev': '<path d="m6 9 6 6 6-6"/>', 'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
 'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>', 'check': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 'ext': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
 'info': '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>', 'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>', 'cal': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
 'refresh': '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/>',
 'plus': '<path d="M5 12h14M12 5v14"/>', 'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>', 'calc': '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01"/>',
 'alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>', 'book': '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
}
def ic(n, s=16, cls=''):
    return f'<svg class="i{(" " + cls) if cls else ""}" viewBox="0 0 24 24" width="{s}" height="{s}" aria-hidden="true">{P[n]}</svg>'

PLAT = {'tiktok-shop': ('#0B1220', '#fff', 'TS'), 'shopee': ('#EE4D2D', '#fff', 'S'), 'lazada': ('#1B1464', '#fff', 'L'), 'amazon': ('#232F3E', '#FF9900', 'a'),
        'etsy': ('#F1641E', '#fff', 'E'), 'ebay': ('#fff', '#0064D2', 'e'), 'ozon': ('#005BFF', '#fff', 'O'), 'wildberries': ('#A3119B', '#fff', 'WB'),
        'yandex-market': ('#FFDC34', '#0B1220', 'YM')}
def ptile(p, s=36):
    bg, fg, t = PLAT[p]
    bd = 'border:1px solid #E7EAF0;' if bg == '#fff' else ''
    fs = int(s * (.34 if len(t) > 1 else .42))
    return f'<span class="tile" style="width:{s}px;height:{s}px;border-radius:{int(s*.28)}px;background:{bg};color:{fg};{bd}font-size:{fs}px" aria-hidden="true">{t}</span>'

def rel(path):
    # All internal URLs are root-relative ("/en/ozon/"), so they work from any depth,
    # including 404.html which GitHub Pages serves at arbitrary paths.
    return '/'

_URL_ATTR = re.compile(r'''(\b(?:href|src|action)=")([^"]*)(")|(url=)([^"'>;\s]+)''')
_SKIP = ('/', '#', '?', 'http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:', '{')

def rootify(html, path):
    """Rewrite any remaining page-relative href/src/meta-refresh URL to a root-relative one,
    resolved against the page's own URL path (e.g. 'en/russia/')."""
    from urllib.parse import urljoin
    page_url = '/' + path.lstrip('/')
    if path and not path.endswith('/') and not path.endswith('.html'): page_url += '/'
    def fix(u):
        if not u or u.startswith(_SKIP): return u
        return urljoin(page_url, u)
    def sub(m):
        if m.group(1): return m.group(1) + fix(m.group(2)) + m.group(3)
        return m.group(4) + fix(m.group(5))
    return _URL_ATTR.sub(sub, html)

def link(frm, to):
    return rel(frm) + to

def issue_url(title, body=''):
    from urllib.parse import quote
    return f'{REPO}/issues/new?title={quote(title)}&body={quote(body)}'

MKT = {
 'zh': {'Malaysia': '马来西亚', 'Philippines': '菲律宾', 'United States': '美国', 'United Kingdom': '英国', 'Singapore': '新加坡', 'Thailand': '泰国', 'UK': '英国', 'Vietnam': '越南', 'Indonesia': '印度尼西亚'},
 'ru': {'Malaysia': 'Малайзия', 'Philippines': 'Филиппины', 'United States': 'США', 'United Kingdom': 'Великобритания', 'Singapore': 'Сингапур', 'Thailand': 'Таиланд', 'UK': 'Великобритания', 'Vietnam': 'Вьетнам', 'Indonesia': 'Индонезия'},
 'ms': {'Philippines': 'Filipina', 'United States': 'Amerika Syarikat', 'Singapore': 'Singapura'},
}
def market_name(name, lang='en'):
    return MKT.get(lang, {}).get(name, name)

def calc_name(m, lang='en'):
    if m['market'] in ('GLOBAL', 'RU'):
        if lang == 'ru': return {'Yandex Market': 'Яндекс Маркет'}.get(m['platformName'], m['platformName'])
        if lang == 'zh': return {'Yandex Market': 'Yandex Market（Яндекс Маркет）'}.get(m['platformName'], m['platformName'])
        return m['platformName']
    return f'{m["platformName"]} {market_name(m["marketName"], lang)}'

def calc_links(lang):
    """(path, label, platform, flag) for every live calculator, in the page language where one exists."""
    out = []
    for k, m in MARKETS.items():
        l = lang if lang in m['langs'] else 'en'
        out.append((f'{l}/{m["slug"]}/', calc_name(m, lang), m['platform'], m['flag'], k))
    return out

TOPBAR = {
 'en': ('UPDATE', 'TikTok Shop Malaysia commission rates change on <b>31 Oct 2026</b>', 'en/guides/tiktok-shop-malaysia-commission-changes-october-2026/', 'See what changes'),
 'ms': ('BAHARU', 'Kadar komisen TikTok Shop Malaysia berubah pada <b>31 Okt 2026</b>', 'ms/tiktok-shop/malaysia/', 'Lihat perubahan'),
 'ru': ('НОВОЕ', 'Ozon обновляет тарифы логистики FBO и FBS с <b>30 октября 2026</b>', 'ru/ozon/', 'Посчитать'),
 'zh': ('新', 'TikTok Shop 马来西亚佣金费率将于 <b>2026年10月31日</b> 调整', 'zh/guides/tiktok-shop-malaysia-commission-changes-october-2026/', '查看变化'),
}
def topbar(lang, path):
    pill, txt, href, cta = TOPBAR[lang]
    return f'<div class="topbar"><div class="wrap"><span class="pill">{pill}</span><span class="tb-txt">{txt}</span> <a href="{rel(path)}{href}">{cta} {ic("arrow", 13)}</a></div></div>'

NAV = {l: [(f'{l}/rate-changes/', 'nav_rates'), (f'{l}/guides/', 'nav_guides'), (f'{l}/about/', 'nav_about')] for l in ('en', 'ms', 'ru', 'zh')}
def header(lang, path, alt=None):
    r = rel(path); L = lambda k: tr(lang, k)
    cl = calc_links(lang)
    dd = ''.join(f'<a href="{r}{u}">{ptile(p, 22)}<span>{esc(n)}</span></a>' for u, n, p, f, k in cl)
    hub = {'ru': 'ru/', 'zh': 'zh/', 'ms': 'ms/'}.get(lang, 'en/')
    items = f'<details class="dd"><summary>{esc(L("nav_calcs"))}{ic("chev", 14)}</summary><div class="ddm">{dd}<a class="all" href="{r}{hub}#calculators">{esc(L("open_calc"))} {ic("arrow", 13)}</a></div></details>'
    items += ''.join(f'<a href="{r}{u}"{" aria-current=page" if path.startswith(u) else ""}>{esc(L(k))}</a>' for u, k in NAV[lang])
    langs = alt or {lang: path}
    code = lambda l: l.upper()
    lm = ''.join(f'<a href="{r}{p}" hreflang="{LANGS[l]["html"]}" lang="{LANGS[l]["html"]}"{" aria-current=true" if l == lang else ""}>{esc(LANGS[l]["name"])}<span class="code">{code(l)}</span></a>' for l, p in langs.items())
    if not alt: lm += f'<span class="lm-note">{esc({"en": "This page is in English only", "ms": "Halaman ini dalam satu bahasa sahaja", "ru": "Страница доступна только на русском", "zh": "此页仅有当前语言版本"}[lang])}</span>'
    lsw = f'<details class="dd lang"><summary aria-label="{esc(L("language"))}">{ic("globe", 15)}<span class="ln">{esc(LANGS[lang]["name"])}</span><span class="code">{code(lang)}</span>{ic("chev", 14)}</summary><div class="ddm right">{lm}</div></details>'
    return f'''<header class="nav"><div class="wrap"><a class="logo" href="{r}{hub}" aria-label="{esc(L('aria_home'))}">{MARK}<span>SellerFee<span class="tld">.app</span></span></a>
<nav class="menu" id="menu" aria-label="{esc(L('aria_main'))}">{items}</nav>
<div class="right">{lsw}<a class="btn btn-primary btn-sm hide-m" href="{r}{hub}#calculators">{ic("calc", 15)} {esc(L("open_calc_btn"))}</a>
<button class="menu-btn" aria-expanded="false" aria-controls="menu" onclick="var n=document.getElementById('menu');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">{ic("menu", 20)}<span class="sr">{esc(L("menu"))}</span></button></div></div></header>
'''

def footer(lang, path, alt=None):
    r = rel(path); L = lambda k: tr(lang, k)
    from markets import COMING
    calcs = ''.join(f'<li><a href="{r}{u}">{esc(n)}</a></li>' for u, n, p, f, k in calc_links(lang))
    soon = ''.join(f'<li><a href="{issue_url("Calculator request: " + p + " " + mk, "Please add a fee calculator for " + p + " (" + mk + ").")}" rel="noopener">{esc(p)} <span class="muted2">· {l10n.text(lang, esc(mk))}</span></a></li>' for p, mk, f in COMING[:6])
    gl = [(f'{lang}/guides/{g["slug"]}/', g['short']) for g in GUIDES_ALL if g.get('lang', 'en') == lang]
    guides = ''.join(f'<li><a href="{r}{u}">{esc(t)}</a></li>' for u, t in gl[:6])
    company = [(f'{lang}/about/', {'en': 'About SellerFee', 'ms': 'Tentang SellerFee', 'ru': 'О проекте', 'zh': '关于 SellerFee'}[lang]), (f'{lang}/about/#how-we-source-rates', {'en': 'How we verify rates', 'ms': 'Cara kami sahkan kadar', 'ru': 'Как мы проверяем тарифы', 'zh': '我们如何核实费率'}[lang])]
    comp = ''.join(f'<li><a href="{r}{u}">{esc(t)}</a></li>' for u, t in company)
    comp += f'<li><a href="{issue_url("Wrong rate: ", "Page: " + BASE + path + chr(10) + "Which fee looks wrong:" + chr(10) + "Link to the official source:")}" rel="noopener">{esc({"en": "Report a wrong rate", "ms": "Laporkan kadar salah", "ru": "Сообщить об ошибке в тарифе", "zh": "反馈错误费率"}[lang])}</a></li>'
    comp += ''.join(f'<li><a href="{r}{lang}/{s}/">{esc(L(k))}</a></li>' for s, k in [('privacy', 'f_privacy'), ('terms', 'f_terms'), ('contact', 'f_contact')])
    tgt = alt or {l: f'{l}/' for l in LANGS}
    langs = ''.join(f'<a class="{"on" if l == lang else ""}" href="{r}{tgt[l]}" hreflang="{v["html"]}" lang="{v["html"]}"{" aria-current=true" if l == lang else ""}>{esc(v["name"])}</a>' for l, v in LANGS.items() if l in tgt)
    soon_h = {'en': 'Coming soon', 'ms': 'Akan datang', 'ru': 'Скоро', 'zh': '即将上线'}[lang]
    return f'''<footer class="footer"><div class="wrap"><div class="grid"><div><a class="logo" href="{r}{lang}/">{MARK}<span>SellerFee<span class="tld">.app</span></span></a>
<p class="ftag">{esc(L('f_tag'))}</p><div class="langs">{langs}</div></div>
<div><h2>{esc(L('f_tools'))}</h2><ul>{calcs}</ul></div><div><h2>{soon_h}</h2><ul>{soon}</ul></div><div><h2>{esc(L('f_guides'))}</h2><ul>{guides}<li><a href="{r}{lang}/guides/">{esc(L("all_guides"))} →</a></li></ul></div>
<div><h2>{esc(L('f_company'))}</h2><ul>{comp}</ul></div></div>
<div class="legal"><p>{esc(L('disclaimer'))} {esc({"en": "Rates last verified", "ms": "Kadar terakhir disahkan", "ru": "Тарифы проверены", "zh": "费率最近核实于"}[lang])} {VFULL[lang]}.</p><p class="nowrap">© 2026 SellerFee · sellerfee.app</p></div></div></footer>
'''

def page(path, lang, title, desc, body, schema=None, alt=None, og_type='website', scripts='', topbar_on=True):
    url = BASE + path
    alts = ''
    if alt:
        alts = ''.join(f'<link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{BASE}{p}">' for l, p in alt.items())
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt.get("en", list(alt.values())[0])}">'
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
<meta property="og:site_name" content="SellerFee"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og.png"><meta property="og:locale" content="{LANGS[lang]['og']}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0B1220">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/style.css">
{ld}
</head>
<body>
<a class="skip" href="#main">{esc(tr(lang, 'skip'))}</a>
{topbar(lang, path) if topbar_on else ''}{header(lang, path, alt)}<main id="main">
{body}
</main>
{footer(lang, path, alt)}<script src="{r}assets/site.js" defer></script>{scripts}</body>
</html>
'''

def crumbs(path, items, lang='en'):
    r = rel(path)
    sep = ic('chev', 12, 'rot')
    h = f'<nav class="crumbs" aria-label="{esc(tr(lang, "aria_crumbs"))}">' + f' {sep} '.join(f'<a href="{r}{u}">{esc(t)}</a>' if u is not None else f'<b>{esc(t)}</b>' for t, u in items) + '</nav>'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": BASE + u} if u is not None else {})} for i, (t, u) in enumerate(items)]}
    return h, ld

def faq_block(faq, lang='en'):
    h = f'<h2 id="faq">{esc(tr(lang, "faq"))}</h2><div class="faq">' + ''.join(f'<details class="q"><summary>{esc(q)}{ic("plus", 18)}</summary><p>{a}</p></details>' for q, a in faq) + '</div>'
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faq]}
    return h, ld

def sources_block(src, lang='en', path=''):
    def sl(t):
        tl = 'ru' if re.search('[А-Яа-яЁё]', t) else ('zh-CN' if re.search('[\u4e00-\u9fff]', t) else 'en')
        return f' lang="{tl}"' if tl != LANGS[lang]['html'] else ''
    tt = lambda t: t if sl(t) else H.unescape(l10n.text(lang, esc(t)))
    items = ''.join(f'<li class="src"><span class="ix">{i + 1:02d}</span><a href="{u}" rel="nofollow noopener" target="_blank"{sl(t)}>{esc(tt(t))}</a>{ic("ext", 14)}</li>' for i, (t, u) in enumerate(src))
    rep = issue_url('Wrong rate: ', f'Page: {BASE}{path}\nWhich fee looks wrong:\nLink to the official source:')
    return (f'<h2 id="sources">{esc(tr(lang, "sources"))}</h2><p class="muted small">{esc(tr(lang, "verified"))}: <time datetime="{VERIFIED}">{VFULL[lang]}</time></p><ol class="srcs">{items}</ol>'
            f'<p class="report">{ic("alert", 14)}<span>{esc(tr(lang, "report_rate"))} <a href="{rep}" rel="noopener">{esc(tr(lang, "report_link"))}</a> {esc(tr(lang, "report_tail"))}</span></p>')

AD = lambda slot: f'<div class="ad-slot" data-ad-slot="{slot}" hidden></div>'

def badge(text, kind='soon', icon=None):
    return f'<span class="badge b-{kind}">{ic(icon, 13) if icon else ""}{text}</span>'

# ---------------- calculator widget
def fld(lang, id, cur_html, value, hint=None, suffix=None, step='0.01', mode='decimal', label=None, extra=''):
    pre = f'<span class="pre sf-cur">{cur_html}</span>' if cur_html else ''
    suf = f'<span class="suf">{suffix}</span>' if suffix else ''
    h = f'<p class="hint">{esc(hint)}</p>' if hint else ''
    return f'<div class="field"{extra}><label class="label" for="sf-{id}">{esc(label or tr(lang, id))}</label><div class="input">{pre}<input id="sf-{id}" type="number" inputmode="{mode}" min="0" step="{step}" value="{value}">{suf}</div>{h}</div>'

def sel_field(id, label, opts, val=None, extra=''):
    o = ''.join(f'<option value="{v}"{" selected" if v == val else ""}>{esc(t)}</option>' for v, t in opts)
    return f'<div class="field"{extra}><label class="label" for="sf-{id}">{esc(label)}</label><div class="input select"><select id="sf-{id}">{o}</select>{ic("chev", 16, "chev")}</div></div>'

TR_OPTS = {'tiktok-shop-uk', 'etsy-uk', 'lazada-my', 'etsy'}   # descriptive option labels written by us -> translated

def widget(mid, lang):
    m = MARKETS[mid]; L = lambda k: tr(lang, k); d = m['defaults']
    cur = m['symbols'].get(m['currency'], m['currency'])
    curh = cur if not m.get('currencyFromOption') else m['currency']
    inp = m['inputs']
    opts = m['selector']['options']; big = bool(m['selector'].get('src'))
    if lang != 'en' and mid in TR_OPTS:
        opts = [dict(o, n=l10n.text(lang, o['n'])) for o in opts]
    src_lang = 'ru' if m['market'] == 'RU' else 'en'
    sl = f' lang="{src_lang}"' if (mid not in TR_OPTS and src_lang != lang) else ''
    if big:
        cat = (f'<div class="field full"><span class="label">{esc(L(m["selector"]["label"]))} <span class="hint"><span id="sf-selcount">{len(opts):,}</span> {esc(L("n_cats"))}</span></span>'
               f'<div class="input search">{ic("search", 15)}<input id="sf-selq" type="search" autocomplete="off" placeholder="{esc(L("search_cat"))}" aria-label="{esc(L("search_cat"))}"></div>'
               f'<div class="g2 catpick"><div class="input select"><select id="sf-grp"{sl} aria-label="{esc(L("grp"))}"></select>{ic("chev", 16, "chev")}</div>'
               f'<div class="input select"><select id="sf-sel"{sl} aria-label="{esc(L(m["selector"]["label"]))}"></select>{ic("chev", 16, "chev")}</div></div><p class="hint" id="sf-selnote"></p></div>')
    else:
        cat = (f'<div class="field full"><label class="label" for="sf-sel">{esc(L(m["selector"]["label"]))} <span class="hint">{len(opts) if m["selector"]["label"] != "vat_uk" else ""} {esc(L("n_cats")) if m["selector"]["label"] not in ("bank", "vat_uk") else ""}</span></label>'
               f'<div class="input select"><select id="sf-sel"{sl}></select>{ic("chev", 16, "chev")}</div><p class="hint" id="sf-selnote"></p></div>')
    s1 = [cat]
    row = []
    if m['store']:
        lab = L('model') if m['market'] == 'RU' else L('store')
        row.append(f'<div class="field"><span class="label">{esc(lab)}</span><div class="seg" role="radiogroup" aria-label="{esc(lab)}">' + ''.join(
            f'<label><input type="radio" name="sf-store" value="{v}"{" checked" if i == 0 else ""}><span>{esc(L(k))}</span></label>' for i, (v, k) in enumerate(m['store'])) + '</div></div>')
    if m['periods']:
        row.append(sel_field('period', L('period'), [(v, L(k)) for v, k in m['periods']]))
    for x in m.get('selects', []):
        ds = f' data-stores="{" ".join(x["stores"])}"' if x.get('stores') else ''
        if x.get('fromTable'):
            row.append(f'<div class="field"{ds}><label class="label" for="sf-x-{x["id"]}">{esc(L(x["label"]))}</label><div class="input select"><select id="sf-x-{x["id"]}"{sl}><option value=""{(' lang="' + LANGS[lang]['html'] + '"') if sl else ''}>{esc(L(x["first"]))}</option></select>{ic("chev", 16, "chev")}</div></div>')
        else:
            o = ''.join(f'<option value="{v}"{" selected" if v == x.get("def_") else ""}>{esc(L(k))}</option>' for v, k in x['options'])
            row.append(f'<div class="field"{ds}><label class="label" for="sf-x-{x["id"]}">{esc(L(x["label"]))}</label><div class="input select"><select id="sf-x-{x["id"]}">{o}</select>{ic("chev", 16, "chev")}</div></div>')
    s1.append(f'<div class="g2">{"".join(row)}</div>')
    s2 = [fld(lang, 'price', curh, d.get('price', 0)), fld(lang, 'qty', None, 1, step='1', mode='numeric'),
          fld(lang, 'sellerDisc', curh, 0, hint=None), fld(lang, 'cost', curh, d.get('cost', 0))]
    s3 = []
    if 'buyerShip' in inp: s3.append(fld(lang, 'buyerShip', curh, d.get('buyerShip', 0)))
    hk = m.get('hints', {})
    if 'tax' in inp: s3.append(fld(lang, 'tax', curh, 0, hint=L(hk.get('tax', 'tax_h'))))
    if 'vol' in inp: s3.append(fld(lang, 'vol', None, d.get('vol', 1), suffix=tr(lang, 'js')['litre'] if 'litre' in tr(lang, 'js') else 'L', step='0.001', hint=L('vol_h')))
    if 'coef' in inp: s3.append(fld(lang, 'coef', None, d.get('coef', 100), suffix='%', step='1', hint=L('coef_h'), extra=' data-stores="fbw fbs"'))
    s3.append(fld(lang, 'shipCost', curh, 0))
    if 'affPct' in inp: s3.append(fld(lang, 'affPct', None, 0, suffix='%', step='0.1'))
    for c in m['components']:
        if c.get('manual'):
            unit = '%' if c['type'] == 'pct' else curh
            s3.append(f'<div class="field sf-rate"><label class="label" for="sf-r-{c["id"]}">{esc(L("c_" + c["id"]))}</label><div class="input"><input id="sf-r-{c["id"]}" type="number" step="0.01" min="0" placeholder="—"><span class="suf">{esc(unit)}</span></div><p class="hint">{esc(L("c_" + c["id"] + "_h"))}</p></div>')
    if 'taxPct' in inp: s3.append(fld(lang, 'taxPct', None, 0, suffix='%', step='0.1', hint=L(hk.get('taxPct', 'taxPct_h')), label=L(hk['taxPct'][:-2]) if 'taxPct' in hk else None))
    s3.append(fld(lang, 'other', curh, 0, hint=L('other_h')))
    tg = ''.join(f'<label class="toggle tg"><input type="checkbox" id="sf-t-{g["id"]}"><span class="sw" aria-hidden="true"></span><span><b>{esc(L("t_" + g["id"]))}</b><small>{esc(L("t_" + g["id"] + "_h"))}</small></span></label>' for g in m['toggles'])
    rates = []
    for c in m['components']:
        if c.get('manual') or c['type'] in ('vol', 'voltab'): continue
        unit = '%' if c['type'] == 'pct' else (curh + ' ' + (L('u_item') if c.get('per') == 'item' else L('u_order')))
        h = f'<p class="hint">{esc(L("ozproc_h"))}</p>' if c['id'] == 'oz_proc' else ''
        rates.append(f'<div class="field sf-rate"><label class="label" for="sf-r-{c["id"]}">{esc(L("c_" + c["id"]))}</label><div class="input"><input id="sf-r-{c["id"]}" type="number" step="0.01" min="0"><span class="suf">{esc(unit)}</span></div>{h}</div>')
    n = lambda i, k, opt=False: f'<h3><span class="n">{i}</span>{esc(L(k))}{('<span class="opt">' + esc(L('optional')) + '</span>') if opt else ''}</h3>'
    sec4 = f'<div class="cs">{n(4, "sec_n4")}<div class="tgs">{tg}</div></div>' if tg else ''
    cfg = {k: m[k] for k in ('currency', 'symbols', 'locale', 'toggles', 'defaultOption', 'bands', 'conds', 'symbolAfter', 'decimals') if k in m}
    if m['market'] == 'RU' and lang != 'ru': cfg['locale'] = 'en-US'
    if lang != 'en': cfg['locale'] = {'zh': 'zh-CN', 'ru': 'ru-RU', 'ms': 'ms-MY'}[lang]
    cfg['currencyFromOption'] = m.get('currencyFromOption', False)
    if big:
        cfg['selector'] = {'src': rel(f'{lang}/{m["slug"]}/') + f'assets/rates/{mid}.json?v={VERIFIED}'}
    else:
        cfg['selector'] = {'options': opts}
    cfg['selects'] = [{k: v for k, v in x.items() if k in ('id', 'fromTable', 'defIndex', 'stores')} | {'def': x.get('def_')} for x in m.get('selects', [])]
    cfg['components'] = [dict(c, label=L('c_' + c['id'])) for c in m['components']]
    if m['compare']:
        C = m['compare']; cfg['compare'] = {'vary': C['vary'], 'a': dict(C['a'], label=L(C['a']['label'])), 'b': dict(C['b'], label=L(C['b']['label'])), 'note': L(C['note'])}
    js = dict(S['en']['js']); js.update(S[lang].get('js', {}))
    for k in ('copied', 'link_copied', 'you_keep', 'res_fees', 'res_payout', 'res_profit'): js['ui_' + k] = L(k)
    cond = '<p class="condnote" id="sf-condnote" hidden></p>' if m.get('conds') else ''
    return f'''<div class="main">
<div class="card calc" id="sf-calc">
<div class="cs">{n(1, "sec_n1")}{"".join(s1)}</div>
<div class="cs">{n(2, "sec_n2")}<div class="g4">{"".join(s2)}</div><p class="hint">{esc(L("sellerDisc_h"))}</p></div>
<div class="cs">{n(3, "sec_n3", True)}<div class="g4">{"".join(s3)}</div></div>
{sec4}
<div class="cs"><details class="adv"><summary>{esc(L("sec_rates"))}{ic("chev", 16)}</summary><p class="hint">{esc(L("rates_h"))}</p><div class="g4">{"".join(rates)}</div></details></div>
</div>
<div class="side"><div class="card res" aria-live="polite">
<div class="top"><div class="k"><span class="kl">{esc(L("you_keep"))}</span><span class="badge b-verified sm">{ic("refresh", 12)}{esc(L("updates"))}</span></div>
<div class="big" id="sf-k-payout">–</div><div class="small muted">{esc(L("settle_after"))}</div>
<div class="stack" id="sf-bar"></div><ul class="legend" id="sf-legend"></ul>{cond}</div>
<div class="kpis"><div><span>{esc(L("res_fees"))}</span><b id="sf-k-fees">–</b><small id="sf-k-feespct"></small></div><div><span>{esc(L("res_profit"))}</span><b id="sf-k-profit">–</b></div><div><span>{esc(tr(lang, "js")["margin"])}</span><b id="sf-k-margin">–</b></div></div>
<div class="bd"><table class="bk"><tbody id="sf-breakdown"></tbody></table></div>
<div class="foot"><button type="button" class="btn btn-secondary btn-sm" id="sf-copy">{ic("copy", 14)}{esc(L("copy_bd"))}</button><button type="button" class="btn btn-secondary btn-sm" id="sf-share">{ic("link", 14)}{esc(L("share_calc"))}</button></div></div>
<div class="tips"><div class="tip"><span>{ic("info", 13)}{esc(L("breakeven"))}</span><b id="sf-be">–</b></div><div class="tip"><span>{ic("info", 13)}{esc(L("price30"))}</span><b id="sf-p30">–</b></div></div>
<p class="small muted note">{esc(L("est_note"))}</p></div>
</div>
<script>window.SF_MARKET={json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))};window.SF_T={json.dumps(js, ensure_ascii=False)};</script>'''
