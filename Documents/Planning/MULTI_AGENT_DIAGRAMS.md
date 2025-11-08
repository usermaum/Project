# 멀티 에이전트 시스템 다이어그램 모음

> **작성일**: 2025-11-08
> **버전**: v1.0.0
> **목적**: 멀티 에이전트 시스템의 시각화

---

## 📋 목차

1. [전체 시스템 아키텍처](#1-전체-시스템-아키텍처)
2. [에이전트 역할 및 책임](#2-에이전트-역할-및-책임)
3. [작업 흐름 (워크플로우)](#3-작업-흐름-워크플로우)
4. [데이터 흐름](#4-데이터-흐름)
5. [의존성 그래프](#5-의존성-그래프)
6. [시퀀스 다이어그램 (상세 예시)](#6-시퀀스-다이어그램-상세-예시)
7. [파일 시스템 구조](#7-파일-시스템-구조)
8. [상태 머신](#8-상태-머신)

---

## 1. 전체 시스템 아키텍처

### 1.1 레이어드 아키텍처

```mermaid
graph TB
    subgraph "사용자 인터페이스 레이어"
        User[👤 사용자]
        CLI[💻 Claude Code CLI]
    end

    subgraph "오케스트레이션 레이어"
        Orchestrator[🎭 총괄 디렉터<br/>Orchestrator Agent]
        PA[📊 Project Analyzer]
        TO[🎯 Task Orchestrator]
        RI[🔗 Result Integrator]
    end

    subgraph "전문 에이전트 레이어"
        DB[🗄️ DB Architect]
        BE[💻 Backend Developer]
        FE[🎨 Frontend Developer]
        UI[🎨 UI/UX Designer]
    end

    subgraph "스킬 레이어"
        Skills1[schema-designer<br/>orm-builder<br/>migration-builder]
        Skills2[api-builder<br/>service-builder<br/>auth-builder]
        Skills3[component-builder<br/>state-manager<br/>api-integrator]
        Skills4[design-system-builder<br/>component-designer<br/>wireframe-builder]
    end

    subgraph "데이터 레이어"
        Context[📁 Agent Context<br/>project.json<br/>tasks.json]
        Templates[📄 Templates<br/>framework-specific]
        Config[⚙️ Config<br/>agents.yaml<br/>frameworks.yaml]
    end

    User --> CLI
    CLI --> Orchestrator

    Orchestrator --> PA
    Orchestrator --> TO
    Orchestrator --> RI

    TO --> DB
    TO --> BE
    TO --> FE
    TO --> UI

    DB --> Skills1
    BE --> Skills2
    FE --> Skills3
    UI --> Skills4

    PA -.-> Context
    TO -.-> Context
    RI -.-> Context

    Skills1 -.-> Templates
    Skills2 -.-> Templates
    Skills3 -.-> Templates
    Skills4 -.-> Templates

    PA -.-> Config
    TO -.-> Config

    style Orchestrator fill:#4A90E2,color:#fff
    style DB fill:#9B59B6,color:#fff
    style BE fill:#50C878,color:#fff
    style FE fill:#FF6B6B,color:#fff
    style UI fill:#F39C12,color:#fff
```

---

## 2. 에이전트 역할 및 책임

### 2.1 에이전트 책임 매트릭스

```mermaid
graph LR
    subgraph "🎭 총괄 디렉터"
        O1[프로젝트 분석]
        O2[작업 분배]
        O3[결과 통합]
        O4[사용자 소통]
    end

    subgraph "🗄️ DB Architect"
        D1[스키마 설계]
        D2[ERD 작성]
        D3[ORM 모델]
        D4[마이그레이션]
    end

    subgraph "💻 Backend Developer"
        B1[API 개발]
        B2[비즈니스 로직]
        B3[인증/인가]
        B4[백엔드 테스트]
    end

    subgraph "🎨 Frontend Developer"
        F1[컴포넌트 개발]
        F2[상태 관리]
        F3[API 연동]
        F4[프론트 테스트]
    end

    subgraph "🎨 UI/UX Designer"
        U1[디자인 시스템]
        U2[컴포넌트 디자인]
        U3[와이어프레임]
        U4[접근성 검증]
    end

    style O1 fill:#4A90E2,color:#fff
    style O2 fill:#4A90E2,color:#fff
    style O3 fill:#4A90E2,color:#fff
    style O4 fill:#4A90E2,color:#fff

    style D1 fill:#9B59B6,color:#fff
    style D2 fill:#9B59B6,color:#fff
    style D3 fill:#9B59B6,color:#fff
    style D4 fill:#9B59B6,color:#fff

    style B1 fill:#50C878,color:#fff
    style B2 fill:#50C878,color:#fff
    style B3 fill:#50C878,color:#fff
    style B4 fill:#50C878,color:#fff

    style F1 fill:#FF6B6B,color:#fff
    style F2 fill:#FF6B6B,color:#fff
    style F3 fill:#FF6B6B,color:#fff
    style F4 fill:#FF6B6B,color:#fff

    style U1 fill:#F39C12,color:#fff
    style U2 fill:#F39C12,color:#fff
    style U3 fill:#F39C12,color:#fff
    style U4 fill:#F39C12,color:#fff
```

---

## 3. 작업 흐름 (워크플로우)

### 3.1 전체 워크플로우

```mermaid
flowchart TD
    Start([👤 사용자 요청]) --> Parse[📝 요청 파싱]

    Parse --> CheckCache{프로젝트<br/>분석 캐시<br/>존재?}
    CheckCache -->|Yes| LoadCache[📂 project.json 로드]
    CheckCache -->|No| Analyze[🔍 프로젝트 분석]

    Analyze --> SaveCache[💾 project.json 저장]
    SaveCache --> LoadCache

    LoadCache --> IdentifyAgents[🎯 필요 에이전트 식별]

    IdentifyAgents --> CheckDeps{의존성<br/>있음?}

    CheckDeps -->|Yes| Sequential[📋 순차 실행 계획]
    CheckDeps -->|No| Parallel[⚡ 병렬 실행 계획]

    Sequential --> Execute[▶️ 에이전트 실행]
    Parallel --> Execute

    Execute --> Agent1[🗄️ DB Architect]
    Execute --> Agent2[💻 Backend Dev]
    Execute --> Agent3[🎨 Frontend Dev]
    Execute --> Agent4[🎨 UI/UX Designer]

    Agent1 --> Wait1{완료?}
    Agent2 --> Wait2{완료?}
    Agent3 --> Wait3{완료?}
    Agent4 --> Wait4{완료?}

    Wait1 -->|Yes| Collect[🔗 결과 수집]
    Wait2 -->|Yes| Collect
    Wait3 -->|Yes| Collect
    Wait4 -->|Yes| Collect

    Collect --> Integrate[🔄 결과 통합]

    Integrate --> CheckConflict{충돌<br/>발생?}

    CheckConflict -->|Yes| Resolve[🛠️ 충돌 해결]
    CheckConflict -->|No| Generate[📄 최종 산출물 생성]

    Resolve --> Generate

    Generate --> Test[✅ 테스트 코드 생성]
    Test --> Doc[📚 문서 업데이트]
    Doc --> Report[📊 리포트 작성]

    Report --> End([✨ 사용자에게 보고])

    style Start fill:#4A90E2,color:#fff
    style End fill:#50C878,color:#fff
    style Agent1 fill:#9B59B6,color:#fff
    style Agent2 fill:#50C878,color:#fff
    style Agent3 fill:#FF6B6B,color:#fff
    style Agent4 fill:#F39C12,color:#fff
```

---

## 4. 데이터 흐름

### 4.1 컨텍스트 데이터 흐름

```mermaid
graph TB
    subgraph "입력 데이터"
        UserReq[👤 사용자 요청<br/>자연어]
        ProjectFiles[📁 프로젝트 파일<br/>코드/설정]
    end

    subgraph "분석 단계"
        ProjectAnalyzer[📊 Project Analyzer]

        PA_Output[project.json<br/>━━━━━━━━━━<br/>tech_stack<br/>architecture<br/>dependencies]
    end

    subgraph "계획 단계"
        TaskOrchestrator[🎯 Task Orchestrator]

        TO_Output[tasks.json<br/>━━━━━━━━━━<br/>agent_list<br/>dependencies<br/>execution_order]
    end

    subgraph "실행 단계"
        DB_Agent[🗄️ DB Architect]
        BE_Agent[💻 Backend Dev]
        FE_Agent[🎨 Frontend Dev]

        DB_Context[db-context.json<br/>━━━━━━━━━━<br/>schema<br/>models<br/>migrations]

        BE_Context[backend-context.json<br/>━━━━━━━━━━<br/>api_endpoints<br/>services<br/>tests]

        FE_Context[frontend-context.json<br/>━━━━━━━━━━<br/>components<br/>routes<br/>state]
    end

    subgraph "통합 단계"
        ResultIntegrator[🔗 Result Integrator]

        Final[최종 산출물<br/>━━━━━━━━━━<br/>코드 파일<br/>테스트<br/>문서]
    end

    UserReq --> ProjectAnalyzer
    ProjectFiles --> ProjectAnalyzer

    ProjectAnalyzer --> PA_Output
    PA_Output --> TaskOrchestrator

    TaskOrchestrator --> TO_Output

    TO_Output --> DB_Agent
    TO_Output --> BE_Agent
    TO_Output --> FE_Agent

    DB_Agent --> DB_Context
    BE_Agent --> BE_Context
    FE_Agent --> FE_Context

    DB_Context --> BE_Agent
    DB_Context --> ResultIntegrator
    BE_Context --> FE_Agent
    BE_Context --> ResultIntegrator
    FE_Context --> ResultIntegrator

    ResultIntegrator --> Final

    style PA_Output fill:#E8F4F8
    style TO_Output fill:#FFF4E6
    style DB_Context fill:#F3E5F5
    style BE_Context fill:#E8F5E9
    style FE_Context fill:#FFEBEE
    style Final fill:#FFF9C4
```

---

## 5. 의존성 그래프

### 5.1 에이전트 간 의존성

```mermaid
graph TD
    User[👤 사용자 요청]

    User --> Orch[🎭 총괄 디렉터<br/>우선순위: 1]

    Orch --> DB[🗄️ DB Architect<br/>우선순위: 2<br/>의존성: 없음]

    DB --> BE[💻 Backend Developer<br/>우선순위: 3<br/>의존성: DB]
    DB --> Designer[🎨 UI/UX Designer<br/>우선순위: 3<br/>의존성: 없음]

    BE --> FE[🎨 Frontend Developer<br/>우선순위: 4<br/>의존성: Backend, Designer]
    Designer --> FE

    FE --> Review[🔍 Code Reviewer<br/>우선순위: 5<br/>의존성: 모든 개발자]
    BE --> Review
    DB --> Review

    Review --> Doc[📚 Documentation Writer<br/>우선순위: 6<br/>의존성: Code Review]

    Doc --> Git[🔀 Git Operator<br/>우선순위: 7<br/>의존성: Documentation]

    Git --> Complete[✅ 작업 완료]

    style Orch fill:#4A90E2,color:#fff
    style DB fill:#9B59B6,color:#fff
    style BE fill:#50C878,color:#fff
    style Designer fill:#F39C12,color:#fff
    style FE fill:#FF6B6B,color:#fff
    style Review fill:#78909C,color:#fff
    style Doc fill:#00897B,color:#fff
    style Git fill:#5E35B1,color:#fff
    style Complete fill:#43A047,color:#fff
```

### 5.2 병렬 vs 순차 실행

```mermaid
graph LR
    subgraph "순차 실행 (Sequential)"
        S1[Task 1<br/>DB 스키마] --> S2[Task 2<br/>Backend API]
        S2 --> S3[Task 3<br/>Frontend UI]
    end

    subgraph "병렬 실행 (Parallel)"
        P1[Task 1<br/>DB 스키마]
        P2[Task 2<br/>UI 디자인]

        P1 --> P3[Task 3<br/>Backend API]
        P2 --> P4[Task 4<br/>Frontend UI]

        P3 --> P5[통합]
        P4 --> P5
    end

    style S1 fill:#9B59B6,color:#fff
    style S2 fill:#50C878,color:#fff
    style S3 fill:#FF6B6B,color:#fff

    style P1 fill:#9B59B6,color:#fff
    style P2 fill:#F39C12,color:#fff
    style P3 fill:#50C878,color:#fff
    style P4 fill:#FF6B6B,color:#fff
    style P5 fill:#4A90E2,color:#fff
```

---

## 6. 시퀀스 다이어그램 (상세 예시)

### 6.1 전체 시스템 시퀀스

```mermaid
sequenceDiagram
    participant U as 👤 사용자
    participant O as 🎭 총괄 디렉터
    participant PA as 📊 Project Analyzer
    participant TO as 🎯 Task Orchestrator
    participant DB as 🗄️ DB Architect
    participant BE as 💻 Backend Dev
    participant FE as 🎨 Frontend Dev
    participant RI as 🔗 Result Integrator

    U->>O: "원두 입고 알림 기능 추가"

    activate O
    O->>PA: 프로젝트 분석 요청
    activate PA

    PA->>PA: package.json 읽기
    PA->>PA: 디렉토리 구조 스캔
    PA->>PA: Git 메타데이터 분석

    PA-->>O: project.json (tech_stack)
    deactivate PA

    O->>TO: 작업 분배 계획 수립
    activate TO

    TO->>TO: 키워드 분석: "원두", "입고", "알림"
    TO->>TO: 필요 에이전트: DB, Backend, Frontend
    TO->>TO: 의존성 그래프 생성

    TO-->>O: tasks.json (실행 계획)
    deactivate TO

    par DB 스키마 설계
        O->>DB: Task 1: 알림 테이블 설계
        activate DB
        DB->>DB: ERD 작성
        DB->>DB: notifications 테이블 스키마
        DB->>DB: ORM 모델 생성 (SQLAlchemy)
        DB->>DB: 마이그레이션 파일 작성
        DB-->>O: db-context.json<br/>(schema, model, migration)
        deactivate DB
    end

    par Backend API 구현
        O->>BE: Task 2: 알림 API 구현
        activate BE
        BE->>DB: 스키마 정보 요청
        DB-->>BE: notifications 스키마
        BE->>BE: GET /api/notifications 엔드포인트
        BE->>BE: POST /api/notifications 엔드포인트
        BE->>BE: NotificationService 작성
        BE->>BE: 테스트 코드 작성
        BE-->>O: backend-context.json<br/>(API, service, tests)
        deactivate BE
    and Frontend UI 구현
        O->>FE: Task 3: 알림 UI 구현
        activate FE
        FE->>BE: API 스펙 요청
        BE-->>FE: API 엔드포인트 목록
        FE->>FE: NotificationBell 컴포넌트
        FE->>FE: NotificationList 페이지
        FE->>FE: 알림 상태 관리 (Context API)
        FE->>FE: API 연동 (Axios)
        FE-->>O: frontend-context.json<br/>(components, routes)
        deactivate FE
    end

    O->>RI: 결과 통합 요청
    activate RI

    RI->>RI: 파일 경로 충돌 체크
    RI->>RI: 코드 병합
    RI->>RI: import 문 정리
    RI->>RI: 테스트 통합
    RI->>RI: 문서 업데이트

    RI-->>O: 통합 리포트 + 파일 목록
    deactivate RI

    O-->>U: 최종 보고<br/>━━━━━━━━━━<br/>✅ 7개 파일 생성<br/>✅ 테스트 커버리지 95%<br/>✅ 문서 업데이트 완료
    deactivate O
```

### 6.2 에러 처리 시퀀스

```mermaid
sequenceDiagram
    participant O as 🎭 총괄 디렉터
    participant BE as 💻 Backend Dev
    participant DB as 🗄️ DB Architect
    participant U as 👤 사용자

    O->>BE: Task: API 구현
    activate BE

    BE->>DB: 스키마 요청
    activate DB
    DB--xBE: ❌ 오류: 스키마 없음
    deactivate DB

    BE->>BE: 오류 감지
    BE-->>O: ⚠️ 작업 실패<br/>사유: DB 스키마 미완성
    deactivate BE

    activate O
    O->>O: 의존성 재검증
    O->>DB: Task 재시도: 스키마 먼저 생성

    activate DB
    DB->>DB: 스키마 생성
    DB-->>O: ✅ 스키마 완료
    deactivate DB

    O->>BE: Task 재시도: API 구현
    activate BE
    BE->>DB: 스키마 요청
    activate DB
    DB-->>BE: ✅ 스키마 전달
    deactivate DB
    BE->>BE: API 구현 완료
    BE-->>O: ✅ 작업 성공
    deactivate BE

    O-->>U: 최종 보고 (재시도 성공)
    deactivate O
```

---

## 7. 파일 시스템 구조

### 7.1 디렉토리 트리

```mermaid
graph TB
    Root[~/.claude/plugins/<br/>multi-agent-system/]

    Root --> Skills[📁 skills/]
    Root --> Templates[📁 templates/]
    Root --> Config[📁 config/]
    Root --> Utils[📁 utils/]
    Root --> Docs[📄 README.md<br/>ARCHITECTURE.md]

    Skills --> Orch[📁 orchestrator/]
    Skills --> BE[📁 backend-developer/]
    Skills --> FE[📁 frontend-developer/]
    Skills --> DB[📁 db-architect/]
    Skills --> UI[📁 ui-ux-designer/]
    Skills --> Shared[📁 shared/]

    Orch --> O1[skill.md<br/>project-analyzer.py<br/>task-orchestrator.py<br/>result-integrator.py]

    BE --> B1[skill.md<br/>api-builder.py<br/>service-builder.py<br/>📁 frameworks/]

    FE --> F1[skill.md<br/>component-builder.py<br/>state-manager.py<br/>📁 frameworks/]

    DB --> D1[skill.md<br/>schema-designer.py<br/>orm-builder.py<br/>📁 templates/]

    UI --> U1[skill.md<br/>design-system-builder.py<br/>component-designer.py<br/>design-tokens.json]

    Shared --> S1[code-reviewer.py<br/>documentation-writer.py<br/>git-operator.py]

    Templates --> T1[📁 web-app/<br/>📁 api-server/<br/>📁 fullstack/]

    Config --> C1[agents.yaml<br/>skills-mapping.yaml<br/>frameworks.yaml]

    Utils --> U2[project-detector.py<br/>framework-analyzer.py<br/>file-generator.py]

    style Root fill:#4A90E2,color:#fff
    style Skills fill:#9B59B6,color:#fff
    style Templates fill:#50C878,color:#fff
    style Config fill:#F39C12,color:#fff
    style Utils fill:#FF6B6B,color:#fff
```

### 7.2 프로젝트별 컨텍스트

```mermaid
graph TB
    Project[프로젝트 루트/<br/>.claude/agent-context/]

    Project --> P1[📄 project.json<br/>━━━━━━━━━━<br/>tech_stack<br/>architecture<br/>recommended_agents]

    Project --> P2[📄 tasks.json<br/>━━━━━━━━━━<br/>current_tasks<br/>completed_tasks<br/>failed_tasks]

    Project --> P3[📄 db-context.json<br/>━━━━━━━━━━<br/>schema<br/>models<br/>migrations]

    Project --> P4[📄 backend-context.json<br/>━━━━━━━━━━<br/>api_endpoints<br/>services<br/>tests]

    Project --> P5[📄 frontend-context.json<br/>━━━━━━━━━━<br/>components<br/>routes<br/>state]

    Project --> P6[📄 designer-context.json<br/>━━━━━━━━━━<br/>design_system<br/>components<br/>accessibility]

    style Project fill:#4A90E2,color:#fff
    style P1 fill:#E8F4F8
    style P2 fill:#FFF4E6
    style P3 fill:#F3E5F5
    style P4 fill:#E8F5E9
    style P5 fill:#FFEBEE
    style P6 fill:#FFF9C4
```

---

## 8. 상태 머신

### 8.1 작업 상태 전이

```mermaid
stateDiagram-v2
    [*] --> Pending: 작업 생성

    Pending --> Analyzing: 프로젝트 분석 시작

    Analyzing --> Planning: 분석 완료
    Analyzing --> Failed: 분석 실패

    Planning --> Executing: 계획 수립 완료
    Planning --> Failed: 계획 실패

    Executing --> WaitingDependency: 의존성 대기
    Executing --> Running: 에이전트 실행

    WaitingDependency --> Running: 의존성 해결
    WaitingDependency --> Failed: 의존성 오류

    Running --> Integrating: 실행 완료
    Running --> Failed: 실행 오류
    Running --> Retrying: 재시도 필요

    Retrying --> Running: 재시도
    Retrying --> Failed: 최대 재시도 초과

    Integrating --> Testing: 통합 완료
    Integrating --> Failed: 통합 충돌

    Testing --> Documenting: 테스트 통과
    Testing --> Failed: 테스트 실패

    Documenting --> Completed: 문서화 완료
    Documenting --> Failed: 문서화 오류

    Completed --> [*]
    Failed --> [*]

    note right of Analyzing
        project-analyzer 실행
        - 기술 스택 감지
        - 프레임워크 식별
    end note

    note right of Planning
        task-orchestrator 실행
        - 에이전트 선택
        - 의존성 그래프
        - 실행 순서 결정
    end note

    note right of Running
        전문 에이전트 실행
        - DB Architect
        - Backend Developer
        - Frontend Developer
        - UI/UX Designer
    end note

    note right of Integrating
        result-integrator 실행
        - 코드 병합
        - 충돌 해결
        - 파일 생성
    end note
```

### 8.2 에이전트 상태 전이

```mermaid
stateDiagram-v2
    [*] --> Idle: 에이전트 로드

    Idle --> Triggered: 작업 할당

    Triggered --> CheckingContext: 컨텍스트 확인

    CheckingContext --> LoadingContext: 캐시 존재
    CheckingContext --> CreatingContext: 캐시 없음

    LoadingContext --> Ready
    CreatingContext --> Ready

    Ready --> Executing: 스킬 실행

    Executing --> Writing: 코드 작성
    Executing --> Reading: 정보 읽기
    Executing --> Analyzing: 분석 수행

    Writing --> Saving: 파일 저장
    Reading --> Processing: 데이터 처리
    Analyzing --> Processing

    Saving --> SavingContext
    Processing --> SavingContext

    SavingContext --> Completed: 성공
    SavingContext --> Error: 실패

    Error --> Retrying: 재시도 가능
    Error --> Failed: 재시도 불가

    Retrying --> Executing

    Completed --> Idle: 다음 작업 대기
    Failed --> Idle: 오류 보고

    Completed --> [*]: 세션 종료
    Failed --> [*]: 세션 종료
```

---

## 9. 통신 프로토콜

### 9.1 메시지 흐름

```mermaid
sequenceDiagram
    participant O as 총괄 디렉터
    participant C as Context Files
    participant A1 as Agent 1
    participant A2 as Agent 2

    Note over O,A2: Phase 1: 컨텍스트 생성

    O->>C: project.json 작성
    C-->>O: 저장 완료

    O->>C: tasks.json 작성
    C-->>O: 저장 완료

    Note over O,A2: Phase 2: 에이전트 실행

    O->>A1: Task 전달 (메모리)
    activate A1

    A1->>C: project.json 읽기
    C-->>A1: 프로젝트 정보

    A1->>A1: 작업 수행

    A1->>C: agent1-context.json 작성
    C-->>A1: 저장 완료

    A1-->>O: 작업 완료 (메모리)
    deactivate A1

    O->>A2: Task 전달 (메모리)
    activate A2

    A2->>C: project.json 읽기
    C-->>A2: 프로젝트 정보

    A2->>C: agent1-context.json 읽기
    C-->>A2: Agent 1 결과물

    A2->>A2: 작업 수행

    A2->>C: agent2-context.json 작성
    C-->>A2: 저장 완료

    A2-->>O: 작업 완료 (메모리)
    deactivate A2

    Note over O,A2: 메모리 = 빠른 전달<br/>파일 = 영구 저장
```

---

## 10. 프레임워크 감지 로직

### 10.1 결정 트리

```mermaid
graph TD
    Start([프로젝트 루트 스캔])

    Start --> CheckPython{Python<br/>프로젝트?}

    CheckPython -->|Yes| PyCheck1{requirements.txt<br/>또는 pyproject.toml}
    CheckPython -->|No| CheckJS

    PyCheck1 -->|streamlit| PyStreamlit[🎯 Streamlit App<br/>Frontend: Streamlit<br/>Backend: Python]
    PyCheck1 -->|fastapi| PyFastAPI[🎯 FastAPI<br/>Backend: FastAPI]
    PyCheck1 -->|django| PyDjango[🎯 Django<br/>Backend: Django]
    PyCheck1 -->|flask| PyFlask[🎯 Flask<br/>Backend: Flask]

    CheckJS{JavaScript/<br/>TypeScript?}

    CheckJS -->|Yes| JSCheck1{package.json<br/>확인}
    CheckJS -->|No| CheckJava

    JSCheck1 -->|react| JSReact[🎯 React App<br/>Frontend: React]
    JSCheck1 -->|vue| JSVue[🎯 Vue App<br/>Frontend: Vue]
    JSCheck1 -->|angular| JSAngular[🎯 Angular App<br/>Frontend: Angular]
    JSCheck1 -->|express| JSExpress[🎯 Express<br/>Backend: Express]
    JSCheck1 -->|nestjs| JSNest[🎯 NestJS<br/>Backend: NestJS]

    CheckJava{Java<br/>프로젝트?}

    CheckJava -->|Yes| JavaCheck1{pom.xml<br/>또는 build.gradle}
    CheckJava -->|No| Unknown

    JavaCheck1 -->|spring| JavaSpring[🎯 Spring Boot<br/>Backend: Spring]

    Unknown[❓ 알 수 없는 프로젝트]

    PyStreamlit --> Recommend1[추천 에이전트:<br/>Frontend Dev<br/>Backend Dev<br/>DB Architect]
    PyFastAPI --> Recommend2[추천 에이전트:<br/>Backend Dev<br/>DB Architect]
    PyDjango --> Recommend2
    PyFlask --> Recommend2

    JSReact --> Recommend3[추천 에이전트:<br/>Frontend Dev<br/>UI/UX Designer]
    JSVue --> Recommend3
    JSAngular --> Recommend3

    JSExpress --> Recommend2
    JSNest --> Recommend2
    JavaSpring --> Recommend2

    Unknown --> Manual[수동 설정 필요]

    style PyStreamlit fill:#50C878,color:#fff
    style PyFastAPI fill:#50C878,color:#fff
    style PyDjango fill:#50C878,color:#fff
    style PyFlask fill:#50C878,color:#fff

    style JSReact fill:#FF6B6B,color:#fff
    style JSVue fill:#FF6B6B,color:#fff
    style JSAngular fill:#FF6B6B,color:#fff
    style JSExpress fill:#50C878,color:#fff
    style JSNest fill:#50C878,color:#fff

    style JavaSpring fill:#50C878,color:#fff
```

---

## 11. 성능 최적화 전략

### 11.1 캐싱 전략

```mermaid
graph TB
    Request[사용자 요청]

    Request --> CheckCache{project.json<br/>캐시 존재?}

    CheckCache -->|Yes| CheckAge{캐시<br/>유효?}
    CheckCache -->|No| FullScan[전체 프로젝트 스캔]

    CheckAge -->|Fresh < 1시간| UseCache[캐시 사용]
    CheckAge -->|Stale > 1시간| IncrementalScan[증분 스캔]

    IncrementalScan --> CompareFiles{파일<br/>변경됨?}

    CompareFiles -->|Yes| PartialUpdate[부분 업데이트]
    CompareFiles -->|No| UseCache

    PartialUpdate --> UpdateCache[캐시 갱신]
    FullScan --> CreateCache[캐시 생성]

    CreateCache --> Done
    UpdateCache --> Done
    UseCache --> Done

    Done([분석 완료])

    style UseCache fill:#50C878,color:#fff
    style IncrementalScan fill:#F39C12,color:#fff
    style FullScan fill:#FF6B6B,color:#fff
```

### 11.2 병렬 실행 최적화

```mermaid
gantt
    title 작업 실행 타임라인 (순차 vs 병렬)
    dateFormat  ss
    axisFormat %S초

    section 순차 실행
    프로젝트 분석        :a1, 00, 10s
    DB 스키마 설계       :a2, after a1, 15s
    Backend API 구현     :a3, after a2, 20s
    Frontend UI 구현     :a4, after a3, 18s
    결과 통합           :a5, after a4, 7s
    총 70초             :milestone, after a5, 0s

    section 병렬 실행
    프로젝트 분석        :b1, 00, 10s
    DB 스키마 설계       :b2, after b1, 15s
    Backend API 구현     :b3, after b2, 20s
    Frontend UI 구현     :crit, after b2, 18s
    UI 디자인           :crit, after b1, 12s
    결과 통합           :b5, after b3, 7s
    총 52초             :milestone, after b5, 0s
```

---

## 📊 요약

### 주요 다이어그램 활용 가이드

| 다이어그램 | 용도 | 대상 |
|----------|------|------|
| **레이어드 아키텍처** | 전체 시스템 구조 이해 | 시스템 설계자 |
| **워크플로우** | 작업 흐름 파악 | 개발자 |
| **시퀀스 다이어그램** | 상세 동작 이해 | 구현 담당자 |
| **의존성 그래프** | 실행 순서 결정 | 총괄 디렉터 |
| **상태 머신** | 작업 상태 추적 | 디버깅 담당자 |
| **프레임워크 감지** | 자동 인식 로직 | 프로젝트 분석기 |

---

**작성자**: Claude Code
**버전**: v1.0.0
**최종 업데이트**: 2025-11-08
