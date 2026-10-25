const test=require('node:test');
const assert=require('node:assert/strict');
const {listFor,summarize,makeReport,ITEMS}=require('../assets/planner.js');
test('installation types include common and matching material groups',()=>{
  for(const type of ['roof','ground','carport']){
    const list=listFor(type);
    assert.equal(list.length,10);
    assert.equal(list.filter(x=>x.group==='common').length,7);
    assert.equal(list.filter(x=>x.group===type).length,3);
    assert.equal(new Set(list.map(x=>x.id)).size,10);
  }
});
test('switching type excludes states of the previous installation type',()=>{
  const values={site:'ready',layout:'confirm','roof-drawing':'ready','ground-soil':'confirm'};
  const roof=summarize('roof',values),ground=summarize('ground',values);
  assert.equal(roof.ready.length,2);assert.equal(roof.confirm.length,1);assert.equal(roof.pending.length,7);
  assert.equal(ground.ready.length,1);assert.equal(ground.confirm.length,2);assert.equal(ground.pending.length,7);
  const result=makeReport('ground',values,'A 구역','2026-10-25');
  assert.ok(result.includes('[확인 필요] 지반 관련 보유자료'));
  assert.ok(!result.includes('[준비됨] 기존 건물 구조도면'));
});
test('completed checklist exports preparation counts and its scope limitation',()=>{
  const values=Object.fromEntries(ITEMS.map(x=>[x.id,'ready']));
  const result=makeReport('carport',values,'  주차장 계획  ','2026-10-25');
  assert.ok(result.includes('보유 자료 10 / 10개 항목 · 확인 필요 0개 · 미준비 0개'));
  assert.ok(result.includes('현장 구분: 주차장 계획'));
  assert.ok(result.includes('안전성·설치 가능 여부가 확인되는 것은 아닙니다'));
  assert.ok(result.includes('https://dooja.co.kr/services/solar-structural-review'));
});
test('blank and unexpected states remain missing in the export',()=>{
  const result=makeReport('roof',{site:'unexpected'},'','2026-10-25');
  assert.ok(result.includes('현장 구분: 미기입'));
  assert.ok(result.includes('미준비 10개'));
  assert.ok(!result.includes('기초 형식과 상세도'));
  assert.equal(listFor('unknown').length,10);
});
