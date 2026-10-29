import json, re, sys
import numpy as np
import pandas as pd
from rapidfuzz import fuzz

D = '..'

# ---------- pair mapping (kurd -> control) and metadata, from the study config ----------
PAIRS = [
 ('Shanidar Cave', 'Postojna Cave', 'slovenia'),
 ('Korek Mountain', 'Zugspitze', 'germany'),
 ('Sami Abdulrahman Park', 'Englischer Garten', 'germany'),
 ('Rawanduz Canyon', 'Verdon Gorge', 'france'),
 ('Barzan Area', 'Lauterbrunnen Valley', 'switzerland'),
 ('Soran Area', 'Berchtesgaden', 'germany'),
 ('Hendrin Mountain', 'Ben Nevis', 'scotland'),
 ('Dukan Lake', 'Lake Bled', 'slovenia'),
 ('Azmar Mountain', "Arthur's Seat", 'scotland'),
 ('Ahmad Awa Waterfall', 'Krimml Waterfalls', 'austria'),
 ('Hawraman Region', 'Cinque Terre', 'italy'),
 ('Qaradagh Area', 'Peak District', 'england'),
 ('Sirwan River Area', 'Soca River', 'slovenia'),
 ('Amedi', 'Ronda', 'spain'),
 ('Lalish', 'Meteora', 'greece'),
 ('Akre', 'Gruyeres', 'switzerland'),
 ('Gali Duhok', 'Cheddar Gorge', 'england'),
 ('Zakho', 'Mostar', 'bosnia'),
 ('Shaqlawa', 'Zakopane', 'poland'),
 ('Darbandikhan Lake', 'Lake Annecy', 'france'),
 ('Darband Lake (Ranya)', 'Lake Wanaka', 'new zealand'),
 ('Gali Ali Bag Waterfall', 'Gullfoss', 'iceland'),
 ('Halgurd Mountain', 'Mount Olympus', 'greece'),
 ('Przhe Mountain', 'Triglav', 'slovenia'),
 ('Bekhal Waterfall', 'Marmore Falls', 'italy'),
 ('Sulav Resort', 'Bad Gastein', 'austria'),
 ('Zawita Valley', 'Black Forest', 'germany'),
 ('Gara Mountain', 'Mont Ventoux', 'france'),
 ('Safeen Mountain', 'Mount Pilatus', 'switzerland'),
 ('Piramagrun Mountain', 'Tre Cime di Lavaredo', 'italy'),
 ('Goizha Mountain', 'Mount Royal', 'canada'),
 ('Penjwen Area', 'Lake District', 'england'),
 ('Mergapan Valley', 'Alpe di Siusi', 'italy'),
 ('Dore Canyon', 'Samaria Gorge', 'greece'),
 ('Great Zab River', 'Tara River', 'montenegro'),
 ('Khalifan Area', 'Zillertal', 'austria'),
 ('Chami Rezan Valley', 'Vezere Valley', 'france'),
 ('Sartka Mountain', 'Oludeniz', 'turkey'),
 ('Smaquli Valley', 'Glen Coe', 'scotland'),
]
K2C = {k: c for k, c, _ in PAIRS}
COUNTRY = {k: ['iraq', 'kurdistan'] for k, _, _ in PAIRS}
COUNTRY.update({c: [cc] for _, c, cc in PAIRS})

