import streamlit as st

st.set_page_config(
    page_title="My Happy Place",
    page_icon="😊",
    layout="wide"
)

st.title("My Happy Place 🏙️")
st.markdown("서울 자치구별 행복도 데이터를 기반으로, 다양한 시각화와 추천 기능을 제공합니다.")

st.subheader("📌 사용 가능한 기능")
st.markdown("- ✅ 시계열 비교: ")
st.markdown("- ✅ 행복지수 비교: ")
st.markdown("- ✅ 서울 자치구 추천: 나의 행복 가치관에 맞는 자치구 추천")

st.info("왼쪽 상단 메뉴에서 원하는 기능을 선택하세요.")