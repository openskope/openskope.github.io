# OpenSKOPE agent guidance

## Scope and decision hierarchy

This repository builds www.openskope.org. Follow the user's request, then the
README, Hugo configuration and authoritative sources, then this file. Keep changes
focused; preserve scientific meaning, publication metadata and published URLs.
Mention unrelated issues without fixing them unless requested. Canonical URLs
should match link labels in slug form; retain legacy WordPress paths as aliases.

## Authoritative sources

- `hugo.yaml`: configuration, menus, theme import and supported Hugo minimum
- `content/`: reviewed site content; imported HTML within Markdown is intentional
- `static/`: local media and custom-domain declaration
- `go.mod` / `go.sum`: exact Docsy module
- `HUGO_VERSION` and `Dockerfile`: matching Hugo version and official image digest
- `package.json` / `package-lock.json`: frontend and Sass dependencies
- `packages/hugoautogen/`: generated workspace; regenerate with `make deps-pack`
- `docs/migration/`: source checksum, page/media mapping and import review evidence
- `data/fonts.json`, `assets/fonts/`, `static/fonts/`: pinned webfonts and licenses
- `shared/web/`: authoritative shared footer content, CSS and tokens; see [maintenance](docs/footer.md)
- `scripts/`, `Makefile`, `docker-compose.yml`: import, validation and container interface

The original WordPress XML is private migration input, ignored by Git, and must
remain unchanged. Import only published pages/posts: drafts, comments, author
records and WordPress configuration must not enter the public site. Do not copy
WordPress PHP or execute imported scripts. Re-import into a separate directory;
never overwrite reviewed content as part of routine builds.

## Invariants

- Run builds, imports, tests and dependency commands in the container via Make.
- Treat the Docker image as the toolchain; supply source through the Compose mount.
- Edit source, then regenerate; never hand-edit `public/`, `resources/_gen/`,
  `node_modules/`, lockfile entries or Hugo workspace metadata.
- Keep theme changes in targeted `layouts/` and `assets/scss/` overrides. Do not
  vendor Docsy or copy large upstream template blocks.
- Preserve subpath support with Hugo URL helpers and the `siteurl` shortcode.
- Retain `static -> static` if adding module mounts.
- Keep credentials, analytics keys and private export data out of commits and logs.
- Do not rewrite historical claims as current facts. Record uncertain source
  links, dated statements and unavailable media for human review.

## Shared content and styling

- The static website owns reusable, shareable project content and styling in
  `shared/web/`: acknowledgments, citation guidance/metadata, terms, and shared
  design tokens and CSS. Keep one editable source; do not maintain competing
  copies in the app. See [shared footer maintenance](docs/footer.md).
- `skopeui` consumes reviewed bundles pinned to full Git commit SHAs, with local
  checksums. Normal builds and browser rendering use local files, not a moving
  branch, the live website, or another repository's build output.
- The app owns application behavior: state, data interaction, dialogs, and consent
  enforcement. Share content and styles without coupling Vue/Vuetify to Hugo/Docsy.
- Keep dependencies one-way: website source to app bundle. This website must not
  import app source or require an app build to render its shared content.
- Update shared sources here, validate, commit, then advance the app's bundle pin
  through review. Adding shared files requires an explicit bundle-contract update.

## Navigation

Keep the main menu thin: Use SKOPE, Data & tools, Research and About, plus the
application link. Individual pages are linked through those entry points and
search; use Docsy `toc_hide` to avoid a flat global catalog. Aggregate prototype
announcements and documentation through `content/news/`, retaining historical
context and published URLs. The home page reuses the main menu.

## Maintenance and validation

Follow [dependency upgrades](docs/dependency-upgrades.md) and the README. Choose
latest stable mutually compatible releases within scope, keep intentional exact
pins, and update Hugo's version/digest/minimum together. Use `make deps-docsy`,
`make deps-pack`, `make deps-lock` in the documented order.

For content, inspect affected pages and links. For import logic, run
`make content-test`. For layouts, dependencies and publishing, run `make check`,
then render once with a subpath `RENDER_BASE_URL` and run `make site-check`.
Review the home page, guide, media/downloads, search, navigation and mobile layout.
Never run `make render` during this Compose project's preview: stop it or use a
separate checkout. See README for port selection and recovery.

## Publication and questions

With repository Actions variable `PAGES_ENABLED=true`, pushes/merges to `main`
publish through GitHub Actions after validation. Until then, builds upload an
artifact and skip deployment for initial repository seeding. Feature
branch PRs build without deployment. Manual dispatch publishes only on `main`.
Do not push, publish, change DNS or activate repository settings without the
user's authorization. Ask before changing published URLs, scientific claims,
major dependency versions or resolving substantive content ambiguities.

## Commits and handoff

Use Conventional Commits with imperative subjects of at most 72 characters.
Explain non-obvious rationale and operational details in concise lowercase body
bullets. Keep this file policy-focused and link procedures instead of duplicating
them. For incomplete work, report changed files/versions, checks performed,
remaining uncertainty and concrete next steps. A local build is not deployment
or proof that notification delivery works.