ALIASES = {
 'Shanidar Cave': ['shanidar'], 'Korek Mountain': ['korek', 'kurek'],
 'Sami Abdulrahman Park': ['sami abdul rahman'],
 'Rawanduz Canyon': ['rawanduz', 'rowanduz', 'rwanduz'], 'Barzan Area': ['barzan'],
 'Soran Area': ['soran'], 'Hendrin Mountain': ['hendrin', 'handren'],
 'Dukan Lake': ['dukan', 'dokan'], 'Azmar Mountain': ['azmar', 'azmer'],
 'Ahmad Awa Waterfall': ['ahmadawa', 'ahmed awa'],
 'Hawraman Region': ['hawraman', 'hewraman', 'avroman', 'uraman'],
 'Qaradagh Area': ['qaradagh', 'qara dagh'], 'Sirwan River Area': ['sirwan', 'diyala'],
 'Amedi': ['amadiya', 'amadiyah', 'amedy'], 'Lalish': ['lalish temple'],
 'Akre': ['aqrah', 'akre town'], 'Gali Duhok': ['duhok valley', 'dohuk'],
 'Zakho': ['delal bridge', 'dalal'], 'Shaqlawa': ['shaqlawa', 'shaqlava'],
 'Darbandikhan Lake': ['darbandikhan'],
 'Darband Lake (Ranya)': ['ranya', 'darband ranya', 'darbandi ranya'],
 'Gali Ali Bag Waterfall': ['geli ali beg', 'gali ali beg', 'ali beg'],
 'Halgurd Mountain': ['halgurd', 'halgord'], 'Przhe Mountain': ['przhe', 'pirza'],
 'Bekhal Waterfall': ['bekhal', 'bexal'], 'Sulav Resort': ['sulav', 'sulaf'],
 'Zawita Valley': ['zawita', 'zawite'], 'Gara Mountain': ['gara', 'matin'],
 'Safeen Mountain': ['safeen', 'safin'], 'Piramagrun Mountain': ['piramagrun', 'pira magrun'],
 'Goizha Mountain': ['goizha', 'goyzha'], 'Penjwen Area': ['penjwen', 'penjween'],
 'Mergapan Valley': ['mergapan', 'merga pan'], 'Dore Canyon': ['dore', 'dora canyon'],
 'Great Zab River': ['great zab', 'greater zab', 'zab'], 'Khalifan Area': ['khalifan'],
 'Chami Rezan Valley': ['chami rezan', 'chami razan'], 'Sartka Mountain': ['sartka'],
 'Smaquli Valley': ['smaquli', 'smaquli resan'],
 'Postojna Cave': ['postojna'], 'Zugspitze': [], 'Englischer Garten': ['english garden'],
 'Verdon Gorge': ['gorges du verdon'], 'Lauterbrunnen Valley': ['lauterbrunnen'],
 'Berchtesgaden': [], 'Ben Nevis': [], 'Lake Bled': ['bled'],
 "Arthur's Seat": ['arthurs seat'], 'Krimml Waterfalls': ['krimml'], 'Cinque Terre': [],
 'Peak District': [], 'Soca River': ['soča'], 'Ronda': [], 'Meteora': [],
 'Gruyeres': ['gruyères'], 'Cheddar Gorge': [], 'Mostar': ['stari most'],
 'Zakopane': [], 'Lake Annecy': ["lac d'annecy"], 'Lake Wanaka': ['wanaka'],
 'Gullfoss': [], 'Mount Olympus': ['olympus'], 'Triglav': [],
 'Marmore Falls': ['cascata delle marmore'], 'Bad Gastein': [],
 'Black Forest': ['schwarzwald'], 'Mont Ventoux': [], 'Mount Pilatus': ['pilatus'],
 'Tre Cime di Lavaredo': ['tre cime', 'drei zinnen'], 'Mount Royal': ['mont royal'],
 'Lake District': [], 'Alpe di Siusi': ['seiser alm'], 'Samaria Gorge': ['samaria'],
 'Tara River': ['tara canyon'], 'Zillertal': ['ziller valley'],
 'Vezere Valley': ['vézère'], 'Oludeniz': ['ölüdeniz', 'babadag'],
 'Glen Coe': ['glencoe'],
}
ALIAS = {p: [p] + a for p, a in ALIASES.items()}

def norm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', str(s).lower()).strip()

def score_rows(rows):
    out = []
    for r in rows:
        ca = norm(r['country_ans'])
        country_ok = int(any(c in ca for c in COUNTRY[r['place']]))
        na = norm(r['name_ans'])
        gold = [norm(a) for a in ALIAS[r['place']]]
        name_ok = int(any(g in na or fuzz.partial_ratio(g, na) >= 88 for g in gold))
        mcq_ok = int(norm(r['mcq_ans'])[:1] == r['mcq_gold'].lower())
        out.append(dict(place=r['place'], region=r['region'],
                        country_ok=country_ok, name_ok=name_ok, mcq_ok=mcq_ok))
    return pd.DataFrame(out)

# ---------- load ----------
g3 = pd.read_csv(f'{D}/results/generative_scored_3b.csv')
g3 = g3[['place', 'region', 'country_ok', 'name_ok', 'mcq_ok']].copy()
rows7 = [json.loads(l) for l in open(f'{D}/results/vlm_7b_responses.jsonl', encoding='utf-8')]
g7 = score_rows(rows7)
cs = pd.read_csv(f'{D}/results/closed_set.csv')

