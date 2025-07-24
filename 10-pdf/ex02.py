# 특정 페이지만 추출해서 새 PDF로 저장

from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("./10-pdf/sample.pdf")
writer = PdfWriter()
writer.add_page(reader.pages[2])  # 3번째 페이지

with open("./10-pdf/page3_only.pdf", "wb") as f:
    writer.write(f)
