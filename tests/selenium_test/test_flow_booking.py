from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.LoginPage import LoginPage
from pages.SearchPage import SearchPage
from pages.ServiceDetailPage import ServiceDetail
from pages.TravelersDetailPage import ServiceDetail as TravelersDetail
from pages.RegisterPage import RegisterPage
from pages.GmailPage import GmailPage
import os
import pytest
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Profile 2")



class FlowBooking:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.search_page = SearchPage(driver)
        self.service_detail_page = ServiceDetail(driver)
        self.travelers_detail_page = TravelersDetail(driver)
        self.register_page = RegisterPage(driver)
        self.gmail_page = GmailPage(driver)

    def test_flow_booking(self, email, password, service_name, fullname, phone, address):
        self.register_page.navigate_to_register_page()
        self.register_page.register(fullname, email, password, phone, address)
        self.gmail_page.open_verification_link()
        self.driver.implicitly_wait(10)
        self.login_page.login(email, password)
        self.login_page.assert_h1("Welcome to our Travel Booking Website")


@pytest.fixture
def chrome_driver():
    # Lightweight fixture - adjust path or options as needed
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_e2e_flow_booking(chrome_driver):
    flow = FlowBooking(chrome_driver)
    # Example parameters - replace with real test values or parametrize
    flow.test_flow_booking(
        email="dangbaohoang1368@gmail.com",
        password="TestPass123",
        service_name="Paris",
        fullname="Test User",
        phone="0123456789",
        address="Hanoi"
    )
   