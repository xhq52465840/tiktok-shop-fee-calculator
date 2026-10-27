#!/usr/bin/env python3
"""i18n checker for the built site.

For every page in /zh/, /ru/ and /ms/ it checks:
  * parity        - the same set of pages exists in every language as in /en/
  * html lang     - <html lang> matches the folder (zh-CN, ru, ms)
  * hreflang      - en / zh-CN / ru / ms / x-default alternates, all targets exist and link back (reciprocity), canonical = self
  * switcher      - header language menu, footer language links and the calculator language tabs point to the same page in each language
  * sitemap       - every indexable page is listed with all alternates
  * leftover English - visible text, <title>, meta description, OG tags, alt / aria-label / title / placeholder attributes, JSON-LD
                      strings, and JS-rendered calculator text (pages rendered in headless Chrome, every toggle / store / period exercised;
                      all UI strings passed to the calculator script are checked too). Allowed: brand / programme names, units and codes
                      (tools/i18n_allowlist.json), official category names from the rate files, and anything inside an element marked
                      with another lang="…" (official source titles, category lists).
  * math (--math) - SF_compute in every language version of every calculator against the Python mirror on random scenarios.

Usage: python3 tools/check_i18n.py [--base http://localhost:8080] [--math N] [--no-browser] [--json /tmp/i18n_report.json]
"""
import argparse, glob, html as H, json, os, random, re, sys
from collections import defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
LANG_HTML = {'en': 'en', 'zh': 'zh-CN', 'ru': 'ru', 'ms': 'ms'}
SITE = 'https://sellerfee.app/'
AL = json.load(open(os.path.join(ROOT, 'tools', 'i18n_allowlist.json')))

def pages(lang):
    out = set()
    for f in glob.glob(os.path.join(ROOT, lang, '**', '*.html'), recursive=True):
        out.add(os.path.relpath(f, os.path.join(ROOT, lang)).replace(os.sep, '/').replace('index.html', ''))
    return out

def url_of(lang, suf): return SITE + lang + '/' + suf

def official_names():
    from markets import MARKETS
    names = set()
    skip = {'tiktok-shop-uk', 'etsy-uk', 'etsy', 'lazada-my'}
    for mid, m in MARKETS.items():
        if mid in skip: continue
        opts = list(m['selector']['options'])
        for o in opts:
            for nm in (o.get('n'), o.get('g')):
                if not nm: continue
                names.add(nm)
                for part in nm.split(' › '): names.add(part)
    return sorted((n for n in names if re.search('[A-Za-z]', n)), key=len, reverse=True)

class English:
    def __init__(self):
        self.phr = sorted(AL['phrases'] + OFFICIAL, key=len, reverse=True)
        self.rx = re.compile('|'.join(r'(?<![A-Za-z])' + re.escape(p) + r'(?![A-Za-z])' for p in self.phr))
        self.words = set(AL['words'])
        self.ms = set(AL['ms_english_markers'])
    def find(self, lang, s):
        s = H.unescape(s)
        s = re.sub(r'https?://\S+|[\w.+-]+@[\w-]+\.[\w.]+|\b[\w-]+(?:\.[\w-]+)*\.(?:app|com|my|sg|ph|th|uk|ru|org|io|json|svg|png)\b', ' ', s)
        s = self.rx.sub(' ', s)
        words = re.findall(r"[A-Za-z][A-Za-z'’]*", s)
        if lang == 'ms':
            bad = [w for w in words if w.lower() in self.ms and w not in self.words]
        else:
            bad = [w for w in words if w not in self.words]
        return bad

