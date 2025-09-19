from selenium import webdriver
from LoginPage import LoginPage
import time

driver = webdriver.Chrome()

def test_correct_login():
    try:
        driver.get("https://hoang.pythonanywhere.com/auth/signin")
        
        login_page_object = LoginPage(driver=driver)
        
        login_page_object.login(email="hoangdang1368@gmail.com", password="Hoang123123")
        
        time.sleep(2)
    finally:
        driver.quit()
        
        
        
