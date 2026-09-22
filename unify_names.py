#!/usr/bin/env python3
# =============================================================================
# unify_names.py  -  give every place ONE name in the whole repo
#
# HOW TO RUN (PowerShell):
#   1. git pull                      (get the latest repo first)
#   2. cd to the repo folder         (the one that has state_district_map.json)
#   3. python unify_names.py         (changes the files)
#      python unify_names.py --dry-run   (only writes the reports, changes nothing)
#   4. Look at the two report files it prints at the end.
#   5. If happy:  git add -A ; git commit -m "Unify duplicate place names" ; git push
#      If NOT happy:  git checkout .     (throws every change away)
#
# WHAT IT CHANGES (names only - it never moves a place and never edits coordinates):
#   * districts  : "BANAS KANTHA" / "BANAS_KANTHA"  -> one spelling
#   * cities     : "Ahmadabad (M Corp.)" / "Ahmedabad" -> "Ahmedabad", also in the
#                  city field of every locality / ward that belongs to it
#   * talukas    : "SONAPUR" / "Sonapur" -> one spelling
#   * localities and wards in the same city that are the same place
#                  ("Nehru Nagar" / "Nehrunagar", within 1.5 km) -> one spelling
#   * villages   : same government (LGD) code, names differ only by spaces /
#                  capitals / punctuation, less than 3 km apart -> one spelling
#   * junk text  : "Dholka/Td&Gt;" -> "Dholka", double spaces -> one space
#   * one more thing: 5 Gujarat districts + Lahaul and Spiti are listed TWICE in
#                  their *_places_index.json (once as "BANAS KANTHA", once as
#                  "BANAS_KANTHA"). The second copy of each row is removed so the
#                  index matches the district files again. Nothing else is deleted.
# Both the district files and the *_places_index.json files are updated the same
# way, so they always agree. state_district_map.json is not touched.
#
# WHAT IT ONLY REPORTS (needs a human): places that might be the same but the
# data is not sure enough - see needs_review_*.csv.
# =============================================================================
import csv, glob, json, math, os, re, sys, collections, datetime

DRY = '--dry-run' in sys.argv
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
ROOT = os.path.abspath(ARGS[0] if ARGS else '.')

AREA_MAX_KM = 1.5      # locality/ward variants further apart than this are only reported
VILLAGE_MAX_KM = 3.0   # same-LGD village variants further apart than this are only reported


# ---------------------------------------------------------------- helpers ----
def junk(s):
    """strip the stray '/Td&Gt;' text and tidy spaces"""
    s = re.sub(r'/?td&gt;', '', str(s if s is not None else ''), flags=re.I)
    return re.sub(r'\s+', ' ', s).strip()

# Only these bracket suffixes mean "type of town" and may be dropped from a CITY
# name ("Halol (M)" -> "Halol").  Other brackets like "(East)" or "(Rajnagar)" are
# part of the name and are never dropped.
MUNI = {'m', 'imc', 'm corp.', 'm corp', 'm.corp', 'm.corp.', 'm.cop', 'td.', 'td', 'town', 'ct', 'np', 'mb', 'cb', 'og'}
# Correct spellings to use when the data has two spellings of the same city.
# Add your own here if the script picks a spelling you do not like.
PREFER_CITY = ['Ahmedabad', 'Ankleshwar', 'Umerkote', 'Shehera']

def has_paren(s):   return '(' in s
def unbalanced(s):  return s.count('(') != s.count(')')
def city_base(s):
    def cut(m):
        return '' if m.group(1).strip().lower() in MUNI else m.group(0)
    b = re.sub(r'\s*\(([^)]*)\)', cut, s).strip()
    return b or s
