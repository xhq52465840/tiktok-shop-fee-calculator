"""Segment-level localisation of English page content.

English pages are the source. For a language without a hand-written page, the English HTML is split into
translatable segments (runs of text + inline tags between block tags, plus a few attributes). Each segment is
normalised into a key: inline tags become numbered placeholders (<a1>…</a1>, <b2>…</b2>), atomic pieces
(icons, elements marked lang="…"/translate="no") become <x1/>, and every number becomes {0}, {1}… so numbers
are always copied from the English source and can never drift in a translation.

Catalogues live in src/l10n/<lang>/*.txt as:
    @@ <hash>
    <translated key, same placeholders>
<hash> = sha1(key)[:10]. Missing keys fall back to English and are listed by `python3 src/l10n.py missing <lang>`.
Official platform names (category names from the rate files) are left untouched and marked with lang="…".
"""
import hashlib, html as H, os, re, glob, json, sys
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'l10n')
TOK = re.compile(r'(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<svg\b.*?</svg>|<[^>]+>)', re.S | re.I)
INLINE = {'a', 'b', 'strong', 'em', 'i', 'code', 'span', 'small', 'sup', 'sub', 'time', 'abbr', 'u', 's', 'mark', 'q', 'kbd', 'cite'}
VOID_INLINE = {'br', 'wbr'}
ATTRS = ('placeholder', 'aria-label', 'title', 'alt', 'data-copy-link')
NUM = re.compile(r'\d+(?:[.,]\d+)*')
LETTER = re.compile(r'[A-Za-z]')
# text with only numbers, currency, units, codes and punctuation needs no translation
NOTR = re.compile(r'^(?:[\s\d.,:;%()\[\]/+\-−–—×→←·•*&=<>~≈≤≥$£€₱₽฿?!\'"’‘“”]|RM|S\$|US\$|MYR|SGD|USD|GBP|PHP|THB|RUB|EUR|BXP|PXP|SCP|SST|GST|VAT|MP|FBO|FBS|FBW|FBY|DBS|realFBS|TX|CGF|PIF|PSF|OPF|SFP|KVV|ID|N/A|L|kg|g|cm|ml|x|h)*$')
CAT = {}   # lang code of official names, filled lazily
_cat = None; _cache = {}; MISSING = {}; USED = {}

def key_hash(k): return hashlib.sha1(k.encode('utf-8')).hexdigest()[:10]

def catalog(lang):
    """Catalogue files: src/l10n/*.txt, entries '@@ <hash>' followed by 'en: …' (reference), 'zh: …', 'ru: …', 'ms: …' lines."""
    if lang not in _cache:
        d = {}
        for f in sorted(glob.glob(os.path.join(DIR, '*.txt'))):
            cur = None
            for line in open(f, encoding='utf-8').read().split('\n'):
                if line.startswith('@@ '): cur = line[3:].split()[0]
                elif cur and line.startswith(lang + ': '): d[cur] = line[len(lang) + 2:].strip()
        _cache[lang] = d
    return _cache[lang]

_brand = None
def brand_only(plain):
    """True when the text is only brand / programme names, codes and units (nothing to translate)."""
    global _brand
    if _brand is None:
        al = json.load(open(os.path.join(os.path.dirname(DIR), '..', 'tools', 'i18n_allowlist.json'), encoding='utf-8'))
        ph = sorted(al['phrases'], key=len, reverse=True)
        _brand = (re.compile('|'.join(r'(?<![A-Za-z])' + re.escape(p) + r'(?![A-Za-z])' for p in ph)), set(al['words']))
    rx, words = _brand
    rest = rx.sub(' ', plain)
    return all(w in words for w in re.findall(r"[A-Za-z][A-Za-z'’]*", rest))

def official():
    """Official category / group names from the rate files -> language of the name."""
    global _cat
    if _cat is None:
        from markets import MARKETS
        _cat = {}
        skip = {'tiktok-shop-uk', 'etsy-uk', 'etsy', 'lazada-my'}   # descriptive labels we wrote: translated, not official
        root = os.path.dirname(DIR)
        for mid, m in MARKETS.items():
            if mid in skip: continue
            lg = 'ru' if m['market'] == 'RU' else 'en'
            opts = m['selector']['options']
            for o in opts:
                for nm in (o.get('n'), o.get('g'), (o['g'] + ' › ' + o['n']) if o.get('g') else None):
                    if nm and len(nm) > 2: _cat[nm] = lg
                if o.get('n') and ' › ' in o['n']:
                    for part in o['n'].split(' › '): _cat.setdefault(part, lg)
    return _cat

def tagname(t):
    m = re.match(r'</?\s*([a-zA-Z0-9]+)', t); return m.group(1).lower() if m else ''

def norm(s): return re.sub(r'\s+', ' ', s).strip()

