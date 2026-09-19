# Northern states (Punjab, Haryana, Delhi, Chandigarh, Himachal Pradesh, Jammu and Kashmir, Ladakh) — Data

Built the same way as the Gujarat / Maharashtra / Goa / DNH&DD layout in this repo, from:
- `LGD_Villages.geojsonl` (all-India LGD/Census village polygons) — villages
- `SBM_Wards.parquet` (Swachh Bharat Mission ward polygons) — the list of cities/ULBs and their footprints (ward polygons are unioned into one city boundary; **no ward names or ward records are stored**)
- `northern-zone-260916_osm.pbf` (Geofabrik OSM, 2026-09-16) — real locality names (`place=suburb|neighbourhood|quarter|locality`) with coordinates, OSM district/state boundaries

## Coverage

| State | Districts | Talukas | Villages | Unnamed (in unmatched_names.json) | Cities/Towns | Real OSM localities | Cities with only a town-centre fallback |
|---|---|---|---|---|---|---|---|
| Punjab | 23 | 80 | 12,181 | 441 | 187 (164 SBM + 23 OSM-only) | 151 | 160 |
| Haryana | 22 | 81 | 6,477 | 230 | 106 (81 SBM + 25 OSM-only) | 343 | 89 |
| Delhi | 11 | 27 | 212 | 163 | 3 (3 SBM + 0 OSM-only) | 990 | 0 |
| Chandigarh | 1 | 1 | 11 | 11 | 1 (1 SBM + 0 OSM-only) | 55 | 0 |
| Himachal Pradesh | 12 | 0 | 0 | 0 | 95 (58 SBM + 37 OSM-only) | 93 | 78 |
| Jammu and Kashmir | 20 | 0 | 0 | 0 | 85 (64 SBM + 21 OSM-only) | 98 | 66 |
| Ladakh | 6 | 0 | 0 | 0 | 7 (1 SBM + 6 OSM-only) | 18 | 3 |
| **Total** | 95 | 189 | 18,881 | 845 | 484 | 1,748 | 396 |

**Villages exist only for Punjab, Haryana, Delhi and Chandigarh.** The supplied LGD file contains no Himachal Pradesh, Jammu and Kashmir or Ladakh records, so those three states have cities and localities only (no `dropdown_data/`, no village files).

## Layout (per state folder)
- `<DISTRICT>.json` — `{"places":[...]}` villages `{name, sub(taluka), type, lat, lng, lgd_code}`, cities `{name, sub, type, lat, lng}`, localities `{name, sub(city), type, lat, lng}`
- `dropdown_data/<DISTRICT>.json` — `{Taluka: [unique village names, sorted]}` (LGD states only)
- `rich_data/<DISTRICT>/<TALUKA>/villages.json` — `name, lgd_code, lat, lon, boundary_wkt`
- `rich_data/<DISTRICT>/subdistricts.json` — `[{name, lgd_code, folder}]`; `unmatched_names.json` — LGD rows with no usable name
- `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` — `name, type, lat, lon, has_boundary` (`has_boundary` = the OSM feature was a polygon; the polygon itself is not stored)
- `rich_data/<DISTRICT>/CITIES/<CITY>/boundary.json` — `name, lat, lon, boundary_wkt` (union of that city's SBM ward polygons; only for SBM cities)
- `<state>_places_index.json` — flat search index, keys `n/t/d/p/lat/lon`, types `village|city|locality`
- `state_district_map.json` — `{"<State>": [districts]}`
- Root `state_district_map.json` in this package merges every state in the repo (previously it only listed Gujarat).

## Method notes
- Village `lat/lon` = polygon centroid (6 dp); `boundary_wkt` = Douglas-Peucker `simplify(0.0003, preserve_topology=True)`, 7 dp. This transform was regression-tested against the existing Rajasthan files (names and lat/lon identical on 913/913 villages, WKT identical on 912/913).
- LGD rows sharing the same code + name + taluka (one village split into parts) are merged into one record; different villages that merely share a code are kept separate.
- Village names are LGD `vilname11`; rows with a blank name or no letters go to `unmatched_names.json`. Census-urban markers such as `(CT)`, `(OG)`, `(M)` are kept as in Gujarat.
- Cities: every SBM ULB inside the state polygon (validated spatially against OSM state boundaries) plus OSM `place=city|town` points that no SBM footprint covers (`OSM-only`, point only, no `boundary.json`).
- Localities: OSM named suburb/neighbourhood/quarter/locality points or polygon centroids inside a city footprint, or within 500 m of one **in the same state**. A city with none gets one `type: "town"` entry at its centre (same fallback as Gujarat/Maharashtra).
- Districts: OSM district polygons for Punjab/Haryana (mapped to the LGD district names so cities sit beside their villages), Himachal, J&K, Ladakh; nearest LGD villages for Delhi.

## Known gaps
- No village data for Himachal Pradesh, Jammu and Kashmir, Ladakh (not in the LGD file).
- SBM `districtname` is blank for most Punjab/Haryana cities, so districts come from geometry. Banur (Punjab) is ambiguous: OSM containment says Patiala, SBM says S.A.S. Nagar (Mohali).
- Delhi's Municipal Corporation spans several districts but is filed under one; all its localities are listed under it.
- Delhi and Chandigarh LGD rows are heavily unnamed (163 of 382 and 11 of 22).
- Ladakh's Changthang district is not in the OSM extract; SBM has a single Ladakh ULB (Leh, 2 wards), so most Ladakh towns are OSM-only points.
- HP/J&K/Ladakh place=locality points outside city footprints are mostly natural/rural places and are not included.
- District names follow LGD (Punjab/Haryana/Delhi) or OSM (others) at data date; SBM city names were cleaned (administrative prefixes such as "Municipal Council" removed, `Dulb Haryana` renamed Gurugram, `800120` resolved to Naina Devi via OSM).
- A few border villages/localities lie up to ~0.6 km outside the OSM state outline (outline precision).
