# Gujarat Villages, Cities & Localities — Data

Gujarat-only. No other states in this repo.

## Folders

### `/dropdown_data/`
33 files, one per district (e.g. `AHMADABAD.json`, `BANAS KANTHA.json`).
Flat format: `{ "TalukaName": ["Village1", "Village2", ...] }` — no
coordinates, just names. This is what a State→District→Taluka dropdown
picker needs. Villages come from the official LGD government survey;
city-only "talukas" (Ahmedabad's Asarva/Vatva/Vejalpur zones, Surat's
Puna/Adajan zones, Vadodara's 4 zones, Rajkot's 3 zones, etc.) are kept
from the older reference data since LGD only covers rural villages.

### `/rich_data/`
Full detail tree: `rich_data/<DISTRICT>/<TALUKA>/villages.json` — every
village with `name`, `lgd_code`, `lat`, `lon`, and a full `boundary_wkt`
polygon. `rich_data/<DISTRICT>/CITIES/<CITY>/` has `wards.json`
(ward name + coordinates), `localities.json` (named neighbourhoods, where
mapped), and `boundary.json` (city outline polygon). Also has
`unmatched_names.json` and `recovered_villages.json` per district —
names from the old reference data that couldn't be matched to an LGD
village record, and ones later recovered via OpenStreetMap.

### `gujarat_places_index.json`
Flat, single-file search index — 17,947 entries (villages, cities,
wards, localities) with just `name`, `type`, `district`, `parent`,
`lat`, `lon`. No boundary polygons (too heavy for a live search field).
This is what the search-by-typing feature loads.

### `state_district_map.json`
`{ "GUJARAT": [ ...33 district names... ] }` — kept for compatibility
with code that expects this top-level shape.

## Known gaps

- Coverage is Gujarat only.
- `localities.json` exists for roughly half of the 204 cities/towns —
  smaller towns often have no OpenStreetMap-mapped neighbourhood names.
- Villages under `unmatched_names.json` per district are the ones that
  didn't survive the match against LGD; small numbers per district
  (typically under 2%).
