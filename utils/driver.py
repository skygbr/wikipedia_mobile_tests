from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import logging
import time
from dotenv import load_dotenv
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

def retry_on_failure(max_attempts=3, delay=1):
    """
    Decorator for retrying methods on failure
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {str(e)}")
                        raise
                    logger.warning(f"Attempt {attempts} failed, retrying in {delay} seconds...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class Driver:
    def __init__(self, platform="ios"):
        self.platform = platform
        self.driver = None
        self.wait = None
        logger.info(f"Initializing driver for platform: {platform}")

    def init_driver(self):
        """
        Initialize the Appium driver with platform-specific capabilities
        """
        try:
            if self.platform == "ios":
                options = XCUITestOptions()
                options.platform_name = 'iOS'
                options.platform_version = '18.3'
                options.device_name = 'iPhone 14 Pro Max'
                options.automation_name = 'XCUITest'
                options.app = os.path.abspath('apps/Wikipedia.app')
                options.no_reset = True
                options.new_command_timeout = 60
                options.wda_local_port = 8100
                options.wda_connection_timeout = 180000
                options.show_xcode_log = True
                options.show_ios_log = True
            else:
                options = UiAutomator2Options()
                options.platform_name = 'Android'
                options.platform_version = '13.0'
                options.device_name = 'Pixel 6'
                options.automation_name = 'UiAutomator2'
                options.app = os.path.abspath('apps/Wikipedia.apk')
                options.no_reset = True
                options.auto_grant_permissions = True
                options.new_command_timeout = 60
                options.android_install_timeout = 90000
                options.adb_exec_timeout = 60000
                options.uiautomator2_server_install_timeout = 60000
                options.uiautomator2_server_launch_timeout = 60000
                options.system_port = 8200

            logger.info(f"Connecting to Appium server with options: {options.to_capabilities()}")
            self.driver = webdriver.Remote('http://127.0.0.1:4723', options=options)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Driver initialized successfully")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to initialize driver: {str(e)}")
            raise

    @retry_on_failure(max_attempts=3, delay=1)
    def wait_for_element(self, locator, timeout=10, condition=EC.presence_of_element_located):
        """
        Wait for an element to be present on the page with retry mechanism
        """
        try:
            logger.debug(f"Waiting for element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(condition(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {locator}")
            raise
        except Exception as e:
            logger.error(f"Error waiting for element {locator}: {str(e)}")
            raise

    def is_element_present(self, locator, timeout=5):
        """
        Check if an element is present on the page
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def take_screenshot(self, name):
        """
        Take a screenshot and save it with timestamp
        """
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshots/{name}_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.get_screenshot_as_file(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def quit(self):
        """
        Safely quit the driver
        """
        if self.driver:
            try:
                logger.info("Quitting driver")
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error quitting driver: {str(e)}")
            finally:
                self.driver = None 