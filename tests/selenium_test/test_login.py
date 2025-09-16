from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://hoang.pythonanywhere.com/auth/signin")

    def tearDown(self):
        self.driver.quit()

    def test_login_correct_credentials(self):
        driver = self.driver
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("hoangdang1368@gmail.com")
        password_input.send_keys("Hoang123123")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for redirect
        # Check for successful login message or redirect
        body_text = driver.page_source
        self.assertIn("Signed in successfully!", body_text)
        
    def test_success_email_sensitive(self):
        driver = self.driver
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("HOANGDANG1368@gmail.com")
        password_input.send_keys("Hoang123123")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for redirect
        # Check for successful login message or redirect
        body_text = driver.page_source
        self.assertIn("Signed in successfully!", body_text)
        
    def test_success_email_extra_spaces(self):
        driver = self.driver
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("   hoangdang1368@gmail.com   ")
        password_input.send_keys("Hoang123123")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for redirect
        # Check for successful login message or redirect
        body_text = driver.page_source
        self.assertIn("Signed in successfully!", body_text)
        
    def test_fail_password_extra_spaces(self):
        driver = self.driver
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("hoangdang1368@gmail.com")
        password_input.send_keys("   Hoang123123   ")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for redirect
        # Check for successful login message or redirect
        message = driver.find_element(By.CLASS_NAME, "flash").text
        self.assertIn("Invalid email or password.", message)
        
    


if __name__ == "__main__":
    unittest.main()