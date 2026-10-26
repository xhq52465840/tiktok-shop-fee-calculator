"""Russia (Ozon, Wildberries, Yandex Market) calculator pages and guides. EN + RU.
Every figure is from markets.compute() or the official rate files; nothing invented."""
from markets import MARKETS, compute
from site_helpers import money, pct, ex_table

RUB = lambda v, lang='en': money(v, 'RUB', lang=lang)
OZ = MARKETS['ozon']['selector']['options']
WB = MARKETS['wildberries']['selector']['options']
YM = MARKETS['yandex-market']['selector']['options']

def _ex(mid, labels, lang='en', **kw):
    f = compute(mid, **kw)
    rows = [(labels['net'], RUB(f['b']['net'], lang))]
    for k, r, a in f['rows']:
        if a == 0 and k == 'acq': continue
        lab = labels[k]
        how = f' ({pct(r)})' if r and k in ('oz_comm', 'wb_comm', 'ym_place', 'ym_deliv', 'ym_transfer', 'oz_heavy', 'acq') else ''
        if k in ('oz_mile', 'oz_proc', 'ym_proc', 'ym_accept') and r:
            how = f' ({RUB(r, lang)})'
        rows.append((lab + how, '−' + RUB(a, lang)))
    rows.append((labels['fees'], RUB(f['total'], lang), True))
    rows.append((labels['payout'], RUB(f['payout'], lang), True))
    if kw.get('cost'):
        rows.append((labels['cost'], '−' + RUB(kw['cost'] * kw.get('qty', 1), lang)))
        rows.append((labels['profit'], RUB(f['profit'], lang), True))
    return f, ex_table(rows)

# ---- sample rates for tables (all from the loaded rate files)
OZ_SAMPLES = [
 ('Красота и гигиена › Косметика для ухода', OZ[MARKETS['ozon']['defaultOption']]['r']),
 ('Электроника › Смартфоны, планшеты, мобильные телефоны', next(o['r'] for o in OZ if o['n'] == 'Смартфоны, планшеты, мобильные телефоны')),
 ('Одежда › Футболки', next((o['r'] for o in OZ if o['g'] == 'Одежда' and 'Футболки' in o['n']), None) or next(o['r'] for o in OZ if o['g'] == 'Одежда')),
 ('Детские товары › Игрушки', next(o['r'] for o in OZ if o['n'] == 'Игрушки')),
]
# find a clothing row for ozon
for o in OZ:
    if o['g'].startswith('Одежда') and 'Футбол' in o['n']:
        OZ_SAMPLES[2] = (f"{o['g']} › {o['n']}", o['r']); break

WB_SAMPLES = [
 ('Одежда › Футболки', WB[MARKETS['wildberries']['defaultOption']]['r']),
 ('Одежда › Платья', next(o['r'] for o in WB if o['n'] == 'Платья')),
 ('Смартфоны и гаджеты › Смартфоны', next(o['r'] for o in WB if o['n'] == 'Смартфоны')),
 ('Обувь › Кроссовки', next(o['r'] for o in WB if o['n'] == 'Кроссовки')),
 ('Ноутбуки и компьютеры › Ноутбуки', next(o['r'] for o in WB if o['n'] == 'Ноутбуки')),
]
YM_SAMPLES = [
 ('Товары для красоты › Косметика… › Уход за лицом', YM[MARKETS['yandex-market']['defaultOption']]['r']),
 ('Электроника › Телефоны › Смартфоны', next(o['r'] for o in YM if o['n'] == 'Телефоны › Смартфоны')),
 ('Одежда, обувь и аксессуары › Одежда для взрослых › Платья', next(o['r'] for o in YM if o['n'] == 'Одежда для взрослых › Платья')),
 ('Товары для животных › Корма для кошек и собак › Корма для кошек', next(o['r'] for o in YM if o['n'] == 'Корма для кошек и собак › Корма для кошек')),
]

def _oz_rate_table(lang):
    h = 'FBO / FBS ≤100 ₽' if lang == 'en' else 'FBO / FBS ≤100 ₽'
    h2 = '101–300 ₽'; h3 = '>300 ₽'; h4 = 'realFBS'
    rows = ''.join(
        f'<tr><td>{n}</td><td class="n">{pct(r["fbo"][0])}</td><td class="n">{pct(r["fbo"][1])}</td>'
        f'<td class="n">{pct(r["fbo"][2])}</td><td class="n">{pct(r["rfbs"])}</td></tr>'
        for n, r in OZ_SAMPLES)
    return f'<div class="tablewrap"><table><thead><tr><th>{"Category" if lang=="en" else "Категория"}</th><th class="n">{h}</th><th class="n">{h2}</th><th class="n">{h3}</th><th class="n">{h4}</th></tr></thead><tbody>{rows}</tbody></table></div>'

def _wb_rate_table(lang):
    rows = ''.join(
        f'<tr><td>{n}</td><td class="n">{pct(r["fbw"])}</td><td class="n">{pct(r["fbs"])}</td><td class="n">{pct(r["dbs"])}</td></tr>'
        for n, r in WB_SAMPLES)
    return f'<div class="tablewrap"><table><thead><tr><th>{"Subject" if lang=="en" else "Предмет"}</th><th class="n">FBW</th><th class="n">FBS</th><th class="n">DBS</th></tr></thead><tbody>{rows}</tbody></table></div>'

def _ym_rate_table(lang):
    rows = ''.join(
        f'<tr><td>{n}</td><td class="n">{pct(r.get("_") or r.get("fby") or list(r.values())[0])}</td></tr>'
        for n, r in YM_SAMPLES)
    return f'<div class="tablewrap"><table><thead><tr><th>{"Category" if lang=="en" else "Категория"}</th><th class="n">{"Placement" if lang=="en" else "Размещение"}</th></tr></thead><tbody>{rows}</tbody></table></div>'

