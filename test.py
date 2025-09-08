import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_search_employee(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys("Admin")

    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "PIM"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type for hints...']"))
    ).send_keys("Linda Anderson")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    assert "Linda" in driver.page_source

    time.sleep(15)