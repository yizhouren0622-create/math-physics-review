"""Build a standalone, dependency-free HTML study site. Python deps are build-only."""
import json, re, html, shutil
from pathlib import Path
import markdown
from latex2mathml.converter import convert
import reader
import practice

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
chapters=[json.loads(p.read_text()) for p in sorted(DATA.glob('ch[1-6].json'))]
exams=json.loads((DATA/'exams.json').read_text()) if (DATA/'exams.json').exists() else []
sources=json.loads((DATA/'sources.json').read_text()) if (DATA/'sources.json').exists() else {}
failures=[]
def esc(x):return html.escape(str(x),quote=True)
def render_md(x):
    if not x:return ''
    tokens=[]
    def math(m):
        block=m.group(1) is not None
        latex=m.group(1) if block else m.group(2)
        try:
            rendered=convert(latex,display='block' if block else 'inline')
            if block:rendered='<div class="equation" tabindex="0">'+rendered+'</div>'
            else:rendered='<span class="inline-equation">'+rendered+'</span>'
        except Exception as e:
            failures.append((latex,str(e)))
            rendered='<code class="math-error">'+esc(latex)+'</code>'
        key='MATHTOKEN'+str(len(tokens))+'END';tokens.append(rendered);return key
    s=re.sub(r'\$\$(.*?)\$\$|(?<!\\)\$([^$\n]+?)(?<!\\)\$',math,str(x),flags=re.S)
    s=markdown.markdown(s,extensions=['tables','sane_lists'])
    for i,t in enumerate(tokens):
        key='MATHTOKEN'+str(i)+'END'
        if t.startswith('<div'):s=s.replace('<p>'+key+'</p>',t)
        s=s.replace(key,t)
    return s
def md(x):return reader.bilingual_md(x,render_md) if x else ''
introductions=json.loads((DATA/'introductions.json').read_text())
for intro in introductions.values():reader.register(intro['zh'],intro['en'])
def equation(x):return md('$$'+x+'$$')
def details(label,body,kind=''):
    return f'<details class="reveal {kind}"><summary>{esc(label)}<span aria-hidden="true">＋</span></summary><div class="reveal-body">{md(body)}</div></details>'

nav=[('beginner.html','从这里开始','→'),('index.html','学习总览','◈'),('chapter-1.html','知识点与证明','∑'),('exercises.html','课后习题全解','⌘'),('exams.html','模拟考场','◷'),('memory.html','记忆与回顾','◇'),('sources.html','资料与勘误','↗')]
def page(filename,title,content,active='',description=''):
    links=''.join(f'<a href="{href}"'+(' class="active" aria-current="page"' if active==href else '')+f'><span aria-hidden="true">{symbol}</span>{label}</a>' for href,label,symbol in nav)
    chapterlinks=''.join(f'<a href="chapter-{c["chapter"]}.html"><span>{c["chapter"]:02d}</span>{esc(c["title"])}</a>' for c in chapters)
    out=f'''<!doctype html><html lang="zh-CN" data-language="zh" data-size="comfortable" data-contrast="high"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#f6f5f0"><meta name="description" content="{esc(description or '上海大学姜颖《数学物理方法》复习：知识点、展开证明、例题、全书习题解析和自编模拟卷。')}"><title>{esc(title)} · 数学物理复习</title><link rel="icon" href="assets/icon.svg" type="image/svg+xml"><script src="assets/preferences.js?v=20261013-2"></script><link rel="stylesheet" href="assets/site.css?v=20261013-2"></head><body>
<a class="skip" href="#main">跳到正文</a><aside class="sidebar" id="sidebar"><a class="brand" href="index.html"><span class="brand-mark">ψ</span><span>数学物理方法<small>理解 · 记忆 · 解题</small></span></a><p class="nav-label">复习工作台</p><nav aria-label="主要导航">{links}</nav><p class="nav-label chapter-label">教材章节</p><nav class="chapter-nav" aria-label="章节导航">{chapterlinks}</nav><div class="sidebar-foot"><span class="online-dot"></span> 静态网页 · 可离线阅读<small>姜颖教材 · 上海大学</small></div></aside>
<div class="workspace"><header class="topbar"><button class="menu-btn" type="button" aria-label="打开导航" aria-controls="sidebar" aria-expanded="false">☰</button><span class="breadcrumb">数学物理方法 <span>/</span> {esc(title)}</span><div class="top-actions"><a href="search.html" class="search-link">⌕ <span>搜索知识点与题号</span> <kbd>/</kbd></a><button type="button" class="print-btn" aria-label="打印当前页">打印</button></div></header><main id="main">{reader.controls()}{content}</main><footer>按教材章节组织 · 解析与模拟卷独立编写 · <a href="sources.html">参考来源与修订记录</a><span>学习记录仅保存在当前浏览器</span></footer></div><div id="toast" role="status" aria-live="polite"></div><script src="assets/ui-data.js?v=20261013-2" defer></script><script src="assets/reader.js?v=20261013-2" defer></script><script src="assets/site.js?v=20261013-2" defer></script></body></html>'''
    (ROOT/filename).write_text(reader.localize(out))

