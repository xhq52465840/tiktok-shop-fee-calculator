"""Embeddable calculator widget: /{lang}/embed/{slug}/ frame pages, the /{lang}/embed/ docs page and assets/embed.js.
Other sites paste a small snippet; embed.js turns it into an auto-sizing iframe. The snippet itself carries a plain
"Powered by sellerfee.app" link to the matching calculator page, so the backlink lives in the host page's HTML."""
import json, html
from markets import MARKETS
from sf_site import widget, page, crumbs, esc, BASE, MARK, ic, ptile, calc_name, VDATE
from i18n import LANGS, tr

ORDER = ['tiktok-shop-my', 'tiktok-shop-sg', 'tiktok-shop-th', 'tiktok-shop-ph', 'tiktok-shop-vn', 'tiktok-shop-id', 'tiktok-shop-us', 'tiktok-shop-uk',
         'shopee-my', 'shopee-sg', 'shopee-th', 'shopee-ph', 'shopee-id', 'shopee-vn', 'lazada-my', 'walmart-us', 'etsy', 'etsy-uk',
         'ozon', 'wildberries', 'yandex-market']

T = {
 'en': dict(powered='Powered by {a}', calc='fee calculator', cta='Embed this calculator', nav='Embed calculators',
    title='Embed a Free Marketplace Fee Calculator on Your Website | SellerFee',
    desc='Add any SellerFee calculator (TikTok Shop, Shopee, Lazada, Walmart, Etsy, Ozon, Wildberries, Yandex Market) to your blog or site with one copy-paste snippet. Free, responsive, always up to date.',
    h1='Embed a fee calculator on your site',
    lede='Put any of our {n} calculators on your blog, course or agency site. Copy one snippet, paste it into your HTML, and your readers get a live calculator that we keep up to date when platforms change their fees.',
    why_h='Why embed it', why=['Free, no account and no API key.', 'Rates are updated on our side, so the widget on your page is always current.', 'Responsive: one column on phones, two columns on wide screens. The script version sets its own height.',
         'Runs in the visitor’s browser. Nothing they type is sent to us or to you, and the widget sets no cookies.'],
    demo_h='Live preview', demo_p='This is the snippet below, running on this page.',
    build_h='Get the code', f_calc='Calculator', f_lang='Language of the widget', f_mode='Code type',
    m_script='Script: sets its own height (recommended)', m_iframe='Plain iframe: for site builders that strip scripts',
    copy='Copy code', copied='Copied', how_h='How to add it',
    how=['Pick a calculator and a language above, then copy the code.', 'Paste it into your page where the calculator should appear. In WordPress use a Custom HTML block; in Webflow, Wix or Squarespace use an Embed / Code block.',
         'Keep the “Powered by sellerfee.app” line under the widget. It is the only thing we ask in return, and it tells your readers where the rates come from.'],
    all_h='Code for every calculator', all_p='The same snippets, one per calculator, in the language of this page.', preview='Open the widget on its own',
    rules_h='Terms of use', rules=['Free for any website, including commercial sites.', 'Please keep the credit link visible and don’t make it nofollow.', 'Don’t frame the widget in a way that hides its source or suggests it is your own tool.'],
    faq_h='Questions', faq=[('Does the widget slow my page down?', 'The script is under 2 KB and loads the calculator lazily, only when it scrolls into view. The calculator itself is cached by the browser.'),
         ('Can I change the size?', 'The widget takes the full width of its container. Put it in a narrower column if you want it smaller. With the plain iframe, set the height attribute yourself (about 1,900 px fits every calculator).'),
         ('Will the numbers stay current?', 'Yes. The widget loads the same rate cards as our calculator pages, so when a platform changes its fees, your embed updates too.')],
    iframe_title='{name} fee calculator by sellerfee.app'),
 'zh': dict(powered='由 {a} 提供支持', calc='费用计算器', cta='嵌入此计算器', nav='嵌入计算器',
    title='在你的网站嵌入免费的电商平台费用计算器 | SellerFee',
    desc='一段代码即可把 SellerFee 的任意计算器（TikTok Shop、Shopee、Lazada、Walmart、Etsy、Ozon、Wildberries、Yandex Market）放到你的博客或网站上。免费、自适应、费率自动更新。',
    h1='把费用计算器嵌入你的网站',
    lede='我们的 {n} 个计算器都可以放到你的博客、课程或代运营网站上。复制一段代码，粘贴到你的 HTML 里，读者就能直接使用实时计算器；平台调整费率时，我们会同步更新。',
    why_h='为什么要嵌入', why=['完全免费，不用注册账号，也不需要 API 密钥。', '费率在我们这边更新，你页面上的计算器始终是最新的。', '自适应布局：手机上单栏，宽屏上双栏。脚本版会自动调整高度。',
         '计算在访客的浏览器里完成，输入的数字不会发给我们或你，计算器也不设置任何 Cookie。'],
    demo_h='实时预览', demo_p='下面就是这段代码在本页运行的效果。',
    build_h='获取代码', f_calc='计算器', f_lang='计算器界面语言', f_mode='代码类型',
    m_script='脚本版：自动调整高度（推荐）', m_iframe='纯 iframe 版：适用于会过滤脚本的建站工具',
    copy='复制代码', copied='已复制', how_h='如何添加',
    how=['在上方选择计算器和语言，然后复制代码。', '把代码粘贴到页面中想显示计算器的位置。WordPress 请使用“自定义 HTML”区块；Webflow、Wix 或 Squarespace 请使用“嵌入/代码”区块。',
         '请保留计算器下方指向 sellerfee.app 的署名链接。这是我们唯一的要求，也能让读者知道费率的来源。'],
    all_h='全部计算器的代码', all_p='每个计算器一段代码，界面语言与本页相同。', preview='单独打开该计算器',
    rules_h='使用条款', rules=['任何网站都可免费使用，包括商业网站。', '请保持署名链接可见，不要加 nofollow。', '请勿以隐藏来源或冒充自有工具的方式嵌入。'],
    faq_h='常见问题', faq=[('嵌入后会拖慢我的页面吗？', '脚本不到 2 KB，计算器采用懒加载，只有滚动到可见位置时才加载，之后由浏览器缓存。'),
         ('可以调整尺寸吗？', '计算器会占满所在容器的宽度，想小一点就放进更窄的栏里。使用纯 iframe 版时，请自行设置 height 属性（约 1,900 像素即可容纳所有计算器）。'),
         ('数据会一直保持最新吗？', '会。嵌入的计算器和我们计算器页面使用同一套费率表，平台调整费用后，你网站上的版本也会同步更新。')],
    iframe_title='sellerfee.app 提供的{name}费用计算器'),
 'ru': dict(powered='Работает на {a}', calc='калькулятор комиссий', cta='Встроить калькулятор', nav='Встроить калькулятор',
    title='Бесплатный калькулятор комиссий маркетплейсов для вашего сайта | SellerFee',
    desc='Добавьте любой калькулятор SellerFee (Ozon, Wildberries, Яндекс Маркет, TikTok Shop, Shopee, Lazada, Walmart, Etsy) на свой блог или сайт одним фрагментом кода. Бесплатно, адаптивно, тарифы всегда актуальны.',
    h1='Встройте калькулятор комиссий на свой сайт',
    lede='Любой из наших {n} калькуляторов можно поставить в блог, на сайт курса или агентства. Скопируйте фрагмент кода, вставьте его в HTML — и у читателей будет живой калькулятор, который мы обновляем, когда площадки меняют тарифы.',
    why_h='Зачем встраивать', why=['Бесплатно, без регистрации и без API-ключа.', 'Тарифы обновляем мы, поэтому виджет на вашей странице всегда актуален.', 'Адаптивный: одна колонка на телефоне, две — на широком экране. Версия со скриптом сама подбирает высоту.',
         'Расчёт идёт в браузере посетителя. Введённые цифры не отправляются ни нам, ни вам, виджет не ставит cookie.'],
    demo_h='Живой пример', demo_p='Это тот же фрагмент кода, что ниже, работающий на этой странице.',
    build_h='Получить код', f_calc='Калькулятор', f_lang='Язык виджета', f_mode='Тип кода',
    m_script='Скрипт: сам подбирает высоту (рекомендуется)', m_iframe='Обычный iframe: для конструкторов, которые вырезают скрипты',
    copy='Скопировать код', copied='Скопировано', how_h='Как добавить',
    how=['Выберите калькулятор и язык выше и скопируйте код.', 'Вставьте его в то место страницы, где должен быть калькулятор. В WordPress — блок «Произвольный HTML», в Tilda — блок T123, в Webflow, Wix или Squarespace — блок Embed / Code.',
         'Оставьте под виджетом строку со ссылкой на sellerfee.app. Это всё, о чём мы просим, и так читатели видят, откуда взяты тарифы.'],
    all_h='Код для каждого калькулятора', all_p='Те же фрагменты, по одному на калькулятор, на языке этой страницы.', preview='Открыть виджет отдельно',
    rules_h='Условия', rules=['Бесплатно для любых сайтов, в том числе коммерческих.', 'Пожалуйста, оставляйте ссылку видимой и не делайте её nofollow.', 'Не встраивайте виджет так, чтобы скрыть источник или выдать его за свой инструмент.'],
    faq_h='Вопросы', faq=[('Не замедлит ли виджет мою страницу?', 'Скрипт весит меньше 2 КБ, а калькулятор загружается лениво — только когда до него доходит прокрутка. Дальше его кэширует браузер.'),
         ('Можно изменить размер?', 'Виджет занимает всю ширину контейнера. Чтобы сделать его меньше, поставьте его в более узкую колонку. Для обычного iframe задайте атрибут height сами (около 1 900 px хватает для любого калькулятора).'),
         ('Цифры будут актуальными?', 'Да. Виджет загружает те же тарифы, что и страницы наших калькуляторов: когда площадка меняет комиссии, обновляется и ваш виджет.')],
    iframe_title='{name}: калькулятор комиссий от sellerfee.app'),
 'ms': dict(powered='Dikuasakan oleh {a}', calc='kalkulator yuran', cta='Benamkan kalkulator ini', nav='Benamkan kalkulator',
    title='Benamkan Kalkulator Yuran Marketplace Percuma di Laman Web Anda | SellerFee',
    desc='Tambah mana-mana kalkulator SellerFee (TikTok Shop, Shopee, Lazada, Walmart, Etsy, Ozon, Wildberries, Yandex Market) ke blog atau laman web anda dengan satu kod salin-tampal. Percuma, responsif, sentiasa dikemas kini.',
    h1='Benamkan kalkulator yuran di laman web anda',
    lede='Letakkan mana-mana daripada {n} kalkulator kami di blog, kursus atau laman agensi anda. Salin satu kod, tampal ke dalam HTML anda, dan pembaca mendapat kalkulator langsung yang kami kemas kini apabila platform menukar yuran.',
    why_h='Kenapa benamkan', why=['Percuma, tiada akaun dan tiada kunci API.', 'Kadar dikemas kini di pihak kami, jadi widget di halaman anda sentiasa terkini.', 'Responsif: satu lajur di telefon, dua lajur di skrin lebar. Versi skrip menetapkan ketinggiannya sendiri.',
         'Berjalan dalam pelayar pelawat. Apa yang ditaip tidak dihantar kepada kami atau anda, dan widget tidak menetapkan kuki.'],
    demo_h='Pratonton langsung', demo_p='Ini ialah kod di bawah, berjalan di halaman ini.',
    build_h='Dapatkan kod', f_calc='Kalkulator', f_lang='Bahasa widget', f_mode='Jenis kod',
    m_script='Skrip: menetapkan ketinggian sendiri (disyorkan)', m_iframe='Iframe biasa: untuk pembina laman yang membuang skrip',
    copy='Salin kod', copied='Disalin', how_h='Cara menambahnya',
    how=['Pilih kalkulator dan bahasa di atas, kemudian salin kod.', 'Tampal di tempat kalkulator patut muncul. Dalam WordPress gunakan blok Custom HTML; dalam Webflow, Wix atau Squarespace gunakan blok Embed / Code.',
         'Kekalkan baris pautan sellerfee.app di bawah widget. Itu sahaja yang kami minta, dan ia memberitahu pembaca dari mana kadar diambil.'],
    all_h='Kod untuk setiap kalkulator', all_p='Kod yang sama, satu bagi setiap kalkulator, dalam bahasa halaman ini.', preview='Buka widget secara berasingan',
    rules_h='Syarat penggunaan', rules=['Percuma untuk mana-mana laman web, termasuk laman komersial.', 'Sila kekalkan pautan kredit kelihatan dan jangan jadikannya nofollow.', 'Jangan benamkan widget dengan cara yang menyembunyikan sumbernya atau menampilkannya sebagai alat anda sendiri.'],
    faq_h='Soalan', faq=[('Adakah widget melambatkan halaman saya?', 'Skrip kurang daripada 2 KB dan kalkulator dimuatkan secara malas, hanya apabila ia ditatal ke paparan. Kalkulator itu kemudian disimpan dalam cache pelayar.'),
         ('Bolehkah saya menukar saiznya?', 'Widget mengambil lebar penuh bekasnya. Letakkan dalam lajur yang lebih sempit jika mahu lebih kecil. Dengan iframe biasa, tetapkan atribut height sendiri (kira-kira 1,900 px muat untuk semua kalkulator).'),
         ('Adakah angka kekal terkini?', 'Ya. Widget memuatkan kad kadar yang sama seperti halaman kalkulator kami, jadi apabila platform menukar yuran, widget anda turut dikemas kini.')],
    iframe_title='Kalkulator yuran {name} oleh sellerfee.app'),
}

