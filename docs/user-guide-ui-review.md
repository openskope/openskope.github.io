# User Guide review against staging

Reviewed 2026-11-25 at [staging.openskope.org](https://staging.openskope.org/),
build `v2026.11.1-6-gbd11a16`. Checked the dataset catalog, Select Area,
Visualize, Analyze and narrow-screen workflow navigation. The local app source
at `bd11a16` matches the deployed build; only shared footer assets/pin differ
locally. This is a UI documentation review, not a scientific-method revision.

## Screenshots updated

Use SKOPE now shows the real staging Select Area interface with PaleoCAR V3 and
the polygon imported through Upload GeoJSON from `skopeui/chaco.geojson`.
The staging preview guide's Select Area section retains both useful views: the
full dataset extent before import, followed by the imported Chaco study area.

Both captures are 1600 × 1000 at device scale 1, with native map controls and
attribution intact. They live in `assets/images/screenshots/` with capture dates
in their filenames; Hugo creates responsive WebP derivatives. The shared image
partial accepts current asset paths and archived WordPress paths. Archived media
remain at their original URLs. Browser evidence and capture provenance are in
ignored `tmp/staging-guide-review/`.

## Released-guide differences and preview updates

The released 2023 guide is preserved at `/users-guide/v2023.10/` and selected
at `/users-guide/`. The operational instructions below are addressed in the
new `/users-guide/next/` preview. Its scientific methods remain linked to the
released explanation rather than rewritten. The filenames below are also an
existing discrepancy in the legacy guide, not solely a new staging change.
See [versioning](user-guide-versioning.md) for promotion to a CalVer release.

## Review findings, in order

1. **Save/restore instructions — Using the App and Analyze.** Replace the old
   LOAD SKOPE ANALYSIS button image/label with **Load saved analysis**. The guide
   tells readers to extract `request.json`; this build expects
   `skope-request.json`. Match the documented export contents to
   `time-series.csv`, `time-series.json`, `summary-statistics.json`, `plot.png`,
   `plot.svg`, `study-area.geojson`, `skope-request.json` and `README.md`.
   Evidence: the live header/analysis Download control and the matching source
   `components/dataset/LoadAnalysis.vue` and
   `pages/dataset/[id]/analyze/[variable].vue`. File names are source-verified;
   a completed live ZIP export was not exercised in this review.

2. **Metadata access — introduction and Select Dataset.** The old guide points
   to a red warning triangle. The current information button is named
   **Dataset details** and opens metadata covering uncertainty/provenance. Update
   the control description and old icon images. Retain all scientific uncertainty
   explanations and caveats; the access path changed, not their importance.

3. **Navigation and responsive layout — Using the App.** Explain the visible
   desktop **Select Dataset → Select Area → Visualize → Analyze** step bar,
   completed/disabled steps, narrow-screen workflow drawer, and separate help
   menu. Include **Edit study area**, **Back to visualize** and return-to-analysis
   actions where applicable. Replace the 2021 header/menu images; avoid making
   pixel-width requirements central to the instructions. Help/contact/reporting
   controls are now explicit header actions, rather than footer-only guidance.

4. **Study-area import and map editing — Select Area.** Name **Upload GeoJSON**,
   **Download GeoJSON**, **Point**, **Circle**, **Rectangle**, **Polygon**,
   **Drag**, **Change**, **Rotate**, **Delete** and **Zoom to shape**. Rectangle
   and circle tools use successive clicks; polygon finishes by clicking its first
   point again. A new drawing replaces the previous shape. Explain the named
   **Base map** layers button instead of the old globe icon. The importer accepts
   one Point/Polygon/MultiPolygon feature (or a single-feature collection);
   multiple polygons must form one MultiPolygon, not multiple study features.
   Evidence: live control tooltips, successful Chaco import, and matching
   `utils/studyArea.ts` and `utils/maplibre/config.ts`.

5. **Dataset discovery — Select Dataset and introductory availability claims.**
   Refresh the screenshot and describe the current cards, grouped variables,
   variable-category chips, Keyword search and Start Year/End Year fields. The
   observed staging catalog has PaleoCAR V3, PaleoCAR V2, LBDA V2 and OWDA V1.
   Confirm the supported catalog before revising claims about SRTM90 or adding
   new scientific descriptions; a staging listing alone is not evidence that a
   dataset has been permanently retired.

6. **Visualization and analysis controls.** Refresh both page screenshots and
   old raster button images. The plot range fields are **From/To**, with **Apply**
   and **Reset**, rather than Min Year/Max Year. **Current year / Shown on map**
   appears in the map header; animation controls sit beneath the map. The source
   has no exposed overlay-opacity control, so the guide's opacity-slider paragraph
   needs removal or qualification. Check actual configured base-map names before
   retaining the Stamen example. Analysis still has the summary/transformation/
   smoothing controls and **Clear/Update**; retain mathematical descriptions,
   updating their locations/labels. Area/cell readouts appear after a successful
   time-series response, not during area selection.

## Review limits

The Chaco import and map capture succeeded with no browser page errors.
The full-range PaleoCAR V3 time-series requests were still showing “Still
working...” during the short inspection. Numerical results, completed-download
behavior and every transformation combination were not validated. Loading,
retry/error recovery and restore validation deserve a short task-based check
when the guide is revised. The released guide prose has not been silently
rewritten. Its section anchors, published URLs, authors, scientific methods and
original media remain in place; the staging preview is a separate draft.