def heading(kicker,title,subtitle='',extra=''):
    return f'<div class="page-heading"><p class="eyebrow">{esc(kicker)}</p><h1>{esc(title)}</h1><p class="subtitle">{esc(subtitle)}</p>{extra}</div>'

def concept_card(item,chapter=None):
    ident=f'c{chapter}-{item["id"]}' if chapter else item['id']
    example=item.get('example',{})
    return f'''<article class="concept card" id="{esc(ident)}" data-memory-id="{esc(ident)}"><div class="card-eyebrow">知识点 <span class="tag">理解后再记忆</span></div><h3>{esc(item['title'])}</h3><div class="plain-intro"><strong>先用一句话理解</strong>{md(introductions[item['id']]['zh'])}</div>{details('再看数学表述',item.get('explain',''))}{equation(item['formula']) if item.get('formula') else ''}<div class="conditions"><strong>使用条件</strong>{md(item.get('conditions',''))}</div>{details('展开证明 / 推导',item.get('proof',''))}{details('做一道简单例题',example.get('question','')+'\n\n**解答**\n\n'+example.get('solution',''))}{practice.render(item['id'],chapter,md)}<div class="memory-note"><span>记忆线索</span>{md(item.get('memory',''))}</div><button type="button" class="text-btn mark-memory" data-id="{esc(ident)}">加入记忆回顾</button></article>'''

def exercise_card(e,c):
    ident=e['id'];err=e.get('errata')
    return f'''<article class="exercise card" id="ex-{esc(ident)}" data-ex-id="{esc(ident)}"><div class="exercise-meta"><span class="pill">习题 {esc(e['section'])} · {e['number']}</span><span>教材 p.{e['page']} / PDF p.{e['page']+9}</span>{'<span class="tag errata-tag">条件 / 勘误</span>' if err else ''}</div><h3>{esc(e['title'])}</h3><div class="question">{md(e['question'])}</div>{'<div class="errata"><strong>读题注意</strong>'+md(err)+'</div>' if err else ''}<label class="scratch-label" for="note-{esc(ident)}">先写下你的思路</label><textarea class="scratch" id="note-{esc(ident)}" data-note="{esc(ident)}" rows="2" placeholder="我准备使用的定理、关键一步……（自动保存在本机）"></textarea>{reader.guided(ident,md)}{details('提示：从哪里入手',e.get('hint') or e.get('idea',''),'hint')}{details('查看完整计算与答案','**解题思路**\n\n'+e.get('idea','')+'\n\n**逐步解答**\n\n'+e['solution']+'\n\n**最终答案**\n\n'+e['answer'],'solution')}{details('这一类题的答题套路与易错点','**可复用步骤**\n\n'+e['pattern']+'\n\n**易错点**\n\n'+e['pitfall'],'pattern')}<div class="exercise-actions"><button type="button" data-progress="{esc(ident)}" data-state="review">↻ 需要复习</button><button type="button" data-progress="{esc(ident)}" data-state="mastered">✓ 已能独立完成</button><a href="#ex-{esc(ident)}" class="text-btn">题目链接</a></div></article>'''

total=sum(len(c['exercises']) for c in chapters)
concepts=[(c,x) for c in chapters for s in c['sections'] for x in s['concepts']]
cards=''
colors=['mint','blue','ochre','pink','lavender','blue']
for c,color in zip(chapters,colors):
    i=c['chapter'];first=c['sections'][0]['page'];count=len(c['exercises'])
    cards+=f'<a class="chapter-card {color}" href="chapter-{i}.html"><div><span class="chapter-number">{i:02d}</span><span class="chapter-count">{count} 道教材习题</span></div><h3>{esc(c["title"])}</h3><p>{" · ".join(esc(s["title"]) for s in c["sections"][:3])}</p><div class="chapter-progress" data-chapter="{i}"><i></i></div><div class="chapter-bottom"><span>从教材 p.{first} 开始</span><span aria-hidden="true">↗</span></div></a>'