def _key(tokens):
    """tokens -> (key, placeholders{name: original}, ok)"""
    ph = {}; out = []; stack = []; n = 0; x = 0; nums = []
    for kind, t in tokens:
        if kind == 'text':
            def numsub(m):
                nums.append(m.group(0)); return '{%d}' % (len(nums) - 1)
            out.append(NUM.sub(numsub, t.replace('{', '\u2983').replace('}', '\u2984')))
        elif kind == 'atom':
            x += 1; nm = f'<x{x}/>'; ph[nm] = t; out.append(nm)
        else:
            tn = tagname(t)
            if tn in VOID_INLINE: out.append('<br>'); ph.setdefault('<br>', t); continue
            if t.startswith('</'):
                if not stack or stack[-1][0] != tn: return None, None, None
                _, idn = stack.pop(); nm = f'</{tn}{idn}>'; ph[nm] = t; out.append(nm)
            else:
                n += 1; nm = f'<{tn}{n}>'; ph[nm] = t; stack.append((tn, n)); out.append(nm)
    if stack: return None, None, None
    return norm(''.join(out)), ph, nums

def _restore(tr, ph, nums):
    def rnum(m):
        i = int(m.group(1)); return nums[i] if i < len(nums) else m.group(0)
    s = re.sub(r'\{(\d+)\}', rnum, tr)
    s = re.sub(r'</?[a-z]+\d+>|<x\d+/>|<br>', lambda m: ph.get(m.group(0), m.group(0)), s)
    return s.replace('\u2983', '{').replace('\u2984', '}')

def _valid(tr, key):
    a = sorted(re.findall(r'</?[a-z]+\d+>|<x\d+/>|\{\d+\}', key)); b = sorted(re.findall(r'</?[a-z]+\d+>|<x\d+/>|\{\d+\}', tr))
    return a == b

CTX = {'page': ''}
def text(lang, s):
    """Translate one plain-text / inline-HTML string."""
    if lang == 'en' or not s: return s
    return localize(lang, s)

def _seg(lang, toks):
    """toks: list of (kind, text). Returns translated html for the run."""
    plain = norm(H.unescape(''.join(t for k, t in toks if k == 'text')))
    if not LETTER.search(plain) or NOTR.match(plain) or brand_only(plain): return ''.join(t for k, t in toks)
    off = official().get(plain)
    if off and all(k != 'tag' for k, _ in toks):
        raw = ''.join(t for k, t in toks); lead = raw[:len(raw) - len(raw.lstrip())]; tail = raw[len(raw.rstrip()):]
        return f'{lead}<span lang="{off}">{raw.strip()}</span>{tail}' if off != lang else raw
    # a run that is only sibling inline elements (no text of its own): handle each child separately
    depth = 0; groups = []; cur = []; own_text = False
    for t in toks:
        if t[0] == 'tag' and tagname(t[1]) in VOID_INLINE: cur.append(t); continue
        if depth == 0 and t[0] == 'text' and t[1].strip(): own_text = True; break
        cur.append(t)
        if t[0] == 'tag':
            if t[1].startswith('</'): depth -= 1
            else: depth += 1
            if depth < 0: own_text = True; break
        if depth == 0 and t[0] != 'text': groups.append(cur); cur = []
    if not own_text and depth == 0 and len(groups) > 1:
        out = ''.join(x[1] for x in cur) if False else ''
        res = []
        for g in groups:
            lead = [x for x in g[:0]]
            if g[-1][0] == 'atom' and len(g) == 1 or all(x[0] != 'text' or not x[1].strip() for x in g if x[0] == 'text') and not any(x[0] == 'text' and LETTER.search(x[1]) for x in g):
                res.append(''.join(x[1] for x in g)); continue
            # g = leading whitespace…, <tag>, inner…, </tag>
            k0 = next(n for n, x in enumerate(g) if x[0] == 'tag')
            res.append(''.join(x[1] for x in g[:k0 + 1]) + _seg(lang, g[k0 + 1:-1]) + g[-1][1])
        return ''.join(res) + ''.join(x[1] for x in cur)
    # whitespace-only text and icons at the ends stay outside; then peel tags that wrap the whole run (<b>…</b>) and
    # leading/trailing tags that would leave the segment unbalanced
    i, j = 0, len(toks)
    ws = lambda t: (t[0] == 'text' and not t[1].strip()) or t[0] == 'atom'
    while i < j and ws(toks[i]): i += 1
    while j > i and ws(toks[j - 1]): j -= 1
    while j - i > 2 and toks[i][0] == 'tag' and toks[j - 1][0] == 'tag' and not toks[i][1].startswith('</') \
            and toks[j - 1][1].startswith('</') and tagname(toks[i][1]) == tagname(toks[j - 1][1]) and _key(toks[i + 1:j - 1])[0] is not None \
            and _key(toks[i:j])[0] is not None:
        i += 1; j -= 1
        while i < j and ws(toks[i]): i += 1
        while j > i and ws(toks[j - 1]): j -= 1
    k, ph, nums = _key(toks[i:j])
    if k is None:
        while i < j and (toks[i][0] != 'text' or not toks[i][1].strip()): i += 1
        while j > i and (toks[j - 1][0] != 'text' or not toks[j - 1][1].strip()): j -= 1
        k, ph, nums = _key(toks[i:j])
    core = toks[i:j]
    if k is None:
        return ''.join(t for kk, t in toks[:i]) + ''.join(_seg(lang, [c]) if c[0] == 'text' else c[1] for c in core) + ''.join(t for kk, t in toks[j:])
    raw = ''.join(t for kk, t in core)
    lead = raw[:len(raw) - len(raw.lstrip())]; tail = raw[len(raw.rstrip()):]
    h = key_hash(k); cat = catalog(lang); tr = cat.get(h)
    USED.setdefault(lang, set()).add(h)
    if tr is None or not _valid(tr, k):
        MISSING.setdefault(lang, {}).setdefault(h, (k, CTX['page'], 'bad' if tr is not None else 'missing'))
        out = raw.strip()
    else:
        out = _restore(tr, ph, nums)
    return ''.join(t for kk, t in toks[:i]) + lead + out + tail + ''.join(t for kk, t in toks[j:])

