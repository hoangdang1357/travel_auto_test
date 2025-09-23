from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class GmailPage:
    def __init__(self, driver):
        self.driver = driver
        self.verify_link = (By.XPATH, "//a[starts-with(@href, 'https://hoang.pythonanywhere.com/auth/signup/')]")
        self.email_item = (By.NAME, "dangbaohoang1368")

    def open_gmail(self):
        self.driver.get("https://mail.google.com/mail/u/0/#inbox")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.email_item)
            )
    
    def click_email_item(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.email_item)
        ).click()

    def click_verify_link(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.verify_link)
        ).click()