def keep(s):        return re.sub(r'[^a-z0-9]', '', s.lower())          # text in ( ) is kept
def cfold(s):       return keep(city_base(s)).replace('e', 'a') or s.lower()   # Ahmadabad == Ahmedabad
def dk(s):          return re.sub(r'[^A-Z0-9]', '_', junk(s).upper())
def letters(s):     return [c for c in s if c.isalpha()]
def shout(s):       return bool(letters(s)) and s == s.upper()
def small(s):       return bool(letters(s)) and s == s.lower()
def mixed(s):       return not shout(s) and not small(s)
def spaces(s):      return s.count(' ')
def title(s):       return re.sub(r'[A-Za-z]+', lambda m: m.group(0).capitalize(), s)
def clean_case(s): return not re.search(r'[a-z][A-Z]', s)   # 'Danilimda' ok, 'DaniLimda' not

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))

def spread(pts):
    return max((km(a, b) for i, a in enumerate(pts) for b in pts[i + 1:]), default=0.0)

def load(path):
    return json.loads(open(path, 'rb').read().decode('utf-8'))

def dump(path, obj):
    # same compact style the repo already uses
    open(path, 'wb').write(json.dumps(obj, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))


# --------------------------------------------------- plan for one district ----
def plan_district(rows, state, dist, review, att):
    """rows = list of place dicts of ONE district (already junk-cleaned).
       att = how many times each (lower-case) name is used anywhere in the state;
       when two spellings are equal otherwise, the one used more in the state wins.
       returns {'city':{}, 'taluka':{}, 'area':{}, 'village':{}}"""
    A = lambda s: att[s.lower()]
    plan = {'city': {}, 'taluka': {}, 'area': {}, 'village': {}}

    # ---- cities: names of city rows + the 'sub' of localities/wards -----------
    forms = collections.defaultdict(collections.Counter)      # group -> raw form -> children
    for r in rows:
        if r['type'] == 'city':
            forms[cfold(r['name'])][r['name']] += 0
        elif r['type'] in ('locality', 'ward') and r['sub']:
            forms[cfold(r['sub'])][r['sub']] += 1
    for g, c in forms.items():
        if len(c) < 2:
            continue
        best = sorted(c, key=lambda s: (unbalanced(s), has_paren(s), -A(s), not clean_case(s), s))[0]
        for pref in PREFER_CITY:
            if any(city_base(f).lower() == pref.lower() for f in c):
                best = pref
        if shout(best) or small(best):
            best = title(best)
        for old in c:
            if old != best:
                plan['city'][old] = best

    # ---- talukas: village 'sub' that differ only by capitals/spaces/punctuation
    tf = collections.defaultdict(collections.Counter)
    for r in rows:
        if r['type'] == 'village' and r['sub']:
            tf[keep(r['sub'])][r['sub']] += 1
    bases = collections.defaultdict(set)
    for r in rows:
        if r['type'] == 'village' and r['sub']:
            bases[re.sub(r'\s*\([^)]*\)', '', r['sub']).strip().lower()].add(r['sub'])
    for g, c in tf.items():
        if len(c) < 2:
            continue
        best = sorted(c, key=lambda s: (unbalanced(s), -spaces(s), not clean_case(s), -A(s), s))[0]
        if shout(best) or small(best):
            best = title(best)
        for old in c:
            if old != best:
                plan['taluka'][old] = best
    for b, s in bases.items():                       # "Gossaigaon" vs "Gossaigaon (Pt)"
        ks = {keep(x) for x in s}
        if len(ks) > 1:
            review.append([state, dist, 'taluka name with/without suffix', ' | '.join(sorted(s)), '', '',
                           'may be the same place or two different parts - not changed'])

    # ---- localities / wards inside the same (renamed) city --------------------
    groups = collections.defaultdict(list)
    for r in rows:
        if r['type'] in ('locality', 'ward') and r['sub']:
            city = plan['city'].get(r['sub'], r['sub'])
            groups[(city, keep(r['name']))].append(r)
    for (city, _), rs in groups.items():
        c = collections.Counter(r['name'] for r in rs)
        if len(c) < 2:
            continue
        pts = [(r['lat'], r['lng']) for r in rs]
        d = spread(pts)
        if d > AREA_MAX_KM:
            review.append([state, dist, 'locality/ward spelled differently but far apart (%s)' % city,
                           ' | '.join(sorted(c)), '', '%.1f km' % d, 'not changed'])
            continue
        best = sorted(c, key=lambda s: (unbalanced(s), has_paren(s), -A(s), not clean_case(s), spaces(s), s))[0]
        if shout(best) or small(best):
            best = title(best)
        for old in c:
            if old != best:
                plan['area'][(city, old)] = best

    # ---- villages: same LGD code ----------------------------------------------
    bycode = collections.defaultdict(list)
    for r in rows:
        if r['type'] == 'village' and r.get('lgd_code') is not None:
            bycode[r['lgd_code']].append(r)
    for code, rs in bycode.items():
        c = collections.Counter(r['name'] for r in rs)
        if len(c) < 2:
            continue
        d = spread([(r['lat'], r['lng']) for r in rs])
        if len({keep(n) for n in c}) == 1 and d <= VILLAGE_MAX_KM:
            best = sorted(c, key=lambda s: (-A(s), spaces(s), s))[0]
            for r in rs:
                if r['name'] != best:
                    sub = plan['taluka'].get(r['sub'], r['sub'])
                    plan['village'][(sub, r['name'], r['lat'], r['lng'])] = best
        else:
            why = 'different spelling, not just spaces/capitals' if len({keep(n) for n in c}) > 1 else 'too far apart'
            review.append([state, dist, 'villages share LGD code %s (%s)' % (code, why),
                           ' | '.join(sorted(c)), rs[0]['sub'], '%.1f km' % d,
                           'could be two villages with a wrong shared code - not changed'])

    # ---- same taluka, same name apart from spaces, DIFFERENT LGD codes -------
    vg = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in rows:
        if r['type'] == 'village':
            vg[(r['sub'], keep(r['name']))][r['name']].add(r.get('lgd_code'))
    for (sub, _), c in vg.items():
        if len(c) > 1:
            codes = set().union(*c.values())
            if len(codes) > 1:
                review.append([state, dist, 'villages in same taluka spelled with/without space',
                               ' | '.join(sorted(c)), sub, '', 'different LGD codes = probably two real villages - not changed'])
    return plan


