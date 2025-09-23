from selenium.webdriver.common.by import By

class ServiceDetail:
    def __init__(self, driver):
        self.driver = driver
        self.heading = (By.TAG_NAME, "h2")
        self.book_button = (By.LINK_TEXT, 'Save and Proceed to Payment')
        
    def get_fullname_field(self, index):
        locator = (By.NAME, f"fullname_{index}")
        return self.driver.find_element(*locator)

    def enter_fullname(self, fullname, index):
        self.get_fullname_field(index).send_keys(fullname)
    
    def get_gender_field(self, index):
        locator = (By.NAME, f"gender_{index}")
        return self.driver.find_element(*locator)
    
    def enter_gender(self, index, dob):
        self.get_gender_field(index).send_keys(dob)
    
    def get_dob_field(self, index):
        locator = (By.NAME, f"dob_{index}")
        return self.driver.find_element(*locator)
    
    def enter_dob(self, dob, index):
        self.get_dob_field(index).send_keys(dob)

    def get_passport_field(self, index):
        locator = (By.NAME, f"passport_number_{index}")
        return self.driver.find_element(*locator)
    
    def enter_passport(self, passport, index):
        self.get_passport_field(index).send_keys(passport)
        
    def enter_traveler_details(self, index, fullname, gender, dob, passport):
        self.enter_fullname(fullname, index)
        self.enter_gender(index, gender)
        self.enter_dob(dob, index)
        self.enter_passport(passport, index)

    def click_book_now(self):
        self.driver.find_element(*self.book_button).click()