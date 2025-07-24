from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 구굴 사이트가 자동화된 SW 임을 인지한다.

driver = webdriver.Chrome()
driver.get("https://www.google.com")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python") # 한방에 입력되므로 사람 아니다.
search_box.send_keys(Keys.RETURN)
time.sleep(50)