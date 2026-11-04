# SellerFee

Fee and profit calculators for cross-border e-commerce sellers. Static site, no framework.

## Layout
- `src/data/<platform>/<market>.json`: rate files extracted from official sources (`src/make_data.py`)
- `src/markets.py`: market registry (selectors, toggles, fee components, sources) and a Python mirror of the engine used to compute the worked examples
- `src/i18n.py`: UI strings per language (`en`, `ms`)
- `src/content.py`: page copy and guides; every figure is computed from the rate files
- `src/sf_site.py`, `src/build.py`: page shell, SEO (canonical, hreflang, OG, JSON-LD), sitemap and robots
- `assets/engine.js`: generic calculator engine driven by the market definition embedded in each page

## Build
    python3 src/build.py            # canonical origin defaults to https://sellerfee.app/

## Add a market
1. Add a rate file under `src/data/<platform>/`.
2. Add an entry to `MARKETS` in `src/markets.py` with its sources.
3. Add the page copy in `src/content.py` (`PAGE_FN`) and rebuild.

## Custom domain
`deploy/CNAME` holds `sellerfee.app`. Copy it to the repo root, or set the custom domain in the Pages settings, only once DNS points at GitHub Pages. Doing it earlier makes the github.io address redirect to a domain that doesn't resolve yet.


## Ads & affiliates
Monetization is off by default. Config lives in `src/ads_config.py` (or env vars).

1. Apply for [Google AdSense](https://www.google.com/adsense/) with site `https://sellerfee.app`.
2. After approval, rebuild with your publisher id:
   ```
   ADSENSE_CLIENT=ca-pub-xxxxxxxxxxxxxxxx python3 src/build.py
   ```
   Optionally set `ADSENSE_SLOT_INARTICLE` / `ADSENSE_SLOT_DISPLAY` for manual units, or enable Auto ads in the AdSense UI.
3. `ads.txt` is written automatically when `ADSENSE_CLIENT` is set.
4. Affiliate cards (Helium 10 / Jungle Scout) appear only when `AFFILIATE_HELIUM10` / `AFFILIATE_JUNGLESCOUT` env vars (or the URLs in `ads_config.py`) are filled.
