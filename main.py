import streamlit as st

st.set_page_config(
    page_title="My Happy Place",
    page_icon="😊",
    layout="wide"
)

st.title("My Happy Place 🏙️")
st.markdown("서울 자치구별 행복도 데이터를 기반으로, 다양한 시각화와 추천 기능을 제공합니다.")

st.subheader("📌 사용 가능한 기능")
st.markdown("- ✅ 지역별 행복지수 변화: '2020 ~ 2024'년도별 변화")
st.markdown("- ✅ 자치구 행복지수 비교: 원하는 2개 자치구 비교")
st.markdown("- ✅ 서울 자치구 추천: 나의 행복 가치관에 맞는 자치구 추천")

st.info("왼쪽 상단 메뉴에서 원하는 기능을 선택하세요.")


with st.expander(":📄프로젝트 제작자 정보 보기"):
    st.markdown("""
    - **프로젝트명:** My Happy Place
    - **제작자:** 김영래, 이지현, 이한빈
    - **소속:** 우리FISA 5기 AI 엔지니어링
    - **프로젝트 기간:** 2025년 7월 16일 ~ 2025년 7월 17일
    - **GitHub:** [github.com/team-happyplace](https://github.com/beening01/happy.git)
    """)