"""
Checkout page objects for Sauce Demo application.
Includes CheckoutStepOnePage, CheckoutStepTwoPage, and CheckoutCompletePage.
"""
from typing import List, Optional

from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Page object for checkout step one (information entry)."""
    
    # Locators
    FIRST_NAME_INPUT = '[data-test="firstName"]'
    LAST_NAME_INPUT = '[data-test="lastName"]'
    POSTAL_CODE_INPUT = '[data-test="postalCode"]'
    CONTINUE_BUTTON = '[data-test="continue"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    ERROR_MESSAGE = '[data-test="error"]'
    ERROR_BUTTON = '.error-button'
    
    def __init__(self, page: Page):
        """
        Initialize checkout step one page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = f"{settings.base_url}/checkout-step-one.html"
    
    def is_loaded(self) -> bool:
        """
        Check if page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return 'checkout-step-one' in self.get_url()
    
    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Fill all checkout information fields.
        
        Args:
            first_name: First name
            last_name: Last name
            postal_code: Postal code
        """
        self.logger.info(f"Filling checkout info: {first_name} {last_name}, {postal_code}")
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
    
    def enter_first_name(self, first_name: str) -> None:
        """Enter first name."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """Enter last name."""
        self.fill(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code: str) -> None:
        """Enter postal code."""
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
    
    def click_continue(self) -> None:
        """Click continue button."""
        self.click(self.CONTINUE_BUTTON)
    
    def click_cancel(self) -> None:
        """Click cancel button."""
        self.click(self.CANCEL_BUTTON)
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Check if error is displayed.
        
        Returns:
            True if error visible, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=2000)
    
    def close_error_message(self) -> None:
        """Close error message."""
        self.click(self.ERROR_BUTTON)
    
    def clear_all_fields(self) -> None:
        """Clear all input fields."""
        self.page.locator(self.FIRST_NAME_INPUT).clear()
        self.page.locator(self.LAST_NAME_INPUT).clear()
        self.page.locator(self.POSTAL_CODE_INPUT).clear()


class CheckoutStepTwoPage(BasePage):
    """Page object for checkout step two (overview/confirmation)."""
    
    # Locators
    CART_ITEM = '.cart_item'
    CART_ITEM_NAME = '.inventory_item_name'
    CART_ITEM_PRICE = '.inventory_item_price'
    SUMMARY_SUBTOTAL = '.summary_subtotal_label'
    SUMMARY_TAX = '.summary_tax_label'
    SUMMARY_TOTAL = '.summary_total_label'
    FINISH_BUTTON = '[data-test="finish"]'
    CANCEL_BUTTON = '[data-test="cancel"]'
    PAYMENT_INFO = '.summary_value_label:nth-of-type(2)'
    SHIPPING_INFO = '.summary_value_label:nth-of-type(4)'
    
    def __init__(self, page: Page):
        """
        Initialize checkout step two page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = f"{settings.base_url}/checkout-step-two.html"
    
    def is_loaded(self) -> bool:
        """
        Check if page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return 'checkout-step-two' in self.get_url()
    
    def get_item_count(self) -> int:
        """
        Get number of items in order.
        
        Returns:
            Item count
        """
        return self.get_element_count(self.CART_ITEM)
    
    def get_all_item_names(self) -> List[str]:
        """
        Get all item names.
        
        Returns:
            List of item names
        """
        return self.get_all_texts(self.CART_ITEM_NAME)
    
    def get_all_item_prices(self) -> List[float]:
        """
        Get all item prices.
        
        Returns:
            List of prices
        """
        price_texts = self.get_all_texts(self.CART_ITEM_PRICE)
        return [float(price.replace('$', '')) for price in price_texts]
    
    def get_subtotal(self) -> float:
        """
        Get subtotal amount.
        
        Returns:
            Subtotal
        """
        text = self.get_text(self.SUMMARY_SUBTOTAL)
        # Extract number from "Item total: $XX.XX"
        return float(text.split('$')[1])
    
    def get_tax(self) -> float:
        """
        Get tax amount.
        
        Returns:
            Tax amount
        """
        text = self.get_text(self.SUMMARY_TAX)
        # Extract number from "Tax: $X.XX"
        return float(text.split('$')[1])
    
    def get_total(self) -> float:
        """
        Get total amount.
        
        Returns:
            Total amount
        """
        text = self.get_text(self.SUMMARY_TOTAL)
        # Extract number from "Total: $XX.XX"
        return float(text.split('$')[1])
    
    def verify_total_calculation(self) -> bool:
        """
        Verify that subtotal + tax = total.
        
        Returns:
            True if calculation is correct, False otherwise
        """
        subtotal = self.get_subtotal()
        tax = self.get_tax()
        total = self.get_total()
        calculated_total = round(subtotal + tax, 2)
        return abs(calculated_total - total) < 0.01  # Allow for small floating point errors
    
    def click_finish(self) -> None:
        """Click finish button to complete order."""
        self.logger.info("Completing order")
        self.click(self.FINISH_BUTTON)
    
    def click_cancel(self) -> None:
        """Click cancel button."""
        self.click(self.CANCEL_BUTTON)
    
    def get_payment_info(self) -> str:
        """
        Get payment information.
        
        Returns:
            Payment info text
        """
        return self.get_text(self.PAYMENT_INFO)
    
    def get_shipping_info(self) -> str:
        """
        Get shipping information.
        
        Returns:
            Shipping info text
        """
        return self.get_text(self.SHIPPING_INFO)


class CheckoutCompletePage(BasePage):
    """Page object for checkout complete (success) page."""
    
    # Locators
    COMPLETE_HEADER = '.complete-header'
    COMPLETE_TEXT = '.complete-text'
    PONY_EXPRESS_IMAGE = '.pony_express'
    BACK_HOME_BUTTON = '[data-test="back-to-products"]'
    
    def __init__(self, page: Page):
        """
        Initialize checkout complete page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = f"{settings.base_url}/checkout-complete.html"
    
    def is_loaded(self) -> bool:
        """
        Check if page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return 'checkout-complete' in self.get_url()
    
    def get_complete_header(self) -> str:
        """
        Get completion header text.
        
        Returns:
            Header text
        """
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self) -> str:
        """
        Get completion message text.
        
        Returns:
            Completion message
        """
        return self.get_text(self.COMPLETE_TEXT)
    
    def is_success_image_visible(self) -> bool:
        """
        Check if success image is visible.
        
        Returns:
            True if visible, False otherwise
        """
        return self.is_visible(self.PONY_EXPRESS_IMAGE)
    
    def click_back_home(self) -> None:
        """Click back home button."""
        self.logger.info("Returning to products page")
        self.click(self.BACK_HOME_BUTTON)
    
    def is_order_complete(self) -> bool:
        """
        Verify order completion by checking for success elements.
        
        Returns:
            True if order is complete, False otherwise
        """
        return (
            self.is_loaded() and
            self.is_visible(self.COMPLETE_HEADER) and
            self.is_success_image_visible()
        )
