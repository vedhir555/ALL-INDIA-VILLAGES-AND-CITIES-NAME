# Maharashtra, Goa & Dadra and Nagar Haveli and Daman and Diu — Data

Built the same way as the existing Gujarat dataset in this repo, from:
- `LGD_Villages.geojsonl` (official LGD/Census-SOI village boundary survey, all-India) — villages
- `western-zone-260916_osm.pbf` (Geofabrik OSM extract covering Gujarat, Maharashtra,
  Goa, and Dadra and Nagar Haveli and Daman and Diu) — cities, towns and localities

No ward-level data is included for these states (by request) — only villages,
cities/towns, and named localities/neighbourhoods.

## Coverage

| State | Districts | Villages (named) | Cities/Towns | Localities |
|---|---|---|---|---|
| Maharashtra | 36 | 44,025 | ~420 | ~1,850 |
| Goa | 2 | 362 | ~20 | ~120 |
| Dadra and Nagar Haveli and Daman and Diu | 3 | 85 | ~5 | ~25 |

(Counts approximate — see each state's `*_places_index.json` for exact totals.)

## Folders (same layout per state as Gujarat)

Each state has its own top-level district JSON files (`<DISTRICT>.json`), its
own `dropdown_data/` and `rich_data/` trees, its own `state_district_map.json`,
and its own `<state>_places_index.json` flat search index. They are **siblings**
of the existing Gujarat files, not merged into them — copy each state's folders
into the repo root and merge the `dropdown_data/`, `rich_data/`, and
`state_district_map.json` contents (see "Merging" below).

- `rich_data/<DISTRICT>/<TALUKA>/villages.json` — village name, LGD code, lat/lon
  centroid, and a simplified boundary polygon (WKT), same shape as Gujarat's.
- `rich_data/<DISTRICT>/subdistricts.json` — taluka name + LGD code + folder name.
- `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — named localities /
  neighbourhoods (OSM `place=neighbourhood|suburb|quarter|locality`) assigned to
  their nearest city/town. Where OSM has no mapped neighbourhoods for a town,
  the town's own point is listed as the sole entry (same fallback Gujarat uses).
- `rich_data/<DISTRICT>/CITIES/<CITY>/boundary.json` — only present where OSM
  had an actual polygon for that city/town (a minority — see gaps below).
- `dropdown_data/<DISTRICT>.json` — `{ "Taluka": ["Village1", ...] }`.
- `<DISTRICT>.json` (top level) — `{"places": [{name, sub, type, lat, lng, lgd_code}, ...]}`.
- `state_district_map.json` — `{ "Maharashtra": [...districts...] }` (one per state).
- `<state>_places_index.json` — flat search index (villages + cities + localities),
  same compact schema as `gujarat_places_index.json` (`n/t/d/p/lat/lon`).

## How cities & localities were built (no ward data used)

LGD's village polygons only cover rural revenue villages, not city/town extents,
so cities came entirely from OSM: every `place=city`/`place=town` node or
polygon in the OSM extract was matched to its LGD district by testing which
taluka boundary polygon (OSM `admin_level=6`) contains it, using the taluka
names already resolved from the LGD village data. Neighbourhood/suburb/quarter/
locality points were then assigned to the nearest city/town within the same
district (within ~12 km).

## Known gaps

- **Village names**: ~9% of Maharashtra's LGD village records and ~6% of Goa's
  have no name in either the survey field or the linked Gram Panchayat field
  (uninhabited/forest revenue villages) — these are dropped, same as Gujarat's
  `unmatched_names` villages, but no name-recovery pass was run since there's
  no legacy reference list to recover against for these states.
- **Taluka boundary matching**: about 358 of ~365 Maharashtra/Goa/DNH&DD taluka
  names matched OSM boundary polygons cleanly (a handful of spelling variants,
  e.g. district-name-only headquarters talukas, weren't resolved). Any
  city/town or locality whose point fell inside one of the ~7 unmatched taluka
  areas isn't included, so the true city/locality count is a bit higher than
  what's here — this is the single biggest gap.
- **City boundaries**: only 28 cities/towns across all three states have a real
  OSM polygon (`boundary.json`); the rest are point-only, same "has_boundary:
  false" fallback pattern as roughly half of Gujarat's towns.
- **Localities**: like Gujarat, OSM has mapped neighbourhood names for only a
  fraction of towns — smaller towns fall back to a single self-referencing
  locality entry.

## Merging into the existing repo

1. Copy `MAHARASHTRA.json`, `GOA*.json`, `DADRA...json` etc. (all top-level
   `<DISTRICT>.json` files from each state folder) into the repo root.
2. Copy each state's `dropdown_data/*.json` into the existing `dropdown_data/`.
3. Copy each state's `rich_data/<DISTRICT>/` folders into the existing
   `rich_data/`.
4. Merge each state's `state_district_map.json` into the existing one (it's
   currently `{"Gujarat": [...]}`; add `"Maharashtra": [...]`, `"Goa": [...]`,
   `"Dadra and Nagar Haveli and Daman and Diu": [...]` as sibling keys).
5. Either keep `maharashtra_places_index.json` / `goa_places_index.json` /
   `dnhdd_places_index.json` as separate search indexes, or concatenate their
   arrays into `gujarat_places_index.json` and rename it something
   state-neutral (e.g. `all_india_places_index.json`) if the search feature
   should span all four regions at once.
