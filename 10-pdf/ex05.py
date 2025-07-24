from PyPDF2 import PdfReader

# 1. 암호화된 PDF 파일 열기
reader = PdfReader("./10-pdf/encrypted_sample.pdf")

# 2. 비밀번호 입력 (정확히 입력해야 함)
if reader.is_encrypted:
    reader.decrypt("password123")

# 3. 첫 페이지 텍스트 추출
page = reader.pages[0]
text = page.extract_text()

print("추출된 텍스트:")
print(text)
