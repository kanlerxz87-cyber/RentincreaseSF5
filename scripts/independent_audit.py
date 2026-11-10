"""Read-only integration audit; does not modify the publishing session's files."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re

INITIAL_PAIR = re.compile(r"\b[A-Z]\s[A-Z]\b")
def _identifier_tokens():
    """Exact identifier tokens, loaded only from a git-ignored private file.

    No personal identifier is committed to this repository: the tokens live in
    private/identifiers.txt, which .gitignore excludes. When the file is absent the
    exact-token check is skipped; the generic initial-pair pattern is still enforced.
    """
    path = Path('private/identifiers.txt')
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


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
                assert u.hostname in {'www.sf.gov','sfgov.legistar.com','leginfo.legislature.ca.gov','calcivilrights.ca.gov','www.hud.gov','github.com'}, (self.path,h)
                # github.com is a repository-housekeeping link, never an official source for a value
                if tag=='a' and self.row and u.hostname!='github.com': self.source=True
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
    for token in _identifier_tokens():
        assert token not in text, (p,'personal identifier token')
    m = INITIAL_PAIR.search(text)
    assert m is None, (p,'initial-pair pattern %r - verify it is a placeholder' % m.group(0))
assert Path('style.css').read_bytes()==Path('site/style.css').read_bytes()
print(f'PASS: {len(pages)} pages, {count} official-sourced data rows, root/site parity, internal links, stylesheet, landmarks, identifier exclusion')