def cta_link(mid, lang):
    return f'<div class="embedcta"><a href="/{lang}/embed/#{mid}">{ic("ext", 14)}{esc(T[lang]["cta"])}</a></div>'

def credit_html(mid, lang, inline_style=True):
    """The credit line that ships in the host page's HTML (dofollow, points to the matching calculator page)."""
    m = MARKETS[mid]; url = f'{BASE}{lang}/{m["slug"]}/'; t = T[lang]
    name = f'{calc_name(m, lang)} {t["calc"]}'
    st = ' style="font:13px/1.5 system-ui,sans-serif;margin:8px 0 0;color:#5b6474"' if inline_style else ''
    return f'<p class="sellerfee-credit"{st}>{html.escape(name)} · {html.escape(t["powered"]).replace("{a}", f'<a href="{url}">sellerfee.app</a>')}</p>'

def snippet(mid, lang, mode='script'):
    m = MARKETS[mid]; t = T[lang]
    title = t['iframe_title'].format(name=calc_name(m, lang))
    if mode == 'script':
        return (f'<div class="sellerfee-embed" data-calc="{m["slug"]}" data-lang="{lang}" data-title="{html.escape(title)}">\n{credit_html(mid, lang)}\n</div>\n'
                f'<script src="{BASE}assets/embed.js" async></script>')
    return (f'<iframe src="{BASE}{lang}/embed/{m["slug"]}/" title="{html.escape(title)}" width="100%" height="1900" loading="lazy" '
            f'allow="clipboard-write" style="border:0;width:100%;max-width:100%;display:block"></iframe>\n{credit_html(mid, lang)}')

