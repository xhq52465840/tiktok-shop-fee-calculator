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
SH_MY = load('shopee/my.json'); SH_SG = load('shopee/sg.json'); LZ_MY = load('lazada/my.json')
SH_PH = load('shopee/ph.json'); WM_US = load('walmart/us.json')
SH_TH, _ = (lambda d: ([{'g': d['groups'][x[0]], 'n': x[1], 'r': x[2]} for x in d['o']], None))(load('shopee/th.json'))
# Walmart Fulfillment Services standard base fee per unit by shipping weight (lb): [max lb, base, per lb, counted from lb]
WFS_STD = [[1, 3.45, 0, 0], [2, 4.95, 0, 0], [3, 5.45, 0, 0], [20, 5.75, 0.40, 4], [30, 15.55, 0.40, 21], [50, 14.55, 0.40, 31], [150, 17.55, 0.40, 51]]
WM_NSS = [('none', 'nss_none'), ('t20', 'nss_t20'), ('t30', 'nss_t30'), ('t40', 'nss_t40')]
SH_TH_TIER = [('std', 'th_tier_std'), ('prime', 'th_tier_prime'), ('small', 'th_tier_small'), ('smallprime', 'th_tier_smallprime')]
for o in ET:
    if o['r']['listing'] is None: o['note'] = 'fx'
def load_ru(p):
    d = load(p); return [{'g': d['groups'][x[0]], 'n': x[1], 'r': x[2]} for x in d['o']], d.get('tables', {})
