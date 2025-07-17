import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

df = pd.read_csv('C:/Users/aikyr/Downloads/20년행복지수.csv')
df = df.iloc[2:]
df = df.set_index('구분별(2)')

year_candidates = [col.split('.')[0] for col in df.columns if col.split('.')[0].isdigit()]
years = sorted(list(set(year_candidates)), key=int)
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
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

지역목록 = df.index.tolist()

st.title("시민 행복지수: 소계(ARIMA 예측) / 나머지(막대그래프)")

col1, col2 = st.columns([2, 2])
with col1:
    지역 = st.selectbox('지역을 선택하세요', 지역목록)
with col2:
    항목 = st.radio('항목을 선택하세요', 항목목록, horizontal=True)

display_years = years[-5:]
display_cols = col_map[항목][-5:]
display_y = df.loc[지역, display_cols].values.astype(float)

if 항목 == "소계":
    # 예측 포함 꺾은선 그래프
    y = df.loc[지역, col_map["소계"]].values.astype(float)
    # 결측치 보정
    if np.isnan(y).any():
        y = pd.Series(y).interpolate(method='linear', limit_direction='both').values

    try:
        model = ARIMA(y, order=(1,0,0))
        model_fit = model.fit()
        pred = model_fit.get_forecast(steps=1)
        y_next = pred.predicted_mean[0]
        conf_int = pred.conf_int(alpha=0.05)
        if hasattr(conf_int, "iloc"):
            lower_next, upper_next = conf_int.iloc[0, 0], conf_int.iloc[0, 1]
        else:
            lower_next, upper_next = conf_int[0, 0], conf_int[0, 1]
    except Exception as e:
        st.error(f"ARIMA 예측 실패: {e}")
        y_next, lower_next, upper_next = np.nan, np.nan, np.nan

    display_years_plus = display_years + [str(int(years[-1]) + 1)]
    display_y_all = list(display_y) + [y_next]
    local_y = list(display_y) + [y_next, lower_next, upper_next]
    ymin = min(local_y) - 0.5
    ymax = max(local_y) + 0.5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=display_years_plus, y=display_y_all,
        mode='lines+markers',
        name="소계",
        line=dict(width=2)
    ))
    fig.add_trace(go.Scatter(
        x=[display_years_plus[-1]], y=[y_next],
        mode='markers+text',
        marker=dict(size=13, color='red'),
        text=[f"{display_years_plus[-1]}예측"],
        textposition="top center",
        name=f"{display_years_plus[-1]}년 예측"
    ))
    fig.add_trace(go.Scatter(
        x=[display_years_plus[-1], display_years_plus[-1]], y=[lower_next, upper_next],
        mode='lines',
        line=dict(color='rgba(255,0,0,0.2)', width=14),
        showlegend=True,
        name=f'{display_years_plus[-1]}년 신뢰구간'
    ))
    fig.update_yaxes(range=[ymin, ymax])
    fig.update_layout(
        title=f"{지역} 소계 (최근 5년 + {display_years_plus[-1]}년 ARIMA 예측)",
        xaxis_title="연도",
        yaxis_title=f"소계 점수",
        xaxis=dict(type='category')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"""
    **{지역} 소계 {display_years_plus[-1]}년 예측값 (ARIMA):** {y_next:.2f}
    - 95% 신뢰구간: {lower_next:.2f} ~ {upper_next:.2f}
    """)
else:
    # 예측 없이 막대그래프만
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=display_years,
        y=display_y,
        name=항목,
        marker=dict(color='steelblue')
    ))
    fig.update_layout(
        title=f"{지역} {항목} (최근 5년 막대그래프)",
        xaxis_title="연도",
        yaxis_title=f"{항목} 점수",
        xaxis=dict(type='category')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"""
    **{지역} {항목} 최근 5년 수치:**  
    {', '.join([f"{y}: {v:.2f}" for y, v in zip(display_years, display_y)])}
    """)
