# Rajasthan Villages, Cities & Localities — Data

## Sources
- Villages: `LGD_Villages.geojsonl` (official LGD government survey, all-India) — filtered to Rajasthan.
- Cities/towns and localities: Geofabrik's India **Northern Zone** OSM extract (`northern-zone-260916_osm.pbf`), which covers Rajasthan, Punjab, Haryana, Delhi, UP, Uttarakhand, HP, and J&K/Ladakh.

## Numbers
- **40,102** total LGD village records for Rajasthan
- **35,892** villages with a usable name, written into `dropdown_data` / `rich_data`
- **4,210** villages had a blank/placeholder name in the LGD source and are filed under each district's `unmatched_names.json` instead
- **33 districts**, **317 talukas** (subdistricts)
- **433** cities/towns matched from OSM (`place=city`/`town`) to a Rajasthan district
- **836** locality entries across those cities (see gap note below)

## Folders
### `/dropdown_data/`
One file per district (e.g. `AJMER.json`). Flat format: `{ "TalukaName": ["Village1", "Village2", ...] }` — no coordinates, just names, matching the Gujarat/Maharashtra convention.

### `/rich_data/`
Full detail tree: `rich_data/<DISTRICT>/<TALUKA>/villages.json` — every village with `name`, `lgd_code`, `lat`, `lon`, `boundary_wkt`.
`rich_data/<DISTRICT>/subdistricts.json` — taluka names + village counts for that district.
`rich_data/<DISTRICT>/unmatched_names.json` — LGD records with no usable name.
`rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — named localities (neighbourhood/suburb/quarter), **no ward names**.

### Top-level `<DISTRICT>.json`
Merged view combining that district's talukas (with villages) and cities (with localities) in one file.

### `rajasthan_places_index.json`
Flat, single-file search index — **36,769 entries** (villages, cities, localities) with `name`, `type`, `district`, `parent`, `lat`, `lon`. No boundary polygons.

### `state_district_map.json`
`{ "RAJASTHAN": [...33 district names...] }`

## Known gaps
- **District boundaries used for city-matching were approximated as convex hulls** built from the union of each district's village polygons (not the true jagged district outline), since no separate taluka/district boundary layer was supplied. This is accurate enough to assign a city to the correct district, but the hull itself isn't stored or meant for drawing district outlines.
- **Two districts (Bikaner, Hanumangarh)** had self-intersecting village polygons in the source LGD data that broke the normal union operation; their hulls were rebuilt from village centroids only. City assignment for these two districts is slightly less precise as a result, though still checked against known district city lists.
- **Locality coverage is much thinner than Gujarat/Maharashtra**: only **41 of 433 cities** (~9%) have real OSM-mapped neighbourhood/suburb/quarter names. The rest fall back to the town's own center point as a single "locality" entry (`type: "town_center"`), the same convention used for small Gujarat towns with no mapped neighbourhoods. This reflects genuinely sparse OSM community mapping in Rajasthan outside a handful of large cities (Jaipur, Alwar, Sikar, Udaipur, etc.) — not a processing gap.
- District names use the pre-2023 33-district scheme (matching what's in the LGD survey data), not Rajasthan's newer 50-district reorganization.
