from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.hotel_field = (By.NAME, "hotel")
        self.flight_field = (By.NAME, "flight")
        self.destination_field = (By.NAME, "destination")
        self.search_button = (By.CSS_SELECTOR, 'button[type="submit"]')
        self.services_card = (By.CLASS_NAME, "service-card")
        self.view_details_button = (By.LINK_TEXT, "View Details")
        
    def enter_destination(self, destination):
        destination_input = self.wait.until(EC.element_to_be_clickable(self.destination_field))
        destination_input.clear()
        destination_input.send_keys(destination)
        
    def click_view_details(self):
        self.wait.until(EC.element_to_be_clickable(self.view_details_button)).click()
        
    def navigate_to_search_page(self):
        self.driver.get("https://hoang.pythonanywhere.com/services")
        # Wait for the page to load by waiting for a key element
        self.wait.until(EC.presence_of_element_located(self.hotel_field))

    def enter_hotel(self, hotel_name):
        hotel_input = self.wait.until(EC.element_to_be_clickable(self.hotel_field))
        hotel_input.clear()
        hotel_input.send_keys(hotel_name)

    def enter_flight(self, flight_name):
        flight_input = self.wait.until(EC.element_to_be_clickable(self.flight_field))
        flight_input.clear()
        flight_input.send_keys(flight_name)

    def click_search(self):
        search_button_element = self.wait.until(EC.element_to_be_clickable(self.search_button))
        search_button_element.click()
        
    def assert_service_present(self, expected_text):
        # Wait for the page to load after search by waiting for services container or no results
        try:
            # Wait for either services to be present or page to fully load
            self.wait.until(lambda driver: 
                len(driver.find_elements(*self.services_card)) >= 0 or
                "No services found" in driver.page_source
            )
        except:
            pass  # Continue with assertion logic even if wait times out
            
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
        
    
        
