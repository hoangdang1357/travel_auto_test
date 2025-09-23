from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ServiceDetail:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.service_name = (By.TAG_NAME, "h1")
        self.service_description = (By.CLASS_NAME, "service-description")
        self.book_button = (By.LINK_TEXT, "Book Now")

    def get_service_name(self):
        service_name_element = self.wait.until(EC.presence_of_element_located(self.service_name))
        return service_name_element.text

    def get_service_description(self):
        service_description_element = self.wait.until(EC.presence_of_element_located(self.service_description))
        return service_description_element.text

    def click_book_now(self):
        book_button_element = self.wait.until(EC.element_to_be_clickable(self.book_button))
        book_button_element.click()