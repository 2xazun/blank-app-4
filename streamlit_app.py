import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="기후안정 프로젝트 대시보드", layout="wide")

# -------------------------------
# (1) 계절별 기온 변화 (예시 데이터: 2000~2020)
# 실제 사용 시: 기상청 기후정보포털 CSV 불러오기
# -------------------------------
years = list(range(2000, 2021))
summer_temp = np.linspace(24.0, 25.4, 21)   # 약 1.4℃ 상승
winter_temp = np.linspace(-1.5, -0.5, 21)   # 겨울 기온 완만한 상승
df_temp = pd.DataFrame({
    "연도": years,
    "여름 평균기온(℃)": summer_temp,
    "겨울 평균기온(℃)": winter_temp
})

# -------------------------------
# (2) 폭염/한파 일수 변화 (예시 데이터)
# 실제 사용 시: 기상청 이상기후 통계
# -------------------------------
heatwave_days = np.linspace(10, 15, 21)  # 폭염일수 증가
coldwave_days = np.linspace(12, 7, 21)   # 한파일수 감소
df_extreme = pd.DataFrame({
    "연도": years,
    "폭염일수(일)": heatwave_days,
    "한파일수(일)": coldwave_days
})

# -------------------------------
# (3) 온실가스 배출량 (예시 데이터: 단위 MtCO2eq)
# 실제 사용 시: 지표누리(온실가스 통계) CSV 불러오기
# -------------------------------
df_emission = pd.DataFrame({
    "연도": years,
    "CO₂": np.linspace(480, 600, 21),
    "CH₄": np.linspace(45, 55, 21),
    "N₂O": np.linspace(20, 25, 21)
})

# -------------------------------
# 사이드바
# -------------------------------
st.sidebar.header("📊 데이터 옵션")
year_range = st.sidebar.slider("기간 선택", 2000, 2020, (2005, 2020))
show_trend = st.sidebar.checkbox("추세선 표시", True)

# -------------------------------
# 본문 레이아웃
# -------------------------------
st.title("🌍 기후안정 프로젝트 : 청소년이 할 수 있는 실천 가이드")

# (1) 계절별 기온 변화
st.subheader("📈 지난 20년간 계절별 평균 기온 변화")
fig_temp = px.line(
    df_temp[(df_temp["연도"] >= year_range[0]) & (df_temp["연도"] <= year_range[1])],
    x="연도", y=["여름 평균기온(℃)", "겨울 평균기온(℃)"],
    markers=True
)
st.plotly_chart(fig_temp, use_container_width=True)

# (2) 폭염/한파 일수 변화
st.subheader("☀️🌨 폭염·한파 발생 일수 추이")
fig_extreme = px.line(
    df_extreme[(df_extreme["연도"] >= year_range[0]) & (df_extreme["연도"] <= year_range[1])],
    x="연도", y=["폭염일수(일)", "한파일수(일)"],
    markers=True, color_discrete_map={"폭염일수(일)":"red","한파일수(일)":"blue"}
)
st.plotly_chart(fig_extreme, use_container_width=True)

# (3) 온실가스 배출량 추이
st.subheader("🧪 온실가스 배출량 추이 (MtCO₂eq)")
fig_emission = px.area(
    df_emission[(df_emission["연도"] >= year_range[0]) & (df_emission["연도"] <= year_range[1])],
    x="연도", y=["CO₂", "CH₄", "N₂O"], 
    title="한국 온실가스 배출량 추세"
)
st.plotly_chart(fig_emission, use_container_width=True)

# -------------------------------
# 데이터 다운로드
# -------------------------------
st.download_button("📥 기온 데이터 다운로드", df_temp.to_csv(index=False).encode("utf-8"), "temp_data.csv", "text/csv")
st.download_button("📥 이상기후 데이터 다운로드", df_extreme.to_csv(index=False).encode("utf-8"), "extreme_data.csv", "text/csv")
st.download_button("📥 온실가스 데이터 다운로드", df_emission.to_csv(index=False).encode("utf-8"), "emission_data.csv", "text/csv")
