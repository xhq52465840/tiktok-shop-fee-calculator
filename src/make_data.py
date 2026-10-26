"""One-off extractor: turns the official tables (saved from TikTok Seller University / Etsy Help on 2026-10-26)
into per-platform, per-market rate files under src/data/. Re-run after re-downloading the source pages."""
import json, re, os
D = os.path.join(os.path.dirname(__file__), 'data')
pct = lambda s: None if s.strip() in ('-', '') else float(s.strip().rstrip('%'))
def dump(p, obj): json.dump(obj, open(os.path.join(D, p), 'w'), ensure_ascii=False, indent=1)

# --- TikTok Shop Malaysia: table 2 of the official commission article
my = json.load(open('/tmp/my.html.json'))[1][2:]
rows = {}
for r in my:
    ind, c1, c2 = r[0], r[1], r[2]; v = [pct(x) for x in r[3:11]]
    names = ['old.mp.bxp','old.mp.non','old.mall.bxp','old.mall.non','new.mp.bxp','new.mp.non','new.mall.bxp','new.mall.non']
    key = f"{c1} › {c2}"
    if key in rows:
        if rows[key]['r'] == dict(zip(names, v)): continue
        key = f"{c1} › {c2} ({ind})"
    rows[key] = {'n': key, 'g': c1, 'r': dict(zip(names, v))}
dump('tiktok-shop/my.json', sorted(rows.values(), key=lambda x: x['n']))

# --- TikTok Shop Philippines
ph = json.load(open('/tmp/ph.html.json'))[0][1:]
cluster = None; out = []
for r in ph:
    names = [x for x in r if not x.endswith('%')]; rates = [pct(x) for x in r if x.endswith('%')]
    if names and re.match(r'^\d\.', names[0]): cluster = re.sub(r'^\d\.\s*', '', names[0]); names = names[1:]
    names = [n for n in names if n]
    cat = names[0]; sub = names[1] if len(names) > 1 else ''
    n = cat + (' › ' + sub if sub else '')
    if cat == 'Pre-Owned': n = f"Pre-Owned ({cluster})"
    note = ''
    if cluster == 'Electronics': g = 1.0
    elif cluster == 'Fashion': g = 1.5
    elif cluster == 'FMCG':
        if cat == 'Food & Beverages': g = 1.0
        elif cat in ('Beauty & Personal Care', 'Health', 'Baby & Maternity'): g = 1.5
        else: g = 1.5; note = 'gn'
    else: g = 1.0 if sub == 'Large Home Appliances' else 1.5
    out.append({'n': n, 'g': cluster, 'r': {'old': rates[0], 'mp': rates[1], 'mall': rates[2], 'growth': g}, 'note': note})
dump('tiktok-shop/ph.json', out)

# --- TikTok Shop US (text of the official referral fee article)
t = open('/tmp/us.html.txt').read()
t = t[t.index('Level 1+Level 2 Category Referral Fee Rate Notes') + 48: t.index('Is the content above helpful')]
us = []
for m in re.finditer(r"([A-Z][^%]*?)\+ ([^%]+?) (\d+)%( Any portion of the sale over \$10K, 3%)?", t):
    l1, l2, rate, tier = m.group(1).strip(), m.group(2).strip(), float(m.group(3)), m.group(4)
    if 'Test Category' in l1: continue
    row = {'n': f"{l1} › {l2}", 'g': l1, 'r': {'rate': rate}}
    if tier: row['r']['over'] = 3.0
    us.append(row)
dump('tiktok-shop/us.json', us)
print('MY', len(rows), 'PH', len(out), 'US', len(us))

# --- Etsy payment processing fees by bank-account location (Etsy Help, article 115015628847)
ETSY = """Argentina|6.5|0.30|USD
Australia (domestic orders)|3|0.25|AUD
Australia (international orders)|4|0.25|AUD
Austria|4|0.30|EUR
Belgium|4|0.30|EUR
Brazil|6.5|0.30|USD
Bulgaria|4|0.30|EUR
Canada (domestic orders or orders from the US)|3|0.25|CAD
Canada (international orders)|4|0.25|CAD
Chile|6.5|0.30|USD
China|6.5|0.30|USD
Croatia|4|0.30|EUR
Cyprus|4|0.30|EUR
Czech Republic|4|0.30|EUR
Denmark|4|2.50|DKK
Egypt|6.5|0.30|USD
Estonia|4|0.30|EUR
Finland|4|0.30|EUR
France|4|0.30|EUR
Georgia|6.5|0.30|USD
Germany|4|0.30|EUR
Greece|4|0.30|EUR
Hong Kong|4.4|2.00|HKD
Hungary|4|0.30|EUR
India|5|25|INR
Indonesia|4.5|7000|IDR
Ireland|4|0.30|EUR
Israel|4.5|2|ILS
Italy|4|0.30|EUR
Japan|6.0|0.30|USD
Kazakhstan|6.5|0.30|USD
Latvia|4|0.30|EUR
Lithuania|4|0.30|EUR
Luxembourg|4|0.30|EUR
Malaysia|4.5|2|MYR
Malta|4|0.30|EUR
Mexico|4.5|8|MXN
Morocco|4.5|5|MAD
Netherlands|4|0.30|EUR
New Zealand (domestic orders)|3|0.30|NZD
New Zealand (international orders)|4|0.30|NZD
Norway|4|2.50|NOK
Pakistan|6.5|0.30|USD
Peru|6.5|0.30|USD
Philippines|4.5|25|PHP
Poland|4|0.30|EUR
Portugal|4|0.30|EUR
Romania|4|0.30|EUR
Serbia|6.5|0.30|USD
Singapore|4.4|0.35|SGD
Slovakia|4|0.30|EUR
Slovenia|4|0.30|EUR
South Africa|4.5|8|ZAR
South Korea|6.5|0.30|USD
Spain|4|0.30|EUR
Sweden|4|3.00|SEK
Switzerland|4|0.50|CHF
Thailand|6|0.30|USD
Türkiye|6.5|14|TRY
Ukraine|6.0|0.30|USD
United Arab Emirates|6.5|0.30|USD
United Kingdom|4|0.20|GBP
United States|3|0.25|USD
Vietnam|4.5|11500|VND"""
et = []
for line in ETSY.splitlines():
    n, p, f, c = line.split('|')
    et.append({'n': n, 'cur': c, 'r': {'pp': float(p), 'pf': float(f), 'listing': 0.20 if c == 'USD' else None}})
dump('etsy/processing.json', et)
print('Etsy', len(et))