# ===================================================================== OZON EN
def ozon_en():
    L = dict(net='Item subtotal', oz_comm='Ozon commission', oz_log='Logistics (FBO/FBS)', oz_mile='Last-mile', oz_proc='FBS processing',
             oz_heavy='Non-standard item', acq='Acquiring', fees='Total fees', payout='Payout', cost='Product cost', profit='Profit')
    fbo, t_fbo = _ex('ozon', L, price=1500, cost=450, vol=1.5)
    fbs, t_fbs = _ex('ozon', L, store='fbs', price=1500, cost=450, vol=1.5)
    cheap, t_cheap = _ex('ozon', L, price=250, cost=80, vol=0.5)
    body = f'''
<p class="callout"><b>Verified 26 Oct 2026.</b> Commission bands from Ozon’s category XLSX in force from <b>28 Aug 2026</b>. Logistics FBO/FBS from the XLSX in force from <b>30 Oct 2026</b>. Rules from «Полный список комиссий и тарифов» (edition printed 7 Oct 2026).</p>
<p>Ozon takes a category commission that depends on the fulfilment model and on the unit price, plus logistics and last-mile on FBO and FBS. realFBS (rFBS) pays only the commission — you handle delivery yourself. Acquiring is not published as a fixed percentage, so the calculator leaves it blank for you to fill in.</p>

<h2 id="models">FBO, FBS and realFBS</h2>
<ul>
<li><b>FBO</b> — stock sits in an Ozon warehouse. Ozon picks, packs and delivers. You pay commission + logistics + last-mile (25 ₽/item).</li>
<li><b>FBS</b> — you ship to an Ozon pickup point or sorting centre. Same commission bands as FBO, plus logistics, last-mile and a processing fee (typically 10 ₽; 0 ₽ at some points, 17 ₽ at some Moscow PPZ).</li>
<li><b>realFBS (rFBS)</b> — you deliver to the buyer yourself. Commission only (the &gt;300 ₽ rate of the category). No Ozon logistics.</li>
</ul>

<h2 id="commission">Commission by price band</h2>
<p>On FBO, FBO Fresh and FBS, Ozon publishes three rates for most product types: <b>17%</b> when the unit price is ≤100 ₽, <b>23%</b> for 101–300 ₽, and a category-specific rate above 300 ₽. realFBS uses a single rate (usually the same as the &gt;300 ₽ FBO/FBS rate). Commission is charged on the seller price including VAT and your discounts, at the rate in force when the order is placed, once the item is delivered.</p>
{_oz_rate_table('en')}
<p class="muted small">Sample of 701 options loaded from the official XLSX. Open the calculator to search every category and product type.</p>

<h2 id="example">Worked example — cosmetics, 1 500 ₽, 1.5 L, Moscow → Moscow</h2>
<p>Default category <i>Красота и гигиена › Косметика для ухода</i> (52% above 300 ₽). Logistics uses the Moscow cluster pair from the 30 Oct 2026 table; last-mile is the flat 25 ₽.</p>
<h3>FBO</h3>
{t_fbo}
<p>Fees {RUB(fbo['total'])} · payout {RUB(fbo['payout'])} · profit {RUB(fbo['profit'])} ({fbo['margin']:.1f}% margin) after a 450 ₽ product cost.</p>
<h3>FBS (same item)</h3>
{t_fbs}
<p>FBS adds the 10 ₽ processing fee. Same logistics and last-mile as FBO when both clusters are Moscow.</p>
<h3>Low-price band — 250 ₽ unit</h3>
{t_cheap}
<p>At 250 ₽ the 23% band applies (101–300 ₽), so commission drops to {RUB(cheap['fee']['oz_comm'])}. Logistics also uses the ≤300 ₽ column of the route table.</p>

<h2 id="logistics">Logistics, last-mile and extras</h2>
<ul>
<li><b>Logistics</b> — route (cluster from → cluster to) × volume bucket × price band (≤300 / &gt;300 ₽). Tariffs are fixed for 60 days from the supply request. When clusters are unknown, Ozon applies a universal (“default”) tariff by volume.</li>
<li><b>Last-mile</b> — 25 ₽ per item on FBO/FBS (pickup-point delivery ≤25 ₽).</li>
<li><b>Non-standard / heavy</b> — 3% of the item price, capped at 280 ₽/item (toggle in the calculator).</li>
<li><b>Forced storage</b> — 2.50 ₽/L/day (not modelled; see the guide).</li>
</ul>
<div class="callout warn"><b>Not modelled here:</b> non-local FBO markup (0–8%), FBO Fresh, FBO PVZ (−3 pp until 1 Dec 2026), Fashion new-seller 27%, realFBS motorbike &gt;500k ₽, returns and storage beyond the forced-storage note. Check Seller Edu for those.</div>

<h2 id="faq"></h2>
'''
    faq = [
     ('What does Ozon charge on FBO vs FBS vs realFBS?',
      'FBO and FBS share the same three price-band commission rates and both pay logistics + 25 ₽ last-mile; FBS also pays a processing fee (usually 10 ₽). realFBS pays only the single commission rate — you deliver yourself.'),
     ('Where do the 17% / 23% low-price rates come from?',
      'From Ozon’s official category XLSX in force from 28 August 2026. On FBO / FBO Fresh / FBS most product types are 17% at ≤100 ₽ and 23% at 101–300 ₽; above 300 ₽ the category rate applies.'),
     ('How is logistics calculated?',
      'From the official FBO/FBS logistics XLSX in force from 30 October 2026: pick the origin and destination clusters, the volume bucket and the ≤300 / &gt;300 ₽ column. Unknown clusters use the universal tariff sheet.'),
     ('Is acquiring included?',
      'Ozon does not publish a single public acquiring percentage on Seller Edu. The calculator leaves acquiring blank so you can enter the rate from your contract or payout report.'),
     ('When do the logistics tariffs in this calculator apply?',
      'The loaded table is the one Ozon marks as in force from 30 October 2026. Commission categories are from the 28 August 2026 XLSX.'),
    ]
    toc = [('models', 'FBO, FBS, realFBS'), ('commission', 'Commission bands'), ('example', 'Worked example'), ('logistics', 'Logistics & extras'), ('faq', 'FAQ'), ('sources', 'Sources')]
    return dict(title='Ozon Fee Calculator Russia 2026 (FBO / FBS / realFBS) | SellerFee',
                desc='Free Ozon Russia fee and profit calculator: FBO, FBS and realFBS commission by category and price band, logistics from 30 Oct 2026, last-mile and processing. Official rates, RUB.',
                h1='Ozon fee calculator (Russia)', lede='Commission by category and price band, FBO/FBS logistics from the 30 Oct 2026 table, last-mile and processing — then your payout and margin in rubles.',
                body=body, faq=faq, toc=toc)

