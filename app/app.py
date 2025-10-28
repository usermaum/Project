"""
더문드립바 웹 애플리케이션 - 메인 앱 (v2.0)
The Moon Drip BAR - Roasting Management System
Streamlit 멀티페이지 애플리케이션
"""

import streamlit as st
import sys
import os
from datetime import datetime

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import SessionLocal, init_db
from services.bean_service import BeanService
from services.blend_service import BlendService
from utils.constants import UI_CONFIG
from i18n import Translator, LanguageManager

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 페이지 설정
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title=UI_CONFIG["app_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 커스텀 스타일
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════
       주요 컬러 변수
       ═══════════════════════════════════════════════════════════ */
    :root {
        --primary: #1F4E78;
        --secondary: #4472C4;
        --success: #70AD47;
        --danger: #C41E3A;
        --sidebar-bg: #f8f9fa;
        --hover-bg: #f0f0f0;
        --text-muted: #666;
        --divider-color: #e0e0e0;
    }

    /* ═══════════════════════════════════════════════════════════
       메인 헤더
       ═══════════════════════════════════════════════════════════ */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }

    .sub-header {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
    }

    /* ═══════════════════════════════════════════════════════════
       Claude Desktop 스타일 사이드바
       ═══════════════════════════════════════════════════════════ */

    /* 사이드바 배경 */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        padding: 1rem 0.5rem;
    }

    /* 사이드바 섹션 헤더 */
    [data-testid="stSidebar"] h3 {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: var(--text-muted);
        letter-spacing: 0.5px;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-left: 0.5rem;
    }

    /* 사이드바 첫 번째 h3는 margin-top 제거 */
    [data-testid="stSidebar"] h3:first-of-type {
        margin-top: 0;
    }

    /* 메뉴 버튼 기본 스타일 */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        padding: 12px 16px;
        border-radius: 8px;
        border: none;
        background-color: transparent !important;
        color: var(--text-muted) !important;
        font-size: 14px;
        font-weight: 400;
        transition: all 0.2s ease;
        margin-bottom: 4px;
        cursor: pointer;
        border-left: 4px solid transparent;
    }

    /* 사이드바 버튼 호버 효과 */
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: var(--hover-bg) !important;
        color: var(--primary) !important;
        border-left-color: transparent;
    }

    /* 사이드바 버튼 활성 (primary type) */
    [data-testid="stSidebar"] .stButton[role="button"] > button {
        background-color: var(--secondary) !important;
        color: white !important;
        font-weight: 600;
        border-left: 4px solid var(--primary) !important;
    }

    /* Divider 스타일 */
    [data-testid="stSidebar"] hr {
        margin: 1rem 0;
        border: none;
        border-top: 1px solid var(--divider-color);
        opacity: 0.5;
    }

    /* 메트릭 카드 (사이드바) */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background-color: white;
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] label {
        font-size: 12px;
        color: var(--text-muted);
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 20px;
        font-weight: 600;
        color: var(--primary);
    }

    /* 사이드바 아이콘 크기 */
    [data-testid="stSidebar"] .stButton > button span {
        font-size: 18px;
    }

    /* Info/Alert Box (사이드바) */
    [data-testid="stSidebar"] .stAlert {
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 13px;
    }

    /* Caption 텍스트 (사이드바) */
    [data-testid="stSidebar"] .stCaption {
        font-size: 11px;
        color: #999;
        line-height: 1.5;
    }

    /* ═══════════════════════════════════════════════════════════
       메인 콘텐츠 버튼
       ═══════════════════════════════════════════════════════════ */

    /* 메인 영역 버튼 */
    .stButton > button {
        background-color: var(--secondary) !important;
        color: white !important;
        border: none !important;
        transition: background-color 0.2s ease;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: var(--primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔄 세션 상태 초기화
# ═══════════════════════════════════════════════════════════════════════════════

def init_session_state():
    """세션 상태 초기화"""
    if "db" not in st.session_state:
        st.session_state.db = SessionLocal()

    if "bean_service" not in st.session_state:
        st.session_state.bean_service = BeanService(st.session_state.db)

    if "blend_service" not in st.session_state:
        st.session_state.blend_service = BlendService(st.session_state.db)

    # 다중 언어 지원 초기화
    if "translator" not in st.session_state:
        st.session_state.translator = Translator(default_language="ko")

    if "language_manager" not in st.session_state:
        st.session_state.language_manager = LanguageManager(st.session_state.translator)


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 헤더 및 사이드바
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    """헤더 렌더링"""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown(f'<p class="main-header">☕ {UI_CONFIG["app_title"]}</p>',
                   unsafe_allow_html=True)
        st.markdown(f'<p class="sub-header">{UI_CONFIG["app_subtitle"]}</p>',
                   unsafe_allow_html=True)

    with col2:
        st.write("")
        st.write("")
        st.metric("현재시간", datetime.now().strftime("%H:%M"))


def render_sidebar():
    """사이드바 렌더링 (Claude Desktop 스타일)"""
    with st.sidebar:
        # ═══════════════════════════════════════════════════════════
        # 1️⃣ 로고 영역
        # ═══════════════════════════════════════════════════════════
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0 2rem 0;'>
            <h2 style='margin: 0; color: #1F4E78; font-size: 28px;'>☕ The Moon</h2>
            <p style='margin: 4px 0 0 0; font-size: 12px; color: #999;'>Drip BAR Roasting System</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 2️⃣ 언어 선택
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 🌐 언어")

        lang_manager = st.session_state.language_manager
        translator = st.session_state.translator
        current_lang = lang_manager.get_current_language()

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "🇰🇷 한글",
                use_container_width=True,
                key="lang_ko",
                type="primary" if current_lang == "ko" else "secondary"
            ):
                if lang_manager.set_current_language("ko"):
                    st.rerun()

        with col2:
            if st.button(
                "🇬🇧 English",
                use_container_width=True,
                key="lang_en",
                type="primary" if current_lang == "en" else "secondary"
            ):
                if lang_manager.set_current_language("en"):
                    st.rerun()

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 3️⃣ 핵심 기능 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📌 핵심 기능")

        # 현재 페이지 감지
        current_page = st.session_state.get("current_page", "home")

        # 홈
        if st.button(
            "🏠 홈",
            type="primary" if current_page == "home" else "secondary",
            use_container_width=True,
            key="nav_home"
        ):
            st.session_state["current_page"] = "home"
            st.switch_page("app.py")

        # 원두관리
        if st.button(
            "☕ 원두관리",
            type="primary" if current_page == "BeanManagement" else "secondary",
            use_container_width=True,
            key="nav_bean"
        ):
            st.session_state["current_page"] = "BeanManagement"
            st.switch_page("pages/BeanManagement.py")

        # 블렌딩관리
        if st.button(
            "🎨 블렌딩관리",
            type="primary" if current_page == "BlendManagement" else "secondary",
            use_container_width=True,
            key="nav_blend"
        ):
            st.session_state["current_page"] = "BlendManagement"
            st.switch_page("pages/BlendManagement.py")

        # 분석
        if st.button(
            "📊 분석",
            type="primary" if current_page == "Analysis" else "secondary",
            use_container_width=True,
            key="nav_analysis"
        ):
            st.session_state["current_page"] = "Analysis"
            st.switch_page("pages/Analysis.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 4️⃣ 운영 관리 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📦 운영 관리")

        # 재고관리
        if st.button(
            "📦 재고관리",
            type="primary" if current_page == "InventoryManagement" else "secondary",
            use_container_width=True,
            key="nav_inventory"
        ):
            st.session_state["current_page"] = "InventoryManagement"
            st.switch_page("pages/InventoryManagement.py")

        # 보고서
        if st.button(
            "📋 보고서",
            type="primary" if current_page == "Report" else "secondary",
            use_container_width=True,
            key="nav_report"
        ):
            st.session_state["current_page"] = "Report"
            st.switch_page("pages/Report.py")

        # Excel동기화
        if st.button(
            "📑 Excel동기화",
            type="primary" if current_page == "ExcelSync" else "secondary",
            use_container_width=True,
            key="nav_excel"
        ):
            st.session_state["current_page"] = "ExcelSync"
            st.switch_page("pages/ExcelSync.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 5️⃣ 고급 기능 (현재 페이지 자동 감지)
        # ═══════════════════════════════════════════════════════════
        st.markdown("### ⭐ 고급 기능")

        # 고급분석
        if st.button(
            "🔬 고급분석",
            type="primary" if current_page == "AdvancedAnalysis" else "secondary",
            use_container_width=True,
            key="nav_advanced"
        ):
            st.session_state["current_page"] = "AdvancedAnalysis"
            st.switch_page("pages/AdvancedAnalysis.py")

        # 설정
        if st.button(
            "⚙️ 설정",
            type="primary" if current_page == "Settings" else "secondary",
            use_container_width=True,
            key="nav_settings"
        ):
            st.session_state["current_page"] = "Settings"
            st.switch_page("pages/Settings.py")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 6️⃣ 빠른 통계
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 📊 현황")

        db = st.session_state.db
        bean_service = st.session_state.bean_service
        blend_service = st.session_state.blend_service

        beans = bean_service.get_active_beans()
        blends = blend_service.get_active_blends()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("☕ 원두", f"{len(beans)}종")
        with col2:
            st.metric("🎨 블렌드", f"{len(blends)}개")

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 7️⃣ 도구
        # ═══════════════════════════════════════════════════════════
        st.markdown("### 🔧 도구")

        if st.button("🔄 새로고침", use_container_width=True, key="btn_refresh"):
            st.rerun()

        st.divider()

        # ═══════════════════════════════════════════════════════════
        # 8️⃣ 정보
        # ═══════════════════════════════════════════════════════════
        st.markdown("### ℹ️ 정보")
        st.caption(f"""
        **{UI_CONFIG["app_title"]}** v1.3.0

        🚀 Claude Desktop Style UI
        📅 업데이트: 2025-10-28
        🎯 상태: 운영 중

        **현재 데이터:**
        - 원두: {len(beans)}종
        - 블렌드: {len(blends)}개
        - 포션: 20개
        """)


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 홈 페이지
# ═══════════════════════════════════════════════════════════════════════════════

def render_home():
    """홈 페이지"""
    # 현재 페이지 저장 (사이드바 활성 표시)
    st.session_state["current_page"] = "home"

    render_header()

    st.divider()

    # 환영 메시지
    st.markdown("""
    # 👋 더문드립바 웹 시스템에 오신 것을 환영합니다!

    이 시스템은 로스팅 원두를 효율적으로 관리하고 분석하기 위한 통합 플랫폼입니다.
    """)

    st.divider()

    # 빠른 시작
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🎯 시작하기

        **원두 관리**
        - 13종 원두 확인
        - 새 원두 추가
        - 원두 정보 수정
        """)
        if st.button("☕ 원두관리로 이동", use_container_width=True):
            st.switch_page("pages/BeanManagement.py")

    with col2:
        st.markdown("""
        ### 🎨 블렌드 관리

        **블렌딩 레시피**
        - 풀문 블렌드 (3개)
        - 뉴문 블렌딩 (3개)
        - 원가 자동 계산
        """)
        if st.button("🎨 블렌딩관리로 이동", use_container_width=True):
            st.switch_page("pages/BlendManagement.py")

    with col3:
        st.markdown("""
        ### 📊 분석

        **통계 및 분석**
        - 판매 추이
        - 수익 분석
        - 선호도 분석
        """)
        if st.button("📊 분석으로 이동", use_container_width=True):
            st.switch_page("pages/Analysis.py")

    st.divider()

    # 주요 통계
    st.markdown("## 📊 주요 통계")

    db = st.session_state.db
    bean_service = st.session_state.bean_service
    blend_service = st.session_state.blend_service

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        bean_summary = bean_service.get_beans_summary()
        st.metric("☕ 총 원두", f"{bean_summary['total_beans']}종")

    with col2:
        blend_summary = blend_service.get_blends_summary()
        st.metric("🎨 총 블렌드", f"{blend_summary['total_blends']}개")

    with col3:
        st.metric("📦 총 포션", "20개")

    with col4:
        st.metric("🌍 국가", "6개")

    st.divider()

    # 원두 분포
    st.markdown("## 🔥 원두 로스팅 레벨 분포")

    bean_summary = bean_service.get_beans_summary()
    roast_data = bean_summary['by_roast_level']

    if roast_data:
        cols = st.columns(len(roast_data))

        for i, (level, count) in enumerate(roast_data.items()):
            level_names = {
                "W": "Light/White",
                "N": "Normal",
                "Pb": "Plus Black",
                "Rh": "Rheuma",
                "SD": "Semi-Dark",
                "SC": "Semi-Dark"
            }

            with cols[i]:
                st.metric(f"{level}\n({level_names.get(level, level)})", f"{count}개")

    st.divider()

    # 블렌드 분포
    st.markdown("## 🎨 블렌드 타입 분포")

    blend_summary = blend_service.get_blends_summary()
    type_data = blend_summary['by_type']

    if type_data:
        cols = st.columns(3)

        for i, (blend_type, count) in enumerate(type_data.items()):
            if i < len(cols):
                with cols[i]:
                    st.metric(f"{blend_type} 블렌드", f"{count}개")


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 메인 실행
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """메인 함수"""
    # 세션 상태 초기화
    init_session_state()

    # 데이터베이스 초기화 (필요 시)
    if not os.path.exists("Data/roasting_data.db"):
        with st.spinner("📊 데이터베이스 초기화 중..."):
            init_db()
            st.session_state.bean_service.init_default_beans()
            st.session_state.blend_service.init_default_blends()
            st.success("✅ 데이터베이스 초기화 완료!")

    # 사이드바
    render_sidebar()

    # 홈 페이지
    render_home()


if __name__ == "__main__":
    main()
