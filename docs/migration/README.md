# WordPress migration review

Initial import: 2026-11-24, from `skope.WordPress.2026-11-25.xml`. The export's
filename uses UTC; the local migration date is November 24 (America/Phoenix).

- 27 published pages imported, including the home page and one empty products page.
- 1 draft excluded. Attachments, navigation configuration, comments and author
  records are not published as content.
- Original export SHA-256:
  `1a1693c05190ee1df94524e201ccc10c28556ab8967ef2e5b92b66641df944ff`.
- One invalid vertical-tab byte was replaced with a space in memory for XML
  parsing. The original file remains unchanged and ignored by Git.
- Canonical URLs follow descriptive link labels; original published paths remain
  as Hugo aliases. Pages normalizes directory paths to trailing slashes. Internal
  links use Hugo helpers for subpath support.
- 45 media paths were referenced. 43 files were recovered from the live WordPress
  site; their content hashes and source URLs are in `media.json`.
- Two unavailable source files returned 404. The redundant September 2021
  screenshot was removed while retaining the adjacent November screenshot.
  The missing article download now links to its cited DOI. `review.json`
  records these and three mechanical link repairs.

`wordpress-import.json` records published-page paths/IDs, exclusions and source
references without copying draft bodies or administrative records. `review.json`
records deliberate edits after import; a re-import must reapply those reviewed
changes. The importer excludes password-protected entries and refuses a nonempty destination. Routine builds never read
or overwrite the WordPress export and never fetch WordPress media.

Imported HTML is intentionally retained inside Markdown files to avoid lossy
conversion of figures, tables, anchors and scientific prose. Gutenberg comments
and generated srcsets are removed; local images replace WordPress-hosted media.
Historical statements, old prototype pages, affiliations and release dates are
preserved for editorial review. They do not establish current application state.
External links have not all been checked or endorsed. No PHP is copied or run.

## Cutover

The old WordPress system has a reported unpatched PHP vulnerability. Prioritize
removing its public exposure. DNS cutover alone does not disable the old origin:
its operator must stop the WordPress/PHP virtual host or block public access,
including legacy hostnames and direct-origin routes. Preserve any required backup
privately; do not publish the raw export as an emergency backup.

The static replacement can be reviewed locally before enabling GitHub Pages.
`www.openskope.org` is the canonical domain; leave `app.openskope.org` unchanged.
See the README for Pages activation, DNS and TLS checks. No live cutover or origin
shutdown is implied by a successful local build.

## Navigation review

The main menu has four entry points (Use SKOPE, Data & tools, Research, About)
plus the application link. Docsy's `toc_hide` keeps individual imported pages out
of the global sidebar without excluding them from search. Entry pages link to
related content; About links to the news/history collection, including prototype
announcements, retired guides and development meetings. The home page reuses the
main menu instead of enumerating every imported page. Original WordPress URLs remain accessible through aliases; canonical
URLs use descriptive slugs recorded in `review.json`. Editorial changes are recorded in `review.json`.

## Existing visual identity

The shared navbar uses the original unlettered climate-trace background
`wp-content/uploads/2018/05/AltHeaderv3.png`, with live Bitter lettering and
the selected Source Sans 3 interface text shared with SKOPE UI. It replaces the separate
home hero. An 80px header on larger screens combines branding, thin navigation
and search; smaller screens use a Menu control. Header/sidebar offsets follow
the chosen height. The original lettered header and WordPress icon remain local.
`branding.json` records image sources; `media.json` records image checksums.
See [self-hosted fonts](../../static/fonts/README.md) for WOFF2 sources, licenses,
checksums, subset loading, preloads and font maintenance. Pixelation is not a
default typographic treatment. The home introduction keeps its wider two-column
layout on large screens and a single column on smaller screens.

## Canonical routes and legacy aliases

Use descriptive slugs matching the page's link label. The main navigation is
`/use-skope/`, `/data-tools/`, `/research/` and `/about/`. Other pages use similarly
readable topic slugs, including `/users-guide/`, `/team/` and `/paleocar/`.
`review.json` records the complete old-to-new mapping. Each renamed page declares
its original WordPress path in front matter `aliases`; Hugo emits redirect pages
at those old paths. `make site-check` verifies both canonical pages and alias
targets, including the deployment prefix. These are static HTML redirects on
GitHub Pages, not server-configured HTTP 301 responses.
