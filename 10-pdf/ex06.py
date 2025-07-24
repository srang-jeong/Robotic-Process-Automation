from PyPDF2 import PdfReader

# 1. PDF 파일 열기
reader = PdfReader("./10-pdf/sample.pdf")

# 2. 메타데이터 가져오기
metadata = reader.metadata

# 3. 메타데이터 출력
print("📄 PDF 메타데이터:")
for key, value in metadata.items():
    print(f"{key}: {value}")