def ozon_ru():
    L = dict(net='Сумма товаров', oz_comm='Вознаграждение Ozon', oz_log='Логистика (FBO/FBS)', oz_mile='Последняя миля', oz_proc='Обработка FBS',
             oz_heavy='Крупногабарит / нестандарт', acq='Эквайринг', fees='Всего комиссий', payout='К выплате', cost='Себестоимость', profit='Прибыль')
    fbo, t_fbo = _ex('ozon', L, 'ru', price=1500, cost=450, vol=1.5)
    fbs, t_fbs = _ex('ozon', L, 'ru', store='fbs', price=1500, cost=450, vol=1.5)
    cheap, t_cheap = _ex('ozon', L, 'ru', price=250, cost=80, vol=0.5)
    body = f'''
<p class="callout"><b>Проверено 26 октября 2026.</b> Комиссии — из XLSX категорий Ozon, действует с <b>28 августа 2026</b>. Логистика FBO/FBS — из XLSX, действует с <b>30 октября 2026</b>. Правила — «Полный список комиссий и тарифов» (редакция от 7 октября 2026).</p>
<p>Ozon удерживает вознаграждение по категории и модели исполнения, плюс логистику и последнюю милю на FBO и FBS. На realFBS (rFBS) платится только вознаграждение — доставку делаете вы. Процент эквайринга в открытых материалах Seller Edu не публикуется, поэтому в калькуляторе поле пустое — впишите свой тариф.</p>

<h2 id="models">FBO, FBS и realFBS</h2>
<ul>
<li><b>FBO</b> — товар на складе Ozon. Комиссия + логистика + последняя миля (25 ₽/шт.).</li>
<li><b>FBS</b> — вы привозите товар на ПВЗ или сортировочный центр Ozon. Те же ценовые полосы комиссии, что у FBO, плюс логистика, последняя миля и обработка (обычно 10 ₽; 0 ₽ на части точек, 17 ₽ на части московских ППЗ).</li>
<li><b>realFBS (rFBS)</b> — доставляете покупателю сами. Только вознаграждение (ставка &gt;300 ₽ категории).</li>
</ul>

<h2 id="commission">Вознаграждение по ценовым полосам</h2>
<p>На FBO, FBO Fresh и FBS у большинства типов товаров три ставки: <b>17%</b> при цене ≤100 ₽, <b>23%</b> при 101–300 ₽ и ставка категории выше 300 ₽. На realFBS — одна ставка. Вознаграждение считается от цены продавца с НДС и вашими скидками, по тарифу на момент заказа, после вручения.</p>
{_oz_rate_table('ru')}
<p class="muted small">Фрагмент из 701 позиции официального XLSX. В калькуляторе можно найти любую категорию и тип.</p>

<h2 id="example">Пример — косметика, 1 500 ₽, 1,5 л, Москва → Москва</h2>
<p>Категория по умолчанию <i>Красота и гигиена › Косметика для ухода</i> (52% свыше 300 ₽). Логистика — пара кластеров Москва из таблицы от 30 октября 2026; последняя миля — фиксированные 25 ₽.</p>
<h3>FBO</h3>
{t_fbo}
<p>Комиссии {RUB(fbo['total'],'ru')} · к выплате {RUB(fbo['payout'],'ru')} · прибыль {RUB(fbo['profit'],'ru')} (маржа {fbo['margin']:.1f}%) при себестоимости 450 ₽.</p>
<h3>FBS (тот же товар)</h3>
{t_fbs}
<p>На FBS добавляется обработка 10 ₽. Логистика и последняя миля те же, если оба кластера — Москва.</p>
<h3>Низкая цена — 250 ₽</h3>
{t_cheap}
<p>При 250 ₽ действует полоса 23% (101–300 ₽), комиссия {RUB(cheap['fee']['oz_comm'],'ru')}. Логистика берётся из колонки «до 300 ₽».</p>

<h2 id="logistics">Логистика, последняя миля и прочее</h2>
<ul>
<li><b>Логистика</b> — маршрут (кластер отправления → назначения) × объём × полоса цены. Тариф фиксируется на 60 дней с заявки на поставку. Если кластер неизвестен — универсальный тариф.</li>
<li><b>Последняя миля</b> — 25 ₽/шт. на FBO/FBS.</li>
<li><b>Нестандарт / КГТ</b> — 3% от цены, максимум 280 ₽/шт. (переключатель в калькуляторе).</li>
<li><b>Вынужденное хранение</b> — 2,50 ₽/л/сутки (в калькуляторе не считается — см. гайд).</li>
</ul>
<div class="callout warn"><b>Не учтено:</b> надбавка за нелокальный FBO (0–8%), FBO Fresh, FBO ПВЗ (−3 п.п. до 1 декабря 2026), Fashion для новых 27%, realFBS мототехника &gt;500 тыс. ₽, возвраты и хранение сверх вынужденного. Смотрите Seller Edu.</div>
'''
    faq = [
     ('Чем отличаются FBO, FBS и realFBS по комиссиям?',
      'У FBO и FBS одни и те же три ценовые ставки вознаграждения, плюс логистика и 25 ₽ последней мили; на FBS ещё обработка (обычно 10 ₽). На realFBS — только одна ставка вознаграждения, доставку делаете вы.'),
     ('Откуда ставки 17% и 23%?',
      'Из официального XLSX категорий Ozon, действует с 28 августа 2026. На FBO / FBO Fresh / FBS у большинства типов 17% до 100 ₽ и 23% от 101 до 300 ₽; выше 300 ₽ — ставка категории.'),
     ('Как считается логистика?',
      'По официальному XLSX логистики FBO/FBS с 30 октября 2026: кластеры, объём и колонка ≤300 / &gt;300 ₽. Неизвестные кластеры — универсальный тариф.'),
     ('Учтён ли эквайринг?',
      'Публичного единого процента эквайринга в Seller Edu нет. В калькуляторе поле пустое — впишите тариф из договора или отчёта о выплатах.'),
     ('С какой даты действуют тарифы логистики?',
      'Загружена таблица, которую Ozon обозначает как действующую с 30 октября 2026. Категории комиссий — из XLSX от 28 августа 2026.'),
    ]
    toc = [('models', 'FBO, FBS, realFBS'), ('commission', 'Вознаграждение'), ('example', 'Пример'), ('logistics', 'Логистика'), ('faq', 'FAQ'), ('sources', 'Источники')]
    return dict(title='Калькулятор комиссий Ozon 2026 (FBO / FBS / realFBS) | SellerFee',
                desc='Бесплатный калькулятор комиссий и прибыли Ozon: FBO, FBS и realFBS, вознаграждение по категориям и ценовым полосам, логистика с 30 окт. 2026, последняя миля. Официальные тарифы, ₽.',
                h1='Калькулятор комиссий Ozon', lede='Вознаграждение по категории и цене, логистика FBO/FBS из таблицы от 30 октября 2026, последняя миля и обработка — затем выплата и маржа в рублях.',
                body=body, faq=faq, toc=toc)

