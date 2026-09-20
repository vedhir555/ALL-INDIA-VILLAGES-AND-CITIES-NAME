# Himachal Pradesh, Jammu & Kashmir, Ladakh — Data (OSM-based rebuild)

## Why these three are built differently from the rest of the repo
LGD (the official village-boundary survey used for every other state in this repo) has **no
polygon coverage at all** for HP, J&K, or Ladakh — confirmed by checking both the November-2023
LGD village snapshot and the newer 2024 nationwide bharatlas snapshot (584,615 villages) directly;
neither includes these three. So unlike MP/UP/etc., there is no official village list or boundary
source here — everything below comes from OpenStreetMap, via a Geofabrik "northern-zone" extract
(covers Punjab, Haryana, Delhi, Chandigarh, Rajasthan, HP, J&K, Ladakh — filtered here to just the
latter three).

## What replaced the previous placeholder data
This overwrites an earlier, much thinner build that existed in the repo for all three: that version
only had town/tehsil-headquarters-level points (e.g. all of Ladakh was 28 entries total; Shimla
district, which has thousands of villages, had 47). It also mislabeled Ladakh's 6 tehsils
(Drass, Kargil, Leh, Nubra, Sham, Zanskar) as "districts" — Ladakh only has 2 real districts,
**Leh** and **Kargil**; those 6 names are tehsils within them.

## How this build works
1. **Districts**: matched by exact name against OSM `boundary=administrative` relations (12/12 HP,
   20/20 J&K, 2/2 Ladakh all matched — mostly `admin_level=5`, a handful of J&K districts and both
   Ladakh districts at `admin_level=6` / suffixed `"<name> district"`).
2. **Talukas/tehsils**: any named `admin_level=6–8` boundary whose centroid falls inside a matched
   district becomes a taluka (115 in HP, 62 in J&K, 3 in Ladakh). Coverage is uneven — HP is well
   mapped (every village lands in a real tehsil polygon); large parts of Ladakh (all of Leh district)
   and part of Srinagar have **no mapped tehsil boundaries in OSM at all**, so villages there (296 in
   Leh, 20 in Srinagar) were grouped by nearest OSM town instead — a stand-in, not an official tehsil.
3. **Villages**: every OSM `place=village|hamlet|isolated_dwelling` node inside a matched district,
   plus any separately-mapped village *polygon* with no matching point, added directly.
4. **Boundaries**: real polygons only where OSM actually mapped one as a closed way or multipolygon
   relation — checked and type-verified (many "boundary" ways in this data are actually open,
   unclosed line fragments; those were discarded rather than saved as fake polygons). Real polygon
   coverage is thin: 84 of 16,879 HP villages, 186 of 4,584 J&K villages, 15 of 640 Ladakh villages.
   Every other village has a real OSM-sourced point (`lat`/`lon`) and `boundary_wkt: null`.
5. **Cities/towns**: every OSM `place=city|town` node/polygon. **No SBM ward data exists for these
   three** (Swachh Bharat Mission's dataset doesn't cover them either), so localities come entirely
   from OSM `suburb|neighbourhood|quarter|locality` points attached to the nearest city (≤8km); a
   city with none gets a single `town_center` fallback entry.

## Numbers
| | Districts | Talukas | Villages | villages w/ real boundary | Cities/towns | places_index |
|---|---|---|---|---|---|---|
| Himachal Pradesh | 12 | 115 | 16,879 | 84 | 82 | 17,165 |
| Jammu & Kashmir | 20 | 62 | 4,584 | 186 | 70 | 4,891 |
| Ladakh | 2 | 3 | 640 | 15 | 3 | 677 |

## Known gaps
- Village *lists* are only as complete as OSM's mapping in each area — HP's dense village mapping
  makes it fairly thorough; Ladakh's sparse population and terrain mean real coverage is almost
  certainly lower than the true village count (Leh district alone has 100+ administrative villages;
  OSM maps 296 named settlements there, so probably reasonably close, but this is not a verified
  exhaustive list the way LGD is elsewhere in this repo).
- No `lgd_code` — none exists for these states.
- Real ("true") boundary polygons are rare; the large majority of villages are point-only, which is
  a structural limit of OSM's India coverage, not something a different pipeline would fix.
- Tehsil/taluka boundaries are missing entirely in parts of Ladakh and Srinagar; those villages are
  grouped by nearest town as a practical stand-in, not an authoritative tehsil assignment.
- Kashmir-region place names are politically sensitive in places; names are taken as-is from OSM
  without alteration.
