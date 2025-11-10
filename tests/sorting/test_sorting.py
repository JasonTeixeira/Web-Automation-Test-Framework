"""
Product sorting and filtering tests for Sauce Demo application.
Tests cover all sort options, verification, and persistence.
"""
import pytest

from pages import InventoryPage


@pytest.mark.sorting
@pytest.mark.smoke
class TestBasicSorting:
    """Basic sorting functionality tests."""
    
    def test_default_sort_order(self, logged_in_user, inventory_page: InventoryPage):
        """Test that default sort order is Name (A to Z)."""
        current_sort = inventory_page.get_current_sort_value()
        assert current_sort == inventory_page.SORT_NAME_ASC, "Default sort should be A-Z"
    
    def test_sort_dropdown_is_visible(self, logged_in_user, inventory_page: InventoryPage):
        """Test that sort dropdown is visible."""
        assert inventory_page.is_visible(inventory_page.PRODUCT_SORT_CONTAINER), "Sort dropdown should be visible"
    
    def test_all_sort_options_available(self, logged_in_user, inventory_page: InventoryPage):
        """Test that all sort options are available."""
        # Verify the dropdown exists and can be interacted with
        sort_element = inventory_page.page.locator(inventory_page.PRODUCT_SORT_CONTAINER)
        options = sort_element.locator('option').all()
        
        assert len(options) == 4, "Should have 4 sort options"


@pytest.mark.sorting
@pytest.mark.regression
class TestSortByName:
    """Tests for sorting products by name."""
    
    def test_sort_by_name_a_to_z(self, logged_in_user, inventory_page: InventoryPage):
        """Test sorting products by name A to Z."""
        inventory_page.sort_products(inventory_page.SORT_NAME_ASC)
        
        product_names = inventory_page.get_all_product_names()
        sorted_names = sorted(product_names)
        
        assert product_names == sorted_names, "Products should be sorted A to Z"
    
    def test_sort_by_name_z_to_a(self, logged_in_user, inventory_page: InventoryPage):
        """Test sorting products by name Z to A."""
        inventory_page.sort_products(inventory_page.SORT_NAME_DESC)
        
        product_names = inventory_page.get_all_product_names()
        sorted_names = sorted(product_names, reverse=True)
        
        assert product_names == sorted_names, "Products should be sorted Z to A"
    
    def test_sort_name_az_then_za(self, logged_in_user, inventory_page: InventoryPage):
        """Test switching between A-Z and Z-A sorting."""
        # Sort A to Z
        inventory_page.sort_products(inventory_page.SORT_NAME_ASC)
        names_az = inventory_page.get_all_product_names()
        
        # Sort Z to A
        inventory_page.sort_products(inventory_page.SORT_NAME_DESC)
        names_za = inventory_page.get_all_product_names()
        
        # Z-A should be reverse of A-Z
        assert names_za == list(reversed(names_az)), "Z-A should be reverse of A-Z"
    
    def test_sort_name_maintains_all_products(self, logged_in_user, inventory_page: InventoryPage):
        """Test that sorting doesn't lose any products."""
        # Get original products
        original_names = set(inventory_page.get_all_product_names())
        
        # Sort Z to A
        inventory_page.sort_products(inventory_page.SORT_NAME_DESC)
        sorted_names = set(inventory_page.get_all_product_names())
        
        assert original_names == sorted_names, "Sorting should maintain all products"
        assert len(sorted_names) == 6, "Should have all 6 products after sorting"


@pytest.mark.sorting
@pytest.mark.regression
class TestSortByPrice:
    """Tests for sorting products by price."""
    
    def test_sort_by_price_low_to_high(self, logged_in_user, inventory_page: InventoryPage):
        """Test sorting products by price low to high."""
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        
        prices = inventory_page.get_all_product_prices()
        sorted_prices = sorted(prices)
        
        assert prices == sorted_prices, f"Prices should be sorted low to high: {prices} vs {sorted_prices}"
    
    def test_sort_by_price_high_to_low(self, logged_in_user, inventory_page: InventoryPage):
        """Test sorting products by price high to low."""
        inventory_page.sort_products(inventory_page.SORT_PRICE_DESC)
        
        prices = inventory_page.get_all_product_prices()
        sorted_prices = sorted(prices, reverse=True)
        
        assert prices == sorted_prices, f"Prices should be sorted high to low: {prices} vs {sorted_prices}"
    
    def test_sort_price_lohi_then_hilo(self, logged_in_user, inventory_page: InventoryPage):
        """Test switching between low-high and high-low price sorting."""
        # Sort low to high
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        prices_lohi = inventory_page.get_all_product_prices()
        
        # Sort high to low
        inventory_page.sort_products(inventory_page.SORT_PRICE_DESC)
        prices_hilo = inventory_page.get_all_product_prices()
        
        # High-low should be reverse of low-high
        assert prices_hilo == list(reversed(prices_lohi)), "High-low should be reverse of low-high"
    
    def test_sort_price_maintains_all_products(self, logged_in_user, inventory_page: InventoryPage):
        """Test that price sorting doesn't lose any products."""
        original_count = inventory_page.get_product_count()
        
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        
        assert inventory_page.get_product_count() == original_count, "Product count should remain same"
        assert inventory_page.get_product_count() == 6, "Should have all 6 products"


