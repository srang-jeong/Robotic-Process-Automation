"""
이메일 자동 분류 및 답장 - 주차 관련 문의 자동 응답
# 프롬프트
# "주차" 또는 "주차장" 이라는 글이 타이틀이나 내용에 들어 있으면, 
# 안내문구를 자동으로 답장하는 코드를 작성해 줘
"""

import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import re

# .env 파일 로드
load_dotenv()

def decode_mime_text(text):
    """MIME 인코딩된 텍스트를 디코딩"""
    if text is None:
        return ""
    
    decoded_parts = decode_header(text)
    decoded_text = ""
    
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            if encoding:
                try:
                    decoded_text += part.decode(encoding)
                except:
                    decoded_text += part.decode('utf-8', errors='ignore')
            else:
                decoded_text += part.decode('utf-8', errors='ignore')
        else:
            decoded_text += str(part)
    
    return decoded_text

def get_email_content(email_message):
    """메일 본문 내용 추출"""
    content = ""
    
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                try:
                    content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    content += str(part.get_payload())
    else:
        try:
            content = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            content = str(email_message.get_payload())
    
    return content

def create_parking_reply(original_subject, sender_name):
    """주차 관련 자동 답장 메시지 생성"""
    
    # 답장 제목 생성
    reply_subject = f"RE: {original_subject}"
    
    # 답장 내용 생성
    reply_content = f"""안녕하세요 {sender_name}님,

주차 관련 문의해 주셔서 감사합니다.

🚗 주차 안내 정보:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 주차장 위치: 건물 지하 1층 ~ 지하 3층
⏰ 이용시간: 24시간 운영
💰 주차요금: 
   - 방문객: 시간당 2,000원
   - 업무목적: 1일 10,000원
   - 월정기: 150,000원

🎫 주차권 발급:
   - 1층 안내데스크에서 발급
   - 사전 예약 가능 (02-1234-5678)

📞 문의사항:
   - 주차 관련: 02-1234-5678
   - 관리사무소: 02-1234-5679

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

추가 문의사항이 있으시면 언제든지 연락 주세요.
감사합니다.

자동 응답 시스템
"""
    
    return reply_subject, reply_content

def send_reply_email(to_email, subject, content):
    """답장 메일 발송"""
    
    # 환경변수에서 계정 정보 가져오기
    email_addr = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    
    try:
        # SMTP 서버 연결
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(email_addr, app_password)
        
        # 답장 메일 작성
        msg = MIMEMultipart()
        msg['From'] = email_addr
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 본문 추가
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 메일 발송
        smtp.sendmail(email_addr, to_email, msg.as_string())
        smtp.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ 답장 발송 실패: {e}")
        return False

def auto_reply_parking_emails():
    """주차 관련 메일 자동 답장 처리"""
    
    # 환경변수에서 계정 정보 가져오기
    email_addr = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    imap_server = os.getenv('IMAP_SERVER')
    
    if not email_addr or not app_password:
        print("❌ .env 파일에서 계정 정보를 찾을 수 없습니다.")
        return
    
    try:
        # Gmail 접속
        print("📧 Gmail 접속 중...")
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_addr, app_password)
        print("✅ Gmail 로그인 성공!")
        
        # 받은편지함 선택
        mail.select("inbox")
        
        # 안읽은 메일 검색
        print("\n🔍 안읽은 메일 검색 중...")
        status, messages = mail.search(None, "UNSEEN")
        
        if status != "OK":
            print("❌ 메일 검색 실패")
            return
        
        mail_ids = messages[0].split()
        
        if not mail_ids:
            print("📭 안읽은 메일이 없습니다.")
            return
        
        print(f"📬 안읽은 메일 {len(mail_ids)}개 발견")
        print("🔍 주차 관련 메일 검색 중...")
        print("=" * 70)
        
        parking_keywords = ["주차", "주차장"]
        replied_count = 0
        
        # 각 메일 확인
        for i, mail_id in enumerate(mail_ids, 1):
            try:
                # 메일 정보 가져오기
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                email_message = email.message_from_bytes(msg_data[0][1])
                
                # 제목, 발신자, 내용 추출
                subject = decode_mime_text(email_message["Subject"])
                from_header = decode_mime_text(email_message["From"])
                content = get_email_content(email_message)
                
                # 발신자 이메일 주소 추출
                from_email_match = re.search(r'<(.+?)>', from_header)
                if from_email_match:
                    from_email = from_email_match.group(1)
                else:
                    from_email = from_header.split()[0] if from_header else ""
                
                # 발신자 이름 추출
                sender_name = from_header.split('<')[0].strip() if '<' in from_header else from_header
                
                # 주차 키워드 검색
                has_parking_keyword = False
                found_keywords = []
                
                for keyword in parking_keywords:
                    if keyword in subject or keyword in content:
                        has_parking_keyword = True
                        found_keywords.append(keyword)
                
                if has_parking_keyword:
                    print(f"🚗 주차 관련 메일 발견!")
                    print(f"   제목: {subject}")
                    print(f"   발신자: {from_header}")
                    print(f"   키워드: {', '.join(found_keywords)}")
                    
                    # 답장 생성
                    reply_subject, reply_content = create_parking_reply(subject, sender_name)
                    
                    # 답장 발송
                    if send_reply_email(from_email, reply_subject, reply_content):
                        print("   ✅ 자동 답장 발송 완료")
                        replied_count += 1
                        
                        # 메일을 읽음 처리
                        mail.store(mail_id, '+FLAGS', '\\Seen')
                    else:
                        print("   ❌ 답장 발송 실패")
                    
                    print("-" * 70)
                
            except Exception as e:
                print(f"❌ 메일 {i} 처리 오류: {e}")
                continue
        
        print(f"\n🎉 총 {replied_count}개의 주차 관련 메일에 자동 답장을 보냈습니다!")
        
        # 연결 종료
        mail.close()
        mail.logout()
        print("✅ Gmail 연결 종료")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("🚗 주차 관련 메일 자동 답장 시스템")
    print("=" * 60)
    
    print("🔍 처리 대상:")
    print("- 제목이나 내용에 '주차' 또는 '주차장' 키워드가 포함된 안읽은 메일")
    print("- 자동으로 주차 안내 정보를 답장으로 발송")
    
    print("\n" + "=" * 60)
    
    # 자동 답장 처리 시작
    auto_reply_parking_emails()
    
    print("\n💡 활용 팁:")
    print("- 이 스크립트를 정기적으로 실행하여 주차 문의에 자동 응답")
    print("- Windows 작업 스케줄러나 cron으로 자동화 가능")
    print("- 답장 내용은 create_parking_reply() 함수에서 수정 가능")

