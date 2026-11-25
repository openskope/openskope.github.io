# OpenSKOPE website

Hugo/Docsy site for **www.openskope.org**, seeded from the existing WordPress
export. The SKOPE application remains a separate service at
<https://app.openskope.org>.

## Local development

Install Git, Make, Docker and Docker Compose. Run from the repository root:

```sh
make serve
# http://localhost:1313
make stop
```

Use `make logs` to inspect Hugo output and `make status` to check the preview.
The Makefile exports the pinned `HUGO_VERSION` for every Compose command. A bare
`docker compose logs` or a Compose UI may report that this variable is missing
even while Hugo is running; use the Make targets to inspect the service.

Use `make serve PREVIEW_PORT=1314` if another site uses port 1313. Source is mounted
into the toolchain image; rebuilding the image does not bake in site content.
`make serve` rebuilds and renews the dependency volume. Project tools run inside
the container; no host Hugo, Go, Node, npm or Python installation is required.

```sh
make render                    # production export in public/
make check                     # render, dependency/import tests, local link/media checks
make web-assets-check          # shared content, token and footer contrast validation
make toolchain-status          # installed tools and dependencies
make shell                     # container shell
```

Stop this project's preview before `make render` or `make check`; the render
checks for a running preview before clearing shared output. In a separate checkout,
use a distinct Compose project, for example `make check COMPOSE_PROJECT_NAME=openskope-review`.
For a subpath check:

```sh
make render RENDER_BASE_URL=https://example.org/preview/
make site-check RENDER_BASE_URL=https://example.org/preview/
make render
```

The interface follows Making Models FAIR and OMF: `HUGO_VERSION` plus the
Dockerfile image digest pin Hugo; `go.mod` pins Docsy; npm supplies Bootstrap,
Font Awesome and embedded Dart Sass. Self-hosted [Bitter and Source Sans 3 fonts](static/fonts/README.md)
are shared with the SKOPE UI changes; font refreshes use `make deps-fonts`. See [dependency upgrades](docs/dependency-upgrades.md)
and [agent guidance](AGENTS.md). OpenSKOPE omits their bibliography/catalog tooling.

## Shared content and styling

This repository owns `shared/web/`: reusable footer content, CSS/tokens,
application terms and canonical application citation metadata. Hugo renders it
directly; `/cite-skope/` and `/terms-of-use/` publish that content. SKOPE UI consumes
a commit-pinned bundle and retains its application behavior and consent flow.
Builds use local verified files with no reverse dependency on the app. See
[shared web maintenance](docs/footer.md) for updates and validation.
The source/build link identifies this website's Git revision; tracked local edits
add `-dirty` to the build label.

Content images use the `legacy-image` shortcode, which supplies intrinsic
dimensions and generates responsive WebP variants through Hugo. Original media
stays at its archived `wp-content/uploads/` URL. Use descriptive `alt` text and
set `eager=true` only for an image near the start of the page; other images load
lazily. Do not edit generated variants in `public/` or `resources/_gen/`.

Keep semantic heading levels sequential below each page's H1. Author/date
metadata belongs in paragraphs. For a literal URL label inside an imported HTML
anchor, encode its colon as `&#58;` so Goldmark does not generate a nested link;
this preserves the displayed text and destination. `make site-check` checks
rendered semantics, image dimensions and all responsive-image URLs.

The small `layouts/docs/baseof.html` override gives Docsy's main and sidebar
regions unique landmarks. It retains upstream chrome partials; review it when
upgrading Docsy. Header offsets track the rendered navbar height, including
enlarged text; without JavaScript, the header stays in normal document flow.

## Content and migration

See the [Hugo/Docsy cleanup review](docs/hugo-content-review.md) for remaining
component opportunities and the recommended order.

Edit `content/`. Prefer Markdown for headings, paragraphs, lists, emphasis and
links. Use explicit heading attributes (`{#existing-anchor}`) when an anchor must
stay stable. Use `skope-figure` for captioned/standalone illustrations and `legacy-image`
for inline icons. Retain HTML for tables, anchored paragraphs, structural
layout wrappers and links whose attributes carry behavior. Separate structural
HTML and Markdown with blank lines, without indenting prose as code.

