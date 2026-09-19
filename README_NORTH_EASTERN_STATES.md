# North-Eastern States — Villages, Cities & Locations (data)

Same layout as the Uttarakhand/Rajasthan folders: one folder per state, each with
`<DISTRICT>.json`, `dropdown_data/`, `rich_data/`, `state_district_map.json` and `<state>_places_index.json`.

## Sources
- Villages: `LGD_Villages.geojsonl` — **only Assam (20,997 polygons), Tripura (880) and 1 Meghalaya row exist in this file**. Arunachal Pradesh, Manipur, Meghalaya, Mizoram, Nagaland and Sikkim are not in it.
- Villages for states/areas LGD does not cover: OSM `place=village|hamlet` (`north-eastern-zone-260916_osm.pbf`) plus GeoNames `IN.txt` PPL, only where the point is outside every LGD polygon and every SBM ward, de-duplicated by name (within ~3 km). These have `lgd_code: null`, `boundary_wkt: null`, and a `source` field.
- Cities/towns: SBM ULBs (Assam 67, Nagaland 7, Sikkim 6; ULB suffixes like `M.B.`, `(Tc)`, `Municipal Board` removed, spelling variants merged) + OSM `place=city|town`. City `lat`/`lon` = centroid of its SBM ward polygons, else the OSM point.
- SBM wards: **ward names/numbers are not used.** Each ward polygon is used only to find named locations inside it.
- Location names: OSM `place=neighbourhood|suburb|quarter|locality`, OSM named residential/commercial landuse and `addr:suburb|neighbourhood|quarter|locality|place`, GeoNames PPLX/PPLL/PPL, India Post S.O./B.O. names, and LGD village names whose centroid falls in a ward.

## Locality fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt`
- `lat`/`lon` = the location's own coordinates.
- `centroid_lat`/`centroid_lon` = centroid of the SBM ward polygon containing it (`boundary_wkt` = that ward polygon, simplified). For towns with no SBM wards the centroid equals `lat`/`lon` and there is no `boundary_wkt`.
- A location is kept only if it lies inside a ward polygon (or within ~250 m of it for proper locality names). India Post rows are used only when the coordinate has >3 decimals and is not shared by another office (shared coordinates are pincode-centre placeholders).
- Village `lat`/`lon` = polygon centroid, or an interior point when the centroid falls outside the polygon.

## Numbers
| State | Districts | Talukas | Villages | Cities/towns | Locations | Town-centre only |
|---|---|---|---|---|---|---|
| Arunachal Pradesh | 26 | 189 | 1,867 (0 LGD) | 80 (0 with SBM wards) | 70 | 49 |
| Assam | 35 | 186 | 16,434 (16,350 LGD) | 144 (59 with SBM wards) | 354 | 76 |
| Manipur | 16 | 46 | 1,515 (0 LGD) | 33 (0 with SBM wards) | 35 | 19 |
| Meghalaya | 12 | 51 | 463 (0 LGD) | 25 (0 with SBM wards) | 56 | 20 |
| Mizoram | 11 | 28 | 399 (0 LGD) | 21 (0 with SBM wards) | 11 | 17 |
| Nagaland | 17 | 118 | 582 (0 LGD) | 42 (7 with SBM wards) | 43 | 29 |
| Sikkim | 6 | 11 | 432 (0 LGD) | 13 (6 with SBM wards) | 7 | 10 |
| Tripura | 8 | 31 | 873 (849 LGD) | 28 (0 with SBM wards) | 26 | 20 |
| **Total** | 131 | 660 | 22,565 | 386 | 602 | 240 |

## Known gaps
- Assam has 4,640 LGD polygons with no village name/code; they are in `unmatched_names.json` (with `soi_name`), not in the village lists. Karbi Anglong / West Karbi Anglong / Dima Hasao are nearly empty in LGD, so those come mostly from OSM/GeoNames points.
- Only 616 SBM wards exist for this region and only ~148 of them contain a named location in the sources above; the rest have no locality entry (no ward name is substituted). Sikkim and Nagaland ward names are real place names — they can be used as a fallback if wanted.
- OSM `town` tags include some small villages (notably Arunachal), and OSM/GeoNames villages have point coordinates only.
- Ward polygons and village polygons are simplified.
