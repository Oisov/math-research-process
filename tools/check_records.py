#!/usr/bin/env python3
"""Validate problem records (templates/record.md) under a directory.

  python3 tools/check_records.py problems/

Errors break the rules in AGENTS.md and exit with status 1; warnings are
reported but do not fail. Needs PyYAML (pip install pyyaml).
"""
import datetime, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit('check_records: needs PyYAML (pip install pyyaml)')

KIND = {'stated', 'implicit', 'inference'}
ORIGIN = {'external', 'ours'}
STAGE = ['untriaged', 'triaged', 'attacking', 'written', 'contested', 'reviewed', 'public', 'abandoned']
STATUS = {'open', 'partial', 'resolved', 'claimed', 'refuted', 'invalid'}
TIER = {'journal', 'arxiv', 'ours-public', 'ours-internal'}
SCOPE = {None, 'full', 'partial'}
SIGN = {None, 'proof', 'counterexample', 'determination'}
FORM = {'conjecture', 'problem', 'question', 'remark', 'ours'}
REQUIRED = ['id', 'title', 'kind', 'origin', 'theme', 'literature', 'ours']
KNOWN = {
    None: {'id', 'title', 'kind', 'origin', 'theme', 'source', 'premises', 'references',
           'literature', 'ours', 'resolution', 'impact', 'difficulty_initial', 'difficulty',
           'scores_note', 'tags', 'effort', 'related', 'aliases'},
    'source': {'paper', 'location', 'posed_by', 'form', 'quote'},
    'literature': {'status', 'checked', 'evidence'},
    'ours': {'stage', 'sign', 'result_scope', 'artifacts', 'review', 'public', 'told_authors'},
    'resolution': {'tier', 'ref', 'checked', 'conditional_on'},
    'effort': {'sessions', 'last', 'parked'},
}
REVIEW = ('by', 'model', 'date', 'verdict')


def score(v):
    return v is None or (isinstance(v, int) and 1 <= v <= 5)


def check(path, seen):
    errors, warnings = [], []
    text = path.read_text()
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not m:
        return ['no YAML frontmatter'], []
    try:
        d = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return [f'YAML: {e}'], []
    body = m.group(2)
    for k in REQUIRED:
        if k not in d:
            errors.append(f'missing {k}')
    if errors:
        return errors, warnings
    for section, allowed in KNOWN.items():
        block = d if section is None else d.get(section)
        if isinstance(block, dict):
            for key in sorted(set(block) - allowed):
                errors.append(f'unknown field {key!r}' + (f' in {section}' if section else ''))
    if d['id'] != path.stem:
        errors.append(f'id {d["id"]} does not match file name')
    if d['id'] in seen:
        errors.append(f'duplicate id (also {seen[d["id"]]})')
    seen[d['id']] = path
    if d['theme'] != path.parent.name:
        errors.append(f'theme {d["theme"]} does not match folder {path.parent.name}')
    if d['kind'] not in KIND:
        errors.append(f'kind {d["kind"]!r} not in {sorted(KIND)}')
    if d['origin'] not in ORIGIN:
        errors.append(f'origin {d["origin"]!r} not in {sorted(ORIGIN)}')
    src = d.get('source') or {}
    if d['kind'] in ('stated', 'implicit'):
        if not (src.get('paper') and src.get('location')):
            errors.append('stated/implicit record needs source.paper and source.location')
        if not src.get('quote'):
            warnings.append('no source.quote (the question verbatim)')
    form = src.get('form')
    if form is None and d['origin'] == 'ours':
        form = 'ours'
    if form not in FORM:
        errors.append(f'source.form {form!r} not in {sorted(FORM)} (how strongly the source poses it)')
    if form == 'ours' and d['origin'] != 'ours':
        errors.append('source.form ours requires origin ours')
    if d['kind'] == 'inference' and not d.get('premises'):
        errors.append('inference record needs premises')
    lit, ours = d['literature'] or {}, d['ours'] or {}
    if lit.get('status') not in STATUS:
        errors.append(f'literature.status {lit.get("status")!r} not in {sorted(STATUS)}')
    if not isinstance(lit.get('checked'), (datetime.date, str)) and ours.get('stage') != 'untriaged':
        errors.append('literature.checked (date of the search) missing after triage')
    stage = ours.get('stage')
    if stage not in STAGE:
        errors.append(f'ours.stage {stage!r} not in {STAGE}')
        return errors, warnings
    if ours.get('sign') not in SIGN:
        errors.append(f'ours.sign {ours.get("sign")!r} not proof/counterexample/determination/null')
    if ours.get('result_scope') not in SCOPE:
        errors.append(f'ours.result_scope {ours.get("result_scope")!r} not full/partial/null')
    for k in ('impact', 'difficulty', 'difficulty_initial'):
        if not score(d.get(k)):
            errors.append(f'{k} must be 1-5 or null')
    if stage != 'untriaged' and d.get('difficulty_initial') is None:
        warnings.append('difficulty_initial not set at triage')
    after_review = STAGE.index(stage) >= STAGE.index('reviewed') and stage != 'abandoned'
    review = ours.get('review')
    if after_review:
        if not isinstance(review, dict) or not all(review.get(k) for k in REVIEW):
            errors.append(f'stage {stage} needs ours.review with {", ".join(REVIEW)}')
    if ours.get('public') and stage != 'public':
        errors.append(f'ours.public is set but stage is {stage}')
    if stage == 'public':
        if not ours.get('public'):
            errors.append('stage public needs ours.public')
        if d['origin'] == 'external' and not ours.get('told_authors'):
            errors.append('external result made public without told_authors (date, or "held: <reason>")')
    if stage == 'abandoned' and not ours.get('abandoned_reason') and 'abandoned' not in body.lower():
        warnings.append('abandoned without a reason')
    res = d.get('resolution') or {}
    if res:
        tier = res.get('tier')
        if tier not in TIER:
            errors.append(f'resolution.tier {tier!r} not in {sorted(TIER)}')
        if not res.get('ref'):
            errors.append('resolution needs ref')
        if stage == 'contested':
            errors.append('a contested result cannot carry a resolution tier')
        if tier in ('ours-public', 'ours-internal'):
            if not after_review:
                errors.append(f'tier {tier} needs a reviewed result (stage {stage})')
            if ours.get('result_scope') == 'partial':
                errors.append('a partial result cannot carry a resolution tier')
            elif ours.get('result_scope') != 'full':
                errors.append(f'tier {tier} needs result_scope full, set by the referee')
            if res.get('checked') is not True:
                errors.append(f'tier {tier} needs resolution.checked: true')
        if tier == 'ours-public' and not ours.get('public'):
            errors.append('tier ours-public needs ours.public (the public PDF)')
        if tier == 'journal' and res.get('conditional_on'):
            errors.append('a journal tier cannot be conditional')
    if stage not in ('untriaged',) and '## State of play' not in body:
        warnings.append('no "## State of play" section')
    return errors, warnings


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else 'problems')
    if not root.is_dir():
        print(f'ERROR {root}: no such records directory')
        return 2
    files = sorted(p for p in root.glob('*/*.md') if not p.name.isupper())
    if not files:
        print(f'ERROR {root}: no records found under <theme>/<ID>.md')
        return 2
    seen, n_err, n_warn = {}, 0, 0
    for p in files:
        errors, warnings = check(p, seen)
        for e in errors:
            print(f'ERROR {p}: {e}')
        for w in warnings:
            print(f'warn  {p}: {w}')
        n_err += len(errors)
        n_warn += len(warnings)
    print(f'check: {len(files)} records, {n_err} errors, {n_warn} warnings')
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
