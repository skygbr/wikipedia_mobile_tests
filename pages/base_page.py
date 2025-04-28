from typing import Tuple, Optional, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import logging

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.wait = WebDriverWait(self.driver, 10)
    
    def _wait_for_element(self, locator: Tuple[str, str], timeout: int = 10, 
                         condition: Any = EC.presence_of_element_located) -> Any:
        """Wait for element with specified condition
        
        Args:
            locator: Tuple of (By, value) for element location
            timeout: Maximum time to wait in seconds
            condition: Expected condition to wait for
            
        Returns:
            WebElement: The found element
            
        Raises:
            TimeoutException: If element is not found within timeout
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(condition(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {locator}")
            self.logger.debug("Current page source: %s", self.driver.page_source)
            raise
    
    def _wait_for_clickable(self, locator: Tuple[str, str], timeout: int = 10) -> Any:
        """Wait for element to be clickable"""
        return self._wait_for_element(locator, timeout, EC.element_to_be_clickable)
    
    def _wait_for_visible(self, locator: Tuple[str, str], timeout: int = 10) -> Any:
        """Wait for element to be visible"""
        return self._wait_for_element(locator, timeout, EC.visibility_of_element_located)
    
    def _safe_click(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """Safely click an element with proper waits"""
        element = self._wait_for_clickable(locator, timeout)
        element.click()
    
    def _safe_send_keys(self, locator: Tuple[str, str], text: str, timeout: int = 10) -> None:
        """Safely enter text into an element with proper waits"""
        element = self._wait_for_clickable(locator, timeout)
        element.clear()
        element.click()
        element.send_keys(text)
    
    def _is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is present on the page"""
        try:
            self._wait_for_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def _is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is visible on the page"""
        try:
            element = self._wait_for_visible(locator, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def _get_element_text(self, locator: Tuple[str, str], timeout: int = 10) -> Optional[str]:
        """Get text from element if present"""
        try:
            element = self._wait_for_visible(locator, timeout)
            return element.text
        except (TimeoutException, NoSuchElementException):
            return None
    
    def _get_element_attribute(self, locator: Tuple[str, str], attribute: str, 
                             timeout: int = 10) -> Optional[str]:
        """Get attribute value from element if present"""
        try:
            element = self._wait_for_element(locator, timeout)
            return element.get_attribute(attribute)
        except (TimeoutException, NoSuchElementException):
            return None
    
    def _scroll_to_element(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """Scroll to make element visible"""
        try:
            element = self._wait_for_element(locator, timeout)
            self.driver.execute_script("mobile: scroll", {"element": element.id})
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            raise 