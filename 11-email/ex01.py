"""
Gmail 메일 보내기 - 환경변수 사용
"""

# dotenv 라이브러리 : .env 값을 가져오는 라이브러리
# py -m pip install dotenv smtplib

import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def send_email():
    """Gmail로 메일 보내기"""
    
    # 환경변수에서 계정 정보 가져오기
    email_addr = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    
    if not email_addr or not app_password:
        print("❌ .env 파일에서 계정 정보를 찾을 수 없습니다.")
        return
    
    # SMTP 서버 연결
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    
    # 로그인
    smtp.login(email_addr, app_password)
    
    # 메일 내용 설정
    msg = MIMEText('내용 : 본문 내용 - 주차장 관련 문의')
    msg['Subject'] = '제목: 파이썬으로 gmail 보내기'
    
    # 메일 보내기
    smtp.sendmail(email_addr, email_addr, msg.as_string())
    
    # 연결 종료
    smtp.quit()
    
    print("✅ 메일 발송 완료")

if __name__ == "__main__":
    send_email()
