from .base_handler import BaseHandler
from selenium.common.exceptions import TimeoutException

class KeyboardHandler(BaseHandler):
    """Handler for managing keyboard interactions"""
    
    def __init__(self, driver, logger, locators):
        super().__init__(driver, logger)
        self.locators = locators
        
    def switch_to_english_keyboard(self) -> bool:
        """Switch to English keyboard if needed
        
        Returns:
            bool: True if switched to English keyboard, False otherwise
        """
        try:
            next_keyboard = self._wait_for_visible(self.locators.NEXT_KEYBOARD_BUTTON, timeout=3)
            if next_keyboard and next_keyboard.is_displayed():
                keyboard_value = next_keyboard.get_attribute('value')
                if keyboard_value == 'English (US)':
                    self.logger.info("Switching to English keyboard")
                    next_keyboard.click()
                    return True
            return False
        except TimeoutException:
            self.logger.info("No keyboard switch button found")
            return False
        except Exception as e:
            self.logger.error(f"Error switching keyboard: {str(e)}")
            return False
            
    def clear_field_with_backspace(self, field, attempts: int = 3) -> None:
        """Clear a field using backspace key
        
        Args:
            field: The input field to clear
            attempts: Number of backspace attempts
        """
        try:
            field.clear()
            for _ in range(attempts):
                field.send_keys("\b")  # Backspace character
        except Exception as e:
            self.logger.error(f"Error clearing field with backspace: {str(e)}") 