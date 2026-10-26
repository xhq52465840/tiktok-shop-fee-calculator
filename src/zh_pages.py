"""Chinese locale home and hub pages for the static build."""
from markets import MARKETS, COMING, compute
from sf_site import page, crumbs, badge, esc, ic, ptile, issue_url, VDATE
from site_helpers import money
import content as C

# Summaries (kept here so build.py C_SUM_ZH can stay optional)
C_SUM_ZH = {
 'tiktok-shop-my': '2026年10月31日起新佣金表，交易手续费 3.78%/4.86%，平台支持费 RM0.54，BXP。',
 'tiktok-shop-ph': '₱5 订单处理费，1%–1.5% 卖家成长费，交易手续费 2.24%，物流服务费。',
 'tiktok-shop-us': '按类目推荐费 6%，精品珠宝与二手 5%，超 $10K 部分 3%。',
 'tiktok-shop-uk': '佣金 9%，指定电子与美妆类目 5%。',
 'etsy': '交易手续费 6.5%、刊登费 US$0.20，以及 60+ 国家支付处理费。',
 'ozon': 'FBO/FBS/realFBS 按类目与价位佣金，物流自 2026年10月30日，末端 25 ₽。',
 'wildberries': '按品类 КВВ（FBW/FBS/DBS），物流 46+14 ₽/升 × 仓库系数。',
 'yandex-market': '按类目展示费、42% 低价费率、配送 5%、中段与货款划转。',
 'shopee-my': 'Marketplace / Mall 佣金自 2026年8月14日（含 SST），交易手续费 3.78%，平台支持费 RM0.54。',
 'shopee-sg': '含 GST 的 Mall/非 Mall 佣金自 2026年8月28日，交易手续费 3.27%，PXP 与封顶。',
 'lazada-my': 'Marketplace 与 LazMall 集群佣金自 2026年8月14日（含 SST 下限）。',
}

