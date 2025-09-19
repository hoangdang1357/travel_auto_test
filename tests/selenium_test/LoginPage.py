from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        
    def enter_email(self, email):
        self.driver.find_element(*self.email_field).send_keys(email)
        
    def enter_password(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)
        
    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()
        
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()