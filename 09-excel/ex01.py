"""
성적표.xlsx 파일 읽기 프로그램
pandas를 사용하여 엑셀 파일을 DataFrame으로 읽어옵니다.
"""

# py -m pip install openpyxl

import pandas as pd
import os

def read_excel_file():
    """성적표.xlsx 파일을 DataFrame으로 읽어서 출력"""
    
    file_name = "./09-excel/성적표.xlsx"
    
    # 파일 존재 확인
    if not os.path.exists(file_name):
        print(f"❌ {file_name} 파일을 찾을 수 없습니다.")
        return
    
    try:
        # 엑셀 파일을 DataFrame으로 읽기
        df = pd.read_excel(file_name)
        
        print("=" * 50)
        print("📊 성적표 내용 (DataFrame)")
        print("=" * 50)
        
        # DataFrame 전체 출력
        print(df)
        
        print("\n" + "=" * 50)
        print("📈 기본 정보")
        print("=" * 50)
        
        # DataFrame 기본 정보
        print(f"📋 행 수: {len(df)}개")
        print(f"📋 열 수: {len(df.columns)}개")
        print(f"📋 컬럼명: {list(df.columns)}")
        
        print("\n📊 기본 통계:")
        print(df.describe())
        
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")

if __name__ == "__main__":
    print("📊 Excel 파일 읽기 (pandas DataFrame)")
    print("=" * 40)
    
    # pandas 설치 확인
    try:
        import pandas as pd
    except ImportError:
        print("❌ pandas 패키지가 설치되어 있지 않습니다.")
        print("다음 명령어로 설치하세요:")
        print("pip install pandas openpyxl")
        exit(1)
    
    read_excel_file()
