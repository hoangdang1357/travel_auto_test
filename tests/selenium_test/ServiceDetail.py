from selenium.webdriver.common.by import By

class ServiceDetail:
    def __init__(self, driver):
        self.driver = driver
        self.service_name = (By.TAG_NAME, "h1")
        self.service_description = (By.CLASS_NAME, "service-description")
        self.book_button = (By.LINK_TEXT, "Book Now")

    def get_service_name(self):
        return self.driver.find_element(*self.service_name).text

    def get_service_description(self):
        return self.driver.find_element(*self.service_description).text

    def click_book_now(self):
        self.driver.find_element(*self.book_button).click()