home=heading('SHU · MATHEMATICAL METHODS','把知识连起来，把题目做明白。','从概念出发，跟着推导理解公式，再用题目检验自己。')
home+=f'''<section class="hero"><div><p class="eyebrow">你的复习，从这里开始</p><h2>先理解为什么，<br>再练习怎么做。</h2><p>证明和答案默认收起。给自己一点思考时间，<br class="desktop">需要时再展开下一步。</p><a class="primary-btn" href="beginner.html">从零开始学 <span>→</span></a><a class="hero-secondary" href="exercises.html">按题号查解析 ↗</a></div><div class="hero-math" aria-hidden="true"><span class="math-orbit orbit-a"></span><span class="math-orbit orbit-b"></span><span class="hero-sigma">∮</span><span class="math-label label-a">解析 · 变换</span><span class="math-label label-b">边界 · 本征值</span><span class="math-label label-c">一个方法，连接多种问题</span><div class="hero-equation">{equation(r'\oint_C f(z)\,dz=2\pi i\sum_k\operatorname{Res}_{z=z_k}f')}</div></div></section>
<section class="stats" aria-label="学习概览"><div><span>教材章节</span><strong>{len(chapters):02d}<small>章</small></strong></div><div><span>知识点与推导</span><strong>{len(concepts)}<small>组</small></strong></div><div><span>全部主编号习题</span><strong>{total}<small>道</small></strong></div><div><span>我已独立完成</span><strong id="mastered-count">0<small>道</small></strong></div></section>
<div class="section-title"><div><p class="eyebrow">从教材到考试</p><h2>六章知识，逐步掌握</h2></div><a href="exercises.html">查看全部习题 →</a></div><section class="chapter-grid">{cards}</section>
<section class="study-strip"><div class="strip-symbol">01 → 02 → 03</div><div><h3>建议这样复习</h3><p>先读知识点，合上证明试着复述；再独立做例题和课后题；最后限时做模拟卷，把卡住的题加入回顾。</p></div><a href="exams.html" class="outline-btn">进入模拟考场 →</a></section><section class="review-queue card"><div class="section-title"><h2>留给下一次的题</h2><a href="memory.html">打开记忆回顾 →</a></div><div id="review-list"><p class="muted">在习题下点击“需要复习”，这里就会显示你的回顾清单。</p></div></section>'''
page('index.html','学习总览',home,'index.html')

for c in chapters:
    i=c['chapter'];n=len(c['exercises']);nconcept=sum(len(s['concepts']) for s in c['sections'])
    h=heading(f'CHAPTER {i:02d} · 教材精读',c['title'],f'{nconcept} 组知识点与推导 · {n} 道主编号习题 · 每题含思路、过程和答题套路')
    h+='<div class="view-tabs" role="group" aria-label="章节视图"><button type="button" class="selected" data-view="concepts">知识点与证明</button><button type="button" data-view="exercises">课后题全解</button></div>'
    reader.register('每张知识卡末尾都有“学完试一题”。先做，再按需要展开提示；完成后继续相关的教材题。','Each concept ends with a Try it yourself problem. Attempt it first, open hints as needed, then continue with the related textbook exercise.')
    h+='<p class="notice">'+reader.pair('每张知识卡末尾都有“学完试一题”。先做，再按需要展开提示；完成后继续相关的教材题。','Each concept ends with a Try it yourself problem. Attempt it first, open hints as needed, then continue with the related textbook exercise.')+'</p>'
    h+='<div class="chapter-layout"><aside class="local-toc"><p>本章目录</p>'+''.join(f'<a href="#section-{s["id"]}">{s["id"]} {esc(s["title"])}</a>' for s in c['sections'])+f'<a href="chapter-{i+1}.html">下一章 →</a>'*(i<6)+'</aside><div class="chapter-content">'
    h+='<div data-panel="concepts">'
    for s in c['sections']:
        section_practice=f'<a href="#exercise-section-{s["id"]}" data-switch-exercises>练习这一节 →</a>' if any(e['section']==s['id'] for e in c['exercises']) else '<span class="muted">本节无书后习题</span>'
        h+=f'<section id="section-{s["id"]}" class="study-section"><div class="section-title"><div><p class="eyebrow">SECTION {s["id"]} · 教材 p.{s["page"]}</p><h2>{esc(s["title"])}</h2></div>{section_practice}</div>'
        h+=''.join(concept_card(x,i) for x in s['concepts'])+'</section>'
    h+='</div><div data-panel="exercises">'
    for s in c['sections']:
        ee=[e for e in c['exercises'] if e['section']==s['id']]
        if not ee:continue
        h+=f'<section class="study-section" id="exercise-section-{s["id"]}"><div class="section-title"><div><p class="eyebrow">教材习题 {s["id"]}</p><h2>{esc(s["title"])}</h2></div><span class="muted">{len(ee)} 道主编号题</span></div>'+''.join(exercise_card(e,c) for e in ee)+'</section>'
    h+='</div></div></div>'
    page(f'chapter-{i}.html',c['title'],h,'chapter-1.html')

