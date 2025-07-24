"""
Gmail 스팸 메일 자동 이동 - "(광고)" 문구 포함 메일 처리
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

def move_ads_to_spam():
    """(광고) 문구가 포함된 메일을 스팸 폴더로 이동"""
    
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
        
        # 모든 메일 검색 (한글 검색 문제 해결)
        print("\n🔍 받은편지함 메일 검색 중...")
        status, messages = mail.search(None, "ALL")
        
        if status != "OK":
            print("❌ 메일 검색 실패")
            return
        
        mail_ids = messages[0].split()
        
        if not mail_ids:
            print("📭 메일이 없습니다.")
            return
        
        print(f"📬 총 {len(mail_ids)}개 메일 검색 완료")
        print("🔍 '(광고)' 문구가 포함된 메일 찾는 중...")
        print("=" * 60)
        
        moved_count = 0
        ads_mails = []
        
        # 각 메일 확인
        for i, mail_id in enumerate(mail_ids, 1):
            try:
                # 메일 정보 가져오기
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                email_message = email.message_from_bytes(msg_data[0][1])
                
                # 제목과 발신자 추출
                subject = decode_subject(email_message["Subject"])
                from_addr = decode_subject(email_message["From"])
                
                # "(광고)" 문구 확인
                if "(광고)" in subject:
                    ads_mails.append((mail_id, subject, from_addr))
                    print(f"📧 발견: {subject}")
                    print(f"   발신자: {from_addr}")
                    print("-" * 60)
                
                # 진행 상황 표시 (100개마다)
                if i % 100 == 0:
                    print(f"🔄 진행 중... {i}/{len(mail_ids)}")
                
            except Exception as e:
                print(f"❌ 메일 {i} 처리 오류: {e}")
                continue
        
        if not ads_mails:
            print("📭 '(광고)' 문구가 포함된 메일이 없습니다.")
            return
        
        print(f"\n🎯 '(광고)' 메일 {len(ads_mails)}개 발견!")
        print("=" * 60)
        
        # 광고 메일들을 스팸 폴더로 이동
        for mail_id, subject, from_addr in ads_mails:
            try:
                # 스팸 폴더로 이동 (Gmail에서는 [Gmail]/&wqTTONVo- 사용)
                mail.copy(mail_id, "[Gmail]/&wqTTONVo-")
                
                # 원본 메일을 삭제 표시
                mail.store(mail_id, '+FLAGS', '\\Deleted')
                
                print(f"✅ 이동 완료: {subject[:50]}...")
                moved_count += 1
                
            except Exception as e:
                print(f"❌ 이동 실패: {subject[:50]}... - {e}")
                continue
        
        # 삭제 표시된 메일들을 실제로 삭제
        if moved_count > 0:
            mail.expunge()
            print(f"\n🎉 총 {moved_count}개의 광고 메일을 스팸 폴더로 이동했습니다!")
        else:
            print("\n😔 이동할 수 있는 메일이 없었습니다.")
        
        # 연결 종료
        mail.close()
        mail.logout()
        print("✅ Gmail 연결 종료")
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def show_folder_list():
    """Gmail 폴더 목록 확인 (디버깅용)"""
    
    email_addr = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    imap_server = os.getenv('IMAP_SERVER')
    
    if not email_addr or not app_password:
        print("❌ .env 파일에서 계정 정보를 찾을 수 없습니다.")
        return
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_addr, app_password)
        
        # 모든 폴더 목록 가져오기
        status, folders = mail.list()
        
        print("📁 Gmail 폴더 목록:")
        print("=" * 40)
        for folder in folders:
            folder_str = folder.decode()
            print(folder_str)
            # 스팸 폴더 식별
            if "&wqTTONVo-" in folder_str:
                print("   ↳ 이 폴더가 스팸 폴더입니다!")
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("🚫 Gmail 스팸 메일 자동 이동")
    print("=" * 50)
    
    # 폴더 목록 확인 (선택사항)
    print("📁 Gmail 폴더 구조 확인:")
    show_folder_list()
    
    print("\n" + "=" * 50)
    
    # 광고 메일 스팸 이동
    move_ads_to_spam()
    
    print("\n💡 팁:")
    print("- 이 스크립트를 정기적으로 실행하면 광고 메일을 자동으로 정리할 수 있습니다.")
    print("- Windows 작업 스케줄러나 cron으로 자동화할 수 있습니다.")
