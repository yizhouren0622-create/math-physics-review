"""Check textbook exercise coverage, data completeness and local HTML links."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parent
expected={'1.1':5,'1.2':3,'1.3':6,'1.4':4,'1.5':5,'1.6':3,'1.7':5,'2.1':6,'2.2':9,'2.3':6,'2.4':6,'2.5':5,'3.1':16,'3.2':8,'3.3':3,'3.4':4,'4.1':3,'4.2':6,'5.1':1,'5.2':9,'5.3':3,'5.4':3,'5.5':2,'6.1':1,'6.2':3,'6.4':1}
all_ex=[]
for p in sorted((ROOT/'data').glob('ch[1-6].json')):
 c=json.loads(p.read_text());all_ex+=c['exercises']
 for s in c['sections']:
  assert s['concepts'],f'No concept in {s["id"]}'
  for k in s['concepts']:
   for field in ['title','explain','formula','conditions','proof','memory']:assert k.get(field),(k['id'],field)
   assert k.get('example',{}).get('solution'),k['id']
 for e in c['exercises']:
  for field in ['title','question','idea','hint','solution','answer','pattern','pitfall']:assert e.get(field),(e['id'],field)
ids=[e['id'] for e in all_ex]
assert len(ids)==len(set(ids)),'Duplicate exercise ID'
assert set(ids)=={f'{s}-{n}' for s,count in expected.items() for n in range(1,count+1)},'Textbook coverage mismatch'
exams=json.loads((ROOT/'data/exams.json').read_text())
assert len(exams)==3
for exam in exams:
 assert sum(q['points'] for q in exam['questions'])==100
 for q in exam['questions']:
  for k in ['question','hint','solution','rubric']:assert q.get(k),(exam['title'],k)
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.ids=[];self.urls=[];self.math=0;self.details=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ['href','src']:
   if key in a:self.urls.append(a[key])
  if tag=='math':self.math+=1
  if tag=='details':
   self.details+=1;assert 'open' not in a,'Answers must start closed'
docs={p.name:Document(p.read_text()) for p in ROOT.glob('*.html')}
assert len(docs)==16
links=0
for name,d in docs.items():
 assert len(d.ids)==len(set(d.ids)),(name,'duplicate HTML IDs')
 for url in d.urls:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  assert (ROOT/target).is_file(),(name,'missing asset',url)
  if u.fragment and target in docs:assert unquote(u.fragment) in docs[target].ids,(name,'missing anchor',url)
  links+=1
assert not json.loads((ROOT/'data/coverage.json').read_text())['formula_failures']
print(json.dumps(dict(status='passed',chapters=6,exercises=len(ids),pages=len(docs),local_links=links,math_elements=sum(d.math for d in docs.values()),closed_details=sum(d.details for d in docs.values())),ensure_ascii=False))

# Both languages and all beginner paths must have the same coverage.
for n in range(1,7):
 zh=json.loads((ROOT/f'data/ch{n}.json').read_text())
 en=json.loads((ROOT/f'data/en/ch{n}.json').read_text())
 guides=json.loads((ROOT/f'data/learn/ch{n}.json').read_text())
 assert [e['id'] for e in zh['exercises']]==[e['id'] for e in en['exercises']]
 assert set(guides)=={e['id'] for e in zh['exercises']}
 def same_math(a,b):
  if isinstance(a,dict):
   for k in a:
    assert k in b,k
    same_math(a[k],b[k])
  elif isinstance(a,list):
   assert len(a)==len(b)
   for x,y in zip(a,b):same_math(x,y)
  elif isinstance(a,str):
   import re
   pattern=r'\$\$.*?\$\$|\$[^$\n]+?\$'
   from collections import Counter
   assert not (Counter(re.findall(pattern,a,re.S))-Counter(re.findall(pattern,b,re.S))),(a[:90],'missing math')
 same_math(zh,en)
 for ident,g in guides.items():
  for language in ['zh','en']:
   assert g[language]['goal'] and g[language]['recognize']
   assert 5<=len(g[language]['steps'])<=9,(ident,language,'Expected 5–9 concrete steps')
   assert g[language]['check']['question'] and g[language]['check']['answer']
  assert len(g['zh']['steps'])==len(g['en']['steps'])
assert not json.loads((ROOT/'data/untranslated.json').read_text()),'Untranslated visible prose'
print('Bilingual coverage and 126 guided learning paths passed.')

# Guide formulas contain no alignment environments: a doubled command escape is a display error.
import re
for p in (ROOT/'data/learn').glob('*.json'):
 def check_guide_strings(x):
  if isinstance(x,dict):
   for v in x.values():check_guide_strings(v)
  elif isinstance(x,list):
   for v in x:check_guide_strings(v)
  elif isinstance(x,str):
   assert not re.search(r'\\\\(?=[A-Za-z])',x),(p.name,'Doubled TeX command escape')
   assert '(1/2'+chr(92)+'pi)' not in x,(p.name,'Ambiguous inverse-transform coefficient')
   assert x.count('$')%2==0,(p.name,'Unclosed guide formula delimiter')
 check_guide_strings(json.loads(p.read_text()))
print('Guided self-check formula escapes and normalization notation passed.')

# Each concept gets one original problem with independently expandable help.
practice=json.loads((ROOT/'data/practice.json').read_text())
concept_chapters={}
for n in range(1,7):
 chapter=json.loads((ROOT/f'data/ch{n}.json').read_text())
 chapter_exercises={e['id'] for e in chapter['exercises']}
 for section in chapter['sections']:
  for concept in section['concepts']:
   ident=concept['id'];concept_chapters[ident]=n
   problem=practice[ident]
   assert problem['chapter']==n,(ident,'wrong chapter')
   assert problem['exercise'] in chapter_exercises,(ident,'missing textbook exercise')
   assert f'try-c{n}-{ident}' in docs[f'chapter-{n}.html'].ids
   for language in ['zh','en']:
    content=problem[language]
    assert all(content.get(field) for field in ['prompt','hints','solution','check'])
    assert len(content['hints'])==3,(ident,'expected three hints')
    assert 3<=len(content['solution'].split('\n\n'))<=5,(ident,'expected short solution steps')
    check_guide_strings(content)
   assert not re.search(r'[\u3400-\u9fff]',json.dumps(problem['en'],ensure_ascii=False)),(ident,'Chinese in English')
   same_math(problem['zh'],problem['en']);same_math(problem['en'],problem['zh'])
assert set(practice)==set(concept_chapters) and len(practice)==38,'Transfer practice coverage mismatch'
print('38 bilingual transfer problems, hints, solutions and textbook links passed.')
