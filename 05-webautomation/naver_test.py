from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyperclip
import pyautogui

def random_delay(min_sec=1, max_sec=3):
    """랜덤한 시간 대기"""
    delay = random.uniform(min_sec, max_sec)
    print(f"  대기 중... ({delay:.1f}초)")
    time.sleep(delay)

def setup_chrome_driver():
    """Chrome 드라이버 설정"""
    print("Chrome 드라이버 설정 중...")

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome 드라이버 생성 성공!")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Chrome 드라이버 생성 실패: {e}")
        return None

def slow_paste(selector, text, driver, delay=0.5):
    """클립보드 붙여넣기(캡차 우회)"""
    elem = driver.find_element(By.CSS_SELECTOR, selector)
    elem.click()
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(delay)

def main():
    driver = None
    naver_id = "sarang_0103"         # 여기에 네이버 아이디 입력
    naver_pw = "ioirwrt26!"   # 여기에 네이버 비밀번호 입력

    try:
        driver = setup_chrome_driver()
        if not driver:
            print("드라이버를 생성할 수 없습니다.")
            return

        print("\n🌐 Naver 로그인 페이지 접속 중...")
        driver.get("https://nid.naver.com/nidlogin.login")
        random_delay(2, 4)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#id")))

        print("⌨️  아이디 입력 중...(캡차 우회)")
        slow_paste("#id", naver_id, driver)
        random_delay(1, 2)

        print("⌨️  비밀번호 입력 중...(캡차 우회)")
        slow_paste("#pw", naver_pw, driver)
        random_delay(1, 2)

        print("🔑 로그인 버튼 클릭")
        login_btn = driver.find_element(By.CSS_SELECTOR, "#log\\.login")
        login_btn.click()

        random_delay(2, 4)

        # 로그인 완료 및 메인 진입 대기
        print("✅ 로그인 프로세스 종료. 메인 페이지 진입 대기.")
        time.sleep(5)

        print(f"\n⏰ 100초 후 자동 종료됩니다...")
        print("   수동으로 종료하려면 Ctrl+C를 누르세요.")

        for i in range(100, 0, -10):
            print(f"   남은 시간: {i}초")
            time.sleep(10)

    except KeyboardInterrupt:
        print("\n⛔ 사용자가 중단했습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            print("🔒 브라우저를 열어둡니다. 수동으로 닫으세요.")
            # driver.quit()는 호출하지 않음

if __name__ == "__main__":
    print("=== 네이버 자동 로그인 시작 ===")
    main()
    print("=== 프로그램 종료 ===")