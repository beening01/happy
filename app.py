import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

df = pd.read_csv('C:/Users/aikyr/Downloads/5개년시민행복지수.csv')
df = df.iloc[2:]
df = df.set_index('구분별(2)')

years = ['2020', '2021', '2022', '2023', '2024']
항목목록 = ['소계', '건강', '재정', '친지관계', '가정생활', '사회생활']
col_map = {
    '소계': [y for y in years],
    '건강': [f"{y}.1" for y in years],
    '재정': [f"{y}.2" for y in years],
    '친지관계': [f"{y}.3" for y in years],
    '가정생활': [f"{y}.4" for y in years],
    '사회생활': [f"{y}.5" for y in years]
}
for 항목 in 항목목록:
    for c in col_map[항목]:
        df[c] = pd.to_numeric(df[c], errors='coerce')

지역목록 = df.index.tolist()

st.title("ARIMA 시계열 예측 기반 행복지수 (2025년 포함)")

col1, col2 = st.columns([2, 2])
with col1:
    지역 = st.selectbox('지역을 선택하세요', 지역목록)
with col2:
    항목 = st.radio('항목을 선택하세요', 항목목록, horizontal=True)

y = df.loc[지역, col_map[항목]].values.astype(float)
index_years = [int(y) for y in years]

# ARIMA(1,1,0) 또는 (1,0,0) 등 여러 옵션 중 테스트, 아래는 (1,1,0)로 고정
try:
    model = ARIMA(y, order=(0,0,0))
    model_fit = model.fit()
    # 2025년까지 예측 (5번째가 2024, 6번째가 2025)
    pred = model_fit.get_forecast(steps=1)
    y_2025 = pred.predicted_mean[0]
    conf_int = pred.conf_int(alpha=0.05)
    lower_2025, upper_2025 = conf_int.iloc[0, 0], conf_int.iloc[0, 1]
except Exception as e:
    y_2025, lower_2025, upper_2025 = np.nan, np.nan, np.nan

years_plus = years + ['2025']
y_all = list(y) + [y_2025]
local_y = list(y) + [y_2025, lower_2025, upper_2025]
ymin = min(local_y) - 0.5
ymax = max(local_y) + 0.5

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years_plus, y=y_all,
    mode='lines+markers',
    name=항목,
    line=dict(width=2)
))


fig.add_trace(go.Scatter(
    x=['2025'], y=[y_2025],
    mode='markers+text',
    marker=dict(size=13, color='red'),
    text=["2025예측"],
    textposition="top center",
    name="2025년 예측"
))

# 신뢰구간 밴드
fig.add_trace(go.Scatter(
    x=['2025', '2025'], y=[lower_2025, upper_2025],
    mode='lines',
    line=dict(color='rgba(255,0,0,0.2)', width=14),
    showlegend=True,
    name='2025년 신뢰구간'
))

fig.update_yaxes(range=[ymin, ymax])
fig.update_layout(
    title=f"{지역} {항목} (ARIMA 기반 2025 예측, 신뢰구간 포함)",
    xaxis_title="연도",
    yaxis_title=f"{항목} 점수",
    xaxis=dict(type='category')
)

st.plotly_chart(fig, use_container_width=True)

st.info(f"""
**{지역} {항목} 2025년 예측값 (ARIMA):** {y_2025:.2f}
- 95% 신뢰구간: {lower_2025:.2f} ~ {upper_2025:.2f}
""")