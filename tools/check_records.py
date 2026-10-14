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
STAGE = ['untriaged', 'triaged', 'attacking', 'written', 'reviewed', 'public', 'abandoned']
STATUS = {'open', 'partial', 'resolved', 'claimed', 'refuted'}
TIER = {'journal', 'arxiv', 'ours-public', 'ours-internal'}
SCOPE = {None, 'full', 'partial'}
REQUIRED = ['id', 'title', 'kind', 'origin', 'theme', 'literature', 'ours']


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
    if ours.get('result_scope') not in SCOPE:
        errors.append(f'ours.result_scope {ours.get("result_scope")!r} not full/partial/null')
    for k in ('impact', 'difficulty', 'difficulty_initial'):
        if not score(d.get(k)):
            errors.append(f'{k} must be 1-5 or null')
    if stage != 'untriaged' and d.get('difficulty_initial') is None:
        warnings.append('difficulty_initial not set at triage')
    after_review = STAGE.index(stage) >= STAGE.index('reviewed') and stage != 'abandoned'
    if after_review and not ours.get('review'):
        errors.append(f'stage {stage} needs ours.review')
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
        if tier in ('ours-public', 'ours-internal'):
            if not after_review:
                errors.append(f'tier {tier} needs a reviewed result (stage {stage})')
            if ours.get('result_scope') == 'partial':
                errors.append('a partial result cannot carry a resolution tier')
        if tier == 'journal' and res.get('conditional_on'):
            errors.append('a journal tier cannot be conditional')
    if stage not in ('untriaged',) and '## State of play' not in body:
        warnings.append('no "## State of play" section')
    return errors, warnings


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else 'problems')
    files = sorted(p for p in root.glob('*/*.md') if not p.name.isupper())
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
