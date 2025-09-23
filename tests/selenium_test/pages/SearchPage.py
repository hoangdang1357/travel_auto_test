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
        
    def assert_service_present(self, expected_text):
        services = self.driver.find_elements(*self.services_card)
        print(f"Found {len(services)} services on the page.")
        if expected_text.lower() in ["no trip is found", "all trips"]:
            if expected_text == "No trip is found":
                assert len(services) == 0, f"Expected no services, but found {len(services)}"
                return True
            elif expected_text == "All trips":
                assert len(services) > 0, "Expected some services, but found none"
                return True
            else:
                raise AssertionError(f"Unexpected expected_text value: {expected_text}")
        for service in services:
            if expected_text in service.text:
                return True
        raise AssertionError(f"Service with text '{expected_text}' not found on the page")
        
    
        
