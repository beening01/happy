
import pandas as pd
import plotly.express as px

from utils.preprocess import load_data

# 데이터 로드
df = load_data("districts.csv")

# melt로 변환
df_melted = df.reset_index().melt(id_vars='구분', 
                                  var_name='행복요소', 
                                  value_name='점수')
df_melted.rename(columns={'구분': '자치구'}, inplace=True)

# Heatmap
fig = px.density_heatmap(
    df_melted,
    x="행복요소",
    y="자치구",
    z="점수",
    color_continuous_scale="YlGnBu",  # 또는 Viridis, Blues, etc.
    title="자치구별 행복 항목 점수 Heatmap",
    height=800
)
fig.update_layout(xaxis_title="행복 항목", yaxis_title="자치구")
# fig.show()

