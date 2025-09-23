from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.full_name_field = (By.NAME, "full_name")
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.phone_field = (By.NAME, "phone")
        self.address_field = (By.NAME, "address")
        self.register_button = (By.CSS_SELECTOR, 'button[type="submit"]')

    def navigate_to_register_page(self):
        self.driver.get("https://hoang.pythonanywhere.com/auth/signup")
        # Wait for the page to load by waiting for a key element
        self.wait.until(EC.presence_of_element_located(self.full_name_field))

    def enter_full_name(self, full_name):
        full_name_element = self.wait.until(EC.element_to_be_clickable(self.full_name_field))
        full_name_element.clear()
        full_name_element.send_keys(full_name)
        
    def enter_email(self, email):
        email_element = self.wait.until(EC.element_to_be_clickable(self.email_field))
        email_element.clear()
        email_element.send_keys(email)
        
    def enter_password(self, password):
        password_element = self.wait.until(EC.element_to_be_clickable(self.password_field))
        password_element.clear()
        password_element.send_keys(password)
        
    def enter_phone(self, phone):
        phone_element = self.wait.until(EC.element_to_be_clickable(self.phone_field))
        phone_element.clear()
        phone_element.send_keys(phone)
        
    def enter_address(self, address):
        address_element = self.wait.until(EC.element_to_be_clickable(self.address_field))
        address_element.clear()
        address_element.send_keys(address)
        
    def click_register_button(self):
        register_button_element = self.wait.until(EC.element_to_be_clickable(self.register_button))
        register_button_element.click()
        
    def assert_h1(self, expected_text):
        h1_element = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        h1_text = h1_element.text
        assert expected_text in h1_text, f"Expected '{expected_text}' in h1, but got '{h1_text}'"
        
    def assert_message(self, expected_text):
        message_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.flashes > li')))
        assert expected_text in message_element.text, f"Expected '{expected_text}' in message, but got '{message_element.text}'"

    def register(self, full_name, email, password, phone, address):
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_phone(phone)
        self.enter_address(address)
        self.click_register_button()