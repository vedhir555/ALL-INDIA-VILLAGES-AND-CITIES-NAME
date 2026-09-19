# West Bengal — Villages, Cities & Locations (data)

Same layout as Bihar, Jharkhand, Odisha and the north-eastern states (v2): `WEST BENGAL/<DISTRICT>.json`, `dropdown_data/`,
`rich_data/`, `state_district_map.json`, `west_bengal_places_index.json`. Copy the `WEST BENGAL` folder into the repo root.

## Sources
- Villages: `LGD_Villages.geojsonl` — 23 districts, 341 talukas (sub-districts), 40,890 polygons.
- Cities/towns: OSM `place=city|town` (`eastern-zone-260916_osm.pbf`) + SBM ULB ward polygons (only 7 ULBs).
- Locations: OSM neighbourhood / suburb / quarter / locality names, GeoNames PPLX/PPLL.

## Numbers
| Districts | Talukas | Villages | Cities/towns | with SBM wards | Locations |
|---|---|---|---|---|---|
| 23 | 341 | 38,848 | 211 | 7 | 896 |

## Village fields
`name, lgd_code, lat, lon, boundary_wkt` (polygon simplified 0.0001°). `lat/lon` = polygon centroid, or an interior point when the
centroid falls outside. Polygons sharing one LGD code inside a taluka are merged (279 merges, MULTIPOLYGON). 1,763 polygons with no
LGD name and no code are in `unmatched_names.json` (with `soi_name`).

## Location fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt`
- Towns without SBM wards (204 of 211): centroid = `lat/lon`, no `boundary_wkt`. `town_center` = town point only (133 towns).
- SBM ward towns (7): `centroid_lat/lon` = centroid of the ward polygon containing the location; `boundary_wkt` = that ward polygon.
- `source` values: `osm`, `osm_landuse`, `geonames`, `lgd_village`, `sbm_ward`, `town_center`.

## Ward data
SBM has only **7 West Bengal ULBs (183 wards)**: Naihati, Serampore, Madhyamgram, Krishnanagar, Habra, Basirhat, Baidyabati.
182 of the 183 ward names are generic ("Ward N"). 24 wards have a name (10 from OSM); 159 have none and are not listed.

## How locations were attached to towns (no ward polygons for most towns)
- An OSM neighbourhood/suburb/quarter/locality is attached to a town when it lies inside that town's LGD urban polygon
  (`Name (M)`, `(M Corp.)`, `(CT)`), or inside an unnamed or urban LGD polygon and within about 12 km of the town; otherwise only if within about 3 km.
- West Bengal mappers tag many villages as `suburb` (about 2,000 in South 24 Parganas: Gangasagar, Namkhana, Mathurapur and so on).
  Those are already in the LGD village list, so they are **not** attached to towns.
- Kolkata's LGD polygons are mostly unnamed, so Kolkata's neighbourhoods are attached by the rule above.

## Known gaps
- Most bigger towns (Durgapur, Asansol, Howrah, Siliguri) have few or no mapped neighbourhoods in OSM.
- OSM `city` and `town` tags include some large villages.
- Names such as `(CT)` / `(M)` in the village lists are LGD urban polygons, kept as-is like other states.
