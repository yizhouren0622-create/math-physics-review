"""Bilingual rendering and a progressive, accessible reading layer."""
import json,re,html
from pathlib import Path
from lxml import etree
from lxml import html as LH
ROOT=Path(__file__).resolve().parent
translations={};missing=set();learn={};ordered=None
CJK=re.compile(r'[\u3400-\u9fff]')
def register(zh,en):
 global ordered
 ordered=None
 if isinstance(zh,str) and isinstance(en,str) and CJK.search(zh):translations[zh]=en
 elif isinstance(zh,list) and isinstance(en,list):
  assert len(zh)==len(en),'Translation list length mismatch'
  for a,b in zip(zh,en):register(a,b)
 elif isinstance(zh,dict) and isinstance(en,dict):
  for k in zh:
   if k in en:register(zh[k],en[k])
for n in range(1,7):
 en=ROOT/f'data/en/ch{n}.json';lp=ROOT/f'data/learn/ch{n}.json'
 if en.exists():register(json.loads((ROOT/f'data/ch{n}.json').read_text()),json.loads(en.read_text()))
 if lp.exists():learn.update(json.loads(lp.read_text()))
if (ROOT/'data/en/exams.json').exists():register(json.loads((ROOT/'data/exams.json').read_text()),json.loads((ROOT/'data/en/exams.json').read_text()))
ui_path=ROOT/'data/ui.json'
if ui_path.exists():translations.update(json.loads(ui_path.read_text()))
ordered=None
def tr(text):
 global ordered
 if not CJK.search(text):return text
 if text in translations:return translations[text]
 if ordered is None:ordered=sorted(translations,key=len,reverse=True)
 result=text
 # Full fields inside compound Markdown must be translated before numeric labels change.
 for source in ordered:
  if len(source)>20 and source in result:result=result.replace(source,translations[source])
 for pattern,repl in [
 (r'(\d+) 组知识点与推导 · (\d+) 道主编号习题 · 每题含思路、过程和答题套路',r'\1 concept sets · \2 numbered exercises · Each includes a plan, working, and reusable method'),
 (r'回顾第\s*(\d+)\s*章 →',r'Review Chapter \1 →'),(r'第\s*(\d+)\s*章',r'Chapter \1'),(r'第\s*(\d+)\s*题',r'Question \1'),
 (r'(\d+) 道教材习题',r'\1 textbook exercises'),(r'(\d+) 道主编号题',r'\1 numbered exercises'),
 (r'从教材 p\.(\d+) 开始',r'From textbook p.\1'),
 (r'教材习题 ([\d.]+)',r'Textbook exercises \1'),(r'习题 ([\d.]+)',r'Exercise \1'),(r'教材 p\.',r'Textbook p.'),
 (r'(\d+) 分钟',r'\1 minutes'),(r'(\d+) 分',r'\1 points'),(r'(\d+) 题',r'\1 questions')]:result=re.sub(pattern,repl,result)
 # Replace complete known prose fragments, longest first.
 for source in ordered:
  if source in result:result=result.replace(source,translations[source])
 if CJK.search(result):missing.add(text)
 return result

def pair(zh,en):
 if zh==en:return html.escape(zh)
 return '<span class="i18n"><span class="lang-zh" lang="zh-CN">'+html.escape(zh)+'</span><span class="lang-en" lang="en">'+html.escape(en)+'</span></span>'

def bilingual_md(source,render):
 en=tr(source)
 zh_html=render(source)
 if en==source:return zh_html
 en_html=render(en)
 # Pair corresponding paragraphs so bilingual readers do not have to hunt below long solutions.
 z=LH.fragment_fromstring(zh_html,create_parent='div');e=LH.fragment_fromstring(en_html,create_parent='div')
 if len(z)==len(e) and not (z.text or e.text):
  out=[]
  for a,b in zip(z,e):
   za=etree.tostring(a,encoding='unicode',method='html');eb=etree.tostring(b,encoding='unicode',method='html')
   if za==eb:out.append(za)
   else:out.append('<div class="language-pair"><div class="lang-zh" lang="zh-CN">'+za+'</div><div class="lang-en" lang="en">'+eb+'</div></div>')
  return ''.join(out)
 return '<div class="language-pair"><div class="lang-zh" lang="zh-CN">'+zh_html+'</div><div class="lang-en" lang="en">'+en_html+'</div></div>'

