import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="기후안정 프로젝트 대시보드", layout="wide")

# -------------------------------
# 예시 데이터 생성 (1900~2024)
# -------------------------------
years = list(range(1900, 2025))

df_temp = pd.DataFrame({
    "연도": years,
    "여름 평균기온(℃)": np.linspace(23.0, 25.5, len(years)),
    "겨울 평균기온(℃)": np.linspace(-2.0, -0.2, len(years))
})

df_extreme = pd.DataFrame({
    "연도": years,
    "폭염일수(일)": np.linspace(5, 20, len(years)),
    "한파일수(일)": np.linspace(20, 5, len(years))
})

df_emission = pd.DataFrame({
    "연도": years,
    "CO₂": np.linspace(300, 620, len(years)),
    "CH₄": np.linspace(40, 60, len(years)),
    "N₂O": np.linspace(15, 28, len(years))
})

# 지역별 데이터 예시
regions = {
    "서울": {"온도": np.linspace(12, 15, len(years)), "폭염": np.linspace(5, 18, len(years))},
    "부산": {"온도": np.linspace(14, 17, len(years)), "폭염": np.linspace(7, 20, len(years))},
    "대전": {"온도": np.linspace(13, 16, len(years)), "폭염": np.linspace(6, 19, len(years))},
    "제주": {"온도": np.linspace(15, 18, len(years)), "폭염": np.linspace(8, 22, len(years))}
}

# -------------------------------
# 사이드바 옵션
# -------------------------------
st.sidebar.header("📊 데이터 옵션")

categories = st.sidebar.multiselect(
    "보고 싶은 데이터 카테고리 선택",
    ["계절별 평균기온", "폭염/한파 발생 일수", "온실가스 배출량"],
    default=["계절별 평균기온", "폭염/한파 발생 일수", "온실가스 배출량"]
)

year_range = st.sidebar.slider(
    "기간 선택",
    min_value=1900, max_value=2024,
    value=(2000, 2020)
)

show_trend = st.sidebar.checkbox("추세선 표시", True)

region_select = st.sidebar.selectbox("지역 선택 (상세 분석)", list(regions.keys()))

# -------------------------------
# 본문 레이아웃
# -------------------------------
st.title("🌍 기후안정 프로젝트 대시보드")
st.write(f"선택된 기간: {year_range[0]}년 ~ {year_range[1]}년")

# -------------------------------
# (1) 계절별 기온 변화
# -------------------------------
if "계절별 평균기온" in categories:
    st.subheader("📈 계절별 평균 기온 변화")
    fig_temp = px.line(
        df_temp[(df_temp["연도"] >= year_range[0]) & (df_temp["연도"] <= year_range[1])],
        x="연도", y=["여름 평균기온(℃)", "겨울 평균기온(℃)"],
        markers=True
    )
    if show_trend:
        fig_temp.update_traces(mode="lines+markers")
    st.plotly_chart(fig_temp, use_container_width=True)

# -------------------------------
# (2) 폭염/한파 발생 일수
# -------------------------------
if "폭염/한파 발생 일수" in categories:
    st.subheader("☀️🌨 폭염·한파 발생 일수 추이")
    fig_extreme = px.line(
        df_extreme[(df_extreme["연도"] >= year_range[0]) & (df_extreme["연도"] <= year_range[1])],
        x="연도", y=["폭염일수(일)", "한파일수(일)"],
        markers=True
    )
    st.plotly_chart(fig_extreme, use_container_width=True)

# -------------------------------
# (3) 온실가스 배출량
# -------------------------------
if "온실가스 배출량" in categories:
    st.subheader("🧪 온실가스 배출량 추세 (MtCO₂eq)")
    fig_emission = px.area(
        df_emission[(df_emission["연도"] >= year_range[0]) & (df_emission["연도"] <= year_range[1])],
        x="연도", y=["CO₂", "CH₄", "N₂O"]
    )
    st.plotly_chart(fig_emission, use_container_width=True)

# -------------------------------
# (4) 지역별 상세 분석
# -------------------------------
st.subheader(f"📍 {region_select} 상세 분석")
df_region = pd.DataFrame({
    "연도": years,
    "평균기온(℃)": regions[region_select]["온도"],
    "폭염일수(일)": regions[region_select]["폭염"]
})
df_region = df_region[(df_region["연도"] >= year_range[0]) & (df_region["연도"] <= year_range[1])]

col1, col2 = st.columns(2)
with col1:
    fig_r1 = px.line(df_region, x="연도", y="평균기온(℃)", markers=True)
    st.plotly_chart(fig_r1, use_container_width=True)
with col2:
    fig_r2 = px.bar(df_region, x="연도", y="폭염일수(일)")
    st.plotly_chart(fig_r2, use_container_width=True)

# -------------------------------
# (5) 해결방안 & 실천 과제
# -------------------------------
st.subheader("✅ 해결방안과 실천 과제")

st.markdown("""
- **개인 차원**: 대중교통 이용, 에너지 절약, 일회용품 줄이기  
- **학교 차원**: 친환경 교육 강화, 교실 내 에너지 관리, 기후 동아리 운영  
- **정부 차원**: 재생에너지 확대, 탄소중립 정책 강화, 기후 취약계층 보호 대책 마련  
""")

# -------------------------------
# (6) 데이터 출처
# -------------------------------
st.markdown("---")
st.markdown("**데이터 출처**: [NOAA](https://www.noaa.gov), [NASA GISS](https://data.giss.nasa.gov), [World Bank Climate Data](https://data.worldbank.org)")
