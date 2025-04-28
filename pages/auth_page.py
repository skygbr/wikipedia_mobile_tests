# Standard library imports
import logging
import os
from typing import Tuple, Optional, Dict, Any, List
import time

# Third-party imports
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotVisibleException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import platform
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from .base_page import BasePage
from .locators import AuthPageLocators
from .handlers.dialog_handler import DialogHandler
from .handlers.keyboard_handler import KeyboardHandler
from .handlers.field_handler import FieldHandler

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

class AuthPage(BasePage):
    """Page object for authentication-related functionality"""
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.locators = AuthPageLocators()
        
        # Initialize handlers
        self.dialog_handler = DialogHandler(driver, self.logger, self.locators)
        self.keyboard_handler = KeyboardHandler(driver, self.logger, self.locators)
        self.field_handler = FieldHandler(driver, self.logger, self.locators)

    def navigate_to_login(self) -> None:
        """Navigate to the login screen"""
        self.logger.info("Navigating to login screen")
        if self.is_on_login_page():
            self.logger.info("Already on login page")
            return
        
        try:
            # First click the profile button
            profile_button = self._wait_for_visible(self.locators.PROFILE_BUTTON)
            if not profile_button.is_displayed():
                self.logger.info("Profile button not visible, attempting to scroll")
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                profile_button = self._wait_for_visible(self.locators.PROFILE_BUTTON)
            
            self.logger.info("Clicking profile button")
            self._safe_click(self.locators.PROFILE_BUTTON)
            
            # Look for "Log in / Join Wikipedia" button
            login_button = self._wait_for_visible(self.locators.LOGIN_BUTTON)
            if not login_button.is_displayed():
                self.logger.info("Login button not visible, attempting to scroll")
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                login_button = self._wait_for_visible(self.locators.LOGIN_BUTTON)
            
            self.logger.info("Clicking login button")
            self._safe_click(self.locators.LOGIN_BUTTON)
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to login screen: {str(e)}")
            self.logger.info("Current page source:")
            self.logger.info(self.driver.page_source)
            raise

    def enter_username(self, username: str) -> None:
        """Enter username in the username field"""
        self.logger.info(f"Entering username: {username}")
        try:
            username_field = self._wait_for_clickable(self.locators.USERNAME_FIELD)
            if not username_field:
                raise Exception("Username field not found")

            # Clear the field and ensure it's focused
            username_field.clear()
            username_field.click()

            # Enter username
            username_field.send_keys(username)

            # Verify username was entered by checking field is not empty
            field_value = username_field.get_attribute('value')
            if not field_value:
                raise Exception("Username field is empty after entry")

            self.logger.info("Username entered successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to enter username: {str(e)}")
            self.logger.error(f"Current page source: {self.driver.page_source}")
            raise

    def enter_password(self, password: str) -> None:
        """Enter password in the password field"""
        try:
            password_field = self._wait_for_clickable(self.locators.PASSWORD_FIELD)
            if not password_field:
                raise Exception("Password field not found")

            # Clear the field and ensure it's focused
            password_field.clear()
            password_field.click()

            # Switch to English keyboard if needed
            self.keyboard_handler.switch_to_english_keyboard()

            # Enter password as a single string
            password_field.send_keys(password)

            # Verify final password entry
            final_value = password_field.get_attribute('value')
            if final_value == 'enter password' or not final_value:
                self.logger.error(f"Password field value after entry: {final_value}")
                raise Exception("Password was not entered correctly")

            self.logger.info("Password entered successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to enter password: {str(e)}")
            self.logger.error(f"Current page source: {self.driver.page_source}")
            raise

    def toggle_remember_me(self) -> None:
        """Toggle the remember me checkbox and handle any additional dialog windows"""
        self.logger.info("Toggling remember me checkbox")
        try:
            remember_me = self._wait_for_clickable(self.locators.REMEMBER_ME_CHECKBOX)
            remember_me.click()
        except Exception as e:
            self.logger.error(f"Failed to toggle remember me: {str(e)}")
            raise

    def click_login(self) -> None:
        """Click the login button"""
        self.logger.info("Attempting to click login button")
        try:
            # Wait for and click the login button
            login_button = self._wait_for_clickable(self.locators.LOGIN_SUBMIT_BUTTON)
            if not login_button:
                raise Exception("Login button not found or not clickable")
            
            login_button.click()
            self.logger.info("Login button clicked successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to click login button: {str(e)}")
            self.logger.info("Current page source:")
            self.logger.info(self.driver.page_source)
            raise

    def handle_captcha(self) -> None:
        """Handle CAPTCHA security check if present"""
        if self._is_element_visible(self.locators.CAPTCHA_TEXT):
            self.logger.info("Handling CAPTCHA security check")
            self._safe_click(self.locators.CAPTCHA_CANCEL_BUTTON)

    def handle_save_password_dialog(self) -> None:
        """Handle the save password dialog"""
        self.dialog_handler.handle_save_password_dialog()

    def handle_reading_list_sync(self) -> None:
        """Handle the reading list sync dialog"""
        self.dialog_handler.handle_reading_list_sync()

    @property
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        try:
            profile_button = self._wait_for_visible(self.locators.PROFILE_BUTTON, timeout=5)
            return profile_button.is_displayed()
        except:
            return False

    def login(self, username: str, password: str, remember_me: bool = False) -> bool:
        """Perform login with given credentials"""
        self.logger.info(f"Starting login process with username: {username}")
        try:
            # Navigate to login screen
            self.navigate_to_login()

            # Enter credentials
            self.enter_username(username)
            self.enter_password(password)
            
            # Toggle remember me if needed
            if remember_me:
                self.toggle_remember_me()
            
            # Click login
            self.click_login()
            
            # Check for error message first
            try:
                error_message = self.get_error_message()
                if error_message:
                    self.logger.info(f"Login failed with error: {error_message}")
                    return False
            except Exception as e:
                self.logger.info(f"No error message found: {str(e)}")
                
            # Only proceed with post-login checks if no error message was found
            try:
                self.handle_save_password_dialog()
                self.handle_reading_list_sync()
                
                # Verify login was successful
                for attempt in range(3):  # Try up to 3 times
                    if self.is_logged_in:
                        self.logger.info("Login successful")
                        return True
                    self._wait_for_element(self.locators.PROFILE_BUTTON, timeout=2)

                self.logger.error("Login verification failed")
                self.logger.info("Current page source:")
                self.logger.info(self.driver.page_source)
                return False

            except Exception as e:
                self.logger.error(f"Login verification failed: {str(e)}")
                self.logger.info("Current page source:")
                self.logger.info(self.driver.page_source)
                return False
            
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            self.logger.info("Current page source:")
            self.logger.info(self.driver.page_source)
            raise

    def logout(self) -> None:
        """Logs out the current user by clicking the profile button, then the Log out button, and confirming."""
        try:
            # Click the profile button
            logging.info("Looking for profile button")
            profile_button = self._wait_for_visible(self.locators.PROFILE_BUTTON)
            
            # Scroll to make profile button visible if needed
            if not profile_button.is_displayed():
                logging.info("Profile button not visible, attempting to scroll")
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                profile_button = self._wait_for_visible(self.locators.PROFILE_BUTTON)
            
            logging.info("Clicking profile button")
            self._safe_click(self.locators.PROFILE_BUTTON)
            
            # Now look for the logout button
            logging.info("Looking for logout button")
            logout_button = self._wait_for_visible(self.locators.LOGOUT_BUTTON)
            
            if not logout_button.is_displayed():
                logging.info("Logout button not visible, attempting to scroll")
                self.driver.execute_script("mobile: scroll", {"direction": "up"})
                logout_button = self._wait_for_visible(self.locators.LOGOUT_BUTTON)
            
            logging.info("Clicking logout button")
            self._safe_click(self.locators.LOGOUT_BUTTON)
            
            # Handle confirmation dialog if present
            try:
                confirm_logout = self._wait_for_visible(self.locators.CONFIRM_LOGOUT_BUTTON, timeout=5)
                if confirm_logout.is_displayed():
                    logging.info("Clicking confirm logout button")
                    self._safe_click(self.locators.CONFIRM_LOGOUT_BUTTON)
            except TimeoutException:
                logging.info("No confirmation dialog found")
            
            # Verify logout was successful
            try:
                login_button = self._wait_for_visible(self.locators.LOGIN_BUTTON, timeout=10)
                if login_button.is_displayed():
                    logging.info("Logout successful")
                    return True
            except TimeoutException:
                logging.error("Could not verify logout success")
                raise Exception("Logout verification failed")
                
        except Exception as e:
            logging.error(f"Logout failed: {str(e)}")
            self.driver.get_screenshot_as_file("logout_failure.png")
            logging.info("Current page source:")
            logging.info(self.driver.page_source)
            raise

    def get_error_message(self) -> Optional[str]:
        """Get the error message displayed on the login page."""
        self.logger.info("Waiting for error message to appear...")
        try:
            error_element = self._wait_for_element(('xpath', '//XCUIElementTypeStaticText[contains(@value, "Incorrect") or contains(@value, "error") or contains(@value, "invalid")]'), timeout=5)
            if error_element:
                message = error_element.text
                self.logger.info(f"Found error message: {message}")
                return message
            else:
                self.logger.warning("Error element found but could not get text")
                return None
        except TimeoutException:
            self.logger.error(f"Timeout waiting for element: {self.locators.ERROR_MESSAGE}")
            self.logger.info("Current page source:")
            self.logger.info(self.driver.page_source)
            return None
        except Exception as e:
            self.logger.error(f"Error getting error message: {str(e)}")
            self.logger.info("Current page source:")
            self.logger.info(self.driver.page_source)
            return None

    def is_on_login_page(self) -> bool:
        """Check if we are currently on the login page by looking for the 'Log in to your account' text"""
        self.logger.info("Checking if we are on the login page")
        try:
            login_header = ('xpath', '//XCUIElementTypeStaticText[@name="Log in to your account"]')
            header_element = self._wait_for_visible(login_header, timeout=5)
            return header_element.is_displayed()
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.info(f"Not on login page: {str(e)}")
            return False

    def is_login_button_disabled(self) -> bool:
        """Check if the login button is disabled"""
        try:
            login_button = self._wait_for_visible(self.locators.LOGIN_SUBMIT_BUTTON)
            if not login_button:
                return False
            
            # On iOS, we need to check both enabled and clickable states
            is_enabled = login_button.is_enabled()
            is_clickable = login_button.is_displayed() and login_button.get_attribute('enabled') == 'true'
            
            self.logger.info(f"Login button enabled status: {is_enabled}, clickable: {is_clickable}")
            return not (is_enabled and is_clickable)
            
        except Exception as e:
            self.logger.error(f"Error checking login button state: {str(e)}")
            return False

    def clear_all_possible_inputs(self) -> Dict[str, int]:
        """Clear all possible input fields on the page"""
        try:
            # Find all possible input fields
            input_fields = self._find_all_input_fields()
            stats = {
                'fields_found': len(input_fields),
                'fields_cleared': 0,
                'fields_failed': 0
            }
            
            # Clear each field
            for field in input_fields:
                try:
                    field.clear()
                    stats['fields_cleared'] += 1
                except Exception as e:
                    self.logger.error(f"Failed to clear field: {str(e)}")
                    stats['fields_failed'] += 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error clearing fields: {str(e)}")
            return {'fields_found': 0, 'fields_cleared': 0, 'fields_failed': 0}

    def _find_all_input_fields(self) -> List[WebDriver]:
        """Find all possible input fields"""
        try:
            # Find all text input fields
            text_fields = self.driver.find_elements(By.XPATH, '//XCUIElementTypeTextField')
            secure_fields = self.driver.find_elements(By.XPATH, '//XCUIElementTypeSecureTextField')
            
            # Combine all fields
            all_fields = text_fields + secure_fields
            return all_fields
            
        except Exception as e:
            self.logger.error(f"Error finding input fields: {str(e)}")
            return [] 