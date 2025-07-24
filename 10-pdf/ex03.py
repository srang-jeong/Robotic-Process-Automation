from PyPDF2 import PdfMerger

# PDF파일 2개를 병합하여 출력하기

merger = PdfMerger()
merger.append("./10-pdf/sample.pdf")
merger.append("./10-pdf/sample2.pdf")
merger.write("./10-pdf/merged.pdf")
merger.close()