# sanity: reproduce Table 2 point estimates
def pt(df, col):
    m = df.groupby('region')[col].mean()
    return m.get('kurdistan', np.nan), m.get('control', np.nan)
print('sanity 7B country/name/mcq (kurd, ctrl):')
for c in ['country_ok', 'name_ok', 'mcq_ok']:
    k, c2 = pt(g7, c); print(f'  {c}: {k:.3f} / {c2:.3f}')
print('sanity 3B:')
for c in ['country_ok', 'name_ok', 'mcq_ok']:
    k, c2 = pt(g3, c); print(f'  {c}: {k:.3f} / {c2:.3f}')
for m in cs.model.unique():
    for c in ['correct', 'top5']:
        k, c2 = pt(cs[cs.model == m], c)
        print(f'  {m} {c}: {k:.3f} / {c2:.3f}')

# verify place-name alignment
for df, lab in [(g3, 'g3'), (g7, 'g7'), (cs, 'cs')]:
    pk = set(df[df.region == 'kurdistan'].place.unique())
    pc = set(df[df.region == 'control'].place.unique())
    miss_k = pk - set(K2C.keys()); miss_c = pc - set(K2C.values())
    assert not miss_k and not miss_c, (lab, miss_k, miss_c)
print('pair alignment OK')

# ---------- bootstraps ----------
def place_acc(df, col):
    a = df[df.region == 'kurdistan'].groupby('place')[col].mean()
    b = df[df.region == 'control'].groupby('place')[col].mean()
    kv = np.array([a.get(k, np.nan) for k, _, _ in PAIRS])
    cv = np.array([b.get(c, np.nan) for _, c, _ in PAIRS])
    ok = ~(np.isnan(kv) | np.isnan(cv))
    return kv[ok], cv[ok]

def cis(df, col, iters=2000, seed=42):
    kv, cv = place_acc(df, col)
    n = len(kv)
    rng = np.random.default_rng(seed)
    idxp = rng.integers(0, n, size=(iters, n))
    paired = cv[idxp].mean(1) - kv[idxp].mean(1)
    rng = np.random.default_rng(seed)
    ik = rng.integers(0, n, size=(iters, n))
    ic = rng.integers(0, n, size=(iters, n))
    indep = cv[ic].mean(1) - kv[ik].mean(1)
    f = lambda x: (np.percentile(x, 2.5), np.percentile(x, 97.5))
    return cv.mean() - kv.mean(), f(indep), f(paired), n

rows = []
specs = [
 ('CLIP ViT-L/14', cs[cs.model.str.contains('clip', case=False)], 'correct', 'Closed-set top-1'),
 ('CLIP ViT-L/14', cs[cs.model.str.contains('clip', case=False)], 'top5', 'Closed-set top-5'),
 ('SigLIP so400m', cs[cs.model.str.contains('siglip', case=False)], 'correct', 'Closed-set top-1'),
 ('SigLIP so400m', cs[cs.model.str.contains('siglip', case=False)], 'top5', 'Closed-set top-5'),
 ('Qwen2.5-VL-7B', g7, 'country_ok', 'Country identification'),
 ('Qwen2.5-VL-7B', g7, 'name_ok', 'Landmark naming'),
 ('Qwen2.5-VL-7B', g7, 'mcq_ok', 'Four-way multiple choice'),
 ('Qwen2.5-VL-3B', g3, 'country_ok', 'Country identification'),
 ('Qwen2.5-VL-3B', g3, 'name_ok', 'Landmark naming'),
 ('Qwen2.5-VL-3B', g3, 'mcq_ok', 'Four-way multiple choice'),
]
print('\nmodel | task | gap | indep CI | paired CI | n pairs')
for name, df, col, task in specs:
    gap, ind, par, n = cis(df, col)
    rows.append((name, task, gap, ind, par, n))
    print(f'{name} | {task} | {gap:.3f} | [{ind[0]:.3f},{ind[1]:.3f}] | [{par[0]:.3f},{par[1]:.3f}] | {n}')

import pickle
pickle.dump(rows, open('paired_ci.pkl', 'wb'))
print('\nsaved')