def _w(path, html):
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, path, 'index.html') if path.endswith('/') or path == '' else os.path.join(root, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(html)

def gcard(path, g, lang):
    from sf_site import rel as rel_
    from i18n import tr
    cov = g.get('cov', 'cov-ink'); fig = g.get('fig', '')
    href = f'{g.get("lang","en")}/guides/{g["slug"]}/'
    words = 700
    return f'''<a class="card gcard" href="{rel_(path)}{href}">
<div class="cov {cov}"><div class="fig">{esc(fig)}</div><div class="cap">{esc(g["short"])}</div></div>
<div class="body"><span class="badge b-brand sm">{esc(tr(lang,"guide"))}</span>
<h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p>
<div class="gmeta"><span>{ic("clock",13)}{max(3, round(words/220))} {esc(tr(lang,"min_read"))}</span><span>{ic("cal",13)}{VDATE[lang]}</span></div></div></a>'''

def home_zh():
    path = 'zh/'
    tabs = [('tiktok-shop/malaysia/', 'tiktok-shop', 'TikTok MY'),
            ('ozon/', 'ozon', 'Ozon'),
            ('wildberries/', 'wildberries', 'Wildberries'),
            ('shopee/malaysia/', 'shopee', 'Shopee MY'),
            ('etsy/', 'etsy', 'Etsy')]
    qc_tabs = ''.join(
        f'<a class="{"on" if i==0 else ""}" href="{u}">{ptile(p,18)}{esc(n)}</a>'
        for i, (u, p, n) in enumerate(tabs))
    pv = compute('tiktok-shop-my', sel='Beauty & Personal Care › Skincare', period='new', price=39.90, cost=12)
    RM = lambda v: money(v, 'MYR')
    qc = (
        f'<div class="card qc"><div class="qc-tabs">{qc_tabs}</div>'
        f'<div class="body"><div class="eyebrow">示例 · TikTok Shop 马来西亚 · 2026年10月31日起</div>'
        f'<div class="chips"><a class="chip on" href="tiktok-shop/malaysia/">护肤</a>'
        f'<a class="chip" href="tiktok-shop/malaysia/">Marketplace</a>'
        f'<a class="chip" href="tiktok-shop/malaysia/">RM 39.90</a>'
        f'<a class="chip" href="tiktok-shop/malaysia/">打开 →</a></div></div>'
        f'<div class="qres"><div class="row"><div><span class="small muted">预估利润</span>'
        f'<div class="v h-display pos">{RM(pv["profit"])}</div>'
        f'<span class="small muted">{pv["margin"]:.1f}% 利润率 · 费用 {RM(pv["total"])}</span></div>'
        f'<a class="btn btn-brand" href="tiktok-shop/malaysia/">打开计算器 {ic("arrow",15)}</a></div></div></div>'
    )

    def prow(mid):
        m = MARKETS[mid]
        note = '10月31日新费率' if mid == 'tiktok-shop-my' else f'已核实 {VDATE["zh"]}'
        nb = (f'<span class="badge b-new" style="height:22px;font-size:12px">{note}</span>'
              if mid == 'tiktok-shop-my' else f'<span class="r">{note}</span>')
        label = m['marketName'] if m['market'] != 'GLOBAL' else '全球'
        return (f'<a class="mrow" href="{m["slug"]}/"><span class="flag" style="font-size:18px">{m["flag"]}</span>'
                f'<span class="nm">{esc(label)}</span>{nb}{badge("已上线","live")}</a>')

    tt = ''.join(prow(k) for k in MARKETS if MARKETS[k]['platform'] == 'tiktok-shop')
    for plat, mk, f in COMING:
        if plat == 'TikTok Shop':
            tt += (f'<div class="mrow off"><span class="flag" style="font-size:18px">{f}</span>'
                   f'<span class="nm">{esc(mk)}</span>{badge("即将上线","soon")}</div>')
    ru = ''.join(
        f'<a class="mrow" href="{MARKETS[k]["slug"]}/"><span class="flag" style="font-size:18px">{MARKETS[k]["flag"]}</span>'
        f'<span class="nm">{esc(MARKETS[k]["platformName"])}</span><span class="r">已核实 {VDATE["zh"]}</span>'
        f'{badge("已上线","live")}</a>'
        for k in ('ozon', 'wildberries', 'yandex-market'))

    live_map = {
        'etsy': [('etsy', 'Etsy')],
        'shopee': [('shopee-my', 'Shopee 马来西亚'), ('shopee-sg', 'Shopee 新加坡')],
        'lazada': [('lazada-my', 'Lazada 马来西亚')],
    }
    ohtml = ''
    for pairs in live_map.values():
        for mid, title in pairs:
            m = MARKETS[mid]
            ohtml += (
                f'<a class="card ccard" href="{m["slug"]}/"><div class="top">{ptile(m["platform"],40)}{badge("已上线","live")}</div>'
                f'<h3>{esc(title)}</h3><p>{esc(C_SUM_ZH[mid])}</p>'
                f'<div class="go">打开计算器 {ic("arrow",14)}</div></a>'
            )
    for name in ('amazon', 'ebay'):
        req = issue_url(f'Calculator request: {name.title()}', f'Please add a fee calculator for {name.title()}.')
        ohtml += (
            f'<a class="card ccard" href="{req}" rel="noopener"><div class="top">{ptile(name,40)}{badge("即将上线","soon")}</div>'
            f'<h3>{name.title()}</h3><p>核实官方费率后上线。</p>'
            f'<div class="go soon">{ic("bell",14)} 申请此计算器</div></a>'
        )

    guides = [g for g in C.GUIDES if g.get('lang') == 'zh'][:6]
    body = f'''<section class="hero"><div class="wrap">
<div><div class="announce">{badge("新","new")}<span>Shopee 马来/新加坡 + Lazada 马来已上线 · <a href="shopee/malaysia/">打开 Shopee {ic("arrow",13)}</a></span></div>
<h1 class="h-display">看清每个平台从你这一单拿走多少。</h1>
<p class="lead">SellerFee 把官方费率表变成可即时计算的工具。选平台、填售价，立刻看到每项费用、结算金额与真实利润率。</p>
<div class="ctas"><a class="btn btn-primary btn-lg" href="tiktok-shop/malaysia/">{ic("calc",16)} TikTok Shop 马来西亚</a>
<a class="btn btn-secondary btn-lg" href="russia/">俄罗斯平台</a></div>
<div class="checks"><span>{ic("check",15)} 仅用官方来源</span><span>{ic("check",15)} 已核实 {VDATE["zh"]}</span><span>{ic("check",15)} 免费，无需注册</span></div></div>
{qc}</div></section>
<div class="stats"><div class="wrap" style="display:contents">
<div><b>11</b><span>已上线计算器</span></div>
<div><b>3</b><span>俄罗斯平台</span></div>
<div><b>16k+</b><span>已加载类目费率</span></div>
<div><b>0</b><span>虚构数字</span></div>
</div></div>
<section class="s" id="calculators"><div class="wrap">
<div class="sh"><div><p class="eyebrow">计算器</p><h2 class="h2">平台与市场</h2></div>
<a class="btn btn-link" href="../en/rate-changes/">费率变动 {ic("arrow",14)}</a></div>
<div class="pgrid">
<div class="card pcard"><div class="ph">{ptile("tiktok-shop",40)}<div><b>TikTok Shop</b><div class="small muted">4 个已上线市场</div></div></div>{tt}
<a class="mrow" href="tiktok-shop/" style="border-top:1px solid var(--line);margin-top:4px"><span class="nm" style="color:var(--brand-600)">全部 TikTok Shop 市场</span>{ic("arrow",14)}</a></div>
<div class="card pcard"><div class="ph">{ptile("ozon",40)}<div><b>俄罗斯</b><div class="small muted">Ozon · WB · Yandex</div></div></div>{ru}
<a class="mrow" href="russia/" style="border-top:1px solid var(--line);margin-top:4px"><span class="nm" style="color:var(--brand-600)">俄罗斯专区</span>{ic("arrow",14)}</a></div>
<div class="stackcol">{ohtml}</div>
</div></div></section>
<section class="s trust"><div class="wrap"><div class="tgrid">
<div><p class="eyebrow">可信</p><h2 class="h2">数字经得起核对</h2>
<div class="step"><span class="n">1</span><div><b>只用官方来源</b><p>每条费率来自平台自己的卖家帮助中心。核实不了，就不发布计算器。</p></div></div>
<div class="step"><span class="n">2</span><div><b>标注核实日期</b><p>每页写明最近核实时间。费率变更时新旧对照并列。</p></div></div>
<div class="step"><span class="n">3</span><div><b>费用算全</b><p>交易费、处理费、物流、封顶与分档——并且任意费率都可按你的账户改。</p></div></div></div>
<div class="card reg"><div class="hd"><b>来源登记</b><span class="small muted">核实于 {VDATE["zh"]}</span></div>
<p class="muted" style="padding:16px">完整来源列表见各计算器页底部，或浏览 <a href="../en/">英文首页</a> 的来源登记表。</p></div>
</div></div></section>
<section class="s"><div class="wrap"><div class="sh"><div><p class="eyebrow">指南</p><h2 class="h2">最新指南</h2></div>
<a class="btn btn-link" href="guides/">全部指南 {ic("arrow",14)}</a></div>
<div class="cards">{''.join(gcard(path, g, 'zh') for g in guides)}</div>
<div class="cta"><div><h2 class="h-display">还缺你需要的市场？</h2>
<p>在 GitHub 开 issue，写明平台与官方费率页。我们核实数字后才会发布。</p></div>
<div class="btns"><a class="btn btn-secondary btn-lg" href="{issue_url("Calculator request: ", "Platform:\nMarket:\nLink to official rates:")}" rel="noopener">{ic("bell",16)} 申请计算器</a>
<a class="btn btn-brand btn-lg" href="../en/about/">我们如何核实费率</a></div></div>
</div></section>'''
    _w(path, page(path, 'zh', 'SellerFee：TikTok Shop、Shopee、Lazada 等费用与利润计算器',
                  '面向跨境卖家的免费费用与利润计算器：TikTok Shop、Shopee、Lazada、Ozon、Wildberries、Yandex Market、Etsy。官方费率，标注核实日期。',
                  body, alt={'en': 'en/', 'ms': 'ms/', 'ru': 'ru/', 'zh': 'zh/'}))

def tiktok_hub_zh():
    path = 'zh/tiktok-shop/'
    ch, cld = crumbs(path, [('SellerFee', 'zh/'), ('TikTok Shop', None)])
    names = {'Malaysia': '马来西亚', 'Philippines': '菲律宾', 'United States': '美国', 'United Kingdom': '英国'}
    cards = ''.join(
        f'<a class="card ccard" href="{m["slug"].split("/")[1]}/">'
        f'<div class="top"><span class="flag" style="font-size:28px">{m["flag"]}</span>{badge("已上线","live")}</div>'
        f'<h3>TikTok Shop {names.get(m["marketName"], m["marketName"])}</h3>'
        f'<p>{esc(C_SUM_ZH[k])}</p><div class="go">打开计算器 {ic("arrow",14)}</div></a>'
        for k, m in MARKETS.items() if m['platform'] == 'tiktok-shop')
    body = f'''<div class="phead"><div class="wrap">{ch}
<h1 class="h-display" style="margin-top:18px">按国家划分的 TikTok Shop 费用计算器</h1>
<p class="lead" style="margin-top:12px">每个市场费用结构不同：东南亚按类目佣金，美国是推荐费，英国是统一佣金。</p></div></div>
<section class="s"><div class="wrap"><div class="cards">{cards}</div></div></section>'''
    _w(path, page(path, 'zh', 'TikTok Shop 费用计算器：马来西亚、菲律宾、美国与英国 | SellerFee',
                  '免费 TikTok Shop 卖家费用计算器，覆盖马来西亚、菲律宾、美国与英国，基于官方 Seller University 费率。',
                  body, [cld], alt={'en': 'en/tiktok-shop/', 'zh': 'zh/tiktok-shop/'}))

def russia_hub_zh():
    path = 'zh/russia/'
    ch, cld = crumbs(path, [('SellerFee', 'zh/'), ('俄罗斯', None)])
    cards = ''.join(
        f'<a class="card ccard" href="../{MARKETS[k]["slug"]}/">'
        f'<div class="top">{ptile(k,40)}{badge("已上线","live")}</div>'
        f'<h3>{esc(MARKETS[k]["platformName"])}</h3><p>{esc(C_SUM_ZH[k])}</p>'
        f'<div class="go">打开计算器 {ic("arrow",14)}</div></a>'
        for k in ('ozon', 'wildberries', 'yandex-market'))
    body = f'''<div class="phead"><div class="wrap">{ch}
<h1 class="h-display" style="margin-top:18px">俄罗斯电商平台费用计算器</h1>
<p class="lead" style="margin-top:12px">Ozon、Wildberries、Yandex Market — FBO/FBS 类模式、类目佣金、物流与支付费用，全部按官方文件以卢布计算。</p>
<p class="muted" style="margin-top:8px">另有 <a href="../../ru/">Русский</a> 与 <a href="../../en/russia/">English</a>。</p></div></div>
<section class="s"><div class="wrap"><div class="cards">{cards}</div></div></section>'''
    _w(path, page(path, 'zh', '俄罗斯费用计算器：Ozon、Wildberries 与 Yandex Market | SellerFee',
                  '面向 Ozon、Wildberries、Yandex Market 卖家的免费费用与利润计算器。官方类目费率、物流与支付费用（卢布）。',
                  body, [cld], alt={'en': 'en/russia/', 'ru': 'ru/', 'zh': 'zh/russia/'}))