# ===================================================================== WB EN
def wb_en():
    L = dict(net='Item subtotal', wb_comm='WB commission (КВВ)', wb_log='Logistics', acq='Acquiring', fees='Total fees', payout='Payout', cost='Product cost', profit='Profit')
    fbw, t_fbw = _ex('wildberries', L, price=1500, cost=450, vol=1.5, coef=170)
    # official volume examples from instructions
    f_log055 = compute('wildberries', price=1500, vol=0.55, coef=170)
    f_log18 = compute('wildberries', price=1500, vol=1.8, coef=170)
    fbs_fast, t_fast = _ex('wildberries', L, store='fbs', price=1500, cost=450, vol=1.5, coef=170, x={'speed': 'h13'})
    body = f'''
<p class="callout"><b>Verified 26 Oct 2026.</b> Commission (КВВ) from Wildberries’ PDF in force from <b>7 Jul 2026</b>. Logistics from seller instructions updated <b>19 Oct 2026</b> (base tariff × warehouse coefficient, 170% since 15 Aug 2026). FBS fast-shipping discounts −5 / −3.5 pp are from Kommersant (7 Oct 2026, secondary).</p>
<p>Wildberries charges a subject-level commission (КВВ) that differs for FBW, FBS and DBS, plus volume-based logistics on FBW/FBS. Acquiring is not published as a fixed public percentage.</p>

<h2 id="models">FBW, FBS and DBS</h2>
<ul>
<li><b>FBW</b> — stock in a WB warehouse. Commission + logistics (base tariff × warehouse coefficient).</li>
<li><b>FBS</b> — you ship to WB. Higher КВВ than FBW on most subjects; same logistics formula (coefficient may differ by warehouse — check your cabinet). Optional fast-shipping discounts on commission.</li>
<li><b>DBS</b> — you deliver to the buyer. Commission only.</li>
</ul>

<h2 id="commission">Commission (КВВ) samples</h2>
{_wb_rate_table('en')}
<p class="muted small">7,464 subjects from the official PDF. Alcohol booking-only rows are omitted.</p>

<h2 id="logistics">Logistics formula</h2>
<p>For volumes up to 1 L WB publishes fixed steps (0.2 L → 23 ₽ … 1 L → 32 ₽). Above 1 L: <b>46 ₽ for the first litre + 14 ₽ per extra litre</b>, then × the warehouse coefficient (170% for WB warehouses since 15 Aug 2026). Reverse delivery uses the base tariff without the coefficient.</p>
<div class="formula"><div class="fr"><span class="fk">0.55 L × 170%</span><span>29 ₽ × 1.70 = <em>{RUB(f_log055['fee']['wb_log'])}</em> (official worked example)</span></div>
<div class="fr"><span class="fk">1.8 L × 170%</span><span>(46 + 14 × 0.8) × 1.70 = <em>{RUB(f_log18['fee']['wb_log'])}</em></span></div></div>

<h2 id="example">Worked example — T-shirts, 1 500 ₽, 1.5 L</h2>
<p>Subject <i>Одежда › Футболки</i>: FBW 43.5%, FBS 48%, DBS 45%.</p>
<h3>FBW</h3>
{t_fbw}
<p>Logistics on 1.5 L at 170% = {RUB(fbw['fee']['wb_log'])}. Profit {RUB(fbw['profit'])} ({fbw['margin']:.1f}%) after 450 ₽ cost.</p>
<h3>FBS with &lt;13 h dispatch (−5 pp)</h3>
{t_fast}
<p>КВВ becomes 48 − 5 = 43% (minimum 1%). Logistics unchanged in this example.</p>
<div class="callout warn"><b>Not modelled:</b> oversize clamp (1 000–3 000 ₽, 100% coefficient), reverse logistics beyond the note, return-to-PP fees (25 ₽ + 4 ₽/L above 1 L), storage. FBS discounts cite a secondary source — confirm in your WB account.</div>
'''
    faq = [
     ('What is КВВ?',
      'Комиссия вознаграждения Wildberries — the subject-level commission percentage. The official PDF lists separate FBW / FBS / DBS values per subject, in force from 7 July 2026.'),
     ('How is logistics calculated?',
      'Stepped tariff to 1 L, then 46 ₽ + 14 ₽ × extra litres, multiplied by the warehouse coefficient (170% for WB warehouses since 15 Aug 2026). Official examples: 0.55 L → 49.30 ₽, 1.8 L → 97.24 ₽ at 170%.'),
     ('Do FBS speed discounts apply?',
      'Kommersant (7 Oct 2026) and seller tools report −5 pp for dispatch under 13 hours and −3.5 pp under 42 hours. They are not in the КВВ PDF itself, so treat them as editable and confirm in your account.'),
     ('Is acquiring included?',
      'No public fixed acquiring % is published. Leave the field blank or enter your contract rate.'),
    ]
    toc = [('models', 'FBW, FBS, DBS'), ('commission', 'КВВ samples'), ('logistics', 'Logistics'), ('example', 'Worked example'), ('faq', 'FAQ'), ('sources', 'Sources')]
    return dict(title='Wildberries Fee Calculator Russia 2026 (FBW / FBS / DBS) | SellerFee',
                desc='Free Wildberries Russia fee calculator: КВВ by subject (FBW/FBS/DBS), logistics 46+14 ₽/L × coefficient, FBS speed discounts. Official PDF and instructions, RUB.',
                h1='Wildberries fee calculator (Russia)', lede='Subject-level КВВ for FBW, FBS and DBS, volume logistics with the warehouse coefficient, then your payout and margin in rubles.',
                body=body, faq=faq, toc=toc)

def wb_ru():
    L = dict(net='Сумма товаров', wb_comm='КВВ Wildberries', wb_log='Логистика', acq='Эквайринг', fees='Всего комиссий', payout='К выплате', cost='Себестоимость', profit='Прибыль')
    fbw, t_fbw = _ex('wildberries', L, 'ru', price=1500, cost=450, vol=1.5, coef=170)
    f_log055 = compute('wildberries', price=1500, vol=0.55, coef=170)
    f_log18 = compute('wildberries', price=1500, vol=1.8, coef=170)
    fbs_fast, t_fast = _ex('wildberries', L, 'ru', store='fbs', price=1500, cost=450, vol=1.5, coef=170, x={'speed': 'h13'})
    body = f'''
<p class="callout"><b>Проверено 26 октября 2026.</b> КВВ — из PDF Wildberries, действует с <b>7 июля 2026</b>. Логистика — из инструкций продавца, обновление <b>19 октября 2026</b> (базовый тариф × коэффициент склада, 170% с 15 августа 2026). Скидки FBS за быструю отгрузку −5 / −3,5 п.п. — по Коммерсанту (7 окт. 2026, вторичный источник).</p>

<h2 id="models">FBW, FBS и DBS</h2>
<ul>
<li><b>FBW</b> — склад WB. КВВ + логистика (базовый тариф × коэффициент).</li>
<li><b>FBS</b> — вы отгружаете на WB. КВВ обычно выше, чем на FBW; та же формула логистики. Опционально скидки за быструю отгрузку.</li>
<li><b>DBS</b> — доставляете сами. Только КВВ.</li>
</ul>

<h2 id="commission">Примеры КВВ</h2>
{_wb_rate_table('ru')}
<p class="muted small">7 464 предмета из официального PDF. Строки алкоголя только с бронью пропущены.</p>

<h2 id="logistics">Формула логистики</h2>
<p>До 1 л — фиксированные ступени. Свыше 1 л: <b>46 ₽ за первый литр + 14 ₽ за каждый следующий</b>, затем × коэффициент склада (170% для складов WB с 15 августа 2026). Обратная логистика — базовый тариф без коэффициента.</p>
<div class="formula"><div class="fr"><span class="fk">0,55 л × 170%</span><span>29 ₽ × 1,70 = <em>{RUB(f_log055['fee']['wb_log'],'ru')}</em></span></div>
<div class="fr"><span class="fk">1,8 л × 170%</span><span>(46 + 14 × 0,8) × 1,70 = <em>{RUB(f_log18['fee']['wb_log'],'ru')}</em></span></div></div>

<h2 id="example">Пример — футболки, 1 500 ₽, 1,5 л</h2>
<p>Предмет <i>Одежда › Футболки</i>: FBW 43,5%, FBS 48%, DBS 45%.</p>
<h3>FBW</h3>
{t_fbw}
<p>Логистика 1,5 л при 170% = {RUB(fbw['fee']['wb_log'],'ru')}. Прибыль {RUB(fbw['profit'],'ru')} ({fbw['margin']:.1f}%) при себестоимости 450 ₽.</p>
<h3>FBS с отгрузкой &lt;13 ч (−5 п.п.)</h3>
{t_fast}
<p>КВВ: 48 − 5 = 43% (минимум 1%).</p>
<div class="callout warn"><b>Не учтено:</b> крупногабарит (1 000–3 000 ₽, коэффициент 100%), обратная логистика сверх примечания, возврат в ПВЗ (25 ₽ + 4 ₽/л свыше 1 л), хранение. Скидки FBS — из вторичного источника, сверьте в личном кабинете.</div>
'''
    faq = [
     ('Что такое КВВ?',
      'Комиссия вознаграждения Wildberries — процент по предмету. В официальном PDF отдельные значения FBW / FBS / DBS, действует с 7 июля 2026.'),
     ('Как считается логистика?',
      'Ступени до 1 л, далее 46 ₽ + 14 ₽ × литры сверх 1 л, умножить на коэффициент склада (170% для складов WB с 15 августа 2026). Примеры: 0,55 л → 49,30 ₽; 1,8 л → 97,24 ₽ при 170%.'),
     ('Действуют ли скидки FBS за скорость?',
      'Коммерсант (7 окт. 2026) сообщает −5 п.п. при отгрузке до 13 ч и −3,5 п.п. до 42 ч. В PDF КВВ этого нет — поле редактируемое, сверьте в кабинете.'),
     ('Учтён ли эквайринг?',
      'Публичного фиксированного процента нет. Оставьте поле пустым или впишите тариф из договора.'),
    ]
    toc = [('models', 'FBW, FBS, DBS'), ('commission', 'КВВ'), ('logistics', 'Логистика'), ('example', 'Пример'), ('faq', 'FAQ'), ('sources', 'Источники')]
    return dict(title='Калькулятор комиссий Wildberries 2026 (FBW / FBS / DBS) | SellerFee',
                desc='Бесплатный калькулятор Wildberries: КВВ по предметам (FBW/FBS/DBS), логистика 46+14 ₽/л × коэффициент, скидки FBS. Официальный PDF и инструкции, ₽.',
                h1='Калькулятор комиссий Wildberries', lede='КВВ по предмету для FBW, FBS и DBS, логистика по объёму с коэффициентом склада — затем выплата и маржа в рублях.',
                body=body, faq=faq, toc=toc)

