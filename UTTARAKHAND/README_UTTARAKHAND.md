# Uttarakhand Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (official LGD/Census-SOI village boundary survey, all-India) — filtered to Uttarakhand.
- City wards: `SBM_Wards.parquet` (Swachh Bharat Mission urban ward polygons). Ward **numbers are not used** — only the ward's place name; the ward polygon centroid is its `lat`/`lon`.
- Cities/towns and neighbourhoods: Geofabrik India **Central Zone** OSM extract (`central-zone-260916_osm.pbf`).
- Neighbourhoods: GeoNames `IN.txt`, feature code `PPLX` (section of populated place), attached to the nearest city in the same district (within ~5 km of its ward outlines or centre).
- Neighbourhoods: India Post All India Pincode Directory (data.gov.in extract, May 2025, via GitHub `imriadutta/pincode-india`) — sub-office (S.O.) names only, with valid coordinates that fall inside a city's ward outlines; suffixes like "S.O" removed, government/institution offices filtered out.

## Numbers
- **13** districts, **80** talukas (subdistricts) — names as in LGD
- **14,157** villages with a usable name (in `dropdown_data` / `rich_data` / index)
- **3,344** LGD polygons with no village name/LGD code → `unmatched_names.json` per district (2,753 carry a Survey of India label in `soi_name`)
- **112** cities/towns (69 with SBM ward names, 29 town-centre only)
- **934** ward localities, plus **177** neighbourhood/suburb/quarter localities from OSM and GeoNames (44 from GeoNames, 67 from India Post)
- **15,380** entries in `uttarakhand_places_index.json`

## Folders (same layout as Rajasthan)
- `<DISTRICT>.json` — `{district, talukas:{Taluka:[villages]}, cities:{City:{name, place_type, lat, lon, localities}}}`
- `dropdown_data/<DISTRICT>.json` — `{Taluka:[village names]}`
- `rich_data/<DISTRICT>/<TALUKA>/villages.json` — `name, lgd_code, lat, lon, boundary_wkt` (`lat`/`lon` = polygon centroid)
- `rich_data/<DISTRICT>/subdistricts.json`, `unmatched_names.json`
- `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — wards (`type: "ward"`, centroid `lat`/`lon` + `boundary_wkt`), neighbourhoods, or a single `town_center` fallback
- `state_district_map.json`, `uttarakhand_places_index.json` (no polygons)

## How cities were built
SBM ULBs were cleaned (suffixes like `(NP)`, `Nagar Palika`, `_U` removed; spelling variants merged), then combined with OSM `place=city|town` points. A city's `lat`/`lon` is the centroid of its ward polygons where SBM exists, otherwise the OSM point. Districts come from the nearest LGD village polygon.

## Known gaps
- Ward names are as entered in SBM: 125 of the 934 ward localities end in "Ward" (many named after people/gods, not neighbourhoods). 32 SBM ward names were dropped as empty or number-only.
- Same-named wards inside one city are merged into one locality.
- Real neighbourhood coverage (OSM + GeoNames) is thin outside the biggest cities; 29 cities have only a `town_center` entry.
- OSM-only "towns" include some places mapped as `town` that are small villages.
- No city boundary files (same as Rajasthan); ward polygons are simplified.
