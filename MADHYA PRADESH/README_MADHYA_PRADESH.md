# Madhya Pradesh Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (official LGD/Census-SOI village boundary survey, all-India) — filtered to Madhya Pradesh.
- City wards: `SBM_Wards.parquet` (Swachh Bharat Mission urban ward polygons). Ward **numbers are not used** — only the ward's place name; the ward polygon centroid is its `lat`/`lon`.
- Cities/towns and neighbourhoods: Geofabrik India **Central Zone** OSM extract (`central-zone-260916_osm.pbf`), `place=city|town|suburb|neighbourhood|quarter` nodes. Points were matched to Madhya Pradesh by nearest LGD village (tightened to ~15km) and cross-checked against the OSM `postal_code`/`addr:postcode` tag (MP PIN prefixes 45–48) where present, which excluded a batch of Uttar Pradesh border towns near Rewa/Satna (Karchana, Naini, Koraon, Shankargarh, Rajapur, etc.) that an earlier pass had pulled in.
- GeoNames `IN.txt` was checked for MP (`admin1 code 35`) but contains no `PPLX` (neighbourhood) records for this state, so it was not used as a locality source here (unlike Chhattisgarh).
- No India Post pincode extract was available for this state, so post-office localities are not included.

## Districts: 55, matching the current official count
The source LGD village survey predates Madhya Pradesh's 2023 district reorganisation, so it originally
carried 52 districts. Three districts created in October 2023 were split out here to match today's map:
- **Maihar** — from Satna (talukas: Maihar, Amarpatan, Ramnagar)
- **Pandhurna** — from Chhindwara (talukas: Pandhurna, Sausar)
- **Mauganj** — from Rewa (talukas: Mauganj, Hanumana, Naigarhi)

Villages and unmatched polygons were moved by their exact taluka name (authoritative — no guessing).
Cities/wards were reassigned by nearest-village geographic lookup against the post-split taluka
boundaries, since ward/OSM records don't carry a taluka field. "East Nimar" (LGD's old name) was
renamed to "Khandwa" to match current usage; all other district names are as in the source survey.

## Numbers
- **55** districts, **416** talukas (subdistricts) — names as in LGD
- **42,945** villages with a usable name (in `dropdown_data` / `rich_data` / index)
- **4,626** LGD polygons with no village name/LGD code → `unmatched_names.json` per district (SOI label kept in `soi_name` where available)
- **419** cities/towns (235 with SBM ward names, 184 OSM-only with a `town_center` fallback)
- **4,166** ward localities, plus **149** neighbourhood/suburb/quarter localities from OSM, plus **184** `town_center` fallback points
- **47,863** entries in `madhya_pradesh_places_index.json`

## Folders (same layout as Chhattisgarh/Rajasthan)
- `<DISTRICT>.json` — `{district, talukas:{Taluka:[villages]}, cities:{City:{name, place_type, lat, lon, localities}}}`
- `dropdown_data/<DISTRICT>.json` — `{Taluka:[village names]}`
- `rich_data/<DISTRICT>/<TALUKA>/villages.json` — `name, lgd_code, lat, lon, boundary_wkt` (`lat`/`lon` = polygon centroid)
- `rich_data/<DISTRICT>/subdistricts.json`, `unmatched_names.json`
- `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — wards (`type: "ward"`, centroid `lat`/`lon` + `boundary_wkt`), OSM neighbourhoods, or a single `town_center` fallback
- `state_district_map.json`, `madhya_pradesh_places_index.json` (no polygons)

## How cities were built
SBM ULBs were cleaned (suffixes like `Nagar Palika`, `(NP)`, `Nagar Nigam`, `_U` removed) and matched to OSM `place=city|town` points by name for `place_type` and grouping; a city's `lat`/`lon` is the average centroid of its ward polygons where SBM data exists, otherwise the OSM point. Districts missing on a ward or OSM record were assigned to the nearest LGD village polygon's district.

## Known gaps
- 8 districts (Ashoknagar, Bhind, Datia, Guna, Morena, Sheopur, Shivpuri, Niwari) have **no SBM ward data** — their towns use OSM points only, each with a single `town_center` locality.
- 2,104 SBM ward rows in MP were blank, purely numeric, or "Ward N" only, and were dropped rather than kept as unnamed wards.
- Real neighbourhood coverage (OSM only, no GeoNames or India Post for this state) is thin outside the biggest cities.
- Same-named wards inside one city are merged into one locality.
- No city boundary files; ward polygons are simplified from source.
- OSM border filtering (see Sources) targets known leakage patterns; a residual handful of near-border OSM towns without a postal_code tag may still be misassigned in either direction.
