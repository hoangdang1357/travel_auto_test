from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NewBookingPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.travel_date = (By.NAME, "travel_date")
        self.num_travelers = (By.NAME, "num_travelers")
        self.booking_header = (By.TAG_NAME, "h1")
        self.confirm_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        
    def enter_travel_date(self, date):
        travel_date_element = self.wait.until(EC.element_to_be_clickable(self.travel_date))
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", travel_date_element)
        travel_date_element.clear()
        self.driver.execute_script("arguments[0].value = arguments[1]", travel_date_element, date)
        
    def enter_num_travelers(self, num):
        num_travelers_element = self.wait.until(EC.element_to_be_clickable(self.num_travelers))
        num_travelers_element.clear()
        num_travelers_element.send_keys(num)
    # to commit the adding explicit wait for NewBookingPage and GmailPage
    def get_booking_header(self):
        header_element = self.wait.until(EC.presence_of_element_located(self.booking_header))
        return header_element.text

    def click_confirm_button(self):
        confirm_button_element = self.wait.until(EC.element_to_be_clickable(self.confirm_button))
        confirm_button_element.click()
