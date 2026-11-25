# Shared web content and styling

The static website is authoritative for reusable project content and styling in
`shared/web/`. Its version-1 bundle contains exactly:

- `footer.json`: acknowledgments, copyright, action labels and website page paths
- `tokens.json`: shared font stacks and footer CSS custom-property values
- `footer.css`: framework-neutral styling using those tokens
- `application-policy.json`: citation guidance and application terms
- `CITATION.cff`: canonical SKOPE application citation metadata

The initial credits and policy wording were preserved from `skopeui`; citation
metadata retains its existing release, authors and DOI. Edit these sources here,
not consumer copies. `CITATION.cff` describes the application, not this website.
The original font choice remains Source Sans 3 across both repositories.

The repository-root `CITATION.cff` is a regular, generated copy for GitHub's
"Cite this repository" metadata. Edit only `shared/web/CITATION.cff`, then run
`make citation-sync` and commit both files together. Build and site checks reject
a missing, symlinked or divergent root copy. A hardlink relationship would not
survive a Git checkout; the checked copy makes the contract explicit and portable.

Hugo renders the bundle directly, including `/cite-skope/` and `/terms-of-use/`.
The small `footer.html` adapter renders escaped text segments and explicit HTTPS
links. `web-assets.html` generates fingerprinted CSS from tokens and styling.
Only the Docsy gutter correction belongs in the website's own footer SCSS.

## Validation and styling ownership

`make web-assets-check` validates schema version 1, required content/labels,
HTTPS acknowledgment links, local policy routes, token references, footer text
contrast in normal/hover states, and citation fields. It runs before production
renders and preview startup. `make content-test` includes rejection tests for
invalid bundles and missing/duplicate rendered footer assets. GitHub Pages CI
runs these through its existing render and test steps.

`make site-check` also validates the source bundle and checks every rendered
non-redirect page for exactly one shared footer and fingerprinted stylesheet,
acknowledgment text/links, copyright and policy actions. It checks the published
policy text and CFF download against their sources, including subpath builds.
Hugo parses the full citation YAML during rendering.

Shared font stacks live in `tokens.json`; the footer and website typography use
those CSS variables. Website theme colors live in
`assets/scss/_variables_project.scss`, and site rules reuse those Sass variables.
Content uses Bootstrap alignment/weight classes and the small set of semantic
classes in `_styles_project.scss`; image display sizes use HTML width attributes.
Edit theme rules rather than adding inline colors or disabling focus outlines.

Footer foreground, background and hover-background tokens use six-digit hex
colors so the validator can enforce at least 4.5:1 contrast. Adding optional
tokens to the existing JSON file preserves the v1 five-file bundle contract.

## One-way dependency

SKOPE UI imports the five files from an exact website commit into
`app/vendor/web-assets/`, with the source SHA and file checksums in
`app/web-assets.lock.json`. Its root `CITATION.cff` is an imported copy for GitHub
and existing citation-generation tooling; Make checks that it matches the bundle.
The app renders shared policy text in its existing dialogs. State, dialogs,
acceptance persistence and enforcement remain app behavior, with no policy change.

Normal builds verify local files and never fetch the other repository. Neither
site loads shared content from the live website at runtime. The website does not
import app source or app build output; there is no reverse dependency.
The imported files are generated copies: never edit them independently.

## Updates

1. Edit shared sources here, keeping schema version 1 backward-compatible.
   Coordinate incompatible schema or CSS-class changes with the app adapter.
2. Run `make check`, root/subpath renders and browser checks on the home page,
   guide, citation and terms pages at desktop/mobile widths. Inspect the CFF
   download and citation metadata. Preserve scientific and legal wording unless
   a content change has been explicitly requested.
3. Commit the website changes. In `skopeui`, run
   `make deps-web-assets WEB_ASSETS_REVISION=<full-40-character-sha>`.
   The website repository currently requires read access. The importer can use
   existing Git credentials or the installed GitHub CLI credential helper. For unpublished local
   commits add `WEB_ASSETS_SOURCE=/absolute/path/to/site`; imports still read
   committed Git objects, never working-tree files. Push the source commit before
   others need to refresh it. Normal app builds need no source credentials.
4. Review the imported files, lock and root CFF. Run `make test` and
   `make build ENVIRONMENT=staging`, then compare both footers, citation display,
   terms and existing app consent behavior. Shared text/CSS changes can affect
   both sites; a pin update is operator-reviewed, never silently applied.
5. Commit/deploy each consumer through its normal review process. Advancing a pin
   does not itself deploy the app. Build/source values identify the local repo.

The importer fetches an exact Git object and exports only the five allowlisted
files. It validates the full export before writing and records checksums.
Checksums detect accidental consumer edits; they do not establish trust in an
unreviewed upstream revision. Any added bundle file requires an explicit update
to the export/import contract and validation.
