import csv
import pytest
from selenium import webdriver
from LoginPage import LoginPage
import os
# helper to load test data from CSV
def load_test_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                row["email"],
                row["password"],
                row["assert_type"],
                row["expected"],
            ))
    return test_cases

# load data once
CSV_PATH = os.path.join(os.path.dirname(__file__), "csv_data", "login_test_data.csv")
test_data = load_test_data_from_csv(CSV_PATH)

@pytest.mark.parametrize("email,password,assert_type,expected", test_data)
def test_login(email, password, assert_type, expected):
    driver = webdriver.Chrome()
    try:
        driver.get("https://hoang.pythonanywhere.com/auth/signin")
        login_page = LoginPage(driver=driver)

        # perform login
        login_page.login(email=email, password=password)
        driver.implicitly_wait(10)

        # flexible assertion depending on type
        if assert_type == "h1":
            login_page.assert_h1(expected)
        elif assert_type == "message":
            login_page.assert_message(expected)
        else:
            pytest.fail(f"Unknown assert type: {assert_type}")
    finally:
        driver.quit()