FRAME_CSS = ('body.sf-embed{background:transparent}.sf-embed .wrap{max-width:none;padding:2px 3px 6px}.sf-embed .main{padding-top:0}'
             '.sf-embed .side{position:static}.sf-pw{display:flex;align-items:center;justify-content:flex-end;gap:6px;margin-top:12px;font-size:12.5px;color:var(--ink-500)}'
             '.sf-pw a{color:var(--ink-900);font-weight:600}.sf-pw .mark{width:16px;height:16px}'
             '.emo>summary{list-style:none;cursor:pointer}.emo>summary::-webkit-details-marker{display:none}.emo>summary h3{margin-bottom:0}'
             '.emo[open]>summary h3{margin-bottom:16px}.emo>summary .chev{margin-left:8px;transition:transform .15s}.emo[open]>summary .chev{transform:rotate(180deg)}')
FRAME_JS = ("(function(){if(window.parent===window)return;var last=0;function s(){var h=Math.ceil(document.documentElement.getBoundingClientRect().height);"
            "if(h&&h!==last){last=h;window.parent.postMessage({sellerfee:'height',h:h},'*')}}"
            "if(window.ResizeObserver)new ResizeObserver(s).observe(document.body);window.addEventListener('load',s);document.addEventListener('toggle',s,true);s()})();")

