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

## Impeccable remediation and follow-up audit — 2026-11-25

Addressed the seven findings in harden, adapt, optimize and polish order. Escaped
URL-label colons to prevent nested anchors; repaired heading ranks and the
workshop agenda list; added descriptive image alternatives; gave Docsy regions
distinct landmarks and added a keyboard skip link. Navbar offsets follow its
actual rendered height, with a normal-flow fallback when JavaScript is disabled.
Images use intrinsic dimensions, responsive WebP variants and below-fold lazy
loading through `legacy-image`. All archived originals remain published.

The container-based full check passed three dependency-tool tests and 17 Python
tests. New semantic regressions cover nested/unnamed anchors, skipped headings,
invalid list nesting, duplicate main landmarks and missing image dimensions,
while allowing non-interactive named anchors. Root and `/preview/` renders each
passed all 50 HTML-file checks, 27 imported routes, 46 original media checksums,
responsive-image URLs and existing aliases, with zero local-link/anchor errors.

Axe-core 4.10.3 returned zero violations on all 31 non-redirect pages in both
builds. Each page fit at 320, 360 and 768 CSS pixels. At 768px and 200% root text
size, the navbar measured 243px and the home heading started at 307px after its
resize observer settled. With JavaScript disabled, the heading started at 355px,
below the same 243px header. Keyboard Tab/Enter reached the visible skip link and
focused `td-main-content`. Synthesized touch opened the mobile menu. No browser
runtime errors were observed.

Measured initial decoded resource bodies fell from 2,961,135 to 1,027,895 bytes
on the current guide (65.3%) and from 4,475,626 to 1,146,418 bytes on the prototype
guide (74.4%). These are local-browser resource measurements, not compressed
GitHub Pages transfers or field Core Web Vitals. Hugo generated 93 image variants.
Desktop/mobile and enlarged-text screenshots were reviewed, along with a web
derivative of a screenshot containing small spreadsheet labels.

Narrative text, existing href destinations and publication metadata were compared
with committed sources and preserved. Citation presentation and metadata remain
unchanged. The app's existing staged bundle changes were left intact.
Browser evidence and runners are in ignored `tmp/impeccable-audit/`; audit reports
are in `.impeccable/audit/`. Physical devices, screen readers and a full
cross-browser zoom matrix remain untested. No WCAG certification, commit, push
or deployment is implied by these local checks.

## Use SKOPE refinement and root citation — 2026-11-25

The Use SKOPE page now leads with the launch action and an existing guide
illustration, followed by four direct guide-section links. The original dated
release paragraph is retained under Release history. Current-guide labels and
the guide title use SKOPE User Guide; published routes, fragment IDs and aliases
are unchanged. Original import metadata and prototype titles remain historical
records. The canonical application CFF now has a regular root copy for GitHub;
`make citation-sync` refreshes it and build/site checks reject drift.

The full container check passed 18 Python tests, three dependency-tool tests and
all 50 rendered HTML files. Root and `/preview/` site checks passed, including
responsive-image URLs and existing aliases. Chromium checked the refreshed page
at 320, 360, 768, 1100, 1440 and 1920 pixels and at 200% text size: no horizontal
overflow, no header overlap, a 50px launch target and a loaded illustration.
The page's axe scan returned no violations. A subpath guide shortcut navigated
to the visible Select Area section, and the guide H1 read SKOPE User Guide.
No browser runtime errors were observed. Screenshots and the runner are in
ignored `tmp/use-skope-review/`. GitHub citation discovery itself awaits a commit
on the default branch; no push or deployment was performed.

## Research page refinement — 2026-11-25

Research now shares its resource-page lead and Launch SKOPE button styling with
Use SKOPE. Publications and Presentations are grouped as research outputs;
YesWorkflow and the existing related pages remain. The launch action points to
the current application. Prototype access remains through the existing Project
news and history archive. Published page routes and aliases are unchanged.

