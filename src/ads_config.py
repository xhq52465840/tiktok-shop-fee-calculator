"""Monetization flags for SellerFee.

Fill these AFTER Google AdSense (and any affiliate programs) approve you.
Until ADSENSE_CLIENT is set, ad slots stay in the HTML as empty hidden placeholders
so pages never show broken ads, and no Google ads script is loaded.

Enable at build time either by editing the defaults below, or with env vars:
  ADSENSE_CLIENT=ca-pub-xxxxxxxxxxxxxxxx python3 src/build.py
  ADSENSE_SLOT_INARTICLE=1234567890 ADSENSE_SLOT_DISPLAY=0987654321 ...
"""
import os

# AdSense publisher client id, e.g. "ca-pub-1234567890123456". Empty = ads off.
ADSENSE_CLIENT = os.environ.get('ADSENSE_CLIENT', '').strip()

# Optional unit slot IDs from AdSense → Ads → By ad unit (digits only).
# Leave empty to rely on Auto ads only (still needs ADSENSE_CLIENT + Auto ads enabled).
ADSENSE_SLOT_INARTICLE = os.environ.get('ADSENSE_SLOT_INARTICLE', '').strip()
ADSENSE_SLOT_DISPLAY = os.environ.get('ADSENSE_SLOT_DISPLAY', '').strip()

# Auto ads: when True and ADSENSE_CLIENT is set, AdSense may place ads site-wide.
# Turn on Auto ads in the AdSense UI as well; this only loads the client script.
ADSENSE_AUTO_ADS = os.environ.get('ADSENSE_AUTO_ADS', '1').strip() not in ('0', 'false', 'False')

# Affiliate destinations. Empty url = that tool is omitted from the page.
# After you join a program, put your tracked link here and rebuild.
AFFILIATES = [
    {
        'id': 'helium10',
        'name': 'Helium 10',
        'blurb': {
            'en': 'Product research and TikTok Shop / Amazon seller toolkit.',
            'zh': '选品与 TikTok Shop / Amazon 卖家工具套件。',
            'ru': 'Исследование товаров и инструменты для TikTok Shop / Amazon.',
            'ms': 'Penyelidikan produk dan alat penjual TikTok Shop / Amazon.',
        },
        'url': os.environ.get('AFFILIATE_HELIUM10', '').strip(),
    },
    {
        'id': 'junglescout',
        'name': 'Jungle Scout',
        'blurb': {
            'en': 'Amazon product research and opportunity finder.',
            'zh': 'Amazon 选品与机会发现工具。',
            'ru': 'Исследование товаров и поиск ниш на Amazon.',
            'ms': 'Penyelidikan produk dan pencari peluang Amazon.',
        },
        'url': os.environ.get('AFFILIATE_JUNGLESCOUT', '').strip(),
    },
]

def ads_enabled():
    return bool(ADSENSE_CLIENT)

def active_affiliates():
    return [a for a in AFFILIATES if a.get('url')]
