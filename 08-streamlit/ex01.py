'''
1. Streamlit 소개 및 설치
Streamlit이란?

파이썬으로 빠르게 웹 애플리케이션을 만들 수 있는 오픈소스 프레임워크
데이터 과학자와 머신러닝 엔지니어를 위한 도구
HTML, CSS, JavaScript 지식 없이도 웹 앱 개발 가능

설치 방법
py -m pip install streamlit

실행 방법
streamlit run app.py

공식 사이트
https://docs.streamlit.io/develop/api-reference

'''

import streamlit as st

# 제목 설정
st.title("내 첫 번째 Streamlit 앱")  # h1

# 텍스트 출력
st.write("안녕하세요! Streamlit에 오신 것을 환영합니다.") # text

# 간단한 계산
number = st.number_input("숫자를 입력하세요", value=0)
st.write(f"입력한 숫자의 제곱: {number ** 2}")