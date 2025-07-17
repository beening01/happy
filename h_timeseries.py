import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# 파일 읽기
df = pd.read_csv('C:/Users/aikyr/Downloads/distrits.csv')
df = df.set_index('구분')

# 컬럼명 매팡
label_map = {
    "소계": "소계",
    "자신의 건강상태": "건강",
    "자신의 재정상태": "재정",
    "주위 친지 친구와의 관계": "친지",
    "가정생활": "가정",
    "사회생활": "사회"
}

# 모든 연도-항목 분리
all_columns = df.columns.tolist()
years = sorted({col.split('_')[0] for col in all_columns if '_' in col})
raw_항목목록 = {col.split('_', 1)[1] for col in all_columns if '_' in col}
항목목록_2글자 = [label_map.get(h, h[:2]) for h in sorted(list(raw_항목목록))]

# 선택을 위한 역매핑
reverse_label_map = {label_map.get(k, k[:2]): k for k in raw_항목목록}

st.title("지역별 행복지수 변화")

col1, col2 = st.columns([2, 2])
with col1:
    지역 = st.selectbox('지역을 선택하세요', df.index.tolist())
with col2:
    선택항목_2글자 = st.multiselect('항목(복수) 선택', 항목목록_2글자, default=항목목록_2글자)

st.markdown("#### [1] 지역별 행복지수 변화(꺾은선그래프)")
fig = go.Figure()

for 항목2 in 선택항목_2글자:
    # 실제 데이터에 있는 "원본 항목명"을 가져와서 매칭
    원본항목 = reverse_label_map[항목2]
    y값 = []
    for y in years:
        colname = f"{y}_{원본항목}"
        if colname in df.columns:
            y값.append(df.loc[지역, colname])
        else:
            y값.append(None)
    fig.add_trace(go.Scatter(
        x=[str(y) for y in years],
        y=y값,
        mode='lines+markers',
        name=항목2
    ))

fig.update_layout(
    xaxis_title="",
    yaxis_title="행복지수",
    legend_title="항목",
    title=f"{지역}",
    xaxis=dict(type='category')
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### [2] 최근년도 항목별 지수 (막대그래프)")
y2024_cols = [c for c in df.columns if c.startswith('2024_')]
y2024_labels_long = [c.split('_', 1)[1] for c in y2024_cols]
y2024_labels = [label_map.get(l, l[:2]) for l in y2024_labels_long]
y2024_vals = [df.loc[지역, c] for c in y2024_cols]



# 최고/최저값 인덱스 찾기
max_idx = y2024_vals.index(max(y2024_vals))
min_idx = y2024_vals.index(min(y2024_vals))

# 색상 리스트 만들기
colors = []
for i in range(len(y2024_vals)):
    if i == max_idx:
        colors.append('red')
    elif i == min_idx:
        colors.append('blue')
    else:
        colors.append('lightgray')

# 막대그래프 그리기
fig2 = go.Figure(go.Bar(
    x=y2024_labels,
    y=y2024_vals,
    marker_color=colors,
    text=[round(v,2) for v in y2024_vals],
    textposition='outside'
))

fig2.update_layout(margin=dict(t=50, b=50, l=50, r=50),
    xaxis_title="항목",
    yaxis_title="행복지수",
    title=f"{지역} - 항목별 행복지수"
)
st.plotly_chart(fig2, use_container_width=True)

styled_df = pd.DataFrame({
    "항목": y2024_labels,
    "2024년 행복지수": [round(v, 2) for v in y2024_vals]
})

st.dataframe(styled_df, hide_index=True, use_container_width=True)

