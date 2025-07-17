import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler

from preprocess import load_data

@st.cache_data


# 유사한 지역 추출 함수 (정규화 + 가중치 + 유사도)
def recommend_similar_regions(df, selected_gu, weights, top_n=3, method='cosine'):
    features = ['자신의 건강상태', '자신의 재정상태', '주위 친지 친구와의 관계', '가정생활', '사회생활']
    
    # 1. 피처 정규화 (z-score)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])
    df_scaled = pd.DataFrame(scaled, index=df.index, columns=features)

    # 2. 가중치 적용
    weighted_df = df_scaled.multiply(weights, axis=1)

    # 3. 선택된 구 기준으로 유사도 계산
    selected_vector = weighted_df.loc[selected_gu].values.reshape(1, -1)
    
    if method == 'cosine':
        scores = cosine_similarity(weighted_df, selected_vector).flatten()
        df['similarity'] = scores
        result = df.drop(index=selected_gu).nlargest(top_n, 'similarity')
    else:  # Euclidean distance
        distances = euclidean_distances(weighted_df, selected_vector).flatten()
        df['distance'] = distances
        result = df.drop(index=selected_gu).nsmallest(top_n, 'distance')  # 거리가 작을수록 유사

    return result[[ 'similarity']] if method == 'cosine' else result[['distance']]

# Streamlit UI
st.title("📍서울 행복도 기반 유사 자치구 추천")

# 1. 데이터 불러오기
df = load_data("district_mean.csv")
gus = df.index.tolist()

# 2. 사용자 입력: 자치구 선택
selected_gu = st.selectbox("현재 거주 중인 자치구를 선택하세요:", gus)

# 3. 가중치 입력
st.subheader("당신이 중요하게 생각하는 행복 요소의 중요도를 선택하세요 (1~5점)")
w1 = st.slider("자신의 건강상태", 1, 5, 3)
w2 = st.slider("자신의 재정상태", 1, 5, 3)
w3 = st.slider("주위 친지 친구와의 관계", 1, 5, 3)
w4 = st.slider("가정생활", 1, 5, 3)
w5 = st.slider("사회생활", 1, 5, 3)

raw_weights = [w1, w2, w3, w4, w5]
weight_sum = sum(raw_weights)
weights = [w / weight_sum for w in raw_weights]

# 4. 유사도 방식 선택
method = st.radio("유사도 계산 방식", ["코사인 유사도", "유클리디안 거리"])
sim_method = 'cosine' if method == "코사인 유사도" else 'euclidean'

# 5. 결과 출력
if st.button("유사한 지역 추천받기"):
    result = recommend_similar_regions(df.copy(), selected_gu, weights, method=sim_method)
    st.subheader(f"🏙️ '{selected_gu}'와 유사한 지역 Top 3")
    st.table(result)

    # ✅ Plotly 시각화 추가
    st.subheader("📊 행복 요소별 점수 비교 (인터랙티브 그래프)")

    # 시각화를 위한 데이터 준비
    compare_gus = [selected_gu] + result.index.tolist()
    features = ['자신의 건강상태', '자신의 재정상태', '주위 친지 친구와의 관계', '가정생활', '사회생활']
    compare_df = df.loc[compare_gus, features]

    # 데이터 형태를 Plotly용 long-format으로 변환
    df_melted = compare_df.reset_index().melt(id_vars='index', value_vars=features,
                                              var_name='행복 요소', value_name='점수')
    df_melted.rename(columns={'index': '자치구'}, inplace=True)

    # Plotly 그래프 생성
    fig = px.bar(df_melted,
                 x='행복 요소',
                 y='점수',
                 color='자치구',
                 barmode='group',
                 text='점수',
                 height=500,
                 title=f"{selected_gu}와 유사한 자치구의 행복 요소 비교")

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    st.plotly_chart(fig, use_container_width=True)

    

