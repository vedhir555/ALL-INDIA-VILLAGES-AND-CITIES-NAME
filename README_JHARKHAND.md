# Jharkhand — Villages, Cities & Ward Locations (data)

Same layout as Bihar and the north-eastern states (v2): `JHARKHAND/<DISTRICT>.json`, `dropdown_data/`, `rich_data/`,
`state_district_map.json`, `jharkhand_places_index.json`. Copy the `JHARKHAND` folder into the repo root.

## Sources
- Villages: `LGD_Villages.geojsonl` — 24 districts, 264 talukas (sub-districts), 32,931 polygons.
- Cities/towns: SBM ULB ward polygons + OSM `place=city|town` (`eastern-zone-260916_osm.pbf`).
- Ward locations: names found inside each SBM ward polygon (OSM first, then GeoNames, LGD village names, SBM ward name).

## Numbers
| Districts | Talukas | Villages | of which LGD | Cities/towns | with SBM wards | Locations |
|---|---|---|---|---|---|---|
| 24 | 264 | 31,893 | 31,889 | 103 | 39 | 772 |

## Village fields
`name, lgd_code, lat, lon, boundary_wkt` (polygon simplified 0.0001°). `lat/lon` = polygon centroid, or an interior point when the
centroid falls outside. Polygons sharing one LGD code inside a taluka are merged (581 merges, MULTIPOLYGON). 461 polygons with no
name and no code are in `unmatched_names.json` (with `soi_name`). 4 villages outside every LGD polygon come from OSM/GeoNames (`lgd_code: null`, `source` set).
The taluka `Nawadiha Bazar/Nawadiha*` keeps that name in the JSON; its folder is `Nawadiha Bazar-Nawadiha-` (`/` and `*` are not allowed in Windows folder names).

## Location (ward) fields
`name, type, lat, lon, centroid_lat, centroid_lon, source, boundary_wkt`
- `lat/lon` = the location's own coordinates. `centroid_lat/lon` = centroid of the SBM ward polygon containing it;
  `boundary_wkt` = that ward polygon (simplified 0.00005°).
- Towns without SBM wards: centroid = `lat/lon`, no `boundary_wkt`. `town_center` = town point only.
- `source` values: `osm`, `osm_landuse`, `geonames`, `lgd_village`, `sbm_ward`, `town_center`.

## Ward names
SBM has 850 unique Jharkhand wards after removing duplicate versions (868 raw rows). 857 of the 868 SBM ward names are generic
("Ward 12"), so SBM names were almost never usable (7 rows).
- **OSM names 220 wards**, at least one name (any source) 365 wards, **485 wards have no name** and are not listed.
- Junk OSM names (buildings, "apartment", house names) were removed.
- OSM hamlets and villages inside ward polygons are listed with their own `type` (hamlet/village).

## City notes
- SBM had 49 ULB labels for 39 towns (spelling and type variants, e.g. "Madhupur (Nagar Parishad)"); they are merged.
  Names use OSM spelling when an OSM town lies inside the ULB (Jhumri Telaiya, Chakradharpur, Hazaribagh).
- OSM towns lying inside another town's ward set (Sindri, Jharia, Loyabad, Barkakana) are listed as locations of that town, not as separate cities.
- 64 towns come from OSM only; 51 cities have a town-centre entry only.

## Known gaps
- SBM covers only about 39 of Jharkhand's urban bodies.
- OSM `town` tags include some large villages. Names such as `(NP)` / `(CT)` in the village lists are LGD urban polygons, kept as-is like other states.
