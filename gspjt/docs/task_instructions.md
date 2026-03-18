# 작업 지시서: 금·은 자산 경제위기 대응력 및 성과 분석 대시보드

## 1. 프로젝트 개요
- **목적**: 지난 10년간의 주요 경제위기 국면에서 금(Gold)과 은(Silver)의 안전자산 가치 검증 및 투자 성과 분석.
- **대상 자산**: 금(GC=F), 은(SI=F), S&P 500(^GSPC).

## 2. 작업 단계별 상세 계획

### 단계 1: 프로젝트 환경 및 폴더 구성
- 워크스페이스 루트 내 `gspjt` 폴더 및 하위 폴더(`src`, `data`, `images`, `docs`) 생성.
- 필요한 패키지 설치: `yfinance`, `pandas`, `plotly`, `streamlit`, `koreanize-matplotlib`.

### 단계 2: 데이터 수집 및 DB 저장 (`src/collect.py`)
- **수집 기간**: 2015-01-01 ~ 현재.
- **수집 항목**: 종가(Close), 수정종가(Adj Close).
- **데이터베이스**: `data/commodity_analysis.db` 생성 및 `raw_prices` 테이블에 전체 원본 데이터 저장.

### 단계 3: 데이터 분석 및 지표 산출 (`src/analyze.py`)
- **수익률 계산**: 일일 수익률 및 누적 수익률.
- **안정성 지표**: 위기 기간별 최대 낙폭(MDD).
- **효율성 지표**: 샤프 지수(위험 대비 수익률).
- **상관관계**: S&P 500과 금/은의 상관계수 산출.
- **위기 코호트 정의**:
    - Brexit (2016-06-01 ~ 2016-08-31)
    - Tariff War (2018-03-01 ~ 2019-12-31)
    - Iran-US Conflict (2020-01-01 ~ 2020-02-29)
    - COVID-19 (2020-03-01 ~ 2020-12-31)
    - Russia-Ukraine War (2022-02-01 ~ 2022-06-30)
- **DB 저장**: 최종 성과 지표를 `crisis_performance` 테이블에 저장.

### 단계 4: Streamlit 대시보드 구현 (`src/app.py`)
- **Chart 1 (Timeline)**: 금/은 가격 추이 및 위기 영역 시각화.
- **Chart 2 (Defense)**: 위기 시 S&P 500 대비 방어력 비교 바 차트.
- **Chart 3 (Ratio)**: 금-은 비율(Gold-Silver Ratio) 및 역사적 평균선.
- **Chart 4 (Efficiency)**: 투자 기간별 샤프 지수 비교.

### 단계 5: 결과 보고서 작성 (`docs/analysis_report.md`)
- 분석 결과 요약 및 위기 국면에서의 투자 전략 제언.

## 3. 성공 기준 (Success Criteria)
- [x] 데이터 수집 및 DB 저장 완료.
- [x] 5대 위기 국면별 지표 산출 완료.
- [x] Plotly를 활용한 인터랙티브 대시보드가 정상 동작.
- [x] 위기 시 자산 배분 전략에 대한 결론 도출.
