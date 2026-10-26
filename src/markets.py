"""Market registry. Each entry describes one calculator: its rate file, selectors, toggles and fee components.
Adding a market = add a rate file under src/data/ and an entry here (plus its page copy in content.py)."""
import json, os
D = os.path.join(os.path.dirname(__file__), 'data')
load = lambda p: json.load(open(os.path.join(D, p)))
VERIFIED = '2026-10-26'
C = ['#ea580c', '#f97316', '#fb923c', '#fdba74', '#fcd34d', '#fde68a']

def idx(opts, name):
    return next(i for i, o in enumerate(opts) if o['n'] == name)

MY = load('tiktok-shop/my.json'); PH = load('tiktok-shop/ph.json'); US = load('tiktok-shop/us.json'); ET = load('etsy/processing.json')
for o in ET:
    if o['r']['listing'] is None: o['note'] = 'fx'
def load_ru(p):
    d = load(p); return [{'g': d['groups'][x[0]], 'n': x[1], 'r': x[2]} for x in d['o']], d.get('tables', {})
OZ, OZ_T = load_ru('ozon/ru.json'); WB, _ = load_ru('wildberries/ru.json'); YM, _ = load_ru('yandex-market/ru.json')
def gidx(opts, g, n):
    return next(i for i, o in enumerate(opts) if o['g'] == g and o['n'] == n)
RUB = dict(currency='RUB', symbols={'RUB': '₽'}, symbolAfter=True, locale='ru-RU', decimals=2)
RU_SPEED_WB = [('std', 'sp_std'), ('h13', 'sp_wb13'), ('h42', 'sp_wb42')]
RU_SPEED_YM = [('std', 'sp_std'), ('h36', 'sp_ym36'), ('h28', 'sp_ym28')]
RU_PAYOUT_YM = [('w4', 'po_w4'), ('w2', 'po_w2'), ('w1', 'po_w1'), ('d', 'po_d')]

UK = [{'n': 'Most categories (standard rate)', 'r': {'rate': 9.0}},
      {'n': 'Specified Electronics and Beauty & Personal Care categories (reduced rate)', 'r': {'rate': 5.0}}]

