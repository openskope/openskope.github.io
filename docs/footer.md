# Shared web content and styling

The static website is authoritative for reusable project content and styling in
`shared/web/`. Its version-1 bundle contains exactly:

- `footer.json`: acknowledgments, copyright, action labels and website page paths
- `tokens.json`: shared footer CSS custom-property values
- `footer.css`: framework-neutral styling using those tokens
- `application-policy.json`: citation guidance and application terms
- `CITATION.cff`: canonical SKOPE application citation metadata

The initial credits and policy wording were preserved from `skopeui`; citation
metadata retains its existing release, authors and DOI. Edit these sources here,
not consumer copies. `CITATION.cff` describes the application, not this website.
The original font choice remains Source Sans 3 across both repositories.

Hugo renders the bundle directly, including `/cite-skope/` and `/terms-of-use/`.
The small `footer.html` adapter renders escaped text segments and explicit HTTPS
links. `web-assets.html` generates fingerprinted CSS from tokens and styling.
Only the Docsy gutter correction belongs in the website's own footer SCSS.

## One-way dependency

SKOPE UI imports the five files from an exact website commit into
`app/shared/web/`, with the source SHA and file checksums in
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
   The website repository currently requires read access. For unpublished local
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
