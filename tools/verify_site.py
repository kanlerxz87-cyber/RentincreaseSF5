import re, os, sys

root = os.path.dirname(os.path.abspath(__file__))
repo = os.path.dirname(root)
os.chdir(repo)

print('--- Files ---')
for base in ['', 'assets', 'pages']:
    d = os.path.join(repo, base) if base else repo
    for f in sorted(os.listdir(d)):
        if os.path.isfile(os.path.join(d, f)):
            print(os.path.relpath(os.path.join(d, f), repo))

print('\n--- Anchor check ---')
src = open('pages/sources.html').read()
defined = set(re.findall(r'id="(s[a-zA-Z0-9]+)"', src))
print('Defined anchors:', sorted(defined))
used = set()
files = ['index.html'] + ['pages/' + p for p in sorted(os.listdir('pages')) if p.endswith('.html')]
for fn in files:
    html = open(fn).read()
    used |= set(re.findall(r'href="([^"]*sources\.html#[^"]+)"', html))
used_ids = set()
for u in used:
    m = re.search(r'#(s[a-zA-Z0-9]+)', u)
    if m:
        used_ids.add(m.group(1))
print('Anchor ids referenced from sources.html links:', sorted(used_ids))
missing = sorted(i for i in used_ids if i not in defined)
print('MISSING anchors:', missing if missing else 'NONE')

print('\n--- Tag balance check ---')
ok = True
for fn in files:
    html = open(fn).read()
    for tag in ['table', 'tr', 'td', 'th', 'div', 'main', 'header', 'footer', 'nav', 'p', 'ul', 'li', 'span', 'a']:
        o = len(re.findall(r'<' + tag + r'[\s>]', html))
        c = len(re.findall(r'</' + tag + r'>', html))
        if o != c:
            print(f'{fn}: <{tag}> open={o} close={c} MISMATCH')
            ok = False
print('Tag check:', 'OK' if ok else 'ISSUES FOUND')

print('\n--- Relative link check ---')
links = set()
for fn in files:
    html = open(fn).read()
    base = os.path.dirname(fn)
    for href in re.findall(r'href="([^"#]+\.html)(?:#[^"]*)?"', html):
        if href.startswith(('http', 'mailto:')):
            continue
        p = os.path.normpath(os.path.join(base, href))
        links.add(p)
for l in sorted(links):
    status = 'OK ' if os.path.exists(os.path.join(repo, l)) else 'BROKEN '
    print(status + l)
print('\nAll checks complete.')
