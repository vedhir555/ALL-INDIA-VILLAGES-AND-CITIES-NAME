# Tamil Nadu — Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (LGD village boundaries, Tamil Nadu only)
- City outlines: `SBM_Wards.parquet` (SBM urban ward polygons merged into one city outline). Ward numbers are not used; nearly all Tamil Nadu SBM ward names are just numbers ("Ward 12"), so almost no ward names exist.
- Cities/towns and neighbourhoods: Geofabrik OSM Southern Zone extract (2026-09-16)
- Neighbourhood names: GeoNames `IN.txt` (feature code PPLX) and India Post pincode directory (data.gov.in extract, May 2025, sub-office names only)

## Coordinates (every record)
- `lat` / `lon` — **map pin**: a point guaranteed to lie inside the boundary (for point-only records it is the point itself)
- `centroid_lat` / `centroid_lon` — geometric centroid (can fall outside a curved boundary, which is why the pin is separate)
- `boundary_wkt` — outline (villages, city outlines, wards, OSM neighbourhoods that have one)

## Numbers
| | Count |
|---|---|
| Districts (LGD) | 38 |
| Talukas with named villages | 291 |
| Villages with names | 16,132 |
| LGD polygons with no usable name/code (`unmatched_names.json`) | 2,027 (1,657 carry a Survey of India label in `soi_name`) |
| Cities/towns | 401 |
| City outlines (`boundary.json`) | 124 |
| Ward names (SBM) | 114 |
| OSM neighbourhood/suburb/quarter names | 1,701 |
| India Post names | 301 |
| GeoNames names | 168 |
| Cities with only a town-centre entry | 169 |
| Search-index entries | 18,817 |

## Layout (same as Karnataka / Rajasthan / Chhattisgarh)
`<DISTRICT>.json` = `{district, talukas, cities}`; `dropdown_data/`; `rich_data/<DISTRICT>/<TALUKA>/villages.json`; `subdistricts.json`; `unmatched_names.json`; `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` + `boundary.json`; `tamil_nadu_places_index.json`; `state_district_map.json`.

## Known gaps
- SBM ward names are numbers, so 115 cities that have outlines have no ward names; their localities come from OSM, GeoNames and India Post.
- About 277 cities/towns are OSM-only points (census towns and places tagged `place=town`), so they have no outline; some are small villages.
- OSM places with only a Tamil-script name were skipped (English name used when present).
- Some India Post office names are estates or government offices, not neighbourhoods.
- 2,027 LGD polygons have no usable name; they are kept in `unmatched_names.json`.
- City outlines come from SBM ward polygons and may differ from current municipal limits.