OZ, OZ_T = load_ru('ozon/ru.json'); WB, _ = load_ru('wildberries/ru.json'); YM, _ = load_ru('yandex-market/ru.json')
TT_SG, _ = load_ru('tiktok-shop/sg.json'); TT_TH, _ = load_ru('tiktok-shop/th.json'); TT_VN, _ = load_ru('tiktok-shop/vn.json'); TT_ID, _ = load_ru('tiktok-shop/id.json'); SH_ID, _ = load_ru('shopee/id.json'); SH_VN, _ = load_ru('shopee/vn.json')
# TikTok Shop & Tokopedia ID Platform Commission Savings from 18 May 2026 (GMV Max / Growth Xtra)
TT_ID_SAV = [('none', 'idsav_none'), ('gmo', 'idsav_gmo'), ('gx', 'idsav_gx'), ('gxgmo', 'idsav_gxgmo'), ('s3', 'idsav_s3'), ('s3gx', 'idsav_s3gx')]
VND = dict(currency='VND', symbols={'VND': '₫'}, symbolAfter=True, locale='en-US', decimals=0, roundFees=0)
IDR = dict(currency='IDR', symbols={'IDR': 'Rp'}, locale='en-US', decimals=0, roundFees=0)
# Shopee ID optional programmes: Gratis Ongkir XTRA (current table, and the table from 1 Dec 2026 non-Mall / 1 Jan 2027 Mall) and Promo XTRA
SH_ID_GOX = [('none', 'sidgox_none'), ('cur_reg', 'sidgox_cur_reg'), ('cur_spec', 'sidgox_cur_spec'), ('new_reg', 'sidgox_new_reg'), ('new_spec', 'sidgox_new_spec')]
SH_ID_PX = [('none', 'sidpx_none'), ('px', 'sidpx_px'), ('pxp', 'sidpx_pxp')]
# TikTok Shop VN Transaction Fee Savings from 21 Oct 2026, by the shop's L30D ads take rate
TT_VN_TXS = [('none', 'txs_none'), ('t05', 'txs_t05'), ('t07', 'txs_t07'), ('t10', 'txs_t10'), ('t12', 'txs_t12'), ('t15', 'txs_t15')]
# Etsy UK: Etsy bills the listing fee (US$0.20) and caps Offsite Ads (US$100/order) in US dollars.
# Converted at the ECB reference rate published 26 Oct 2026 (1 USD = 0.7492 GBP); both are editable in the calculator.
USD_GBP = 0.7492
ETSY_UK_VAT = [{'n': 'Not VAT-registered, or no UK VAT number added in Etsy', 'r': {'vat': 20}},
               {'n': 'VAT number added in Etsy (Etsy charges no VAT on its fees)', 'r': {'vat': 0}}]
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
   flag='🇲🇾', currency='MYR', symbols={'MYR': 'RM'}, locale='en-MY', langs=['en', 'ms', 'zh'],
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
   flag='🇵🇭', currency='PHP', symbols={'PHP': '₱'}, locale='en-PH', langs=['en', 'zh'],
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
     ('Seller Growth Fee start date (27 Apr 2026) — Baijing report, secondary source', 'https://www.baijing.cn/article/55291'),
     ('Seller Growth Fee change from 1 Nov 2026 — AMZ123 report (27 Oct 2026), secondary source', 'https://www.amz123.com/t/InpmAzN5')]),
 'tiktok-shop-us': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='US', marketName='United States', slug='tiktok-shop/united-states',
   flag='🇺🇸', currency='USD', symbols={'USD': '$'}, locale='en-US', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 24.99, 'cost': 7}, selector={'label': 'cat', 'options': US},
   defaultOption=idx(US, "Womenswear & Underwear › Women's Tops"), store=None, periods=None, toggles=[],
   components=[dict(id='referral', type='pct', rate='opt:rate', base='net_ship', tier={'threshold': 10000, 'key': 'over'}, color=C[0])],
   compare=None,
   sources=[('TikTok Shop Referral Fees by Category — TikTok Shop US Seller University (revised 8 Oct 2026)', 'https://seller-us.tiktok.com/university/essay?knowledge_id=5988482086864682&lang=en')]),
 'tiktok-shop-uk': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='UK', marketName='United Kingdom', slug='tiktok-shop/united-kingdom',
   flag='🇬🇧', currency='GBP', symbols={'GBP': '£'}, locale='en-GB', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 22, 'cost': 7}, selector={'label': 'ukcat', 'options': UK}, defaultOption=0,
   store=None, periods=None, toggles=[],
   components=[dict(id='commission', type='pct', rate='opt:rate', base='net_ship', color=C[0])], compare=None,
   sources=[('TikTok Shop UK Commission Rate Policy — TikTok Shop UK Seller University (policy page dated 18 Sep 2025)', 'https://seller-uk.tiktok.com/university/essay?knowledge_id=3337893683398432&lang=en')]),
 'tiktok-shop-sg': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='SG', marketName='Singapore', slug='tiktok-shop/singapore',
   flag='🇸🇬', currency='SGD', symbols={'SGD': 'S$'}, locale='en-SG', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 29.90, 'cost': 9}, selector={'label': 'cat', 'options': TT_SG, 'src': 'tiktok-sg'},
   defaultOption=gidx(TT_SG, 'Beauty & Personal Care', 'Skincare › Serums & Essences'),
   store=None, periods=[('new', 'period_sg_new'), ('old', 'period_sg_old')],
   toggles=[dict(id='bxp', vals=['non', 'bxp']), dict(id='sgCampaign', vals=['', ''], requires='bxp')],
   components=[
     dict(id='commission', type='pct', rate='opt:{period}.{bxp}', base='net', capPerItem='opt:cap_{period}', color=C[0]),
     dict(id='tx', type='pct', rate=3.27, base='net_ship', color=C[1]),
     dict(id='bxp', type='pct', rate='opt:bxpfee', when='bxp', adj=[{'t': 'sgCampaign', 'd': 1.09}], base='net', capPerItem=30, color=C[2])],
   compare=dict(vary=['commission'], a={'label': 'cmp_sg_a', 'state': {'period': 'old'}}, b={'label': 'cmp_sg_b', 'state': {'period': 'new'}}, note='cmp_sg_note'),
   sources=[
     ('Platform Commission Fee (table from 1 Sep 2026, GST-inclusive) — TikTok Shop SG Seller University (updated 17 Aug 2026)', 'https://seller-sg.tiktok.com/university/essay?knowledge_id=2161524467910401&lang=en'),
     ('Transaction Fee — TikTok Shop SG Seller University (13 Mar 2026)', 'https://seller-sg.tiktok.com/university/essay?knowledge_id=780268081530625&lang=en'),
     ('Bonus Extra Program (BXP) service fee — TikTok Shop SG Seller University (24 Aug 2026)', 'https://seller-sg.tiktok.com/university/essay?knowledge_id=2192573259400976&lang=en'),
     ('Introduction to Seller Fees — TikTok Shop SG Seller University (13 Mar 2026)', 'https://seller-sg.tiktok.com/university/essay?knowledge_id=113323786536705&lang=en')]),
 'tiktok-shop-th': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='TH', marketName='Thailand', slug='tiktok-shop/thailand',
   flag='🇹🇭', currency='THB', symbols={'THB': '฿'}, locale='en-TH', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 299, 'cost': 90}, selector={'label': 'cat', 'options': TT_TH, 'src': 'tiktok-th'},
   defaultOption=gidx(TT_TH, 'Beauty & Personal Care', 'Skincare › Serums & Essences'),
   store=[('mp', 'mp'), ('mall', 'mall')], periods=[('new', 'period_th_new'), ('old', 'period_th_old')],
   toggles=[dict(id='combo', vals=['', '_combo'], stores=['mall']), dict(id='gmvMax', vals=['', ''], stores=['mp']),
            dict(id='smallSeller', vals=['', ''], stores=['mp']), dict(id='cgfWaived', vals=['', '']), dict(id='pifWaived', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{period}.{store}{combo}', adj=[{'t': 'gmvMax', 'd': -1.07}], base='net', color=C[0]),
     dict(id='tx', type='pct', rate=3.21, base='net_ship', color=C[1]),
     dict(id='cgf', type='pct', rate='opt:cgf', adj=[{'t': 'smallSeller', 'd': -0.54}], zeroIf='cgfWaived', base='net', capPerItem=199, color=C[2]),
     dict(id='pif', type='fixed', rate=1.07, zeroIf='pifWaived', color=C[3])],
   compare=dict(vary=['commission'], a={'label': 'cmp_th_a', 'state': {'period': 'old'}}, b={'label': 'cmp_th_b', 'state': {'period': 'new'}}, note='cmp_th_note'),
   sources=[
     ('Platform Commission Fee for Marketplace (non-Mall) sellers, table from 5 Jul 2026 — TikTok Shop TH Seller University (updated 17 Jul 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=10014445&lang=en'),
     ('Mall Commission Fee, table from 5 Jul 2026 — TikTok Shop TH Seller University (updated 17 Jul 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=7485510424282896&lang=en'),
     ('Mall Combo Package — TikTok Shop TH Seller University (21 Sep 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=7576841150449425&lang=en'),
     ('Transaction Fee — TikTok Shop TH Seller University (20 Feb 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=6837804139087618&lang=en'),
     ('Commerce Growth Fee — TikTok Shop TH Seller University (21 Sep 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=4831419884979969&lang=en'),
     ('Platform Infrastructure Fee — TikTok Shop TH Seller University (3 Jul 2026)', 'https://seller-th.tiktok.com/university/essay?knowledge_id=4832028500215569&lang=en')]),
 'tiktok-shop-vn': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='VN', marketName='Vietnam', slug='tiktok-shop/vietnam',
   flag='🇻🇳', **VND, langs=['en'], catLang='en',
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 199000, 'cost': 60000}, selector={'label': 'cat', 'options': TT_VN, 'src': 'tiktok-vn'},
   defaultOption=gidx(TT_VN, 'Beauty & Personal Care', 'Skincare › Serums & Essences'),
   store=[('mp', 'mp'), ('mall', 'mall')], periods=None,
   selects=[dict(id='txs', label='txs_label', options=TT_VN_TXS, def_='none')],
   toggles=[dict(id='vnWht', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=6, base='net_ship', adj=[{'x': 'txs', 'v': 't05', 'd': -0.5}, {'x': 'txs', 'v': 't07', 'd': -0.7}, {'x': 'txs', 'v': 't10', 'd': -1.0},
                                                         {'x': 'txs', 'v': 't12', 'd': -1.2}, {'x': 'txs', 'v': 't15', 'd': -1.5}], color=C[1]),
     dict(id='opf', type='fixed', rate=3000, color=C[3]),
     dict(id='wht', type='pct', rate=1.5, when='vnWht', base='net', color=C[5])],
   compare=None,
   sources=[
     ('Platform Commission Fee (Marketplace table from 3 Jul 2026, Mall table from 20 Oct 2026) — TikTok Shop VN Seller University (updated 30 Sep 2026)', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=3396736626312961&lang=en'),
     ('Introduction to Seller Fees — TikTok Shop VN Seller University (4 Aug 2026)', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=8858869405370113&lang=en'),
     ('Transaction Fee (6% from 9 May 2026; savings tiers from 21 Oct 2026) — TikTok Shop VN Seller University (13 Oct 2026)', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=753295858337537&lang=en'),
     ('Order Processing Fee (VND 3,000 per order from 27 Oct 2025) — TikTok Shop VN Seller University', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=2968734088120080&lang=en'),
     ('Logistics Service Fee for parcels over 10 kg (from 12 Oct 2026) — TikTok Shop VN Seller University (8 Oct 2026)', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=4723305845458708&lang=en'),
     ('Withholding Taxes for Individual and Business Household Sellers (1% VAT + 0.5% PIT) — TikTok Shop VN Seller University', 'https://seller-vn.tiktok.com/university/essay?knowledge_id=2632156783101712&lang=en')]),
 'tiktok-shop-id': dict(
   platform='tiktok-shop', platformName='TikTok Shop', market='ID', marketName='Indonesia', slug='tiktok-shop/indonesia',
   flag='🇮🇩', **IDR, langs=['en'], catLang='en',
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 89000, 'cost': 30000}, selector={'label': 'cat', 'options': TT_ID, 'src': 'tiktok-id'},
   defaultOption=gidx(TT_ID, 'Beauty & Personal Care', 'Skincare › Serums & Essences'),
   store=[('mp', 'mp'), ('mall', 'mall')], periods=None,
   selects=[dict(id='sav', label='idsav_label', options=TT_ID_SAV, def_='none')],
   toggles=[dict(id='idNew', vals=['', '']), dict(id='preOrder', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}.{x:sav}', base='net', color=C[0]),
     dict(id='dcf', type='pct', rate='opt:dcf', base='net', capPerItem=60000, color=C[1]),
     dict(id='mallsf', type='pct', rate=1.8, base='net', capPerItem=50000, whenStore='mall', color=C[2]),
     dict(id='opf', type='fixed', rate=1250, zeroIf='idNew', color=C[3]),
     dict(id='lsf', type='fixed', rate=690, color=C[4]),
     dict(id='preorder', type='pct', rate=3, base='net', when='preOrder', color=C[5]),
     dict(id='gxp', type='pct', rate=None, base='net_ship', manual=True, color=C[0])],
   compare=None,
   sources=[
     ('Platform Commission Fee and Platform Commission Savings from 18 May 2026 (PDF and fee calculator XLSX) — TikTok Shop & Tokopedia Seller University (updated 28 Apr 2026)', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=5411650459305729&lang=en'),
     ('Dynamic Commission Fee (3%–8% by category, capped at Rp60,000 per item) — TikTok Shop & Tokopedia Seller University (16 Sep 2026)', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=6385751723132688&lang=en'),
     ('Introduction to Seller Fees — TikTok Shop & Tokopedia Seller University (15 Sep 2026)', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=7753828090824449&lang=en'),
     ('Mall Service Fee (1.8%, capped at Rp50,000 per product) — TikTok Shop & Tokopedia Seller University', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=7868735055857409&lang=en'),
     ('Order Processing Fee (Rp1,250 per order; first 50 orders free for new sellers) — TikTok Shop & Tokopedia Seller University (28 Apr 2026)', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=2767365667784464&lang=en'),
     ('Logistics Service Fee effective 1 May 2026 (rate table XLSX) — TikTok Shop & Tokopedia Seller University (7 Aug 2026)', 'https://seller-id.tokopedia.com/university/essay?knowledge_id=3039885401655041&lang=en')]),
 'shopee-id': dict(
   platform='shopee', platformName='Shopee', market='ID', marketName='Indonesia', slug='shopee/indonesia',
   flag='🇮🇩', **IDR, langs=['en'], catLang='id',
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 89000, 'cost': 30000}, selector={'label': 'cat', 'options': SH_ID, 'src': 'shopee-id'},
   defaultOption=gidx(SH_ID, 'Perawatan & Kecantikan', 'Perawatan Wajah'),
   store=[('nonstar', 'nonstar'), ('star', 'star'), ('mall', 'mall')], periods=None,
   selects=[dict(id='gox', label='sidgox_label', options=SH_ID_GOX, def_='none'), dict(id='px', label='sidpx_label', options=SH_ID_PX, def_='none')],
   toggles=[dict(id='sidNew', vals=['', '']), dict(id='liveX', vals=['', '']), dict(id='preOrder', vals=['', ''])],
   components=[
     dict(id='admin', type='pct', rate='opt:{store}', zeroIf='sidNew', base='net', color=C[0]),
     dict(id='mallpay', type='pct', rate=1.8, base='net', capPerItem=50000, whenStore='mall', color=C[1]),
     dict(id='opf', type='fixed', rate=1250, zeroIf='sidNew', color=C[3]),
     dict(id='gox', type='pct', rate='opt:{x:gox}', base='net', capPerItem='opt:cap_{x:gox}', whenX=['gox', ['cur_reg', 'cur_spec', 'new_reg', 'new_spec']], color=C[2]),
     dict(id='promox', type='pct', rate=4.5, base='net', capPerItem=60000, whenX=['px', ['px']], color=C[4]),
     dict(id='promoxp', type='pct', rate=6.5, base='net', capPerItem=80000, whenX=['px', ['pxp']], color=C[4]),
     dict(id='livex', type='pct', rate=3, base='net', capPerItem=20000, when='liveX', adj=[{'x': 'px', 'v': 'px', 'd': -1}, {'x': 'px', 'v': 'pxp', 'd': -1}], color=C[5]),
     dict(id='preorder', type='pct', rate=3, base='net', when='preOrder', color=C[0])],
   compare=None,
   sources=[
     ('Ringkasan Jenis Biaya untuk Berjualan di Shopee (fee summary by seller type) — Shopee ID Seller Education Hub (31 Jul 2026)', 'https://seller.shopee.co.id/edu/article/3489'),
     ('Biaya Administrasi Penjual Shopee (Non-Star, Star/Star+, Mall; no cap; new-seller waiver) — Shopee ID Seller Education Hub (31 Jul 2026)', 'https://seller.shopee.co.id/edu/article/7187'),
     ('Rincian Biaya Penjual Shopee per Kategori Produk (admin fee by product type) — Shopee ID Seller Education Hub (31 Jul 2026)', 'https://seller.shopee.co.id/edu/article/15965'),
     ('Ketentuan Biaya untuk Penjual Shopee Mall (1.8% payment fee, max Rp50,000 per item) — Shopee ID Seller Education Hub (23 Jul 2026)', 'https://seller.shopee.co.id/edu/article/6756'),
     ('Rincian Persentase Gratis Ongkir XTRA by product (current table, and new table from 1 Dec 2026 non-Mall / 1 Jan 2027 Mall) — Shopee ID Seller Education Hub (14 Oct 2026)', 'https://seller.shopee.co.id/edu/article/7216'),
     ('Program Opsional Promo XTRA — Shopee ID Seller Education Hub (20 Oct 2026)', 'https://seller.shopee.co.id/edu/article/18196'),
     ('Ilustrasi Perhitungan Estimasi Biaya Proses Pesanan (Rp1,250 per completed order) — Shopee ID Seller Education Hub', 'https://seller.shopee.co.id/edu/article/25275')]),
 'shopee-vn': dict(
   platform='shopee', platformName='Shopee', market='VN', marketName='Vietnam', slug='shopee/vietnam',
   flag='🇻🇳', **VND, langs=['en'], catLang='vi',
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 199000, 'cost': 60000}, selector={'label': 'cat', 'options': SH_VN, 'src': 'shopee-vn'},
   defaultOption=gidx(SH_VN, 'Sắc Đẹp', 'Chăm sóc da mặt › Tinh chất dưỡng'),
   store=[('mp', 'mp_nonmall'), ('mall', 'mall')], periods=None,
   toggles=[dict(id='svnNew', vals=['', '']), dict(id='vXtra', vals=['', '']), dict(id='piShip', vals=['', '']), dict(id='svWht', vals=['', ''])],
   components=[
     dict(id='fixedfee', type='pct', rate='opt:{store}', zeroIf='svnNew', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=6, base='net_ship', color=C[1]),
     dict(id='infra', type='fixed', rate=3000, color=C[3]),
     dict(id='vxtra', type='pct', rate=5.5, base='net', capPerItem=50000, when='vXtra', color=C[2]),
     dict(id='piship', type='fixed', rate=2700, when='piShip', color=C[4]),
     dict(id='wht', type='pct', rate=1.5, when='svWht', base='net', color=C[5])],
   compare=None,
   sources=[
     ('Một số phí bán hàng trên Shopee (fee overview) — Shopee VN Seller Education Hub (14 May 2026)', 'https://banhang.shopee.vn/edu/article/251'),
     ('Phí Cố Định for non-Mall sellers from 23 May 2026 (category table PDF attached) — Shopee VN Seller Education Hub (14 May 2026)', 'https://banhang.shopee.vn/edu/article/2139'),
     ('Phí Cố Định for Shopee Mall sellers from 4 Oct 2026 (category table PDF attached) — Shopee VN Seller Education Hub (14 Sep 2026)', 'https://banhang.shopee.vn/edu/article/2579'),
     ('Phí Xử Lý Giao Dịch (6% transaction processing fee from 1 May 2026 non-Mall / 8 May 2026 Mall) — Shopee VN Seller Education Hub (24 Apr 2026)', 'https://banhang.shopee.vn/edu/article/2150'),
     ('Phí Hạ Tầng (infrastructure fee, 3,000 ₫ per order) — Shopee VN Seller Education Hub', 'https://banhang.shopee.vn/edu/article/25223'),
     ('Fee and policy update from 23 May 2026: Voucher Xtra 5.5% (max 50,000 ₫ per item), PiShip 2,700 ₫ per order — Shopee VN Seller Education Hub (28 May 2026)', 'https://banhang.shopee.vn/edu/article/27540'),
     ('Ưu đãi Người bán hàng mới: no fixed fee for 30 days — Shopee VN Seller Education Hub', 'https://banhang.shopee.vn/edu/article/19130'),
     ('Shopee withholds 1% VAT + 0.5% PIT for household and individual sellers from 1 Jul 2025 (Decree 117/2025) — Shopee VN Seller Education Hub', 'https://banhang.shopee.vn/edu/article/24233')]),
 'etsy': dict(
   platform='etsy', platformName='Etsy', market='GLOBAL', marketName='All countries', slug='etsy',
   flag='🧶', currency='USD', symbols={'USD': '$', 'GBP': '£', 'EUR': '€'}, locale='en-US', langs=['en', 'zh'], currencyFromOption=True,
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
 'etsy-uk': dict(
   platform='etsy', platformName='Etsy', market='UK', marketName='UK', slug='etsy/uk',
   flag='🇬🇧', currency='GBP', symbols={'GBP': '£'}, locale='en-GB', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'tax', 'taxPct', 'other'],
   hints={'tax': 'tax_uk_h', 'taxPct': 'taxPct_uk_h'},
   defaults={'price': 25, 'cost': 8, 'buyerShip': 4}, selector={'label': 'vat_uk', 'options': ETSY_UK_VAT},
   defaultOption=0, store=None, periods=None,
   toggles=[dict(id='offsite', vals=['', '']), dict(id='offsite12', vals=['', ''], requires='offsite')],
   components=[
     dict(id='listing', type='fixed', per='item', rate=round(0.20 * USD_GBP, 2), color=C[3]),
     dict(id='etx', type='pct', rate=6.5, base='net_ship', color=C[0]),
     dict(id='epp', type='pct', rate=4, base='gross', color=C[1]),
     dict(id='epf', type='fixed', rate=0.20, color=C[2]),
     dict(id='rof', type='pct', rate=0.48, base='net_ship', color=C[4]),
     dict(id='offads', type='pct', rate=15, rateIf=[{'t': 'offsite12', 'rate': 12}], when='offsite', base='net_ship', capPerOrder=round(100 * USD_GBP, 2), color='#c2410c'),
     dict(id='feevat', type='pct', rate='opt:vat', base='fees', color=C[5])],
   compare=None,
   sources=[('Etsy Fee Basics — Etsy Help (en-GB)', 'https://help.etsy.com/hc/en-gb/articles/360035902374-Etsy-Fee-Basics'),
            ('What are Payment Processing Fees for Selling on Etsy? (United Kingdom: 4% + 0.20 GBP) — Etsy Help', 'https://help.etsy.com/hc/en-gb/articles/115015628847-What-are-Payment-Processing-Fees-for-Selling-on-Etsy'),
            ('What is a Regulatory Operating Fee? (UK 0.48%) — Etsy Help', 'https://help.etsy.com/hc/en-us/articles/1500011073202-What-is-a-Regulatory-Operating-Fee'),
            ('Regulatory Operating Fee updates for some markets (UK 0.32% → 0.48% from 22 Jun 2026) — Etsy Community announcement', 'https://community.etsy.com/forum/announcements-290/topic/regulatory-operating-fee-updates-for-some-markets-181930/'),
            ('How VAT Is Collected on Seller Fees — Etsy Help (en-GB)', 'https://help.etsy.com/hc/en-gb/articles/360040584433-How-VAT-Is-Collected-on-Seller-Fees'),
            ("How Etsy's Offsite Ads Work (15% / 12%, max US$100 per order) — Etsy Help (en-GB)", 'https://help.etsy.com/hc/en-gb/articles/360000338367-How-Etsy-s-Offsite-Ads-Work'),
            ('Fees & Payments Policy — Etsy UK', 'https://www.etsy.com/uk/legal/fees/'),
            ('VAT rates (standard rate 20%) — GOV.UK', 'https://www.gov.uk/vat-rates'),
            ('Euro foreign exchange reference rates, 26 Oct 2026 (USD/GBP used to convert US$ amounts) — European Central Bank', 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html')]),
 'ozon': dict(
   platform='ozon', platformName='Ozon', market='RU', marketName='Russia', slug='ozon', flag='🇷🇺', **RUB, langs=['en', 'ru', 'zh'],
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
   platform='wildberries', platformName='Wildberries', market='RU', marketName='Russia', slug='wildberries', flag='🇷🇺', **RUB, langs=['en', 'ru', 'zh'],
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
   platform='yandex-market', platformName='Yandex Market', market='RU', marketName='Russia', slug='yandex-market', flag='🇷🇺', **RUB, langs=['en', 'ru', 'zh'],
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
 'shopee-my': dict(
   platform='shopee', platformName='Shopee', market='MY', marketName='Malaysia', slug='shopee/malaysia',
   flag='🇲🇾', currency='MYR', symbols={'MYR': 'RM'}, locale='en-MY', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 39.90, 'cost': 12}, selector={'label': 'cat', 'options': SH_MY, 'src': 'shopee'},
   defaultOption=next(i for i, o in enumerate(SH_MY) if o['n'] == 'Beauty › Skincare'),
   store=[('mp', 'mp'), ('mall', 'mall')],
   periods=[('new', 'period_shopee_my_new'), ('old', 'period_shopee_my_old')],
   toggles=[dict(id='scp', vals=['non', 'scp']), dict(id='newSeller', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{period}.{store}.{scp}', zeroIf='newSeller', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=3.78, base='net_ship', color=C[1]),
     dict(id='psf', type='fixed', rate=0.54, color=C[3])],
   compare=dict(vary=['commission'], a={'label': 'cmp_shopee_my_a', 'state': {'period': 'old'}}, b={'label': 'cmp_shopee_my_b', 'state': {'period': 'new'}}, note='cmp_shopee_my_note'),
   sources=[
     ('Fees for Local Shopee Sellers — Shopee MY Seller Education Hub (updated 31 Jul 2026)', 'https://seller.shopee.com.my/edu/article/3503'),
     ('Marketplace Commission Fee table (effective 14 Aug 2026) — Shopee MY Seller Education Hub', 'https://seller.shopee.com.my/edu/article/6799'),
     ('Shopee Mall Commission Fee table (effective 14 Aug 2026) — Shopee MY Seller Education Hub', 'https://seller.shopee.com.my/edu/article/6799')]),
 'shopee-sg': dict(
   platform='shopee', platformName='Shopee', market='SG', marketName='Singapore', slug='shopee/singapore',
   flag='🇸🇬', currency='SGD', symbols={'SGD': 'S$'}, locale='en-SG', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 29.90, 'cost': 10}, selector={'label': 'cat', 'options': SH_SG},
   defaultOption=next(i for i, o in enumerate(SH_SG) if 'Mobile Phones' in o['n']),
   store=[('nonmall', 'mp'), ('mall', 'mall')],
   periods=None,
   toggles=[dict(id='pxp', vals=['', '_pxp']), dict(id='newSeller', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}{pxp}', zeroIf='newSeller', base='net',
          capPerItem='opt:cap_{store}', color=C[0]),
     dict(id='tx', type='pct', rate=3.27, base='net_ship', color=C[1]),
     dict(id='pxp_svc', type='pct', rate=None, when='pxp', base='net', manual=True, color=C[2])],
   compare=None,
   sources=[
     ('About Commission, Service, and Transaction Fees — Shopee SG Seller Education Hub (updated 19 Oct 2026)', 'https://seller.shopee.sg/edu/article/13107'),
     ('Commission fee tables (GST-inclusive, from 28 Aug 2026) — Shopee SG Seller Education Hub', 'https://seller.shopee.sg/edu/article/13107')]),
 'lazada-my': dict(
   platform='lazada', platformName='Lazada', market='MY', marketName='Malaysia', slug='lazada/malaysia',
   flag='🇲🇾', currency='MYR', symbols={'MYR': 'RM'}, locale='en-MY', langs=['en', 'zh'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 49.90, 'cost': 15}, selector={'label': 'cat_lz', 'options': LZ_MY},
   defaultOption=0,
   store=[('mp', 'mp'), ('mall', 'lazmall')],
   periods=None, toggles=[dict(id='newSeller', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}', zeroIf='newSeller', base='net', color=C[0]),
     dict(id='lz_pay', type='pct', rate=None, base='net_ship', manual=True, color=C[1])],
   compare=None,
   sources=[
     ('Marketplace / LazMall Commission Rate (effective 14 Aug 2026, subject to 8% SST) — Lazada Seller Center → Settings → Commission', 'https://sellercenter.lazada.com.my/'),
     ('Lazada Malaysia New Commission Rates for Marketplace & LazMall Sellers (Effective 14 August 2026) — BigSeller reprint of Lazada tables (secondary source)', 'https://www.bigseller.com/blog/articleDetails/4828/lazada-commission-rates-2026.htm')]),
 'walmart-us': dict(
   platform='walmart', platformName='Walmart', market='US', marketName='United States', slug='walmart/united-states',
   flag='🇺🇸', currency='USD', symbols={'USD': '$'}, locale='en-US', langs=['en'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'wt', 'dimwt', 'other'],
   defaults={'price': 24.99, 'cost': 8, 'wt': 1.5}, selector={'label': 'cat_wm', 'options': WM_US},
   defaultOption=idx(WM_US, 'Home, Kitchen, Decor & Garden'),
   store=[('self', 'wm_self'), ('wfs', 'wm_wfs')], periods=None,
   conds={'u10': {'maxUnit': 9.99, 'stores': ['wfs']}},
   selects=[dict(id='nss', label='nss_label', options=WM_NSS, def_='none')],
   toggles=[dict(id='wfsApparel', vals=['', ''], stores=['wfs']), dict(id='wfsHazmat', vals=['', ''], stores=['wfs']),
            dict(id='wfsOversize', vals=['', ''], stores=['wfs']), dict(id='wfsCredit', vals=['', ''], stores=['wfs'])],
   components=[
     dict(id='referral', type='pct', rate='opt:rate', bandsKey='bands', bandBase='net_ship', portion={'key': 'over', 'at': 'at'}, base='net_ship', color=C[0]),
     dict(id='nss', type='pct', rate={'none': 0, 't20': 20, 't30': 30, 't40': 40}, by='nss', whenX=['nss', ['t20', 't30', 't40']], baseRows=['referral'], negative=True, color='#16a34a'),
     dict(id='wfs', type='wt', wt=WFS_STD, whenStore='wfs', color=C[1]),
     dict(id='wfs_app', type='fixed', per='item', rate=0.50, when='wfsApparel', whenStore='wfs', color=C[2]),
     dict(id='wfs_haz', type='fixed', per='item', rate=0.50, when='wfsHazmat', whenStore='wfs', color=C[3]),
     dict(id='wfs_low', type='fixed', per='item', rate=1.00, condOnly='u10', whenStore='wfs', color=C[4]),
     dict(id='wfs_ovr', type='fixed', per='item', rate=3.00, when='wfsOversize', whenStore='wfs', color=C[5]),
     dict(id='wfs_credit', type='pct', rate=10, when='wfsCredit', whenStore='wfs', baseRows=['wfs', 'wfs_app', 'wfs_haz', 'wfs_low', 'wfs_ovr'], negative=True, color='#22c55e')],
   compare=dict(vary=[], a={'label': 'cmp_wm_a', 'state': {'x': {'nss': 'none'}}}, b={'label': 'cmp_wm_b', 'state': {'x': {'nss': 't20'}}}, note='cmp_wm_note'),
   sources=[
     ('Referral fee schedule for contract categories — Walmart Marketplace Learn (updated 9 Mar 2026)', 'https://marketplacelearn.walmart.com/guides/Policies%20&%20standards/Product%20listings/Referral-fee-schedule-for-contract-categories'),
     ('Pricing: referral fees and Walmart Fulfillment Services fees — Walmart Marketplace (checked 27 Oct 2026)', 'https://marketplace.walmart.com/pricing/'),
     ('New-Seller Savings 2026 (20% / 30% / 40% off referral fees, 2 Feb 2026 – 31 Jan 2027) — Walmart Marketplace', 'https://marketplace.walmart.com/new-seller-savings-2026/'),
     ('New Seller Savings — general offer details and terms — Walmart Marketplace', 'https://marketplace.walmart.com/nss-offer-details/'),
     ('WFS fees (fees effective April 2025; long-term storage from 30 Jun 2026) — Walmart Marketplace Learn (updated 27 May 2026)', 'https://marketplacelearn.walmart.com/guides/Walmart%20Fulfillment%20Services%20(WFS)/WFS%20basics/WFS-fees')]),
 'shopee-ph': dict(
   platform='shopee', platformName='Shopee', market='PH', marketName='Philippines', slug='shopee/philippines',
   flag='🇵🇭', currency='PHP', symbols={'PHP': '₱'}, locale='en-PH', langs=['en'], roundFees=0,
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 499, 'cost': 180}, selector={'label': 'cat', 'options': SH_PH, 'src': 'shopee-ph'},
   defaultOption=next(i for i, o in enumerate(SH_PH) if o['g'] == 'Women Clothes'),
   store=[('mp', 'mp'), ('mall', 'mall')], periods=None,
   toggles=[dict(id='newSeller', vals=['', '']), dict(id='opfExempt', vals=['', '']), dict(id='mdv', vals=['', ''])],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}', zeroIf='newSeller', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=2.24, base='net_ship', color=C[1]),
     dict(id='psf_ph', type='pct', rate={'mp': 5.6, 'mall': 4.48}, base='net', capPerItem=100, color=C[2]),
     dict(id='sgsf', type='pct', rate='opt:sgsf', zeroIf='newSeller', base='net', color=C[4]),
     dict(id='opf', type='fixed', rate=5, zeroIf=['newSeller', 'opfExempt'], color=C[3]),
     dict(id='mdv', type='pct', rate=4, when='mdv', base='net', capPerItem=200, color=C[5])],
   compare=None,
   sources=[
     ('Seller Fees — Shopee PH Seller Education Hub (all fees VAT-inclusive; sections updated 13 May 2025 to 22 Oct 2026)', 'https://seller.shopee.ph/edu/article/21077'),
     ('Commission Fee Rates for Shopee Marketplace, VAT-inclusive (effective 1 Jun 2025) — Shopee PH (Google Doc linked from the Seller Fees article)', 'https://docs.google.com/document/d/1zZGKQl9FfykrLhKxLjI8ucAnXBhrzYYp16YcVub5yVw/edit?tab=t.0'),
     ('Commission Fee Rates for Shopee Mall, VAT-inclusive (effective 1 Jan 2025) — Shopee PH (Google Doc linked from the Seller Fees article)', 'https://docs.google.com/document/d/103EMWxNmlnUgQB0rAWUL4c-_STfxB_rCyKGIA4-YVLs/edit?tab=t.0'),
     ('Seller Growth Support Fee by category (updated 22 Oct 2026) — Shopee PH Seller Education Hub', 'https://seller.shopee.ph/edu/article/27461'),
     ('Sample computation of seller net income (fees rounded to the nearest peso) — Shopee PH Seller Education Hub', 'https://seller.shopee.ph/edu/article/27462')]),
 'shopee-th': dict(
   platform='shopee', platformName='Shopee', market='TH', marketName='Thailand', slug='shopee/thailand',
   flag='🇹🇭', currency='THB', symbols={'THB': '฿'}, locale='en-TH', langs=['en'],
   inputs=['price', 'qty', 'sellerDisc', 'cost', 'buyerShip', 'shipCost', 'affPct', 'other'],
   defaults={'price': 299, 'cost': 90}, selector={'label': 'cat', 'options': SH_TH, 'src': 'shopee-th'},
   defaultOption=gidx(SH_TH, 'Beauty', 'Skincare › Facial Serum & Essence'),
   store=[('mp', 'mp_nonmall'), ('mall', 'mall')], periods=None,
   selects=[dict(id='tier', label='th_tier', options=SH_TH_TIER, def_='std')],
   toggles=[],
   components=[
     dict(id='commission', type='pct', rate='opt:{store}.{x:tier}', base='net', color=C[0]),
     dict(id='tx', type='pct', rate=3.21, base='net_ship', color=C[1]),
     dict(id='pif', type='fixed', rate=1.07, color=C[3]),
     dict(id='svc', type='pct', rate=None, base='net', manual=True, color=C[2])],
   compare=None,
   sources=[
     ('นโยบายค่าธรรมเนียม (Fee Policy; new Sale Transaction Fee tables from 4 Aug 2026) — Shopee TH Help Centre', 'https://help.shopee.co.th/portal/4/article/77254'),
     ('Sale Transaction Fee for Non-Mall sellers by category, VAT-inclusive, effective 4 Aug 2026 (English PDF linked from the Fee Policy)', 'https://drive.google.com/file/d/1EiOQVESYZNQ6CMPBejrctqQNNl34ozMH/view'),
     ('Sale Transaction Fee for Mall sellers by category, VAT-inclusive, effective 4 Aug 2026 (English PDF linked from the Fee Policy)', 'https://drive.google.com/file/d/1GcaQ6jv-JcE-diGgZ7hJ-zV-BVBGCQTa/view'),
     ('ค่าธรรมเนียมการทำธุรกรรม (Payment Transaction Fee, 3% + VAT, from 7 Apr 2026) — Shopee TH Seller Education Hub', 'https://seller.shopee.co.th/edu/article/404')]),
}

COMING = [
  ('Lazada', 'Singapore, Philippines & more', '📦'), ('Amazon', 'US, UK & more', '📦'), ('eBay', 'US & UK', '🏷️')]

# ---------- Python mirror of assets/engine.js (used to compute worked examples in the guides)
from decimal import Decimal, ROUND_HALF_UP
def r2(n):
    return float(Decimal(format(n * 100, '.12g')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) / 100

def r4(n):
    return float(Decimal(format(n * 10000, '.12g')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) / 10000

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
    if c.get('whenX') and not in_list(s['x'].get(c['whenX'][0]), c['whenX'][1]): return False
    return in_list(s.get('store'), c.get('whenStore'))

def zeroed(c, s):
    z = c.get('zeroIf') or []
    return any(s['tg'].get(k) for k in ([z] if isinstance(z, str) else z))

def unit_base(c, o):
    b = max(0, o['price'] * o['qty'] - o['sellerDisc']) + (o['buyerShip'] if c.get('bandBase') == 'net_ship' else 0)
    return b / o['qty'] if o['qty'] else 0

def ship_weight(o):
    import math
    if not (o['wt'] > 0) and not (o['dimwt'] > 0): return 0
    return math.ceil(o['wt'] + 0.25 - 1e-9) if 0 < o['wt'] < 1 else math.ceil(max(o['wt'], o['dimwt']) - 1e-9)

def wt_cost(pw, W):
    for mx, base, per, frm in pw:
        if W <= mx: return base + per * max(0, W - frm)
    return None

def rnd(m, n):
    d = m.get('roundFees')
    if d is None: return r2(n)
    f = 10 ** d
    return float(Decimal(format(n * f, '.12g')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) / f

def unit_price(o):
    return max(0, o['price'] * o['qty'] - o['sellerDisc']) / o['qty'] if o['qty'] else 0

def conds(m, s, o):
    out = {}
    for k, c in (m.get('conds') or {}).items():
        out[k] = in_list(s.get('store'), c.get('stores')) and unit_price(o) <= c.get('maxUnit', 1e18) and o['vol'] <= c.get('maxVol', 1e18)
    return out

def def_rate(m, c, s, o):
    if not active(c, s): return None
    cd = conds(m, s, o)
    if c.get('condOnly') and not cd.get(c['condOnly']): return 0
    if zeroed(c, s): return 0
    r = c.get('rate')
    if isinstance(r, str) and r.startswith('opt:'):
        R = m['selector']['options'][s['sel']]['r']; k = key_for(r[4:], m, s); r = R.get(k, R.get('_'))
        if c.get('bandsKey') and R.get(c['bandsKey']):
            u = unit_base(c, o)
            for mx, br in R[c['bandsKey']]:
                if u <= mx + 1e-9: r = br; break
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
    return r4(r)

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
    o = dict(price=0, qty=1, sellerDisc=0, buyerShip=0, shipCost=0, cost=0, other=0, affPct=0, tax=0, taxPct=0, vol=0, coef=100, wt=0, dimwt=0); o.update(inp)
    net = max(0, o['price'] * o['qty'] - o['sellerDisc'])
    b = {'net': net, 'net_ship': net + o['buyerShip'], 'gross': net + o['buyerShip'] + o['tax']}
    rows = []; cd = conds(m, s, o)
    for c in m['components']:
        if not active(c, s): continue
        if c.get('condOnly') and not cd.get(c['condOnly']): continue
        if any(cd.get(k) for k in c.get('condZero', [])): rows.append((c['id'], 0, 0)); continue
        r = def_rate(m, c, s, o)
        if rates and c['id'] in rates: r = rates[c['id']]
        r = r or 0
        if c['type'] == 'wt':
            W = ship_weight(o); pu = wt_cost(c['wt'], W) if W else 0
            amt = (pu or 0) * o['qty']
        elif c['type'] == 'vol':
            amt = vol_cost(c['vol'], o['vol']) * (o[c['vol']['mult']] / 100 if c['vol'].get('mult') else 1) * o['qty']
        elif c['type'] == 'voltab':
            amt = voltab_cost(m, c, s, o)[0] * o['qty']
        elif c['type'] == 'fixed':
            amt = r * (o['qty'] if c.get('per') == 'item' else 1)
        else:
            if c.get('baseRows'): base = sum(x[2] for x in rows if x[0] in c['baseRows'])
            else: base = sum(x[2] for x in rows) if c.get('base') == 'fees' else b[c.get('base', 'net')]
            amt = base * r / 100
            if c.get('portion'):
                R = m['selector']['options'][s['sel']]['r']; ov = R.get(c['portion']['key']); at = R.get(c['portion']['at'])
                if ov is not None and at is not None and o['qty']:
                    uu = base / o['qty']; amt = (min(uu, at) * r / 100 + max(0, uu - at) * ov / 100) * o['qty']
            if c.get('tier'):
                over = m['selector']['options'][s['sel']]['r'].get(c['tier']['key'])
                if over is not None and base > c['tier']['threshold']:
                    amt = c['tier']['threshold'] * r / 100 + (base - c['tier']['threshold']) * over / 100
            cap = c.get('capPerItem')
            if isinstance(cap, str) and cap.startswith('opt:'):
                R = m['selector']['options'][s['sel']]['r']; cap = R.get(key_for(cap[4:], m, s))
            if cap: amt = min(amt, cap * o['qty'])
            if c.get('capPerOrder'): amt = min(amt, c['capPerOrder'])
            if c.get('negative'): amt = -amt
        rows.append((c['id'], r, -rnd(m, -amt) if c.get('negative') else rnd(m, amt)))
    if o['affPct'] > 0: rows.append(('aff', o['affPct'], r2(net * o['affPct'] / 100)))
    total = r2(sum(x[2] for x in rows)); payout = r2(b['net_ship'] - o['shipCost'] - total)
    goods = r2(o['cost'] * o['qty'] + o['other']); tax = r2(net * o['taxPct'] / 100); profit = r2(payout - goods - tax)
    return dict(b=b, rows=rows, fee={k: a for k, _, a in rows}, rate={k: r for k, r, _ in rows}, total=total, payout=payout, profit=profit,
                tax=tax, cond=cd, margin=(profit / net * 100 if net else 0))
