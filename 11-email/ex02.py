"""
Gmail 안읽은 메일 조회 (간단 버전) - 환경변수 사용
"""

import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def decode_subject(subject):
    """제목 디코딩"""
    if subject is None:
        return "제목 없음"
    
    decoded = decode_header(subject)[0]
    if isinstance(decoded[0], bytes):
        return decoded[0].decode(decoded[1] or 'utf-8')
    return decoded[0]

def get_unread_emails():
    """안읽은 메일 조회"""
    
    # 환경변수에서 계정 정보 가져오기
    email_addr = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    imap_server = os.getenv('IMAP_SERVER')
    
    if not email_addr or not app_password:
        print("❌ .env 파일에서 계정 정보를 찾을 수 없습니다.")
        return
    
    # Gmail 접속
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_addr, app_password)
    mail.select("inbox") # 받은편지함
    
    # 안읽은 메일 검색
    status, messages = mail.search(None, "UNSEEN")
    mail_ids = messages[0].split()
    
    if not mail_ids:
        print("📭 안읽은 메일이 없습니다.")
        return
    
    print(f"📬 안읽은 메일 {len(mail_ids)}개")
    print("=" * 50)
    
    # 메일 정보 출력
    for i, mail_id in enumerate(mail_ids, 1):
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        email_message = email.message_from_bytes(msg_data[0][1])
        
        # 제목과 날짜 추출
        subject = decode_subject(email_message["Subject"])
        date = email_message["Date"]
        
        print(f"{i}. {subject}")
        print(f"   시간: {date}")
        print("-" * 50)
    
    mail.close()
    mail.logout()

if __name__ == "__main__":
    get_unread_emails()
