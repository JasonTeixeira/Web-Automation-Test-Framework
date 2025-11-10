"""
Inventory/Products page tests for Sauce Demo application.
Tests cover product display, add to cart, cart badge, and product interactions.
"""
import pytest

from pages import InventoryPage, LoginPage, CartPage


@pytest.mark.inventory
@pytest.mark.smoke
class TestInventoryDisplay:
    """Test inventory page display and product information."""
    
    def test_inventory_page_loads_after_login(self, logged_in_user, inventory_page: InventoryPage):
        """Test that inventory page loads successfully after login."""
        assert inventory_page.is_loaded(), "Inventory page should be loaded"
        assert inventory_page.get_product_count() > 0, "At least one product should be displayed"
    
    def test_all_products_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all 6 products are displayed."""
        product_count = inventory_page.get_product_count()
        assert product_count == 6, f"Expected 6 products, found {product_count}"
    
    def test_product_names_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all products have names."""
        product_names = inventory_page.get_all_product_names()
        
        assert len(product_names) == 6, "Should have 6 product names"
        for name in product_names:
            assert len(name) > 0, "Each product should have a non-empty name"
    
    def test_product_prices_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all products have prices."""
        prices = inventory_page.get_all_product_prices()
        
        assert len(prices) == 6, "Should have 6 product prices"
        for price in prices:
            assert price > 0, f"Price should be positive, got {price}"
    
    def test_product_descriptions_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that products have descriptions."""
        product_name = inventory_page.get_product_name_by_index(0)
        description = inventory_page.get_product_description_by_name(product_name)
        
        assert len(description) > 0, "Product should have a description"
    
    def test_app_logo_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that app logo is displayed."""
        logo_text = inventory_page.get_app_logo_text()
        assert "Swag Labs" in logo_text, f"Expected 'Swag Labs' in logo, got: {logo_text}"
    
    def test_footer_displayed(self, logged_in_user, inventory_page: InventoryPage):
        """Test that footer is displayed."""
        assert inventory_page.is_footer_visible(), "Footer should be visible"
        footer_text = inventory_page.get_footer_text()
        assert len(footer_text) > 0, "Footer should have text"


@pytest.mark.inventory
@pytest.mark.smoke
class TestAddToCart:
    """Test adding products to cart functionality."""
    
    def test_add_single_product_to_cart(self, logged_in_user, inventory_page: InventoryPage):
        """Test adding a single product to cart."""
        product_name = inventory_page.get_product_name_by_index(0)
        
        inventory_page.add_product_to_cart_by_name(product_name)
        
        assert inventory_page.is_cart_badge_visible(), "Cart badge should appear"
        assert inventory_page.get_cart_item_count() == 1, "Cart should have 1 item"
        assert inventory_page.is_product_in_cart(product_name), "Product should show as in cart"
    
    def test_add_multiple_products_to_cart(self, logged_in_user, inventory_page: InventoryPage):
        """Test adding multiple products to cart."""
        product_names = inventory_page.get_all_product_names()[:3]
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        assert inventory_page.get_cart_item_count() == 3, "Cart should have 3 items"
    
    def test_add_all_products_to_cart(self, logged_in_user, inventory_page: InventoryPage):
        """Test adding all 6 products to cart."""
        inventory_page.add_all_products_to_cart()
        
        assert inventory_page.get_cart_item_count() == 6, "Cart should have all 6 items"
    
    def test_add_and_remove_product(self, logged_in_user, inventory_page: InventoryPage):
        """Test adding then removing a product."""
        product_name = inventory_page.get_product_name_by_index(0)
        
        # Add
        inventory_page.add_product_to_cart_by_name(product_name)
        assert inventory_page.get_cart_item_count() == 1
        
        # Remove
        inventory_page.remove_product_from_cart_by_name(product_name)
        assert not inventory_page.is_cart_badge_visible(), "Cart badge should disappear"
    
    def test_remove_all_products_from_cart(self, logged_in_user, inventory_page: InventoryPage):
        """Test removing all products from cart."""
        inventory_page.add_all_products_to_cart()
        assert inventory_page.get_cart_item_count() == 6
        
        inventory_page.remove_all_products_from_cart()
        assert not inventory_page.is_cart_badge_visible(), "Cart should be empty"
    
    def test_add_product_by_index(self, logged_in_user, inventory_page: InventoryPage):
        """Test adding product using index."""
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.add_product_to_cart_by_index(1)
        
        assert inventory_page.get_cart_item_count() == 2
    
    def test_cart_badge_increments_correctly(self, logged_in_user, inventory_page: InventoryPage):
        """Test that cart badge increments with each addition."""
        for i in range(1, 4):
            inventory_page.add_product_to_cart_by_index(i-1)
            assert inventory_page.get_cart_item_count() == i, f"Cart should have {i} items"


@pytest.mark.inventory
class TestProductNavigation:
    """Test navigation and product detail interactions."""
    
    def test_click_product_name_navigates_to_detail(self, logged_in_user, inventory_page: InventoryPage):
        """Test clicking product name navigates to product detail."""
        product_name = inventory_page.get_product_name_by_index(0)
        inventory_page.click_product_name(product_name)
        
        # Should navigate to product detail page
        assert "inventory-item.html" in inventory_page.get_url()
    
    def test_click_shopping_cart_navigates_to_cart(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test clicking shopping cart icon navigates to cart page."""
        inventory_page.click_shopping_cart()
        
        assert cart_page.is_loaded(), "Should navigate to cart page"
    
    def test_burger_menu_opens(self, logged_in_user, inventory_page: InventoryPage):
        """Test that burger menu opens."""
        inventory_page.open_burger_menu()
        
        # Wait for menu to be visible
        assert inventory_page.is_visible(inventory_page.LOGOUT_LINK, timeout=2000), "Logout link should be visible in menu"
    
    def test_logout_returns_to_login_page(self, logged_in_user, inventory_page: InventoryPage, login_page: LoginPage):
        """Test logout functionality."""
        inventory_page.logout()
        
        # Should return to login page
        assert login_page.is_logo_visible(), "Should be back on login page"
        assert settings.base_url == login_page.get_url().rstrip('/'), "URL should be login page"


