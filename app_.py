import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats

# 데이터 읽기
df = pd.read_csv('C:/Users/JIHYEON/Downloads/exdata.csv')
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

# 데이터타입 변환
for 항목 in 항목목록:
    for c in col_map[항목]:
        df[c] = pd.to_numeric(df[c], errors='coerce')

지역목록 = df.index.tolist()

st.title("지역별 행복지수 시계열 및 2025년 예측 (신뢰구간 포함)")

col1, col2 = st.columns([2, 2])
with col1:
    지역 = st.selectbox('지역을 선택하세요', 지역목록)
with col2:
    항목 = st.radio('항목을 선택하세요', 항목목록, horizontal=True)

# 선택 항목 데이터
x = np.array([2020, 2021, 2022, 2023, 2024]).reshape(-1, 1)
y = df.loc[지역, col_map[항목]].values.astype(float)
model = LinearRegression().fit(x, y)
y_pred = model.predict(x)
y_2025 = model.predict([[2025]])[0]
n = len(x)
x_mean = np.mean(x)
t_value = stats.t.ppf(0.975, df=n-2)
s_err = np.sqrt(np.sum((y - y_pred) ** 2) / (n - 2))
conf = t_value * s_err * np.sqrt(1 + 1/n + ((2025 - x_mean)**2) / np.sum((x - x_mean)**2))
lower_2025 = y_2025 - conf
upper_2025 = y_2025 + conf

years_plus = years + ['2025']
y_all = list(y) + [y_2025]

# y축 범위는 선택된 지역·항목+예측+신뢰구간만 반영 (자동)
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
    title=f"{지역} {항목} 시계열 (2025 예측, 신뢰구간 포함)",
    xaxis_title="연도",
    yaxis_title=f"{항목} 점수",
    xaxis=dict(type='category')
)

st.plotly_chart(fig, use_container_width=True)

st.info(f"""
**{지역} {항목} 2025년 예측값:** {y_2025:.2f}
- 95% 신뢰구간: {lower_2025:.2f} ~ {upper_2025:.2f}
""")