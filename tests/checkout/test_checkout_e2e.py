"""
End-to-end checkout flow tests.
Tests complete user journey from login to order completion.
"""
import pytest

from pages import (
    LoginPage,
    InventoryPage,
    CartPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage
)
from utils import test_data
from config import settings


@pytest.mark.checkout
@pytest.mark.smoke
@pytest.mark.regression
class TestCheckoutE2E:
    """End-to-end checkout flow tests."""
    
    def test_complete_checkout_flow_single_item(
        self,
        login_page: LoginPage,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
        checkout_data
    ):
        """Test complete checkout flow with a single product."""
        # Login
        username, password = settings.get_user_credentials("standard")
        login_page.navigate()
        login_page.login(username, password)
        assert inventory_page.is_loaded()
        
        # Add product to cart
        product_name = inventory_page.get_product_name_by_index(0)
        product_price = inventory_page.get_product_price_by_index(0)
        inventory_page.add_product_to_cart_by_name(product_name)
        
        # Go to cart
        inventory_page.click_shopping_cart()
        assert cart_page.is_loaded()
        assert cart_page.is_item_in_cart(product_name)
        
        # Proceed to checkout
        cart_page.proceed_to_checkout()
        assert checkout_step_one_page.is_loaded()
        
        # Fill checkout information
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        # Verify checkout overview
        assert checkout_step_two_page.is_loaded()
        assert product_name in checkout_step_two_page.get_all_item_names()
        
        # Verify price calculations
        subtotal = checkout_step_two_page.get_subtotal()
        assert abs(subtotal - product_price) < 0.01
        assert checkout_step_two_page.verify_total_calculation()
        
        # Complete order
        checkout_step_two_page.click_finish()
        
        # Verify order completion
        assert checkout_complete_page.is_loaded()
        assert checkout_complete_page.is_order_complete()
        assert "Thank you" in checkout_complete_page.get_complete_header()
    
    def test_complete_checkout_flow_multiple_items(
        self,
        logged_in_user,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
        checkout_data
    ):
        """Test complete checkout flow with multiple products."""
        # Add 3 products
        product_names = inventory_page.get_all_product_names()[:3]
        expected_total = 0
        
        for name in product_names:
            inventory_page.add_product_to_cart_by_name(name)
        
        # Calculate expected subtotal
        prices = inventory_page.get_all_product_prices()[:3]
        expected_subtotal = sum(prices)
        
        # Go to cart and checkout
        inventory_page.click_shopping_cart()
        cart_page.proceed_to_checkout()
        
        # Fill information
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        # Verify items and prices
        assert checkout_step_two_page.get_item_count() == 3
        actual_subtotal = checkout_step_two_page.get_subtotal()
        assert abs(actual_subtotal - expected_subtotal) < 0.01
        
        # Complete order
        checkout_step_two_page.click_finish()
        assert checkout_complete_page.is_order_complete()
    
    def test_checkout_with_all_products(
        self,
        logged_in_user,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
        checkout_data
    ):
        """Test checkout with all 6 products in cart."""
        # Add all products
        inventory_page.add_all_products_to_cart()
        assert inventory_page.get_cart_item_count() == 6
        
        # Complete checkout
        inventory_page.click_shopping_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        # Verify all items present
        assert checkout_step_two_page.get_item_count() == 6
        assert checkout_step_two_page.verify_total_calculation()
        
        checkout_step_two_page.click_finish()
        assert checkout_complete_page.is_order_complete()
    
    def test_return_to_products_after_checkout(
        self,
        logged_in_user,
        inventory_page: InventoryPage,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_complete_page: CheckoutCompletePage,
        checkout_data
    ):
        """Test returning to products page after completing order."""
        # Complete a checkout
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.click_shopping_cart()
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        checkout_step_two_page.click_finish()
        
        # Click back home
        checkout_complete_page.click_back_home()
        
        # Should be back on inventory page
        assert inventory_page.is_loaded()
        assert not inventory_page.is_cart_badge_visible(), "Cart should be empty after order"


@pytest.mark.checkout
class TestCheckoutValidation:
    """Test checkout form validation."""
    
    def test_checkout_requires_first_name(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """Test that first name is required."""
        cart_page.proceed_to_checkout()
        
        # Try to continue without first name
        checkout_step_one_page.enter_last_name("Doe")
        checkout_step_one_page.enter_postal_code("12345")
        checkout_step_one_page.click_continue()
        
        assert checkout_step_one_page.is_error_displayed()
        assert "first name is required" in checkout_step_one_page.get_error_message().lower()
    
    def test_checkout_requires_last_name(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """Test that last name is required."""
        cart_page.proceed_to_checkout()
        
        checkout_step_one_page.enter_first_name("John")
        checkout_step_one_page.enter_postal_code("12345")
        checkout_step_one_page.click_continue()
        
        assert checkout_step_one_page.is_error_displayed()
        assert "last name is required" in checkout_step_one_page.get_error_message().lower()
    
    def test_checkout_requires_postal_code(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """Test that postal code is required."""
        cart_page.proceed_to_checkout()
        
        checkout_step_one_page.enter_first_name("John")
        checkout_step_one_page.enter_last_name("Doe")
        checkout_step_one_page.click_continue()
        
        assert checkout_step_one_page.is_error_displayed()
        assert "postal code is required" in checkout_step_one_page.get_error_message().lower()
    
    def test_cancel_button_returns_to_cart(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage
    ):
        """Test that cancel button returns to cart."""
        cart_page.proceed_to_checkout()
        checkout_step_one_page.click_cancel()
        
        assert cart_page.is_loaded(), "Should return to cart page"


@pytest.mark.checkout
@pytest.mark.regression
class TestPriceCalculations:
    """Test price calculations during checkout."""
    
    def test_subtotal_matches_cart_total(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_data
    ):
        """Test that subtotal on checkout matches cart total."""
        expected_total = cart_page.get_total_price()
        
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        actual_subtotal = checkout_step_two_page.get_subtotal()
        assert abs(actual_subtotal - expected_total) < 0.01
    
    def test_tax_is_calculated(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_data
    ):
        """Test that tax is calculated and added."""
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        tax = checkout_step_two_page.get_tax()
        assert tax > 0, "Tax should be positive"
        assert tax < 100, "Tax seems unreasonably high"
    
    def test_total_equals_subtotal_plus_tax(
        self,
        cart_with_items,
        cart_page: CartPage,
        checkout_step_one_page: CheckoutStepOnePage,
        checkout_step_two_page: CheckoutStepTwoPage,
        checkout_data
    ):
        """Test that total = subtotal + tax."""
        cart_page.proceed_to_checkout()
        checkout_step_one_page.fill_information(
            checkout_data.first_name,
            checkout_data.last_name,
            checkout_data.postal_code
        )
        checkout_step_one_page.click_continue()
        
        assert checkout_step_two_page.verify_total_calculation()
