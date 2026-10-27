"""Simplified Chinese pages and guides for TikTok Shop Singapore & Thailand and Etsy UK. Numbers from markets.compute() / rate files only."""
from markets import MARKETS, compute, USD_GBP
from site_helpers import money, pct, ex_table
from content_new import sg_stats, th_stats, LIST_GBP, CAP_GBP

SGD = lambda v: money(v, 'SGD'); THB = lambda v: money(v, 'THB'); GBP = lambda v: money(v, 'GBP')
FIXED = ('pif', 'listing', 'epf')
LBL = dict(commission='佣金', tx='交易手续费', bxp='BXP 服务费', cgf='商业增长费', pif='平台基础设施费', aff='达人佣金',
           listing='刊登费（US$0.20 换算）', etx='交易手续费', epp='支付处理费', epf='支付处理费（固定）',
           rof='监管运营费', offads='站外广告费', feevat='Etsy 费用的 VAT')

def ex_rows(f, cur, extra_top=()):
    M = lambda v: money(v, cur)
    rows = list(extra_top)
    for k, r, a in f['rows']:
        rows.append((LBL[k] if k in FIXED else f"{LBL[k]}（{pct(r)}）", '−' + M(a)))
    rows.append(('费用合计', M(f['total']), True))
    rows.append(('结算金额', M(f['payout']), True))
    return rows

