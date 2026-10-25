(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;if(root.document)api.mount(root.document,root);})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const TYPES={roof:'지붕형',ground:'지상형',carport:'주차장형'};
  const STATES={pending:'미준비',ready:'준비됨',confirm:'확인 필요'};
  const ITEMS=[
    {id:'site',group:'common',title:'대상 위치와 설치 구역',help:'위치도에 검토할 건물·구역을 구분하고 설치 형식을 적어 주세요.'},
    {id:'purpose',group:'common',title:'검토 목적과 요청 범위',help:'신규 설치, 증설, 배치 변경 등 목적과 필요한 결과물을 정리하세요.'},
    {id:'layout',group:'common',title:'배치도와 도면 버전',help:'모듈 배치·기울기·높이가 표시된 도면의 파일명, 개정번호와 날짜를 확인하세요.'},
    {id:'module',group:'common',title:'모듈과 추가 설비 사양',help:'제품명, 치수, 중량이 표시된 자료와 함께 지지대·부속 설비 자료를 모으세요.'},
    {id:'frame',group:'common',title:'지지구조와 접합 상세',help:'부재 재질·단면·간격, 볼트·클램프·앵커 등 연결 방식이 표시된 자료를 준비하세요.'},
    {id:'photos',group:'common',title:'현장사진과 촬영 위치',help:'안전하게 접근 가능한 위치에서 전체, 지지부, 접합부 사진을 구분해 정리하세요.'},
    {id:'changes',group:'common',title:'변경·보수 이력',help:'설치 후 변경, 부재 교체, 보강·보수 이력의 유무를 확인하고 관련 자료를 모으세요.'},
    {id:'roof-drawing',group:'roof',title:'기존 건물 구조도면·계산서',help:'보유 자료의 작성 시점과 실제 현장 상태가 일치하는지 표시하세요. 없으면 미보유로 알리세요.'},
    {id:'roof-loadpath',group:'roof',title:'지붕과 하부 구조의 연결 정보',help:'지붕재, 퍼린, 보·기둥과 설비 연결 위치를 확인할 수 있는 도면·사진을 모으세요.'},
    {id:'roof-condition',group:'roof',title:'지붕 상태와 기존 설비',help:'누수·부식·변형 여부, 기존 옥상 설비와 지붕 보수 기록을 정리하세요.'},
    {id:'ground-plan',group:'ground',title:'부지 배치와 지형 자료',help:'설치 범위, 지형 차이와 주변 여건을 파악할 수 있는 자료를 모으세요.'},
    {id:'ground-foundation',group:'ground',title:'기초 형식과 상세도',help:'계획한 기초 형식·치수, 기둥과 기초의 연결 상세를 준비하세요.'},
    {id:'ground-soil',group:'ground',title:'지반 관련 보유자료',help:'지반조사보고서 등 보유 여부를 확인하세요. 자료의 적정성은 검토 담당자와 협의합니다.'},
    {id:'carport-plan',group:'carport',title:'주차장 배치와 구조 계획',help:'차량 동선, 기둥 위치, 높이와 경간이 표시된 계획 자료를 모으세요.'},
    {id:'carport-foundation',group:'carport',title:'기초·앵커 계획과 지반자료',help:'상부 구조와 기초의 연결 상세, 사용 가능한 지반자료를 함께 확인하세요.'},
    {id:'carport-existing',group:'carport',title:'기존 구조물 활용 여부',help:'신설인지 기존 시설 위에 추가하는지 구분하고, 기존 시설을 쓰면 해당 도면과 상태 자료를 준비하세요.'}
  ];
  function listFor(type){const safe=Object.hasOwn(TYPES,type)?type:'roof';return ITEMS.filter(x=>x.group==='common'||x.group===safe);}
  function summarize(type,values){const items=listFor(type);const ready=items.filter(x=>values[x.id]==='ready');const confirm=items.filter(x=>values[x.id]==='confirm');const pending=items.filter(x=>!['ready','confirm'].includes(values[x.id]));return {items,ready,confirm,pending};}
  function makeReport(type,values,label,date){const s=summarize(type,values);const lines=['태양광 구조검토 · 준비자료 정리', '작성일: '+date,'현장 구분: '+(label.trim()||'미기입'),'설치 형식: '+(TYPES[type]||TYPES.roof),'','보유 자료 '+s.ready.length+' / '+s.items.length+'개 항목 · 확인 필요 '+s.confirm.length+'개 · 미준비 '+s.pending.length+'개','','[자료 목록]'];s.items.forEach(x=>lines.push('['+(STATES[values[x.id]]||STATES.pending)+'] '+x.title,'  '+x.help));lines.push('','[상담할 때 확인할 질문]','1. 현재 자료로 확인 가능한 범위와 추가 조사·도면 작성이 필요한 범위는 무엇인가요?','2. 지지구조, 접합부, 기존 건물 또는 기초 중 어떤 부분이 검토 범위에 포함되나요?','3. 검토에 사용할 도면 개정번호와 이후 변경 시 재확인 절차는 어떻게 되나요?','4. 결과물의 종류, 제출 목적, 적용 조건과 제외 범위는 어떻게 정하나요?','','이 목록은 보유 자료를 정리하는 도구입니다. 모든 항목을 준비해도 안전성·설치 가능 여부가 확인되는 것은 아닙니다. 실제 필요한 자료는 현장과 검토 범위에 따라 달라집니다.','','자료실: https://starichdog-collab.github.io/solar-structural-review/','운영: 두자(DOOJA)','업무범위 안내: https://dooja.co.kr/services/solar-structural-review');return lines.join('\n');}
  function mount(doc,win){const form=doc.getElementById('preparation-form');if(!form)return;const type=doc.getElementById('system-type'),label=doc.getElementById('site-label'),status=doc.getElementById('download-status');function values(){const out={};form.querySelectorAll('[data-material]').forEach(el=>out[el.dataset.material]=el.value);return out;}function update(){doc.querySelectorAll('[data-system]').forEach(el=>{const inactive=el.dataset.system!==type.value;el.hidden=inactive;el.querySelectorAll('select').forEach(s=>s.disabled=inactive);});const s=summarize(type.value,values());doc.getElementById('ready-count').textContent=s.ready.length;doc.getElementById('total-count').textContent=s.items.length;doc.getElementById('summary-status').textContent='확인 필요 '+s.confirm.length+'개 · 미준비 '+s.pending.length+'개';const list=doc.getElementById('missing-list');list.replaceChildren();const remaining=[...s.confirm,...s.pending];if(!remaining.length){const li=doc.createElement('li');li.textContent='모든 자료를 준비됨으로 표시했습니다. 자료의 내용과 현장 일치 여부는 검토 담당자에게 확인하세요.';list.appendChild(li);}else remaining.forEach(x=>{const li=doc.createElement('li');li.textContent=x.title;list.appendChild(li);});}
    form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('change',()=>{status.textContent='';update();});doc.getElementById('download-report').addEventListener('click',()=>{const now=new Date();const date=new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul'}).format(now);const blob=new Blob(['\ufeff'+makeReport(type.value,values(),label.value,date)],{type:'text/plain;charset=utf-8'});const url=win.URL.createObjectURL(blob),a=doc.createElement('a');a.href=url;a.download='solar-review-preparation-'+date+'.txt';doc.body.appendChild(a);a.click();a.remove();win.setTimeout(()=>win.URL.revokeObjectURL(url),3000);status.textContent='준비자료 정리 파일을 내려받았습니다.';});doc.getElementById('print-report').addEventListener('click',()=>win.print());doc.getElementById('reset-form').addEventListener('click',()=>{form.reset();status.textContent='입력 내용을 초기화했습니다.';update();});update();}
  return {TYPES,STATES,ITEMS,listFor,summarize,makeReport,mount};
});
