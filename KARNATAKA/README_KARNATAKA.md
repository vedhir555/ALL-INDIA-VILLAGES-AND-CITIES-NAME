# Karnataka — Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (LGD village boundaries, Karnataka only)
- City wards and outlines: `SBM_Wards.parquet` (SBM urban ward polygons). Ward **numbers are not used**; only ward names. City outline = the wards merged together.
- Cities/towns and neighbourhoods: Geofabrik OSM Southern Zone extract (2026-09-16)
- Neighbourhood names: GeoNames `IN.txt` (feature code PPLX) and India Post pincode directory (data.gov.in extract, May 2025, sub-office names only)

## Coordinates (every record)
- `lat` / `lon` — **map pin**: a point guaranteed to lie inside the boundary (for point-only records it is the point itself)
- `centroid_lat` / `centroid_lon` — geometric centroid (can fall outside a curved boundary, which is why the pin is separate)
- `boundary_wkt` — outline (villages, wards, city outlines, OSM neighbourhoods that have one)

## Numbers
| | Count |
|---|---|
| Districts (LGD) | 31 |
| Talukas | 234 |
| Villages with names | 30,295 |
| LGD polygons with no name/code (`unmatched_names.json`) | 121 |
| Cities/towns | 316 |
| City outlines (`boundary.json`) | 229 |
| Ward names (SBM) | 1,518 |
| OSM neighbourhood/suburb/quarter names | 1,464 |
| India Post names | 333 |
| GeoNames names | 103 |
| Cities with only a town-centre entry | 147 |
| Search-index entries | 34,029 |

## Layout (same as Rajasthan / Chhattisgarh / Uttarakhand)
`<DISTRICT>.json` = `{district, talukas, cities}`; `dropdown_data/`; `rich_data/<DISTRICT>/<TALUKA>/villages.json`; `subdistricts.json`; `unmatched_names.json`; `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` + `boundary.json`; `karnataka_places_index.json`; `state_district_map.json`.

## Known gaps
- Most SBM ward names in Karnataka are just numbers ("Ward 12"). These were dropped, so 168 cities that have ward outlines have no ward names; their localities come from OSM, GeoNames and India Post.
- Ward pieces with the same name in one city are merged into one locality.
- 11 generic OSM names such as "1st Block" or "4th Phase" were dropped.
- OSM names in Kannada script only were skipped (English name used when present).
- OSM-only "towns" include some small places tagged `place=town`.
- Some India Post office names are government offices or estates, not neighbourhoods.
- City outlines come from SBM ward polygons and may differ from current municipal limits.
- Some LGD village names contain numbers (for example `2NE CHOWDLU`); they are kept as in LGD.
