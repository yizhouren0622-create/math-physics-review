'use strict';
(()=>{
 const root=document.documentElement,key='math-physics-display-v2';
 const lang=()=>root.dataset.language||'zh';
 function t(zh,en){en=en||window.REVIEW_TRANSLATIONS?.[zh]||zh;return lang()==='en'?en:lang()==='both'&&en!==zh?zh+' / '+en:zh;}
 window.reviewText=t;window.reviewLanguage=lang;
 function apply(){
  root.lang=lang()==='en'?'en':'zh-CN';
  document.querySelectorAll('[data-text-zh]').forEach(el=>el.textContent=t(el.dataset.textZh,el.dataset.textEn));
  for(const attr of ['aria-label','placeholder','title'])document.querySelectorAll('[data-'+attr+'-zh]').forEach(el=>el.setAttribute(attr,t(el.getAttribute('data-'+attr+'-zh'),el.getAttribute('data-'+attr+'-en'))));
  for(const kind of ['language','size','contrast']){const el=document.getElementById('reading-'+kind);if(el)el.value=root.dataset[kind];}
 }
 for(const kind of ['language','size','contrast'])document.getElementById('reading-'+kind)?.addEventListener('change',e=>{
  root.dataset[kind]=e.target.value;try{localStorage.setItem(key,JSON.stringify({language:lang(),size:root.dataset.size,contrast:root.dataset.contrast}));}catch{}
  apply();document.dispatchEvent(new Event('review:language-change'));
 });
 apply();
 document.querySelectorAll('.guided').forEach(guide=>{
  const steps=[...guide.querySelectorAll('.guided-step')],prev=guide.querySelector('.guide-prev'),next=guide.querySelector('.guide-next'),all=guide.querySelector('.guide-all'),counter=guide.querySelector('.guide-counter');let current=0,showAll=false;
  function draw(){steps.forEach((step,i)=>{step.hidden=!showAll&&i!==current;step.setAttribute('aria-label',t('第 '+(i+1)+' 步','Step '+(i+1)));});prev.disabled=showAll||current===0;next.disabled=showAll||current===steps.length-1;all.setAttribute('aria-pressed',String(showAll));counter.textContent=showAll?t('完整步骤 · 共 '+steps.length+' 步','All '+steps.length+' steps'):t('第 '+(current+1)+' / '+steps.length+' 步：先完成眼前这一步','Step '+(current+1)+' of '+steps.length+': focus on this step');all.textContent=showAll?t('返回逐步学习','Return to one step at a time'):t('显示全部步骤','Show all steps');}
  prev.addEventListener('click',()=>{current=Math.max(0,current-1);draw();});next.addEventListener('click',()=>{current=Math.min(steps.length-1,current+1);draw();});all.addEventListener('click',()=>{showAll=!showAll;draw();});document.addEventListener('review:language-change',draw);draw();
 });
})();
