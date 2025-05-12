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
import requests

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
                options.webdriver_agent_url = 'http://localhost:8100'
                options.derived_data_path = os.path.expanduser('~/Library/Developer/Xcode/DerivedData')
                options.use_new_wda = True
                options.use_simple_build_test = True
                
                # Find and set WebDriverAgent path
                wda_path = self.find_wda_path()
                if wda_path:
                    options.webdriver_agent_path = wda_path
                    logger.info(f"Using WebDriverAgent from: {wda_path}")
                else:
                    logger.warning("Could not find WebDriverAgent path, using default")
                
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

    def before_test(self):
        """
        Prepare the test environment by launching Wikipedia app in simulator
        """
        try:
            logger.info("Starting Wikipedia app in simulator")
            if self.platform == "ios":
                # Launch simulator if not already running
                simulator_id = "6D346A21-DB65-45A1-AEEE-0CD3925B13F2"  # iPhone 14 Pro Max
                os.system(f'xcrun simctl boot {simulator_id}')
                time.sleep(5)  # Wait for simulator to boot
                
                # Initialize driver if not already initialized
                if not self.driver:
                    self.init_driver()
                
                # Check WebDriverAgent status
                if not self.check_wda_status():
                    logger.error("WebDriverAgent is not running properly")
                    raise Exception("WebDriverAgent is not running properly")
                
                # Launch Wikipedia app
                os.system(f'xcrun simctl launch {simulator_id} org.wikimedia.wikipedia')
                logger.info("Wikipedia app launched successfully")
            else:
                # Android implementation
                if not self.driver:
                    self.init_driver()
                self.driver.activate_app('org.wikimedia.wikipedia')
                logger.info("Wikipedia app launched successfully on Android")
                
        except Exception as e:
            logger.error(f"Failed to launch Wikipedia app: {str(e)}")
            raise

    def check_wda_status(self):
        """
        Check if WebDriverAgent is running and accessible
        """
        try:
            response = requests.get('http://localhost:8100/status')
            if response.status_code == 200:
                logger.info("WebDriverAgent is running and accessible")
                return True
            else:
                logger.error(f"WebDriverAgent returned status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Failed to check WebDriverAgent status: {str(e)}")
            return False

    def find_wda_path(self):
        """
        Find the exact path to WebDriverAgent
        """
        try:
            # Common paths where WebDriverAgent might be located
            possible_paths = [
                os.path.expanduser('~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug-iphonesimulator/WebDriverAgentRunner-Runner.app'),
                os.path.expanduser('~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*/Build/Products/Debug/WebDriverAgentRunner-Runner.app'),
                '/usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj',
                os.path.expanduser('~/Library/Developer/Xcode/DerivedData/WebDriverAgent-*')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    logger.info(f"Found WebDriverAgent at: {path}")
                    return path
                
            logger.error("WebDriverAgent not found in common locations")
            return None
        except Exception as e:
            logger.error(f"Error finding WebDriverAgent path: {str(e)}")
            return None

    def after_test(self):
        """
        Clean up after the test by clicking Cancel and closing the app
        """
        try:
            logger.info("Starting test cleanup")
            if self.platform == "ios":
                # Try to find and click Cancel button if present
                try:
                    cancel_button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Cancel")
                    if cancel_button.is_displayed():
                        cancel_button.click()
                        logger.info("Clicked Cancel button")
                        time.sleep(1)  # Wait for the action to complete
                except NoSuchElementException:
                    logger.info("Cancel button not found, proceeding with app termination")
                
                # Terminate the Wikipedia app
                simulator_id = "6D346A21-DB65-45A1-AEEE-0CD3925B13F2"  # iPhone 14 Pro Max
                os.system(f'xcrun simctl terminate {simulator_id} org.wikimedia.wikipedia')
                logger.info("Wikipedia app terminated successfully")
            
            # Quit the driver
            self.quit()
            
        except Exception as e:
            logger.error(f"Error during test cleanup: {str(e)}")
            # Ensure driver is quit even if there's an error
            self.quit()

    def setUp(self):
        """
        Initialize the driver and prepare the test environment
        """
        if not self.driver:
            self.init_driver()
        self.before_test() 