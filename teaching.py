"""Render beginner-first worked examples and reference solutions."""
import json
import re
from pathlib import Path
import reader

ROOT=Path(__file__).resolve().parent
examples=json.loads((ROOT/'data/examples.json').read_text())
for example in examples.values():
    reader.register(example['zh'],example['en'])

def _pair_md(zh,en,md):
    reader.register(zh,en)
    return md(zh)

def _label(zh,en):
    reader.register(zh,en)
    return reader.pair(zh,en)

def _short_lines(text,english=False):
    if english:return re.sub(r'(?<=[.!?])\s+(?=[A-Z])','\n\n',text)
    return re.sub(r'(?<=[。！？])\s*','\n\n',text).strip()

def _paragraphs(text,english=False):
    return [part.strip() for part in _short_lines(text,english).split('\n\n') if part.strip()]

def _step_cards(zh,en,md,css='calculation-steps'):
    zp,ep=_paragraphs(zh),_paragraphs(en,True)
    if len(zp)!=len(ep):
        return '<div class="solution-prose">'+_pair_md(_short_lines(zh),_short_lines(en,True),md)+'</div>'
    items=[]
    for index,(z,e) in enumerate(zip(zp,ep),1):
        items.append('<li><div class="step-number">'+_label(f'第 {index} 步',f'Step {index}')+'</div><div class="step-calculation">'+_pair_md(z,e,md)+'</div></li>')
    return '<ol class="'+css+'">'+''.join(items)+'</ol>'

def worked_example(concept_id,md):
    item=examples[concept_id];zh,en=item['zh'],item['en']
    steps=[]
    for index,(z,e) in enumerate(zip(zh['steps'],en['steps']),1):
        steps.append(
            '<li class="worked-step"><div class="worked-step-title"><span>'+_label(f'第 {index} 步',f'Step {index}')+'</span><strong>'+_label(z['title'],e['title'])+'</strong></div>'
            '<div class="worked-why"><b>'+_label('为什么这样做','Why this step')+'</b>'+_pair_md(z['why'],e['why'],md)+'</div>'
            '<div class="worked-calc"><b>'+_label('具体怎么算','Calculation')+'</b>'+_pair_md(z['work'],e['work'],md)+'</div></li>'
        )
    checks=''.join('<li>'+_pair_md(z,e,md)+'</li>' for z,e in zip(zh['check'],en['check']))
    return (
        '<details class="reveal worked-example"><summary>'+_label('做一道简单例题：按步骤看计算','Worked example: follow each calculation')+'<span aria-hidden="true">＋</span></summary><div class="reveal-body">'
        '<div class="worked-question"><strong>'+_label('题目','Problem')+'</strong>'+_pair_md(zh['question'],en['question'],md)+'</div>'
        '<div class="problem-map worked-map"><div><strong>'+_label('已知什么','Given')+'</strong>'+_pair_md(zh['given'],en['given'],md)+'</div><div><strong>'+_label('要求什么','Find')+'</strong>'+_pair_md(zh['goal'],en['goal'],md)+'</div></div>'
        '<ol class="worked-steps">'+''.join(steps)+'</ol>'
        '<div class="worked-check"><strong>'+_label('做完以后这样检查','Check after solving')+'</strong><ul>'+checks+'</ul></div>'
        '</div></details>'
    )

def exercise_solution(idea,solution,answer,md):
    en_idea,en_solution,en_answer=reader.tr(idea),reader.tr(solution),reader.tr(answer)
    return (
        '<details class="reveal solution reference-solution"><summary>'+_label('参考完整解答：先看分步讲解再打开','Full reference solution: use after the guided steps')+'<span aria-hidden="true">＋</span></summary><div class="reveal-body">'
        '<div class="solution-route"><strong>'+_label('整道题的路线','Plan for the whole problem')+'</strong>'+_pair_md(idea,en_idea,md)+'</div>'
        '<h4 class="calculation-heading">'+_label('把计算一行一行写出来','Write the calculation line by line')+'</h4>'+_step_cards(solution,en_solution,md)
        +'<div class="final-answer"><strong>'+_label('最后答案','Final answer')+'</strong>'+_pair_md(answer,en_answer,md)+'</div></div></details>'
    )

def compact_solution(label_zh,label_en,solution,md,extra_zh='',extra_en='',css_class=''):
    en_solution=reader.tr(solution)
    extra=''
    if extra_zh:
        extra='<div class="final-answer"><strong>'+_label('核对要点','Checkpoints')+'</strong>'+_pair_md(extra_zh,extra_en or reader.tr(extra_zh),md)+'</div>'
    return '<details class="reveal solution structured-solution '+css_class+'"><summary>'+_label(label_zh,label_en)+'<span aria-hidden="true">＋</span></summary><div class="reveal-body">'+_step_cards(solution,en_solution,md)+extra+'</div></details>'
