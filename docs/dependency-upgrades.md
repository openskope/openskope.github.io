# Dependency upgrades

Maintain Hugo, Docsy, Sass and frontend assets as a tested deployment set. Select
latest stable compatible versions within the requested scope; record blockers
when a component must remain behind. Use container Make targets throughout.

## Automated checks and security alerts

`.github/dependabot.yml` checks npm, Go modules, Docker images and GitHub Actions
on Monday and Friday at 09:00 `America/Phoenix` (3- and 4-day gaps). Review PRs
using the procedure below; retain human approval before merging and publishing.
Hugo version files, generated workspace metadata and cross-file version/digest
alignment still require operator review.

Leave `cooldown` unset. As of 2026-11-24, GitHub's documented default is a
[3-day minimum release age](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#cooldown)
for routine version updates. The next Monday/Friday check after eligibility can
propose the release, typically about 3–7 days after publication before operator
review, subject to successful resolution and available PR capacity. Security
updates bypass this cooldown. Recheck the upstream default during maintenance.

Activate and verify notifications separately from this YAML file:

1. Merge the config into the default branch. In repository **Settings → Advanced
   Security**, verify the dependency graph, Dependabot alerts and Dependabot
   security updates are enabled. Confirm the dependency graph lists the expected
   manifests, and inspect **Security and quality → Dependabot** for existing alerts.
2. In personal [notification settings](https://github.com/settings/notifications),
   enable individual Dependabot email and GitHub notifications. Also enable email
   delivery for watched repositories. A weekly digest alone is insufficient.
3. For each repository, choose **Watch → Custom → Security alerts → Apply**.
   Confirm your account has access to its security alerts. Assign a primary and
   backup responder, verify the destination mailbox, and confirm receipt when an
   alert arrives; an enabled setting alone is not delivery evidence.

For multiple repositories, an organization owner can apply a
[security configuration](https://docs.github.com/en/code-security/how-tos/secure-at-scale/configure-organization-security/establish-complete-coverage/create-custom-configuration)
in bulk and make it the default for newly created repositories. Apply it to
existing repositories too; transferred repositories need separate attention.
Each organization has its own configuration. Personal delivery preferences are
account-wide; repository watch subscriptions still need verification.

[Security-update PRs are advisory-triggered](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-pull-requests),
independently of routine checks. Treat Critical/High alerts as immediate triage:
check affected versions and build/runtime exposure, prioritize known exploitation,
and validate a compatible fix before merging. If no fix is available, record the
mitigation, owner and next review date. An alert can exist without a fix PR.
[Configure individual notifications](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependabot-notifications)
when GitHub detects a new Critical/High advisory; discovery is not guaranteed at
the instant a CVE is published. Continue checking host/system dependencies during
maintenance: these checks do not cover all container packages or host software.

## Pins and ordered procedure

| Component | Source |
| --- | --- |
| Hugo | `HUGO_VERSION`, matching Dockerfile digest, `hugo.yaml` supported minimum |
| Docsy | `go.mod` / `go.sum` and `hugo.yaml` import |
| Sass and frontend assets | `package.json` / `package-lock.json` |
| Hugo npm workspace | Generated `packages/hugoautogen/`; regenerate rather than hand-edit |
| CI | Commit pins and version comments in `.github/workflows/` |

1. Start on a clean branch; check system package currency and runtime support.
   Check whether a preview is running. Stop it or use a separate checkout.
2. Run `make build`, `make toolchain-status`, then `make check` for a baseline.
3. Review upstream compatibility and release notes. For Hugo, update the exact
   `HUGO_VERSION`, official image digest and tested minimum together. Run
   `make build` before changing npm manifests, preserving a usable existing image.
4. For Docsy, run `make deps-docsy DOCSY_VERSION=vX.Y.Z`. The target rejects
   floating versions and prereleases. Review local SCSS/layouts against upstream.
5. Update direct npm declarations as needed. Root Bootstrap and Font Awesome pins
   take precedence over Docsy module requirements. Run `make deps-pack`, then
   `make deps-lock`, then `make build`. These dependency commands reuse the image
   while manifests/locks change; lock resolution occurs in a temporary workspace
   and preserves the existing lockfile on failure.
6. Reconcile `layouts/partials/navbar.html`, Docsy search and Bootstrap collapse
   behavior, plus fixed-header/sticky-sidebar offsets, after theme changes.
   Run `make toolchain-status` and `make check`. Review the home page, long user
   guide, publications, tables, images, PDF downloads, navigation, search and
   mobile layout; inspect console/network errors and compare published routes.
7. Run `make render RENDER_BASE_URL=https://example.org/preview/` followed by
   `make site-check RENDER_BASE_URL=https://example.org/preview/`. Finish with
   `make render` for production output. Review `git diff --check`, source pins,
   generated workspace and lockfile changes before committing.
8. Record exact versions, checks and any reconciliation. Distinguish local work
   from deployed state. Merge only after operator approval: successful `main`
   builds publish once `PAGES_ENABLED=true`.

For a Dependabot PR, reconcile related pins and generated metadata using the same
steps. An npm PR or a successful render does not establish compatibility of local
overrides. Major upgrades require deliberate review. See the README for Pages
activation, custom domain and recovery; no dependency target publishes directly.
