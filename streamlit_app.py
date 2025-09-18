import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="기후안정 프로젝트 대시보드 (원인 포함)", layout="wide")

# -------------------------------
# 데이터 로드 함수들
# -------------------------------

@st.cache_data
def load_sector_emissions():
    # 실제 데이터 출처 Our World in Data / IEA 등
    # 예시 데이터: 부문별 배출 비율 변화 (에너지 / 산업 / 수송 / 기타)
    years = list(range(2000, 2024))
    data = []
    sectors = ["에너지 산업", "수송", "산업 공정", "농업", "폐기물"]
    for sec in sectors:
        base = {"에너지 산업":300, "수송":80, "산업 공정":70, "농업":30, "폐기물":20}[sec]
        for y in years:
            emissions = base * (1 + 0.02*(y - 2000)) + np.random.normal(0, base*0.05)
            data.append({"year": y, "sector": sec, "emissions": emissions})
    return pd.DataFrame(data)

@st.cache_data
def load_biomass_forest_change():
    years = list(range(2015, 2024))
    biomass = [8,9,10,11,12,12.5,13,13.8,14]  # 단위: Mt CO2
    forest_loss = [50,52,55,60,62,63,65,68,70]  # 천 헥타르
    return pd.DataFrame({"year": years, "biomass_emission": biomass, "forest_loss_kt": forest_loss})

@st.cache_data
def load_emission_data():
    # 예시 데이터: 한국 전체 온실가스 배출량 (단위: kt CO2-eq)
    years = list(range(2000, 2024))
    emissions = []
    for y in years:
        base = 500000  # 기준값 (2000년: 50만 kt CO2-eq)
        value = base * (1 + 0.015*(y - 2000)) + np.random.normal(0, base*0.02)
        emissions.append({"year": y, "emissions": value})
    return pd.DataFrame(emissions)

# -------------------------------
# 사이드바 옵션
# -------------------------------
st.sidebar.header("📊 데이터 옵션")

categories = st.sidebar.multiselect(
    "보고 싶은 데이터 카테고리 선택",
    ["계절별 평균기온", "온실가스 배출량", "부문별 배출 원인", "바이오매스 & 산림 변화"],
    default=["계절별 평균기온", "온실가스 배출량"]
)

year_range = st.sidebar.slider(
    "기간 선택",
    min_value=2000, max_value=2023,
    value=(2005, 2022)
)

show_markers = st.sidebar.checkbox("마커 표시", True)
use_log = st.sidebar.checkbox("로그 스케일 (y축)", False)

# -------------------------------
# 본문
# -------------------------------
st.title("🌍 기후 안정 프로젝트 대시보드 (원인 중심)")

st.write(f"선택된 기간: {year_range[0]}년 ~ {year_range[1]}년")

# -- (A) 부문별 배출 원인 --
if "부문별 배출 원인" in categories:
    st.subheader("🔍 한국의 부문별 온실가스 배출 변화")
    df_sec = load_sector_emissions()
    df_sec_f = df_sec[(df_sec["year"] >= year_range[0]) & (df_sec["year"] <= year_range[1])]
    fig_sec = px.line(
        df_sec_f, x="year", y="emissions", color="sector",
        markers=show_markers,
        labels={"emissions":"부문별 배출량 (단위 Mt CO₂-eq)", "year":"연도", "sector":"부문"}
    )
    if use_log:
        fig_sec.update_yaxes(type="log")
    st.plotly_chart(fig_sec, use_container_width=True)

# -- (B) 바이오매스 및 산림 변화 --
if "바이오매스 & 산림 변화" in categories:
    st.subheader("🌱 바이오매스 발전 배출 & 산림 변화 추이")
    df_bf = load_biomass_forest_change()
    df_bf_f = df_bf[(df_bf["year"] >= year_range[0]) & (df_bf["year"] <= year_range[1])]
    
    col1, col2 = st.columns(2)
    with col1:
        fig_bio = px.line(
            df_bf_f, x="year", y="biomass_emission",
            markers=show_markers,
            labels={"biomass_emission":"바이오매스 발전 배출량 (Mt CO₂)", "year":"연도"}
        )
        st.plotly_chart(fig_bio, use_container_width=True)
    with col2:
        fig_forest = px.line(
            df_bf_f, x="year", y="forest_loss_kt",
            markers=show_markers,
            labels={"forest_loss_kt":"산림 손실 (천 헥타르)", "year":"연도"}
        )
        st.plotly_chart(fig_forest, use_container_width=True)

# -- (C) 기존 온실가스 배출량 전체 --
if "온실가스 배출량" in categories:
    st.subheader("🧪 전체 온실가스 배출량 변화")
    df_em = load_emission_data()
    df_em_f = df_em[(df_em["year"] >= year_range[0]) & (df_em["year"] <= year_range[1])]
    fig_em = px.line(
        df_em_f, x="year", y="emissions",
        markers=show_markers,
        labels={"emissions":"전체 배출량 (kt CO₂-eq)", "year":"연도"}
    )
    if use_log:
        fig_em.update_yaxes(type="log")
    st.plotly_chart(fig_em, use_container_width=True)

# -------------------------------
# 해결방안 & 실천 과제
# -------------------------------
st.subheader("✅ 해결방안과 실천 과제")
st.markdown("""
- **에너지 전환 강화**: 화석연료(특히 석탄) 발전소 단계적 폐지 & 재생에너지/핵발전 확대  
- **바이오매스 발전의 투명성 확보 및 지속 가능성 평가 강화**  
- **산림 복구 및 토지 이용 관리**: 삼림 복원, 숲의 탄소 흡수 기능 개선  
- **수송 부문 탈탄소화**: 전기차/수소차 보급 확대, 대중교통 활성화  
- **산업 부문 기술 혁신**: 탄소 포집·저장(CCS), 공정 효율 향상  
""")

st.markdown("---")
st.markdown("**데이터 출처**:")
st.markdown("- Greenhouse Gas Emissions in South Korea / Emission-Index")
st.markdown("- South Korea: CO₂ Country Profile / Our World in Data")
st.markdown("- 10 Years of Biomass Power in South Korea (바이오매스 발전 배출)")
st.markdown("- South Korea Deforestation Rates & Statistics / Global Forest Watch")
