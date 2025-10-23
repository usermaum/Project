# 🏗️ Lotto AI WebApp Architecture

## 프로젝트 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                        Lotto AI WebApp                         │
│                    (Streamlit + Linear Design)                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Linear Design │  │   Chart.js      │  │   Streamlit     │  │
│  │   Components    │  │   Components    │  │   UI Framework  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   AI Models     │  │   Data          │  │   User          │  │
│  │   Management    │  │   Processing    │  │   Management    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Performance   │  │   A/B Testing   │  │   Feedback      │  │
│  │   Monitoring    │  │   System        │  │   System        │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   SQLite        │  │   Model         │  │   Log Files     │  │
│  │   Database      │  │   Weights       │  │   & Analytics   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 컴포넌트 계층 구조

### 1. UI Layer (사용자 인터페이스)
```
components/
├── linear_design/           # Linear Design System
│   ├── container.py         # 최상위 컨테이너
│   ├── section.py          # 섹션 헤더
│   ├── panel.py            # 패널 컨테이너
│   ├── button.py           # 버튼 컴포넌트
│   ├── grid.py             # 그리드 레이아웃
│   ├── spacer.py           # 간격 조정
│   ├── divider.py          # 구분선
│   ├── card.py             # 카드 컴포넌트
│   ├── badge.py            # 배지 컴포넌트
│   └── alert.py            # 알림 컴포넌트
└── chart_js.py             # Chart.js 래퍼
```

### 2. AI Models Layer (AI 모델)
```
modules/lotto/models/
├── lstm_predictor.py        # LSTM 신경망
├── transformer_predictor.py # Transformer 모델
├── prophet_predictor.py     # Prophet 시계열
└── ensemble_predictor.py    # 앙상블 모델
```

### 3. Management Layer (관리 시스템)
```
modules/lotto/
├── model_manager.py         # 모델 통합 관리
├── performance_monitor.py   # 성능 모니터링
├── hyperparameter_tuner.py  # 하이퍼파라미터 튜닝
├── realtime_learner.py      # 실시간 학습
├── ab_testing.py            # A/B 테스트
└── user_feedback.py         # 사용자 피드백
```

### 4. Settings Layer (설정 및 인증)
```
modules/settings/
├── auth.py                  # 사용자 인증
├── database.py              # 데이터베이스 모델
└── admin.py                 # 관리자 기능
```

## 데이터 흐름

### 1. 사용자 요청 흐름
```
사용자 요청 → Streamlit UI → Linear Design Components → Business Logic → Database
     ↑                                                                      ↓
     └─────────────── 응답 ← Chart.js Components ← AI Models ←─────────────┘
```

### 2. AI 예측 흐름
```
데이터 로드 → 전처리 → 모델 선택 → 예측 실행 → 결과 후처리 → UI 표시
     ↑              ↓
     └── 성능 모니터링 ← 예측 결과 저장
```

### 3. 사용자 피드백 흐름
```
사용자 피드백 → 피드백 시스템 → 데이터베이스 저장 → 분석 → 인사이트 생성
```

## 컴포넌트 간 의존성

### 1. UI 컴포넌트 의존성
```
Linear Design Components
    ↓
Streamlit Framework
    ↓
Python Runtime
```

### 2. AI 모델 의존성
```
AI Models (LSTM, Transformer, Prophet)
    ↓
ModelManager
    ↓
PerformanceMonitor
    ↓
Database
```

### 3. 데이터 의존성
```
SQLite Database
    ↓
Data Processing
    ↓
AI Models
    ↓
Predictions
    ↓
UI Display
```

## 주요 패턴

### 1. 컴포넌트 사용 패턴
```python
# 기본 레이아웃 패턴
with Container.render(max_width="1400px", padding="xl"):
    with Section.render("제목", "설명"):
        with Panel.render("패널", padding="xl", elevation="dialog"):
            # 내용
```

### 2. AI 모델 사용 패턴
```python
# 모델 예측 패턴
try:
    manager = ModelManager(db_path="app/data/lotto.db")
    if not manager.load_model_from_db('LSTM'):
        manager.train_lstm()
    predicted = manager.predict_lstm(top_k=6)
except Exception as e:
    st.error(f"예측 실패: {e}")
```

### 3. 에러 처리 패턴
```python
# 통일된 에러 처리
try:
    # 실행할 코드
    st.success("성공 메시지")
    logger.info("로그 메시지")
except Exception as e:
    st.error(f"에러 메시지: {e}")
    logger.error(f"에러 로그: {e}")
```

## 확장성 고려사항

### 1. 새로운 AI 모델 추가
- `modules/lotto/models/` 디렉토리에 새 모델 클래스 추가
- `ModelManager`에 새 모델 메서드 추가
- UI에 새 모델 버튼 추가

### 2. 새로운 UI 컴포넌트 추가
- `components/linear_design/` 디렉토리에 새 컴포넌트 추가
- `__init__.py`에 export 추가
- VS Code 스니펫에 새 컴포넌트 추가

### 3. 새로운 기능 추가
- `modules/lotto/` 디렉토리에 새 기능 모듈 추가
- 메인 앱에 새 페이지 추가
- 관리자 기능에 새 메뉴 추가

## 성능 최적화

### 1. 캐싱 전략
```python
@st.cache_resource
def load_model_manager():
    return ModelManager(DB_PATH)

@st.cache_data
def load_lotto_data():
    return processor.load_data()
```

### 2. 비동기 처리
- 실시간 학습은 백그라운드 스레드에서 실행
- 모델 학습은 별도 프로세스에서 실행
- 사용자 인터페이스는 블로킹되지 않음

### 3. 데이터베이스 최적화
- 인덱스 추가로 쿼리 성능 향상
- 연결 풀링으로 연결 오버헤드 감소
- 정기적인 데이터 정리

## 보안 고려사항

### 1. 사용자 인증
- 모든 보호된 페이지에 인증 확인
- 세션 기반 인증 시스템
- 관리자 권한 분리

### 2. 데이터 보호
- 사용자 입력 검증
- SQL 인젝션 방지
- 민감한 정보 암호화

### 3. 에러 처리
- 상세한 에러 정보 노출 방지
- 로그에 민감한 정보 포함하지 않음
- 사용자에게는 친화적인 에러 메시지

## 모니터링 및 로깅

### 1. 로깅 전략
```python
import logging
logger = logging.getLogger(__name__)

# 중요한 작업에 로깅
logger.info("모델 학습 시작")
logger.error(f"예측 실패: {e}")
```

### 2. 성능 모니터링
- 모델 예측 정확도 추적
- 사용자 피드백 분석
- 시스템 리소스 사용량 모니터링

### 3. 알림 시스템
- 에러 발생 시 알림
- 성능 저하 감지 시 알림
- 사용자 피드백 급증 시 알림

이 아키텍처는 확장 가능하고 유지보수가 용이하도록 설계되었습니다.