The full check passed 18 Python tests, three maintenance tests and 50 rendered
HTML files. Root and `/preview/` site checks passed with zero link or anchor
errors. Chromium checked Research and Use SKOPE at 320, 360, 768, 1100, 1440 and
1920 pixels: no overflow or header overlap; both launch buttons measured 50px.
Axe returned no violations for either page. Research also fit at 200% root text
size. Browser navigation confirmed the current application URL and the path from
Related pages through Project news and history to the prototype overview.
Desktop/mobile screenshots were reviewed; no runtime page errors were observed.
Evidence is in ignored `tmp/research-review/`. Changes remain local.

## Hugo components and Markdown pass — 2026-11-25

Section headings now use Markdown with explicit attributes for existing anchors.
Hugo's native TableOfContents replaces the rendered-HTML outline parser and
Docsy content adapter. Structural wrappers use blank lines around Markdown so
Hugo sees all sections, including the User Guide link on Use SKOPE. The outline
coverage guard compares every rendered level 2–4 heading with the page outline.

The launch/guide action partial centralizes markup, icon, external-link behavior
and button classes; templates and the content shortcode share it. Labels and
URLs come from the launch menu entry and guide page. Home, Use SKOPE, Research
and the navbar use this renderer. Navbar expansion accommodates the common
button dimensions.

Ordinary paragraphs, links and flat lists now use Markdown. Figures, tables,
anchored paragraphs, nested historical lists, layout wrappers and links requiring
special attributes retain HTML. Compared with the committed source, 118 plain
paragraph wrappers and all raw section-heading tags were removed. Original media
shortcodes and accessibility repairs remain in place. A before/after comparison
of rendered content bodies verified all destinations and existing anchors, and
matched prose after normalizing Hugo's smart punctuation and the repaired
FedData package emphasis. Published paths, aliases and citation presentation
remain unchanged.

Docker/Make validation in the isolated checkout passed: 21 Python tests, 3 Node
maintenance tests, 50 HTML pages, 27 imported routes and 46 archived media files;
no errors or anchor warnings. Browser evidence is kept in ignored
`tmp/hugo-review/`.

Chromium audited all 31 non-redirect pages with zero axe violations, responsive
failures or runtime errors. Root checks covered Home, Research and Use SKOPE at
320, 360, 768, 1100, 1200, 1399, 1400, 1440 and 1920px; keyboard skip navigation,
touch-menu expansion, no-JavaScript layout and 200% text also passed. Native
outlines matched headings on Use SKOPE, Research and the User Guide. Clicking
the guide outline entry left its heading visible below the navbar. A `/preview/`
build/site check and targeted mobile/desktop browser checks passed, including
current-app and historical-prototype navigation. The final Docsy review and
prioritized follow-ups are in `docs/hugo-content-review.md`.

## Figures, catalog and archive conversion — 2026-11-25

Completed the three follow-ups in order. All 18 figure wrappers now use
`skope-figure`; its Markdown captions and optional original-image links share the
same image pipeline as `legacy-image` inline icons. The catalog's 25 entries use
Markdown definition lists and links. Both workshop/meeting archives use Markdown
emphasis, nested lists and explicit line breaks, as does the release feature list.
The user's edited landing-page May 2022 announcement is byte-for-byte retained.

Compared every rendered content body with a fresh pre-change root build:
wording, link destinations and existing anchors match after whitespace
normalization. The 10:00 meeting break is separated from its preceding item.
All 44 rendered images preserve source, srcset, sizes, alt text, dimensions and
loading/decoding attributes. No archived original media or published route changed.
The catalog's historical URL/label mismatches remain intact; its Markdown links
use normal same-tab navigation.

Docker/Make checks passed: 22 Python tests (including figure captions, original
links, subpath URLs, responsive output and inline-icon behavior), 3 Node tests,
50 HTML pages, 27 imported routes and 46 archived media files. Root and
`/preview/` render/site checks report no errors or anchor warnings. Chromium's
31-page root audit reports zero axe violations, responsive failures or runtime
errors. Skip navigation, touch navigation, no-JavaScript rendering and 200% text
checks also pass. Focused desktop/mobile checks cover all 18 figures, the catalog
and archives; screenshots and runner evidence are in ignored
`tmp/content-components-review/`. Desktop/mobile screenshots were visually reviewed.
The final `/preview/` browser pass also passed all 18 mobile/desktop viewport
checks across the nine affected pages, with all 18 figures, 25 catalog entries,
zero axe violations and no runtime errors.