# ===================================================================== YM EN
def ym_en():
    L = dict(net='Item subtotal', ym_place='Placement', ym_deliv='Delivery', ym_mid='Middle mile', ym_proc='FBS processing',
             ym_transfer='Payment transfer', ym_accept='Payment acceptance', fees='Total fees', payout='Payout', cost='Product cost', profit='Profit')
    fby, t_fby = _ex('yandex-market', L, price=1500, cost=450, vol=1.5)
    cheap, t_cheap = _ex('yandex-market', L, price=250, cost=80, vol=1)
    mid37 = compute('yandex-market', price=1500, vol=37)
    body = f'''
<p class="callout"><b>Verified 26 Oct 2026.</b> Placement tariffs from Yandex Market help «Размещение товаров на витрине» (as published on the check date — the page itself has no effective-date stamp). Delivery, middle mile, processing and payment fees from the FBY / FBS / acquiring help pages.</p>
<p>Yandex Market charges category placement (usually the same across models; some rows differ for FBY/FBS/Express/DBS), plus delivery 5% (cap 1 000 ₽/item), middle-mile by volume, FBS processing 25 ₽, payment transfer 1.6–3.3% by payout schedule, and 0.12 ₽ acceptance per distinct SKU. Up to 99% of placement can be paid with Market points; placement is refunded on returns.</p>

<h2 id="models">FBY, FBS and DBS</h2>
<ul>
<li><b>FBY</b> — stock in a Market warehouse. Placement + delivery + middle mile + payment fees. Storage is free from 11 Oct to 31 Dec 2026.</li>
<li><b>FBS</b> — you ship to Market. Same stack plus 25 ₽ processing; optional speed discounts −4 / −7 pp on placement. Courier visit fee by daily order volume is not modelled.</li>
<li><b>DBS</b> — you deliver. Placement + payment fees only.</li>
</ul>

<h2 id="placement">Placement samples</h2>
{_ym_rate_table('en')}
<p class="muted small">8,329 options (first two category levels kept; deeper levels folded when rates match the ancestor). Published range roughly 0.5–53%.</p>

<h2 id="cheap">42% low-price tariff</h2>
<p>Until the end of 2026, FBY/FBS orders with unit price ≤300 ₽ and volume ≤5 L use a flat <b>42% placement</b> and <b>zero</b> delivery and middle mile. Official example: 250 ₽ / 1 L → placement {RUB(cheap['fee']['ym_place'])}.</p>
{t_cheap}

<h2 id="example">Worked example — face care, 1 500 ₽, 1.5 L, weekly payout</h2>
{t_fby}
<p>Middle mile on 1.5 L = {RUB(fby['fee']['ym_mid'])}. Official middle-mile example at 37 L = {RUB(mid37['fee']['ym_mid'])} (92 + 8 × 36, within the 5 500 ₽ cap).</p>
<div class="callout warn"><b>Not modelled:</b> FBS courier visit (500/350/150/0 ₽/day by volume), storage outside the free window, Express-only extras. Placement page is undated — we report “as published on 26 Oct 2026”.</div>
'''
    faq = [
     ('What is the 42% low-price tariff?',
      'Until the end of 2026, FBY/FBS items priced ≤300 ₽ with volume ≤5 L pay 42% placement and no delivery or middle-mile fee. Confirmed by the official worked example (250 ₽ → 105 ₽ placement).'),
     ('How is middle mile calculated?',
      'Ceil litres: 92 ₽ for the first litre, +8 ₽ per litre to 200 L, then +5 ₽, capped at 5 500 ₽. Official example: 37 L → 380 ₽.'),
     ('What are the payment transfer rates?',
      'From the acquiring help page: 1.6% (every 4 weeks), 2.3% (every 2 weeks), 2.8% (weekly), 3.3% (daily), plus 0.12 ₽ acceptance per distinct SKU.'),
     ('Can I pay placement with Market points?',
      'Yes — up to 99% of placement. Placement is refunded if the order is returned.'),
    ]
    toc = [('models', 'FBY, FBS, DBS'), ('placement', 'Placement'), ('cheap', '42% low-price'), ('example', 'Worked example'), ('faq', 'FAQ'), ('sources', 'Sources')]
    return dict(title='Yandex Market Fee Calculator 2026 (FBY / FBS / DBS) | SellerFee',
                desc='Free Yandex Market fee calculator: placement by category, 42% low-price tariff, delivery 5%, middle mile, payment transfer 1.6–3.3%. Official help pages, RUB.',
                h1='Yandex Market fee calculator', lede='Category placement, the 42% low-price tariff, delivery, middle mile and payment fees — then your payout and margin in rubles.',
                body=body, faq=faq, toc=toc)

