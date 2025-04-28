from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

class AuthPageLocators:
    """Locators for authentication page elements"""
    
    # Login page elements
    LOGIN_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Log in / Join Wikipedia"]')
    USERNAME_FIELD = (By.XPATH, '//XCUIElementTypeTextField[contains(@name, "username") or @value="enter username" or @value="AutotestUsr" or @value="nonexistent_user"]')
    PASSWORD_FIELD = (By.XPATH, '//XCUIElementTypeSecureTextField[contains(@name, "password") or @value="enter password" or @value="AutotestPwd" or @value="wrong_password"]')
    REMEMBER_ME_CHECKBOX = (By.XPATH, '//XCUIElementTypeButton[@name="Remember me"]')
    LOGIN_SUBMIT_BUTTON = (By.XPATH, '//XCUIElementTypeButton[contains(@name, "Log in") or @name="Log in" or @label="Log in"]')
    
    # Profile and logout elements
    PROFILE_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="profile-button"]')
    LOGOUT_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Log out"]')
    CONFIRM_LOGOUT_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Log out"]')
    
    # Dialog elements
    SAVE_PASSWORD_DIALOG = (By.XPATH, '//XCUIElementTypeAlert[@name="Save Password?"]')
    SAVE_PASSWORD_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Save Password"]')
    SAVE_PASSWORD_NOT_NOW = (By.XPATH, '//XCUIElementTypeButton[@name="Not Now"]')
    READING_LIST_SYNC_DIALOG = (By.XPATH, '//XCUIElementTypeAlert[@name="Reading list sync"]')
    READING_LIST_SYNC_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Turn on"]')
    
    # Other UI elements
    DONE_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Done"]')
    NEXT_KEYBOARD_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Next keyboard"]')
    ERROR_MESSAGE = (AppiumBy.XPATH, '//XCUIElementTypeStaticText[contains(@name, "error") or contains(@name, "incorrect") or contains(@name, "invalid")]')
    CAPTCHA_TEXT = (By.XPATH, '//XCUIElementTypeStaticText[contains(@name, "CAPTCHA security check")]')
    CAPTCHA_CANCEL_BUTTON = (By.XPATH, '//XCUIElementTypeButton[@name="Cancel"]') 