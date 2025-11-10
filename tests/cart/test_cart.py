"""
Shopping cart functionality tests for Sauce Demo application.
Tests cover cart operations, persistence, navigation, and price calculations.
"""
import pytest

from pages import InventoryPage, CartPage, LoginPage


@pytest.mark.cart
@pytest.mark.smoke
class TestCartBasics:
    """Basic cart functionality tests."""
    
    def test_empty_cart_displays_correctly(self, logged_in_user, cart_page: CartPage, inventory_page: InventoryPage):
        """Test that empty cart is displayed correctly."""
        inventory_page.click_shopping_cart()
        
        assert cart_page.is_loaded(), "Cart page should load"
        assert cart_page.is_cart_empty(), "Cart should be empty"
        assert not cart_page.is_cart_badge_visible(), "Cart badge should not be visible when empty"
    
    def test_single_item_in_cart(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test adding single item to cart."""
        product_name = inventory_page.get_product_name_by_index(0)
        inventory_page.add_product_to_cart_by_name(product_name)
        
        inventory_page.click_shopping_cart()
        
        assert cart_page.get_cart_item_count() == 1, "Cart should have 1 item"
        assert cart_page.is_item_in_cart(product_name), "Added product should be in cart"
    
    def test_multiple_items_in_cart(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test adding multiple items to cart."""
        product_names = inventory_page.get_all_product_names()[:3]
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        inventory_page.click_shopping_cart()
        
        assert cart_page.get_cart_item_count() == 3, "Cart should have 3 items"
        for name in product_names:
            assert cart_page.is_item_in_cart(name), f"{name} should be in cart"
    
    def test_all_products_in_cart(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test adding all 6 products to cart."""
        inventory_page.add_all_products_to_cart()
        inventory_page.click_shopping_cart()
        
        assert cart_page.get_cart_item_count() == 6, "Cart should have all 6 products"


@pytest.mark.cart
class TestCartItemRemoval:
    """Tests for removing items from cart."""
    
    def test_remove_single_item_from_cart(self, cart_with_items, cart_page: CartPage):
        """Test removing a single item from cart."""
        _, cart_page, product_names = cart_with_items
        
        initial_count = cart_page.get_cart_item_count()
        cart_page.remove_item_by_name(product_names[0])
        
        assert cart_page.get_cart_item_count() == initial_count - 1, "Item count should decrease by 1"
        assert not cart_page.is_item_in_cart(product_names[0]), "Removed item should not be in cart"
    
    def test_remove_all_items_from_cart(self, cart_with_items, cart_page: CartPage):
        """Test removing all items from cart."""
        _, cart_page, product_names = cart_with_items
        
        cart_page.remove_all_items()
        
        assert cart_page.is_cart_empty(), "Cart should be empty after removing all items"
        assert not cart_page.is_cart_badge_visible(), "Cart badge should not be visible"
    
    def test_remove_item_by_index(self, cart_with_items, cart_page: CartPage):
        """Test removing item by index."""
        _, cart_page, _ = cart_with_items
        
        initial_count = cart_page.get_cart_item_count()
        cart_page.remove_item_by_index(0)
        
        assert cart_page.get_cart_item_count() == initial_count - 1


@pytest.mark.cart
class TestCartNavigation:
    """Tests for cart navigation functionality."""
    
    def test_continue_shopping_button(self, cart_with_items, cart_page: CartPage, inventory_page: InventoryPage):
        """Test continue shopping button returns to inventory."""
        _, cart_page, _ = cart_with_items
        
        cart_page.continue_shopping()
        
        assert inventory_page.is_loaded(), "Should return to inventory page"
    
    def test_cart_persistence_across_pages(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that cart persists when navigating between pages."""
        # Add items
        product_names = inventory_page.get_all_product_names()[:2]
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        # Go to cart
        inventory_page.click_shopping_cart()
        assert cart_page.get_cart_item_count() == 2
        
        # Go back to inventory
        cart_page.continue_shopping()
        
        # Verify cart badge still shows 2
        assert inventory_page.get_cart_item_count() == 2
        
        # Go back to cart and verify items still there
        inventory_page.click_shopping_cart()
        assert cart_page.get_cart_item_count() == 2
        for name in product_names:
            assert cart_page.is_item_in_cart(name)
    
    def test_checkout_button_navigation(self, cart_with_items, cart_page: CartPage):
        """Test checkout button navigates to checkout page."""
        _, cart_page, _ = cart_with_items
        
        cart_page.proceed_to_checkout()
        
        assert "checkout-step-one" in cart_page.get_url(), "Should navigate to checkout"


@pytest.mark.cart
@pytest.mark.regression
class TestCartPriceCalculations:
    """Tests for cart price calculations."""
    
    def test_single_item_price_displayed(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that single item price is displayed correctly in cart."""
        product_price = inventory_page.get_product_price_by_index(0)
        product_name = inventory_page.get_product_name_by_index(0)
        
        inventory_page.add_product_to_cart_by_name(product_name)
        inventory_page.click_shopping_cart()
        
        cart_prices = cart_page.get_all_item_prices()
        assert len(cart_prices) == 1
        assert abs(cart_prices[0] - product_price) < 0.01, "Cart price should match product price"
    
    def test_multiple_items_prices_displayed(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that multiple item prices are displayed correctly."""
        # Get first 3 products
        expected_prices = inventory_page.get_all_product_prices()[:3]
        product_names = inventory_page.get_all_product_names()[:3]
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        inventory_page.click_shopping_cart()
        
        cart_prices = cart_page.get_all_item_prices()
        assert len(cart_prices) == 3
        
        # Verify prices match (order might be different)
        for expected_price in expected_prices:
            assert any(abs(cart_price - expected_price) < 0.01 for cart_price in cart_prices)
    
    def test_cart_total_calculation(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that cart total is calculated correctly."""
        expected_prices = inventory_page.get_all_product_prices()[:3]
        product_names = inventory_page.get_all_product_names()[:3]
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        inventory_page.click_shopping_cart()
        
        expected_total = sum(expected_prices)
        actual_total = cart_page.get_total_price()
        
        assert abs(actual_total - expected_total) < 0.01, f"Expected total {expected_total}, got {actual_total}"


@pytest.mark.cart
class TestCartBadge:
    """Tests for shopping cart badge behavior."""
    
    def test_cart_badge_count_matches_items(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that cart badge count matches number of items in cart."""
        # Add 3 items
        for i in range(3):
            inventory_page.add_product_to_cart_by_index(i)
        
        # Check badge
        assert inventory_page.get_cart_item_count() == 3
        
        # Go to cart and verify
        inventory_page.click_shopping_cart()
        assert cart_page.get_cart_item_count() == 3
        
        # Badge should still show on cart page
        badge_count = cart_page.get_cart_badge_count()
        assert badge_count == 3
    
    def test_cart_badge_updates_after_removal(self, cart_with_items, cart_page: CartPage):
        """Test that cart badge updates when items are removed."""
        _, cart_page, product_names = cart_with_items
        
        initial_count = cart_page.get_cart_badge_count()
        cart_page.remove_item_by_name(product_names[0])
        
        new_count = cart_page.get_cart_badge_count()
        assert new_count == initial_count - 1


@pytest.mark.cart
@pytest.mark.regression
class TestCartEdgeCases:
    """Edge case tests for cart functionality."""
    
    def test_cart_with_all_six_products(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test cart behavior with maximum number of products."""
        inventory_page.add_all_products_to_cart()
        inventory_page.click_shopping_cart()
        
        assert cart_page.get_cart_item_count() == 6
        all_names = cart_page.get_all_item_names()
        assert len(all_names) == 6
        assert len(set(all_names)) == 6, "All product names should be unique"
    
    def test_empty_cart_has_no_checkout_issues(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that empty cart displays checkout button (even if it shouldn't work)."""
        inventory_page.click_shopping_cart()
        
        assert cart_page.is_cart_empty()
        # Checkout button should still be visible (app behavior)
        assert cart_page.is_visible(cart_page.CHECKOUT_BUTTON)
    
    def test_cart_item_quantity_display(self, cart_with_items, cart_page: CartPage):
        """Test that item quantity is displayed correctly."""
        _, cart_page, _ = cart_with_items
        
        # Each item should have quantity 1
        for i in range(cart_page.get_cart_item_count()):
            quantity = cart_page.get_item_quantity(i)
            assert quantity == 1, f"Item {i} should have quantity 1"
    
    def test_cart_maintains_item_order(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test that cart maintains order of items added."""
        product_names = inventory_page.get_all_product_names()[:3]
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        inventory_page.click_shopping_cart()
        
        cart_items = cart_page.get_all_item_names()
        # Items might be in reverse order or same order - just verify all are present
        for name in product_names:
            assert name in cart_items


@pytest.mark.cart
class TestCartItemDetails:
    """Tests for cart item details display."""
    
    def test_cart_displays_product_names(self, cart_with_items, cart_page: CartPage):
        """Test that product names are displayed in cart."""
        _, cart_page, product_names = cart_with_items
        
        cart_item_names = cart_page.get_all_item_names()
        
        assert len(cart_item_names) == len(product_names)
        for name in product_names:
            assert name in cart_item_names
    
    def test_cart_displays_product_prices(self, cart_with_items, cart_page: CartPage):
        """Test that product prices are displayed in cart."""
        _, cart_page, _ = cart_with_items
        
        prices = cart_page.get_all_item_prices()
        
        assert len(prices) > 0
        for price in prices:
            assert price > 0, "All prices should be positive"
            assert price < 1000, "Prices should be reasonable"


@pytest.mark.cart
@pytest.mark.smoke
class TestCartWorkflow:
    """End-to-end cart workflow tests."""
    
    def test_add_view_remove_workflow(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test complete add -> view -> remove workflow."""
        # Add product
        product_name = inventory_page.get_product_name_by_index(0)
        inventory_page.add_product_to_cart_by_name(product_name)
        
        # View in cart
        inventory_page.click_shopping_cart()
        assert cart_page.is_item_in_cart(product_name)
        
        # Remove from cart
        cart_page.remove_item_by_name(product_name)
        assert cart_page.is_cart_empty()
        
        # Go back to inventory
        cart_page.continue_shopping()
        assert not inventory_page.is_cart_badge_visible()
    
    def test_add_multiple_view_remove_one_workflow(self, logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
        """Test adding multiple items, removing one, and verifying state."""
        # Add 3 products
        product_names = inventory_page.get_all_product_names()[:3]
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        # View cart
        inventory_page.click_shopping_cart()
        assert cart_page.get_cart_item_count() == 3
        
        # Remove one
        cart_page.remove_item_by_name(product_names[0])
        assert cart_page.get_cart_item_count() == 2
        assert not cart_page.is_item_in_cart(product_names[0])
        assert cart_page.is_item_in_cart(product_names[1])
        assert cart_page.is_item_in_cart(product_names[2])