def ym_ru():
    L = dict(net='Сумма товаров', ym_place='Размещение', ym_deliv='Доставка', ym_mid='Средняя миля', ym_proc='Обработка FBS',
             ym_transfer='Перевод платежа', ym_accept='Приём платежа', fees='Всего комиссий', payout='К выплате', cost='Себестоимость', profit='Прибыль')
    fby, t_fby = _ex('yandex-market', L, 'ru', price=1500, cost=450, vol=1.5)
    cheap, t_cheap = _ex('yandex-market', L, 'ru', price=250, cost=80, vol=1)
    mid37 = compute('yandex-market', price=1500, vol=37)
    body = f'''
<p class="callout"><b>Проверено 26 октября 2026.</b> Тарифы размещения — страница «Размещение товаров на витрине» (на дату проверки; на самой странице даты вступления нет). Доставка, средняя миля, обработка и платежи — из справки FBY / FBS / эквайринг.</p>

<h2 id="models">FBY, FBS и DBS</h2>
<ul>
<li><b>FBY</b> — склад Маркета. Размещение + доставка + средняя миля + платежи. Хранение бесплатно с 11 октября по 31 декабря 2026.</li>
<li><b>FBS</b> — отгружаете на Маркет. То же плюс обработка 25 ₽; скидки за скорость −4 / −7 п.п. к размещению. Плата за визит курьера не моделируется.</li>
<li><b>DBS</b> — доставляете сами. Размещение + платежи.</li>
</ul>

<h2 id="placement">Примеры размещения</h2>
{_ym_rate_table('ru')}
<p class="muted small">8 329 позиций (первые два уровня категорий; более глубокие свёрнуты, если ставки совпадают). Диапазон примерно 0,5–53%.</p>

<h2 id="cheap">Тариф 42% для низких цен</h2>
<p>До конца 2026 на FBY/FBS при цене ≤300 ₽ и объёме ≤5 л действует <b>42% размещения</b> и <b>ноль</b> за доставку и среднюю милю. Пример: 250 ₽ / 1 л → размещение {RUB(cheap['fee']['ym_place'],'ru')}.</p>
{t_cheap}

<h2 id="example">Пример — уход за лицом, 1 500 ₽, 1,5 л, выплата раз в неделю</h2>
{t_fby}
<p>Средняя миля 1,5 л = {RUB(fby['fee']['ym_mid'],'ru')}. Официальный пример на 37 л = {RUB(mid37['fee']['ym_mid'],'ru')}.</p>
<div class="callout warn"><b>Не учтено:</b> визит курьера FBS (500/350/150/0 ₽/день), хранение вне бесплатного окна, отдельные опции Express. Страница размещения без даты — указываем «как опубликовано 26 октября 2026».</div>
'''
    faq = [
     ('Что такое тариф 42%?',
      'До конца 2026 на FBY/FBS при цене ≤300 ₽ и объёме ≤5 л — 42% размещения без доставки и средней мили. Официальный пример: 250 ₽ → 105 ₽.'),
     ('Как считается средняя миля?',
      'Литры вверх: 92 ₽ за первый литр, +8 ₽ до 200 л, далее +5 ₽, потолок 5 500 ₽. Пример: 37 л → 380 ₽.'),
     ('Какие ставки перевода платежа?',
      'Из справки по эквайрингу: 1,6% (раз в 4 недели), 2,3% (раз в 2 недели), 2,8% (еженедельно), 3,3% (ежедневно), плюс 0,12 ₽ за приём на каждый SKU.'),
     ('Можно ли оплатить размещение баллами?',
      'Да, до 99% размещения. При возврате размещение возвращается.'),
    ]
    toc = [('models', 'FBY, FBS, DBS'), ('placement', 'Размещение'), ('cheap', 'Тариф 42%'), ('example', 'Пример'), ('faq', 'FAQ'), ('sources', 'Источники')]
    return dict(title='Калькулятор комиссий Яндекс Маркета 2026 (FBY / FBS / DBS) | SellerFee',
                desc='Бесплатный калькулятор Яндекс Маркета: размещение по категориям, тариф 42%, доставка 5%, средняя миля, перевод платежа 1,6–3,3%. Официальная справка, ₽.',
                h1='Калькулятор комиссий Яндекс Маркета', lede='Размещение по категории, тариф 42% для низких цен, доставка, средняя миля и платежи — затем выплата и маржа в рублях.',
                body=body, faq=faq, toc=toc)

# ---- Guides (EN)
def g_ozon_models():
    fbo = compute('ozon', price=1500, cost=450, vol=1.5)
    fbs = compute('ozon', store='fbs', price=1500, cost=450, vol=1.5)
    rfbs = compute('ozon', store='rfbs', price=1500, cost=450, vol=1.5)
    return f'''
<div class="kt"><h4>Key takeaways</h4><ul>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} FBO and FBS share the same three price-band commission rates; realFBS uses one rate.</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Logistics + 25 ₽ last-mile apply to FBO and FBS only; FBS adds ~10 ₽ processing.</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} On a 1 500 ₽ cosmetics SKU, FBO fees {RUB(fbo["total"])}, FBS {RUB(fbs["total"])}, realFBS {RUB(rfbs["total"])} (commission only).</li>
</ul></div>
<p>Ozon’s three fulfilment models look similar in the seller cabinet but the fee stack is different. This guide walks through the same SKU under each model using the rates in force in late October 2026.</p>
<h2 id="bands">Price bands on FBO/FBS</h2>
<p>Most product types pay <b>17%</b> at ≤100 ₽, <b>23%</b> at 101–300 ₽ and a category rate above 300 ₽. The calculator’s default, <i>Косметика для ухода</i>, is 52% above 300 ₽. realFBS ignores the low-price bands and uses that single rate.</p>
<h2 id="compare">Same SKU, three models</h2>
<p>1 500 ₽, 1.5 L, Moscow → Moscow, product cost 450 ₽.</p>
{ex_table([('FBO total fees', RUB(fbo['total'])), ('FBS total fees', RUB(fbs['total'])), ('realFBS total fees', RUB(rfbs['total'])),
           ('FBO profit', RUB(fbo['profit']), True), ('FBS profit', RUB(fbs['profit']), True), ('realFBS profit', RUB(rfbs['profit']), True)])}
<p>realFBS looks cheapest on fees only because you still pay your own delivery — add that under “shipping you pay” in the calculator before you compare.</p>
<h2 id="gaps">What we leave out</h2>
<p>Non-local FBO markup, FBO Fresh, FBO PVZ (−3 pp until 1 Dec 2026), Fashion new-seller 27%, forced storage 2.50 ₽/L/day and returns. See the linked Seller Edu documents.</p>
'''

