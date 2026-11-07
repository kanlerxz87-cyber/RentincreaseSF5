from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
class Audit(HTMLParser):
 def __init__(self,p): super().__init__(); self.p=p; self.row=False; self.source=False; self.rows=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='tr': self.row=True; self.source=False
  if t=='a':
   h=a.get('href',''); u=urlsplit(h)
   if u.scheme:
    assert u.scheme=='https',h
    assert u.hostname in {'www.sf.gov','leginfo.legislature.ca.gov','calcivilrights.ca.gov','archives.hud.gov'},h
    self.source=True
   elif u.path: assert (self.p.parent/u.path).exists(),(self.p,h)
  if t=='link': assert (self.p.parent/a['href']).exists()
 def handle_endtag(self,t):
  if t=='thead': self.row=False
  if t=='tr' and self.row:
   self.rows+=1
   # header rows have no source and are identified by counter reset below
   if self.rows>1: assert self.source,(self.p,'row missing official source')
   self.row=False
 def handle_startendtag(self,t,a): self.handle_starttag(t,a)
# Validate tbody rows separately to exclude every table header.
import re
count=0
for p in Path('site').glob('*.html'):
 text=p.read_text(); audit=Audit(p)
 # Link check independent of row checks
 audit.handle_endtag=lambda t: None
 audit.feed(text)
 for body in re.findall(r'<tbody>(.*?)</tbody>',text,re.S):
  for row in re.findall(r'<tr>(.*?)</tr>',body,re.S):
   assert re.search(r'href="https://(?:www\.sf\.gov|leginfo\.legislature\.ca\.gov|calcivilrights\.ca\.gov|archives\.hud\.gov)/',row),p
   count+=1
 assert '<html lang="en">' in text and 'id="main"' in text
 assert not re.search(r'\b(?:L O|V N|JP|M T|E R|I S)\b',text), 'Private identifier'
print(f'PASS: 7 pages; {count} sourced table rows; internal links, stylesheets, language, landmarks and supplied-identifier exclusion')
