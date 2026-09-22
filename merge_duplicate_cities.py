#!/usr/bin/env python3
# =============================================================================
# merge_duplicate_cities.py  -  one ROW per city (run AFTER unify_names.py)
#
# unify_names.py already gave every place one NAME. It renamed city rows but
# never deleted one, so a few cities that used to be spelled two ways are now
# spelled the same but still have TWO rows in the data - for example Ahmedabad
# has one row from the old "Ahmadabad (M Corp.)" spelling and one row from the
# old "Ahmedabad" spelling, at two slightly different points on the map.
# This script keeps ONE row per city and removes the extra one(s).
#
# HOW TO RUN (PowerShell, inside the repo folder - the one with
# state_district_map.json):
#   python merge_duplicate_cities.py --dry-run     (only writes the report)
#   python merge_duplicate_cities.py                (changes the files)
#   git add -A ; git commit -m "Merge duplicate city rows" ; git push
#   If NOT happy:  git checkout .
#
# WHICH ROW IS KEPT: the one whose old `sub` text still matches the most
# locality/ward rows in that file (that is the city's real, well-used point).
# If it's a tie, the coordinates of the tied rows are averaged into one point.
# Every locality/ward keeps its own name and coordinates - only the CITY row
# is affected, and a locality/ward is never deleted or moved.
# =============================================================================
import csv, glob, json, os, re, sys, collections, datetime

def dnorm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())

DRY = '--dry-run' in sys.argv
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
ROOT = os.path.abspath(ARGS[0] if ARGS else '.')


def load(path):
    return json.loads(open(path, 'rb').read().decode('utf-8'))

def dump_bytes(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def merge_file(path, state, report):
    """Collapse duplicate city rows inside one district file. Returns the
    mapping {old (name,sub,lat,lng) -> kept (name,sub,lat,lng)} for this
    district, used to also collapse the state index below."""
    obj = load(path)
    rows = obj['places']
    dist = os.path.basename(path)[:-5]

    by_name = collections.defaultdict(list)
    for r in rows:
        if r['type'] == 'city':
            by_name[r['name']].append(r)

    keep_map = {}          # id(old row) -> kept row dict (by value)
    drop = set()            # ids of rows to remove from `rows`
    for name, group in by_name.items():
        if len(group) < 2:
            continue

        def kidcount(r):
            return sum(1 for q in rows
                       if q['type'] in ('locality', 'ward') and q['sub'] == r['sub'])

        counts = [(kidcount(r), r) for r in group]
        counts.sort(key=lambda x: -x[0])
        top = counts[0][0]
        winners = [r for c, r in counts if c == top]

        if len(winners) == 1:
            kept = dict(winners[0])
        else:
            # tie: average the coordinates, keep the shortest/plainest sub text
            kept = dict(sorted(winners, key=lambda r: (len(r['sub']), r['sub']))[0])
            kept['lat'] = round(sum(r['lat'] for r in winners) / len(winners), 6)
            kept['lng'] = round(sum(r['lng'] for r in winners) / len(winners), 6)

        for _, r in counts:
            key = (r['name'], r['sub'], r['lat'], r['lng'])
            keep_map[key] = kept
        for r in group:
            if r is not (winners[0] if len(winners) == 1 else None):
                pass  # handled by identity check below
        # mark every row in the group except one physical object for removal
        keeper_obj = winners[0] if len(winners) == 1 else None
        removed_here = []
        for r in group:
            if keeper_obj is not None and r is keeper_obj:
                continue
            drop.add(id(r))
            removed_here.append(r['sub'])
        if keeper_obj is None:
            # tie-break made a brand-new averaged row: drop ALL originals,
            # keep the averaged one by inserting it once
            for r in group:
                drop.add(id(r))
            rows.append(kept)
            removed_here = [r['sub'] for r in group]
        report.append([state, dist, name,
                        ' | '.join(sorted(set(removed_here))), kept['sub'],
                        kept['lat'], kept['lng']])

    new_rows = [r for r in rows if id(r) not in drop]
    obj['places'] = new_rows
    before = open(path, 'rb').read()
    out = dump_bytes(obj)
    changed = out != before
    if changed and not DRY:
        open(path, 'wb').write(out)
    return dist, keep_map, changed


def merge_index(idx_path, per_dist_maps, report_extra):
    rows = load(idx_path)
    kept_seen = collections.defaultdict(set)   # dist-key -> set of kept (name,sub,lat,lng)
    out = []
    for r in rows:
        if r['type'] != 'city':
            out.append(r)
            continue
        dist_key = dnorm(r['district'])
        keymap = per_dist_maps.get(dist_key)
        key = (r['name'], r['sub'], r['lat'], r['lng'])
        if keymap and key in keymap:
            kept = keymap[key]
            sig = (kept['name'], kept['sub'], kept['lat'], kept['lng'])
            if sig in kept_seen[dist_key]:
                continue                        # duplicate city row in the index - drop it
            kept_seen[dist_key].add(sig)
            r = dict(r)
            r['name'], r['sub'], r['lat'], r['lng'] = kept['name'], kept['sub'], kept['lat'], kept['lng']
        out.append(r)
    before = open(idx_path, 'rb').read()
    o = dump_bytes(out)
    if o != before and not DRY:
        open(idx_path, 'wb').write(o)
    return o != before


def main():
    if not os.path.exists(os.path.join(ROOT, 'state_district_map.json')):
        sys.exit('Run this inside the repo folder (the one containing state_district_map.json).')

    report = []
    files_changed = 0
    states = sorted(d for d in os.listdir(ROOT)
                    if os.path.isdir(os.path.join(ROOT, d))
                    and glob.glob(os.path.join(ROOT, d, '*_places_index.json')))
    for st in states:
        folder = os.path.join(ROOT, st)
        idx_path = glob.glob(os.path.join(folder, '*_places_index.json'))[0]
        dfiles = sorted(p for p in glob.glob(os.path.join(folder, '*.json')) if p != idx_path)

        per_dist_maps = {}
        for p in dfiles:
            dist, keymap, changed = merge_file(p, st, report)
            if keymap:
                per_dist_maps[dnorm(dist)] = keymap
            if changed:
                files_changed += 1

        if per_dist_maps and merge_index(idx_path, per_dist_maps, report):
            files_changed += 1
        print('  done', st)

    rep = os.path.join(os.path.dirname(ROOT), 'name_reports')
    os.makedirs(rep, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ('_dryrun' if DRY else '')
    with open(os.path.join(rep, 'city_merges_' + stamp + '.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['state', 'district', 'city', 'old sub-names removed', 'kept sub', 'kept lat', 'kept lng'])
        for row in report:
            w.writerow(row)

    print()
    print('DRY RUN - nothing was changed.' if DRY else 'Files rewritten: %d' % files_changed)
    print('City rows merged:', len(report))
    print('Report:', os.path.join(rep, 'city_merges_' + stamp + '.csv'))


if __name__ == '__main__':
    main()