def compact(h):
    """Fold the optional sections (3: other costs, 4: programmes) so the embed stays short; ids are unchanged."""
    out = []
    for line in h.split('\n'):
        for n in ('3', '4'):
            pre = f'<div class="cs"><h3><span class="n">{n}</span>'
            if line.startswith(pre):
                i = line.index('</h3>') + 5
                line = '<div class="cs"><details class="emo"><summary>' + line[len('<div class="cs">'):i].replace('</h3>', ic('chev', 16, 'chev') + '</h3>') + '</summary>' + line[i:-len('</div>')] + '</details></div>'
        out.append(line)
    return '\n'.join(out)

def embed_frame(mid, lang, w):
    m = MARKETS[mid]; t = T[lang]; url = f'{BASE}{lang}/{m["slug"]}/'
    name = calc_name(m, lang)
    path = f'{lang}/embed/{m["slug"]}/'
    doc = f'''<!doctype html>
<html lang="{LANGS[lang]["html"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(name)} · SellerFee</title><meta name="robots" content="noindex,follow">
<link rel="stylesheet" href="/assets/style.css"><style>{FRAME_CSS}</style></head>
<body class="sf-embed"><div class="wrap">{compact(widget(mid, lang))}
<p class="sf-pw">{MARK}<span>{esc(t["powered"]).replace("{a}", f'<a href="{url}" target="_blank" rel="noopener">sellerfee.app</a>')}</span></p></div>
<script>window.SF_MARKET.page={json.dumps(url)};</script><script src="/assets/engine.js?v=2" defer></script><script>{FRAME_JS}</script></body></html>
'''
    w(path, doc)

