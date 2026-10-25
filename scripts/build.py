#!/usr/bin/env python3
"""Build the dependency-free GitHub Pages resource library."""
from pathlib import Path
from html import escape
import json
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://solar.dooja.co.kr/'
DATE = '2026-10-25'
DOE = 'https://www.energy.gov/cmei/femp/life-cycle-photovoltaic-systems-install-and-commission-photovoltaic-system'
KCSC = 'https://www.kcsc.re.kr/standardCode/list/102041'
MATERIALS = json.loads(subprocess.check_output(['node', '-e', "process.stdout.write(JSON.stringify(require('./assets/planner.js').ITEMS))"], cwd=ROOT))
PAGES = {}

def header(active):
    links = [('index.html','자료실'),('preparation.html','준비자료 정리'),('report-reading.html','계산서 읽기')]
    nav = ''.join('<a href="'+('./' if url=='index.html' else url)+'"'+(' aria-current="page"' if url==active else '')+'>'+label+'</a>' for url,label in links)
    return '<a class="skip" href="#main">본문 바로가기</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="https://dooja.co.kr/" aria-label="두자 공식 홈페이지로 이동"><strong>DOOJA.</strong><span>STRUCTURAL<br>RESOURCE LIBRARY</span></a><nav class="nav" aria-label="주 메뉴">'+nav+'<a class="external" href="https://dooja.co.kr/">공식 홈페이지 ↗</a></nav></div></header>'

def footer():
    return '''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><strong>태양광 구조검토 자료실</strong><p>두자(DOOJA)가 운영하는 공개 기술자료 공간입니다.<br>자료 준비와 결과 이해를 돕고, 개별 현장의 검토 범위는 상담에서 확인합니다.</p></div><div><div class="footer-links"><a href="https://dooja.co.kr/services/solar-structural-review">두자건설 업무범위</a><a href="https://dooja.co.kr/#contact">상담 안내</a><a href="https://blog.naver.com/doojasun1">공식 블로그</a></div><p><a href="tel:0222132634">02-2213-2634</a> · <a href="mailto:doojakorea@naver.com">doojakorea@naver.com</a><br>서울 동대문구 장한로24길 21 JK빌딩 5층</p></div></div><div class="footer-bottom"><span>© DOOJA · 자료 편집: 두자(DOOJA) · 수정일 2026.10.25</span><span><a href="sitemap.xml">사이트맵</a> · <a href="feed.xml">RSS</a></span></div></div></footer>'''

