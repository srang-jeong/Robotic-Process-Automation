# proj01.py

"""
맞춤형 수료증/인증서 대량 발급기

프로젝트 설명: 교육 과정 수료생 명단(Excel)을 읽어와, 각 개인의 이름과 수료 과정명이 포함된 맞춤형 수료증(PDF)을 대량으로 생성하고, 
각 수료생에게 이메일로 자동 발송합니다.

주요 활용 기술:
pandas: 수료생 명단 데이터 관리
Pillow, ReportLab: 이미지나 템플릿 위에 텍스트를 입혀 PDF 수료증 생성
smtplib: 개인별 맞춤 이메일 및 PDF 첨부파일 발송

"""

import pandas as pd
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
from dotenv import load_dotenv

# py -m pip install reportlab

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

load_dotenv()

class CertificateGenerator:
    def __init__(self):
        self.output_dir = "certificates"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def register_font(self):
        """한글 폰트 등록"""
        fonts = ["C:/Windows/Fonts/malgun.ttf", "./fonts/NanumGothic.ttf"]
        for font_path in fonts:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('Korean', font_path))
                    return True
                except:
                    continue
        return False
    
    def create_pdf(self, name, course_name, completion_date, cert_id):
        if not REPORTLAB_OK:
            return None
        
        has_korean = self.register_font()
        font = "Korean" if has_korean else "Helvetica"
        bold_font = "Korean" if has_korean else "Helvetica-Bold"
        
        filename = f"{self.output_dir}/수료증_{name}_{cert_id}.pdf"
        
        try:
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            
            # 배경 및 테두리
            c.setFillColorRGB(0.95, 0.95, 0.95)
            c.rect(0, 0, width, height, fill=1)
            c.setStrokeColorRGB(0.2, 0.2, 0.8)
            c.setLineWidth(3)
            c.rect(50, 50, width-100, height-100, fill=0)
            
            # 제목
            c.setFillColorRGB(0.1, 0.1, 0.6)
            c.setFont(bold_font, 36)
            title = "수 료 증"
            c.drawString((width - c.stringWidth(title, bold_font, 36)) / 2, height - 150, title)
            
            # 영문 제목
            c.setFont("Helvetica", 16)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            eng_title = "Certificate of Completion"
            c.drawString((width - c.stringWidth(eng_title, "Helvetica", 16)) / 2, height - 180, eng_title)
            
            # 이름
            c.setFillColorRGB(0.8, 0.2, 0.2)
            c.setFont(bold_font, 32)
            name_text = f"{name} 님"
            c.drawString((width - c.stringWidth(name_text, bold_font, 32)) / 2, height - 280, name_text)
            
            # 과정명
            c.setFillColorRGB(0.1, 0.1, 0.1)
            c.setFont(font, 18)
            course_text = f"『 {course_name} 』"
            c.drawString((width - c.stringWidth(course_text, font, 18)) / 2, height - 320, course_text)
            
            # 내용
            c.setFont(font, 14)
            completion_text = "위 과정을 성실히 이수하였기에 이를 증명합니다."
            c.drawString((width - c.stringWidth(completion_text, font, 14)) / 2, height - 360, completion_text)
            
            # 날짜
            c.setFont(bold_font, 16)
            c.setFillColorRGB(0.2, 0.2, 0.2)
            date_text = f"수료일: {completion_date}"
            c.drawString((width - c.stringWidth(date_text, bold_font, 16)) / 2, height - 420, date_text)
            
            # 발급기관
            c.setFont(font, 12)
            c.setFillColorRGB(0.4, 0.4, 0.4)
            org_text = "파이썬 교육원"
            c.drawString((width - c.stringWidth(org_text, font, 12)) / 2, height - 480, org_text)
            
            # 발급일
            today = datetime.now().strftime("%Y년 %m월 %d일")
            issue_text = f"발급일: {today}"
            c.drawString((width - c.stringWidth(issue_text, font, 10)) / 2, height - 520, issue_text)
            
            # 인증번호
            cert_text = f"인증번호: {cert_id}"
            c.drawString((width - c.stringWidth(cert_text, font, 10)) / 2, height - 540, cert_text)
            
            c.save()
            return filename
        except Exception as e:
            print(f"❌ PDF 생성 실패: {e}")
            return None

