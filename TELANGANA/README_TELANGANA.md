# Telangana — Villages, Cities & Localities — Data

## Districts (2026)
Telangana has **33 districts** in 2026 (latest reports, August 2026). In January 2026 the state announced a judicial commission to "rationalise" districts, mandals and revenue divisions (media reports mention cutting the count, and there are demands such as merging Warangal and Hanamkonda), but nothing has been implemented, so the current 33 are used. LGD and OSM both carry the same 33 districts, including Hanumakonda, Mulugu and Narayanpet. LGD's older spellings were aligned: `Jagitial` -> `Jagtial`, `Jangoan` -> `Jangaon`, `Medchal Malkajgiri` -> `Medchal-Malkajgiri`.

## Sources
- Villages: `LGD_Villages.geojsonl` (Telangana, state code 36)
- Cities/towns: `SBM_Wards.parquet` (ULB list + ward polygons unioned into one city outline; **no ward names or wards stored**) plus OSM `place=city|town` points that SBM does not cover
- Localities and district boundaries: Geofabrik OSM Southern Zone extract (2026-09-16)

## Numbers
| | Count |
|---|---|
| Districts | 33 |
| Talukas (LGD subdistricts) | 571 |
| Villages written | 10,712 |
| LGD rows with no usable name (`unmatched_names.json`) | 24 |
| Cities/towns | 165 (114 SBM + 51 OSM-only) |
| City outlines (`boundary.json`) | 114 |
| Real OSM locality names | 1,712 in 37 cities |
| Cities with only a town-centre fallback entry | 128 |
| Search-index entries (`telangana_places_index.json`) | 12,717 |

## Notes and known gaps
- **Hyderabad:** SBM's `Greater Hyderabad Municipal Corporation` (145 wards) is named `Hyderabad` and filed under Hyderabad district, but its outline actually straddles four districts (about Ranga Reddy 35%, Medchal-Malkajgiri 34%, Hyderabad 27%, Sangareddy 4%). All its 1,205 localities are listed under it. The SBM ward data predates any later GHMC restructuring.
- SBM lists 114 urban bodies; the state has more (about 140), so towns not in SBM appear only as OSM-only points without outlines.
- SBM ULB `802900` is one ULB whose wards carry three labels (`Bellampalle (M)`, `Bellampally`, blank); it is published as `Bellampalli` (the OSM spelling).
- Bollaram is placed in Sangareddy by geometry; SBM's own label says Vikarabad.
- LGD village names contain characters such as `[ ]`, `@` and `+`; they are kept as in LGD.
- Localities are only listed when inside or within 500 m of a city outline (or within 3-5 km of the centre of an OSM-only town); OSM locality mapping outside Hyderabad is sparse, so most towns have only the town-centre fallback entry.

## Layout and method
Same layout as Kerala and the other states. Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = `simplify(0.0003)` at 7 dp. Rows with the same LGD code, name and taluka were merged into one village.