def page(path,title,description,body,script=False):
    url=BASE+('' if path=='index.html' else path)
    org={'@type':'Organization','@id':'https://dooja.co.kr/#organization','name':'두자(DOOJA)','alternateName':['두자건설','두자엔지니어링'],'url':'https://dooja.co.kr/'}
    website={'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'태양광 구조검토 자료실 | 두자 DOOJA','inLanguage':'ko-KR','publisher':{'@id':org['@id']}}
    web={'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,'datePublished':DATE,'dateModified':DATE,'inLanguage':'ko-KR','isPartOf':{'@id':website['@id']},'publisher':{'@id':org['@id']},'author':{'@id':org['@id']}}
    crumbs=[{'@type':'ListItem','position':1,'name':'태양광 구조검토 자료실','item':BASE}]
    if path!='index.html': crumbs.append({'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':url})
    schema={'@context':'https://schema.org','@graph':[org,website,web,{'@type':'BreadcrumbList','itemListElement':crumbs}]}
    html='''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'''
    html+='<title>'+escape(title)+'</title><meta name="description" content="'+escape(description,quote=True)+'"><link rel="canonical" href="'+url+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#173b3a"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="두자 태양광 구조검토 자료실"><meta property="og:title" content="'+escape(title,quote=True)+'"><meta property="og:description" content="'+escape(description,quote=True)+'"><meta property="og:url" content="'+url+'"><meta name="twitter:card" content="summary"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><link rel="alternate" type="application/rss+xml" title="태양광 구조검토 자료실" href="'+BASE+'feed.xml"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False)+'</script>'
    if script:html+='<script src="assets/planner.js" defer></script>'
    html+='</head><body>'+header(path)+body+footer()+'</body></html>\n'
    (ROOT/path).write_text(html,encoding='utf-8')
    PAGES[path]={'url':url,'title':title,'description':description}

hero_art='''<figure class="hero-art"><div class="art-label"><span>REVIEW THE WHOLE CONNECTION</span><span>01—03</span></div><svg viewBox="0 0 460 280" role="img" aria-labelledby="art-title art-desc"><title id="art-title">태양광 설비와 지지구조의 연결 개념</title><desc id="art-desc">모듈, 지지대와 접합부, 하부 구조를 각각 구분해 자료를 정리하는 개념도. 실제 시공 상세나 구조계산 모델이 아닙니다.</desc><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#315651" stroke-width=".6"/></pattern></defs><rect width="460" height="280" fill="url(#grid)"/><g fill="none" stroke-linejoin="round"><path d="M57 131 218 55 399 95 236 174Z" fill="#345b53" stroke="#ddef8b" stroke-width="2"/><path d="m108 108 179 42m-125-67 179 42M115 145 279 69m-3 94 164-76" stroke="#9db6a1" stroke-width="1.2"/><path d="M70 144 236 188 388 115M111 155v60m125-27v54m107-108v61M111 215l125 27 107-47m-232-40 125 87m0-54 107 7" stroke="#d9e5d5" stroke-width="3"/><path d="m55 217 187 45 159-76" stroke="#6d9183" stroke-width="8"/><path d="M57 131v-32H25m374-4 26 5v58h17M236 242v25" stroke="#c5d6bc" stroke-width="1" stroke-dasharray="4 4"/></g><g fill="#ddef8b" font-family="monospace" font-size="13"><text x="4" y="97">01</text><text x="431" y="178">02</text><text x="229" y="279">03</text></g><g fill="#ddef8b"><circle cx="111" cy="155" r="4"/><circle cx="236" cy="188" r="4"/><circle cx="343" cy="134" r="4"/></g></svg><div class="legend"><span><b>01 / EQUIPMENT</b>모듈·설비 사양</span><span><b>02 / CONNECTION</b>지지대·접합 상세</span><span><b>03 / STRUCTURE</b>건물·기초 자료</span></div><figcaption>자료를 구분하기 위한 개념도입니다. 실제 시공 상세나 검토 결과를 나타내지 않습니다.</figcaption></figure>'''

home='''<main id="main"><div class="wrap"><section class="hero"><div><p class="eyebrow">DOOJA / TECHNICAL RESOURCES</p><h1><span>태양광 구조검토,</span><span>현장을 설명하는</span><span class="accent-line">자료부터.</span></h1><p class="lead">검토를 의뢰하기 전에는 무엇을 준비하고,<br>계산서를 받은 뒤에는 무엇을 확인해야 할까요?<br>설치 형식과 도면, 검토 조건을 차근차근 정리하세요.</p><div class="button-row"><a class="button" href="preparation.html">준비자료 정리하기 <span aria-hidden="true">↗</span></a><a class="button secondary" href="#reading">자료 둘러보기 <span aria-hidden="true">↓</span></a></div><p class="small">두자(DOOJA) 운영 · 공개 안내와 무료 준비 도구</p></div>'''+hero_art+'''</section><div class="facts-strip"><div>검토 전 <span>보유 자료와 빈칸 정리</span></div><div>검토 중 <span>대상과 도면 버전 확인</span></div><div>검토 후 <span>적용 조건과 변경사항 확인</span></div></div>
<section class="section" id="reading"><p class="section-number">01 / START HERE</p><div class="section-header"><h2>지금 필요한 내용부터<br>찾아보세요.</h2><p>설치 형식에 따라 필요한 정보가 달라집니다. 먼저 자료를 정리하고, 검토 대상과 결과물의 범위를 같은 기준으로 이야기해 보세요.</p></div><ul class="reading-list"><li><span class="number">01</span><h3><a href="preparation.html">구조검토 준비자료 정리 <span class="tag">도구</span></a></h3><p>지붕형·지상형·주차장형을 선택하고, 보유 자료와 확인할 질문을 TXT 파일로 내려받습니다.</p><span class="arrow" aria-hidden="true">↗</span></li><li><span class="number">02</span><h3><a href="report-reading.html">구조계산서 읽는 순서</a></h3><p>검토 대상, 입력 조건, 접합부, 결과의 적용 범위를 도면과 함께 확인하는 방법입니다.</p><span class="arrow" aria-hidden="true">↗</span></li><li><span class="number">03</span><h3><a href="downloads/report-questions.txt" download>결과 확인 질문지 <span class="tag">TXT</span></a></h3><p>검토 담당자에게 물어볼 질문을 메모하고, 답변과 관련 도면을 함께 정리하는 빈 양식입니다.</p><span class="arrow" aria-hidden="true">↓</span></li></ul></section>
<section class="section" id="scope"><p class="section-number">02 / DEFINE THE SCOPE</p><div class="split"><div class="prose"><h2>모듈에서 하부 구조까지,<br>검토 대상을 분명하게.</h2><p>태양광 구조검토는 설비의 무게만 정리하는 작업으로 끝나지 않습니다. 모듈과 지지구조가 어떻게 연결되고, 그 힘이 기존 건물이나 기초로 어떻게 전달되는지 확인할 수 있는 자료가 필요합니다.</p><p>같은 설치 용량이라도 배치, 지지대 간격, 접합 방식, 설치 높이와 기존 구조물의 상태가 다르면 검토 조건도 달라질 수 있습니다. 다른 현장의 결과를 그대로 적용하지 말고 대상 현장의 조건을 구분하세요.</p><div class="callout"><p>이 자료실은 검토 준비와 결과 이해를 돕습니다. 현장별 설계하중 산정, 구조계산, 안전성 판정은 담당 전문가가 실제 자료와 적용 기준을 확인하여 수행해야 합니다.</p></div></div><ol class="steps"><li><strong>지붕형 — 기존 건물과의 관계</strong><p>모듈·지지대 자료에 더해 지붕재, 퍼린, 보·기둥과 연결 부분을 설명할 자료를 모읍니다. 기존 도면과 실제 상태의 차이도 구분합니다.</p></li><li><strong>지상형 — 기초와 지반 조건</strong><p>상부 구조 계획, 기초 상세와 지반 관련 보유자료를 함께 확인합니다. 조사자료가 없으면 미보유 상태를 먼저 알립니다.</p></li><li><strong>증설·변경 — 이전 조건과의 차이</strong><p>변경 전후의 배치도와 사양을 나란히 정리합니다. 기존 검토 결과의 적용 범위에 변경 사항이 포함되는지 확인합니다.</p></li></ol></div></section>
<section class="section"><div class="resource-band"><div><p class="eyebrow">PREPARATION WORKSPACE</p><h3>가지고 있는 자료부터 체크하세요.</h3><p>확인 필요 항목과 미준비 항목을 정리해 내려받을 수 있습니다. 입력은 현재 화면에서만 사용하며 서버로 전송하지 않습니다.</p></div><div class="button-row"><a class="button" href="preparation.html">준비자료 도구 열기 ↗</a></div></div></section>
<section class="section" id="published-records"><p class="section-number">03 / PUBLISHED RECORDS</p><div class="section-header"><h2>공개된 도면에서는<br>이런 내용을 살펴보세요.</h2><p>두자 공식 홈페이지의 공개 수행자료로 연결됩니다. 여기서는 자료의 구성만 소개하며 개별 현장의 계산 결과를 일반화하지 않습니다.</p></div><div class="related"><article><p class="eyebrow">경주 삼지2호 / 측면 구성</p><h3><a href="https://dooja.co.kr/projects/samji2-solar">모듈·지지부재·기초의 위치 관계 ↗</a></h3><p>측면도에서 모듈 배치와 지지부재, 지표선과 기초의 위치 관계를 살펴볼 수 있습니다. 내 현장에서는 어떤 자료가 빠져 있는지 정리하는 참고로 활용하세요.</p></article><article><p class="eyebrow">평택 삼계리 / 구조 모델</p><h3><a href="https://dooja.co.kr/projects/samgye-solar">입체 모델과 평면 구성 읽기 ↗</a></h3><p>공개 계산서의 입체·평면 모델에서 골조와 연결부재의 구성을 확인할 수 있습니다. 모델과 실제 배치가 같은 대상을 설명하는지가 확인의 출발점입니다.</p></article></div></section>
<section class="section" id="questions"><p class="section-number">04 / COMMON QUESTIONS</p><h2>준비할 때 자주 묻는 질문</h2><details><summary>도면이 없으면 무엇부터 정리하나요?</summary><p>설치 위치, 설비 사양, 안전하게 촬영할 수 있는 현장사진과 보수 이력을 먼저 정리하고 도면 미보유 사실을 알리세요. 기존 자료 확보, 현장조사 또는 도면 작성이 어느 정도 필요한지는 담당자와 범위를 정합니다.</p></details><details><summary>태양광 검토와 태양광 구조검토는 같은 업무인가요?</summary><p>태양광 검토라는 말은 설치 조건, 발전량, 전기 연결, 공사 범위 등을 함께 뜻할 수 있습니다. 구조검토는 구조 안전과 관련된 대상을 다룹니다. 의뢰할 때 어떤 검토와 결과물이 필요한지 구체적으로 구분하세요.</p></details><details><summary>모든 자료를 체크하면 설치 가능한가요?</summary><p>체크 도구는 보유 자료 목록을 정리할 뿐 안전 여부를 판단하지 않습니다. 자료의 적정성, 실제 현장과의 일치 여부, 설계 기준과 검토 결과는 별도로 확인해야 합니다.</p></details><details><summary>두자건설에 어떤 범위로 상담할 수 있나요?</summary><p>두자(DOOJA)의 <a href="https://dooja.co.kr/services/solar-structural-review">태양광 구조검토 업무 안내</a>에서 준비자료와 진행 순서를 확인할 수 있습니다. 구체적인 대상, 결과물과 일정은 보유 자료를 기준으로 협의합니다.</p></details></section>
<section class="section" id="sources"><p class="section-number">05 / REFERENCES</p><div class="split"><div><h2>공식 자료와 함께<br>확인하세요.</h2><p>적용 기준은 검토 대상과 시점에 따라 확인해야 합니다. 이 자료실의 요약이나 해외 자료가 국내 설계기준을 대신하지 않습니다.</p></div><ol class="source-list"><li><a href="'''+KCSC+'''">국가건설기준센터 · 건축구조기준</a><small>국내 설계기준과 개정 이력의 공식 확인 경로입니다. 적용 기준과 판본은 검토 담당자에게 확인하세요.</small></li><li><a href="'''+DOE+'''">미국 에너지부 · 태양광 설비 설치 및 시운전 안내</a><small>지붕형·지상형·주차장형의 구조·접합·현장 조건을 다루는 해외 참고자료입니다. 국내 하중 수치나 허가 요건으로 적용하지 않습니다.</small></li></ol></div></section></div></main>'''
page('index.html','태양광 구조검토 자료실 | 준비자료·구조계산서 안내 · 두자 DOOJA','태양광 구조검토를 위한 지붕형·지상형·주차장형 준비자료 체크 도구와 구조계산서 확인 질문을 제공합니다. 두자(DOOJA)가 운영하는 공개 기술자료실입니다.',home)

def material_group(group,title):
    attrs='' if group=='common' else ' data-system="'+group+'"'+(' hidden' if group!='roof' else '')
    s='<fieldset class="material-group"'+attrs+'><legend>'+title+'</legend>'
    for item in MATERIALS:
        if item['group']!=group:continue
        i=item['id'];disabled=' disabled' if group not in ['common','roof'] else ''
        s+='<div class="material-row"><div><label for="'+i+'">'+item['title']+'</label><small id="'+i+'-help">'+item['help']+'</small></div><select id="'+i+'" data-material="'+i+'" aria-describedby="'+i+'-help"'+disabled+'><option value="pending">미준비</option><option value="ready">준비됨</option><option value="confirm">확인 필요</option></select></div>'
    return s+'</fieldset>'

prep='''<main id="main"><div class="wrap"><div class="page-intro"><p class="breadcrumb"><a href="./">자료실</a> / 준비자료 정리</p><p class="eyebrow">PREPARATION / INTERACTIVE WORKSHEET</p><h1>태양광 구조검토<br>준비자료 정리 도구</h1><p class="lead">가지고 있는 자료를 표시하고, 확인이 필요한 부분을 정리하세요.<br>설치 형식에 맞춘 목록과 상담 질문을 한 파일로 내려받을 수 있습니다.</p><p class="note">입력 내용은 현재 화면에서만 사용합니다. 저장·전송되지 않으며 새로고침하면 초기화됩니다. 현장 이름 대신 알아볼 수 있는 별칭을 사용해도 됩니다.</p></div><noscript><p>체크 도구는 JavaScript가 필요합니다. <a href="downloads/solar-structural-review-request.txt" download>빈 준비 양식 내려받기</a>를 이용하거나 아래 목록을 참고하세요.</p></noscript><div class="planner-layout"><div><form id="preparation-form"><div class="settings"><label class="field" for="system-type">설치 형식<select id="system-type"><option value="roof">지붕형</option><option value="ground">지상형</option><option value="carport">주차장형</option></select></label><label class="field" for="site-label">현장 별칭 <span class="small">선택 입력</span><input id="site-label" maxlength="80" autocomplete="off" placeholder="예: A동 옥상 설치 계획"></label></div>'''+material_group('common','01 / 공통 자료')+material_group('roof','02 / 지붕형 추가 자료')+material_group('ground','02 / 지상형 추가 자료')+material_group('carport','02 / 주차장형 추가 자료')+'''</form><div class="callout"><p>자료를 모두 준비해도 안전성이나 설치 가능 여부가 확인되는 것은 아닙니다. 실제 필요한 자료와 조사 범위는 현장 조건에 따라 달라집니다.</p></div><section class="section prose"><h2>준비 상태를 이렇게 표시하세요.</h2><ul><li><strong>준비됨:</strong> 검토 담당자에게 제공할 수 있는 자료를 가지고 있습니다.</li><li><strong>확인 필요:</strong> 자료는 있지만 최신 도면인지, 대상 구역과 맞는지 등의 확인이 필요합니다.</li><li><strong>미준비:</strong> 자료가 없거나 아직 확보하지 못했습니다. 존재하지 않는 정보를 추정해서 채우지 마세요.</li></ul><p>설치 형식을 바꾸면 해당 형식의 항목만 파일에 포함됩니다. 다른 형식에서 체크한 내용은 화면을 닫거나 초기화하기 전까지 유지됩니다.</p></section><p class="no-print"><a href="report-reading.html">다음 단계: 구조계산서를 받으면 무엇을 확인하나요? ↗</a></p></div><aside class="summary-box" aria-label="준비자료 요약"><h2>보유 자료 요약</h2><div aria-live="polite" aria-atomic="true"><div class="summary-count"><b id="ready-count">0</b> <span>/ <b id="total-count">10</b>개 항목</span></div><p id="summary-status">확인 필요 0개 · 미준비 10개</p></div><p class="small">안전 점수가 아닌 자료 보유 현황입니다.</p><hr class="summary-rule"><button class="button" type="button" id="download-report">정리 파일 내려받기 ↓</button><button class="button secondary" type="button" id="print-report">인쇄 · PDF로 저장</button><button class="button secondary" type="button" id="reset-form">입력 초기화</button><p id="download-status" class="feedback" role="status"></p><hr class="summary-rule"><h3>다음에 확인할 자료</h3><ul id="missing-list"><li>준비 상태를 표시하면 목록이 갱신됩니다.</li></ul><hr class="summary-rule"><a href="https://dooja.co.kr/services/solar-structural-review">두자건설 업무범위 확인 ↗</a></aside></div></div></main>'''
page('preparation.html','태양광 구조검토 준비자료 체크 도구 | 두자 기술자료실','지붕형·지상형·주차장형 태양광 구조검토 준비자료를 정리하세요. 보유 도면과 사양, 현장사진의 준비 상태를 체크하고 미준비 항목과 상담 질문을 TXT로 내려받습니다.',prep,True)

report='''<main id="main"><div class="wrap"><div class="page-intro"><p class="breadcrumb"><a href="./">자료실</a> / 계산서 읽기</p><p class="eyebrow">READING A STRUCTURAL REPORT</p><h1>태양광 구조계산서,<br>어떤 순서로 읽어야 할까요?</h1><p class="lead">결론과 함께 검토 대상, 도면 버전, 입력 조건과 적용 범위를 확인하세요.<br>아래 질문을 실제 계산서와 도면 옆에 두고 담당자에게 확인하면 도움이 됩니다.</p></div><article class="reading-body prose"><section><h2>1. 같은 현장을 설명하는 자료인지 확인합니다.</h2><p>현장명만 같다고 모든 도면이 같은 설계를 나타내는 것은 아닙니다. 설치 구역, 모듈 배치, 지지대 형식, 도면 개정번호와 작성 날짜를 함께 비교하세요. 계산서 작성 이후 배치가 바뀌었다면 변경 내용이 반영되었는지 확인해야 합니다.</p><div class="callout"><p><strong>첫 질문:</strong> “이 계산서는 어느 날짜의 어떤 배치도와 구조 상세를 기준으로 작성되었나요?”</p></div></section><section><h2>2. 검토에 포함된 대상을 구분합니다.</h2><p>상부 지지구조, 볼트·클램프·앵커 같은 접합부, 기존 건물, 기초와 지반의 검토 범위를 구분하세요. 한 부분의 검토 결과만으로 연결된 모든 부분이 확인되었다고 해석하지 않는 것이 중요합니다.</p><div class="table-wrap"><table><caption>구조계산서와 도면을 함께 확인할 때의 질문</caption><thead><tr><th scope="col">확인 대상</th><th scope="col">같이 볼 자료</th><th scope="col">담당자에게 물어볼 내용</th></tr></thead><tbody><tr><th scope="row">설비·지지구조</th><td>모듈 사양, 부재 목록, 배치도</td><td>계산에 사용한 규격·중량·간격이 현재 계획과 같은가요?</td></tr><tr><th scope="row">접합부</th><td>연결 상세, 체결 부품 사양</td><td>검토에 포함한 연결 위치와 부품은 무엇인가요?</td></tr><tr><th scope="row">기존 건물</th><td>구조도면, 현장 확인 자료</td><td>기존 건물 검토의 범위와 확인하지 못한 조건은 무엇인가요?</td></tr><tr><th scope="row">기초·지반</th><td>기초도, 보유 지반자료</td><td>계산에 사용한 근거자료와 적용 조건은 무엇인가요?</td></tr></tbody></table></div></section><section><h2>3. 입력 조건과 실제 계획을 대조합니다.</h2><p>자중, 바람, 눈 등 고려한 하중과 조합은 적용 기준과 현장 조건을 바탕으로 결정합니다. 이 자료실에서는 모든 현장에 공통으로 넣는 하중 숫자를 제시하지 않습니다. 계산서의 기준명·판본, 설치 위치와 형상, 재료·부재·접합 조건이 무엇인지 담당자에게 설명을 요청하세요.</p><ul><li>계산에 사용한 모듈·지지대·추가 설비의 사양은 무엇인가요?</li><li>실제와 다르거나 아직 확인되지 않은 조건을 어떻게 처리했나요?</li><li>현장 확인 또는 추가 자료가 필요한 부분이 남아 있나요?</li></ul></section><section><h2>4. 결과에 붙은 조건과 제외 범위를 읽습니다.</h2><p>결과표의 문구뿐 아니라 주석, 검토 범위, 보완사항과 도면의 일치 여부를 함께 봅니다. 특정 상세를 적용하거나 추가 자료를 확인하는 조건이 있다면 담당자에게 이행 방법과 확인 자료를 요청하세요. 결과의 의미가 불명확하면 문구를 임의로 확대 해석하지 마세요.</p><p>구조계산서와 구조안전확인서 등의 제출자료는 목적과 형식이 다를 수 있습니다. 어떤 문서를 누가 작성·확인해야 하는지, 제출처가 요구하는 서류가 무엇인지는 의뢰 전에 별도로 확인합니다.</p></section><section><h2>5. 설계가 바뀌면 기준 자료를 다시 맞춥니다.</h2><p>모듈 제품, 설치 높이, 지지대 간격, 연결 부품이나 기초 계획이 변경되면 변경 전후 자료를 구분해 전달하세요. 변경 내용을 어느 검토와 도면에 반영해야 하는지 담당자에게 확인하고, 최종본의 파일명·개정번호·날짜를 남깁니다.</p><div class="callout"><p><strong>자료 정리 예시:</strong> “A동_배치도_R02_날짜.pdf”와 “A동_배치도_R03_날짜.pdf”를 구분하고, 변경 위치와 내용을 짧게 적습니다. 이는 정리 방식의 예시이며 실제 수행사례가 아닙니다.</p></div></section><section><div class="resource-band"><div><h3>질문을 적어서 확인하세요.</h3><p>검토 범위, 도면 버전, 입력 조건과 결과물에 대한 질문지를 내려받을 수 있습니다.</p></div><div class="button-row"><a class="button" href="downloads/report-questions.txt" download>결과 확인 질문지 ↓</a></div></div></section><section><h2>관련 안내와 참고자료</h2><ul class="source-list"><li><a href="preparation.html">태양광 구조검토 준비자료 체크 도구</a><small>가지고 있는 도면·사양·현장 자료를 먼저 정리할 때 사용하세요.</small></li><li><a href="https://dooja.co.kr/services/solar-structural-review">두자건설 태양광 구조검토 업무범위</a><small>현장별 의뢰 범위, 진행 과정과 결과물은 상담에서 확인합니다.</small></li><li><a href="'''+KCSC+'''">국가건설기준센터 · 건축구조기준</a><small>국내 설계기준 확인 경로입니다. 구체적인 적용과 판본은 담당 전문가가 확인합니다.</small></li><li><a href="'''+DOE+'''">미국 에너지부 · 태양광 설치 단계 참고자료</a><small>구조, 지지대, 접합부와 설치 형식별 고려사항을 다루는 해외 참고자료입니다. 국내 기준을 대신하지 않습니다.</small></li></ul><p class="note">이 안내는 계산서를 이해하기 위한 일반적인 질문을 제공합니다. 개별 구조계산의 적정성 심사나 안전성 판정을 대신하지 않습니다.</p></section></article></div></main>'''
page('report-reading.html','태양광 구조계산서 읽는 법과 확인 질문 | 두자 기술자료실','태양광 구조계산서의 검토 대상, 도면 버전, 입력 조건, 접합부와 결과의 적용 범위를 확인하는 순서를 정리했습니다. 결과 확인 질문지도 내려받을 수 있습니다.',report)

questions='''태양광 구조검토 결과 확인 질문지
운영: 두자(DOOJA) / 작성 기준: 2026-10-25

현장 구분:
확인 일자:
담당자:
계산서 파일명 / 작성일:
기준 도면명 / 개정번호 / 날짜:

1. 검토 대상
- 어느 설치 구역을 대상으로 했나요?
- 상부 구조, 접합부, 기존 건물, 기초 중 포함한 범위는 무엇인가요?
- 포함하지 않은 대상과 별도 확인 사항은 무엇인가요?
답변 / 관련 페이지:

2. 입력 조건
- 적용 기준과 판본은 무엇인가요?
- 모듈, 지지대, 부속 설비의 사양과 배치는 어느 자료를 기준으로 했나요?
- 실제 상태와 다르거나 확인이 필요한 가정은 무엇인가요?
답변 / 관련 페이지:

3. 결과와 적용 범위
- 결과에 붙은 조건이나 보완사항이 있나요?
- 최종 도면에 반영하거나 현장에서 확인할 사항은 무엇인가요?
- 제출 목적에 맞는 문서의 종류와 확인 주체는 누구인가요?
답변 / 관련 페이지:

4. 설계 변경
- 변경된 배치, 높이, 간격, 부품 또는 기초 상세가 있나요?
- 변경 전후 자료를 어떤 방식으로 전달하면 되나요?
- 재확인한 결과와 최종 도면의 버전을 어떻게 식별하나요?
답변 / 관련 페이지:

이 양식은 질문과 회신을 정리하기 위한 빈 자료입니다.
개별 현장의 구조안전 판단이나 구조계산 검증을 대신하지 않습니다.
자료실: https://solar.dooja.co.kr/
두자 업무안내: https://dooja.co.kr/services/solar-structural-review
'''
(ROOT/'downloads/report-questions.txt').write_text(questions,encoding='utf-8-sig')

ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
urlset=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
for p in PAGES.values():
    node=ET.SubElement(urlset,'url');ET.SubElement(node,'loc').text=p['url'];ET.SubElement(node,'lastmod').text=DATE
ET.ElementTree(urlset).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
for k,v in [('title','두자 태양광 구조검토 자료실'),('link',BASE),('description','구조검토 준비자료 정리와 구조계산서 이해를 돕는 공개 기술자료'),('language','ko-KR'),('lastBuildDate','Sun, 25 Oct 2026 00:00:00 +0900')]:ET.SubElement(channel,k).text=v
for p in PAGES.values():
    item=ET.SubElement(channel,'item')
    for k,v in [('title',p['title']),('link',p['url']),('description',p['description']),('pubDate','Sun, 25 Oct 2026 00:00:00 +0900')]:ET.SubElement(item,k).text=v
    ET.SubElement(item,'guid',isPermaLink='true').text=p['url']
ET.ElementTree(rss).write(ROOT/'feed.xml',encoding='utf-8',xml_declaration=True)
print('Built '+str(len(PAGES))+' pages, sitemap, RSS and question worksheet.')