def localize(document):
 root=LH.document_fromstring(document)
 def skip(el):return any(a.tag in ['script','style','math','title'] or 'lang-zh' in a.get('class','').split() or 'lang-en' in a.get('class','').split() for a in [el,*el.iterancestors()])
 for el in list(root.iter()):
  if not isinstance(el.tag,str) or skip(el):continue
  for attr in ['aria-label','placeholder','title']:
   value=el.get(attr)
   if value and CJK.search(value):el.set('data-'+attr+'-zh',value);el.set('data-'+attr+'-en',tr(value))
  if el.tag=='option':
   value=el.text or ''
   if CJK.search(value):el.set('data-text-zh',value);el.set('data-text-en',tr(value))
   continue
  if el.text and CJK.search(el.text):
   value=el.text;el.text=None;holder=LH.fragment_fromstring('<span class="i18n">'+pair(value,tr(value))+'</span>');el.insert(0,holder)
  for child in list(el):
   if child.tail and CJK.search(child.tail):
    value=child.tail;child.tail=None;holder=LH.fragment_fromstring('<span class="i18n">'+pair(value,tr(value))+'</span>');el.insert(el.index(child)+1,holder)
 title=root.find('.//title')
 if title is not None:title.set('data-text-zh',title.text);title.set('data-text-en',tr(title.text))
 return '<!doctype html>'+etree.tostring(root,encoding='unicode',method='html')

def controls():
 return '''<section class="reader-controls" aria-label="阅读设置"><label>语言<select id="reading-language"><option value="zh">中文</option><option value="en">English</option><option value="both">中英对照</option></select></label><label>字号<select id="reading-size"><option value="comfortable">舒适 · 22px</option><option value="large">大字 · 26px</option><option value="largest">特大 · 30px</option></select></label><label>对比度<select id="reading-contrast"><option value="high">高对比</option><option value="soft">柔和</option></select></label><p>设置自动记住，所有页面通用。</p></section>'''

def guided(ident,md):
 if ident not in learn:raise ValueError('Missing beginner guide '+ident)
 x=learn[ident];z=x['zh'];e=x['en']
 def bm(a,b):register(a,b);return md(a)
 steps=''.join('<li class="guided-step">'+bm(a,b)+'</li>' for a,b in zip(z['steps'],e['steps']))
 return '<div class="problem-entry"><strong>'+pair('这道题要你做什么','What are you trying to find?')+'</strong>'+bm(z['goal'],e['goal'])+'<strong>'+pair('看到什么，就想到这个方法','Clue → choice of method')+'</strong>'+bm(z['recognize'],e['recognize'])+'</div><details class="reveal guided"><summary>'+pair('不会做？带我一步一步做','Guide me, one step at a time')+'<span aria-hidden="true">＋</span></summary><div class="reveal-body"><p class="guide-counter" aria-live="polite"></p><ol class="guided-steps">'+steps+'</ol><div class="guide-controls"><button type="button" class="guide-prev">'+pair('上一步','Previous')+'</button><button type="button" class="guide-next primary-btn">'+pair('下一步','Next step')+'</button><button type="button" class="guide-all">'+pair('显示全部步骤','Show all steps')+'</button></div><div class="self-check"><strong>'+pair('停一下，试着回答','Pause and check')+'</strong>'+bm(z['check']['question'],e['check']['question'])+'<details class="reveal"><summary>'+pair('核对这个小问题','Check this answer')+'</summary><div class="reveal-body">'+bm(z['check']['answer'],e['check']['answer'])+'</div></details></div></div></details>'

def finish():
 (ROOT/'assets/ui-data.js').write_text('window.REVIEW_TRANSLATIONS='+json.dumps(json.loads(ui_path.read_text()),ensure_ascii=False)+';')
 (ROOT/'data/untranslated.json').write_text(json.dumps(sorted(missing),ensure_ascii=False,indent=2))
