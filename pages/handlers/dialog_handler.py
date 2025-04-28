from .base_handler import BaseHandler
from selenium.common.exceptions import TimeoutException

class DialogHandler(BaseHandler):
    """Handler for managing dialog windows"""
    
    def __init__(self, driver, logger, locators):
        super().__init__(driver, logger)
        self.locators = locators
        
    def handle_save_password_dialog(self) -> None:
        """Handle the save password dialog if it appears and any additional dialog windows"""
        self.logger.info("Handling save password dialog")
        try:
            save_dialog = self._wait_for_visible(self.locators.SAVE_PASSWORD_DIALOG, timeout=5)
            if save_dialog and save_dialog.is_displayed():
                save_button = self._wait_for_clickable(self.locators.SAVE_PASSWORD_BUTTON)
                if save_button:
                    save_button.click()
                    self._handle_additional_dialog()
                    
        except TimeoutException:
            self.logger.info("Save password dialog did not appear")
        except Exception as e:
            self.logger.error(f"Failed to handle save password dialog: {str(e)}")
            
    def handle_reading_list_sync(self) -> None:
        """Handle the reading list sync dialog if it appears"""
        self.logger.info("Handling reading list sync dialog")
        try:
            sync_dialog = self._wait_for_visible(self.locators.READING_LIST_SYNC_DIALOG, timeout=5)
            if sync_dialog and sync_dialog.is_displayed():
                sync_button = self._wait_for_clickable(self.locators.READING_LIST_SYNC_BUTTON)
                if sync_button:
                    sync_button.click()
                    self._handle_additional_dialog()
                    
        except TimeoutException:
            self.logger.info("Reading list sync dialog did not appear")
        except Exception as e:
            self.logger.error(f"Failed to handle reading list sync dialog: {str(e)}")
            
    def _handle_additional_dialog(self) -> None:
        """Handle any additional dialog window that might appear"""
        try:
            close_button = self._wait_for_visible(self.locators.DIALOG_CLOSE_BUTTON, timeout=5)
            if close_button and close_button.is_displayed():
                self.logger.info("Found additional dialog window, clicking close button")
                close_button.click()
        except Exception as e:
            self.logger.info(f"No additional dialog window found: {str(e)}") 