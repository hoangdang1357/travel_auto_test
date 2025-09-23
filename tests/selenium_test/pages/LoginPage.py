from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        
    def enter_email(self, email):
        email_element = self.wait.until(EC.element_to_be_clickable(self.email_field))
        email_element.clear()
        email_element.send_keys(email)
        
    def enter_password(self, password):
        password_element = self.wait.until(EC.element_to_be_clickable(self.password_field))
        password_element.clear()
        password_element.send_keys(password)
        
    def click_login_button(self):
        login_button_element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        login_button_element.click()
        
    def assert_h1(self, expected_text):
        h1_element = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_text = h1_element.text
        assert expected_text in h1_text, f"Expected '{expected_text}' in h1, but got '{h1_text}'"
        
    def assert_message(self, expected_text):
        message_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.flashes > li')))
        assert expected_text in message_element.text, f"Expected '{expected_text}' in message, but got '{message_element.text}'"

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    