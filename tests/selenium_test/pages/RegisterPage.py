from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.full_name_field = (By.NAME, "full_name")
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.phone_field = (By.NAME, "phone")
        self.address_field = (By.NAME, "address")
        self.register_button = (By.CSS_SELECTOR, 'button[type="submit"]')

    def navigate_to_register_page(self):
        self.driver.get("https://hoang.pythonanywhere.com/auth/signup")

    def enter_full_name(self, full_name):
        self.driver.find_element(*self.full_name_field).send_keys(full_name)
        
    def enter_email(self, email):
        self.driver.find_element(*self.email_field).send_keys(email)
        
    def enter_password(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)
        
    def enter_phone(self, phone):
        self.driver.find_element(*self.phone_field).send_keys(phone)
        
    def enter_address(self, address):
        self.driver.find_element(*self.address_field).send_keys(address)
        
    def click_register_button(self):
        self.driver.find_element(*self.register_button).click()
        
    def assert_h1(self, expected_text):
        h1_text = self.driver.find_element(By.TAG_NAME, "h1").text
        assert expected_text in h1_text, f"Expected '{expected_text}' in h1, but got '{h1_text}'"
        
    def assert_message(self, expected_text):
        message_element = self.driver.find_element(By.CSS_SELECTOR, 'ul.flashes > li')
        assert expected_text in message_element.text, f"Expected '{expected_text}' in message, but got '{message_element.text}'"

    def register(self, full_name, email, password, phone, address):
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_phone(phone)
        self.enter_address(address)
        self.click_register_button()