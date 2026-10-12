import csv, json, hashlib, collections
import numpy as np
from scipy.optimize import nnls

V = '/mnt/user-data/outputs/validation/'
runs = list(csv.DictReader(open(V + 'data/runs.csv')))
levels = list(csv.DictReader(open(V + 'data/levels.csv')))

# ---------- Task 1 ----------
h = hashlib.sha256(open(V + 'predictions_frozen.csv', 'rb').read()).hexdigest()
print('T1 sha256', h, h == '11d2e03060d6de2b0d26e76da09690e468fdff53851eda638bf2905fa8cc9721')

# ---------- kept runs ----------
ok = [r for r in runs if r['status'] == 'ok']
cells_with_rerun = {(r['config'], r['schedule']) for r in ok if r['mode'] == 'rerun'}
kept = [r for r in ok if ((r['config'], r['schedule']) not in cells_with_rerun) or r['mode'] == 'rerun']
print('status counts', collections.Counter(r['status'] for r in runs))
print('rerun cells', sorted(cells_with_rerun))
print('kept runs', len(kept), collections.Counter((r['config'], r['schedule']) for r in kept).most_common(3),
      min(collections.Counter((r['config'], r['schedule']) for r in kept).values()))
kept_ids = {r['run_id'] for r in kept}

# check nonkern == T - K
md = max(abs(float(r['window_wall']) - float(r['kern']) - float(r['nonkern'])) for r in kept)
print('max |T-K-O| over kept runs', md)

configs = sorted({r['config'] for r in runs})
info = {}
for r in runs:
    info[r['config']] = dict(dim=int(r['dim']), role=r['role'], L=int(r['L']))
SCH = ['global', 'subcycle']

med = {}  # (c,s) -> dict T,K,O
for c in configs:
    for s in SCH:
        rr = [r for r in kept if r['config'] == c and r['schedule'] == s]
        med[(c, s)] = dict(T=np.median([float(r['window_wall']) for r in rr]),
                           K=np.median([float(r['kern']) for r in rr]),
                           O=np.median([float(r['nonkern']) for r in rr]),
                           n=len(rr))

# level data from kept runs
lv = collections.defaultdict(list)  # (c,s,l) -> rows
for x in levels:
    if x['run_id'] in kept_ids:
        lv[(x['config'], x['schedule'], int(x['level']))].append(x)

# ---------- Task 6: identity of counts ----------
ident_ok = True
for c in configs:
    L = info[c]['L']
    for l in range(L + 1):
        vals = set()
        for s in SCH:
            for x in lv[(c, s, l)]:
                vals.add((x['N'], x['B'], x['G']))
        if len(vals) != 1:
            ident_ok = False
            print('COUNT MISMATCH', c, l, vals)
# also check all (incl. dropped primary) level rows
ident_all = True
alllv = collections.defaultdict(set)
for x in levels:
    alllv[(x['config'], int(x['level']))].add((x['N'], x['B']))
for k, v in alllv.items():
    if len(v) != 1:
        ident_all = False; print('ALL-ROWS MISMATCH', k, v)
# n_adv consistency within schedule
adv_ok = True
for k, v in lv.items():
    if len({x['n_adv'] for x in v}) != 1:
        adv_ok = False; print('n_adv mismatch', k)
print('T6 counts identical (kept, N,B,G):', ident_ok, ' all rows N,B:', ident_all, ' n_adv consistent:', adv_ok)

def counts(c, s):
    L = info[c]['L']
    A = np.array([float(lv[(c, s, l)][0]['n_adv']) for l in range(L + 1)])
    N = np.array([float(lv[(c, s, l)][0]['N']) for l in range(L + 1)])
    B = np.array([float(lv[(c, s, l)][0]['B']) for l in range(L + 1)])
    G = np.array([float(lv[(c, s, l)][0]['G']) for l in range(L + 1)])
    kl = np.array([np.median([float(x['kern']) for x in lv[(c, s, l)]]) for l in range(L + 1)])
    return A, N, B, G, kl

# check A vs plan: A^L = nc q_l, A^G = nc Q
for c in configs:
    nc = int([r for r in kept if r['config'] == c][0]['nc'])
    L = info[c]['L']
    AG = counts(c, 'global')[0]; AL = counts(c, 'subcycle')[0]
    if not (np.all(AG == nc * 2 ** L) and np.all(AL == nc * 2.0 ** np.arange(L + 1))):
        print('A mismatch', c, nc, AG, AL)

S = {c: med[(c, 'global')]['T'] / med[(c, 'subcycle')]['T'] for c in configs}
H = {c: med[(c, 'subcycle')]['O'] - med[(c, 'global')]['O'] for c in configs}
print('T6 H<0 all:', all(v < 0 for v in H.values()), 'max H', max(H.values()))
for c in configs:
    print('  %-18s %-8s S=%.4f H=%.4f x=%.3f n=%d/%d' % (c, info[c]['role'], S[c], H[c], H[c] / med[(c, 'global')]['K'],
          med[(c, 'global')]['n'], med[(c, 'subcycle')]['n']))

# ---------- models ----------
def kfeat(kind, A, N, B):
    if kind == 'K1':
        return np.column_stack([A * N])
    if kind == 'K2':
        return np.column_stack([A * N, A * B])

