# Andaman and Nicobar Islands — Villages, Cities & Localities — Data

## Districts (2026)
Three districts: **Nicobar, North and Middle Andaman, South Andaman** (no new district found in 2026). LGD's census spellings `Nicobars` and `South Andamans` were changed to the official names. The capital was renamed **Sri Vijaya Puram** (formerly Port Blair) in 2024; it is listed as `Sri Vijaya Puram (Port Blair)` so both names are searchable.

## Source notes
- 595 of the 799 LGD rows have no usable name (`unmatched_names.json`); the 143 alternate Survey-of-India labels on those rows are things like `SHEET ROCK`, `VACANT LAND`, `P.F.` and were **not** used as village names.
- Trailing `*` markers were removed from four village names.
- SBM has a single ward in this territory (`Port Blair (M Cl)`), too small to publish as an outline, so Sri Vijaya Puram has no `boundary.json`. Its centre comes from OSM, and localities are matched within ~15 km of that centre (it is the only city on South Andaman island). Potang and Uttara Jetty were too far away and are not included.
- Diglipur, Mayabunder and Rangat are OSM-only points with no OSM locality names, so each has a single town-centre fallback entry.

## Sources
Villages: `LGD_Villages.geojsonl` · Cities: `SBM_Wards.parquet` (no ward names or wards stored) plus OSM `place=city|town` points not covered by SBM · Localities and boundaries: Geofabrik OSM Southern Zone extract (2026-09-16).

## Numbers
| | Count |
|---|---|
| Districts | 3 |
| Talukas (LGD subdistricts) | 9 |
| Villages written | 192 |
| LGD rows with no usable name (`unmatched_names.json`) | 595 |
| Cities/towns | 4 (1 SBM + 3 OSM-only) |
| City outlines (`boundary.json`) | 0 |
| Real OSM locality names | 28 |
| Cities with only a town-centre fallback entry | 3 |
| Search-index entries (`andaman_and_nicobar_places_index.json`) | 227 |

## Layout and method
Same layout as Kerala and the other states. Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = `simplify(0.0003)` at 7 dp. Rows with the same LGD code, name and taluka were merged into one village.
