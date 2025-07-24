import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 데이터 처리 도구")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_csv(uploaded_file)
    
    st.subheader("원본 데이터")
    st.dataframe(df, use_container_width=True)
    
    # 데이터 정보
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("행 수", len(df))
    with col2:
        st.metric("열 수", len(df.columns))
    with col3:
        st.metric("결측값", df.isnull().sum().sum())
    
    # 데이터 처리 옵션
    st.subheader("데이터 처리 옵션")
    
    processing_options = st.multiselect(
        "처리할 작업을 선택하세요",
        ["결측값 제거", "중복값 제거", "숫자 컬럼만 선택", "정규화"]
    )
    
    processed_df = df.copy()
    
    if "결측값 제거" in processing_options:
        processed_df = processed_df.dropna()
        st.info("결측값이 제거되었습니다.")
    
    if "중복값 제거" in processing_options:
        processed_df = processed_df.drop_duplicates()
        st.info("중복값이 제거되었습니다.")
    
    if "숫자 컬럼만 선택" in processing_options:
        processed_df = processed_df.select_dtypes(include=[np.number])
        st.info("숫자 컬럼만 선택되었습니다.")
    
    if "정규화" in processing_options:
        numeric_columns = processed_df.select_dtypes(include=[np.number]).columns
        processed_df[numeric_columns] = (processed_df[numeric_columns] - processed_df[numeric_columns].mean()) / processed_df[numeric_columns].std()
        st.info("숫자 데이터가 정규화되었습니다.")
    
    if processing_options:
        st.subheader("처리된 데이터")
        st.dataframe(processed_df, use_container_width=True)
        
        # 처리된 데이터 다운로드
        csv = processed_df.to_csv(index=False)
        st.download_button(
            label="처리된 데이터 다운로드",
            data=csv,
            file_name='processed_data.csv',
            mime='text/csv'
        )
    
    # 기본 통계
    if not processed_df.empty:
        st.subheader("데이터 요약 통계")
        st.dataframe(processed_df.describe(), use_container_width=True)

else:
    st.info("CSV 파일을 업로드하여 시작하세요!")