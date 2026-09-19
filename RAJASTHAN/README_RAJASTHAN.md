# Rajasthan Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (official LGD government survey, all-India) — filtered to Rajasthan.
- District boundaries, cities/towns and localities: Geofabrik's India **Northern Zone** OSM extract (`northern-zone-260916_osm.pbf`).

## Numbers
- **40,102** total LGD village records for Rajasthan
- **35,892** villages with a usable name, written into `dropdown_data` / `rich_data`
- **4,210** villages had a blank name in the LGD source and are filed under each district's `unmatched_names.json` instead
- **41 districts** (the current scheme after the December 2024 reorganisation), **317 talukas**
- **392** cities/towns from OSM (`place=city`/`town`), each placed inside a real Rajasthan district boundary
- **676** locality entries across those cities (see gap note below)

## District scheme (41 districts)
The LGD village file uses Census 2011 codes, i.e. 33 districts. The 8 districts kept after the 2023 reorganisation were carved out of it:
Balotra (from Barmer), Beawar (from Ajmer, Pali, Bhilwara), Deeg (from Bharatpur), Didwana-Kuchaman (from Nagaur), Khairthal-Tijara (from Alwar), Kotputli-Behror (from Alwar, Jaipur), Phalodi (from Jodhpur), Salumbar (from Udaipur).

Every LGD village was placed in a district by testing its polygon's interior point against the OSM district boundary. Talukas keep their LGD (Census) names. Three talukas straddle a new district border and appear under both districts: Thanagazi (Alwar / Kotputli-Behror), Osian (Jodhpur / Phalodi) and Shergarh (Jodhpur / Phalodi). A handful of villages (1–5 per taluka) that fell just across a border because of boundary mismatch were kept with the rest of their taluka.

Folder and file names are upper case; the district `Ganganagar` is Sri Ganganagar, `Dholpur` is Dhaulpur.

## Folders
### `/dropdown_data/`
One file per district (e.g. `AJMER.json`). Flat format: `{ "TalukaName": ["Village1", "Village2", ...] }` — no coordinates, just names, matching the Gujarat/Maharashtra convention.

### `/rich_data/`
Full detail tree: `rich_data/<DISTRICT>/<TALUKA>/villages.json` — every village with `name`, `lgd_code`, `lat`, `lon` (polygon centroid), `boundary_wkt` (polygon simplified to about 30 m).
`rich_data/<DISTRICT>/subdistricts.json` — taluka names + village counts for that district.
`rich_data/<DISTRICT>/unmatched_names.json` — LGD records with no usable name.
`rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — named localities (neighbourhood/suburb/quarter), **no ward names**.

### Top-level `<DISTRICT>.json`
Merged view combining that district's talukas (with villages) and cities (with localities) in one file.

### `rajasthan_places_index.json`
Flat, single-file search index — **36,599 entries** (villages, cities, localities) with `name`, `type`, `district`, `parent`, `lat`, `lon`. No boundary polygons.

### `state_district_map.json`
`{ "RAJASTHAN": [...41 district names...] }`

## Known gaps
- **City-to-district matching now uses the real OSM district outlines** (40 of 41 districts). Chittorgarh's outline is missing from the OSM extract, so its area was rebuilt from its village polygons (with a small buffer). Earlier versions used approximate convex hulls, which wrongly pulled Haryana, Punjab and Gujarat towns (Gurgaon, Rewari, Sirsa, Fazilka, etc.) into Rajasthan districts; those are removed.
- **Locality coverage is thin**: only **31 of 392 cities** (~8%) have real OSM-mapped neighbourhood/suburb/quarter names, assigned to the nearest city within 15 km. The rest have a single `town_center` entry at the town's own point. This reflects sparse OSM mapping in Rajasthan, not a processing gap.
- When two towns in one district share a name (Hanumangarh, Ramgarh in Sikar), only one is kept.
- Talukas are the 2011 Census subdistricts; newer talukas created since then are not represented.