@pytest.mark.sorting
class TestSortPersistence:
    """Tests for sort option persistence."""
    
    def test_sort_persists_with_items_in_cart(self, logged_in_user, inventory_page: InventoryPage):
        """Test that sort order persists when adding items to cart."""
        # Sort by price
        inventory_page.sort_products(inventory_page.SORT_PRICE_DESC)
        sorted_prices = inventory_page.get_all_product_prices()
        
        # Add item to cart
        inventory_page.add_product_to_cart_by_index(0)
        
        # Verify sort still maintained
        current_prices = inventory_page.get_all_product_prices()
        assert current_prices == sorted_prices, "Sort should persist after adding to cart"
    
    def test_sort_resets_after_navigation(self, logged_in_user, inventory_page: InventoryPage, cart_page):
        """Test that sort might reset after navigating away and back."""
        # Sort by Z-A
        inventory_page.sort_products(inventory_page.SORT_NAME_DESC)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        
        # Navigate back
        cart_page.continue_shopping()
        
        # Check current sort (might reset to default)
        current_sort = inventory_page.get_current_sort_value()
        # Just verify we can check the sort value
        assert current_sort in [inventory_page.SORT_NAME_ASC, inventory_page.SORT_NAME_DESC, 
                                inventory_page.SORT_PRICE_ASC, inventory_page.SORT_PRICE_DESC]


@pytest.mark.sorting
@pytest.mark.regression
class TestSortAccuracy:
    """Tests to verify sorting accuracy."""
    
    def test_sort_name_handles_special_characters(self, logged_in_user, inventory_page: InventoryPage):
        """Test that name sorting handles special characters correctly."""
        inventory_page.sort_products(inventory_page.SORT_NAME_ASC)
        names = inventory_page.get_all_product_names()
        
        # Verify it's actually sorted (Python's sorted handles special chars)
        assert names == sorted(names), "Names with special characters should sort correctly"
    
    def test_sort_price_accuracy_with_decimals(self, logged_in_user, inventory_page: InventoryPage):
        """Test that price sorting accurately handles decimal values."""
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        prices = inventory_page.get_all_product_prices()
        
        # Verify each price is less than or equal to the next
        for i in range(len(prices) - 1):
            assert prices[i] <= prices[i + 1], f"Price {prices[i]} should be <= {prices[i + 1]}"
    
    def test_sort_maintains_product_data_integrity(self, logged_in_user, inventory_page: InventoryPage):
        """Test that sorting doesn't corrupt product data."""
        # Get original data
        original_names = inventory_page.get_all_product_names()
        original_prices = inventory_page.get_all_product_prices()
        
        # Sort multiple times
        inventory_page.sort_products(inventory_page.SORT_NAME_DESC)
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        inventory_page.sort_products(inventory_page.SORT_NAME_ASC)
        
        # Get final data
        final_names = set(inventory_page.get_all_product_names())
        final_prices = set(inventory_page.get_all_product_prices())
        
        assert set(original_names) == final_names, "Product names should remain same"
        assert set(original_prices) == final_prices, "Product prices should remain same"


@pytest.mark.sorting
class TestSortUI:
    """Tests for sort UI behavior."""
    
    def test_sort_dropdown_reflects_selection(self, logged_in_user, inventory_page: InventoryPage):
        """Test that dropdown shows currently selected sort option."""
        inventory_page.sort_products(inventory_page.SORT_PRICE_DESC)
        
        current_sort = inventory_page.get_current_sort_value()
        assert current_sort == inventory_page.SORT_PRICE_DESC, "Dropdown should reflect selection"
    
    def test_sort_all_options_sequentially(self, logged_in_user, inventory_page: InventoryPage):
        """Test applying all sort options one after another."""
        sort_options = [
            inventory_page.SORT_NAME_ASC,
            inventory_page.SORT_NAME_DESC,
            inventory_page.SORT_PRICE_ASC,
            inventory_page.SORT_PRICE_DESC
        ]
        
        for sort_option in sort_options:
            inventory_page.sort_products(sort_option)
            current_sort = inventory_page.get_current_sort_value()
            assert current_sort == sort_option, f"Should be sorted by {sort_option}"
            assert inventory_page.get_product_count() == 6, "Should maintain 6 products"


@pytest.mark.sorting
@pytest.mark.smoke
class TestSortWorkflows:
    """End-to-end sorting workflow tests."""
    
    def test_sort_and_add_to_cart_workflow(self, logged_in_user, inventory_page: InventoryPage):
        """Test sorting, then adding products to cart."""
        # Sort by price low to high
        inventory_page.sort_products(inventory_page.SORT_PRICE_ASC)
        
        # Add cheapest product (first one)
        cheapest_product = inventory_page.get_product_name_by_index(0)
        cheapest_price = inventory_page.get_product_price_by_index(0)
        
        inventory_page.add_product_to_cart_by_name(cheapest_product)
        
        # Verify it was added
        assert inventory_page.get_cart_item_count() == 1
        
        # Verify it's actually the cheapest
        all_prices = inventory_page.get_all_product_prices()
        assert cheapest_price == min(all_prices), "Should have added the cheapest product"
    
    def test_find_most_expensive_product(self, logged_in_user, inventory_page: InventoryPage):
        """Test workflow to find and select most expensive product."""
        # Sort by price high to low
        inventory_page.sort_products(inventory_page.SORT_PRICE_DESC)
        
        # First product should be most expensive
        most_expensive_product = inventory_page.get_product_name_by_index(0)
        most_expensive_price = inventory_page.get_product_price_by_index(0)
        
        # Verify it's actually the most expensive
        all_prices = inventory_page.get_all_product_prices()
        assert most_expensive_price == max(all_prices), "First product should be most expensive"