def embed_doc(lang, w, alt):
    t = T[lang]; path = f'{lang}/embed/'
    ch, cld = crumbs(path, [('SellerFee', f'{lang}/'), (t['nav'], None)], lang)
    mids = [k for k in ORDER if k in MARKETS] + [k for k in MARKETS if k not in ORDER]
    demo = 'tiktok-shop-my' if lang != 'ru' else 'ozon'
    copts = ''.join(f'<option value="{k}"{" selected" if k == demo else ""}>{esc(calc_name(MARKETS[k], lang))}</option>' for k in mids)
    lopts = ''.join(f'<option value="{l}" lang="{LANGS[l]["html"]}"{" selected" if l == lang else ""}>{esc(LANGS[l]["name"])}</option>' for l in ('en', 'zh', 'ru', 'ms'))
    data = {k: {l: {'script': snippet(k, l, 'script'), 'iframe': snippet(k, l, 'iframe')} for l in ('en', 'zh', 'ru', 'ms')} for k in mids}
    cpbtn = lambda tgt: f'<button type="button" class="btn btn-secondary btn-sm" data-embed-copy="{tgt}" data-done="{esc(t["copied"])}">{ic("copy", 14)}{esc(t["copy"])}</button>'
    rows = ''.join(f'''<details class="q emb" id="{k}"><summary>{ptile(MARKETS[k]["platform"], 22)} {esc(calc_name(MARKETS[k], lang))}{ic("plus", 18)}</summary>
<div class="embrow"><pre class="code"><code id="code-{k}">{esc(snippet(k, lang))}</code></pre>
<div class="embact">{cpbtn("code-" + k)}<a class="btn btn-link" href="/{lang}/embed/{MARKETS[k]["slug"]}/" target="_blank" rel="noopener">{esc(t["preview"])} {ic("ext", 13)}</a></div></div></details>''' for k in mids)
    ul = lambda xs: '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in xs) + '</ul>'
    ol = lambda xs: '<ol>' + ''.join(f'<li>{esc(x)}</li>' for x in xs) + '</ol>'
    faq = ''.join(f'<details class="q"><summary>{esc(q)}{ic("plus", 18)}</summary><p>{esc(a)}</p></details>' for q, a in t['faq'])
    body = f'''<div class="phead"><div class="wrap">{ch}<h1 class="h-display" style="margin-top:18px">{esc(t["h1"])}</h1>
<p class="lead" style="margin-top:12px">{esc(t["lede"].format(n=len(MARKETS)))}</p></div></div>
<section class="s"><div class="wrap narrow prose embdoc">
<h2 id="why">{esc(t["why_h"])}</h2>{ul(t["why"])}
<h2 id="code">{esc(t["build_h"])}</h2>
<div class="card embbuild"><div class="g2"><div class="field"><label class="label" for="eb-calc">{esc(t["f_calc"])}</label><div class="input select"><select id="eb-calc">{copts}</select>{ic("chev", 16, "chev")}</div></div>
<div class="field"><label class="label" for="eb-lang">{esc(t["f_lang"])}</label><div class="input select"><select id="eb-lang">{lopts}</select>{ic("chev", 16, "chev")}</div></div></div>
<div class="field" style="margin-top:14px"><span class="label">{esc(t["f_mode"])}</span><div class="seg" role="radiogroup" aria-label="{esc(t["f_mode"])}">
<label><input type="radio" name="eb-mode" value="script" checked><span>{esc(t["m_script"])}</span></label><label><input type="radio" name="eb-mode" value="iframe"><span>{esc(t["m_iframe"])}</span></label></div></div>
<pre class="code"><code id="eb-out">{esc(data[demo][lang]["script"])}</code></pre><div class="embact">{cpbtn("eb-out")}</div></div>
<h2 id="how">{esc(t["how_h"])}</h2>{ol(t["how"])}
<h2 id="preview">{esc(t["demo_h"])}</h2><p>{esc(t["demo_p"])}</p></div>
<div class="wrap embdemo">{snippet(demo, lang).replace(BASE + "assets/embed.js", "/assets/embed.js")}</div>
<div class="wrap narrow prose embdoc"><h2 id="all">{esc(t["all_h"])}</h2><p>{esc(t["all_p"])}</p><div class="faq">{rows}</div>
<h2 id="terms">{esc(t["rules_h"])}</h2>{ul(t["rules"])}
<h2 id="faq">{esc(t["faq_h"])}</h2><div class="faq">{faq}</div></div></section>
<script>window.SF_EMBED={json.dumps(data, ensure_ascii=False).replace('</', '<\\/')};</script>
<script>(function(){{var D=window.SF_EMBED,c=document.getElementById('eb-calc'),l=document.getElementById('eb-lang'),o=document.getElementById('eb-out');
function upd(){{var m=document.querySelector('input[name=eb-mode]:checked').value;o.textContent=D[c.value][l.value][m]}}
[c,l].forEach(function(e){{e.addEventListener('change',upd)}});document.querySelectorAll('input[name=eb-mode]').forEach(function(e){{e.addEventListener('change',upd)}});
document.querySelectorAll('[data-embed-copy]').forEach(function(b){{b.addEventListener('click',function(){{var txt=document.getElementById(b.getAttribute('data-embed-copy')).textContent,h=b.innerHTML;
function done(){{b.textContent=b.getAttribute('data-done');setTimeout(function(){{b.innerHTML=h}},1600)}}
if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(txt).then(done);else{{var a=document.createElement('textarea');a.value=txt;document.body.appendChild(a);a.select();try{{document.execCommand('copy');done()}}catch(e){{}}a.remove()}}}})}});
if(location.hash&&/^#[a-z0-9-]+$/.test(location.hash)){{var d=document.getElementById(location.hash.slice(1));if(d&&d.tagName==='DETAILS'){{d.open=true;if(D[d.id]){{c.value=d.id;upd()}}}}}}}})();</script>'''
    app = {"@context": "https://schema.org", "@type": "WebPage", "name": t['h1'], "url": BASE + path, "inLanguage": LANGS[lang]['html']}
    w(path, page(path, lang, t['title'], t['desc'], body, [app, cld], alt=alt))

