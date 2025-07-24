import streamlit as st
import pandas as pd
import numpy as np

# py -m pip install numpy

# 데이터프레임 생성
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '정지은'],
    '나이': [25, 30, 35, 28],
    '점수': [85, 92, 78, 88]
})

# 데이터프레임 표시
st.dataframe(df)

# 테이블 표시
st.table(df)

# 메트릭 표시
st.metric("평균 점수", f"{df['점수'].mean():.1f}", delta="2.3")