def fit_kernel(kind, train, d):
    X, y = [], []
    for c in train:
        if info[c]['dim'] != d: continue
        for s in SCH:
            A, N, B, G, kl = counts(c, s)
            F = kfeat(kind, A, N, B)
            for i in range(len(A)):
                X.append(F[i] / kl[i]); y.append(1.0)
    return nnls(np.array(X), np.array(y))[0]

def khat(kind, coef, c, s):
    A, N, B, G, kl = counts(c, s)
    return float(np.sum(kfeat(kind, A, N, B) @ coef))

def ofeat(kind, c, s, kcoef, kkind):
    A, N, B, G, kl = counts(c, s)
    if kind == 'O1':
        return np.array([khat(kkind, kcoef, c, s)])
    if kind == 'O3':
        return np.array([A.sum(), (A * G).sum(), (A * N).sum()])

def fit_overhead(kind, train, d, kcoef, kkind):
    out = {}
    for s in SCH:
        X, y = [], []
        for c in train:
            if info[c]['dim'] != d: continue
            Oobs = med[(c, s)]['O']
            X.append(ofeat(kind, c, s, kcoef, kkind) / Oobs); y.append(1.0)
        out[s] = nnls(np.array(X), np.array(y))[0]
    return out

def fit_pair(kk, ok_, train):
    co = {}
    for d in (2, 3):
        kc = fit_kernel(kk, train, d)
        oc = fit_overhead(ok_, train, d, kc, kk)
        co[d] = (kc, oc)
    return co

def predict(kk, ok_, co, c):
    kc, oc = co[info[c]['dim']]
    res = {}
    for s in SCH:
        K = khat(kk, kc, c, s)
        O = float(ofeat(ok_, c, s, kc, kk) @ oc[s])
        res[s] = (K, O, K + O)
    return res['global'][2] / res['subcycle'][2], res

train = [c for c in configs if info[c]['role'] == 'training']
held = [c for c in configs if info[c]['role'] == 'heldout']
print('train', len(train), 'held', len(held))

# ---------- Task 3: recompute S_hat from JSON coefficients ----------
sel = json.load(open(V + 'predictions_frozen_selection.json'))
frozen = {r['config']: r for r in csv.DictReader(open(V + 'predictions_frozen.csv'))}
jco = {}
for d in (2, 3):
    e = sel['coefficients'][str(d)]
    jco[d] = (np.array(e['kernel']), {s: np.array(e['overhead'][s]) for s in SCH})
maxrel3 = 0
for c in held:
    Sh, res = predict('K1', 'O3', jco, c)
    fr = frozen[c]
    pairs = [(Sh, fr['S_hat']), (res['global'][2], fr['T_G_hat']), (res['subcycle'][2], fr['T_L_hat']),
             (res['global'][0], fr['K_G_hat']), (res['subcycle'][0], fr['K_L_hat']),
             (res['global'][1], fr['O_G_hat']), (res['subcycle'][1], fr['O_L_hat'])]
    for a, b in pairs:
        maxrel3 = max(maxrel3, abs(a - float(b)) / abs(float(b)))
print('T3 max rel diff JSON-coef recompute vs frozen (all 7 columns):', maxrel3)

# ---------- Task 4: refit on training ----------
co = fit_pair('K1', 'O3', train)
maxc = 0
for d in (2, 3):
    kc, oc = co[d]
    jk, jo = jco[d]
    print('T4 dim', d, 'kernel', kc, 'json', jk)
    for s in SCH:
        print('     ', s, oc[s], 'json', jo[s])
        for a, b in zip(oc[s], jo[s]):
            if b != 0: maxc = max(maxc, abs(a - b) / abs(b))
            else: maxc = max(maxc, abs(a))
    maxc = max(maxc, float(np.max(np.abs(kc - jk) / jk)))
print('T4 max coef rel diff (abs if json zero):', maxc)
maxrel4 = 0
for c in held:
    Sh, res = predict('K1', 'O3', co, c)
    maxrel4 = max(maxrel4, abs(Sh - float(frozen[c]['S_hat'])) / float(frozen[c]['S_hat']))
print('T4 max rel diff refit S_hat vs frozen:', maxrel4)

# ---------- Task 2 ----------
es = []
for c in held:
    Sh = float(frozen[c]['S_hat'])
    e = abs(Sh - S[c]) / S[c]
    es.append(e)
    print('T2 %-18s S=%.4f Shat=%.4f e=%.4f' % (c, S[c], Sh, e))
print('T2 median e', np.median(es), 'max e', max(es))

# ---------- Task 5: LOCO ----------
for kk, ok_ in [('K1', 'O3'), ('K1', 'O1'), ('K2', 'O3')]:
    errs = {}
    for c in train:
        tr = [x for x in train if x != c]
        co_ = fit_pair(kk, ok_, tr)
        Sh, _ = predict(kk, ok_, co_, c)
        errs[c] = abs(Sh - S[c]) / S[c]
    rep = next(x for x in sel['loco'] if x['pair'] == kk + '+' + ok_)
    md = max(abs(errs[c] - rep['errors'][c]) for c in train)
    print('T5 %s+%s median %.6f reported %.6f  max per-config diff %.2e' % (kk, ok_, np.median(list(errs.values())), rep['median'], md))
