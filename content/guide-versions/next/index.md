---
title: SKOPE User Guide — staging preview
linkTitle: Staging preview
type: docs
toc_hide: false
url: /users-guide/next/
guide_version: next
weight: 20
lastmod: 2026-11-25
---

{{< guide-version >}}

This preview follows the updated SKOPE interface. It uses PaleoCAR V3 and the
Chaco example study area. The [released guide]({{< relref "/users-guide" >}}) remains available for the
interface currently running at [app.openskope.org](https://app.openskope.org/).

## Using the App {#using-the-app}

Open [staging.openskope.org](https://staging.openskope.org/) and review the terms
on your first visit. On a wide screen, use the **Select Dataset → Select Area →
Visualize → Analyze** step bar. Steps become available as you choose a dataset
and study area. On a narrow screen, open the workflow menu beside the SKOPE title.

**User Guide**, **Contact** and **Report a bug** provide help. Some controls move
into menus on narrower screens. **Load saved analysis** restores an exported
analysis request; see [Analyze Data](#analyze-data).

## Select Dataset {#select-dataset}

Use **Filter by variable category**, **Keyword search**, **Start Year** and
**End Year** to narrow the dataset cards. Expand a variable group to see its
variables, or select a dataset title to choose a study area.

Open **Dataset details**, the information button beside a dataset title, to
review its metadata, uncertainty and provenance before interpreting results.
The screenshot example below uses **PaleoCAR: SW USA Paleoclimate Reconstruction
(V3)**.

## Select Area {#select-area}

The initial map shows the dataset's full extent. Choose **Point**, **Circle**,
**Rectangle** or **Polygon** from the map toolbar. A rectangle uses two corner
clicks; a circle uses a center click and a radius click. For a polygon, click its
corners, then click the first corner again to finish. Follow the tool's pointer
instructions.

{{< skope-figure src="images/screenshots/paleocar-v3-extent-select-area-2026-11-25.png" alt="Current Select Area page showing the full PaleoCAR V3 dataset extent over the southwestern United States before a study area is selected." caption="**PaleoCAR V3:** the full dataset extent before selecting a study area." >}}

Alternatively, select **Upload GeoJSON** and choose a study-area file. The Chaco
example was imported from `chaco.geojson`. The importer accepts one Point,
Polygon or MultiPolygon feature, including a single-feature FeatureCollection.
A file containing several separate study features is rejected.

{{< skope-figure src="images/screenshots/paleocar-v3-chaco-select-area-2026-11-25.png" alt="Current Select Area page with PaleoCAR V3, the imported Chaco study area, and the GeoJSON and map editing controls." caption="**Chaco example:** the study-area polygon imported from `chaco.geojson`." >}}

Use **Drag**, **Change**, **Rotate** or **Delete** to edit the selected shape.
**Zoom to shape** brings it back into view. Drawing a new shape replaces the
current selection. **Download GeoJSON** saves the selected geometry.

Use **Base map**, the layers button near the zoom controls, to choose a background
map. Select **Visualize Data** when the study area is ready.

## Visualize Data {#visualize-data}

Select a variable beside the dataset title. Use the plot's **From** and **To**
fields, then **Apply**, to change the interval; **Reset** restores the available
range. **Current year**, labeled **Shown on map**, controls the map's displayed
time step. The animation controls beneath the map provide first/previous,
play/pause and next/last time-step actions. Clicking the time-series plot also
selects a time step.

The map and plot appear side by side on wider screens and stack on narrower
screens. Loading a time series can take time; wait for the request to finish
before interpreting the graph. If a request fails and **Retry time series** is
shown, use it to retry. **Edit study area** returns to area selection, and
**Analyze Data** opens the analysis controls.

## Analyze Data {#analyze-data}

Use **For each time step, summarize selected area as**, **Select a transformation
option** and **Select a smoothing option** to configure the analysis. Additional
interval/window fields appear for options that need them. Select **Update** to
apply the settings; **Clear** clears the transformed series. Use the plot's
**From/To**, **Apply** and **Reset** controls for its temporal range.

The statistics panel is titled **Statistics for the Temporal Interval**.
Area/cell readouts become available after a time-series response. **Edit study
area** returns to the map; **Back to visualize** returns to visualization.

Once a request completes and the plot is ready, **Download** exports a ZIP with
`time-series.csv`, `time-series.json`, `summary-statistics.json`, `plot.png`,
`plot.svg`, `study-area.geojson`, `skope-request.json` and `README.md`. To restore
an analysis later, extract **skope-request.json** from the ZIP and choose it with
**Load saved analysis**. A GeoJSON study-area file and a saved analysis request
serve different purposes; use their corresponding upload controls.

This preview's export filenames and import rules were checked against the app
source for the displayed build. A completed staging export and every numerical
transformation remain to be checked before publishing a release guide.

## PaleoCAR methods and uncertainty {#paleocar}

The interface refresh does not establish a scientific-method revision. Consult
the dataset's **Dataset details** and the
[existing PaleoCAR methods, uncertainty discussion and references]({{< relref "/guide-versions/v2023.10" >}}#paleocar).