Figures share the image pipeline (dimensions, responsive WebP variants and lazy
loading) with inline icons. Captions support inline Markdown:

```go-html-template
{{< skope-figure src="wp-content/uploads/2021/11/Header.png" alt="SKOPE application header." caption="**SKOPE Header**" >}}
```

Optional `width`, `align` (`left`, `right`, `center`), `class`, `image-class`,
`link` and `eager=true` parameters control display without duplicating HTML.
Keep archived media in place; `link` can point to an original image URL.

“On this page” uses Hugo's native `TableOfContents` for headings at levels 2–4.
Keep headings in Markdown so they appear automatically; do not duplicate a list
of section links. `notoc: true` deliberately disables this outline; `toc_hide`
controls the separate left sidebar catalog.

Launch and guide buttons share `layouts/partials/skope/action.html` and the
`skope/actions.html` group. Templates call the partial; content uses
`{{< skope-actions >}}` (or `items="launch"` / `items="guide"`). The launch label
and destination come from the `launch-skope` menu item; the guide label and URL
come from its page. Styling lives in `.skope-action` and `.skope-actions`. Use descriptive URL slugs matching link labels, and retain original WordPress
paths as front matter aliases when renaming pages. See [migration review](docs/migration/README.md).

The original XML remains local and is ignored by Git: it includes unpublished
and administrative data. **Never put it in `static/` or publish it.** Routine
builds do not read the export or fetch WordPress media.

```sh
make import-wordpress IMPORT_OUTPUT=/src/tmp/wordpress-review
# Review tmp/wordpress-review on the host before copying into source.
```

Set `WORDPRESS_EXPORT=/src/other-export.xml` for another export. The importer
refuses nonempty output directories. `make media-fetch` is an explicit network
operation which writes the referenced media and their checksums; review changes.
The initial lock/workspace can be regenerated with `make bootstrap` if starting
from manifests without those files; ordinary clones already contain both and
should use `make build`.

## GitHub Pages

Source repository: <https://github.com/openskope/openskope.github.io> (private).
To activate Pages after reviewing and committing the source:

1. Review the local changes and migration report, then commit and push to `main`
   to seed the repository. Builds validate and upload an artifact; deployment
   stays disabled until the `PAGES_ENABLED` repository variable is set to `true`.
2. After that first push, in **Settings → Pages**, choose **GitHub Actions** as
   the source. This avoids requiring Pages configuration before content exists.
3. Configure the custom domain as `www.openskope.org`, verify domain ownership,
   and follow GitHub's current DNS instructions. `static/CNAME` records the intended
   domain; it does not configure repository settings or DNS.
4. Confirm TLS and HTTPS enforcement before switching traffic from WordPress.
   Keep a private backup for comparison; isolate the vulnerable WordPress/PHP
   origin promptly and do not restore it as a public rollback target.
5. When ready for publication, add repository Actions variable `PAGES_ENABLED`
   with value `true` under **Settings → Secrets and variables → Actions → Variables**.
   Run **Actions → Build and deploy to GitHub Pages → Run workflow** on `main`.
   Subsequent successful pushes to `main` publish automatically. Feature-branch
   PRs and manual dispatches on feature branches cannot deploy. Clear the variable to suspend new
   deployments; this does not remove an already published site.
6. Enable repository security monitoring and personal notification delivery using
   the [dependency runbook](docs/dependency-upgrades.md).

Do not repoint `app.openskope.org`. This repository publishes the information and
documentation site only. Before cutover, review unresolved legacy references and
historical statements, compare key pages, navigation and search on desktop/mobile,
and verify media/downloads. No GitHub repository, DNS or live site is changed by
local initialization.

For recovery, redeploy the last accepted source commit through the same workflow;
retain a previous Pages artifact before publication. Application/database recovery
belongs to the separate SKOPE deployment. Reverting this static site does not
recover or roll back application data.
