import csv
import pytest
from selenium import webdriver
from pages.SearchPage import SearchPage
import os

# helper to load test data from CSV
def load_test_data_from_csv(filepath):
    test_cases = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_cases.append((
                row["hotel"],
                row["flight"],
                row["expected"],
            ))
    return test_cases

# load data once
CSV_PATH = os.path.join(os.path.dirname(__file__), "csv_data", "search_test_data.csv")
test_data = load_test_data_from_csv(CSV_PATH)

@pytest.mark.parametrize("hotel,flight,expected", test_data)
def test_search_hotel_flight(hotel, flight, expected):
    driver = webdriver.Chrome()
    try:
        driver.get("https://hoang.pythonanywhere.com/services/")
        search_page = SearchPage(driver=driver)
        driver.implicitly_wait(10)

        # perform search
        search_page.enter_hotel(hotel_name=hotel)
        search_page.enter_flight(flight_name=flight)
        search_page.click_search()
        driver.implicitly_wait(10)
        search_page.assert_service_present(expected_text=expected)
        # assert results
    finally:
        driver.quit()