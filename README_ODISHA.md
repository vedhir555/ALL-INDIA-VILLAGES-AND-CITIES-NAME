# Odisha — Villages, Cities & Ward Locations (data)

Same layout as Bihar, Jharkhand and the north-eastern states (v2): `ODISHA/<DISTRICT>.json`, `dropdown_data/`, `rich_data/`,
`state_district_map.json`, `odisha_places_index.json`. Copy the `ODISHA` folder into the repo root.

## Sources
- Villages: `LGD_Villages.geojsonl` — 30 districts, 476 talukas (sub-districts), 52,663 polygons.
- Cities/towns: SBM ULB ward polygons + OSM `place=city|town` (`eastern-zone-260916_osm.pbf`).
- Ward locations: names found inside each SBM ward polygon (OSM first, then GeoNames, LGD village names, SBM ward name).

## Numbers
| Districts | Talukas | Villages | of which LGD | Cities/towns | with SBM wards | Locations |
|---|---|---|---|---|---|---|
| 30 | 476 | 49,472 | 49,467 | 183 | 102 | 1,327 |

## Village fields
`name, lgd_code, lat, lon, boundary_wkt` (polygon simplified 0.0001°). `lat/lon` = polygon centroid, or an interior point when the
centroid falls outside. Polygons sharing one LGD code inside a taluka are merged (179 merges, MULTIPOLYGON). 3,017 polygons with no
LGD name and no code are in `unmatched_names.json` (with `soi_name`). 5 villages outside every LGD polygon come from OSM/GeoNames (`lgd_code: null`, `source` set).

## Location (ward) fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt`
- `lat/lon` = the location's own coordinates. `centroid_lat/lon` = centroid of the SBM ward polygon containing it;
  `boundary_wkt` = that ward polygon (simplified 0.00005°).
- Towns without SBM wards: centroid = `lat/lon`, no `boundary_wkt`. `town_center` = town point only.
- `source` values: `osm`, `osm_landuse`, `osm_addr`, `geonames`, `lgd_village`, `sbm_ward`, `town_center`.

## Ward names
SBM has 1,745 unique Odisha wards after removing duplicate versions (1,752 raw rows). 1,335 of the ward names are generic ("Ward 12").
- **OSM names 189 wards**, at least one name (any source) 711 wards, **1,034 wards have no name** and are not listed.
- `sbm_ward` rows (407) use the ward's interior point as `lat/lon`; list-type ward names are split into rows (max 6), so those rows share coordinates.
- Junk OSM names (buildings, "apartment", house names) were removed.

## City notes
- SBM had 107 ULB labels with mixed suffixes ("(M)", "(Nac)", "N.A.C", "Town (M)", "Municipality"); they are cleaned and merged into 102 towns.
  Names use OSM spelling when an OSM town lies inside the ULB (Kendujhargarh, Brahmapur); Bhubaneswar keeps the official spelling.
- SBM has about 20 ward rows with the ULB label "Canacona" (a Goa town name). Their polygons are in Odisha (Barbil, Kesinga area), so they are named from the nearest OSM town.
- Twelve SBM rows carry the state label "Goa" with Odisha's code (21); they are included as Odisha.
- OSM towns inside another town's ward set (for example Jajpur Road inside Byasanagar) are listed as locations of that town.
- 81 towns come from OSM only; 92 cities have a town-centre entry only.

## Known gaps
- SBM covers 102 of Odisha's urban bodies.
- OSM `town` tags include some large villages. Names such as `(NP)` / `(CT)` in the village lists are LGD urban polygons, kept as-is like other states.
