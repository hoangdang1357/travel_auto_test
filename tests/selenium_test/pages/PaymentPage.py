from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.payment_header = (By.TAG_NAME, "h1")
        self.payment_info = (By.CLASS_NAME, "payment-info")
        self.payNowButton = (By.CSS_SELECTOR, 'button[type="submit"]')

    def get_payment_header(self):
        header_element = self.wait.until(EC.presence_of_element_located(self.payment_header))
        return header_element.text

    def get_payment_info(self):
        info_element = self.wait.until(EC.presence_of_element_located(self.payment_info))
        return info_element.text
    
    def click_pay_now_button(self):
        pay_now_button_element = self.wait.until(EC.element_to_be_clickable(self.payNowButton))
        pay_now_button_element.click()