EMBED_JS = r"""/* SellerFee embed loader: https://sellerfee.app/en/embed/ */
(function () {
  'use strict';
  var me = document.currentScript, m = me && me.src.match(/^https?:\/\/[^\/]+/), origin = m ? m[0] : 'https://sellerfee.app';
  var frames = [];
  function mount(el) {
    if (el.getAttribute('data-sf-done')) return;
    var calc = (el.getAttribute('data-calc') || '').replace(/^\/+|\/+$/g, ''), lang = el.getAttribute('data-lang') || 'en';
    if (!/^[a-z0-9-]+(\/[a-z0-9-]+)?$/.test(calc)) return;
    if (!/^(en|zh|ru|ms)$/.test(lang)) lang = 'en';
    el.setAttribute('data-sf-done', '1');
    var f = document.createElement('iframe');
    f.src = origin + '/' + lang + '/embed/' + calc + '/';
    f.title = el.getAttribute('data-title') || 'Seller fee calculator by sellerfee.app';
    f.setAttribute('loading', 'lazy'); f.setAttribute('allow', 'clipboard-write');
    f.style.cssText = 'display:block;width:100%;max-width:100%;border:0;overflow:hidden;color-scheme:light;height:' + (parseInt(el.getAttribute('data-height'), 10) || 1900) + 'px';
    el.insertBefore(f, el.firstChild); frames.push(f);
  }
  window.addEventListener('message', function (e) {
    if (e.origin !== origin || !e.data || e.data.sellerfee !== 'height') return;
    for (var i = 0; i < frames.length; i++) if (frames[i].contentWindow === e.source) frames[i].style.height = Math.max(200, e.data.h | 0) + 'px';
  });
  function run() { var l = document.querySelectorAll('.sellerfee-embed[data-calc]'); for (var i = 0; i < l.length; i++) mount(l[i]); }
  run();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  window.SellerFeeEmbed = { mount: run };
})();
"""
