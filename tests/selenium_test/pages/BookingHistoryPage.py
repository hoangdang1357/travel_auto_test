from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingHistoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 second timeout
        self.history_header = (By.TAG_NAME, "h1")
        self.booking_entries = (By.CLASS_NAME, "booking-entry")

    def get_history_header(self):
        header_element = self.wait.until(EC.presence_of_element_located(self.history_header))
        return header_element.text

    def get_booking_entries(self):
        entries = self.wait.until(EC.presence_of_all_elements_located(self.booking_entries))
        return [entry.text for entry in entries]

    def assert_booking_contains_text(self, expected_text: str):
        """Assert that at least one booking row contains expected_text (case-insensitive).

        expected_text is normalized (lower/strip) before matching.
        Raises AssertionError if not found.
        """
        expected_norm = expected_text.strip().lower()
        # Prefer reading table rows if present
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
            for row in rows:
                if expected_norm in row.text.strip().lower():
                    return True
        except Exception:
            # fallback to booking entries text
            entries = self.get_booking_entries()
            for e in entries:
                if expected_norm in e.strip().lower():
                    return True
        raise AssertionError(f"No booking row contains expected text: {expected_text}")