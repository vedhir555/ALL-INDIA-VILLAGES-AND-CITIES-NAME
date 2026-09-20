# Puducherry — Villages, Cities & Localities — Data

## Districts (2026)
Four districts/regions are used: **Puducherry, Karaikal, Mahe, Yanam**. These are the four in LGD and the census. Note that the Puducherry government describes only Puducherry and Karaikal as administrative districts, with Mahé and Yanam as administrative units under Puducherry district; they are kept separate here because Mahé (inside Kerala) and Yanam (inside Andhra Pradesh) are separate territories. LGD's old spelling `Pondicherry` was changed to `Puducherry`.

## Sources notes
- SBM lists only two urban bodies (`Puducherry` and `Oulgaret-Ozhukarai`, 76 wards). Karaikal, Mahe, Yanam and Nettapakkam appear as OSM-only points without outlines.
- SBM spelled the ULB `Puducherry;` (stray semicolon), cleaned.
- Mahe and Yanam cities are assigned by location because OSM has no separate district outline for them in this extract.

## Sources
Villages: `LGD_Villages.geojsonl` · Cities: `SBM_Wards.parquet` (no ward names or wards stored) plus OSM `place=city|town` points not covered by SBM · Localities and boundaries: Geofabrik OSM Southern Zone extract (2026-09-16).

## Numbers
| | Count |
|---|---|
| Districts | 4 |
| Talukas (LGD subdistricts) | 8 |
| Villages written | 105 |
| LGD rows with no usable name (`unmatched_names.json`) | 1 |
| Cities/towns | 7 (2 SBM + 5 OSM-only) |
| City outlines (`boundary.json`) | 2 |
| Real OSM locality names | 42 |
| Cities with only a town-centre fallback entry | 3 |
| Search-index entries (`puducherry_places_index.json`) | 157 |

## Layout and method
Same layout as Kerala and the other states. Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = `simplify(0.0003)` at 7 dp. Rows with the same LGD code, name and taluka were merged into one village.
