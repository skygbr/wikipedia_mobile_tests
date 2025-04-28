import pytest
import allure
import os
import logging
import time
from utils.driver import Driver

# Register custom markers
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "android: mark test to run on Android platform"
    )
    config.addinivalue_line(
        "markers", "ios: mark test to run on iOS platform"
    )

# Configure logging
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to initialize and cleanup the Appium driver
    """
    platform = request.config.getoption("--platform", default="ios")
    logger.info(f"Initializing driver for platform: {platform}")
    
    driver_instance = Driver(platform=platform)
    driver = driver_instance.init_driver()
    
    # Add environment information to Allure report
    env_info = {
        'platform': platform,
        'app_version': driver.capabilities.get('appVersion', 'Unknown'),
        'device_name': driver.capabilities.get('deviceName', 'Unknown'),
        'platform_version': driver.capabilities.get('platformVersion', 'Unknown')
    }
    allure.attach(
        str(env_info),
        name='environment',
        attachment_type=allure.attachment_type.TEXT
    )
    
    # Log test start
    logger.info(f"Starting test: {request.node.name}")
    
    yield driver
    
    # Log test end
    logger.info(f"Ending test: {request.node.name}")
    
    # Cleanup
    driver_instance.quit()

def pytest_addoption(parser):
    """
    Add command line options for the test suite
    """
    parser.addoption(
        "--platform",
        action="store",
        default="ios",
        help="platform to run tests on (ios or android)"
    )
    
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="run tests in headless mode"
    )
    
    parser.addoption(
        "--screenshot-on-failure",
        action="store_true",
        default=True,
        help="take screenshots on test failure"
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to add screenshots and logs to Allure report on test failure
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver')
        if driver and hasattr(driver, 'save_screenshot'):
            driver.save_screenshot(f"screenshots/failure_{item.name}.png")
        
        # Add test logs to report
        if hasattr(item, "_test_logs"):
            allure.attach(
                item._test_logs,
                name="test_logs",
                attachment_type=allure.attachment_type.TEXT
            )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """
    Hook to set up test environment
    """
    # Start time for test
    start_time = time.time()
    
    yield
    
    # Calculate test duration
    duration = time.time() - start_time
    
    # Add test duration to Allure report
    allure.attach(
        f"Test duration: {duration:.2f} seconds",
        name="test_duration",
        attachment_type=allure.attachment_type.TEXT
    )

def pytest_collection_modifyitems(items):
    """
    Modify test collection to add markers and organize tests
    """
    for item in items:
        # Add platform marker based on test name or other criteria
        if "android" in item.name.lower():
            item.add_marker(pytest.mark.android)
        elif "ios" in item.name.lower():
            item.add_marker(pytest.mark.ios)
        else:
            # Default to both platforms if not specified
            item.add_marker(pytest.mark.android)
            item.add_marker(pytest.mark.ios) 