def static_checks(report):
    from html.parser import HTMLParser
    en = pages('en'); per = {l: pages(l) for l in LANG_HTML}
    for l in ('zh', 'ru', 'ms'):
        for suf in sorted(en - per[l]): report['parity'].append(f'missing {l}/{suf}')
        for suf in sorted(per[l] - en): report['parity'].append(f'extra {l}/{suf} (no English page)')
    sm = open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    sm_urls = dict(re.findall(r'<url><loc>([^<]+)</loc>(.*?)</url>', sm.replace('\n', ''), re.S))
    for l in LANG_HTML:
        for suf in sorted(per[l]):
            f = os.path.join(ROOT, l, suf, 'index.html') if not suf.endswith('.html') else os.path.join(ROOT, l, suf)
            s = open(f, encoding='utf-8').read(); me = url_of(l, suf); page = f'{l}/{suf}'
            m = re.search(r'<html lang="([^"]+)"', s)
            if not m or m.group(1) != LANG_HTML[l]: report['html_lang'].append(f'{page}: lang={m.group(1) if m else None}')
            if suf.endswith('404.html'): continue
            if 'name="robots" content="noindex' in s: continue
            alts = dict((b, a) for a, b in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s))
            alts = {v: k for k, v in alts.items()}
            alts = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s))
            can = re.search(r'<link rel="canonical" href="([^"]+)">', s)
            if not can or can.group(1) != me: report['hreflang'].append(f'{page}: canonical {can.group(1) if can else None}')
            need = ['en', 'zh-CN', 'ru', 'ms', 'x-default']
            for h in need:
                if h not in alts: report['hreflang'].append(f'{page}: no hreflang {h}')
            if alts.get(LANG_HTML[l]) != me: report['hreflang'].append(f'{page}: self hreflang {alts.get(LANG_HTML[l])}')
            if 'x-default' in alts and alts['x-default'] != alts.get('en'): report['hreflang'].append(f'{page}: x-default != en')
            for h, u in alts.items():
                if h == 'x-default': continue
                p2 = u.replace(SITE, '')
                f2 = os.path.join(ROOT, p2, 'index.html')
                if not os.path.isfile(f2): report['hreflang'].append(f'{page}: hreflang {h} -> missing {p2}'); continue
                s2 = open(f2, encoding='utf-8').read()
                back = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s2))
                if back.get(LANG_HTML[l]) != me: report['hreflang'].append(f'{page}: not reciprocal from {p2}')
            # language switchers: header menu, footer list, calculator tabs
            exp = {k: v.replace(SITE, '/') for k, v in alts.items() if k != 'x-default'}
            hm = re.search(r'<details class="dd lang">.*?</details>', s, re.S)
            fm = re.search(r'<div class="langs">(.*?)</div>', s, re.S)
            for name, blk in (('header', hm.group(0) if hm else ''), ('footer', fm.group(1) if fm else '')):
                got = dict((b, a) for a, b in re.findall(r'<a [^>]*href="([^"]+)"[^>]*hreflang="([^"]+)"', blk))
                if set(got) != set(exp): report['switcher'].append(f'{page}: {name} switcher languages {sorted(got)}')
                for h, u in got.items():
                    if exp.get(h) != u: report['switcher'].append(f'{page}: {name} switcher {h} -> {u} (expected {exp.get(h)})')
            ls = re.search(r'<div class="langseg">(.*?)</div></div>', s, re.S)
            if ls:
                for u, h in re.findall(r'<a href="([^"]+)" hreflang="([^"]+)"', ls.group(1)):
                    if exp.get(h) != u: report['switcher'].append(f'{page}: calculator tab {h} -> {u}')
            if me not in sm_urls: report['sitemap'].append(f'{page}: not in sitemap')
            else:
                smalt = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', sm_urls[me]))
                if smalt != alts: report['sitemap'].append(f'{page}: sitemap alternates differ')
    return per

