# North-Eastern States — Villages, Cities & Locations (data)

Same layout as the Uttarakhand/Rajasthan folders: one folder per state, each with `<DISTRICT>.json`, `dropdown_data/`, `rich_data/`, `state_district_map.json` and `<state>_places_index.json`.

## Sources
- Villages: `LGD_Villages.geojsonl` — only Assam, Tripura and 1 Meghalaya row exist in this file.
- Villages elsewhere (and LGD gaps such as Karbi Anglong / Dima Hasao): OSM `place=village|hamlet` plus GeoNames PPL, only outside every LGD polygon and SBM ward, de-duplicated by name. These have `lgd_code: null`, `boundary_wkt: null` and a `source` field.
- Cities/towns: SBM ULBs (Assam, Nagaland, Sikkim) + OSM `place=city|town`. Only places inside Indian district boundaries are kept.
- SBM ward names/numbers are not used; ward polygons only locate named places inside them.
- Location names: OSM place/landuse/addr tags, GeoNames, India Post S.O./B.O. (only precise, non-shared coordinates), LGD village names inside a ward.

## Districts (current names)
Assam uses today's names (Sribhumi, Morigaon, Kamrup Metropolitan, South Salmara-Mankachar) instead of the older LGD spellings. Arunachal has 27 districts: Longding is built from its OSM circle boundaries (Longding HQ, Kanubari, Lawnu, Pumao, Pongchau) because OSM has no separate district polygon; Dibang Valley is named Upper Dibang Valley. Itanagar Capital Complex is not a separate district here.

## Locality fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt` — `lat/lon` = the location; `centroid_*` = centroid of its SBM ward polygon (equal to `lat/lon` when the town has no ward polygons).

## Numbers
| State | Districts | Talukas | Villages | Cities/towns | Locations | Town-centre only |
|---|---|---|---|---|---|---|
| Arunachal Pradesh | 27 | 190 | 1,879 (0 LGD) | 78 (0 with SBM wards) | 67 | 49 |
| Assam | 35 | 181 | 16,384 (16,350 LGD) | 142 (59 with SBM wards) | 354 | 74 |
| Manipur | 16 | 45 | 1,478 (0 LGD) | 32 (0 with SBM wards) | 35 | 18 |
| Meghalaya | 12 | 48 | 453 (0 LGD) | 24 (0 with SBM wards) | 56 | 19 |
| Mizoram | 11 | 27 | 360 (0 LGD) | 21 (0 with SBM wards) | 11 | 17 |
| Nagaland | 17 | 113 | 562 (0 LGD) | 41 (7 with SBM wards) | 43 | 28 |
| Sikkim | 6 | 10 | 359 (0 LGD) | 13 (6 with SBM wards) | 7 | 10 |
| Tripura | 8 | 25 | 853 (849 LGD) | 22 (0 with SBM wards) | 26 | 14 |
| **Total** | 132 | 639 | 22,328 | 373 | 599 | 229 |

## Known gaps
- Assam has 4,640 LGD polygons with no village name (in `unmatched_names.json` with `soi_name`).
- Only ~148 of 616 SBM wards contain a named location in the sources; the rest have no locality entry.
- OSM `town` tags include some small villages (notably Arunachal); OSM/GeoNames villages are points only.