class EmailSender:
    def __init__(self):
        self.email = os.getenv('GMAIL_EMAIL')
        self.password = os.getenv('GMAIL_APP_PASSWORD')
    
    def get_safe_filename(self, name):
        """안전한 파일명 생성"""
        mapping = {
            '김철수': 'Kim_Cheolsu', '이영희': 'Lee_Younghee', 
            '박민수': 'Park_Minsu', '정다영': 'Jung_Dayoung', '최준호': 'Choi_Junho'
        }
        return f"Certificate_{mapping.get(name, 'Student')}.pdf"
    
    def send_email(self, to_email, name, course_name, pdf_path):
        if not self.email or not self.password:
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = f"🎓 [{course_name}] 수료증 발급 - {name}님"
            
            body = f"""안녕하세요 {name}님,

『{course_name}』 과정 수료를 축하드립니다! 🎉

수료증을 첨부파일로 보내드립니다.

감사합니다.
파이썬 교육원"""
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # PDF 첨부
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    safe_filename = self.get_safe_filename(name)
                    part = MIMEApplication(f.read(), _subtype='pdf')
                    part.add_header('Content-Disposition', f'attachment; filename="{safe_filename}"')
                    msg.attach(part)
            
            # 발송
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_email, msg.as_string())
            server.quit()
            
            print(f"✅ 발송완료: {name}님")
            return True
        except Exception as e:
            print(f"❌ 발송실패: {name}님 - {e}")
            return False

class CertificateManager:
    def __init__(self):
        self.generator = CertificateGenerator()
        self.sender = EmailSender()
    
    def read_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            required = ['이름', '이메일', '과정명', '수료일']
            if not all(col in df.columns for col in required):
                print(f"❌ 필수 컬럼 누락: {required}")
                return None
            return df.dropna(subset=required)
        except Exception as e:
            print(f"❌ Excel 읽기 실패: {e}")
            return None
    
    def generate_id(self, name, course):
        import hashlib
        data = f"{name}_{course}_{datetime.now().strftime('%Y%m%d')}"
        return hashlib.md5(data.encode()).hexdigest()[:8].upper()
    
    def process(self, excel_file):
        print("🎓 수료증 대량 발급 시작")
        
        df = self.read_excel(excel_file)
        if df is None:
            return
        
        print(f"📋 처리 대상: {len(df)}명")
        success = 0
        
        for _, row in df.iterrows():
            name = row['이름']
            email = row['이메일']
            course = row['과정명']
            date = row['수료일']
            
            print(f"📝 처리중: {name}님")
            
            cert_id = self.generate_id(name, course)
            pdf_file = self.generator.create_pdf(name, course, str(date), cert_id)
            
            if pdf_file:
                if self.sender.send_email(email, name, course, pdf_file):
                    success += 1
        
        print(f"🎉 완료: {success}/{len(df)}명 성공")

def create_sample():
    data = {
        '이름': ['김철수', '이영희', '박민수', '정다영', '최준호'],
        '이메일': ['nissisoft21@gmail.com'] * 5,
        '과정명': ['파이썬 기초', '웹 크롤링', '데이터 분석', '머신러닝', '자동화 스크립트'],
        '수료일': ['2024-01-15', '2024-01-20', '2024-01-25', '2024-01-30', '2024-02-05']
    }
    df = pd.DataFrame(data)
    df.to_excel('수료생_명단.xlsx', index=False)
    print("✅ 샘플 파일 생성: 수료생_명단.xlsx")

if __name__ == "__main__":
    if not REPORTLAB_OK:
        print("❌ pip install reportlab pandas python-dotenv openpyxl")
        exit(1)
    
    excel_file = '수료생_명단.xlsx'
    if not os.path.exists(excel_file):
        create_sample()
    
    manager = CertificateManager()
    manager.process(excel_file)
