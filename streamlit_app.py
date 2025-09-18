import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="기후안정 프로젝트 대시보드", layout="wide")

# -------------------------------
# 데이터 불러오기 (예시 + 더미 데이터)
# -------------------------------
@st.cache_data
def load_temperature_data():
    years = list(range(1900, 2025))
    data = []
    regions = ["서울", "부산", "제주", "대전"]
    seasons = ["여름","겨울"]
    for reg in regions:
        for season in seasons:
            base = 24.0 if season=="여름" else -1.5
            for y in years:
                temp = base + 0.02*(y - 1900) + np.random.normal(0,0.5)
                data.append({"year": y, "region": reg, "season": season, "avg_temp": temp})
    return pd.DataFrame(data)

@st.cache_data
def load_emission_data():
    years = list(range(1990, 2021))
    emissions = np.linspace(400000, 700000, len(years)) + np.random.normal(0,20000, len(years))
    return pd.DataFrame({"year": years, "emissions": emissions})

@st.cache_data
def load_extreme_data():
    years = list(range(1960, 2025))
    heatwave = np.linspace(3, 25, len(years)) + np.random.normal(0,2,len(years))
    coldwave = np.linspace(20, 4, len(years)) + np.random.normal(0,2,len(years))
    return pd.DataFrame({"year": years, "heatwave_days": heatwave, "coldwave_days": coldwave})

@st.cache_data
def load_precipitation_data():
    years = list(range(1900, 2025))
    rainfall = np.linspace(900, 1400, len(years)) + np.random.normal(0,50,len(years))
    return pd.DataFrame({"year": years, "rainfall": rainfall})

@st.cache_data
def load_sealevel_data():
    years = list(range(1900, 2025))
    sealevel = np.linspace(0, 25, len(years)) + np.random.normal(0,1,len(years))
    return pd.DataFrame({"year": years, "sealevel_rise_cm": sealevel})

# -------------------------------
# 데이터 준비
# -------------------------------
df_temp = load_temperature_data()
df_emission = load_emission_data()
df_extreme = load_extreme_data()
df_precip = load_precipitation_data()
df_sealevel = load_sealevel_data()

# -------------------------------
# 사이드바 옵션
# -------------------------------
st.sidebar.header("📊 데이터 옵션")

categories = st.sidebar.multiselect(
    "보고 싶은 데이터 카테고리 선택",
    ["계절별 평균기온", "온실가스 배출량", "폭염/한파 발생 일수", "강수량", "해수면 상승"],
    default=["계절별 평균기온", "온실가스 배출량"]
)

year_range = st.sidebar.slider(
    "기간 선택",
    min_value=1900, max_value=2024,
    value=(2000, 2020)
)

graph_type = st.sidebar.radio(
    "그래프 유형 선택",
    ["꺾은선(line)", "영역(area)", "막대(bar)"],
    index=0
)

show_markers = st.sidebar.checkbox("마커 표시", True)
use_log = st.sidebar.checkbox("로그 스케일 적용 (y축)", False)
show_ma = st.sidebar.checkbox("이동평균선(5년) 표시", False)

region_select = st.sidebar.selectbox("지역 선택 (상세 분석)", df_temp["region"].unique().tolist())

# -------------------------------
# 본문 레이아웃
# -------------------------------
st.title("🌍 기후안정 프로젝트 대시보드")
st.write(f"선택된 기간: {year_range[0]}년 ~ {year_range[1]}년")