h=heading('EXERCISE LIBRARY','每一道课后题，都有来路。',f'按教材原节号与题号定位。共 {total} 道主编号题；题内各小问在解析中分别展开。')
h+='<div class="notice">先做题，再看提示，最后核对过程。带“条件 / 勘误”的题目会说明原题的适用条件或需要修正的地方。</div><div class="filter-bar"><label for="exercise-search">查找题目</label><input id="exercise-search" type="search" placeholder="输入题号、方法或关键词，例如 3.1、留数、边界"><label for="chapter-filter">章节</label><select id="chapter-filter"><option value="">全部章节</option>'+''.join(f'<option value="{c["chapter"]}">第{c["chapter"]}章 {esc(c["title"])}</option>' for c in chapters)+'</select><label class="check-label"><input type="checkbox" id="review-filter">只看待复习</label></div><p id="filter-count" class="muted" aria-live="polite"></p><div class="exercise-index">'
for c in chapters:
    for e in c['exercises']:
        h+=f'<a class="exercise-row" data-chapter="{c["chapter"]}" data-id="{e["id"]}" data-search="{esc(e["id"]+" "+e["title"]+" "+e["question"]+" "+reader.tr(e["title"])+" "+reader.tr(e["question"]))}" href="chapter-{c["chapter"]}.html#ex-{e["id"]}"><span class="row-number">{e["section"]} · {e["number"]}</span><div><strong>{esc(e["title"])}</strong><small>第{c["chapter"]}章 · 教材 p.{e["page"]}'+(' · 含条件说明 / 勘误' if e.get('errata') else '')+f'</small></div><span class="progress-badge" data-badge="{e["id"]}">未标记</span><span aria-hidden="true">↗</span></a>'
h+='</div><p id="empty-filter" hidden class="empty">没有符合条件的题目。试试更短的关键词或取消筛选。</p>'
page('exercises.html','课后习题全解',h,'exercises.html')

h=heading('MOCK EXAM','把学过的，放进一张试卷。','自编模拟卷 · 提示和答案默认收起 · 计时与自评均保存在本机')
h+='<div class="exam-grid">'
for j,e in enumerate(exams,1):
    h+=f'<a class="exam-cover card" href="exam-{j}.html"><span class="eyebrow">PAPER {j:02d}</span><h2>{esc(e["title"])}</h2><p>{esc(e["scope"])}</p><div><span>{e["minutes"]} 分钟</span><span>{sum(q["points"] for q in e["questions"])} 分</span><span>{len(e["questions"])} 题</span></div><strong>开始独立作答 →</strong></a>'
