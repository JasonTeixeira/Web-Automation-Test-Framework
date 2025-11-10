"""
Inventory/Products page object for Sauce Demo application.
"""
from typing import List, Optional

from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for the inventory/products page."""
    
    # Locators
    INVENTORY_CONTAINER = '.inventory_container'
    INVENTORY_LIST = '.inventory_list'
    INVENTORY_ITEM = '.inventory_item'
    INVENTORY_ITEM_NAME = '.inventory_item_name'
    INVENTORY_ITEM_DESC = '.inventory_item_desc'
    INVENTORY_ITEM_PRICE = '.inventory_item_price'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart"]'
    REMOVE_BUTTON = '[data-test^="remove"]'
    SHOPPING_CART_BADGE = '.shopping_cart_badge'
    SHOPPING_CART_LINK = '.shopping_cart_link'
    PRODUCT_SORT_CONTAINER = '.product_sort_container'
    BURGER_MENU = '#react-burger-menu-btn'
    LOGOUT_LINK = '#logout_sidebar_link'
    APP_LOGO = '.app_logo'
    PEEK_IMAGE = '.peek'
    FOOTER = '.footer'
    
    # Sort options
    SORT_NAME_ASC = 'az'
    SORT_NAME_DESC = 'za'
    SORT_PRICE_ASC = 'lohi'
    SORT_PRICE_DESC = 'hilo'
    
    def __init__(self, page: Page):
        """
        Initialize inventory page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = f"{settings.base_url}/inventory.html"
    
    def is_loaded(self) -> bool:
        """
        Check if inventory page is loaded.
        
        Returns:
            True if loaded, False otherwise
        """
        return self.is_visible(self.INVENTORY_CONTAINER, timeout=10000)
    
    def get_product_count(self) -> int:
        """
        Get total number of products displayed.
        
        Returns:
            Number of products
        """
        return self.get_element_count(self.INVENTORY_ITEM)
    
    def get_all_product_names(self) -> List[str]:
        """
        Get names of all products.
        
        Returns:
            List of product names
        """
        return self.get_all_texts(self.INVENTORY_ITEM_NAME)
    
    def get_all_product_prices(self) -> List[float]:
        """
        Get prices of all products.
        
        Returns:
            List of product prices as floats
        """
        price_texts = self.get_all_texts(self.INVENTORY_ITEM_PRICE)
        return [float(price.replace('$', '')) for price in price_texts]
    
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Add a product to cart by its name.
        
        Args:
            product_name: Name of the product
        """
        self.logger.info(f"Adding product to cart: {product_name}")
        # Convert product name to button ID format
        button_id = f'add-to-cart-{product_name.lower().replace(" ", "-")}'
        self.click(f'[data-test="{button_id}"]')
    
    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """
        Remove a product from cart by its name.
        
        Args:
            product_name: Name of the product
        """
        self.logger.info(f"Removing product from cart: {product_name}")
        button_id = f'remove-{product_name.lower().replace(" ", "-")}'
        self.click(f'[data-test="{button_id}"]')
    
    def add_product_to_cart_by_index(self, index: int) -> None:
        """
        Add a product to cart by its index position.
        
        Args:
            index: Zero-based index of the product
        """
        self.logger.info(f"Adding product at index {index} to cart")
        add_buttons = self.page.locator(self.ADD_TO_CART_BUTTON).all()
        if index < len(add_buttons):
            add_buttons[index].click()
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in shopping cart from badge.
        
        Returns:
            Number of items in cart (0 if badge not visible)
        """
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000):
            count_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(count_text)
        return 0
    
    def is_cart_badge_visible(self) -> bool:
        """
        Check if shopping cart badge is visible.
        
        Returns:
            True if badge is visible, False otherwise
        """
        return self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000)
    
    def click_shopping_cart(self) -> None:
        """Navigate to shopping cart page."""
        self.logger.info("Navigating to shopping cart")
        self.click(self.SHOPPING_CART_LINK)
    
    def sort_products(self, sort_option: str) -> None:
        """
        Sort products by specified option.
        
        Args:
            sort_option: Sort option (az, za, lohi, hilo)
        """
        self.logger.info(f"Sorting products by: {sort_option}")
        self.select_option(self.PRODUCT_SORT_CONTAINER, sort_option)
    
    def get_current_sort_value(self) -> Optional[str]:
        """
        Get currently selected sort option.
        
        Returns:
            Current sort option value
        """
        return self.page.locator(self.PRODUCT_SORT_CONTAINER).input_value()
    
    def open_burger_menu(self) -> None:
        """Open the burger menu."""
        self.logger.info("Opening burger menu")
        self.click(self.BURGER_MENU)
    
    def logout(self) -> None:
        """Logout from the application."""
        self.logger.info("Logging out")
        self.open_burger_menu()
        self.click(self.LOGOUT_LINK)
    
    def get_product_name_by_index(self, index: int) -> str:
        """
        Get product name at specified index.
        
        Args:
            index: Zero-based index
            
        Returns:
            Product name
        """
        names = self.get_all_product_names()
        return names[index] if index < len(names) else ""
    
    def get_product_price_by_index(self, index: int) -> float:
        """
        Get product price at specified index.
        
        Args:
            index: Zero-based index
            
        Returns:
            Product price
        """
        prices = self.get_all_product_prices()
        return prices[index] if index < len(prices) else 0.0
    
    def get_product_description_by_name(self, product_name: str) -> str:
        """
        Get product description by product name.
        
        Args:
            product_name: Name of the product
            
        Returns:
            Product description
        """
        # Find the item containing the product name, then get its description
        item_locator = self.page.locator(f'{self.INVENTORY_ITEM}:has-text("{product_name}")')
        desc_locator = item_locator.locator(self.INVENTORY_ITEM_DESC)
        return desc_locator.text_content() or ""
    
    def click_product_name(self, product_name: str) -> None:
        """
        Click on a product name to view details.
        
        Args:
            product_name: Name of the product
        """
        self.logger.info(f"Clicking product: {product_name}")
        self.page.locator(f'{self.INVENTORY_ITEM_NAME}:has-text("{product_name}")').first.click()
    
    def click_product_image(self, index: int) -> None:
        """
        Click on a product image by index.
        
        Args:
            index: Zero-based index of the product
        """
        self.logger.info(f"Clicking product image at index {index}")
        images = self.page.locator('.inventory_item_img').all()
        if index < len(images):
            images[index].click()
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if a product has been added to cart (Remove button visible).
        
        Args:
            product_name: Name of the product
            
        Returns:
            True if product is in cart, False otherwise
        """
        button_id = f'remove-{product_name.lower().replace(" ", "-")}'
        return self.is_visible(f'[data-test="{button_id}"]', timeout=2000)
    
    def add_all_products_to_cart(self) -> None:
        """Add all products to cart."""
        self.logger.info("Adding all products to cart")
        product_count = self.get_product_count()
        for i in range(product_count):
            self.add_product_to_cart_by_index(i)
    
    def remove_all_products_from_cart(self) -> None:
        """Remove all products from cart."""
        self.logger.info("Removing all products from cart")
        while self.get_element_count(self.REMOVE_BUTTON) > 0:
            self.page.locator(self.REMOVE_BUTTON).first.click()
    
    def get_app_logo_text(self) -> str:
        """
        Get app logo text.
        
        Returns:
            Logo text
        """
        return self.get_text(self.APP_LOGO)
    
    def is_footer_visible(self) -> bool:
        """
        Check if footer is visible.
        
        Returns:
            True if visible, False otherwise
        """
        return self.is_visible(self.FOOTER)
    
    def get_footer_text(self) -> str:
        """
        Get footer text.
        
        Returns:
            Footer text
        """
        return self.get_text(self.FOOTER)
