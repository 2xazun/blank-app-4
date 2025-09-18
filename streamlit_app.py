import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# -------------------------------
# 가상 데이터 생성 (실제 데이터로 교체 가능)
# -------------------------------
regions = ["북극해", "서태평양", "동태평양", "지중해", "인도양", "대서양"]
sea_level_rise = [4.1, 3.8, 2.8, 2.9, 3.1, 3.2]  # mm/년

latitudes = [75, 5, -5, 35, -10, 0]
longitudes = [0, 150, -120, 20, 70, -30]

df = pd.DataFrame({
    "지역": regions,
    "상승률(mm/년)": sea_level_rise,
    "위도": latitudes,
    "경도": longitudes
})

# -------------------------------
# Streamlit UI 구성
# -------------------------------
st.set_page_config(page_title="해수면 분석 대시보드", layout="wide")

st.sidebar.header("🌊 해수면 데이터 옵션")
year_range = st.sidebar.slider("기간 선택", 1990, 2024, (1993, 2024))
show_trend = st.sidebar.checkbox("추세선 표시", True)

st.sidebar.header("🔎 분석 옵션")
analysis_period = st.sidebar.slider("분석 기간", 1990, 2024, (1990, 2024))
correlation = st.sidebar.checkbox("상관관계 분석 표시", True)
window_size = st.sidebar.slider("이동평균 윈도우", 1, 10, 5)

st.sidebar.header("🧪 온실가스 분석 옵션")
gas_types = st.sidebar.multiselect("온실가스 종류 선택", ["CO2", "CH4", "N2O"], ["CO2", "CH4"])
gas_year_range = st.sidebar.slider("온실가스 분석 기간", 1990, 2022, (1990, 2022))

# -------------------------------
# 본문 레이아웃
# -------------------------------
st.title("📘 주요 지역별 해수면 상승률")
st.markdown("전 세계 주요 해역별 해수면 상승률 (mm/년)")

# 지도 시각화
fig_map = px.scatter_geo(
    df,
    lat="위도",
    lon="경도",
    text="지역",
    size="상승률(mm/년)",
    color="상승률(mm/년)",
    projection="natural earth",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------
# 지역별 순위
# -------------------------------
st.subheader("📊 지역별 상승률 순위")
sorted_df = df.sort_values("상승률(mm/년)", ascending=False)

for i, row in sorted_df.iterrows():
    level = "고위험" if row["상승률(mm/년)"] >= 4 else "중위험" if row["상승률(mm/년)"] >= 3 else "저위험"
    st.markdown(f"**{row['지역']}**: {row['상승률(mm/년)']}mm/년 ({level})")

# -------------------------------
# 히트맵 (지역별 상승률)
# -------------------------------
st.subheader("🔥 지역별 상승률 히트맵")
fig, ax = plt.subplots(figsize=(6, 3))
heatmap_data = np.array(sea_level_rise).reshape(2, 3)  # 2행 3열 구조
im = ax.imshow(heatmap_data, cmap="Blues")

# 라벨링
ax.set_xticks(np.arange(3))
ax.set_yticks(np.arange(2))
ax.set_xticklabels(regions[:3])
ax.set_yticklabels(regions[3:])

for i in range(2):
    for j in range(3):
        ax.text(j, i, f"{heatmap_data[i, j]:.1f}", ha="center", va="center", color="black")

st.pyplot(fig)
