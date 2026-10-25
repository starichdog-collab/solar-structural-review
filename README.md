# 태양광 구조검토 자료실 · 두자 DOOJA

두자(DOOJA)가 운영하는 공개 기술자료와 브라우저에서 실행되는 준비자료 도구입니다.

- 자료실: https://solar.dooja.co.kr/
- 공식 홈페이지: https://dooja.co.kr/
- 업무 안내: https://dooja.co.kr/services/solar-structural-review

## 제공 내용

| 페이지 | 용도 |
| --- | --- |
| index.html | 자료실 홈, 검토 범위와 공개 참고자료 안내 |
| preparation.html | 지붕형·지상형·주차장형 준비자료 체크, TXT 다운로드 및 인쇄 |
| report-reading.html | 구조계산서 대상·도면·입력 조건·적용 범위를 확인하는 질문 |
| downloads/report-questions.txt | 결과 확인 질문지 |

이 자료실은 개별 현장의 하중 계산, 안전성 판정 또는 허가·계약 업무를 수행하지 않습니다. 자료 보유 개수는 안전 점수가 아닙니다. 관련 업무 범위와 상담은 두자 공식 홈페이지에서 안내합니다.

## 데이터 처리

도구의 입력 내용은 현재 화면에서만 사용하며 서버로 전송하거나 브라우저 저장소에 저장하지 않습니다. 새로고침하면 초기화됩니다. 내려받은 TXT/PDF 파일은 사용자가 보관합니다. GitHub Pages 호스팅 서비스의 일반적인 요청 처리는 별개입니다.

## 유지보수

외부 패키지가 필요하지 않습니다. GitHub Pages의 main 브랜치 루트에서 배포합니다.

- 생성: python3 scripts/build.py
- 검증: node --test tests/planner.test.cjs
- 항목과 동작: assets/planner.js
- 문서 내용: scripts/build.py
- 스타일: assets/site.css
- 내용을 실제로 수정한 날짜만 빌더와 본문·RSS에 반영합니다.
- 각 문서의 canonical은 자료실의 고유 주소입니다. 회사 홈페이지와 문서를 복제하지 않습니다.
- sitemap.xml은 독립 자료실의 문서 3개만 포함합니다.
- 맞춤 도메인 연결 후 이 저장소 루트의 robots.txt를 사용합니다.
- 검색 노출, 순위, 외부 인용은 보장하지 않습니다.

## 기존 주소 보존

2026-10-25에 첫 화면을 독립 준비자료실로 변경했습니다. 기존에 회사 도메인으로 이전한 다음 문서의 이동 동작은 보존합니다.

- roof-solar-review.html
- wind-load.html
- snow-load.html
- structural-calculation-report.html

기존 downloads/solar-structural-review-request.txt도 유지합니다. 회사 홈페이지의 소스·도메인·배포 설정은 이 저장소에서 수정하지 않습니다.

## 참고자료

- [국가건설기준센터](https://www.kcsc.re.kr/standardCode/list/102041): 국내 설계기준 공식 확인 경로
- [미국 에너지부 PV 설치 및 시운전 안내](https://www.energy.gov/cmei/femp/life-cycle-photovoltaic-systems-install-and-commission-photovoltaic-system): 해외 참고자료이며 국내 기준을 대신하지 않음

공개 수행자료는 두자 홈페이지의 해당 프로젝트로 연결합니다. 확인되지 않은 실적·결과·자격·고객 평가는 추가하지 않습니다.


## 맞춤 도메인 전환 준비

이 브랜치는 solar.dooja.co.kr 연결용 변경본입니다. 아직 실제 도메인 연결이 완료되었다는 의미가 아닙니다. GitHub Settings → Pages의 Custom domain을 설정하고, DNS와 HTTPS를 확인한 뒤 main에 반영합니다. CNAME 파일만 추가해도 도메인 설정이 자동으로 완료되지는 않습니다.

DNS: CNAME / host solar / target starichdog-collab.github.io.
기존 dooja.co.kr의 A·MX·TXT 레코드는 변경하지 않습니다.
