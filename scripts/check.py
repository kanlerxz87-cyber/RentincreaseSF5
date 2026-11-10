from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
class Check(HTMLParser):
 def __init__(self): super().__init__();self.row=False;self.official=False;self.rows=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='tr':self.row=True;self.official=False
  if tag=='a':
   u=a.get('href','');p=urlsplit(u)
   if p.scheme=='https':
    assert p.hostname in {'www.sf.gov','sfgov.legistar.com','leginfo.legislature.ca.gov','calcivilrights.ca.gov','www.hud.gov','github.com'},u
    self.official=True
   elif u and not u.startswith('#'):assert Path('site',p.path).exists(),u
 def handle_endtag(self,tag):
  if tag=='thead':self.row=False
  if tag=='tr' and self.row:
   # header-only rows have no source; data rows checked separately below
   self.rows+=1
for f in Path('site').glob('*.html'):
 text=f.read_text();c=Check();c.feed(text)
 for r in text.split('<tbody>')[1:]:
  for tr in r.split('</tbody>')[0].split('</tr>'):
   if '<tr>' in tr:assert 'href="https://' in tr,(f,tr)
 assert '<h1>' in text
 assert 'analytics' not in text.replace('no tenant names, initials, exact address, analytics','')
print('PASS: local links, official source allowlist, every data row source, page headings, no analytics')
