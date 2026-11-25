# Self-hosted site fonts

The website and SKOPE UI use Bitter 700 for SKOPE branding and Source Sans 3
300–700 for interface/content, including real italic text. Bitter retains the
staging header identity; Source Sans 3 replaces Roboto by explicit design choice.
The site serves local WOFF2 files through Hugo's fingerprint pipeline.

`data/fonts.json` records versioned upstream URLs, Unicode ranges and SHA-256
checksums. This directory retains each family's unmodified SIL Open Font License.
Font declarations are in `layouts/partials/fonts.html`; Hugo resolves their URLs
for root/subpath builds. Source Sans 3's Latin/Latin Extended subsets load by
Unicode range. Only the two normal Latin faces used immediately are preloaded.
All faces use `font-display: swap` with fallback fonts; italic/extended faces load
on demand. Content-hashed filenames invalidate caches when font bytes change.
Regular builds use committed files and make no Google Fonts or WordPress calls.

Run `make deps-fonts` to restore pinned files with checksum verification. For a
reviewed upstream change, edit source URLs/metadata in `data/fonts.json`, run
`make deps-fonts FONT_UPDATE_LOCK=1`, and review binary/checksum/license changes.
Do not enable hash updates during normal builds. `make site-check` verifies font
sources, published files and licenses. Coordinate the same set with SKOPE UI's
`app/fonts.lock.json`; its restore command is `make fonts`.

Font version bumps are operator-led. Prioritize useful glyph/rendering fixes or
security advisories, and review branding, genuine italic text, wrapping, header
fit, mobile layout, search and font network requests before deployment.
