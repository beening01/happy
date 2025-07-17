import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 데이터 읽기
df = pd.read_csv('C:/Users/JIHYEON/Downloads/distrits.csv')

# 자치구명을 인덱스로 설정
df = df.set_index('구분')

# 연도 및 항목 정의
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

# 데이터 타입 변환
for 항목 in 항목목록:
    for year in years:
        col_name = f"{year}_{항목_컬럼명[항목]}"
        if col_name in df.columns:
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')

# 자치구 리스트
지역목록 = df.index.tolist()

# Streamlit UI
st.title("두 자치구의 항목별 연도별 비교 시각화")

col1, col2 = st.columns(2)
with col1:
    지역1 = st.selectbox("자치구 1 선택", 지역목록, index=0)
with col2:
    지역2 = st.selectbox("자치구 2 선택", 지역목록, index=1)

항목 = st.radio("비교할 항목 선택", 항목목록, horizontal=True)

# 그래프 데이터 생성
x = []
y1 = []
y2 = []

for year in years:
    col_name = f"{year}_{항목_컬럼명[항목]}"
    if col_name in df.columns:
        x.append(year)
        y1.append(df.loc[지역1, col_name])
        y2.append(df.loc[지역2, col_name])

# 그래프 그리기
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y1,
    mode='lines+markers',
    name=지역1,
    line=dict(width=2, color='blue')
))

fig.add_trace(go.Scatter(
    x=x, y=y2,
    mode='lines+markers',
    name=지역2,
    line=dict(width=2, color='green')
))

fig.update_layout(
    title=f"{지역1} vs {지역2} - '{항목}' 항목 연도별 비교",
    xaxis_title="연도",
    yaxis_title=f"{항목} 점수",
    xaxis=dict(type='category'),
    yaxis=dict(rangemode='tozero'),
    legend=dict(x=1.02, y=1.0, xanchor='left', yanchor='top',
    bgcolor='rgba(255,255,255,0.8)',   # 반투명 흰 배경
    bordercolor='black', borderwidth=1)
)

st.plotly_chart(fig, use_container_width=True)

