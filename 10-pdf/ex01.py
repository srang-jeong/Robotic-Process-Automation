from PyPDF2 import PdfReader

# py -m pip install PyPDF2

reader = PdfReader("./10-pdf/sample.pdf")
print(reader.pages[0].extract_text())
# 테스트용 PDF
# 1