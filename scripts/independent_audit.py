"""Read-only integration audit; does not modify the publishing session's files."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
class Audit(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path=path; self.body=False; self.row=False; self.source=False; self.rows=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='tbody': self.body=True
        if tag=='tr' and self.body: self.row=True; self.source=False
        if tag in ('a','link'):
            h=a.get('href',''); u=urlsplit(h)
            if u.scheme:
                assert u.scheme=='https', (self.path,h)
                assert u.hostname in {'www.sf.gov','leginfo.legislature.ca.gov','calcivilrights.ca.gov','www.hud.gov'}, (self.path,h)
                if tag=='a' and self.row: self.source=True
            elif u.path:
                assert (self.path.parent/unquote(u.path)).exists(), (self.path,h)
    def handle_endtag(self,tag):
        if tag=='tr' and self.row:
            assert self.source,(self.path,'row without official source')
            self.rows+=1; self.row=False
        if tag=='tbody': self.body=False
count=0
pages=list(Path('site').glob('*.html'))
for p in pages:
    text=p.read_text(); a=Audit(p); a.feed(text); count+=a.rows
    assert 'id="main"' in text and 'lang="en"' in text, p
    assert p.name and Path(p.name).read_bytes()==p.read_bytes(), (p,'published root differs from site artifact')
    for token in ['L O','V N','M T','E R','I S']:
        assert token not in text, (p,'supplied initials')
assert Path('style.css').read_bytes()==Path('site/style.css').read_bytes()
print(f'PASS: {len(pages)} pages, {count} official-sourced data rows, root/site parity, internal links, stylesheet, landmarks, identifier exclusion')