JS_COLLECT = r"""() => {
  const lang = document.documentElement.lang; const out = [];
  const foreign = el => { const c = el.closest('[lang]'); return c && c.getAttribute('lang') !== lang; };
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; while ((n = w.nextNode())) {
    const p = n.parentElement; if (!p || ['SCRIPT','STYLE','NOSCRIPT'].includes(p.tagName) || p.closest('var,code,kbd')) continue;  // math variables / code are not prose
    const t = n.nodeValue.trim(); if (!t || foreign(p) || p.closest('[aria-hidden="true"]')) continue; out.push(['text', t, p.tagName.toLowerCase() + (p.id ? '#' + p.id : '')]);
  }
  document.querySelectorAll('[title],[alt],[aria-label],[placeholder],[data-copy-link]').forEach(e => {
    if (foreign(e)) return;
    for (const a of ['title','alt','aria-label','placeholder','data-copy-link']) if (e.hasAttribute(a) && e.getAttribute(a).trim()) out.push(['@' + a, e.getAttribute(a), e.tagName.toLowerCase()]);
  });
  out.push(['title', document.title, 'head']);
  for (const k of ['description']) { const m = document.querySelector('meta[name=' + k + ']'); if (m) out.push(['meta', m.content, k]); }
  for (const k of ['og:title','og:description']) { const m = document.querySelector('meta[property="' + k + '"]'); if (m) out.push(['meta', m.content, k]); }
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    const skipK = new Set(['@context','@type','url','item','logo','image','mainEntityOfPage','inLanguage','priceCurrency','price','operatingSystem','applicationCategory','datePublished','dateModified']);
    const walk = (o, k) => { if (typeof o === 'string') { if (!skipK.has(k)) out.push(['jsonld', o, k]); } else if (o && typeof o === 'object') for (const kk in o) walk(o[kk], kk); };
    try { walk(JSON.parse(s.textContent), ''); } catch (e) {}
  });
  if (window.SF_T) for (const k in window.SF_T) if (typeof SF_T[k] === 'string') out.push(['js', SF_T[k], 'SF_T.' + k]);
  if (window.SF_MARKET) { const M = window.SF_MARKET; (M.components || []).forEach(c => out.push(['js', c.label, 'component'])); if (M.compare) { out.push(['js', M.compare.a.label, 'cmp']); out.push(['js', M.compare.b.label, 'cmp']); out.push(['js', M.compare.note, 'cmp']); } }
  return out;
}"""
JS_EXERCISE = r"""async () => {
  const root = document.getElementById('sf-calc'); if (!root) return [];
  const lang = document.documentElement.lang; const got = [];
  const grab = () => ['sf-breakdown','sf-legend','sf-selnote','sf-condnote','sf-compare','sf-k-feespct','sf-bar'].forEach(id => { const e = document.getElementById(id); if (e) { got.push(['js-rendered', e.innerText, id]); e.querySelectorAll('[title]').forEach(x => got.push(['@title', x.getAttribute('title'), id])); } });
  const fire = e => e.dispatchEvent(new Event('change', {bubbles: true}));
  for (const id of ['sf-shipCost','sf-buyerShip','sf-other','sf-affPct','sf-taxPct','sf-tax','sf-sellerDisc']) { const e = document.getElementById(id); if (e) { e.value = id === 'sf-affPct' || id === 'sf-taxPct' ? '5' : '3'; e.dispatchEvent(new Event('input', {bubbles: true})); } }
  grab();
  const radios = [...root.querySelectorAll('input[name=sf-store]')];
  for (const r of (radios.length ? radios : [null])) {
    if (r) { r.checked = true; fire(r); }
    for (const t of root.querySelectorAll('input[type=checkbox]')) { if (!t.disabled) { t.checked = true; fire(t); grab(); } }
    const per = document.getElementById('sf-period');
    if (per) for (const o of per.options) { per.value = o.value; fire(per); grab(); }
    for (const t of root.querySelectorAll('input[type=checkbox]')) { t.checked = false; fire(t); }
  }
  for (const s of root.querySelectorAll('select[id^=sf-x-]')) { for (const o of [...s.options].slice(0, 3)) { s.value = o.value; fire(s); grab(); } }
  const v = document.getElementById('sf-vol'); if (v) { v.value = '0'; v.dispatchEvent(new Event('input', {bubbles: true})); grab(); }
  const q = document.getElementById('sf-selq'); if (q) { q.value = 'zzzzqqq'; q.dispatchEvent(new Event('input', {bubbles: true})); got.push(['js-rendered', document.getElementById('sf-sel').innerText, 'search']); q.value = ''; q.dispatchEvent(new Event('input', {bubbles: true})); }
  const sel = document.getElementById('sf-sel'); const fr = sel && sel.closest('[lang]'); 
  return got.filter(x => !(x[2] === 'search' && fr && fr.getAttribute('lang') !== lang));
}"""

def browser_checks(report, base, per, math_n):
    from playwright.sync_api import sync_playwright
    E = English()
    exe = '/usr/bin/google-chrome' if os.path.exists('/usr/bin/google-chrome') else None
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        for l in ('zh', 'ru', 'ms'):
            for suf in sorted(per[l]):
                page = f'{l}/{suf}'; errs.clear()
                pg.goto(f'{base}/{page}', wait_until='load')
                if pg.query_selector('#sf-calc'):
                    try: pg.wait_for_function('window.SF_ready===true', timeout=20000)
                    except Exception: report['js'].append(f'{page}: calculator did not initialise')
                items = pg.evaluate(JS_COLLECT)
                if pg.query_selector('#sf-calc'): items += pg.evaluate(JS_EXERCISE)
                if suf.endswith('404.html') is False and errs: report['js'].append(f'{page}: JS error {errs[0][:120]}')
                seen = set()
                for kind, txt, where in items:
                    for line in txt.split('\n'):
                        bad = E.find(l, line)
                        if bad:
                            k = (kind, line.strip()[:160])
                            if k in seen: continue
                            seen.add(k); report['english'].append(f'{page} [{kind} {where}] {" ".join(dict.fromkeys(bad))} :: {line.strip()[:160]}')
        # root 404 in every language
        nf = open(os.path.join(ROOT, '404.html'), encoding='utf-8').read()
        pg.route('**/no-such-page-xyz/', lambda route: route.fulfill(status=404, content_type='text/html', body=nf))
        for l in ('zh', 'ru', 'ms'):
            pg.goto(f'{base}/{l}/no-such-page-xyz/')
            t = pg.evaluate("() => [document.documentElement.lang, document.title, [...document.querySelectorAll('.nf')].filter(e => !e.hidden).map(e => e.innerText).join(' ')]")
            if t[0] != LANG_HTML[l]: report['html_lang'].append(f'root 404 for /{l}/: lang={t[0]}')
            for s in t[1:]:
                bad = E.find(l, s)
                if bad: report['english'].append(f'root 404 /{l}/ :: {bad}')
        if math_n: math_checks(report, pg, base, math_n)
        b.close()