def _attr(lang, tag):
    def sub(m):
        v = H.unescape(m.group(2))
        if not LETTER.search(v) or NOTR.match(v) or brand_only(v): return m.group(0)
        tv = _seg(lang, [('text', H.escape(v, quote=False))])
        return f'{m.group(1)}="{H.escape(H.unescape(tv), quote=True)}"'
    return re.sub(r'\b(' + '|'.join(ATTRS) + r')="([^"]*)"', sub, tag)

def localize(lang, html):
    if lang == 'en' or not html: return html
    parts = [p for p in TOK.split(html) if p != '']
    out = []; run = []; skip = None; depth = 0
    def flush():
        if run: out.append(_seg(lang, run)); run.clear()
    for p in parts:
        if skip:
            run[-1] = ('atom', run[-1][1] + p) if run and run[-1][0] == 'atom' else ('atom', p)
            if p.startswith('<') and not p.startswith('<!--'):
                tn = tagname(p)
                if tn == skip:
                    if p.startswith('</'): depth -= 1
                    elif not p.endswith('/>'): depth += 1
                if depth == 0:
                    skip = None
                    # an atomic run that is a whole block-level element: emit as is
                    if tagname(run[-1][1]) not in INLINE:
                        a = run.pop(); flush(); out.append(a[1])
            continue
        if not p.startswith('<'):
            run.append(('text', p)); continue
        if p.startswith('<!--') or p.lower().startswith(('<script', '<style')):
            flush(); out.append(p); continue
        if p.lower().startswith('<svg'):
            run.append(('atom', p)); continue
        tn = tagname(p)
        if not p.startswith('</') and re.search(r'\s(lang|translate)="|\saria-hidden="true"', p) and not p.endswith('/>') and tn not in ('br', 'wbr', 'input', 'img'):
            if tn not in INLINE: flush()
            skip = tn; depth = 1; run.append(('atom', p)); continue
        p = _attr(lang, p) if not p.startswith('</') else p
        if tn in INLINE or tn in VOID_INLINE:
            run.append(('tag', p))
        else:
            flush(); out.append(p)
    flush()
    s = ''.join(out)
    return ru_numbers(s) if lang == 'ru' else s

def ru_numbers(s):
    """Russian number typography on text nodes outside lang-marked elements: 1,234.5 -> 1 234,5."""
    parts = TOK.split(s); out = []; skip = None; depth = 0
    for p in parts:
        if p.startswith('<'):
            if skip:
                tn = tagname(p)
                if tn == skip: depth += -1 if p.startswith('</') else (0 if p.endswith('/>') else 1)
                if depth == 0: skip = None
            elif not p.startswith('</') and re.search(r'\s(lang|translate)="', p) and not p.endswith('/>') and not p.startswith(('<script', '<style', '<svg', '<!--')):
                skip = tagname(p); depth = 1
            out.append(p); continue
        if skip: out.append(p); continue
        p = re.sub(r'(?<![\d.,])(\d{1,3})((?:,\d{3})+)(?![\d,])', lambda m: m.group(1) + m.group(2).replace(',', '\u00a0'), p)
        p = re.sub(r'(?<=\d)\.(?=\d)', ',', p)
        out.append(p)
    return ''.join(out)

def write_missing(path_dir='/tmp/l10n'):
    os.makedirs(path_dir, exist_ok=True)
    for lang, d in MISSING.items():
        with open(os.path.join(path_dir, f'{lang}.txt'), 'w', encoding='utf-8') as f:
            last = None
            for h, (k, pg, why) in d.items():
                if pg != last: f.write(f'# page: {pg}\n'); last = pg
                f.write(f'@@ {h}{"  (BAD PLACEHOLDERS)" if why == "bad" else ""}\n{k}\n')
    return {l: len(d) for l, d in MISSING.items()}