# ------------------------------------------------------------------ 新加坡
def sg_zh():
    st = sg_stats()
    new = compute('tiktok-shop-sg', price=29.90, cost=9); old = compute('tiktok-shop-sg', period='old', price=29.90, cost=9)
    bxp = compute('tiktok-shop-sg', tg={'bxp': True}, price=29.90, cost=9)
    pn = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', price=499, cost=380)
    po = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', period='old', price=499, cost=380)
    e1 = compute('tiktok-shop-sg', tg={'bxp': True}, price=160, sellerDisc=20, buyerShip=2)
    e2 = compute('tiktok-shop-sg', tg={'bxp': True}, price=600, sellerDisc=10, buyerShip=2)
    toc = [('how', 'TikTok Shop 新加坡费用怎么算'), ('examples', '计算示例'), ('changes', '9月1日改了什么'), ('limits', '计算器的假设'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 新加坡费用怎么算</h2>
<p>官方「卖家费用介绍」列出两项卖家费用：<b>平台佣金</b>与<b>交易手续费</b>；参加 Bonus Extra Program（BXP）的卖家另收 <b>BXP 服务费</b>。新加坡站公布的费率均<b>已含 9% GST</b>。</p>
<ul>
<li><b>平台佣金：</b>自 2026年9月1日 00:00（GMT+8）起，官方费率表所有类目统一为<b>标准 9.810%</b>、<b>BXP 7.085%</b>。「<span lang="en">EL, Toys &amp; Collectibles</span>」行业（电子、家电、电脑、玩具、收藏品、券类等，共 {st['cap_new']} 个三级类目）设 <b>S$30 封顶</b>，其余不封顶。基数 =（商品价 − 卖家折扣）× 费率，不含运费和平台补贴。</li>
<li><b>交易手续费：</b>自 2025年10月1日起为 <b>3.27%</b>（此前 2.18%）。自 2026年4月1日起按「买家实付（含运费）+ 平台折扣 − 退款」计。退货按比例退还。</li>
<li><b>BXP 服务费：</b>每笔完成订单都收（无论是否用券）：指定电子、母婴、家电二级类目 <b>3.27%</b>，其余 <b>5.45%</b>；基数为（商品净价 − 卖家折扣），<b>每件封顶 S$30</b>。双数日与 Payday 大促期间 +1.09 个百分点（4.36% / 6.54%）。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：S$29.90 精华，非 BXP，9月1日前后对比（成本 S$9）</h4>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">7月27日–8月31日</th><th class="n">9月1日起</th></tr></thead><tbody>
<tr><td>佣金</td><td class="n">{pct(old['rate']['commission'])} = −{SGD(old['fee']['commission'])}</td><td class="n">{pct(new['rate']['commission'])} = −{SGD(new['fee']['commission'])}</td></tr>
<tr><td>交易手续费（3.27%）</td><td class="n">−{SGD(old['fee']['tx'])}</td><td class="n">−{SGD(new['fee']['tx'])}</td></tr>
<tr><td><b>利润</b></td><td class="n"><b>{SGD(old['profit'])}</b></td><td class="n"><b>{SGD(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>新表每单少赚 {SGD(old['profit'] - new['profit'])}。</p></div>
<div class="example"><h4>示例 2：同一商品，BXP 卖家</h4>
{ex_table(ex_rows(bxp, 'SGD'))}
<p>利润 {SGD(bxp['profit'])}，低于非 BXP 的 {SGD(new['profit'])}——BXP 只有在优惠券带来增量订单时才划算。</p></div>
<div class="example"><h4>示例 3：S$499 手机——新的 S$30 封顶</h4>
<p>旧表 {pct(po['rate']['commission'])}（封顶 S$50）佣金 {SGD(po['fee']['commission'])}；新表 9.81% 本应 {SGD(499 * 0.0981)}，封顶后为 <b>{SGD(pn['fee']['commission'])}</b>。利润由 {SGD(po['profit'])} 升至 {SGD(pn['profit'])}——高客单电子产品反而更便宜。</p></div>
<div class="example"><h4>示例 4：官方 BXP 例题</h4>
<p>S$160、卖家折扣 S$20：BXP 服务费 <b>{SGD(e1['fee']['bxp'])}</b>（(160 − 20) × 5.45%）；S$600、折扣 S$10：本应 {SGD(590 * 0.0545)}，封顶为 <b>{SGD(e2['fee']['bxp'])}</b>。与官方结果一致。</p></div>
<h2 id="changes">9月1日改了什么</h2>
<div class="tablewrap"><table><thead><tr><th></th><th>2026年7月27日–8月31日</th><th>2026年9月1日起</th></tr></thead><tbody>
<tr><td>标准佣金</td><td>多数 8.175%；{st['old_non'].get(6.54, 0)} 个电子与家电类目 6.54%</td><td>全部 9.810%</td></tr>
<tr><td>BXP 佣金</td><td>7.085%；上述类目 5.45%</td><td>全部 7.085%</td></tr>
<tr><td>封顶</td><td>{st['cap_old']} 个类目 S$50</td><td>{st['cap_new']} 个类目 S$30</td></tr>
</tbody></table></div>
<p>详细解读见 <a href="/zh/guides/tiktok-shop-singapore-commission-september-2026/">9月1日佣金调整指南</a>；完整 {st['n']:,} 个类目费率表见 <a href="/en/tiktok-shop/singapore/#rates">英文版页面</a>。</p>
<h2 id="limits">计算器的假设</h2>
<ul>
<li><b>本地卖家费率。</b>跨境卖家走全球卖家（<span lang="en">Global Seller</span>）体系，其 2026年9月3日公告示例中的费率不同，请以全球卖家中心为准。</li>
<li><b>Mall 与 Marketplace。</b>官方页面称两者费率可能不同，但 9月1日 PDF 只公布一套费率；若你的 Mall 合同不同，请修改佣金费率。</li>
<li><b>S$30 按件封顶。</b>官方写作「<span lang="en">fee upper cap</span>」，我们按每件计（与 BXP 封顶表述一致）。</li>
<li><b>不能参加 BXP 的商品</b>（虚拟商品、婴儿配方奶粉、黄金）按标准费率收取，请关闭 BXP 开关。</li>
<li>未计入 1.09% 预售服务费，如适用请填入「其他成本」。</li>
</ul>
'''
    faq = [
     ('TikTok Shop 新加坡 2026 年收哪些费用？', '2026年9月1日起平台佣金 9.810%（BXP 7.085%），电子、玩具与收藏品类目每件封顶 S$30；交易手续费 3.27%；BXP 卖家另收 3.27% 或 5.45% 的服务费（每件封顶 S$30）。均含 9% GST。'),
     ('佣金所有类目都一样吗？', '9月1日起官方表中所有类目都是标准 9.810%、BXP 7.085%；区别只在电子、玩具与收藏品行业（官方行业名 EL, Toys & Collectibles）有 S$30 封顶。'),
     ('交易手续费怎么算？', '按买家实付（含运费）加平台折扣、减去退款计算，费率 3.27%，退货按比例退还。'),
     ('BXP 服务费什么时候变高？', '双数日与 Payday 大促期间 +1.09 个百分点：3.27% → 4.36%，5.45% → 6.54%。'),
     ('跨境卖家能用这个计算器吗？', '本计算器用的是本地卖家费率表。跨境卖家请以全球卖家中心为准，并在「所用费率」中修改。'),
    ]
    return dict(title='TikTok Shop 新加坡费用计算器 2026（9月1日起佣金 9.81%）| SellerFee',
                desc='免费 TikTok Shop 新加坡费用与利润计算器：2026年9月1日起佣金 9.81% / BXP 7.085%、电子类 S$30 封顶、3.27% 交易手续费与 BXP 服务费，均含 GST。',
                h1='TikTok Shop 新加坡费用计算器',
                lede='按 2026年9月1日起的官方含 GST 佣金表，算出 TikTok Shop 新加坡每单扣费、结算与利润。',
                body=body, faq=faq, toc=toc)

# ------------------------------------------------------------------ 泰国
def th_zh():
    st = th_stats()
    new = compute('tiktok-shop-th', price=299, cost=90); old = compute('tiktok-shop-th', period='old', price=299, cost=90)
    mall = compute('tiktok-shop-th', store='mall', price=299, cost=90); combo = compute('tiktok-shop-th', store='mall', tg={'combo': True}, price=299, cost=90)
    g1 = compute('tiktok-shop-th', price=1000, sellerDisc=100)
    hm = compute('tiktok-shop-th', sel='Audio & Video › Headphones, Earphones & Accessories', store='mall', price=2000, cost=1100)
    cap = compute('tiktok-shop-th', price=3000, cost=1500)
    toc = [('how', 'TikTok Shop 泰国费用怎么算'), ('examples', '计算示例'), ('changes', '2026 年的变化'), ('limits', '计算器的假设'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">TikTok Shop 泰国费用怎么算</h2>
<p>泰国站每笔已送达订单要扣<b>四项</b>平台费用，官方费率均<b>已含税</b>（VAT）。</p>
<ul>
<li><b>平台佣金：</b>按三级类目，Marketplace（非 Mall）与 Mall 各一张表。2026年7月5日 00:00（GMT+7）起，多数 Marketplace 类目 <b>10.70%</b>、多数 Mall 类目 <b>13.91%</b>，全表区间 5.35%–13.91%。参加 <b>Mall Combo Package</b>（同时参加 Mall Live Specials 与 Brands Crazy Deals）的 Mall 卖家走更低的 Combo 列，通常 10.70%。基数 =（商品价 − 卖家折扣）。近 30 天 GMV Max 花费超过营收 3% 的非 Mall 卖家，佣金降 1.07 个百分点（自 2026年4月1日）。</li>
<li><b>交易手续费：</b><b>3.21%</b>，自 2026年3月21日起按「买家实付 + 平台折扣」计（含买家运费），送达后退货不退还。</li>
<li><b>商业增长费（CGF）：</b>自 2026年5月6日起，Electronics 行业（{st['el']} 个类目）<b>6.96%</b>、其他 <b>8.03%</b>，基数（商品价 − 卖家折扣），<b>每件封顶 ฿199</b>。近 30 天 GMV 低于 ฿10,000 的非 Mall 卖家为 6.42% / 7.49%；新卖家前 30 天免收（7月16日后入驻上限 ฿1,000）；只用自有车队配送的卖家不收。不退还。</li>
<li><b>平台基础设施费：</b>每笔送达订单 <b>฿1.07</b>（自 2025年10月1日），不退还；前 30 天（截至每月 20 日）订单 1–100 单的卖家次月豁免。</li>
</ul>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：฿299 精华，Marketplace，7月5日前后（成本 ฿90）</h4>
<div class="tablewrap"><table><thead><tr><th></th><th class="n">5月6日–7月4日</th><th class="n">7月5日起</th></tr></thead><tbody>
<tr><td>佣金</td><td class="n">{pct(old['rate']['commission'])} = −{THB(old['fee']['commission'])}</td><td class="n">{pct(new['rate']['commission'])} = −{THB(new['fee']['commission'])}</td></tr>
<tr><td>交易手续费（3.21%）</td><td class="n">−{THB(old['fee']['tx'])}</td><td class="n">−{THB(new['fee']['tx'])}</td></tr>
<tr><td>商业增长费（8.03%）</td><td class="n">−{THB(old['fee']['cgf'])}</td><td class="n">−{THB(new['fee']['cgf'])}</td></tr>
<tr><td>平台基础设施费</td><td class="n">−{THB(old['fee']['pif'])}</td><td class="n">−{THB(new['fee']['pif'])}</td></tr>
<tr><td><b>利润</b></td><td class="n"><b>{THB(old['profit'])}</b></td><td class="n"><b>{THB(new['profit'])}</b></td></tr>
</tbody></table></div>
<p>费用合计 {THB(new['total'])}，占售价 {new['total'] / 299 * 100:.1f}%。</p></div>
<div class="example"><h4>示例 2：同一商品，Mall 卖家</h4>
<p>标准 Mall 佣金 {pct(mall['rate']['commission'])}：费用 {THB(mall['total'])}，利润 {THB(mall['profit'])}。加入 Mall Combo 后佣金 {pct(combo['rate']['commission'])}：费用 {THB(combo['total'])}，利润 {THB(combo['profit'])}。</p></div>
<div class="example"><h4>示例 3：官方例题</h4>
<p>฿1,000、卖家折扣 ฿100，Marketplace 10.70%：佣金 <b>{THB(g1['fee']['commission'])}</b>、交易手续费 <b>{THB(g1['fee']['tx'])}</b>、商业增长费 <b>{THB(g1['fee']['cgf'])}</b>。฿2,000 耳机（Mall）：佣金 <b>{THB(hm['fee']['commission'])}</b>（11.77%）、商业增长费 <b>{THB(hm['fee']['cgf'])}</b>（6.96%）。均与官方一致。</p></div>
<div class="example"><h4>示例 4：฿199 封顶</h4>
<p>฿3,000 非电子商品按 8.03% 本应 {THB(3000 * 0.0803)}，封顶后为 <b>{THB(cap['fee']['cgf'])}</b>。</p></div>
<h2 id="changes">2026 年的变化</h2>
<div class="tablewrap"><table><thead><tr><th>生效</th><th>变化</th></tr></thead><tbody>
<tr><td>2026年3月21日</td><td>交易手续费基数改为买家实付 + 平台折扣（3.21%）。</td></tr>
<tr><td>2026年4月1日</td><td>GMV Max 花费超营收 3% 的非 Mall 卖家佣金 −1.07 个百分点。</td></tr>
<tr><td>2026年5月6日</td><td>新佣金表；商业增长费由 5.89% / 6.96% 升至 6.96% / 8.03%，每件封顶 ฿199。</td></tr>
<tr><td>2026年7月5日</td><td>新 Marketplace 与 Mall 佣金表：多数 Marketplace 类目 8.56% → 10.70%，多数 Mall 类目 11.77% → 13.91%。</td></tr>
</tbody></table></div>
<p>详细解读见 <a href="/zh/guides/tiktok-shop-thailand-seller-fees-2026/">泰国卖家费用指南</a>；完整 {st['n']:,} 个类目费率表见 <a href="/en/tiktok-shop/thailand/#rates">英文版页面</a>。</p>
<h2 id="limits">计算器的假设</h2>
<ul>
<li>本地卖家费率；跨境卖家以全球卖家中心为准。</li>
<li>Mall Live Specials 与 Brands Crazy Deals 可能另有费用；Combo 开关只改变佣金。</li>
<li>对比列使用 2026年5月6日费率表；未加载 5月6日的 Mall Combo 列。</li>
<li>未计入 2.14% 预售服务费，如适用请填入「其他成本」。</li>
</ul>
'''
    faq = [
     ('TikTok Shop 泰国 2026 年收哪些费用？', '按类目的佣金（7月5日起多数 Marketplace 10.70%、Mall 13.91%）、3.21% 交易手续费、商业增长费 6.96%（电子）/ 8.03%（每件封顶 ฿199），以及每单 ฿1.07 平台基础设施费。均含税。'),
     ('新佣金什么时候开始？', '2026年7月5日 00:00（泰国时间 GMT+7），Marketplace 与 Mall 同时生效。'),
     ('商业增长费是什么？', '按（商品价 − 卖家折扣）收取：电子行业 6.96%，其他 8.03%，每件封顶 ฿199；新卖家前 30 天免收，只用自有车队配送的卖家不收。'),
     ('退货会退哪些费用？', '退货商品的佣金会退；送达后交易手续费、商业增长费和平台基础设施费不退。'),
    ]
    return dict(title='TikTok Shop 泰国费用计算器 2026（佣金、商业增长费与 ฿1.07）| SellerFee',
                desc='免费 TikTok Shop 泰国费用与利润计算器：2026年7月5日起 Marketplace / Mall 佣金、3.21% 交易手续费、6.96%/8.03% 商业增长费（封顶 ฿199）与 ฿1.07 平台基础设施费。',
                h1='TikTok Shop 泰国费用计算器',
                lede='按 2026年7月5日起的官方费率表，一次算清佣金、交易手续费、商业增长费与 ฿1.07 基础设施费。',
                body=body, faq=faq, toc=toc)

# ------------------------------------------------------------------ Etsy 英国
def etsy_uk_zh():
    a = compute('etsy-uk', price=25, buyerShip=4, cost=8, shipCost=3.6)
    v = compute('etsy-uk', sel=1, price=25, buyerShip=4, cost=8, shipCost=3.6, taxPct=16.67)
    o = compute('etsy-uk', tg={'offsite': True}, price=25, buyerShip=4, cost=8, shipCost=3.6)
    toc = [('how', '英国卖家的 Etsy 费用'), ('vat', 'Etsy 费用的 VAT'), ('examples', '计算示例'), ('limits', '计算器的假设'), ('faq', '常见问题'), ('sources', '官方来源')]
    body = f'''
<h2 id="how">英国卖家的 Etsy 费用</h2>
<p>英国店铺、通过 Etsy Payments 收款到英国银行账户，一笔普通订单要付：</p>
<ul>
<li><b>刊登费：</b>每个刊登 US$0.20，多件售出或售出后自动续期时每件再收一次。Etsy 按美元收取，计算器按 2026年10月26日欧洲央行参考汇率（1 USD = {USD_GBP} GBP）换算为 <b>{GBP(LIST_GBP)}</b>，可在「所用费率」中修改。</li>
<li><b>交易手续费：</b>订单总额（商品价 + 你收取的运费与礼品包装）的 <b>6.5%</b>。</li>
<li><b>支付处理费：</b>英国银行账户 <b>4% + £0.20</b> 每单，按含运费及 Etsy 代收税费的总额计。</li>
<li><b>监管运营费（<span lang="en">Regulatory Operating Fee</span>）：</b>自 <b>2026年6月22日</b>起为订单总额的 <b>0.48%</b>（此前 0.32%）。</li>
<li><b>站外广告费</b>（仅来自 Offsite Ads 的订单）：订单总额 15%；店铺任一 365 天销售额达 US$10,000 后为 12%；每单最高 US$100（约 {GBP(CAP_GBP)}）。</li>
</ul>
<h2 id="vat">Etsy 费用的 VAT</h2>
<p>英国属于 Etsy 对卖家费用收取 VAT 的国家：如果你<b>没有</b>在 Etsy 填写 VAT 号，Etsy 会对卖家费用（以及按规定对支付处理费）加收 VAT；填写有效 VAT 号后不再收取，月度发票会注明未收 VAT。计算器按英国标准税率 <b>20%</b> 计入（顶部「你在 Etsy 的 VAT 状态」第一项），第二项为 0%。</p>
<p>若你已注册 VAT，你的销售本身也要缴 VAT：在「你需缴纳的销售 VAT」填 16.67，即可扣除含税价中的 VAT。</p>
<h2 id="examples">计算示例</h2>
<div class="example"><h4>示例 1：£25 商品 + £4 运费，未注册 VAT（成本 £8，面单 £3.60）</h4>
{ex_table(ex_rows(a, 'GBP'))}
<p>到手 {GBP(a['payout'])}，利润 <b>{GBP(a['profit'])}</b>。</p></div>
<div class="example"><h4>示例 2：同一订单，已注册 VAT 并在 Etsy 填写 VAT 号</h4>
<p>费用不再含 VAT，降至 {GBP(v['total'])}；但 £25 售价中含 {GBP(v['tax'])} 的销项 VAT，利润为 <b>{GBP(v['profit'])}</b>。</p></div>
<div class="example"><h4>示例 3：同一订单来自站外广告</h4>
<p>15% 站外广告费 {GBP(o['fee']['offads'])} 也要加 VAT，费用合计 {GBP(o['total'])}，利润 {GBP(o['profit'])}。</p></div>
<h2 id="limits">计算器的假设</h2>
<ul>
<li>英国店铺、英国银行账户、以英镑刊登；以其他币种刊登另收 2.5% 货币转换费。</li>
<li>美元金额（刊登费、站外广告封顶）按 2026年10月26日欧洲央行参考汇率换算，Etsy 实际按当日汇率。</li>
<li>VAT 按英国标准税率 20%（Etsy 原文为「适用的 VAT」）。</li>
</ul>
<p>其他国家的卖家请用 <a href="/zh/etsy/">Etsy 全球费用计算器</a>。</p>
'''
    faq = [
     ('英国卖家 2026 年的 Etsy 费用有哪些？', f'刊登费 US$0.20（约 {GBP(LIST_GBP)}）、6.5% 交易手续费（含运费与礼品包装）、4% + £0.20 支付处理费、自 2026年6月22日起 0.48% 监管运营费；未填写 VAT 号时，这些费用另加 20% VAT。站外广告订单另收 15% 或 12%，每单最高 US$100。'),
     ('英国的监管运营费是多少？', '自 2026年6月22日起为订单总额（商品、运费、礼品包装与个性化）的 0.48%，此前为 0.32%。'),
     ('Etsy 会对英国卖家的费用收 VAT 吗？', '会，除非你在 Etsy 账户中填写有效的 VAT 号。'),
     ('刊登费换成英镑是多少？', f'Etsy 按 US$0.20 收取，英镑金额随汇率变化；按 2026年10月26日欧洲央行汇率约为 {GBP(LIST_GBP)}。'),
    ]
    return dict(title='Etsy 英国费用计算器 2026：0.48% 监管运营费与费用 VAT | SellerFee',
                desc='免费 Etsy 英国费用与利润计算器：6.5% 交易手续费、4% + £0.20 支付处理费、2026年6月22日起 0.48% 监管运营费、Etsy 费用的 VAT 与站外广告费，以英镑计算。',
                h1='Etsy 英国费用计算器',
                lede='一次算清 Etsy 从英国订单中收取的全部费用——刊登、交易、支付处理、0.48% 监管运营费与费用 VAT——以及你到手多少。',
                body=body, faq=faq, toc=toc)

# ------------------------------------------------------------------ 指南
def g_sg_zh():
    st = sg_stats()
    new = compute('tiktok-shop-sg', price=29.90, cost=9); old = compute('tiktok-shop-sg', period='old', price=29.90, cost=9)
    pn = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', price=499, cost=380); po = compute('tiktok-shop-sg', sel='Phones & Tablets › Mobile Phones', period='old', price=499, cost=380)
    return f'''
<p>TikTok Shop 新加坡自 <b>2026年9月1日</b>起把分类目佣金表改成统一费率：标准 <b>9.810%</b>、BXP <b>7.085%</b>（含 GST），电子、玩具与收藏品类目每件封顶 <b>S$30</b>。下面用 <a href="/zh/tiktok-shop/singapore/">新加坡费用计算器</a> 看谁多付、谁少付。</p>
<h2 id="what">改了什么</h2>
<ul>
<li>{st['moved'].get((8.175, 9.81), 0):,} 个类目标准佣金由 8.175% 升到 9.81%（+1.635 个百分点）；BXP 仍为 7.085%。</li>
<li>{st['moved'].get((6.54, 9.81), 0)} 个原 6.54% 的电子与家电类目升到 9.81%，但多数改为 S$30 封顶。</li>
<li>封顶：旧表 {st['cap_old']} 个类目 S$50 → 新表 {st['cap_new']} 个类目 S$30。交易手续费 3.27% 与 BXP 服务费不变。</li>
</ul>
<h2 id="impact">对真实订单的影响</h2>
<p>S$29.90 精华（成本 S$9）：佣金 {SGD(old['fee']['commission'])} → {SGD(new['fee']['commission'])}，利润 {SGD(old['profit'])} → {SGD(new['profit'])}。S$499 手机：佣金 {SGD(po['fee']['commission'])} → {SGD(pn['fee']['commission'])}（封顶），利润 {SGD(po['profit'])} → {SGD(pn['profit'])}。按 9.81% 计，售价约 {SGD(30 / 0.0981)} 以上就触顶。</p>
<h2 id="action">卖家可以做什么</h2>
<ul>
<li>美妆、服饰、食品等低客单商品承担了全部涨幅，优先复核定价。</li>
<li>BXP 少 2.725 个百分点佣金，但多付 3.27% / 5.45% 服务费，按单看几乎总是更贵，要靠优惠券带来增量。</li>
<li>跨境卖家的费率与本地不同，请以全球卖家中心为准。</li>
</ul>
'''

def g_th_zh():
    new = compute('tiktok-shop-th', price=299, cost=90); old = compute('tiktok-shop-th', period='old', price=299, cost=90)
    return f'''
<p>TikTok Shop 泰国现在每单扣四项费用，其中两项在 2026 年年中调整。下面用 <a href="/zh/tiktok-shop/thailand/">泰国费用计算器</a> 讲清楚。</p>
<h2 id="stack">四项费用</h2>
<div class="tablewrap"><table><thead><tr><th>费用</th><th>费率（含税）</th><th>退货是否退还</th></tr></thead><tbody>
<tr><td>平台佣金</td><td>按类目：Marketplace 多数 10.70%，Mall 多数 13.91%（7月5日起）</td><td>退</td></tr>
<tr><td>交易手续费</td><td>3.21%（买家实付 + 平台折扣）</td><td>送达后不退</td></tr>
<tr><td>商业增长费</td><td>电子 6.96% / 其他 8.03%，每件封顶 ฿199</td><td>不退</td></tr>
<tr><td>平台基础设施费</td><td>每单 ฿1.07</td><td>不退</td></tr>
</tbody></table></div>
<h2 id="impact">对真实订单的影响</h2>
<p>฿299 精华（成本 ฿90，Marketplace）：费用由 {THB(old['total'])} 增至 {THB(new['total'])}，利润由 {THB(old['profit'])} 降至 {THB(new['profit'])}。非电子类 Marketplace 商品三项比例费合计约 21.9%，再加 ฿1.07。</p>
<h2 id="action">卖家可以做什么</h2>
<ul>
<li>定价时把四项费用都算进去，不要只看佣金。</li>
<li>投放 GMV Max 的非 Mall 卖家，检查是否达到营收 3% 门槛以享受佣金 −1.07 个百分点。</li>
<li>Mall 卖家评估 Mall Combo：佣金通常由 13.91% 降到 10.70%。</li>
</ul>
'''

def g_etsy_uk_zh():
    a = compute('etsy-uk', price=25, buyerShip=4, cost=8, shipCost=3.6)
    return f'''
<p>英国 Etsy 卖家有两项常被忽略的费用：<b>监管运营费</b>自 2026年6月22日起升至 <b>0.48%</b>；未填写 VAT 号时，Etsy 还会对其费用加收 <b>VAT</b>。用 <a href="/zh/etsy/uk/">Etsy 英国费用计算器</a> 一次算清。</p>
<h2 id="list">全部费用</h2>
<ul>
<li>刊登费 US$0.20（约 {GBP(LIST_GBP)}）</li>
<li>交易手续费 6.5%（商品 + 运费 + 礼品包装）</li>
<li>支付处理费 4% + £0.20 每单</li>
<li>监管运营费 0.48%（2026年6月21日前为 0.32%）</li>
<li>未填写 VAT 号：上述费用另加 20% VAT</li>
<li>站外广告：15% 或 12%，每单最高 US$100</li>
</ul>
<h2 id="example">示例</h2>
<p>£25 商品 + £4 运费、未注册 VAT：Etsy 费用合计 {GBP(a['total'])}（其中 VAT {GBP(a['fee']['feevat'])}），占订单 {a['total'] / 29 * 100:.1f}%；扣除成本 £8 与面单 £3.60 后利润 {GBP(a['profit'])}。</p>
<h2 id="action">定价建议</h2>
<ul>
<li>按订单总额的 12–14% 预留 Etsy 费用，低价商品更高。</li>
<li>热销款要把站外广告费（含其 VAT）算进售价。</li>
<li>注册 VAT 后尽快在 Etsy 填写 VAT 号。</li>
</ul>
'''

GUIDES_NEW_ZH = [
 dict(lang='zh', slug='tiktok-shop-singapore-commission-september-2026', short='新加坡佣金调整（9月1日）',
      title='TikTok Shop 新加坡 2026年9月1日佣金调整：统一 9.81% 与 S$30 封顶',
      desc='新加坡站 9月1日起统一佣金 9.81%（BXP 7.085%），电子类 S$30 封顶。谁多付、谁少付，附新元示例。',
      market='tiktok-shop-sg', cov='cov-ink', fig='9.81%', body=g_sg_zh, sources=MARKETS['tiktok-shop-sg']['sources']),
 dict(lang='zh', slug='tiktok-shop-thailand-seller-fees-2026', short='泰国卖家费用 2026',
      title='TikTok Shop 泰国 2026 卖家费用：佣金、3.21% 交易费、商业增长费与 ฿1.07',
      desc='泰国站每单四项费用、7月5日佣金上调、商业增长费与 Mall Combo，附泰铢示例。',
      market='tiktok-shop-th', cov='cov-amber', fig='4 项', body=g_th_zh, sources=MARKETS['tiktok-shop-th']['sources']),
 dict(lang='zh', slug='etsy-uk-fees-vat-regulatory-fee', short='Etsy 英国费用与 VAT',
      title='Etsy 英国卖家费用 2026：0.48% 监管运营费、费用 VAT 与实例',
      desc='英国店铺的全部 Etsy 费用：6.5% 交易费、4% + £0.20 处理费、6月22日起 0.48% 监管运营费与费用 VAT。',
      market='etsy-uk', cov='cov-green', fig='0.48%', body=g_etsy_uk_zh, sources=MARKETS['etsy-uk']['sources']),
]
PAGE_FN_NEW_ZH = {('tiktok-shop-sg', 'zh'): sg_zh, ('tiktok-shop-th', 'zh'): th_zh, ('etsy-uk', 'zh'): etsy_uk_zh}
