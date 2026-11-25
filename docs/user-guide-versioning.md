# Release-specific SKOPE guides

SKOPE uses CalVer. Match real app tags exactly: `vYYYY.MM`, with an optional
numeric release suffix such as `v2026.11.1`. Do not substitute SemVer labels or
turn a Git describe string into a release number.

## Reader URLs

- `/users-guide/` always renders the latest **published guide**, from one frozen
  release source. Existing anchors and `/skope-users-guide/` continue working.
- `/users-guide/v2023.10/` is the fixed snapshot for the released 2023 interface.
- `/users-guide/next/` is the clearly labeled staging preview. It names the base
  CalVer release, exact build and full app commit; it is not a released guide.

The observed production app reports `v2023.10-4-g3189`; staging reports
`v2026.11.1-6-gbd11a16`. The existing authored guide matches the 2023 interface.
A newer Git tag alone does not publish or approve a new guide.

## Hugo and Docsy ownership

`hugo.yaml` is the guide catalog. Native Docsy `params.versions`, `version_menu`
and `version_menu_pagelinks` settings provide the version selector; additional
entry metadata pins the app commit, guide page and frozen content checksum.
`guide_latest_released` selects the released source to include at the stable URL.
There is no second hand-maintained version menu. Review the small adapter when
upgrading Docsy, alongside the existing navbar override.

The guide page's version notice calls Docsy's upstream
`navbar-version-selector.html`; the archive index embeds the same selector.
The global navbar stays consistent across guide and project pages. A small adapter resolves local Hugo pages to deployment-aware
URLs, since Docsy expects complete version URLs. The guide archive index uses
Docsy's `simple_list` option to avoid skipped heading levels in its default
summaries. The selector uses explicit guide URLs rather than appending the current
path: only the guide is versioned, not the entire project website. Older released guides use Docsy's upstream
`version-banner.html`; a guide-specific notice identifies the staging build.

`released-guide` uses Hugo's `RenderShortcodes` with Markdown shortcode notation.
This renders the release body once while retaining native section navigation.
The released body lives under `content/guide-versions/`; root content only selects
it. No app checkout, runtime fetch or app build is required by the website.

## Publishing a guide for a release

1. Finish the staging guide against an actual CalVer tag and full app commit.
   Check selection/import, metadata, visualization, analysis, downloads, restore,
   responsive navigation, uncertainty caveats and scientific explanations.
2. Copy the reviewed guide into `content/guide-versions/<tag>/index.md`, set its
   permanent URL to `/users-guide/<tag>/`, and set `guide_version` to the tag.
   Update its title and remove completed draft-review notices. Retain established
   section IDs. Record actual screenshots under dated asset
   names; retain their staging/release provenance and map attribution.
3. Add a Docsy `params.versions` entry with the exact tag, full `app_revision`,
   permanent URL, `guide_page` and `content_sha256`. The checksum covers the
   Markdown body after front matter, with surrounding whitespace trimmed.
4. After review, advance `guide_latest_released`. The stable URL now renders
   that frozen body; old snapshot URLs keep their previous content. Update the
   preview entry for the next development build independently.
5. Run `make check`, a subpath render/site check, and desktop/mobile browser
   checks of the native dropdown, deep links and both release/preview content.
6. After guide publication, pin the matching app release's help links to its
   snapshot URL; staging can use `/users-guide/next/`. Do not ship an app link
   to a guide that has not been published.

The stable entry point rejects preview pointers and release/page mismatches.
Frozen-content checks reject accidental edits to released guide bodies. A
necessary correction requires an explicit checksum update and an errata note
explaining it in Git; do not silently refresh an old screenshot in place.
Scientific changes require scientific review, independently of UI documentation.

Sources: [Docsy versioning](https://www.docsy.dev/docs/content/versioning/) and
[Hugo RenderShortcodes](https://gohugo.io/methods/page/rendershortcodes/).
