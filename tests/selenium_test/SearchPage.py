from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.hotel_field = (By.NAME, "hotel")
        self.flight_field = (By.NAME, "flight")
        self.search_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        self.services_card = (By.CLASS_NAME, "service-card")

    def enter_hotel(self, hotel_name):
        hotel_input = self.driver.find_element(*self.hotel_field)
        hotel_input.clear()
        hotel_input.send_keys(hotel_name)

    def enter_flight(self, flight_name):
        flight_input = self.driver.find_element(*self.flight_field)
        flight_input.clear()
        flight_input.send_keys(flight_name)

    def click_search(self):
        self.driver.find_element(*self.search_button).click()
        
    
        