def apply_row(r, plan):
    """returns list of (field, old, new) changes; modifies r"""
    ch = []
    t = r.get('type')
    def setf(f, v):
        if r.get(f) != v:
            ch.append((f, r.get(f), v)); r[f] = v
    if t == 'city':
        setf('name', plan['city'].get(r['name'], r['name']))
    elif t in ('locality', 'ward'):
        setf('sub', plan['city'].get(r['sub'], r['sub']))
        setf('name', plan['area'].get((r['sub'], r['name']), r['name']))
    elif t == 'village':
        setf('sub', plan['taluka'].get(r['sub'], r['sub']))
        setf('name', plan['village'].get((r['sub'], r['name'], r['lat'], r['lng']), r['name']))
    return ch


# ------------------------------------------------------------------- main ----
def main():
    if not os.path.exists(os.path.join(ROOT, 'state_district_map.json')):
        sys.exit('Run this inside the repo folder (the one containing state_district_map.json), '
                 'or pass the folder: python unify_names.py "C:\\path\\to\\repo"')

    changes = collections.Counter()      # (state, district, kind, old, new) -> rows
    review = []
    files_changed = 0
    per_kind = collections.Counter()

    states = sorted(d for d in os.listdir(ROOT)
                    if os.path.isdir(os.path.join(ROOT, d)) and glob.glob(os.path.join(ROOT, d, '*_places_index.json')))
    for st in states:
        folder = os.path.join(ROOT, st)
        idx_path = glob.glob(os.path.join(folder, '*_places_index.json'))[0]
        dfiles = sorted(p for p in glob.glob(os.path.join(folder, '*.json')) if p != idx_path)
        plans = {}                                   # district key -> plan
        filecount = {}                               # district key -> rows the district file holds

        # 1) district files: clean, plan, apply
        objs = {}
        att = collections.Counter()
        for p in dfiles:
            obj = load(p)
            for r in obj['places']:
                for f in ('name', 'sub'):
                    cleaned = junk(r.get(f))
                    if cleaned != r.get(f) and r.get(f) not in (None, ''):
                        changes[(st, os.path.basename(p)[:-5], f, r.get(f), cleaned)] += 1
                    r[f] = cleaned
                    if cleaned:
                        att[cleaned.lower()] += 1
            objs[p] = obj
        for p in dfiles:
            dist = os.path.basename(p)[:-5]
            obj = objs[p]
            rows = obj['places']
            plan = plan_district(rows, st, dist, review, att)
            plans[dk(dist)] = plan
            for r in rows:
                for f, old, new in apply_row(r, plan):
                    changes[(st, dist, f, old, new)] += 1
            filecount[dk(dist)] = collections.Counter(
                (r['type'], r['name'], r['sub'], r['lat'], r['lng']) for r in rows)
            before = open(p, 'rb').read()
            out = json.dumps(obj, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
            if out != before:
                files_changed += 1
                if not DRY: open(p, 'wb').write(out)
        objs = None

        # 2) index file: same plans, plus one spelling of the district field
        rows = load(idx_path)
        forms = collections.defaultdict(collections.Counter)
        for r in rows:
            forms[dk(r['district'])][junk(r['district'])] += 1
        canon = {}
        for k, c in forms.items():
            best = sorted(c, key=lambda s: ('_' in s, -c[s], s))[0]
            canon[k] = best
            if len(c) > 1:
                for old in c:
                    if old != best:
                        changes[(st, k, 'district', old, best)] += c[old]
        kept, used = [], collections.defaultdict(collections.Counter)
        for r in rows:
            r['name'] = junk(r.get('name')); r['sub'] = junk(r.get('sub'))
            key = dk(r['district'])
            r['district'] = canon[key]
            if key in plans:
                apply_row(r, plans[key])
                k = (r['type'], r['name'], r['sub'], r['lat'], r['lng'])
                if used[key][k] >= filecount[key][k]:        # listed more often than in the district file
                    changes[(st, key, 'index row listed twice - removed', '(second copy)', '(removed)')] += 1
                    continue
                used[key][k] += 1
            kept.append(r)
        rows = kept
        before = open(idx_path, 'rb').read()
        out = json.dumps(rows, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        if out != before:
            files_changed += 1
            if not DRY: open(idx_path, 'wb').write(out)

        # 3) district folders that look like the same district under two names
        codes = {}
        for p in dfiles:
            codes[os.path.basename(p)[:-5]] = {r.get('lgd_code') for r in load(p)['places']
                                                if r['type'] == 'village' and r.get('lgd_code') is not None}
        names = sorted(codes)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if codes[a] and codes[b]:
                    ov = len(codes[a] & codes[b]) / min(len(codes[a]), len(codes[b]))
                    if ov >= 0.5:
                        review.append([st, a + ' / ' + b, 'two district files hold the same villages',
                                       a + ' | ' + b, '', '%d%% overlap' % round(ov * 100),
                                       'same district under two names? merge by hand - not changed'])
        print('  done', st)

    # ---- reports (outside the repo so they are never committed by accident) ---
    rep = os.path.join(os.path.dirname(ROOT), 'name_reports')
    os.makedirs(rep, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ('_dryrun' if DRY else '')
    with open(os.path.join(rep, 'name_changes_' + stamp + '.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(['state', 'district', 'field', 'old name', 'new name', 'rows changed'])
        for (st, d, fld, old, new), n in sorted(changes.items()):
            w.writerow([st, d, fld, old, new, n])
    with open(os.path.join(rep, 'needs_review_' + stamp + '.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow(['state', 'district', 'what', 'names', 'taluka / city', 'distance', 'note'])
        for row in review:
            w.writerow(row)

    print()
    print('DRY RUN - nothing was changed.' if DRY else 'Files rewritten: %d' % files_changed)
    print('Name changes (distinct old->new):', len(changes), ' rows touched:', sum(changes.values()))
    print('Needs a human look:', len(review), 'items')
    print('Reports are in:', rep)


if __name__ == '__main__':
    main()
