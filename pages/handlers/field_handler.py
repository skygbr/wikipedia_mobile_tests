from selenium.webdriver.common.by import By
from .base_handler import BaseHandler
from selenium.common.exceptions import TimeoutException
from typing import Dict, List, Any

class FieldHandler(BaseHandler):
    """Handler for managing input fields"""
    
    def __init__(self, driver, logger, locators):
        super().__init__(driver, logger)
        self.locators = locators
        
    def clear_all_possible_inputs(self) -> Dict[str, int]:
        """Clear all possible input fields on the page
        
        Returns:
            Dict[str, int]: Statistics about cleared fields
        """
        self.logger.info("Clearing all possible input fields")
        stats = {
            'fields_found': 0,
            'fields_cleared': 0,
            'fields_failed': 0
        }
        
        try:
            fields = self._find_all_input_fields()
            stats['fields_found'] = len(fields)
            
            for field in fields:
                try:
                    field.clear()
                    stats['fields_cleared'] += 1
                except Exception:
                    stats['fields_failed'] += 1
                    
        except Exception as e:
            self.logger.error(f"Error clearing fields: {str(e)}")
            
        return stats
        
    def _find_all_input_fields(self) -> List[Any]:
        """Find all possible input fields
        
        Returns:
            List[Any]: List of found input fields
        """
        field_types = [
            'XCUIElementTypeTextField',
            'XCUIElementTypeSecureTextField',
            'XCUIElementTypeTextView',
            'XCUIElementTypeSearchField'
        ]
        
        all_fields = []
        for field_type in field_types:
            xpath = f'//{field_type}'
            fields = self.driver.find_elements(By.XPATH, xpath)
            all_fields.extend(fields)
            
        return all_fields
        
    def verify_field_value(self, field, expected_value: str) -> bool:
        """Verify that a field has the expected value
        
        Args:
            field: The input field to check
            expected_value: The expected value
            
        Returns:
            bool: True if field has expected value, False otherwise
        """
        try:
            actual_value = field.get_attribute('value')
            if actual_value != expected_value:
                self.logger.error(f"Field value mismatch. Expected: {expected_value}, Got: {actual_value}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error verifying field value: {str(e)}")
            return False 