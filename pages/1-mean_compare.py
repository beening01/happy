import streamlit as st
import pandas as pd
import plotly.graph_objs as go

from utils.preprocess import load_data

# 데이터 불러오기
df = load_data("districts.csv")

# 인덱스 설정
#df = df.set_index('구분')

# 연도 및 항목 설정
years = ['2020', '2021', '2022', '2023', '2024']
항목목록 = ['소계', '건강상태', '재정상태', '친지관계', '가정생활', '사회생활']
항목_컬럼명 = {
    '소계': '소계',
    '건강상태': '자신의 건강상태',
    '재정상태': '자신의 재정상태',
    '친지관계': '주위 친지 친구와의 관계',
    '가정생활': '가정생활',
    '사회생활': '사회생활'
}

# 자치구 목록
지역목록 = df.index.tolist()

# Streamlit UI
st.title("📍자치구 행복지수 비교")
st.write("✅2020 ~ 2024년도 항목별 평균치")

col1, col2 = st.columns(2)
with col1:
    지역1 = st.selectbox("자치구 1 선택", 지역목록, index=0)
with col2:
    지역2 = st.selectbox("자치구 2 선택", 지역목록, index=1)

# 항목별 5년치 평균 계산 함수
def calc_avg_scores(df, region):
    avg_scores = []
    for 항목 in 항목목록:
        cols = [f"{year}_{항목_컬럼명[항목]}" for year in years]
        # 존재하지 않는 컬럼이 있을 수 있으니 필터링
        cols = [c for c in cols if c in df.columns]
        values = df.loc[region, cols].astype(float)
        avg = values.mean()
        avg_scores.append(avg)
    return avg_scores

# 평균값 계산
r1 = calc_avg_scores(df, 지역1)
r2 = calc_avg_scores(df, 지역2)

# 레이더 차트 그리기
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=r1,
    theta=항목목록,
    fill='toself',
    name=지역1,
    line=dict(color="#55cbcd")
))

fig.add_trace(go.Scatterpolar(
    r=r2,
    theta=항목목록,
    fill='toself',
    name=지역2,
    line=dict(color="#ff968a")
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[2, 8], # 점수 범위
            tickfont=dict(size=10)  # 글자 작게
        )
    ),
    showlegend=True,
    title=f"📌{지역1} vs {지역2} - 항목별 행복지수 평균 비교"
)

st.plotly_chart(fig)
