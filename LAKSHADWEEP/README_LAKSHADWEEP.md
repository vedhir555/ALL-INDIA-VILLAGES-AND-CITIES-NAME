# Lakshadweep — Villages, Cities & Localities — Data

## Districts (2026)
One district: **Lakshadweep** (no change found).

## Source notes
- **All 27 LGD village rows have a blank census name.** Names here come from the Survey of India label on each polygon (`vilnam_soi`), cleaned (title case, `>` fixed to `a`, e.g. `BANG>RAM` -> `Bangaram Island`). They are island and islet names, not census village names, and a few repeat (five `Kalpeni` entries; the two `Kalpeni Island` rows are different polygons with different LGD codes).
- SBM has no ward data for Lakshadweep, so there are no city outlines; Kavaratti, Minicoy and Andrott are OSM `place=town` points with a town-centre fallback entry each. OSM has only one other locality-type point (Agatti Village Center), which is not near any of them and is not included.

## Sources
Villages: `LGD_Villages.geojsonl` · Cities: `SBM_Wards.parquet` (no ward names or wards stored) plus OSM `place=city|town` points not covered by SBM · Localities and boundaries: Geofabrik OSM Southern Zone extract (2026-09-16).

## Numbers
| | Count |
|---|---|
| Districts | 1 |
| Talukas (LGD subdistricts) | 10 |
| Villages written | 27 |
| LGD rows with no usable name (`unmatched_names.json`) | 0 |
| Cities/towns | 3 (0 SBM + 3 OSM-only) |
| City outlines (`boundary.json`) | 0 |
| Real OSM locality names | 0 |
| Cities with only a town-centre fallback entry | 3 |
| Search-index entries (`lakshadweep_places_index.json`) | 33 |

## Layout and method
Same layout as Kerala and the other states. Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = `simplify(0.0003)` at 7 dp. Rows with the same LGD code, name and taluka were merged into one village.
