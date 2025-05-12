import pytest
import allure
import logging
import time
from pages.auth_page import AuthPage
import os
from dotenv import load_dotenv
from datetime import datetime
from selenium.webdriver.common.by import By
from utils.driver import Driver

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

# Test data
VALID_USERNAME = os.getenv('WIKIPEDIA_USERNAME')
VALID_PASSWORD = os.getenv('WIKIPEDIA_PASSWORD')
INVALID_USERNAME = "nonexistent_user"
INVALID_PASSWORD = "wrong_password"

@allure.epic("Wikipedia Mobile App")
@allure.feature("Authentication")
class TestAuthentication:
    @allure.story("Test Setup")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Initialize test environment")
    def before_test(self):
        """Initialize test environment before each test"""
        driver_instance = Driver(platform="ios")
        driver_instance.driver = self.driver
        driver_instance.setUp()

    @allure.story("Test Cleanup")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Clean up test environment")
    def after_test(self):
        """Clean up test environment after each test"""
        driver_instance = Driver(platform="ios")
        driver_instance.driver = self.driver
        driver_instance.after_test()

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture that runs before each test
        """
        self.driver = driver
        self.auth_page = AuthPage(driver)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Test setup completed")
        
        # Initialize test environment
        self.before_test()
        
        yield
        
        self.logger.info("Test cleanup started")
        # Teardown: logout after each test only if logged in
        try:
            # First check if we're on the login page
            if self.auth_page.is_on_login_page():
                self.logger.info("Already on login page, no cleanup needed")
            # If not on login page, check if logged in
            elif self.auth_page.is_logged_in:
                self.logger.info("User is logged in, performing logout")
                self.auth_page.logout()
            else:
                self.logger.info("User is not logged in and not on login page, no cleanup needed")
        except Exception as e:
            self.logger.warning(f"Cleanup encountered an issue: {str(e)}")
        self.logger.info("Test cleanup completed")

    @allure.story("Login Functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test successful login with valid credentials")
    def test_successful_login(self, driver):
        """Test successful login with valid credentials"""
        self.auth_page.login(
            username=VALID_USERNAME,
            password=VALID_PASSWORD
        )
        
        # Take screenshot of successful login
        driver.save_screenshot("screenshots/successful_login.png")
        
        # Verify successful login
        assert self.auth_page.is_logged_in

    @allure.story("Login Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login with invalid password shows error message")
    def test_invalid_password(self):
        """Test login attempt with an invalid password.
        
        This test verifies that:
        1. Login fails when using an invalid password
        2. An appropriate error message is displayed
        3. User remains on the login page
        4. A screenshot is captured for debugging
        """
        self.logger.info("Starting invalid password test")
        
        # Attempt login with invalid password
        self.auth_page.login(username=VALID_USERNAME, password=INVALID_PASSWORD)
        self.logger.info("Login attempt made with invalid password")
        
        # Verify error message
        error_msg = self.auth_page.get_error_message()
        self.logger.info(f"Received error message: {error_msg}")
        assert error_msg is not None, "Error message should be displayed"
        assert "incorrect" in error_msg.lower(), f"Error message should mention 'incorrect', got: {error_msg}"
        
        # Verify we're still on login page
        assert self.auth_page.is_on_login_page(), "User should remain on login page after failed attempt"
        
        # Capture screenshot for debugging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.driver.save_screenshot(f"failed_login_{timestamp}.png")
        self.logger.info("Screenshot captured of failed login attempt")

    @allure.story("Login Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login with invalid username")
    def test_invalid_username(self):
        """Test login with invalid username"""
        self.logger.info("Starting test: Login with invalid username")
        try:
            # Comprehensive field clearing before test
            self.logger.info("Clearing all possible input fields before test")
            clearing_stats = self.auth_page.clear_all_possible_inputs()
            self.logger.info(f"Field clearing stats: {clearing_stats}")
            
            # Enter invalid username
            self.auth_page.enter_username("invalid_user")
            self.auth_page.enter_password(VALID_PASSWORD)
            
            # Click login and verify error message
            self.logger.info("Clicking login button")
            self.auth_page.click_login()
            
            # Wait for error message with increased timeout
            self.logger.info("Waiting for error message")
            error_message = self.auth_page.get_error_message()
            assert error_message is not None, "Error message should be displayed"
            assert "incorrect" in error_message.lower(), "Error message should contain 'incorrect'"
            
            # Verify we're still on login page
            assert self.auth_page.is_on_login_page(), "Should remain on login page"
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            self.driver.save_screenshot("invalid_username_error.png")
            raise

    @allure.story("Login Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test login button is disabled with empty credentials")
    def test_empty_credentials(self):
        """Test that login button is disabled with empty credentials"""
        self.logger.info("Starting test_empty_credentials")
        try:
            # Handle CAPTCHA security check if present
            try:
                captcha_text = self.driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[contains(@name, "CAPTCHA security check")]')
                if captcha_text.is_displayed():
                    self.logger.info("Found CAPTCHA security check text, looking for Cancel button")
                    captcha_button = self.driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="Cancel"]')
                    if captcha_button.is_displayed():
                        self.logger.info("Clicking Cancel button for CAPTCHA")
                        captcha_button.click()
            except:
                self.logger.info("No CAPTCHA security check found")

            # Handle Save Password dialog if present
            try:
                save_password_dialog = self.driver.find_element(By.XPATH, '//XCUIElementTypeAlert[@name="Save Password?"]')
                if save_password_dialog.is_displayed():
                    self.logger.info("Found Save Password dialog, clicking Not Now")
                    not_now_button = self.driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="Not Now"]')
                    not_now_button.click()
            except:
                self.logger.info("No Save Password dialog found")

            # Navigate back to login page if needed
            if not self.auth_page.is_on_login_page():
                self.logger.info("Navigating back to login page")
                self.auth_page.navigate_to_login()

            # Comprehensive field clearing before test
            self.logger.info("Clearing all possible input fields before test")
            clearing_stats = self.auth_page.clear_all_possible_inputs()
            self.logger.info(f"Field clearing stats: {clearing_stats}")
            
            # Verify login button is disabled
            assert self.auth_page.is_login_button_disabled(), "Login button should be disabled with empty credentials"
            
            # Take screenshot for debugging
            self.driver.save_screenshot("empty_credentials.png")
            self.logger.info("Test completed successfully")
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            self.driver.save_screenshot("empty_credentials_error.png")
            raise
        finally:
            self.after_test()

    @allure.story("Login Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test remember me functionality")
    def test_remember_me(self, driver):
        """Test remember me functionality"""
        self.logger.info("Perform login with remember me option")
        try:
            # Handle CAPTCHA security check if present
            try:
                captcha_text = self.driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[contains(@name, "CAPTCHA security check")]')
                if captcha_text.is_displayed():
                    self.logger.info("Found CAPTCHA security check text, looking for Cancel button")
                    captcha_button = self.driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="Cancel"]')
                    if captcha_button.is_displayed():
                        self.logger.info("Clicking Cancel button for CAPTCHA")
                        captcha_button.click()
            except:
                self.logger.info("No CAPTCHA security check found")

            # Handle Save Password dialog if present
            try:
                save_password_dialog = self.driver.find_element(By.XPATH, '//XCUIElementTypeAlert[@name="Save Password?"]')
                if save_password_dialog.is_displayed():
                    self.logger.info("Found Save Password dialog, clicking Not Now")
                    not_now_button = self.driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="Not Now"]')
                    not_now_button.click()
            except:
                self.logger.info("No Save Password dialog found")

            # Navigate back to login page if needed
            if not self.auth_page.is_on_login_page():
                self.logger.info("Navigating back to login page")
                self.auth_page.navigate_to_login()

            # Comprehensive field clearing before test
            self.logger.info("Clearing all possible input fields before test")
            clearing_stats = self.auth_page.clear_all_possible_inputs()
            self.logger.info(f"Field clearing stats: {clearing_stats}")
            
            result = self.auth_page.login(
                username=VALID_USERNAME,
                password=VALID_PASSWORD,
                remember_me=True
            )
            
            with allure.step("Verify login was successful"):
                assert result is True, "Login should be successful with remember me"
                
            # Take screenshot for remember me login
            driver.save_screenshot("screenshots/remember_me.png")
            
        except Exception as e:
            self.logger.error(f"Remember me test failed: {str(e)}")
            driver.save_screenshot("screenshots/remember_me_error.png")
            raise
            
        # Additional steps to verify remember me functionality
        # This would typically involve logging out and checking if credentials are remembered
        # Implementation depends on app behavior 