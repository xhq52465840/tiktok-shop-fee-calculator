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
    for g in m['toggles']:
        out = out.replace('{' + g['id'] + '}', g['vals'][1 if s['tg'].get(g['id']) else 0])
    return out

def def_rate(m, c, s):
    if c.get('when') and not s['tg'].get(c['when']): return None
    if c.get('zeroIf') and s['tg'].get(c['zeroIf']): return 0
    r = c['rate']
    if isinstance(r, str) and r.startswith('opt:'): r = m['selector']['options'][s['sel']]['r'].get(key_for(r[4:], m, s))
    if isinstance(r, dict): r = r[s['store']]
    for x in c.get('rateIf', []):
        if s['tg'].get(x['t']): r = x['rate']
    return r

def compute(mid, sel=None, period='new', store='mp', tg=None, rates=None, **inp):
    m = MARKETS[mid]
    s = {'sel': m['defaultOption'] if sel is None else (sel if isinstance(sel, int) else idx(m['selector']['options'], sel)),
         'period': period, 'store': store, 'tg': tg or {}}
    o = dict(price=0, qty=1, sellerDisc=0, buyerShip=0, shipCost=0, cost=0, other=0, affPct=0, tax=0); o.update(inp)
    net = max(0, o['price'] * o['qty'] - o['sellerDisc'])
    b = {'net': net, 'net_ship': net + o['buyerShip'], 'gross': net + o['buyerShip'] + o['tax']}
    rows = []
    for c in m['components']:
        if c.get('when') and not s['tg'].get(c['when']): continue
        r = def_rate(m, c, s)
        if rates and c['id'] in rates: r = rates[c['id']]
        r = r or 0
        if c['type'] == 'fixed':
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
    goods = r2(o['cost'] * o['qty'] + o['other']); profit = r2(payout - goods)
    return dict(b=b, rows=rows, fee={k: a for k, _, a in rows}, rate={k: r for k, r, _ in rows}, total=total, payout=payout, profit=profit,
                margin=(profit / net * 100 if net else 0))
