from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.LoginPage import LoginPage
from pages.SearchPage import SearchPage
from pages.ServiceDetailPage import ServiceDetail
from pages.TravelersDetailPage import ServiceDetail as TravelersDetail
from pages.RegisterPage import RegisterPage
from pages.GmailPage import GmailPage
from helpers.verification_helper import get_verification_url_for_email
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import shutil

options = webdriver.ChromeOptions()
# keep the options minimal here; the fixture will create a temp profile
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
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
        # Instead of opening real Gmail, look up the verification token in the test DB
        # and navigate directly to the verification URL for stability.
        verification_url = get_verification_url_for_email(email)
        if verification_url:
            # Visit the verification URL to mark email as verified
            self.driver.get(verification_url)
            # small implicit wait to allow redirect/flash
            self.driver.implicitly_wait(3)
        else:
            # fallback to the Gmail flow (legacy) if DB lookup failed
            self.gmail_page.open_verification_link()
        self.login_page.login(email, password)
        self.login_page.assert_h1("Welcome to our Travel Booking Website")


@pytest.fixture
def chrome_driver():
    # Create a temporary user-data-dir to avoid locking real profile
    tmp_profile = tempfile.mkdtemp(prefix="selenium-profile-")
    local_options = webdriver.ChromeOptions()
    for arg in options.arguments:
        local_options.add_argument(arg)
    local_options.add_argument(f"--user-data-dir={tmp_profile}")
    # Use webdriver-manager to get a matching chromedriver binary
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=local_options)
    try:
        yield driver
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        shutil.rmtree(tmp_profile, ignore_errors=True)


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
   