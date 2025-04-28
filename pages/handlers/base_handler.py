import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BaseHandler:
    """Base class for all handlers with common functionality"""
    
    def __init__(self, driver: WebDriver, logger: logging.Logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)
        
    def _wait_for_visible(self, locator, timeout: int = 10):
        """Wait for element to be visible"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.warning(f"Timeout waiting for element: {locator}")
            return None
            
    def _wait_for_clickable(self, locator, timeout: int = 10):
        """Wait for element to be clickable"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.logger.warning(f"Timeout waiting for clickable element: {locator}")
            return None 