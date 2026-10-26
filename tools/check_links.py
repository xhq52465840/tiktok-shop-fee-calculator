"""Check every internal link in the built site: python3 tools/check_links.py
Resolves each href/src/meta-refresh/JSON "src" against the page's URL and confirms the target file exists.
Also flags any page-relative (non root-relative) internal URL, since 404.html is served at arbitrary depths."""
import os, re, sys
from urllib.parse import urljoin, urlsplit, unquote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'src', 'tools', 'deploy', 'node_modules'}
PAT = re.compile(r'''\b(?:href|src|action)="([^"]*)"|url=([^"'>;\s]+)|"src":\s*"([^"]+)"''')
EXT = ('http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:', '//')
OWN = ('https://sellerfee.app/', 'http://sellerfee.app/')

def exists(p):
    f = os.path.join(ROOT, unquote(p).lstrip('/'))
    if p.endswith('/') or os.path.isdir(f): return os.path.isfile(os.path.join(f, 'index.html'))
    return os.path.isfile(f)

broken, relative, n, pages = [], [], 0, 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
    for fn in files:
        if not fn.endswith('.html'): continue
        pages += 1
        fp = os.path.join(d, fn); rp = os.path.relpath(fp, ROOT).replace(os.sep, '/')
        url = '/' + (rp[:-len('index.html')] if fn == 'index.html' else rp)
        for m in PAT.finditer(open(fp, encoding='utf-8').read()):
            u = next(g for g in m.groups() if g is not None)
            if not u or u.startswith('#') or '{' in u: continue
            for o in OWN:
                if u.startswith(o): u = '/' + u[len(o):]
            if u.startswith(EXT): continue
            n += 1
            if not u.startswith('/'): relative.append((url, u))
            path = urlsplit(urljoin(url, u)).path
            if not exists(path): broken.append((url, u, path))
print(f'{pages} HTML files, {n} internal URLs checked')
for x in relative: print('RELATIVE', *x)
for x in broken: print('BROKEN  ', *x)
print(f'broken={len(broken)} relative={len(relative)}')
sys.exit(1 if broken or relative else 0)