def math_checks(report, pg, base, n):
    from markets import MARKETS, compute
    rnd = random.Random(11)
    for mid, m in MARKETS.items():
        opts = m['selector']['options']
        cases = []
        for i in range(n):
            sel = rnd.randrange(len(opts))
            inp = dict(price=round(rnd.choice([rnd.uniform(1, 60), rnd.uniform(60, 5000)]), 2), qty=rnd.randint(1, 3),
                       sellerDisc=rnd.choice([0, round(rnd.uniform(0, 5), 2)]), buyerShip=rnd.choice([0, round(rnd.uniform(0, 9), 2)]),
                       cost=round(rnd.uniform(0, 20), 2), vol=round(rnd.uniform(0.1, 30), 3), coef=rnd.choice([100, 170]), tax=rnd.choice([0, 1.5]))
            store = rnd.choice(m['store'])[0] if m.get('store') else None
            period = rnd.choice(m['periods'])[0] if m.get('periods') else 'new'
            tg = {g['id']: rnd.random() < .5 for g in m.get('toggles', [])}
            for g in m.get('toggles', []):
                if g.get('requires') and not tg.get(g['requires']): tg[g['id']] = False
                if g.get('stores') and store not in g['stores']: tg[g['id']] = False
            x = {}
            for s in m.get('selects', []):
                if s.get('fromTable'): x[s['id']] = rnd.choice(['', '0', '3', '7'])
                else: x[s['id']] = rnd.choice(s['options'])[0]
            try: r = compute(mid, sel=sel, period=period, store=store, tg=tg, x=x, **inp)
            except Exception as e: continue
            if mid == 'tiktok-shop-th' and any(v is None for v in r['rate'].values()): continue
            cases.append(dict(sel=sel, inp=inp, ex=dict(period=period, tg=tg, x=x, **({'store': store} if store else {})), total=r['total'], payout=r['payout'], profit=r['profit']))
        for l in ('en', 'zh', 'ru', 'ms'):
            try:
                pg.goto(f'{base}/{l}/{m["slug"]}/'); pg.wait_for_function('window.SF_ready===true', timeout=20000)
            except Exception:
                report['math'].append(f'{l}/{m["slug"]}/: calculator page missing or did not load'); continue
            res = pg.evaluate('cs=>cs.map(c=>{var f=SF_compute(c.inp,c.sel,c.ex);return [f.total,f.payout,f.profit]})', cases)
            bad = sum(1 for c, j in zip(cases, res) if max(abs(j[0] - c['total']), abs(j[1] - c['payout']), abs(j[2] - c['profit'])) > 0.006)
            report['math_cases'] += len(cases)
            if bad: report['math'].append(f'{l}/{m["slug"]}/: {bad}/{len(cases)} scenarios differ from the Python mirror')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--base', default='http://localhost:8080'); ap.add_argument('--math', type=int, default=0)
    ap.add_argument('--no-browser', action='store_true'); ap.add_argument('--json', default='/tmp/i18n_report.json'); ap.add_argument('-v', action='store_true')
    a = ap.parse_args()
    OFFICIAL = official_names()
    report = defaultdict(list); report['math_cases'] = 0
    per = static_checks(report)
    if not a.no_browser: browser_checks(report, a.base, per, a.math)
    counts = {l: len(per[l]) for l in LANG_HTML}
    keys = ['parity', 'html_lang', 'hreflang', 'switcher', 'sitemap', 'english', 'js', 'math']
    json.dump({k: report[k] for k in keys} | {'pages': counts, 'math_cases': report['math_cases']}, open(a.json, 'w'), ensure_ascii=False, indent=1)
    print('pages per locale:', counts)
    total = 0
    for k in keys:
        n = len(report[k]); total += n
        print(f'{k:10s} {n}')
        for x in report[k][: (10**6 if a.v else 8)]: print('   ', x)
    if a.math: print(f'math scenarios checked: {report["math_cases"]}')
    print('TOTAL ISSUES', total)
    sys.exit(1 if total else 0)
