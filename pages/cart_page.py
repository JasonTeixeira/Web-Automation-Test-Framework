"""
Shopping Cart page object for Sauce Demo application.
"""
from typing import List

from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the shopping cart page."""
    
    # Locators
    CART_LIST = '.cart_list'
    CART_ITEM = '.cart_item'
    CART_ITEM_NAME = '.inventory_item_name'
    CART_ITEM_PRICE = '.inventory_item_price'
    CART_ITEM_DESC = '.inventory_item_desc'
    CART_QUANTITY = '.cart_quantity'
    REMOVE_BUTTON = '[data-test^="remove"]'
    CONTINUE_SHOPPING_BUTTON = '[data-test="continue-shopping"]'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    SHOPPING_CART_BADGE = '.shopping_cart_badge'
    
    def __init__(self, page: Page):
        """
        Initialize cart page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = f"{settings.base_url}/cart.html"
    
    def is_loaded(self) -> bool:
        """
        Check if cart page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return 'cart.html' in self.get_url()
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart.
        
        Returns:
            Number of items
        """
        return self.get_element_count(self.CART_ITEM)
    
    def get_all_item_names(self) -> List[str]:
        """
        Get names of all items in cart.
        
        Returns:
            List of item names
        """
        return self.get_all_texts(self.CART_ITEM_NAME)
    
    def get_all_item_prices(self) -> List[float]:
        """
        Get prices of all items in cart.
        
        Returns:
            List of prices as floats
        """
        price_texts = self.get_all_texts(self.CART_ITEM_PRICE)
        return [float(price.replace('$', '')) for price in price_texts]
    
    def get_total_price(self) -> float:
        """
        Calculate total price of all items in cart.
        
        Returns:
            Total price
        """
        return sum(self.get_all_item_prices())
    
    def remove_item_by_name(self, product_name: str) -> None:
        """
        Remove an item from cart by name.
        
        Args:
            product_name: Name of the product
        """
        self.logger.info(f"Removing item from cart: {product_name}")
        button_id = f'remove-{product_name.lower().replace(" ", "-")}'
        self.click(f'[data-test="{button_id}"]')
    
    def remove_item_by_index(self, index: int) -> None:
        """
        Remove an item from cart by index.
        
        Args:
            index: Zero-based index
        """
        self.logger.info(f"Removing item at index {index}")
        remove_buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(remove_buttons):
            remove_buttons[index].click()
    
    def continue_shopping(self) -> None:
        """Click continue shopping button."""
        self.logger.info("Continuing shopping")
        self.click(self.CONTINUE_SHOPPING_BUTTON)
    
    def proceed_to_checkout(self) -> None:
        """Click checkout button."""
        self.logger.info("Proceeding to checkout")
        self.click(self.CHECKOUT_BUTTON)
    
    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty.
        
        Returns:
            True if empty, False otherwise
        """
        return self.get_cart_item_count() == 0
    
    def is_item_in_cart(self, product_name: str) -> bool:
        """
        Check if specific item is in cart.
        
        Args:
            product_name: Name of the product
            
        Returns:
            True if item is in cart, False otherwise
        """
        item_names = self.get_all_item_names()
        return product_name in item_names
    
    def get_item_quantity(self, index: int = 0) -> int:
        """
        Get quantity of an item.
        
        Args:
            index: Zero-based index of the item
            
        Returns:
            Item quantity
        """
        quantities = self.page.locator(self.CART_QUANTITY).all()
        if index < len(quantities):
            qty_text = quantities[index].text_content() or "1"
            return int(qty_text)
        return 0
    
    def remove_all_items(self) -> None:
        """Remove all items from cart."""
        self.logger.info("Removing all items from cart")
        while self.get_cart_item_count() > 0:
            self.remove_item_by_index(0)
    
    def get_cart_badge_count(self) -> int:
        """
        Get count from shopping cart badge.
        
        Returns:
            Badge count (0 if not visible)
        """
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000):
            count_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(count_text)
        return 0
