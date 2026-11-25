# Hugo and Docsy cleanup review

Reviewed 2026-11-25 against the pinned Hugo/Docsy setup. These are maintenance
priorities, not unresolved production failures. Preserve authored wording,
publication metadata, page/fragment URLs and archived image originals throughout.

## Completed

- Markdown headings feed Hugo's native `TableOfContents` at levels 2–4. The
  rendered-HTML heading parser and content adapter are unnecessary and removed.
- Plain paragraphs and flat lists use Markdown. Internal content links use
  `relref`; archived media URLs use `siteurl`/`relURL`.
- Launch/guide actions share one partial and thin content shortcode. Menu and
  guide-page metadata supply their labels and destinations.
- Project styles use Docsy's supported `_variables_project.scss` and
  `_styles_project.scss` entry points. Duplicate navbar breakpoint declarations
  and an unused guide-icon rule were removed.
- No `style=` attributes remain in `content/` or the site-owned templates.
  HTML in templates is normal; the remaining content markup needs selective
  replacement, not a blanket ban on HTML or `safeHTML`.

## Completed follow-ups, in requested order

1. **Centralized all 18 figures.** Content now calls `skope-figure` with image,
   caption, alignment and optional original-link parameters. Captions use inline
   Markdown. Both figure and inline-image shortcodes call `skope/image.html`,
   preserving the existing dimensions, responsive derivatives, loading behavior
   and archived media URLs. Inline icons remain inline.

2. **Converted the environmental resource catalog.** Native Markdown definition
   lists and links replace strong-label/raw-anchor blocks. Labels, descriptions
   and historical destinations (including mismatches) are retained. Links use
   ordinary Markdown navigation; the catalog remains one authored source.

3. **Simplified the archives.** The 2015 workshop and 2017 meeting now use Markdown
   emphasis, nested lists and intentional line breaks instead of formatting spans
   and raw lists. Participants, dates, wording and existing anchors are retained.
   The same list conversion handles the 2022 release's nested feature list.
   No agenda-specific shortcode or data duplication was introduced. The user's
   simplified landing-page May 2022 announcement is preserved.

## Lower-priority opportunities and boundaries

- `fonts.html` and `hooks/head-end.html` emit the only two site-owned style
  blocks: data-generated `@font-face` declarations and the URL-aware navbar
  background. A fingerprinted Hugo Pipes stylesheet could make these cacheable
  across pages. Preserve font preloads, subpath URLs and initial rendering;
  neither block duplicates authored page CSS today.
- Use/Research layout wrappers contain Markdown and have no inline CSS. Extract
  a named, narrowly scoped component when this layout recurs. Do not introduce
  nested generic wrappers that hide headings from Hugo's native outline.
- Keep the small Docsy shell and TOC overrides under review on theme upgrades.
  Their landmark labels and outline validation are deliberate. Continue calling
  upstream chrome/content partials rather than copying theme implementation.
- JSON front matter is supported Hugo input and preserves the import metadata;
  converting it to YAML/TOML alone would be cosmetic churn.
- Docsy's landing-page `blocks/*` shortcodes have their own layout conventions.
  Use them where those conventions fit; do not force them into reading pages
  solely to remove a few structural HTML tags.

Reference: [Docsy project styles](https://www.docsy.dev/docs/content/lookandfeel/),
[Docsy navigation](https://www.docsy.dev/docs/content/navigation/),
[Docsy shortcodes](https://www.docsy.dev/docs/content/shortcodes/), and
[Hugo shortcode notation](https://gohugo.io/content-management/shortcodes/).