h+='</div><div class="notice">模拟卷用于检验方法掌握程度，题型与分值为本站编排。完成后可按每题评分要点自评，并回到相应章节查漏补缺。</div>'
page('exams.html','模拟考场',h,'exams.html')
for j,e in enumerate(exams,1):
    h=heading(f'PAPER {j:02d} · 自编模拟卷',e['title'],e['scope'])
    h+=f'<section class="exam-toolbar card" data-exam="{j}" data-minutes="{e["minutes"]}"><div><span class="eyebrow">剩余时间</span><strong class="timer" aria-live="off">{e["minutes"]:02d}:00</strong></div><button type="button" class="primary-btn timer-start">开始计时</button><button type="button" class="outline-btn timer-reset">重新计时</button><div class="exam-score">我的自评 <strong id="score-total">0</strong> / 100</div><button type="button" class="text-btn close-answers">收起全部答案</button></section>'
    for k,q in enumerate(e['questions'],1):
        h+=f'<article class="exam-question card" id="q{k}"><div class="exercise-meta"><span class="pill">第 {k} 题</span><span>{q["points"]} 分 · {esc(q["topic"])}</span></div><h3>{esc(q["title"])}</h3>{md(q["question"])}<label class="scratch-label" for="exam-note-{j}-{k}">我的作答</label><textarea class="scratch" data-note="exam-{j}-{k}" id="exam-note-{j}-{k}" rows="3" placeholder="在纸上计算，也可在这里记录关键步骤。"></textarea>{details("展开提示",q["hint"],"hint")}{details("展开答案与评分要点",q["solution"]+"\n\n**评分要点**\n\n"+q["rubric"],"solution")}<div class="score-control"><label for="score-{j}-{k}">本题自评分</label><input id="score-{j}-{k}" class="score-input" type="number" min="0" max="{q["points"]}" value="0" data-score-key="{j}-{k}"><span>/ {q["points"]}</span><a href="chapter-{q["chapter"]}.html">回顾第 {q["chapter"]} 章 →</a></div></article>'
    page(f'exam-{j}.html',e['title'],h,'exams.html')

h=heading('ACTIVE RECALL','合上答案，试着讲给自己听。','先复述公式、使用条件和关键一步，再展开检查。掌握后安排下一次回顾。')
h+='<div class="memory-toolbar"><label class="check-label"><input type="checkbox" id="due-only">只看今天到期与已加入的卡片</label><span id="memory-count" class="muted" aria-live="polite"></span></div><div class="memory-grid">'
for c,x in concepts:
    ident=f'c{c["chapter"]}-{x["id"]}'
    body='**关键公式**\n\n$$'+x.get('formula','')+'$$\n\n**使用条件**\n\n'+x.get('conditions','')+'\n\n**记忆线索**\n\n'+x.get('memory','')
    h+=f'<article class="memory-card card" data-card-id="{esc(ident)}"><p class="eyebrow">第 {c["chapter"]} 章 · 主动回忆</p><h3>{esc(x["title"])}</h3><p>不看答案，写出公式，并说出它何时可以使用。</p>{details("展开核对",body)}<p class="memory-due" data-due="{esc(ident)}">尚未安排回顾</p><div class="memory-grades"><button type="button" data-grade="again" data-id="{esc(ident)}">再练一次</button><button type="button" data-grade="good" data-id="{esc(ident)}">已能复述</button></div><a href="chapter-{c["chapter"]}.html#{ident}" class="text-btn">返回完整讲解 →</a></article>'
h+='</div><div class="record-tools card"><h2>我的学习记录</h2><p>思路笔记、题目状态、记忆回顾和模拟卷自评保存在本机。可导出备份后在另一台设备导入。</p><button class="outline-btn" type="button" id="export-progress">导出学习记录</button><label class="outline-btn import-label">导入学习记录<input type="file" id="import-progress" accept="application/json,.json"></label></div>'
page('memory.html','记忆与回顾',h,'memory.html')

h=heading('SOURCES & CORRECTIONS','知道结论，也知道它的条件。','教材定位、公开参考链接与发现的问题，集中保留在这里。')
h+='<section class="card prose"><h2>教材与页码</h2><p>本网站依据用户提供的姜颖《数学物理方法》（科学出版社，ISBN 978-7-03-057435-0）教材组织。页面引用的是书内印刷页码；所提供 PDF 的对应页为印刷页码加 9。题干按教材题号转写，解题步骤、知识解释和模拟卷独立编写。</p><h2>教师公开参考答案</h2><p>以下是“上大老姜”的公开答案来源。本站不把仅找到链接的章节标为已核对；第二、四章参考图片中发现的具体差异已写入相关解析。</p><ul>'
for s in sources.get('chapters',[]):
    h+=f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">第{s["chapter"]}章{esc(s.get("scope",""))} · 上大老姜公开分享 ↗</a> — '+('已读取参考图片，独立复算后使用' if s.get('imagesRead') else '已确认来源，图片正文未能读取；本站解答独立推导')+'</li>'