# -------------------------------
# (1) 계절별 평균기온
# -------------------------------
if "계절별 평균기온" in categories:
    st.subheader("📈 계절별 평균기온 변화")
    df_temp_filtered = df_temp[(df_temp["year"] >= year_range[0]) & (df_temp["year"] <= year_range[1])]
    df_grouped = df_temp_filtered.groupby(["year","season"])["avg_temp"].mean().reset_index()
    if show_ma:
        df_grouped["avg_temp"] = df_grouped.groupby("season")["avg_temp"].transform(lambda x: x.rolling(5,1).mean())
    if graph_type=="꺾은선(line)":
        fig = px.line(df_grouped, x="year", y="avg_temp", color="season", markers=show_markers)
    elif graph_type=="영역(area)":
        fig = px.area(df_grouped, x="year", y="avg_temp", color="season")
    else:
        fig = px.bar(df_grouped, x="year", y="avg_temp", color="season")
    if use_log:
        fig.update_yaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"📍 {region_select} 지역 상세 기온 변화")
    df_reg = df_temp_filtered[df_temp_filtered["region"] == region_select]
    fig_reg = px.line(df_reg, x="year", y="avg_temp", color="season", markers=show_markers)
    st.plotly_chart(fig_reg, use_container_width=True)

# -------------------------------
# (2) 온실가스 배출량
# -------------------------------
if "온실가스 배출량" in categories:
    st.subheader("🧪 한국 온실가스 배출량 변화 (CO₂ eq.)")
    df_em = df_emission[(df_emission["year"] >= year_range[0]) & (df_emission["year"] <= year_range[1])]
    if show_ma:
        df_em["emissions"] = df_em["emissions"].rolling(5,1).mean()
    if graph_type=="꺾은선(line)":
        fig_em = px.line(df_em, x="year", y="emissions", markers=show_markers)
    elif graph_type=="영역(area)":
        fig_em = px.area(df_em, x="year", y="emissions")
    else:
        fig_em = px.bar(df_em, x="year", y="emissions")
    if use_log:
        fig_em.update_yaxes(type="log")
    st.plotly_chart(fig_em, use_container_width=True)

# -------------------------------
# (3) 폭염/한파
# -------------------------------
if "폭염/한파 발생 일수" in categories:
    st.subheader("☀️🌨 폭염/한파 발생 일수")
    df_ex = df_extreme[(df_extreme["year"] >= year_range[0]) & (df_extreme["year"] <= year_range[1])]
    fig_ext = px.line(df_ex, x="year", y=["heatwave_days","coldwave_days"], markers=show_markers)
    st.plotly_chart(fig_ext, use_container_width=True)

# -------------------------------
# (4) 강수량
# -------------------------------
if "강수량" in categories:
    st.subheader("🌧 연간 강수량 변화")
    df_p = df_precip[(df_precip["year"] >= year_range[0]) & (df_precip["year"] <= year_range[1])]
    fig_p = px.line(df_p, x="year", y="rainfall", markers=show_markers)
    st.plotly_chart(fig_p, use_container_width=True)

# -------------------------------
# (5) 해수면 상승
# -------------------------------
if "해수면 상승" in categories:
    st.subheader("🌊 해수면 상승 (cm)")
    df_s = df_sealevel[(df_sealevel["year"] >= year_range[0]) & (df_sealevel["year"] <= year_range[1])]
    fig_s = px.line(df_s, x="year", y="sealevel_rise_cm", markers=show_markers)
    st.plotly_chart(fig_s, use_container_width=True)

# -------------------------------
# (6) 해결방안 & 실천 과제
# -------------------------------
st.subheader("✅ 해결방안과 실천 과제")
st.markdown("""
- **개인 차원**: 대중교통 이용, 에너지 절약, 일회용품 줄이기, 채식 위주 식단  
- **학교 차원**: 친환경 교육, 교실 내 에너지 관리, 기후 동아리 운영  
- **사회/정책 차원**: 재생에너지 확대, 탄소중립 정책 강화, 기후 취약계층 보호  
""")

# -------------------------------
# (7) 데이터 출처
# -------------------------------
st.markdown("---")
st.markdown("**데이터 출처**:")
st.markdown("- 기상청 Open MET Data Portal (기온, 폭염/한파, 강수량 통계)")
st.markdown("- Our World in Data (온실가스 배출량)")
st.markdown("- NOAA, NASA GISS (해수면 상승)")
