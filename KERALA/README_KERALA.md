# Kerala — Villages, Cities & Localities — Data

## Districts (2026)
Kerala has **14 districts** in 2026 — no district has been created since Kasaragod (1984). Reports in June 2026 say Tirur and Muvattupuzha may become districts, but only a study commission has been announced and any decision waits for the next census, so they are not included. All three sources agree on the same 14 names (LGD villages, OSM district boundaries, SBM city labels).

## Sources
- Villages: `LGD_Villages.geojsonl` (LGD, Kerala only)
- Cities/towns: `SBM_Wards.parquet` (ULB list + ward polygons unioned into one city footprint; **no ward names or wards stored**) plus OSM `place=city|town` points that SBM does not cover
- Localities and district boundaries: Geofabrik OSM Southern Zone extract (2026-09-16)

## Numbers
| | Count |
|---|---|
| Districts | 14 |
| Talukas (LGD subdistricts) | 76 |
| Villages written | 1,527 |
| LGD rows with no usable name (`unmatched_names.json`) | 8 |
| Cities/towns | 248 (75 from SBM + 173 OSM-only) |
| City boundaries (`boundary.json`) | 72 |
| Real OSM locality names | 2,214 in 216 cities |
| Cities with only a town-centre fallback entry | 32 |
| Search-index entries | 4,021 |

## Layout
Same as the other states: `<DISTRICT>.json`, `dropdown_data/`, `rich_data/<DISTRICT>/<TALUK>/villages.json`, `rich_data/<DISTRICT>/subdistricts.json`, `unmatched_names.json`, `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` (+ `boundary.json`), `kerala_places_index.json` (keys `n/t/d/p/lat/lon`), `state_district_map.json`.
Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = `simplify(0.0003)` at 7 dp (same transform as Rajasthan and the northern states).

## Fixes applied to the source data
- SBM ULB `803309` (Varkala) contained 20 wards mislabelled `Thiruvananthpuram` that sit 39 km away inside Thiruvananthapuram Corporation (18 of them duplicate its wards). They were dropped so Varkala's footprint and centre are correct.
- SBM lists Kozhikode, Nedumangad and Sulthan Bathery with only 2 wards each. Their outlines would be misleading, so these three have **no `boundary.json`**; their centres come from the matching OSM city/town point and their localities are matched by distance to that point.
- Administrative markers were removed from SBM names (`Adoor (M)` → `Adoor`, `Kollam Corporation` → `Kollam`, `Varkala Municipality` → `Varkala`).
- Entirely lowercase OSM names were title-cased.

## Known gaps
- SBM lists 75 of Kerala's 93 urban bodies (6 corporations + 87 municipalities). The rest, including Kannur Corporation, Kottayam and Malappuram, appear only as OSM-only points (no city outline). OSM-only entries also include census towns and small places tagged `place=town` in OSM.
- LGD has 76 taluks for Kerala; the state officially has 77.
- LGD keeps split villages such as `Peringanadu (Part)`; rows with the same code, name and taluk were merged (88 rows), different villages sharing a code were kept separate.
- City outlines come from SBM wards before Kerala's 2025 ward delimitation.
- Localities are only listed when inside or within 500 m of a city outline (or within 3–5 km of the centre of an OSM-only or weak-footprint city); rural neighbourhood points elsewhere are not included.
