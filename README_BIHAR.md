# Bihar — Villages, Cities & Ward Locations (data)

Same layout as the north-eastern states (v2): `BIHAR/<DISTRICT>.json`, `BIHAR/dropdown_data/`, `BIHAR/rich_data/`,
`BIHAR/state_district_map.json`, `BIHAR/bihar_places_index.json`. Copy the `BIHAR` folder into the repo root.

## Sources
- Villages: `LGD_Villages.geojsonl` — all 38 districts, 533 talukas (sub-districts), 43,332 polygons.
- Cities/towns: SBM ULB ward polygons (58 ULBs) + OSM `place=city|town` (`eastern-zone-260916_osm.pbf`).
- Ward locations: names found inside each SBM ward polygon (see "Ward names" below).

## Numbers
| Districts | Talukas | Villages | of which LGD | Cities/towns | with SBM wards | Locations |
|---|---|---|---|---|---|---|
| 38 | 533 | 41,784 | 41,773 | 187 | 58 | 2,236 |

## Village fields
`name, lgd_code, lat, lon, boundary_wkt` (polygon simplified 0.0001°). `lat/lon` = polygon centroid, or an interior point when the
centroid falls outside. Polygons that share one LGD code inside the same taluka are merged into one record (MULTIPOLYGON).
185 polygons that have an LGD code but no LGD name use the Survey of India name. 507 polygons with neither are in
`unmatched_names.json` (with `soi_name`). 11 villages outside every LGD polygon come from OSM/GeoNames (`lgd_code: null`, `source` set).

## Location (ward) fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt`
- `lat/lon` = the location's own coordinates. `centroid_lat/lon` = centroid of the SBM ward polygon containing it;
  `boundary_wkt` = that ward polygon (simplified 0.00005°).
- Towns without SBM wards: centroid = `lat/lon`, no `boundary_wkt`. `town_center` = town point only.
- `source` values: `osm`, `osm_landuse`, `osm_addr`, `geonames`, `lgd_village`, `sbm_ward`, `town_center`.
  Filter on `source` if you only want OSM names.

## Ward names
SBM has 1,890 unique Bihar wards after removing duplicate versions (2,502 raw rows; Patna alone had 552 duplicate "Ward N" fragments).
- **OSM names only 70 wards** (of 1,890). OSM in Bihar has very few mapped neighbourhoods; junk names (buildings, "apartment", house names) were removed.
- Wards with no OSM name fall back to GeoNames PPLX/PPLL/PPL, LGD village names inside the ward, then the SBM ward name **only if it is a real
  name** (not "Ward 12", "One", "Twenty"). `sbm_ward` rows use the ward's interior point as `lat/lon`; list-type ward names are split into
  separate rows (max 6), so those rows share the same coordinates.
- 1,592 wards have at least one name; **298 wards have none** (generic "Ward N" names and nothing else inside them) and are not listed.

## City notes
- The SBM ULB called "Danapur" also contains Kishanganj's 34 wards; they are split out and named Kishanganj.
- "Patna Municipal Corporation" is merged into Patna. City names use OSM spelling when an OSM city/town lies inside the ULB (Arrah, Chhapra, Bihar Sharif, Mokama).
- City `lat/lon` = centroid of its SBM ward polygons, else the OSM point. 129 towns come from OSM only; 119 of them have no locations (town centre only).

## Known gaps
- SBM covers only 58 of Bihar's urban bodies; the other towns have no ward data.
- OSM `town` tags include some large villages. Names inside `(NP)`, `(CT)`, `(Nagar Parishad)` in the village lists are LGD urban polygons, kept as-is like other states.
- Ward and village polygons are simplified.
