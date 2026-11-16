# Editorial modification dates

`content_dates.json` is a reviewed per-URL record. `modified` is the date that
primary page content actually changed, in UTC+8. `source_commit` identifies the
historical main-branch commit supporting the baseline date. It is independent
of `markets.VERIFIED`, which remains the marketplace rate/source verification
date (26 October 2026); no fee or source-verification claim changes here.

The baseline was reconstructed on 16 November 2026 from the actual first-parent
Git history through `2772c122f092dba73de0896cbd0ff90bb56583a5`:

- Calculator/guide pages: compare primary article text plus headline/lede.
- Other pages: compare main-content text.
- Ignore scripts, styles, icons, advertising placeholders, bylines and guide-card
  dates. A sitewide navigation/banner/ad change alone does not make every article
  newly modified. Preserve the historical date when the primary content is equal.
- The two Chinese Malaysia calculators and Chinese homepage genuinely changed
  on 14 November. The existing Malaysia guides did not gain new article text in
  that release; their dates must not be changed to 14 November for a banner edit.

These records establish modification dates, not proof of the first date a page
was publicly available. The previous `datePublished = VERIFIED` was unsupported
and is removed; an actual first-publication date may be added only with evidence.

For future substantive edits, review and update only the affected URL records
and record the supporting commit/change in the PR. Do not set all pages to the
build date or move the rate-verification date. If a new page has no established
date, the builder omits its `lastmod`/`dateModified` rather than guessing. The
current regression check requires complete coverage of the established pages.

The localized visible content-update date, JSON-LD `dateModified`, guide-card
date and sitemap `lastmod` all use this one registry. Source blocks and verified
badges deliberately continue to show the independent `VERIFIED` value.
