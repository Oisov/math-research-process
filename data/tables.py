#!/usr/bin/env python3
"""Recompute every count in the paper from data/records.csv.

  python3 data/tables.py

One row per problem record, anonymised: no identifiers, titles or sources.
Columns:
- outcome: others | ours | partial | open
- significance: H | M | L, for answers settled by our agents; the author's
  grade (six chosen at the time, a seventh added on 14 October)
- significance_reread: H | M | L, a blind re-read of each record by a fresh
  agent that did not see the first grades and did not search the literature
- result_kind: L = literature assembly, R = routine argument, C = construction
  or certificate, S = substantial argument
- initial_difficulty: the first score each record received, before the
  12-October campaign
"""
import csv
import collections
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).with_name('records.csv'))))


def table(title, key_r, key_c, rows, order_r=None, order_c=None):
    c = collections.Counter((key_r(r), key_c(r)) for r in rows)
    rs = order_r or sorted({k[0] for k in c})
    cs = order_c or sorted({k[1] for k in c})
    print(f'\n{title}')
    print(' ' * 22 + ''.join(f'{x:>12}' for x in cs) + f'{"total":>8}')
    for r in rs:
        print(f'{str(r):22}' + ''.join(f'{c[(r, x)]:>12}' for x in cs) + f'{sum(c[(r, x)] for x in cs):>8}')


ours = [r for r in rows if r['outcome'] == 'ours']
print('records', len(rows), dict(collections.Counter(r['outcome'] for r in rows)))
print('origin', dict(collections.Counter(r['origin'] for r in rows)), 'kind', dict(collections.Counter(r['kind'] for r in rows)))
print('initial difficulty', dict(sorted(collections.Counter(r['initial_difficulty'] for r in rows).items())))
OUT = ['others', 'ours', 'partial', 'open']
table('Outcome by initial difficulty (all records)', lambda r: r['initial_difficulty'], lambda r: r['outcome'], rows, None, OUT)
table('Sign by kind (settled by us)', lambda r: r['sign'], lambda r: r['result_kind'], ours)
table('Sign by significance (settled by us)', lambda r: r['sign'], lambda r: r['significance'], ours, None, ['H', 'M', 'L'])
table('Origin by significance (settled by us)', lambda r: r['origin'], lambda r: r['significance'], ours, None, ['H', 'M', 'L'])
table('How posed, by outcome', lambda r: r['form'], lambda r: r['outcome'], rows, ['conjecture', 'problem', 'question', 'remark', 'ours'], OUT)
table('How posed, high significance', lambda r: r['form'], lambda r: r['significance'], ours, ['conjecture', 'problem', 'question', 'remark', 'ours'], ['H', 'M', 'L'])
table('When settled, by initial difficulty', lambda r: r['settled_when'], lambda r: r['initial_difficulty'], ours, ['before-12-Oct', '12-Oct', '13-Oct'])
table('When settled, by significance', lambda r: r['settled_when'], lambda r: r['significance'], ours, ['before-12-Oct', '12-Oct', '13-Oct'], ['H', 'M', 'L'])
uns = [r for r in rows if r['outcome'] in ('partial', 'open')]
for name, g in [('unsettled', uns), ('settled by us', ours)]:
    n = len(g)
    hi = sum(1 for r in g if r['initial_difficulty'] in ('4', '5'))
    ext = sum(1 for r in g if r['origin'] == 'external')
    imp = sum(1 for r in g if r['impact'] in ('4', '5'))
    lit = sum(1 for r in g if r['literature_status'] == 'partial')
    ses = [int(r['sessions']) for r in g if r['sessions']]
    print(f'\n{name}: n={n}, initial 4-5: {hi}, external: {ext} ({100*ext/n:.0f}%), impact>=4: {imp} ({100*imp/n:.0f}%), '
          f'literature partial: {lit} ({100*lit/n:.0f}%), mean sessions {sum(ses)/len(ses):.2f}, sessions distribution {dict(sorted(collections.Counter(ses).items()))}')

table('Significance: first grade by blind re-read (settled by us)', lambda r: r['significance'], lambda r: r['significance_reread'], ours, ['H', 'M', 'L'], ['H', 'M', 'L'])
agree = sum(r['significance'] == r['significance_reread'] for r in ours)
n = len(ours)
pa = collections.Counter(r['significance'] for r in ours)
pb = collections.Counter(r['significance_reread'] for r in ours)
pe = sum(pa[g] * pb[g] for g in 'HML') / n ** 2
print(f'\nre-read agreement {agree}/{n} ({100*agree/n:.0f}%), Cohen kappa {(agree/n - pe)/(1 - pe):.2f}')
