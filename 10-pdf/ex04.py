from PyPDF2 import PdfReader, PdfWriter

# 1. 기존 PDF 파일 열기
reader = PdfReader("./10-pdf/sample.pdf")  # 암호를 걸고 싶은 기존 PDF 파일

# 2. PdfWriter 객체 생성
writer = PdfWriter()

# 3. 모든 페이지 복사
for page in reader.pages:
    writer.add_page(page)

# 4. 암호 설정 (읽을 때 필요한 비밀번호)
writer.encrypt("password123")

# 5. 암호화된 새 PDF 파일 저장
with open("./10-pdf/encrypted_sample.pdf", "wb") as f:
    writer.write(f)

print("암호화된 PDF 파일이 저장되었습니다.")
