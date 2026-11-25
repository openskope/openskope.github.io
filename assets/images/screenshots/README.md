# SKOPE UI captures

Captured 2026-11-25 from
<https://staging.openskope.org/dataset/paleocar_v3>, build
`v2026.11.1-6-gbd11a16` (app commit
`bd11a160de7e6b0072bd98d6aa223be3cd9f1d26`).

Both PNGs are unaltered 1600 × 1000 browser captures at device scale 1:

- `paleocar-v3-extent-select-area-2026-11-25.png`: the full PaleoCAR V3 extent
  before importing a study area.
- `paleocar-v3-chaco-select-area-2026-11-25.png`: the same screen after uploading
  `skopeui/chaco.geojson`, with the map fitted to that geometry. The input file's
  SHA-256 is `eb988f8311609d4a2a00b8aa71217eb75b29869b4d19010ae479c0f5d8972c97`.

Native map attribution remains visible. Use `skope-figure` with these asset paths;
Hugo produces disposable responsive WebP derivatives. Keep dated source filenames
stable and add new captures when an interface changes. Archived WordPress images
remain available at their original URLs.