@pytest.mark.inventory
class TestCartBadge:
    """Test shopping cart badge behavior."""
    
    def test_cart_badge_not_visible_when_empty(self, logged_in_user, inventory_page: InventoryPage):
        """Test that cart badge is not visible when cart is empty."""
        assert not inventory_page.is_cart_badge_visible(), "Cart badge should not be visible for empty cart"
    
    def test_cart_badge_appears_with_first_item(self, logged_in_user, inventory_page: InventoryPage):
        """Test that cart badge appears when first item is added."""
        inventory_page.add_product_to_cart_by_index(0)
        
        assert inventory_page.is_cart_badge_visible(), "Cart badge should appear"
        assert inventory_page.get_cart_item_count() == 1
    
    def test_cart_badge_disappears_when_empty(self, logged_in_user, inventory_page: InventoryPage):
        """Test that badge disappears when cart becomes empty."""
        product_name = inventory_page.get_product_name_by_index(0)
        
        inventory_page.add_product_to_cart_by_name(product_name)
        assert inventory_page.is_cart_badge_visible()
        
        inventory_page.remove_product_from_cart_by_name(product_name)
        assert not inventory_page.is_cart_badge_visible()
    
    def test_cart_badge_count_accuracy(self, logged_in_user, inventory_page: InventoryPage):
        """Test that cart badge shows accurate count."""
        for i in range(1, 6):
            inventory_page.add_product_to_cart_by_index(i-1)
            badge_count = inventory_page.get_cart_item_count()
            assert badge_count == i, f"Badge should show {i}, got {badge_count}"


@pytest.mark.inventory
@pytest.mark.regression
class TestProductData:
    """Test product data integrity and consistency."""
    
    def test_product_prices_are_valid_numbers(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all prices are valid positive numbers."""
        prices = inventory_page.get_all_product_prices()
        
        for price in prices:
            assert isinstance(price, float), f"Price should be float, got {type(price)}"
            assert price > 0, f"Price should be positive, got {price}"
            assert price < 1000, f"Price seems unreasonably high: {price}"
    
    def test_product_names_are_unique(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all product names are unique."""
        product_names = inventory_page.get_all_product_names()
        unique_names = set(product_names)
        
        assert len(unique_names) == len(product_names), "All product names should be unique"
    
    def test_no_empty_product_names(self, logged_in_user, inventory_page: InventoryPage):
        """Test that no products have empty names."""
        product_names = inventory_page.get_all_product_names()
        
        for name in product_names:
            assert name.strip(), "Product name should not be empty"
    
    def test_product_price_format(self, logged_in_user, inventory_page: InventoryPage):
        """Test that prices have correct decimal format (max 2 decimal places)."""
        prices = inventory_page.get_all_product_prices()
        
        for price in prices:
            # Check decimal places
            decimal_str = str(price).split('.')
            if len(decimal_str) > 1:
                assert len(decimal_str[1]) <= 2, f"Price should have max 2 decimal places: {price}"


@pytest.mark.inventory
class TestButtonStates:
    """Test button state changes."""
    
    def test_add_button_changes_to_remove(self, logged_in_user, inventory_page: InventoryPage):
        """Test that Add to Cart button changes to Remove after clicking."""
        product_name = inventory_page.get_product_name_by_index(0)
        
        # Initially should have Add button
        assert not inventory_page.is_product_in_cart(product_name)
        
        # Add product
        inventory_page.add_product_to_cart_by_name(product_name)
        
        # Should now have Remove button
        assert inventory_page.is_product_in_cart(product_name)
    
    def test_remove_button_changes_to_add(self, logged_in_user, inventory_page: InventoryPage):
        """Test that Remove button changes back to Add to Cart."""
        product_name = inventory_page.get_product_name_by_index(0)
        
        # Add then remove
        inventory_page.add_product_to_cart_by_name(product_name)
        inventory_page.remove_product_from_cart_by_name(product_name)
        
        # Should be back to Add button
        assert not inventory_page.is_product_in_cart(product_name)


from config import settings
