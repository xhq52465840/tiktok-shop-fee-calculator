"""Simplified Chinese calculator pages and guides. Numbers from markets.compute() / rate files only."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

MYO = MARKETS['tiktok-shop-my']['selector']['options']
PHO = MARKETS['tiktok-shop-ph']['selector']['options']
myr = lambda n: next(o for o in MYO if o['n'] == n)['r']
RM = lambda v: money(v, 'MYR'); PHP = lambda v: money(v, 'PHP')
USD = lambda v: money(v, 'USD'); GBP = lambda v: money(v, 'GBP')
SGD = lambda v: money(v, 'SGD'); RUB = lambda v: money(v, 'RUB', lang='zh')

LBL = dict(commission='佣金', tx='交易手续费', bxp='BXP 服务费', psf='平台支持费', ssf='物流服务费',
           opf='订单处理费', growth='卖家成长费', referral='推荐费', aff='达人佣金',
           listing='刊登费', etx='交易手续费', epp='支付处理费', epf='支付处理费（固定）',
           pxp_svc='PXP 服务费', lz_pay='支付/其他费用')

def _ex_rows(f, cur, labels, extra_top=()):
    M = lambda v: money(v, cur)
    rows = list(extra_top)
    for k, r, a in f['rows']:
        if k in ('psf', 'opf', 'listing', 'epf') or (k == 'lz_pay' and a == 0):
            rows.append((labels.get(k, k), '−' + M(a)))
        else:
            rows.append((f"{labels.get(k, k)} ({pct(r)})", '−' + M(a)))
    rows.append(('费用合计', M(f['total']), True))
    rows.append(('结算金额', M(f['payout']), True))
    return rows

# ======================================================================= TikTok MY
def my_zh():
    sk = 'Beauty & Personal Care › Skincare'; r = myr(sk)
    old = compute('tiktok-shop-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('tiktok-shop-my', sel=sk, period='new', price=39.90, cost=12)
    bxp = compute('tiktok-shop-my', sel=sk, period='new', tg={'bxp': True}, price=39.90, cost=12)
    g = compute('tiktok-shop-my', sel='Toys & Hobbies › Musical Instruments & Accessories', price=1000, sellerDisc=100)
    toc = [('how', '马来西亚费用怎么算'), ('examples', '计算示例'), ('changes', '2026 年费率变化'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 马来西亚费用怎么算</h2>
<p>每笔成功签收订单，TikTok Shop 马来西亚会从结算中扣除三项费用；若你加入 Bonus Extra Program（BXP），还有第四项。TikTok 公布的马来西亚费率<strong>已含 8% SST</strong>，无需再加税。</p>
<ul>
<li><b>佣金：</b>按商品子类目、Marketplace / Mall、是否 BXP 卖家计收。佣金 =（商品售价 − 卖家折扣）× 费率。运费与平台出资优惠不计入基数。自 <b>2026年10月31日</b> 起，费率区间约 0%–20.52%。</li>
<li><b>交易手续费：</b>3.78%。自 2026年2月15日起，基数为「原价 − 卖家折扣 + 买家支付运费」。自 2026年10月16日 00:00 起，TikTok PayLater 订单按 <b>4.86%</b> 收取。</li>
<li><b>平台支持费：</b>每笔成功签收订单固定 <b>RM0.54</b>（RM0.50 + SST），与订单金额、件数无关。签收后退货不退还该费用。</li>
<li><b>BXP 服务费（仅 BXP 卖家）：</b>每笔成交订单 4.86%；自 2026年10月7日起，活动日（Double Day、Payday）为 7.02%，每件封顶 RM54。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：RM39.90 护肤精华，Marketplace，非 BXP，成本 RM12</h4>
<p>护肤类目非 BXP Marketplace 佣金由 {pct(r['old.mp.non'])} 调整为 {pct(r['new.mp.non'])}（10月31日起）。</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">10月31日前</th><th class="n">10月31日起</th></tr></thead><tbody>
<tr><td>佣金</td><td class="n">−{RM(old['fee']['commission'])}</td><td class="n">−{RM(new['fee']['commission'])}</td></tr>
<tr><td>交易手续费（3.78%）</td><td class="n">−{RM(old['fee']['tx'])}</td><td class="n">−{RM(new['fee']['tx'])}</td></tr>
<tr><td>平台支持费</td><td class="n">−{RM(old['fee']['psf'])}</td><td class="n">−{RM(new['fee']['psf'])}</td></tr>
<tr><td><b>结算</b></td><td class="n"><b>{RM(old['payout'])}</b></td><td class="n"><b>{RM(new['payout'])}</b></td></tr>
<tr><td><b>扣除成本后利润</b></td><td class="n"><b>{RM(old['profit'])}</b></td><td class="n"><b>{RM(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>新表使该单利润减少 {RM(old['profit'] - new['profit'])}，利润率由 {old['margin']:.1f}% 降至 {new['margin']:.1f}%。</p></div>
<div class="example"><h4>示例 2：同一商品，BXP 卖家</h4>
<p>BXP 新佣金为 {pct(r['new.mp.bxp'])}，但需加收 BXP 服务费。</p>
{ex_table(_ex_rows(bxp, 'MYR', LBL))}
<p>普通日利润 {RM(bxp['profit'])}（{bxp['margin']:.1f}%）。是否加入 BXP，取决于优惠券带来的增量订单是否覆盖服务费——请用计算器上的 BXP 开关自测。</p></div>
<div class="example"><h4>示例 3：TikTok 官方例题</h4>
<p>Seller University 以 RM1,000 吉他、RM100 卖家折扣、非 BXP Marketplace 12.96% 佣金为例。本计算器复现：佣金 {RM(g['fee']['commission'])}，交易手续费 {RM(g['fee']['tx'])}，另加平台支持费 RM0.54（官方例题写作 SST 前的 RM0.50）。</p></div>
<h2 id="changes">2026 年费率变化</h2>
<div class="tablewrap"><table><thead><tr><th>生效日</th><th>变化</th></tr></thead><tbody>
<tr><td>2026年2月15日</td><td>新增平台支持费 RM0.54；交易手续费基数改为售价 − 卖家折扣 + 买家运费。</td></tr>
<tr><td>2026年10月7日</td><td>BXP 活动日费率由 4.86% 升至 7.02%。</td></tr>
<tr><td>2026年10月16日</td><td>TikTok PayLater 订单交易手续费升至 4.86%。</td></tr>
<tr><td>2026年10月31日</td><td>Marketplace / Mall 新佣金表生效；此前下单仍按旧表。</td></tr>
</tbody></table></div>
<p>全部 {len(MYO)} 个子类目对照表见 <a href="../../../en/tiktok-shop/malaysia/">英文版完整页面</a>。</p>
'''
    faq = [
     ('2026 年 TikTok Shop 马来西亚卖家费用有哪些？', '类目佣金、交易手续费 3.78%（PayLater 自 10月16日起 4.86%）、平台支持费 RM0.54。BXP 卖家另付 BXP 服务费 4.86%（活动日 7.02%）。全部含 8% SST。'),
     ('新佣金什么时候开始？', '马来西亚时间 2026年10月31日 00:00。此前下单按旧费率。'),
     ('佣金怎么算？', '佣金 =（商品售价 − 卖家折扣）× 类目费率。运费与平台出资优惠不计入。'),
     ('签收后退货，平台支持费退吗？', '不退。仅整单在发货前取消时才可能退还。'),
     ('这些费率含 SST 吗？', '是。TikTok 公布的佣金、交易手续费、BXP 与平台支持费均已含 8% SST。'),
    ]
    return dict(title='TikTok Shop 马来西亚费用计算器 2026（10月31日新佣金）| SellerFee',
                desc='免费 TikTok Shop 马来西亚费用与利润计算器：10月31日新佣金表、交易手续费 3.78%/4.86%、平台支持费 RM0.54、BXP。',
                h1='TikTok Shop 马来西亚费用计算器',
                lede='按官方佣金表，一眼看出马来西亚每笔订单扣多少、你能留下多少——覆盖 2026年10月31日起的新费率。',
                body=body, faq=faq, toc=toc)

# ======================================================================= TikTok PH
def ph_zh():
    top = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=499, cost=180)
    ph = compute('tiktok-shop-ph', sel='Phones & Electronics › Phones & Tablets', store='mall', price=8000, cost=6900)
    cheap = compute('tiktok-shop-ph', sel='Kitchenware', price=149, cost=60)
    shoes = compute('tiktok-shop-ph', sel='Shoes', store='mall', price=1900, sellerDisc=120)
    toc = [('how', '菲律宾费用怎么算'), ('examples', '计算示例'), ('changes', '2026 年变化'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 菲律宾费用怎么算</h2>
<p>菲律宾站对每笔成功签收订单扣除五项费用。以下费率均为 TikTok 公布的<strong>含税（含 VAT）</strong>数字。</p>
<ul>
<li><b>佣金：</b>基数为售价 − 卖家折扣。自 2025年1月15日起 Marketplace 约 5%–7.3%，Mall 约 5%–9.1%。新卖家前 90 天佣金 0%。</li>
<li><b>交易手续费：</b>2.24%。计算器按「折扣后商品小计 + 买家运费」计（2026年7月起的基数口径）。</li>
<li><b>物流服务费：</b>Marketplace 5.5%、Mall 5%，基数为售价 − 卖家折扣，每件封顶 ₱100。</li>
<li><b>订单处理费：</b>自 2026年9月1日 00:00 起每笔成功签收固定 <b>₱5</b>（此前优惠期为 ₱3）。新卖家及现有卖家每月前 50 单可豁免。</li>
<li><b>卖家成长费：</b>电子/杂货/大家电 1%，美妆、服饰、母婴、健康与生活方式等 1.5%。卖家报表多标注自 2026年4月27日起。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：₱499 女装上衣，Marketplace，成本 ₱180</h4>
{ex_table(_ex_rows(top, 'PHP', LBL))}
<p>平台合计扣 {PHP(top['total'])}，利润 {PHP(top['profit'])}（{top['margin']:.1f}%）。</p></div>
<div class="example"><h4>示例 2：₱8,000 手机，Mall</h4>
<p>物流服务费名义 5%×₱8,000=₱400，但封顶后仅 ₱100。</p>
{ex_table(_ex_rows(ph, 'PHP', LBL))}
<p>高客单价下封顶很关键：有效费率约 {ph['total']/8000*100:.2f}%。</p></div>
<div class="example"><h4>示例 3：₱149 厨具</h4>
{ex_table(_ex_rows(cheap, 'PHP', LBL))}
<p>固定 ₱5 处理费约占售价 {5/149*100:.2f}%，低价单受固定费影响更大。</p></div>
<div class="example"><h4>示例 4：TikTok 官方佣金例题</h4>
<p>灰色鞋子 ₱1,900、卖家折扣 ₱120、Mall 鞋类 7.9%。计算器佣金与官方一致：{PHP(shoes['fee']['commission'])}。</p></div>
<h2 id="changes">2026 年变化</h2>
<div class="tablewrap"><table><thead><tr><th>生效</th><th>变化</th></tr></thead><tbody>
<tr><td>约 2026年4月27日</td><td>引入 1%/1.5% 卖家成长费；符合条件卖家 Bonus Cashback 免费。</td></tr>
<tr><td>2026年9月1日</td><td>订单处理费优惠结束：₱3 → ₱5。</td></tr>
<tr><td>2026年11月1日（据报道）</td><td>卖家成长费公告：菲律宾时间 0 点起对所有卖家的每笔成功订单收取；生活方式类（大家电除外）1.5%，据报道由 1% 上调；电子、杂货、大家电维持 1%。计算器已按此费率计算，与 TikTok 2026年10月13日官方费用总览一致。</td></tr>
<tr><td>未变</td><td>佣金（2025年1月15日表）、交易手续费 2.24%、物流服务费 5.5%/5% 封顶 ₱100。</td></tr>
</tbody></table></div>
'''
    faq = [
     ('2026 年菲律宾卖家费用有哪些？', '类目佣金（Marketplace 5%–7.3%，Mall 5%–9.1%）、交易手续费 2.24%、物流服务费 5.5%/5%（每件封顶 ₱100）、订单处理费 ₱5、卖家成长费 1% 或 1.5%。均为含税。'),
     ('订单处理费是 ₱3 还是 ₱5？', '自 2026年9月1日 00:00 起为 ₱5；2025年12月1日至 2026年8月31日为 ₱3。'),
     ('谁可以不交 ₱5？', '首件商品上架未满 90 天的新卖家次月豁免；现有卖家每月前 50 单豁免。'),
     ('新卖家交佣金吗？', '前 90 天佣金 0%，其他费用仍可能收取。'),
    ]
    return dict(title='TikTok Shop 菲律宾费用计算器 2026（₱5 + 成长费）| SellerFee',
                desc='免费 TikTok Shop 菲律宾费用与利润计算器：₱5 订单处理费、1%–1.5% 卖家成长费、2.24% 交易手续费与物流服务费。',
                h1='TikTok Shop 菲律宾费用计算器',
                lede='把菲律宾站每笔订单的全部扣费算清楚，包括很多计算器仍遗漏的 ₱5 处理费与卖家成长费。',
                body=body, faq=faq, toc=toc)

# ======================================================================= TikTok US
def us_zh():
    tee = compute('tiktok-shop-us', price=24.99, buyerShip=4.99, cost=7, shipCost=4.5)
    aff = compute('tiktok-shop-us', price=24.99, buyerShip=4.99, cost=7, shipCost=4.5, affPct=15)
    card = compute('tiktok-shop-us', sel='Collectibles › Trading Cards & Accessories', price=12000)
    gold = compute('tiktok-shop-us', sel='Jewelry Accessories & Derivatives › Gold', price=450, cost=260)
    toc = [('how', '美国推荐费怎么算'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 美国推荐费怎么算</h2>
<p>美国站主要平台费是<strong>推荐费</strong>。TikTok 公式为：推荐费 = 费率 ×（顾客实付 + 平台优惠 − 税费）。实务上即「折扣后商品价 + 买家支付运费」；平台出资优惠会加回基数，销售税不计入。</p>
<p>绝大多数类目为 <b>6%</b>。五类精品珠宝（钻石、黄金、翡翠、铂金/K 金、红宝石/蓝宝石/祖母绿）及全部 Pre-Owned 子类自 2024年10月31日起为 <b>5%</b>。收藏品与二手在单笔售价超过 $10,000 的部分按 <b>3%</b>。</p>
<p>若走达人带货，你设定的联盟佣金会叠在推荐费之上，往往比平台费还高——请在计算器中填写。</p>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：$24.99 T 恤，买家运费 $4.99</h4>
<p>推荐费基数为 {USD(tee['b']['net_ship'])}。成本 $7，面单 $4.50。</p>
{ex_table(_ex_rows(tee, 'USD', LBL))}
<p>利润 {USD(tee['profit'])}（{tee['margin']:.1f}%）。若达人佣金 15%，利润降至 {USD(aff['profit'])}。</p></div>
<div class="example"><h4>示例 2：$12,000 收藏卡</h4>
<p>前 $10,000 按 6%、超出部分按 3%：合计 {USD(card['total'])}，有效费率约 {card['total']/12000*100:.2f}%。</p></div>
<div class="example"><h4>示例 3：$450 金项链</h4>
<p>黄金子类 5%，推荐费 {USD(gold['total'])}（若按 6% 则为 $27.00）。</p></div>
'''
    faq = [
     ('2026 年美国站推荐费是多少？', '多数类目 6%；五类精品珠宝与全部 Pre-Owned 为 5%。收藏品与二手超过 $10,000 的部分为 3%。'),
     ('运费计入推荐费吗？', '计入买家支付的运费；销售税不计入。'),
     ('平台优惠会降低推荐费吗？', '不会。平台优惠会加回基数。'),
     ('联盟佣金包含在内吗？', '不包含。达人佣金由你设定，请在计算器中单独填写。'),
    ]
    return dict(title='TikTok Shop 美国费用计算器 2026：推荐费与利润 | SellerFee',
                desc='免费 TikTok Shop 美国费用计算器：6% 推荐费（精品珠宝与二手 5%）、运费进基数、$10K 阶梯，以及达人佣金与利润。',
                h1='TikTok Shop 美国费用计算器',
                lede='按官方类目费率，计算美国站推荐费、结算与利润。',
                body=body, faq=faq, toc=toc)

# ======================================================================= TikTok UK
def uk_zh():
    dress = compute('tiktok-shop-uk', price=22, buyerShip=3.49, cost=7, shipCost=3.2)
    elec = compute('tiktok-shop-uk', sel=1, price=60, cost=30)
    toc = [('how', '英国佣金怎么算'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 英国佣金怎么算</h2>
<p>英国站对每笔销售收取佣金。标准费率 <b>9%</b>（含 VAT），减免前。公式大致为：佣金 =（净销售额 + 买家运费 + 平台优惠 − 退款相关项）× 费率。买家运费计入，平台优惠加回，退款相应冲减。</p>
<p>指定电子与美妆个护类目自动获 4 个百分点减免，有效费率 <b>5%</b>。Seller Centre 任务也可能提供减免，但同一商品同一时间只适用一种减免，不可叠加。</p>
<div class="callout warn"><p>哪些子类可享 5%，以政策页链接的「Commission Rate by Product Categories」文档为准。请确认类目正确：审核中若被改类，减免可能失效。</p></div>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：£22 连衣裙，买家运费 £3.49</h4>
{ex_table(_ex_rows(dress, 'GBP', LBL))}
<p>佣金基数 {GBP(dress['b']['net_ship'])}。成本 £7、邮资 £3.20 后，利润 {GBP(dress['profit'])}。</p></div>
<div class="example"><h4>示例 2：£60 符合减免的电子类目</h4>
<p>按 5% 佣金为 {GBP(elec['total'])}（若按 9% 则为 £5.40）。</p></div>
'''
    faq = [
     ('英国站佣金是多少？', '多数类目 9%（含 VAT）；指定电子与美妆个护有效费率为 5%。'),
     ('邮资计入佣金吗？', '计入买家支付的运费。'),
     ('减免可以叠加吗？', '不可以。同一商品同一时间只适用一种减免。'),
     ('退货退佣金吗？', '整单退货退还全部佣金；部分退货仅退对应部分佣金。'),
    ]
    return dict(title='TikTok Shop 英国费用计算器 2026：9% 佣金与利润 | SellerFee',
                desc='免费 TikTok Shop 英国佣金与利润计算器：标准 9%、符合条件电子与美妆 5%，运费进基数，可加达人佣金。',
                h1='TikTok Shop 英国费用计算器',
                lede='按官方佣金政策，估算英国站每单佣金与你能留下多少。',
                body=body, faq=faq, toc=toc)

# ======================================================================= Etsy
def etsy_zh():
    us = compute('etsy', price=30, buyerShip=5, tax=2.4, cost=9, shipCost=4.8)
    uk = compute('etsy', sel='United Kingdom', price=25, buyerShip=4, cost=8, shipCost=3.6, rates={'listing': 0})
    toc = [('how', 'Etsy 费用怎么算'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">Etsy 费用怎么算</h2>
<p>多数 Etsy 成交包含三项费用：</p>
<ul>
<li><b>交易手续费：</b>售价与运费合计的 <b>6.5%</b>（部分市场另有当地税费口径，以帮助中心为准）。</li>
<li><b>刊登费：</b>每售出一件通常 <b>US$0.20</b>（按美元计，非美元账户需在「所用费率」中换算）。</li>
<li><b>支付处理费：</b>依收款银行所在国家而定，一般为百分比 + 固定金额；基数常含销售税。</li>
</ul>
<p>请在计算器顶部选择银行账户所在国家，以加载对应处理费率。</p>
<div class="callout"><p><b>英国卖家？</b>英国店铺还要付 0.48% 监管运营费；未填写 VAT 号时，Etsy 费用另加 20% VAT。<a href="/zh/etsy/uk/">Etsy 英国费用计算器</a> 已全部计入（以英镑计算）。</p></div>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：美国账户，$30 商品 + $5 运费 + $2.40 税</h4>
{ex_table(_ex_rows(us, 'USD', LBL))}
<p>成本 $9、面单 $4.80 后，利润 {USD(us['profit'])}。</p></div>
<div class="example"><h4>示例 2：英国账户，£25 + £4 运费</h4>
{ex_table(_ex_rows(uk, 'GBP', LBL))}
<p>刊登费若已用美元另付，可在费率区将刊登费设为 0（本例如此）。</p></div>
'''
    faq = [
     ('Etsy 交易手续费是多少？', '一般为商品价与运费合计的 6.5%。'),
     ('刊登费怎么收？', '通常每售出一件 US$0.20；按美元计。'),
     ('支付处理费含税吗？', '通常按含税总额计。可在计算器中填写销售税。'),
    ]
    return dict(title='Etsy 费用计算器 2026：6.5% 交易费与支付处理费 | SellerFee',
                desc='免费 Etsy 费用与利润计算器：6.5% 交易手续费、US$0.20 刊登费，以及 60+ 国家的支付处理费。',
                h1='Etsy 费用计算器',
                lede='按官方费率估算 Etsy 每单扣费、结算与利润，覆盖主要收款国家的支付处理费。',
                body=body, faq=faq, toc=toc)

# ======================================================================= Russia
def _ru_ex(mid, labels, **kw):
    f = compute(mid, **kw)
    rows = [(labels['net'], RUB(f['b']['net']))]
    for k, r, a in f['rows']:
        if a == 0 and k == 'acq': continue
        lab = labels[k]
        how = f' ({pct(r)})' if r and k in ('oz_comm', 'wb_comm', 'ym_place', 'ym_deliv', 'ym_transfer', 'oz_heavy', 'acq') else ''
        if k in ('oz_mile', 'oz_proc', 'ym_proc', 'ym_accept') and r:
            how = f' ({RUB(r)})'
        rows.append((lab + how, '−' + RUB(a)))
    rows.append((labels['fees'], RUB(f['total']), True))
    rows.append((labels['payout'], RUB(f['payout']), True))
    if kw.get('cost'):
        rows.append((labels['cost'], '−' + RUB(kw['cost'] * kw.get('qty', 1))))
        rows.append((labels['profit'], RUB(f['profit']), True))
    return f, ex_table(rows)

def ozon_zh():
    L = dict(net='商品小计', oz_comm='Ozon 佣金', oz_log='物流（FBO/FBS）', oz_mile='末端配送', oz_proc='FBS 处理',
             oz_heavy='非标件', acq='收单', fees='费用合计', payout='结算', cost='商品成本', profit='利润')
    fbo, t_fbo = _ru_ex('ozon', L, price=1500, cost=450, vol=1.5)
    fbs, t_fbs = _ru_ex('ozon', L, store='fbs', price=1500, cost=450, vol=1.5)
    toc = [('models', 'FBO / FBS / realFBS'), ('commission', '按价位的佣金'), ('example', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<p class="callout"><b>核实日期 2026年10月26日。</b>类目佣金取自 Ozon 自 <b>2026年8月28日</b> 起生效的 XLSX；FBO/FBS 物流取自 <b>2026年10月30日</b> 起的 XLSX。规则见「Полный список комиссий и тарифов」（2026年10月7日版）。</p>
<h2 id="models">FBO、FBS 与 realFBS</h2>
<ul>
<li><b>FBO</b> — 货在 Ozon 仓，平台拣货打包配送。佣金 + 物流 + 末端 25 ₽/件。</li>
<li><b>FBS</b> — 你发到 Ozon 取货点/分拣中心。佣金档与 FBO 相同，另加物流、末端与处理费（常见 10 ₽）。</li>
<li><b>realFBS</b> — 你自行配送。通常只收该类目 &gt;300 ₽ 档佣金，无 Ozon 物流。</li>
</ul>
<h2 id="commission">按价位的佣金</h2>
<p>FBO / FBS 多数品类公布三档：单价 ≤100 ₽ 为 <b>17%</b>，101–300 ₽ 为 <b>23%</b>，&gt;300 ₽ 为类目特定费率。realFBS 通常用单一费率（多与 &gt;300 ₽ 档相同）。</p>
<h2 id="example">示例 — 化妆品 1 500 ₽，1.5 升，莫斯科 → 莫斯科</h2>
<p>默认类目「Красота и гигиена › Косметика для ухода」（&gt;300 ₽ 为 52%）。物流取 10月30日表中莫斯科线路；末端 25 ₽。</p>
<h3>FBO</h3>
{t_fbo}
<p>费用 {RUB(fbo['total'])} · 结算 {RUB(fbo['payout'])} · 利润 {RUB(fbo['profit'])}（{fbo['margin']:.1f}%）。</p>
<h3>FBS（同款）</h3>
{t_fbs}
<p>FBS 另加 10 ₽ 处理费；两集群均为莫斯科时物流与末端与 FBO 相同。</p>
<div class="callout warn"><b>本计算器未建模：</b>非本地 FBO 加价、FBO Fresh、部分仓优惠、退货与超期仓储等。请以 Seller Edu 为准。</div>
'''
    faq = [
     ('Ozon FBO 和 FBS 佣金一样吗？', '价位档一致；FBS 另加处理费，物流与末端仍按线路与体积计。'),
     ('realFBS 交物流费吗？', '通常不交 Ozon 物流，只交佣金（多为该类目高价档）。'),
     ('收单费率是多少？', '由银行设定，Ozon 不公布统一百分比；请在计算器中自行填写。'),
    ]
    return dict(title='Ozon 费用计算器 2026（FBO / FBS / realFBS）| SellerFee',
                desc='免费 Ozon 俄罗斯费用计算器：按类目与价位的佣金、2026年10月30日 FBO/FBS 物流表、末端与处理费，输出卢布结算与利润。',
                h1='Ozon 费用计算器（俄罗斯）',
                lede='按官方类目与价位佣金、10月30日物流表，计算每单扣费、结算与利润（卢布）。',
                body=body, faq=faq, toc=toc)

def wb_zh():
    L = dict(net='商品小计', wb_comm='佣金（КВВ）', wb_log='配送至买家', fees='费用合计', payout='结算', cost='商品成本', profit='利润', acq='收单')
    fbw, t_fbw = _ru_ex('wildberries', L, price=1500, cost=450, vol=1.5, coef=170)
    fbs, t_fbs = _ru_ex('wildberries', L, store='fbs', price=1500, cost=450, vol=1.5, coef=170)
    toc = [('how', 'КВВ 与物流'), ('example', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<p class="callout"><b>核实日期 2026年10月26日。</b>КВВ 取自 Wildberries 自 <b>2026年7月7日</b> 起的 PDF；物流说明页更新于 <b>2026年10月19日</b>。基础物流 46+14 ₽/升 × 仓库系数，自 2026年8月15日起俄罗斯仓系数多为 170%。</p>
<h2 id="how">佣金（КВВ）与物流</h2>
<ul>
<li><b>КВВ</b> — 按「предмет」与履约模式（FBW / FBS / DBS）公布百分比。</li>
<li><b>物流</b> — 常见口径为 46 ₽ + 14 ₽/升，再乘仓库系数（俄罗斯仓 170%，超大件 100%）。</li>
<li><b>FBS 加速</b> — 13 小时内交接可降 КВВ 约 5 个百分点；13–42 小时约降 3.5 个百分点（以官方说明为准）。</li>
</ul>
<h2 id="example">示例 — 1 500 ₽，1.5 升，系数 170%</h2>
<h3>FBW</h3>
{t_fbw}
<p>费用 {RUB(fbw['total'])} · 利润 {RUB(fbw['profit'])}（{fbw['margin']:.1f}%）。</p>
<h3>FBS</h3>
{t_fbs}
'''
    faq = [
     ('仓库系数 170% 是什么？', '自 2026年8月15日起，俄罗斯境内多数 WB 仓配送系数为 170%；超大件常为 100%。请在卖家中心「费率」核对你的仓。'),
     ('DBS 还交物流吗？', 'DBS 为自配送，通常只交 КВВ，不按仓配物流公式计。'),
    ]
    return dict(title='Wildberries 费用计算器 2026（FBW / FBS / DBS）| SellerFee',
                desc='免费 Wildberries 费用计算器：按品类的 КВВ、体积物流与仓库系数，输出卢布结算与利润。',
                h1='Wildberries 费用计算器',
                lede='按官方 КВВ 与物流说明，计算 FBW / FBS / DBS 下的扣费、结算与利润。',
                body=body, faq=faq, toc=toc)

def ym_zh():
    L = dict(net='商品小计', ym_place='展示费', ym_deliv='配送', ym_mid='中段运费', ym_proc='FBS 处理',
             ym_transfer='货款划转', ym_accept='收款', fees='费用合计', payout='结算', cost='商品成本', profit='利润', acq='收单')
    n, t_n = _ru_ex('yandex-market', L, price=1500, cost=450, vol=1.5)
    cheap, t_c = _ru_ex('yandex-market', L, price=250, cost=80, vol=0.5)
    toc = [('how', '展示费与低价 42%'), ('example', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<p class="callout"><b>核实日期 2026年10月26日。</b>展示费、FBY/FBS 与支付相关费率取自 Yandex Market 帮助中心当时公布内容。至 2026 年底，符合条件的低价商品可适用 <b>42%</b> 综合费率。</p>
<h2 id="how">展示费与 42% 低价费率</h2>
<ul>
<li><b>展示费</b> — 按类目百分比。</li>
<li><b>配送 / 中段</b> — 常见配送约 5%，另有中段等项（随模式变化）。</li>
<li><b>42% 低价费率</b> — 售价 ≤300 ₽ 且体积 ≤5 升时，可用 42% 替代展示、配送与中段等组合（以官方条件为准，有效期至 2026 年底）。</li>
<li><b>货款划转 / 收款</b> — 与结算周期选项相关（如每周延迟 4 周约 1.6% 等）。</li>
</ul>
<h2 id="example">计算示例</h2>
<h3>普通价 1 500 ₽，1.5 升</h3>
{t_n}
<p>费用 {RUB(n['total'])} · 利润 {RUB(n['profit'])}。</p>
<h3>低价 250 ₽，0.5 升（可能触发 42%）</h3>
{t_c}
'''
    faq = [
     ('42% 什么时候适用？', '通常要求售价 ≤300 ₽ 且体积 ≤5 升，并满足官方对 FBY/FBS 等模式的条件；有效期至 2026 年底。'),
     ('结算周期影响什么？', '影响货款划转等支付相关费率；选项越短通常费率越高。'),
    ]
    return dict(title='Yandex Market 费用计算器 2026（FBY / FBS / DBS）| SellerFee',
                desc='免费 Yandex Market 费用计算器：类目展示费、42% 低价费率、配送与支付相关费用，输出卢布结算与利润。',
                h1='Yandex Market 费用计算器',
                lede='按官方展示费与低价规则，估算每单扣费、结算与利润。',
                body=body, faq=faq, toc=toc)

# ======================================================================= Shopee / Lazada
def shopee_my_zh():
    sk = 'Beauty › Skincare'
    r = next(o for o in MARKETS['shopee-my']['selector']['options'] if o['n'] == sk)['r']
    old = compute('shopee-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('shopee-my', sel=sk, period='new', price=39.90, cost=12)
    scp = compute('shopee-my', sel=sk, period='new', tg={'scp': True}, price=39.90, cost=12)
    toc = [('how', 'Shopee 马来西亚费用'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">Shopee 马来西亚费用怎么算</h2>
<p>本地成交订单通常扣除：类目佣金、交易手续费、平台支持费。佣金取决于类目、Marketplace / Mall、是否加入返现计划（SCP）。我们加载的佣金百分比为<strong>含 SST</strong>（官方表 × 1.08），与 Shopee 例题把 9.0% 写成 9.72% 的口径一致。</p>
<ul>
<li><b>佣金</b> =（售价 − 卖家折扣）× 类目费率。平台出资券不减基数。自 <b>2026年8月14日</b> 起 Marketplace / Mall 表再次更新。</li>
<li><b>交易手续费</b>：买家实付金额（含运费）的 <b>3.78%</b>（含 SST），四舍五入到分。</li>
<li><b>平台支持费</b>：每笔成交 <b>RM0.54</b>（含 SST）。</li>
<li><b>新卖家</b>：自 2026年8月1日起，Marketplace 佣金在「首件上架满 120 天」或「成交超 200 单」较早者之后才开始收取。可用「新卖家」开关模拟。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例：RM39.90 护肤，Marketplace，非 SCP</h4>
<p>8月14日后护肤非 SCP Marketplace 佣金为 {pct(r['new.mp.non'])}（含 SST）。</p>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">8月14日前</th><th class="n">8月14日起</th></tr></thead><tbody>
<tr><td>佣金</td><td class="n">−{RM(old['fee']['commission'])}</td><td class="n">−{RM(new['fee']['commission'])}</td></tr>
<tr><td>交易手续费（3.78%）</td><td class="n">−{RM(old['fee']['tx'])}</td><td class="n">−{RM(new['fee']['tx'])}</td></tr>
<tr><td>平台支持费</td><td class="n">−{RM(old['fee']['psf'])}</td><td class="n">−{RM(new['fee']['psf'])}</td></tr>
<tr><td><b>结算</b></td><td class="n"><b>{RM(old['payout'])}</b></td><td class="n"><b>{RM(new['payout'])}</b></td></tr>
<tr><td><b>利润</b></td><td class="n"><b>{RM(old['profit'])}</b></td><td class="n"><b>{RM(new['profit'])}</b></td></tr>
</tbody></table></div></div>
<div class="example"><h4>同一商品，SCP 卖家</h4>
<p>SCP 使新佣金降至 {pct(r['new.mp.scp'])}。</p>
{ex_table(_ex_rows(scp, 'MYR', LBL))}
<p>利润 {RM(scp['profit'])}，对比非 SCP 的 {RM(new['profit'])}。</p></div>
'''
    faq = [
     ('Shopee 马来西亚交易手续费是多少？', '含 SST 后为 3.78%，按买家实付（含运费）计。'),
     ('平台支持费是多少？', '每笔成交 RM0.54（含 SST）。'),
     ('SCP 是什么？', '返现计划卖家可走更低佣金列；请以卖家中心资格为准。'),
    ]
    return dict(title='Shopee 马来西亚费用计算器 2026（佣金 / 3.78% / RM0.54）| SellerFee',
                desc='免费 Shopee 马来西亚费用计算器：2026年8月14日佣金表（含 SST）、交易手续费 3.78%、平台支持费 RM0.54。',
                h1='Shopee 马来西亚费用计算器',
                lede='按 8月14日官方佣金表，算出 Marketplace / Mall、SCP / 非 SCP 下每单扣费与利润。',
                body=body, faq=faq, toc=toc)

def shopee_sg_zh():
    new = compute('shopee-sg', price=29.90, cost=10)
    toc = [('how', 'Shopee 新加坡费用'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">Shopee 新加坡费用怎么算</h2>
<p>新加坡站佣金表自 <b>2026年8月28日</b> 起更新，费率为<strong>含 GST</strong>。另收交易手续费约 <b>3.27%</b>（含 GST），PXP 卖家可能另有优惠佣金与独立服务费及封顶规则。</p>
<ul>
<li><b>佣金</b> — Mall / 非 Mall、类目不同；PXP 可走优惠列。</li>
<li><b>交易手续费</b> — 约 3.27%（含 GST）。</li>
<li><b>PXP</b> — 优惠佣金 + 可能的 PXP 服务费（请按卖家中心类目费率填写）。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例：S$29.90，成本 S$10</h4>
{ex_table(_ex_rows(new, 'SGD', LBL))}
<p>结算 {SGD(new['payout'])}，利润 {SGD(new['profit'])}（{new['margin']:.1f}%）。</p></div>
'''
    faq = [
     ('新加坡佣金含 GST 吗？', '是，我们加载的为含 GST 费率，与官方例题口径一致。'),
     ('交易手续费是多少？', '约 3.27%（含 GST），请以卖家中心为准。'),
    ]
    return dict(title='Shopee 新加坡费用计算器 2026（含 GST 佣金与 3.27% 交易费）| SellerFee',
                desc='免费 Shopee 新加坡费用计算器：2026年8月28日起含 GST 的 Mall/非 Mall 佣金、约 3.27% 交易手续费与 PXP。',
                h1='Shopee 新加坡费用计算器',
                lede='按含 GST 的官方佣金与交易手续费，估算每单结算与利润。',
                body=body, faq=faq, toc=toc)

def lazada_my_zh():
    new = compute('lazada-my', price=39.90, cost=12)
    toc = [('how', 'Lazada 马来西亚费用'), ('examples', '计算示例'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">Lazada 马来西亚费用怎么算</h2>
<p>自 <b>2026年8月14日</b> 起，Marketplace 与 LazMall 按商品集群公布佣金区间（含 SST 的下限口径）。实际订单可能还有支付或活动相关费用——请按费用账单在计算器中补填。</p>
<ul>
<li><b>佣金</b> — 按集群与 Marketplace / LazMall；我们加载区间下限（含 SST），可在「所用费率」改成你后台精确值。</li>
<li><b>支付/其他</b> — 可选手动填写百分比。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例：RM39.90，成本 RM12</h4>
{ex_table(_ex_rows(new, 'MYR', LBL))}
<p>结算 {RM(new['payout'])}，利润 {RM(new['profit'])}。请用你卖家中心的精确佣金百分比核对。</p></div>
'''
    faq = [
     ('为什么佣金是区间？', '官方按集群公布范围；计算器默认用含 SST 的下限，并允许你改成账单上的精确值。'),
     ('还有哪些费用？', '可能含支付、活动等；请对照费用账单填写「支付/其他」。'),
    ]
    return dict(title='Lazada 马来西亚费用计算器 2026（8月14日佣金）| SellerFee',
                desc='免费 Lazada 马来西亚费用计算器：2026年8月14日起 Marketplace 与 LazMall 集群佣金（含 SST），可编辑为后台精确费率。',
                h1='Lazada 马来西亚费用计算器',
                lede='按 8月14日集群佣金表估算每单扣费与利润，并可改成你卖家中心的精确百分比。',
                body=body, faq=faq, toc=toc)

# ======================================================================= Guides (zh)
def g_my_zh():
    sk = 'Beauty & Personal Care › Skincare'; r = myr(sk)
    old = compute('tiktok-shop-my', sel=sk, period='old', price=39.90, cost=12)
    new = compute('tiktok-shop-my', sel=sk, period='new', price=39.90, cost=12)
    return f'''
<h2 id="what">10月31日改什么</h2>
<p>TikTok Shop 马来西亚自 <b>2026年10月31日 00:00</b>（马来西亚时间）起启用新的 Marketplace / Mall 佣金表。交易手续费、平台支持费与 BXP 服务费规则不变，但 PayLater 交易费率已于 10月16日调整为 4.86%，BXP 活动日费率已于 10月7日调整为 7.02%。</p>
<p>护肤类目非 BXP Marketplace 佣金由 {pct(r['old.mp.non'])} 变为 {pct(r['new.mp.non'])}。以 RM39.90、成本 RM12 为例，利润从 {RM(old['profit'])} 降到 {RM(new['profit'])}。</p>
<p>请用 <a href="../../tiktok-shop/malaysia/">马来西亚费用计算器</a> 切换「费率适用期」做新旧对照，并查看完整类目表。</p>
<h2 id="action">卖家可以做什么</h2>
<ul>
<li>对涨幅大的类目重新核价，或做组合装摊薄固定的 RM0.54 平台支持费。</li>
<li>用计算器测 BXP：服务费是否能被优惠券带来的增量订单覆盖。</li>
<li>定价时预留部分订单走 PayLater 4.86% 交易手续费。</li>
</ul>
'''

def g_ph_zh():
    top = compute('tiktok-shop-ph', sel='Womenswear & Underwear', price=499, cost=180)
    return f'''
<h2 id="what">卖家成长费是什么</h2>
<p>菲律宾站的卖家成长费按成功订单收取：电子、杂货、大家电 <b>1%</b>；美妆、服饰、母婴、健康与生活方式等 <b>1.5%</b>。它与 ₱5 订单处理费、2.24% 交易手续费、物流服务费叠加。</p>
<p>以 ₱499 女装为例（Marketplace），成长费约 1.5%，本计算器费用合计 {PHP(top['total'])}，利润 {PHP(top['profit'])}。</p>
<p>打开 <a href="../../tiktok-shop/philippines/">菲律宾费用计算器</a>，切换类目即可看到成长费列。</p>
<h2 id="nov-2026">2026年11月1日费用上调</h2>
<p>据 AMZ123 2026年10月27日报道，TikTok Shop 菲律宾站发布费用调整公告：自 2026年11月1日 00:00（菲律宾时间）起，对所有卖家的每笔成功订单收取卖家成长费。报道称生活方式类（大家电除外）由 1% 上调至 1.5%；电子、杂货、大家电维持 1%；美妆个护、服饰、母婴、健康维持 1.5%。以上费率均含增值税。</p>
<p>我们没能打开公告原文，因此生效日期按“据报道”处理。新费率与 TikTok 2026年10月13日官方费用总览一致，计算器已按此计算。家居、厨具、宠物等生活方式类卖家，请在 11.11 前按多出的 0.5% 重新核算价格。</p>
<h2 id="tips">注意</h2>
<ul>
<li>部分类目未出现在官方成长费名单时，我们按 1.5% 估算并注明——请以结算单为准。</li>
<li>每月前 50 单可豁免 ₱5 处理费；新卖家另有豁免窗口。</li>
</ul>
<p>Shopee 菲律宾也收类似的卖家成长支持费，TikTok Shop 泰国则收高得多的商业增长费。详见 <a href="../seller-growth-fee-tiktok-shopee-lazada/">TikTok Shop、Shopee、Lazada 成长费对比</a>。</p>
'''

def g_price_zh():
    return '''
<h2 id="formula">目标利润率怎么定售价</h2>
<p>一个实用近似：先估出「有效费率」（佣金 + 交易费 + 固定费折算），再留出成本与目标利润。</p>
<p>售价 ≈（单件成本 + 每单固定费分摊）÷（1 − 有效费率 − 目标利润率）。</p>
<p>固定费（如马来西亚 RM0.54、菲律宾 ₱5）在低客单上占比很高——要么提高客单，要么用组合装摊薄。</p>
<p>用各国计算器中的「达到 30% 利润率的售价」提示，或自行调整售价看利润率变化。</p>
<h2 id="check">核对结算</h2>
<p>定价后对照卖家中心结算明细：佣金基数是否含运费、是否有 PayLater / BXP / 成长费等开关项。发现不一致，欢迎在 GitHub 反馈。</p>
'''

GUIDES_ZH = [
 dict(lang='zh', slug='tiktok-shop-malaysia-commission-changes-october-2026', short='马来西亚佣金调整（10月31日）',
      title='TikTok Shop 马来西亚 2026年10月31日佣金调整解读',
      desc='马来西亚佣金表 10月31日怎么变：哪些类目涨跌、BXP 与非 BXP、令吉示例与调价思路。',
      market='tiktok-shop-my', cov='cov-ink', fig='10月31日', body=g_my_zh,
      sources=MARKETS['tiktok-shop-my']['sources']),
 dict(lang='zh', slug='tiktok-shop-philippines-seller-growth-fee', short='菲律宾卖家成长费',
      title='TikTok Shop 菲律宾卖家成长费：2026年11月1日费用上调、费率与实例',
      desc='PH 卖家成长费 11月1日起对所有卖家收取：1% / 1.5% 怎么收，如何与 ₱5 处理费叠加，真实订单成本多少。',
      market='tiktok-shop-ph', cov='cov-amber', fig='1–1.5%', body=g_ph_zh,
      sources=MARKETS['tiktok-shop-ph']['sources']),
 dict(lang='zh', slug='tiktok-shop-pricing-target-margin', short='按目标利润率定价',
      title='如何在 TikTok Shop 定价以达到目标利润率',
      desc='扣除佣金、交易费与固定费用后仍能达到目标利润率的简单定价思路，附 MY / PH / US 思路。',
      market=None, cov='cov-green', fig='30%', body=g_price_zh,
      sources=MARKETS['tiktok-shop-my']['sources'][:2] + MARKETS['tiktok-shop-ph']['sources'][:2]),
]

PAGE_FN_ZH = {
 ('tiktok-shop-my', 'zh'): my_zh,
 ('tiktok-shop-ph', 'zh'): ph_zh,
 ('tiktok-shop-us', 'zh'): us_zh,
 ('tiktok-shop-uk', 'zh'): uk_zh,
 ('etsy', 'zh'): etsy_zh,
 ('ozon', 'zh'): ozon_zh,
 ('wildberries', 'zh'): wb_zh,
 ('yandex-market', 'zh'): ym_zh,
 ('shopee-my', 'zh'): shopee_my_zh,
 ('shopee-sg', 'zh'): shopee_sg_zh,
 ('lazada-my', 'zh'): lazada_my_zh,
}