MARKETS = {
 'tiktok-shop-my': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='MY', marketName='Malaysia', slug='tiktok-shop/malaysia',
   flag='🇲🇾', currency='MYR', symbols={'MYR': 'RM'}, locale='en-MY', langs=['en', 'ms'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 39.90, 'cost': 12}, selector={'label': 'cat', 'options': MY},
   defaultOption=idx(MY, 'Beauty & Personal Care › Skincare'),
   store=[('mp', 'mp'), ('mall', 'mall')],
   periods=[('new', 'period_new'), ('old', 'period_old')],
   toggles=[dict(id='bxp', vals=['non', 'bxp']), dict(id='campaign', vals=['', ''], requires='bxp'),
            dict(id='paylater', vals=['', '']), dict(id='psfWaived', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{period}.{store}.{bxp}', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=3.78, rateIf=[{'t': 'paylater', 'rate': 4.86}], base='net_ship', color=C[1]),
     dict(id='bxp', type='pct', rate=4.86, rateIf=[{'t': 'campaign', 'rate': 7.02}], when='bxp', base='net', capPerItem=54, color=C[2]),
     dict(id='psf', type='fixed', rate=0.54, zeroIf='psfWaived', color=C[3])],
   compare=dict(vary=['commission'], a={'label': 'cmp_my_a', 'state': {'period': 'old'}}, b={'label': 'cmp_my_b', 'state': {'period': 'new'}}, note='cmp_my_note'),
   sources=[
     ('Commission Fee & Seller Fees Calculations — TikTok Shop MY Seller University (updated 16 Oct 2026)', 'https://seller-my.tiktok.com/university/essay?knowledge_id=6907739532281602&lang=en'),
     ('Transaction Fee — TikTok Shop MY Seller University', 'https://seller-my.tiktok.com/university/essay?knowledge_id=10013511&lang=en'),
     ('Platform Support Fee — TikTok Shop MY Seller University', 'https://seller-my.tiktok.com/university/essay?knowledge_id=7992113007347457&lang=en'),
     ('Bonus Extra Program (BXP) — TikTok Shop MY Seller University (22 Sep 2026)', 'https://seller-my.tiktok.com/university/essay?knowledge_id=8969995510564625&lang=en')]),
 'tiktok-shop-ph': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='PH', marketName='Philippines', slug='tiktok-shop/philippines',
   flag='🇵🇭', currency='PHP', symbols={'PHP': '₱'}, locale='en-PH', langs=['en'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 499, 'cost': 180}, selector={'label': 'cat', 'options': PH},
   defaultOption=idx(PH, 'Womenswear & Underwear'), store=[('mp', 'mp'), ('mall', 'mall')], periods=None,
   toggles=[dict(id='newSeller', vals=['', '']), dict(id='opfExempt', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}', zeroIf='newSeller', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=2.24, base='net_ship', color=C[1]),
     dict(id='ssf', type='pct', rate={'mp': 5.5, 'mall': 5.0}, base='net', capPerItem=100, color=C[2]),
     dict(id='opf', type='fixed', rate=5, zeroIf='opfExempt', color=C[3]),
     dict(id='growth', type='pct', rate='opt:growth', base='net', color=C[4])],
   compare=dict(vary=[], a={'label': 'cmp_ph_a', 'rates': {'opf': 3, 'growth': 0}}, b={'label': 'cmp_ph_b'}, note='cmp_ph_note'),
   sources=[
     ('Introduction to Seller Fees — TikTok Shop PH Seller University (updated 13 Oct 2026)', 'https://seller-ph.tiktok.com/university/essay?knowledge_id=2675772847064834&lang=en'),
     ('Platform Commission Fee — TikTok Shop PH Seller University', 'https://seller-ph.tiktok.com/university/essay?knowledge_id=3157977859229442&lang=en'),
     ('[Philippines] Order Processing Fee — TikTok Shop Academy (18 Aug 2026)', 'https://seller.tiktokglobalshop.com/university/essay?knowledge_id=6361124523788048'),
     ('Seller Growth Fee start date (27 Apr 2026) — Baijing report, secondary source', 'https://www.baijing.cn/article/55291')]),
 'tiktok-shop-us': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='US', marketName='United States', slug='tiktok-shop/united-states',
   flag='🇺🇸', currency='USD', symbols={'USD': '$'}, locale='en-US', langs=['en'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 24.99, 'cost': 7}, selector={'label': 'cat', 'options': US},
   defaultOption=idx(US, "Womenswear & Underwear › Women's Tops"), store=None, periods=None, toggles=[],
   components=[dict(id='referral', type='pct', rate='opt:rate', base='net_ship', tier={'threshold': 10000, 'key': 'over'}, color=C[0])],
   compare=None,
   sources=[('TikTok Shop Referral Fees by Category — TikTok Shop US Seller University (revised 8 Oct 2026)', 'https://seller-us.tiktok.com/university/essay?knowledge_id=5988482086864682&lang=en')]),
 'tiktok-shop-uk': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='UK', marketName='United Kingdom', slug='tiktok-shop/united-kingdom',
   flag='🇬🇧', currency='GBP', symbols={'GBP': '£'}, locale='en-GB', langs=['en'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 22, 'cost': 7}, selector={'label': 'ukcat', 'options': UK}, defaultOption=0,
   store=None, periods=None, toggles=[],
   components=[dict(id='commission', type='pct', rate='opt:rate', base='net_ship', color=C[0])], compare=None,
   sources=[('TikTok Shop UK Commission Rate Policy — TikTok Shop UK Seller University (policy page dated 18 Sep 2025)', 'https://seller-uk.tiktok.com/university/essay?knowledge_id=3337893683398432&lang=en')]),
 'etsy': dict(
   platform='etsy', platformName='Etsy', market='GLOBAL', marketName='All countries', slug='etsy',
   flag='🧶', currency='USD', symbols={'USD': '$', 'GBP': '£', 'EUR': '€'}, locale='en-US', langs=['en'], currencyFromOption=True,
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'tax', 'other'],
   defaults={'price': 30, 'cost': 9, 'buyerShip': 5}, selector={'label': 'bank', 'options': ET},
   defaultOption=idx(ET, 'United States'), store=None, periods=None, toggles=[],
   components=[
     dict(id='listing', type='fixed', per='item', rate='opt:listing', color=C[3]),
     dict(id='etx', type='pct', rate=6.5, base='net_ship', color=C[0]),
     dict(id='epp', type='pct', rate='opt:pp', base='gross', color=C[1]),
     dict(id='epf', type='fixed', rate='opt:pf', color=C[2])],
   compare=None,
   sources=[('Etsy Fee Basics — Etsy Help', 'https://help.etsy.com/hc/en-us/articles/360035902374-Etsy-Fee-Basics'),
            ('What are Payment Processing Fees for Selling on Etsy? — Etsy Help', 'https://help.etsy.com/hc/en-us/articles/115015628847-What-are-Payment-Processing-Fees-for-Selling-on-Etsy'),
            ('Fees & Payments Policy — Etsy', 'https://www.etsy.com/legal/fees/')]),
 'ozon': dict(
   platform='ozon', platformName='Ozon', market='RU', marketName='Russia', slug='ozon', flag='🇷🇺', **RUB, langs=['en', 'ru'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'vol', 'shipCost', 'taxPct', 'other'],
   defaults={'price': 1500, 'cost': 450, 'vol': 1.5}, selector={'label': 'cat_oz', 'options': OZ, 'src': 'ozon'},
   defaultOption=gidx(OZ, 'Красота и гигиена', 'Косметика для ухода'), tables=OZ_T,
   store=[('fbo', 'm_fbo'), ('fbs', 'm_fbs'), ('rfbs', 'm_rfbs')], periods=None, bands=[100, 300],
   selects=[dict(id='from', label='oz_from', fromTable=['logistics', 'clusters'], first='oz_unknown', defIndex=15, stores=['fbo', 'fbs']),
            dict(id='to', label='oz_to', fromTable=['logistics', 'clusters'], first='oz_unknown', defIndex=15, stores=['fbo', 'fbs'])],
   toggles=[dict(id='heavy', vals=['', ''], stores=['fbo', 'fbs'])],
   components=[
     dict(id='oz_comm', type='pct', rate='opt:{store}', base='net', color=C[0]),
     dict(id='oz_log', type='voltab', table='logistics', **{'from': 'from'}, to='to', whenStore=['fbo', 'fbs'], color=C[1]),
     dict(id='oz_mile', type='fixed', per='item', rate=25, whenStore=['fbo', 'fbs'], color=C[2]),
     dict(id='oz_proc', type='fixed', rate=10, whenStore='fbs', color=C[3]),
     dict(id='oz_heavy', type='pct', rate=3, when='heavy', base='net', capPerItem=280, color=C[4]),
     dict(id='acq', type='pct', rate=None, base='net', manual=True, color=C[5])],
   compare=None,
   sources=[
     ('Полный список комиссий и тарифов — Ozon Seller Edu (edition printed 7 Oct 2026; sections 1, 2.1, 2.4, 2.8, 2.10, 2.23)', 'https://seller-edu.ozon.ru/libra/commissions-tariffs/legal-information/full-actual-commissions'),
     ('Таблица категорий и типов для расчёта вознаграждения, in force from 28 Aug 2026 — Ozon (XLSX)', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8%CC%86_%D0%B4%D0%BB%D1%8F_%D1%80%D0%B0%D1%81%D1%87%D0%B5%CC%88%D1%82%D0%B0_%D0%B2%D0%BE%D0%B7%D0%BD%D0%B0%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F_28082026-3_1787574038.xlsx'),
     ('Логистика FBO и FBS, tariffs in force from 30 Oct 2026 — Ozon (XLSX)', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/logistika-fbo-fbs-30102026_1789376537.xlsx')]),
 'wildberries': dict(
   platform='wildberries', platformName='Wildberries', market='RU', marketName='Russia', slug='wildberries', flag='🇷🇺', **RUB, langs=['en', 'ru'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'vol', 'coef', 'shipCost', 'taxPct', 'other'],
   defaults={'price': 1500, 'cost': 450, 'vol': 1.5, 'coef': 170}, selector={'label': 'cat_wb', 'options': WB, 'src': 'wildberries'},
   defaultOption=gidx(WB, 'Одежда', 'Футболки'),
   store=[('fbw', 'm_fbw'), ('fbs', 'm_fbs'), ('dbs', 'm_dbs')], periods=None,
   selects=[dict(id='speed', label='sp_label', options=RU_SPEED_WB, stores=['fbs'], def_='std')],
   toggles=[],
   components=[
     dict(id='wb_comm', type='pct', rate='opt:{store}', base='net', adj=[{'x': 'speed', 'v': 'h13', 'd': -5}, {'x': 'speed', 'v': 'h42', 'd': -3.5}], minRate=1, color=C[0]),
     dict(id='wb_log', type='vol', vol={'table': [[0.2, 23], [0.4, 26], [0.6, 29], [0.8, 30], [1, 32]], 'first': 46, 'per': 14, 'mult': 'coef'}, whenStore=['fbw', 'fbs'], color=C[1]),
     dict(id='acq', type='pct', rate=None, base='net', manual=True, color=C[5])],
   compare=None,
   sources=[
     ('Таблица со значениями для расчёта КВВ, in force from 7 Jul 2026 — Wildberries (PDF)', 'https://static-basket-02.wbbasket.ru/vol20/folder/comission/KVV_Wildberries_ru_20260630.pdf'),
     ('Доставка: виды и расчёт стоимости — Wildberries seller instructions (updated 19 Oct 2026)', 'https://seller.wildberries.ru/instructions/ru/ru/material/logistics-types-and-cost-calculation'),
     ('Коэффициент вознаграждения Wildberries — seller instructions', 'https://seller.wildberries.ru/instructions/ru/ru/material/wildberries-reward-ratio'),
     ('Wildberries cuts FBS late-shipment penalties; FBS fast-shipping commission discounts −5 / −3.5 p.p. — Kommersant, 7 Oct 2026 (secondary)', 'https://www.kommersant.ru/doc/9008220')]),
 'yandex-market': dict(
   platform='yandex-market', platformName='Yandex Market', market='RU', marketName='Russia', slug='yandex-market', flag='🇷🇺', **RUB, langs=['en', 'ru'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'vol', 'shipCost', 'taxPct', 'other'],
   defaults={'price': 1500, 'cost': 450, 'vol': 1.5}, selector={'label': 'cat_ym', 'options': YM, 'src': 'yandex-market'},
   defaultOption=gidx(YM, 'Товары для красоты', 'Косметика, парфюмерия и уход › Уход за лицом'),
   store=[('fby', 'm_fby'), ('fbs', 'm_fbs'), ('dbs', 'm_dbs')], periods=None,
   conds={'cheap': {'maxUnit': 300, 'maxVol': 5, 'stores': ['fby', 'fbs']}},
   selects=[dict(id='payout', label='po_label', options=RU_PAYOUT_YM, def_='w1'),
            dict(id='speed', label='sp_label', options=RU_SPEED_YM, stores=['fbs'], def_='std')],
   toggles=[],
   components=[
     dict(id='ym_place', type='pct', rate='opt:{store}', base='net', condRate={'cheap': 42}, adj=[{'x': 'speed', 'v': 'h36', 'd': -4}, {'x': 'speed', 'v': 'h28', 'd': -7}], color=C[0]),
     dict(id='ym_deliv', type='pct', rate=5, base='net', capPerItem=1000, whenStore=['fby', 'fbs'], condZero=['cheap'], color=C[1]),
     dict(id='ym_mid', type='vol', vol={'ceil': True, 'table': [[1, 92]], 'first': 92, 'per': 8, 'steps': [[200, 5]], 'cap': 5500}, whenStore=['fby', 'fbs'], condZero=['cheap'], color=C[2]),
     dict(id='ym_proc', type='fixed', rate=25, whenStore='fbs', color=C[3]),
     dict(id='ym_transfer', type='pct', rate={'w4': 1.6, 'w2': 2.3, 'w1': 2.8, 'd': 3.3}, by='payout', base='net', color=C[4]),
     dict(id='ym_accept', type='fixed', rate=0.12, color=C[5])],
   compare=None,
   sources=[
     ('Размещение товаров на витрине (category tariffs) — Yandex Market help', 'https://yandex.ru/support/marketplace/ru/introduction/rates/placement'),
     ('Тарифы на услуги по модели FBY — Yandex Market help', 'https://yandex.ru/support/marketplace/ru/introduction/rates/models/fby'),
     ('Тарифы на услуги по модели FBS — Yandex Market help', 'https://yandex.ru/support/marketplace/ru/introduction/rates/models/fbs'),
     ('Приём и перевод платежей покупателей — Yandex Market help', 'https://yandex.ru/support/marketplace/ru/introduction/rates/acquiring')]),
}

COMING = [
  ('TikTok Shop', 'Singapore', '🇸🇬'), ('TikTok Shop', 'Thailand', '🇹🇭'), ('TikTok Shop', 'Vietnam', '🇻🇳'), ('TikTok Shop', 'Indonesia', '🇮🇩'),
  ('Shopee', 'Malaysia, Philippines & more', '🛍️'), ('Lazada', 'Malaysia, Philippines & more', '📦'), ('Amazon', 'US, UK & more', '📦'), ('eBay', 'US & UK', '🏷️')]

# ---------- Python mirror of assets/engine.js (used to compute worked examples in the guides)
from decimal import Decimal, ROUND_HALF_UP
def r2(n):
    return float(Decimal(format(n * 100, '.12g')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) / 100

def key_for(tpl, m, s):
    out = tpl.replace('{period}', str(s.get('period'))).replace('{store}', str(s.get('store')))
    for k, v in s.get('x', {}).items(): out = out.replace('{x:' + k + '}', str(v))
    for g in m['toggles']:
        out = out.replace('{' + g['id'] + '}', g['vals'][1 if s['tg'].get(g['id']) else 0])
    return out

def in_list(v, l):
    return l is None or (v in l if isinstance(l, list) else v == l)

def active(c, s):
    if c.get('when') and not s['tg'].get(c['when']): return False
    return in_list(s.get('store'), c.get('whenStore'))

def unit_price(o):
    return max(0, o['price'] * o['qty'] - o['sellerDisc']) / o['qty'] if o['qty'] else 0

def conds(m, s, o):
    out = {}
    for k, c in (m.get('conds') or {}).items():
        out[k] = in_list(s.get('store'), c.get('stores')) and unit_price(o) <= c.get('maxUnit', 1e18) and o['vol'] <= c.get('maxVol', 1e18)
    return out

def def_rate(m, c, s, o):
    if not active(c, s): return None
    if c.get('zeroIf') and s['tg'].get(c['zeroIf']): return 0
    r = c.get('rate'); cd = conds(m, s, o)
    if isinstance(r, str) and r.startswith('opt:'):
        R = m['selector']['options'][s['sel']]['r']; k = key_for(r[4:], m, s); r = R.get(k, R.get('_'))
    if isinstance(r, dict): r = r[s['x'][c['by']]] if c.get('by') else r[s['store']]
    if isinstance(r, list):
        b = sum(1 for th in m.get('bands', []) if unit_price(o) > th); r = r[min(b, len(r) - 1)]
    for x in c.get('rateIf', []):
        if s['tg'].get(x['t']): r = x['rate']
    replaced = False
    for k, v in (c.get('condRate') or {}).items():
        if cd.get(k): r = v; replaced = True
    if r is None: return None
    if not replaced:
        for a in c.get('adj', []):
            if (s['tg'].get(a['t']) if a.get('t') else s['x'].get(a['x']) == a['v']): r += a['d']
    if c.get('minRate') is not None: r = max(r, c['minRate'])
    return r2(r)

def vol_cost(v, L):
    import math
    if not L or L <= 0: return 0
    if v.get('ceil'): L = math.ceil(L - 1e-9)
    tb = v.get('table', [])
    if tb and L <= tb[-1][0]:
        p = next(pr for mx, pr in tb if L <= mx + 1e-9)
    else:
        p = v['first'] + v['per'] * max(0, L - 1)
        for frm, add in v.get('steps', []):
            if L > frm: p += (L - frm) * add
    if v.get('cap') is not None: p = min(p, v['cap'])
    return p

def voltab_cost(m, c, s, o):
    tb = m['tables'][c['table']]; L = o['vol']
    if not L or L <= 0: return 0, None
    bi = 0
    while bi < len(tb['upper']) - 1 and L > tb['upper'][bi] + 1e-9: bi += 1
    fr, to = s['x'].get(c['from'], ''), s['x'].get(c['to'], '')
    arr = tb['routes'].get(f'{fr}-{to}') if fr != '' and to != '' else None
    arr = arr or tb['default']
    return arr[bi][1 if unit_price(o) > tb['bands'][0] else 0], tb['labels'][bi]

def compute(mid, sel=None, period='new', store=None, tg=None, rates=None, x=None, **inp):
    m = MARKETS[mid]
    if store is None: store = m['store'][0][0] if m.get('store') else 'mp'
    xs = {d['id']: (d.get('defIndex', '') if d.get('fromTable') else d.get('def_')) for d in m.get('selects', [])}
    xs.update(x or {})
    s = {'sel': m['defaultOption'] if sel is None else (sel if isinstance(sel, int) else idx(m['selector']['options'], sel)),
         'period': period, 'store': store, 'tg': tg or {}, 'x': xs}
    o = dict(price=0, qty=1, sellerDisc=0, buyerShip=0, shipCost=0, cost=0, other=0, affPct=0, tax=0, taxPct=0, vol=0, coef=100); o.update(inp)
    net = max(0, o['price'] * o['qty'] - o['sellerDisc'])
    b = {'net': net, 'net_ship': net + o['buyerShip'], 'gross': net + o['buyerShip'] + o['tax']}
    rows = []; cd = conds(m, s, o)
    for c in m['components']:
        if not active(c, s): continue
        if any(cd.get(k) for k in c.get('condZero', [])): rows.append((c['id'], 0, 0)); continue
        r = def_rate(m, c, s, o)
        if rates and c['id'] in rates: r = rates[c['id']]
        r = r or 0
        if c['type'] == 'vol':
            amt = vol_cost(c['vol'], o['vol']) * (o[c['vol']['mult']] / 100 if c['vol'].get('mult') else 1) * o['qty']
        elif c['type'] == 'voltab':
            amt = voltab_cost(m, c, s, o)[0] * o['qty']
        elif c['type'] == 'fixed':
            amt = r * (o['qty'] if c.get('per') == 'item' else 1)
        else:
            base = b[c.get('base', 'net')]; amt = base * r / 100
            if c.get('tier'):
                over = m['selector']['options'][s['sel']]['r'].get(c['tier']['key'])
                if over is not None and base > c['tier']['threshold']:
                    amt = c['tier']['threshold'] * r / 100 + (base - c['tier']['threshold']) * over / 100
            if c.get('capPerItem'): amt = min(amt, c['capPerItem'] * o['qty'])
        rows.append((c['id'], r, r2(amt)))
    if o['affPct'] > 0: rows.append(('aff', o['affPct'], r2(net * o['affPct'] / 100)))
    total = r2(sum(x[2] for x in rows)); payout = r2(b['net_ship'] - o['shipCost'] - total)
    goods = r2(o['cost'] * o['qty'] + o['other']); tax = r2(net * o['taxPct'] / 100); profit = r2(payout - goods - tax)
    return dict(b=b, rows=rows, fee={k: a for k, _, a in rows}, rate={k: r for k, r, _ in rows}, total=total, payout=payout, profit=profit,
                tax=tax, cond=cd, margin=(profit / net * 100 if net else 0))
