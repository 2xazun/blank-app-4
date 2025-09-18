import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="기후안정 프로젝트 대시보드", layout="wide")

# -------------------------------
# 예시용 긴 기간 데이터 생성 (1900~2024)
# 실제 데이터로 교체 가능
# -------------------------------
years = list(range(1900, 2025))

# 계절별 기온 (단순 선형 추세 예시)
summer_temp = np.linspace(23.0, 25.5, len(years))  # 여름 평균
winter_temp = np.linspace(-2.0, -0.2, len(years))  # 겨울 평균

df_temp = pd.DataFrame({
    "연도": years,
    "여름 평균기온(℃)": summer_temp,
    "겨울 평균기온(℃)": winter_temp
})

# 폭염/한파 일수
heatwave_days = np.linspace(5, 20, len(years))
coldwave_days = np.linspace(20, 5, len(years))
df_extreme = pd.DataFrame({
    "연도": years,
    "폭염일수(일)": heatwave_days,
    "한파일수(일)": coldwave_days
})

# 온실가스 배출량
df_emission = pd.DataFrame({
    "연도": years,
    "CO₂": np.linspace(300, 620, len(years)),
    "CH₄": np.linspace(40, 60, len(years)),
    "N₂O": np.linspace(15, 28, len(years))
})

# -------------------------------
# 사이드바 옵션
# -------------------------------
st.sidebar.header("📊 데이터 옵션")

# 표시할 데이터 카테고리 선택
categories = st.sidebar.multiselect(
    "보고 싶은 데이터 카테고리 선택",
    ["계절별 평균기온", "폭염/한파 발생 일수", "온실가스 배출량"],
    default=["계절별 평균기온", "폭염/한파 발생 일수", "온실가스 배출량"]
)

# 분석 기간 (1900~2024)
year_range = st.sidebar.slider(
    "기간 선택",
    min_value=1900, max_value=2024,
    value=(2000, 2020)
)

show_trend = st.sidebar.checkbox("추세선 표시", True)

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
        markers=True, color_discrete_map={"폭염일수(일)":"red","한파일수(일)":"blue"}
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
