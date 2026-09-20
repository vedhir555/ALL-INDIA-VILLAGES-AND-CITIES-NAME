# Andhra Pradesh — Villages, Cities & Localities — Data

## Districts (2026)
Andhra Pradesh has **28 districts** as of 31 December 2025: the 26 districts of 2022 plus **Markapuram** (carved from Prakasam) and **Polavaram** (carved from Alluri Sitharama Raju, headquarters Rampachodavaram). A third proposed district, Madanapalle, was dropped; Madanapalle became the headquarters of Annamayya district instead. The reorganisation also moved mandals between 17 of the existing districts.
LGD (2023) still uses the old 26-district structure and older spellings (`Ntr`, `Spsr Nellore`, `Y.S.R.`, `Visakhapatanam`). To get the 2026 districts, each mandal (LGD subdistrict) was assigned to the district that contains most of its villages according to the current OSM district boundaries, so whole mandals move together. **1,484 villages** moved to a different district than in LGD (Markapuram 444 villages / 21 mandals, Polavaram 496 / 11 mandals, plus mandal transfers between Annamayya, Tirupati, YSR Kadapa, Chittoor, Nellore, Prakasam, Bapatla, Konaseema, East Godavari, Eluru and West Godavari); a further 1,767 villages only changed the spelling of their district's name. No mandal had an ambiguous district vote. District boundaries follow OSM; a mandal-level check against the official 2025 notification is recommended.

## Sources
- Villages: `LGD_Villages.geojsonl` (Andhra Pradesh, state code 37)
- City outlines: `SBM_Wards.parquet` (SBM urban ward polygons merged into one outline per city). **Ward names are not used.**
- Cities/towns and neighbourhoods: Geofabrik OSM Southern Zone extract (2026-09-16)
- Not used: GeoNames and India Post neighbourhood names (the files were not available for this build), and SBM ward names.

## Coordinates (every record)
- `lat` / `lon` — **map pin**: a point guaranteed to lie inside the boundary (for point-only records it is the point itself). In the rich `villages.json` files, as in the other states, `lat`/`lon` hold the geometric centroid.
- `centroid_lat` / `centroid_lon` — geometric centroid
- `boundary_wkt` — outline (villages, city outlines, OSM neighbourhoods that have one)

## Numbers
| | Count |
|---|---|
| Districts | 28 |
| Talukas (mandals) with named villages | 666 |
| Villages with names | 14,463 |
| LGD polygons with no usable name/code (`unmatched_names.json`) | 980 (562 carry a Survey of India label in `soi_name`; reserved-forest labels are blanked) |
| Cities/towns | 194 (104 SBM + 90 OSM-only points) |
| City outlines (`boundary.json`) | 104 |
| OSM neighbourhood/suburb/quarter names | 1,535 |
| Cities with only a town-centre entry | 93 |
| Search-index entries | 16,192 |

## Layout (same as Karnataka / Tamil Nadu / Rajasthan)
`<DISTRICT>.json` = `{district, talukas, cities}`; `dropdown_data/`; `rich_data/<DISTRICT>/<TALUKA>/villages.json`; `subdistricts.json`; `unmatched_names.json`; `rich_data/<DISTRICT>/CITIES/<CITY>/localities.json` + `boundary.json`; `andhra_pradesh_places_index.json`; `state_district_map.json`. Village boundaries use `simplify(0.00003)` at 6 decimals, the same transform as the other schema-B states (checked against Tamil Nadu: 99.96% of village records identical). City outlines merge the ward polygons into one clean outline (gaps of about 55 m closed).

## Name fixes
- SBM's ULB `Gvmc` (97 wards) is Greater Visakhapatnam and is listed as `Visakhapatnam`.
- SBM ULB `900064` is labelled `Gudur` but sits on the OSM town Atmakuru (Nellore district); it is listed as `Atmakur` (a separate Atmakur in Nandyal district is a different ULB).
- 14 SBM city names were replaced by the matching OSM spelling, as in the other states (for example `Chilakalurpet` to `Chilakaluripet`, `Guntukal` to `Guntakal`). `Rajahmundry` and `Palacole` are kept as SBM spells them (OSM: Rajamahendravaram, Palakollu).

## Known gaps
- SBM ward district labels are the old 13-district ones, so they were not used.
- SBM lists 104 urban bodies; the state has more, so 90 towns are OSM-only points with no outline (some are census towns or small places tagged `place=town`).
- About 2,600 SBM ward names look like real locality names (for example `Pappu Bazar`) but were not added, because ward names were excluded for this build.
- OSM `place=locality` points are not used (only suburb, neighbourhood, quarter), as in Karnataka and Tamil Nadu.
- Some mandals created or renamed in 2025 (for example Peddaharivanam, Vasavi Penugonda) are not in LGD.
- Greater Visakhapatnam and Vijayawada outlines come from SBM wards and may differ from current municipal limits.
- OSM names in Telugu script only were skipped (English name used when present).
