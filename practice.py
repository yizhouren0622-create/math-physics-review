"""Small transfer problems: attempt first, then open only as much help as needed."""
import json
from pathlib import Path
import reader
import teaching

problems=json.loads((Path(__file__).resolve().parent/'data/practice.json').read_text())
for problem in problems.values():
    reader.register(problem['zh'],problem['en'])

def render(concept_id,chapter,md):
    problem=problems[concept_id]
    assert problem['chapter']==chapter
    zh,en=problem['zh'],problem['en']
    ident=f'c{chapter}-{concept_id}'
    def text(a,b):
        reader.register(a,b)
        return md(a)
    def reveal(label,label_en,body,body_en,kind):
        return '<details class="reveal '+kind+'"><summary>'+reader.pair(label,label_en)+'<span aria-hidden="true">＋</span></summary><div class="reveal-body">'+text(body,body_en)+'</div></details>'
    labels=[('提示 1：先选方法','Hint 1: choose a method'),('提示 2：写第一行','Hint 2: write the first line'),('提示 3：关键计算','Hint 3: key calculation')]
    hints=''.join(reveal(a,b,z,e,'transfer-hint') for (a,b),z,e in zip(labels,zh['hints'],en['hints']))
    note_id='try-note-'+ident
    out=[
        '<details class="reveal transfer-practice" id="try-'+ident+'"><summary>',
        reader.pair('学完试一题：合上例题，自己做','Try it yourself: close the worked example'),
        '<span aria-hidden="true">＋</span></summary><div class="reveal-body"><p class="practice-instruction">',
        reader.pair('先独立写第一步。卡住时只开一个提示，做完再核对答案。','Write your first step independently. Open one hint if stuck; check the solution after attempting the problem.'),
        '</p><div class="question">',text(zh['prompt'],en['prompt']),
        '</div><label class="scratch-label" for="'+note_id+'">',
        reader.pair('我的起手步骤与计算','My first step and calculation'),
        '</label><textarea class="scratch" id="'+note_id+'" data-note="practice-'+ident+'" rows="2"></textarea>',
        hints,
        teaching.compact_solution('展开分步完整解答','Open the full step-by-step solution',zh['solution'],md,css_class='transfer-solution'),
        reveal('怎样检查，哪里容易错','Check your result and common mistakes',zh['check'],en['check'],'transfer-check'),
        '<button type="button" class="outline-btn" data-close-practice>',
        reader.pair('收起提示与答案','Close hints and solution'),
        '</button><p><a class="practice-textbook" href="chapter-'+str(chapter)+'.html#ex-'+problem['exercise']+'">',
        reader.pair('继续练相关教材题 '+problem['exercise'],'Continue with related textbook exercise '+problem['exercise']),
        ' →</a></p><p class="muted">',
        reader.pair('合上答案重做一次，仍卡住可用下方按钮加入记忆回顾。','Close the solution and try again. Use the button below to add this concept to recall if you still need help.'),
        '</p></div></details>'
    ]
    return ''.join(out)
