# Local validation

Validated on 2026-11-24 for `https://www.openskope.org/`. Validation used local builds and previews; no push or deployment was performed.

- Initial `make check` passed the container build, three dependency-tool tests,
  seven importer tests, render and rendered-site checks. Hugo v0.170.1, Docsy
  v0.18.1, Bootstrap 5.3.9 and embedded Dart Sass 1.108.2.
- After navigation, branding, layout and URL changes, production and `/preview/`
  renders and site checks passed: 48 HTML files, including 19 legacy redirects;
  all 27 imported WordPress addresses remain available; 46 archived media files;
  two unavailable source references retired with documented replacements; zero
  broken internal links or anchor warnings.
- Canonical navigation routes are `/use-skope/`, `/data-tools/`, `/research/` and
  `/about/`. Original WordPress aliases and their canonical targets are verified
  by `make site-check`; `review.json` records the complete mapping.
- Final browser checks passed search, guide images, the responsive Menu control,
  home/guide mobile layout, and zero console/HTTP asset errors. At widths 360,
  600, 768, 1024, 1200, 1440 and 1920 pixels, branding stays within the compact
  shared navbar, content stays below it, and widescreens use two columns.
- There is no separate hero. The shared navbar uses the unchanged original
  unlettered `AltHeaderv3.png` trace with live Bitter wordmark/subtitle text.
  Body and controls use Source Sans 3, as selected for both website and SKOPE UI.
- Font source/output/license checksums passed. Chrome's rendered-font inspection
  confirmed both custom fonts; exactly two font preloads; `font-display: swap`;
  no Google Fonts requests. All font files/licenses are local. Subpath font/link
  checks and all 19 legacy redirects passed.
- SKOPE UI received the same five faces/checksums, offline build/typecheck font
  verification, font refresh tooling and Vuetify typography settings. Its full
  type check/test suite and deployable staging-image build passed. The isolated
  local production preview at port 3001 confirmed real custom-font rendering,
  two preloads, no Google Fonts requests, HTTP 200 font/license responses and
  `public, max-age=31536000, immutable` caching for hashed WOFF2 files.
- Browser screenshots and the runner are local evidence in ignored `tmp/browser/`.
  The original XML remains unchanged and excluded from Git/public output.

GitHub CI, Pages deployment, DNS/TLS and old-origin shutdown remain separate
operations. Historical external links and editorial claims are not all reviewed.
See the migration README and review record for source limitations and deliberate
content/navigation changes.

## Shared footer and provenance review — 2026-11-25

The citation and terms pages bring the current render to 50 HTML files, including
19 legacy redirects. Root and `/preview/` builds retain all 27 imported routes,
46 archived media files and zero internal-link errors or anchor warnings.
The original XML checksum remains unchanged; it remains private and ignored.
Homepage testing/feedback and release passages and the Research hub's original
links were restored from that export. Migration edits are recorded in `review.json`.

The website owns the five-file `shared/web/` bundle. The app imports a full Git
revision and verifies local checksums; its root CFF matches the imported CFF.
The app's 531 existing tests, bundle tests, type checks and production-image build
passed. Browser checks compared footer text and computed styling at 360, 768,
1440 and 1920 pixels and verified citation content, acceptance persistence,
decline behavior and first-visit consent. Citation/CFF downloads and shared
footer links also passed the website's root/subpath browser checks.
