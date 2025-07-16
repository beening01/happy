import streamlit as st


ani_list = ['짱구는못말려', '몬스터','릭앤모티']
img_list = ['https://i.imgur.com/t2ewhfH.png', 
            'https://i.imgur.com/ECROFMC.png', 
            'https://i.imgur.com/MDKQoDc.jpg']

# 텍스트를 입력받아서 해당 텍스트와 일치하는 이미지를 화면에 출력하는 검색창을 만들어 주세요.

ani_name = st.text_input("애니메이션 이름을 입력해주세요")


if ani_name:
   for ani in ani_list:
      if ani_name in ani:
        st.image(img_list[ani_list.index(ani)])


# 변화가 많은 데이터를 사용할 때는 변수의 변화에 따라 코드도 변화될 수 있도록
# range(3) 하드코딩 변수명, 숫자로 지정하는 것 -> 데이터가 많아지거나 추가되면 수정 힘듦