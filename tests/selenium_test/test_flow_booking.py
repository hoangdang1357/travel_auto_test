from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.LoginPage import LoginPage
from pages.SearchPage import SearchPage
from pages.ServiceDetail import ServiceDetail
from pages.TravelersDetail import ServiceDetail as TravelersDetail
from pages.RegisterPage import RegisterPage
import os

class FlowBooking:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.search_page = SearchPage(driver)
        self.service_detail_page = ServiceDetail(driver)
        self.travelers_detail_page = TravelersDetail(driver)
        self.register_page = RegisterPage(driver)

    def test_flow_booking(self, email, password, service_name, fullname, phone, address):
        self.register_page.navigate_to_register_page()
        self.register_page.register(fullname, email, password, phone, address)
        
        