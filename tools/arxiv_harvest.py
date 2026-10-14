#!/usr/bin/env python3
"""Fetch arXiv papers and extract candidate open problems from their sources.

Uses only arXiv's public API and e-print endpoint, at most one request every
three seconds (arXiv's published limit). No other sites are contacted.

  python3 tools/arxiv_harvest.py --ids 2504.05986 --out sources/
  python3 tools/arxiv_harvest.py --authors "A. Author" --since 2016 --out sources/
  python3 tools/arxiv_harvest.py --query 'cat:math.CV AND abs:"Hardy space"' --max 50 --out sources/
  python3 tools/arxiv_harvest.py --local paper.tar.gz src-dir/ --out sources/   # files or folders you supplied

Per paper it writes sources/<id>/metadata.json, the extracted source (or
paper.pdf when no source exists) and candidates.jsonl. Candidates are not
problems: an agent reads each in context (playbooks/01-harvest.md).
Standard library only.
"""
import argparse, shutil, gzip, io, json, os, re, sys, tarfile, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = 'https://export.arxiv.org/api/query'
EPRINT = 'https://arxiv.org/e-print/'
ATOM = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
MIN_DELAY = 3.0
TARGET = re.compile(r'conjecture|question|problem|open', re.I)
DEFAULT_ENVS = {'conjecture', 'conj', 'question', 'problem', 'openproblem', 'openquestion', 'prob', 'ques'}
PHRASES = re.compile(
    r'it would be (?:interesting|nice|desirable)|we do not know|it is not known|remains? (?:an )?open|'
    r'open (?:question|problem)|it is natural to ask|we conjecture|we ask whether|we do not have|'
    r'an interesting question|unknown whether|we believe that', re.I)

_last = [0.0]


def fetch(url, delay):
    wait = max(delay, MIN_DELAY) - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    contact = os.environ.get('ARXIV_CONTACT', '')
    ua = 'math-research-process/0.1' + (f' (mailto:{contact})' if contact else '')
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    finally:
        _last[0] = time.time()


def search(params, delay, limit):
    """Yield Atom entries as dicts, paging through the API."""
    start, page = 0, min(limit, 100)
    while start < limit:
        q = dict(params, start=start, max_results=min(page, limit - start))
        root = ET.fromstring(fetch(API + '?' + urllib.parse.urlencode(q), delay))
        entries = root.findall('a:entry', ATOM)
        if not entries:
            return
        for e in entries:
            idurl = e.findtext('a:id', '', ATOM)
            if '/abs/' not in idurl:
                continue  # API error entries
            yield {
                'id': idurl.rsplit('/abs/', 1)[1],
                'title': ' '.join(e.findtext('a:title', '', ATOM).split()),
                'authors': [a.findtext('a:name', '', ATOM) for a in e.findall('a:author', ATOM)],
                'published': e.findtext('a:published', '', ATOM),
                'updated': e.findtext('a:updated', '', ATOM),
                'comment': e.findtext('arxiv:comment', '', ATOM),
                'categories': [c.get('term') for c in e.findall('a:category', ATOM)],
            }
        start += len(entries)


def safe_extract(tar, dest):
    dest = dest.resolve()
    for m in tar.getmembers():
        target = (dest / m.name).resolve()
        if not (m.isfile() or m.isdir()) or not str(target).startswith(str(dest) + os.sep):
            continue  # skip links, devices and path traversal
        if m.isdir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with tar.extractfile(m) as src, open(target, 'wb') as out:
                out.write(src.read())


def unpack(blob, dest):
    """Store an e-print blob; return 'source', 'pdf' or 'unknown'."""
    dest.mkdir(parents=True, exist_ok=True)
    if blob[:4] == b'%PDF':
        (dest / 'paper.pdf').write_bytes(blob)
        return 'pdf'
    data = blob
    if blob[:2] == b'\x1f\x8b':
        data = gzip.decompress(blob)
    try:
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            safe_extract(tar, dest / 'src')
        return 'source'
    except tarfile.ReadError:
        pass
    if data[:4] == b'%PDF':
        (dest / 'paper.pdf').write_bytes(data)
        return 'pdf'
    text = data.decode('utf-8', 'replace')
    if '\\documentclass' in text or '\\begin{document}' in text:
        (dest / 'src').mkdir(exist_ok=True)
        (dest / 'src' / 'main.tex').write_text(text)
        return 'source'
    (dest / 'eprint.bin').write_bytes(blob)
    return 'unknown'


def strip_comments(line):
    return re.sub(r'(?<!\\)%.*', '', line)