h+='</ul><p>访问日期：2026-10-12。第五章其余部分与第六章未找到可读取的对应公开答案；解答不标为已由教师核验。</p><h2>如何看待勘误</h2><p>如果命题条件不足、展开区域包含奇点，或积分只能按主值理解，解析会明确说明。参考解答不是考试官方评分标准；遇到与课堂约定不同的符号或归一化时，优先统一约定再比较。</p></section><div class="section-title"><h2>题目中的条件与勘误</h2></div>'
for c in chapters:
    for e in c['exercises']:
        if e.get('errata'):
            h+=f'<article class="card correction"><a href="chapter-{c["chapter"]}.html#ex-{e["id"]}">习题 {e["section"]} · {e["number"]} →</a>{md(e["errata"])}</article>'
revisions=json.loads((DATA/'revisions.json').read_text()) if (DATA/'revisions.json').exists() else []
if revisions:
    reader.register('本次内容修订','Content revisions')
    reader.register('独立复算与教材核对后的修订记录；未读取的教师答案仍不标为已核验。','Revisions after independent recalculation and textbook checks. Unread teacher references remain unverified.')
    h+='<section class="card prose"><h2>本次内容修订</h2><p>独立复算与教材核对后的修订记录；未读取的教师答案仍不标为已核验。</p>'
    for change in revisions:
        reader.register(change['zh'],change['en'])
        h+=f'<article class="correction"><p><a href="{esc(change["link"])}">{esc(change["label"])}</a> · {esc(change["date"])}</p>'+md(change['zh'])+'</article>'
    h+='</section>'
page('sources.html','资料与勘误',h,'sources.html')

index=[]
for c in chapters:
    for s in c['sections']:
        for x in s['concepts']:
            index.append(dict(type='知识点',label=x['title'],text=x['explain']+' '+x.get('memory',''),url=f'chapter-{c["chapter"]}.html#c{c["chapter"]}-{x["id"]}',chapter=c['chapter']))
            problem=practice.problems[x['id']]
            index.append(dict(type='变式练习',typeEn='Transfer practice',label=x['title'],labelEn=reader.tr(x['title']),text=problem['zh']['prompt'],textEn=problem['en']['prompt'],url=f'chapter-{c["chapter"]}.html#try-c{c["chapter"]}-{x["id"]}',chapter=c['chapter']))
    for e in c['exercises']:index.append(dict(type='习题 '+e['id'],label=e['title'],text=e['question']+' '+e['pattern'],url=f'chapter-{c["chapter"]}.html#ex-{e["id"]}',chapter=c['chapter']))
for item in index:
    for field in ['type','label','text']:
        if field+'En' not in item:item[field+'En']=reader.tr(item[field])
(ROOT/'assets/index-data.js').write_text('window.STUDY_INDEX='+json.dumps(index,ensure_ascii=False)+';\nwindow.STUDY_EXERCISES='+json.dumps([dict(id=e['id'],title=e['title'],titleEn=reader.tr(e['title']),chapter=c['chapter'],url=f'chapter-{c["chapter"]}.html#ex-{e["id"]}') for c in chapters for e in c['exercises']],ensure_ascii=False)+';')
page('search.html','搜索',heading('SEARCH','把不确定的地方，找出来。','支持题号、概念名称与解题方法关键词。')+'<div class="search-box"><label for="global-search">搜索本站</label><input id="global-search" type="search" placeholder="例如：2.4-3、傅里叶、勒让德、格林函数" autofocus></div><p class="muted" id="search-status" aria-live="polite">输入关键词开始搜索。</p><div id="search-results"></div>')

manifest={'chapters':len(chapters),'exercises':total,'concepts':len(concepts),'exercise_ids':[e['id'] for c in chapters for e in c['exercises']],'exam_points':[sum(q['points'] for q in e['questions']) for e in exams],'formula_failures':failures}
(ROOT/'data/coverage.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
if failures:
    print(json.dumps(failures[:30],ensure_ascii=False,indent=2));raise SystemExit(f'{len(failures)} formula rendering errors')
import beginner
beginner.build(page,heading,md,reader)
reader.finish()
print(json.dumps({k:v for k,v in manifest.items() if k not in ['exercise_ids','formula_failures']},ensure_ascii=False))
