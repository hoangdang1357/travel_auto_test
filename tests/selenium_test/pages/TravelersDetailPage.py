from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class ServiceDetail:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.heading = (By.TAG_NAME, "h2")
        self.submitButton = (By.CSS_SELECTOR, 'button[type="submit"]')
        
    def get_fullname_field(self, index):
        locator = (By.ID, f"full_name_{index}")
        return self.wait.until(EC.element_to_be_clickable(locator))

    def enter_fullname(self, fullname, index):
        fullname_element = self.get_fullname_field(index)
        fullname_element.clear()
        fullname_element.send_keys(fullname)
    
    def get_gender_field(self, index):
        # the select has id="gender_<index>" in the page; use ID to uniquely target it
        locator = (By.ID, f"gender_{index}")
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def enter_gender(self, index, gender):
        gender_element = self.get_gender_field(index)
        # Use Selenium Select for <select> elements. Accept either the option value
        # (e.g. 'male') or visible text (e.g. 'Male').
        select = Select(gender_element)
        # try selecting by value first, then by visible text as a fallback
        try:
            select.select_by_value(gender)
        except Exception:
            try:
                select.select_by_visible_text(gender)
            except Exception:
                # last resort: try case-insensitive match of visible text
                for opt in select.options:
                    if opt.text.strip().lower() == str(gender).strip().lower():
                        select.select_by_visible_text(opt.text)
                        break
    
    def get_dob_field(self, index):
        locator = (By.ID, f"dob_{index}")
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def enter_dob(self, dob, index):
        dob_element = self.get_dob_field(index)
        dob_element.clear()
        dob_element.send_keys(dob)

    def get_passport_field(self, index):
        locator = (By.ID, f"passport_number_{index}")
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def enter_passport(self, passport, index):
        passport_element = self.get_passport_field(index)
        passport_element.clear()
        passport_element.send_keys(passport)
        
    def enter_traveler_details(self, index, fullname, gender, dob, passport):
        self.enter_fullname(fullname, index)
        self.enter_gender(index, gender)
        self.enter_dob(dob, index)
        self.enter_passport(passport, index)

    def click_book_now(self):
        book_button_element = self.wait.until(EC.element_to_be_clickable(self.submitButton))
        book_button_element.click()