def candidates(src):
    """Theorem-like environments named Conjecture/Question/Problem, and open-question phrases."""
    files = sorted(p for p in src.rglob('*.tex') if p.is_file())
    texts = {p: p.read_text('utf-8', 'replace').splitlines() for p in files}
    envs = {}
    newthm = re.compile(r'\\newtheorem\*?\{([^}]+)\}(?:\[[^]]*\])?\{([^}]*)\}')
    declthm = re.compile(r'\\declaretheorem\*?(?:\[([^]]*)\])?\{([^}]+)\}(?:\[([^]]*)\])?')
    for lines in texts.values():
        for line in lines:
            line = strip_comments(line)
            for env, name in newthm.findall(line):
                envs[env] = name or env
            for before, env, after in declthm.findall(line):
                opt = re.search(r'name\s*=\s*\{?([^,}\]]+)', before + ',' + after)
                envs[env] = opt.group(1).strip() if opt else env
    wanted = {e for e, n in envs.items() if TARGET.search(n)} | (DEFAULT_ENVS - set(envs))
    out = []
    for path, lines in texts.items():
        rel = str(path.relative_to(src))
        clean = [strip_comments(l) for l in lines]
        i = 0
        while i < len(clean):
            m = re.search(r'\\begin\{([^}]+)\}(\[[^]]*\])?', clean[i])
            if m and m.group(1).rstrip('*') in wanted:
                env = m.group(1)
                j = i
                while j < len(clean) and f'\\end{{{env}}}' not in clean[j]:
                    j += 1
                body = ' '.join(x.strip() for x in clean[i:j + 1])
                label = re.search(r'\\label\{([^}]+)\}', body)
                out.append({'kind': 'environment', 'env': env, 'name': envs.get(env.rstrip('*'), env),
                            'title': (m.group(2) or '').strip('[]'), 'label': label.group(1) if label else None,
                            'file': rel, 'line': i + 1, 'text': body[:4000]})
                i = j + 1
                continue
            if PHRASES.search(clean[i]):
                lo, hi = max(0, i - 2), min(len(clean), i + 3)
                out.append({'kind': 'phrase', 'phrase': PHRASES.search(clean[i]).group(0),
                            'file': rel, 'line': i + 1,
                            'text': ' '.join(x.strip() for x in clean[lo:hi])[:1500]})
            i += 1
    return out


def process(meta, blob, out, local=False, srcdir=None):
    pid = meta['id'].replace('/', '_')
    dest = out / pid
    if srcdir is not None:
        shutil.copytree(srcdir, dest / 'src', dirs_exist_ok=True)
        kind = 'source'
    else:
        kind = unpack(blob, dest)
    meta = dict(meta, eprint=kind, local=local)
    if meta.get('comment') and re.search(r'withdraw', meta['comment'], re.I):
        meta['warning'] = 'comment mentions withdrawal: check the abstract page'
    (dest / 'metadata.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    cands = candidates(dest / 'src') if kind == 'source' else []
    with open(dest / 'candidates.jsonl', 'w') as f:
        for c in cands:
            f.write(json.dumps(dict(c, paper=meta['id']), ensure_ascii=False) + '\n')
    print(f"{meta['id']}: {kind}, {len(cands)} candidates  {meta.get('title', '')[:70]}", flush=True)
    return len(cands)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--ids', nargs='+', help='arXiv ids, e.g. 2504.05986 or 2504.05986v3')
    g.add_argument('--authors', nargs='+', help='author names (each searched separately)')
    g.add_argument('--query', help='raw arXiv API search_query')
    g.add_argument('--local', nargs='+', type=Path, help='source archives, PDFs or source folders you supplied')
    ap.add_argument('--since', type=int, help='keep papers first submitted in or after this year')
    ap.add_argument('--max', type=int, default=100, help='maximum results per search (default 100)')
    ap.add_argument('--category', help='keep only papers with this category, e.g. math.CV')
    ap.add_argument('--metadata-only', action='store_true', help='do not download sources')
    ap.add_argument('--delay', type=float, default=MIN_DELAY, help='seconds between requests (minimum 3)')
    ap.add_argument('--out', type=Path, default=Path('sources'))
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)

    if a.local:
        failed = 0
        for p in a.local:
            meta = {'id': p.name.split('.tar')[0].split('.pdf')[0], 'title': p.name}
            if p.is_dir():
                process(meta, None, a.out, local=True, srcdir=p)
            elif p.is_file():
                process(meta, p.read_bytes(), a.out, local=True)
            else:
                print(f'{p}: no such file or directory', file=sys.stderr)
                failed += 1
        return 1 if failed else 0

    if a.ids:
        metas = list(search({'id_list': ','.join(a.ids)}, a.delay, len(a.ids)))
    else:
        queries = [f'au:"{n}"' for n in a.authors] if a.authors else [a.query]
        seen, metas = set(), []
        for q in queries:
            for m in search({'search_query': q, 'sortBy': 'submittedDate', 'sortOrder': 'descending'},
                            a.delay, a.max):
                if m['id'] not in seen:
                    seen.add(m['id'])
                    metas.append(m)
    if a.since:
        metas = [m for m in metas if int(m['published'][:4] or 0) >= a.since]
    if a.category:
        metas = [m for m in metas if a.category in m['categories']]
    print(f'{len(metas)} papers', flush=True)
    (a.out / 'index.jsonl').open('a').writelines(json.dumps(m, ensure_ascii=False) + '\n' for m in metas)
    if a.metadata_only:
        return 0
    total = 0
    for k, m in enumerate(metas, 1):
        print(f'[{k}/{len(metas)}] ', end='', flush=True)
        try:
            total += process(m, fetch(EPRINT + m['id'], a.delay), a.out)
        except Exception as e:  # keep going; report the paper as missing
            print(f"{m['id']}: FAILED {e}", flush=True)
    print(f'{total} candidates in {len(metas)} papers', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
