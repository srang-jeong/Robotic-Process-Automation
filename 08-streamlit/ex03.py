import streamlit as st

# 텍스트 입력
name = st.text_input("이름을 입력하세요")
if name:
    st.write(f"안녕하세요, {name}님!")

# 텍스트 영역
message = st.text_area("메시지를 입력하세요", height=100)
if message:
    st.write(f"입력한 메시지: {message}")
    
# 숫자 입력
age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, value=25)
st.write(f"입력한 나이: {age}세")

# 슬라이더
score = st.slider("점수를 선택하세요", min_value=0, max_value=100, value=50)
st.write(f"선택한 점수: {score}점")

# 셀렉트박스
city = st.selectbox("도시를 선택하세요", ["서울", "부산", "대구", "인천", "광주"])
st.write(f"선택한 도시: {city}")

# 멀티셀렉트
hobbies = st.multiselect("취미를 선택하세요", ["독서", "영화감상", "운동", "게임", "요리"])
if hobbies:
    st.write(f"선택한 취미: {', '.join(hobbies)}")

# 라디오 버튼
gender = st.radio("성별을 선택하세요", ["남성", "여성", "기타"])
st.write(f"선택한 성별: {gender}")

# 체크박스
agree = st.checkbox("이용약관에 동의합니다")
if agree:
    st.write("동의해주셔서 감사합니다!")