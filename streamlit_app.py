import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="기후안정 프로젝트 대시보드", layout="wide")

# -------------------------------
# 공개 데이터 로드
# -------------------------------
@st.cache_data
def load_temperature_data():
    # 예시: 기상청 Open MET Data Portal에서 '기온 통계' CSV 다운로드 후 사용
    # 예: 서울 계절별 평균기온, 전국 평균 기온 등
    # 실제 URL로 바꿔주세요
    url = "https://data.kma.go.kr/path/to/seasonal_temperature_Korea.csv"
    try:
        df = pd.read_csv(url)
        # 컬럼 예: year, region, season, avg_temp
        # 전처리
        df = df.dropna(subset=["year", "avg_temp", "region", "season"])
        df["year"] = df["year"].astype(int)
        return df
    except Exception:
        # 실패 시 더미 예시 데이터
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
    # 예시: Our World in Data 또는 Macrotrends / World Bank에서 한국 온실가스 배출량 연도별 데이터
    # 실제 URL 교체
    url = "https://ourworldindata.org/path/to/south_korea_ghg_emissions.csv"
    try:
        df = pd.read_csv(url)
        # 컬럼 예: year, emissions (kt CO2 eq)
        df = df.dropna(subset=["year","emissions"])
        df["year"] = df["year"].astype(int)
        return df
    except Exception:
        # 실패 시 더미 데이터
        years = list(range(1990, 2021))
        emissions = np.linspace(400000, 700000, len(years)) + np.random.normal(0,20000, len(years))
        return pd.DataFrame({"year": years, "emissions": emissions})

# -------------------------------
# 데이터 준비
# -------------------------------
df_temp = load_temperature_data()
df_emission = load_emission_data()

# -------------------------------
# 사이드바 옵션
# -------------------------------
st.sidebar.header("📊 데이터 옵션")

categories = st.sidebar.multiselect(
    "보고 싶은 데이터 카테고리 선택",
    ["계절별 평균기온", "온실가스 배출량"],
    default=["계절별 평균기온", "온실가스 배출량"]
)

year_range = st.sidebar.slider(
    "기간 선택",
    min_value=int(df_temp["year"].min()), max_value=int(df_temp["year"].max()),
    value=(2000, df_temp["year"].max())
)

show_markers = st.sidebar.checkbox("마커 표시", True)

region_select = st.sidebar.selectbox("지역 선택 (상세 분석)", df_temp["region"].unique().tolist())

# -------------------------------
# 본문 레이아웃
# -------------------------------
st.title("🌍 기후안정 프로젝트 대시보드")
st.write(f"선택된 기간: {year_range[0]}년 ~ {year_range[1]}년")

# -------------------------------
# (1) 계절별 평균기온 변화
# -------------------------------
if "계절별 평균기온" in categories:
    st.subheader("📈 계절별 평균기온 변화")
    # 전국/모든 지역 평균
    df_temp_filtered = df_temp[(df_temp["year"] >= year_range[0]) & (df_temp["year"] <= year_range[1])]
    fig = px.line(
        df_temp_filtered.groupby(["year","season"])["avg_temp"].mean().reset_index(),
        x="year", y="avg_temp", color="season",
        markers=show_markers,
        labels={"avg_temp":"평균기온 (℃)", "year":"연도", "season":"계절"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 지역별 상세 분석: 선택된 지역
    st.subheader(f"📍 {region_select} 평균기온 변화 (계절별)")
    df_reg = df_temp_filtered[df_temp_filtered["region"] == region_select]
    fig_reg = px.line(
        df_reg, x="year", y="avg_temp", color="season",
        markers=show_markers,
        labels={"avg_temp":"평균기온 (℃)", "year":"연도", "season":"계절"}
    )
    st.plotly_chart(fig_reg, use_container_width=True)

# -------------------------------
# (2) 온실가스 배출량 변화
# -------------------------------
if "온실가스 배출량" in categories:
    st.subheader("🧪 한국 온실가스 배출량 변화 (CO₂ 환산)")
    df_em = df_emission[(df_emission["year"] >= year_range[0]) & (df_emission["year"] <= year_range[1])]
    fig_em = px.line(
        df_em, x="year", y="emissions",
        markers=show_markers,
        labels={"emissions":"배출량 (kt CO₂ equivalent)", "year":"연도"}
    )
    st.plotly_chart(fig_em, use_container_width=True)

# -------------------------------
# (3) 해결방안 & 실천 과제
# -------------------------------
st.subheader("✅ 해결방안과 실천 과제")
st.markdown("""
- **개인 차원**:  
  - 대중교통 및 자전거/도보 이용  
  - 전기 절약 (불필요한 전등/가전 OFF)  
  - 생활 속 에너지 효율 제품 사용  
  - 식습관 개선 (육류 섭취 줄이기, 지역식 중심)

- **학교 차원**:  
  - 교실 냉·난방 온도 관리  
  - 창의적 에너지 절약 캠페인 운영  
  - 기후 동아리 활동 활성화 및 공유 발표  
  - 학교 시설의 신재생에너지 도입 검토

- **사회 / 정책 차원**:  
  - 탄소중립 목표 강화 및 법제화  
  - 재생에너지 확대 및 화석연료 감축 정책  
  - 산업 배출 조절 및 기술 혁신 지원  
  - 이상기후 대응 및 취약 지역 보호를 위한 정책

""")

# -------------------------------
# 출처 표시
# -------------------------------
st.markdown("---")
st.markdown("**데이터 출처**:")
st.markdown(f"- 기상청 Open MET Data Portal (기온 통계) :contentReference[oaicite:0]{index=0}")
st.markdown(f"- Our World in Data: 한국 온실가스 배출량 데이터 :contentReference[oaicite:1]{index=1}")
