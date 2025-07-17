import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 데이터 읽기
df = pd.read_csv('C:/Users/JIHYEON/Downloads/distrits.csv')
df = df.set_index('구분')

# 항목 정보
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
st.title("2024년 항목별 행복지수 레이더 차트 비교")

col1, col2 = st.columns(2)
with col1:
    지역1 = st.selectbox("자치구 1 선택", 지역목록, index=0)
with col2:
    지역2 = st.selectbox("자치구 2 선택", 지역목록, index=1)

# 2024년 항목별 점수 추출
r1 = [df.loc[지역1, f"2024_{항목_컬럼명[항목]}"] for 항목 in 항목목록]
r2 = [df.loc[지역2, f"2024_{항목_컬럼명[항목]}"] for 항목 in 항목목록]

# 레이더 차트 그리기
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=r1,
    theta=항목목록,
    fill='toself',
    name=지역1,
    line=dict(color='blue')
))

fig.add_trace(go.Scatterpolar(
    r=r2,
    theta=항목목록,
    fill='toself',
    name=지역2,
    line=dict(color='red')
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 8])  # 점수 0~8 기준
    ),
    showlegend=True,
    title=f"{지역1} vs {지역2} - 2024년 항목별 행복지수 비교 (레이더 차트)"
)

st.plotly_chart(fig)