def g_wb_unit():
    a = compute('wildberries', price=1500, vol=0.55, coef=170)
    b = compute('wildberries', price=1500, vol=1.8, coef=170)
    c = compute('wildberries', price=1500, cost=450, vol=1.5, coef=170)
    return f'''
<div class="kt"><h4>Key takeaways</h4><ul>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} КВВ is per subject and per model (FBW / FBS / DBS); PDF in force from 7 Jul 2026.</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Logistics: steps to 1 L, then 46 + 14 ₽/L, × warehouse coefficient (170% since 15 Aug).</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Official checks: 0.55 L → {RUB(a["fee"]["wb_log"])}, 1.8 L → {RUB(b["fee"]["wb_log"])}.</li>
</ul></div>
<p>Unit economics on Wildberries are commission plus volume logistics. Below is how the two pieces combine on a T-shirt at 1 500 ₽.</p>
<h2 id="kvv">КВВ</h2>
<p>Subject <i>Футболки</i>: FBW 43.5%, FBS 48%, DBS 45%. FBS fast-shipping discounts (−5 / −3.5 pp) come from secondary reporting — confirm in your account.</p>
<h2 id="log">Logistics</h2>
<div class="formula"><div class="fr"><span class="fk">≤ 1 L</span><span>fixed steps (0.2→23 … 1.0→32 ₽), then × coefficient</span></div>
<div class="fr"><span class="fk">&gt; 1 L</span><span>(46 + 14 × extra litres) × coefficient</span></div></div>
<h2 id="ex">T-shirt example</h2>
{ex_table([('Item subtotal', RUB(1500)), ('КВВ 43.5%', '−' + RUB(c['fee']['wb_comm'])), ('Logistics 1.5 L × 170%', '−' + RUB(c['fee']['wb_log'])),
           ('Total fees', RUB(c['total']), True), ('Payout', RUB(c['payout']), True), ('Profit after 450 ₽ cost', RUB(c['profit']), True)])}
'''

def g_ym_cheap():
    c = compute('yandex-market', price=250, cost=80, vol=1)
    n = compute('yandex-market', price=1500, cost=450, vol=1.5)
    m = compute('yandex-market', price=1500, vol=37)
    return f'''
<div class="kt"><h4>Key takeaways</h4><ul>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Until end of 2026: ≤300 ₽ and ≤5 L on FBY/FBS → 42% placement, no delivery, no middle mile.</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Official check: 250 ₽ / 1 L → placement {RUB(c["fee"]["ym_place"])}.</li>
<li>{'<svg class="i" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>'} Above the threshold, delivery 5% (cap 1 000 ₽) and middle mile (37 L → {RUB(m["fee"]["ym_mid"])}) return.</li>
</ul></div>
<p>Yandex Market’s low-price tariff is a temporary override on FBY and FBS. Cross the 300 ₽ or 5 L line and the normal stack comes back.</p>
<h2 id="in">Inside the tariff</h2>
{ex_table([('Item', '250 ₽ · 1 L · FBY'), ('Placement 42%', '−' + RUB(c['fee']['ym_place'])), ('Delivery', '0'), ('Middle mile', '0'),
           ('Transfer 2.8% (weekly)', '−' + RUB(c['fee']['ym_transfer'])), ('Acceptance', '−' + RUB(c['fee']['ym_accept'])),
           ('Payout', RUB(c['payout']), True)])}
<h2 id="out">Outside the tariff</h2>
{ex_table([('Item', '1 500 ₽ · 1.5 L · face care 52%'), ('Placement', '−' + RUB(n['fee']['ym_place'])), ('Delivery 5%', '−' + RUB(n['fee']['ym_deliv'])),
           ('Middle mile', '−' + RUB(n['fee']['ym_mid'])), ('Transfer + acceptance', '−' + RUB(n['fee']['ym_transfer'] + n['fee']['ym_accept'])),
           ('Total fees', RUB(n['total']), True)])}
'''

# RU guide bodies (shorter mirrors)
def g_ozon_models_ru():
    fbo = compute('ozon', price=1500, cost=450, vol=1.5)
    fbs = compute('ozon', store='fbs', price=1500, cost=450, vol=1.5)
    rfbs = compute('ozon', store='rfbs', price=1500, cost=450, vol=1.5)
    return f'''
<div class="kt"><h4>Главное</h4><ul>
<li>У FBO и FBS одни ценовые полосы комиссии; у realFBS — одна ставка.</li>
<li>Логистика + 25 ₽ последней мили — только FBO/FBS; на FBS ещё ~10 ₽ обработки.</li>
<li>На косметике 1 500 ₽: FBO {RUB(fbo["total"],"ru")}, FBS {RUB(fbs["total"],"ru")}, realFBS {RUB(rfbs["total"],"ru")}.</li>
</ul></div>
<h2 id="bands">Ценовые полосы</h2>
<p>Большинство типов: <b>17%</b> ≤100 ₽, <b>23%</b> 101–300 ₽, ставка категории выше 300 ₽. realFBS берёт одну ставку.</p>
<h2 id="compare">Один SKU — три модели</h2>
{ex_table([('Комиссии FBO', RUB(fbo['total'],'ru')), ('Комиссии FBS', RUB(fbs['total'],'ru')), ('Комиссии realFBS', RUB(rfbs['total'],'ru')),
           ('Прибыль FBO', RUB(fbo['profit'],'ru'), True), ('Прибыль FBS', RUB(fbs['profit'],'ru'), True), ('Прибыль realFBS', RUB(rfbs['profit'],'ru'), True)])}
<p>На realFBS комиссии ниже, но доставку оплачиваете вы — добавьте её в калькуляторе перед сравнением.</p>
'''

def g_wb_unit_ru():
    a = compute('wildberries', price=1500, vol=0.55, coef=170)
    b = compute('wildberries', price=1500, vol=1.8, coef=170)
    c = compute('wildberries', price=1500, cost=450, vol=1.5, coef=170)
    return f'''
<div class="kt"><h4>Главное</h4><ul>
<li>КВВ — по предмету и модели; PDF с 7 июля 2026.</li>
<li>Логистика: ступени до 1 л, далее 46+14 ₽/л × коэффициент (170% с 15 августа).</li>
<li>Проверка: 0,55 л → {RUB(a["fee"]["wb_log"],"ru")}, 1,8 л → {RUB(b["fee"]["wb_log"],"ru")}.</li>
</ul></div>
<h2 id="ex">Пример — футболка 1 500 ₽</h2>
{ex_table([('Сумма', RUB(1500,'ru')), ('КВВ 43,5%', '−' + RUB(c['fee']['wb_comm'],'ru')), ('Логистика 1,5 л × 170%', '−' + RUB(c['fee']['wb_log'],'ru')),
           ('Всего', RUB(c['total'],'ru'), True), ('К выплате', RUB(c['payout'],'ru'), True), ('Прибыль после 450 ₽', RUB(c['profit'],'ru'), True)])}
'''

