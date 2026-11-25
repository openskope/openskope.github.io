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

## Footer and styling centralization — 2026-11-25

The footer hover background is now a shared token (`#4a7171`); white action text
has 5.40:1 hover contrast (4.52:1 on the unchanged normal background). Website
builds and preview startup validate the shared bundle before Hugo runs.
Rendered checks require one shared footer and its fingerprinted stylesheet on
every non-redirect page, shared acknowledgments/actions and matching policy/CFF
content. GitHub Pages uses these checks through the existing Make targets.

Shared font stacks feed website typography; site colors reuse the existing Sass
palette. Inline styles in ten content files were replaced with theme/utility
classes and image width attributes. A comparison against committed sources
confirmed that authored text and link/media destinations are unchanged.
`review.json` records the presentation changes.

Validation used an isolated checkout under `/tmp/openskope-footer-review`, with
Compose project `openskope-footer-review`, while the existing preview continued
running. Production root and `/preview/` builds passed: 50 HTML files, all 27
imported routes, 46 archived media files, zero internal-link/anchor errors.
All three dependency-tool tests and 15 Python tests passed, including corrupt
bundle, low-contrast hover, missing token, empty citation field and missing or
duplicate rendered-footer cases. The Impeccable source detector returned no
findings for the changed files.

Headless Chromium checks passed at widths 360, 600, 768, 1024, 1200, 1440 and
1920: responsive layout, mobile Menu, search and actual custom-font rendering.
Home, guide, citation and terms footers passed at 360, 768, 1440 and 1920 on both
root and subpath builds. Computed hover colors and the 3px keyboard-focus outline
passed, as did citation downloads; no browser errors or failed asset requests
were observed. Desktop home and mobile footer screenshots were visually reviewed.
The runner, screenshots and JSON results are in ignored
`tmp/browser/centralization/`.

This validation preceded the website commit and app bundle update. Follow
`docs/footer.md` to import the reviewed website commit and run the app checks.
No push or deployment was performed for this validation.