def g_ym_cheap_ru():
    c = compute('yandex-market', price=250, cost=80, vol=1)
    n = compute('yandex-market', price=1500, cost=450, vol=1.5)
    return f'''
<div class="kt"><h4>Главное</h4><ul>
<li>До конца 2026: ≤300 ₽ и ≤5 л на FBY/FBS → 42% размещения без доставки и средней мили.</li>
<li>Проверка: 250 ₽ / 1 л → {RUB(c["fee"]["ym_place"],"ru")}.</li>
<li>Выше порога возвращаются доставка 5% и средняя миля.</li>
</ul></div>
<h2 id="in">Внутри тарифа</h2>
{ex_table([('Товар', '250 ₽ · 1 л · FBY'), ('Размещение 42%', '−' + RUB(c['fee']['ym_place'],'ru')), ('Доставка / ср. миля', '0'),
           ('Перевод 2,8%', '−' + RUB(c['fee']['ym_transfer'],'ru')), ('К выплате', RUB(c['payout'],'ru'), True)])}
<h2 id="out">Вне тарифа</h2>
{ex_table([('Товар', '1 500 ₽ · 1,5 л'), ('Размещение 52%', '−' + RUB(n['fee']['ym_place'],'ru')), ('Доставка 5%', '−' + RUB(n['fee']['ym_deliv'],'ru')),
           ('Средняя миля', '−' + RUB(n['fee']['ym_mid'],'ru')), ('Всего комиссий', RUB(n['total'],'ru'), True)])}
'''

GUIDES_RU = [
 dict(slug='ozon-fbo-fbs-realfbs-2026', short='Ozon FBO vs FBS vs realFBS', lang='en', cov='cov-blue', fig='FBO/FBS',
      title='Ozon FBO vs FBS vs realFBS in 2026: which fee stack you actually pay',
      desc='Side-by-side Ozon fees for the three fulfilment models on the same SKU, with the 17%/23% price bands and logistics from 30 Oct 2026.',
      market='ozon', body=g_ozon_models,
      sources=[('Полный список комиссий и тарифов — Ozon Seller Edu', 'https://seller-edu.ozon.ru/libra/commissions-tariffs/legal-information/full-actual-commissions'),
               ('Таблица категорий, с 28 Aug 2026 — Ozon XLSX', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8%CC%86_%D0%B4%D0%BB%D1%8F_%D1%80%D0%B0%D1%81%D1%87%D1%91%D1%82%D0%B0_%D0%B2%D0%BE%D0%B7%D0%BD%D0%B0%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F_28082026.xlsx'),
               ('Логистика FBO и FBS с 30 Oct 2026 — Ozon XLSX', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/logistika-fbo-fbs-30102026_1789376537.xlsx')]),
 dict(slug='wildberries-logistics-commission-2026', short='Wildberries unit economics', lang='en', cov='cov-amber', fig='46+14₽',
      title='Wildberries logistics and commission unit economics in 2026',
      desc='How WB КВВ and the 46+14 ₽/L logistics tariff with the 170% coefficient combine, with the official 0.55 L and 1.8 L checks.',
      market='wildberries', body=g_wb_unit,
      sources=[('Таблица КВВ, с 7 Jul 2026 — Wildberries PDF', 'https://static-basket-02.wbbasket.ru/vol20/folder/comission/KVV_Wildberries_ru_20260630.pdf'),
               ('Доставка: виды и расчёт — WB instructions (19 Oct 2026)', 'https://seller.wildberries.ru/instructions/ru/ru/material/logistics-types-and-cost-calculation')]),
 dict(slug='yandex-market-42-percent-low-price-2026', short='Yandex Market 42% tariff', lang='en', cov='cov-green', fig='42%',
      title='Yandex Market’s 42% low-price tariff until the end of 2026',
      desc='When the 42% placement override applies (≤300 ₽, ≤5 L), what it zeroes out, and how fees jump once you leave it.',
      market='yandex-market', body=g_ym_cheap,
      sources=[('Размещение товаров на витрине — Yandex Market', 'https://yandex.ru/support/marketplace/ru/introduction/rates/placement'),
               ('Тарифы FBY — Yandex Market', 'https://yandex.ru/support/marketplace/ru/introduction/rates/models/fby'),
               ('Приём и перевод платежей — Yandex Market', 'https://yandex.ru/support/marketplace/ru/introduction/rates/acquiring')]),
 # Russian mirrors
 dict(slug='ozon-fbo-fbs-realfbs-2026', short='Ozon FBO / FBS / realFBS', lang='ru', cov='cov-blue', fig='FBO/FBS',
      title='Ozon FBO, FBS и realFBS в 2026: какая схема комиссий у каждой модели',
      desc='Сравнение комиссий Ozon на одном SKU для трёх моделей, ценовые полосы 17%/23% и логистика с 30 октября 2026.',
      market='ozon', body=g_ozon_models_ru,
      sources=[('Полный список комиссий и тарифов — Ozon Seller Edu', 'https://seller-edu.ozon.ru/libra/commissions-tariffs/legal-information/full-actual-commissions'),
               ('Таблица категорий с 28.08.2026 — Ozon XLSX', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/%D0%A2%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0_%D0%BA%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D0%B8%CC%86_%D0%B4%D0%BB%D1%8F_%D1%80%D0%B0%D1%81%D1%87%D1%91%D1%82%D0%B0_%D0%B2%D0%BE%D0%B7%D0%BD%D0%B0%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F_28082026.xlsx'),
               ('Логистика FBO и FBS с 30.10.2026 — Ozon XLSX', 'https://cdn.ozone.ru/s3/ozon-disk-api/Seller-edu/files/commissions-tariffs/commissions/logistika-fbo-fbs-30102026_1789376537.xlsx')]),
 dict(slug='wildberries-logistics-commission-2026', short='Экономика Wildberries', lang='ru', cov='cov-amber', fig='46+14₽',
      title='Логистика и КВВ Wildberries в 2026: юнит-экономика',
      desc='Как складываются КВВ и тариф логистики 46+14 ₽/л с коэффициентом 170%, с проверкой 0,55 л и 1,8 л.',
      market='wildberries', body=g_wb_unit_ru,
      sources=[('Таблица КВВ с 07.07.2026 — Wildberries PDF', 'https://static-basket-02.wbbasket.ru/vol20/folder/comission/KVV_Wildberries_ru_20260630.pdf'),
               ('Доставка: виды и расчёт — инструкции WB (19.10.2026)', 'https://seller.wildberries.ru/instructions/ru/ru/material/logistics-types-and-cost-calculation')]),
 dict(slug='yandex-market-42-percent-low-price-2026', short='Тариф 42% Маркета', lang='ru', cov='cov-green', fig='42%',
      title='Тариф Яндекс Маркета 42% для низких цен до конца 2026',
      desc='Когда действует тариф 42% (≤300 ₽, ≤5 л), что обнуляется и как растут комиссии после выхода из него.',
      market='yandex-market', body=g_ym_cheap_ru,
      sources=[('Размещение товаров на витрине — Яндекс Маркет', 'https://yandex.ru/support/marketplace/ru/introduction/rates/placement'),
               ('Тарифы FBY — Яндекс Маркет', 'https://yandex.ru/support/marketplace/ru/introduction/rates/models/fby'),
               ('Приём и перевод платежей — Яндекс Маркет', 'https://yandex.ru/support/marketplace/ru/introduction/rates/acquiring')]),
]

PAGE_FN_RU = {
 ('ozon', 'en'): ozon_en, ('ozon', 'ru'): ozon_ru,
 ('wildberries', 'en'): wb_en, ('wildberries', 'ru'): wb_ru,
 ('yandex-market', 'en'): ym_en, ('yandex-market', 'ru'): ym_ru,
}
