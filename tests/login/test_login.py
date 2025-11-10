"""
Login functionality tests for Sauce Demo application.
Tests cover positive scenarios, negative scenarios, UI validation, and accessibility.
"""
import pytest
from playwright.sync_api import expect

from config import settings
from pages import LoginPage, InventoryPage
from utils import test_data


@pytest.mark.login
@pytest.mark.smoke
class TestLoginPositive:
    """Positive login test scenarios."""
    
    def test_successful_login_with_standard_user(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Test successful login with standard user credentials."""
        username, password = settings.get_user_credentials("standard")
        
        login_page.navigate()
        login_page.login(username, password)
        
        assert inventory_page.is_loaded(), "Inventory page should load after successful login"
        assert "/inventory.html" in inventory_page.get_url(), "URL should contain inventory.html"
    
    def test_successful_login_with_problem_user(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Test successful login with problem user credentials."""
        username, password = settings.get_user_credentials("problem")
        
        login_page.navigate()
        login_page.login(username, password)
        
        assert inventory_page.is_loaded(), "Problem user should be able to login"
    
    def test_successful_login_with_performance_user(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Test successful login with performance glitch user."""
        username, password = settings.get_user_credentials("performance")
        
        login_page.navigate()
        login_page.login(username, password)
        
        assert inventory_page.is_loaded(), "Performance user should be able to login"
    
    def test_login_with_enter_key(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Test login submission using Enter key."""
        username, password = settings.get_user_credentials("standard")
        
        login_page.navigate()
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.submit_with_enter_key()
        
        assert inventory_page.is_loaded(), "Enter key should submit login form"
    
    def test_login_credentials_are_case_sensitive(self, login_page: LoginPage):
        """Test that login credentials are case-sensitive."""
        login_page.navigate()
        login_page.login("STANDARD_USER", "secret_sauce")  # Wrong case
        
        assert login_page.is_error_displayed(), "Error should be displayed for wrong case username"
        assert "do not match" in login_page.get_error_message().lower()


@pytest.mark.login
@pytest.mark.smoke
class TestLoginNegative:
    """Negative login test scenarios."""
    
    def test_login_with_locked_out_user(self, login_page: LoginPage):
        """Test login attempt with locked out user."""
        username, password = settings.get_user_credentials("locked")
        
        login_page.navigate()
        login_page.login(username, password)
        
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_msg = login_page.get_error_message()
        assert "locked out" in error_msg.lower(), f"Expected 'locked out' in error message, got: {error_msg}"
    
    def test_login_with_empty_credentials(self, login_page: LoginPage):
        """Test login with empty username and password."""
        login_page.navigate()
        login_page.login("", "")
        
        assert login_page.is_error_displayed(), "Error should be displayed for empty credentials"
        error_msg = login_page.get_error_message()
        assert "username is required" in error_msg.lower()
    
    def test_login_with_empty_username(self, login_page: LoginPage):
        """Test login with empty username."""
        login_page.navigate()
        login_page.login("", "secret_sauce")
        
        assert login_page.is_error_displayed()
        assert "username is required" in login_page.get_error_message().lower()
    
    def test_login_with_empty_password(self, login_page: LoginPage):
        """Test login with empty password."""
        login_page.navigate()
        login_page.login("standard_user", "")
        
        assert login_page.is_error_displayed()
        assert "password is required" in login_page.get_error_message().lower()
    
    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        """Test login with completely invalid credentials."""
        login_page.navigate()
        login_page.login("invalid_user", "wrong_password")
        
        assert login_page.is_error_displayed()
        error_msg = login_page.get_error_message()
        assert "do not match" in error_msg.lower()
    
    def test_login_with_wrong_password(self, login_page: LoginPage):
        """Test login with valid username but wrong password."""
        login_page.navigate()
        login_page.login("standard_user", "wrong_password")
        
        assert login_page.is_error_displayed()
        assert "do not match" in login_page.get_error_message().lower()
    
    @pytest.mark.parametrize("invalid_cred", test_data.generate_invalid_credentials())
    def test_login_with_various_invalid_credentials(self, login_page: LoginPage, invalid_cred):
        """Test login with various invalid credential combinations."""
        login_page.navigate()
        login_page.login(invalid_cred.username, invalid_cred.password)
        
        assert login_page.is_error_displayed(), f"Error should be shown for {invalid_cred.user_type}"


@pytest.mark.login
class TestLoginUI:
    """UI and visual validation tests for login page."""
    
    def test_login_page_loads_correctly(self, login_page: LoginPage):
        """Test that login page loads with all essential elements."""
        login_page.navigate()
        
        assert login_page.is_logo_visible(), "Sauce Labs logo should be visible"
        assert login_page.is_visible(login_page.USERNAME_INPUT), "Username input should be visible"
        assert login_page.is_visible(login_page.PASSWORD_INPUT), "Password input should be visible"
        assert login_page.is_visible(login_page.LOGIN_BUTTON), "Login button should be visible"
    
    def test_login_page_title(self, login_page: LoginPage):
        """Test login page title."""
        login_page.navigate()
        title = login_page.get_title()
        assert "Swag Labs" in title, f"Expected 'Swag Labs' in title, got: {title}"
    
    def test_login_button_is_enabled(self, login_page: LoginPage):
        """Test that login button is enabled by default."""
        login_page.navigate()
        assert login_page.is_login_button_enabled(), "Login button should be enabled"
    
    def test_error_message_can_be_closed(self, login_page: LoginPage):
        """Test that error message can be dismissed."""
        login_page.navigate()
        login_page.login("", "")
        
        assert login_page.is_error_displayed(), "Error should be displayed first"
        
        login_page.close_error_message()
        assert login_page.is_error_closed(), "Error should be closeable"
    
    def test_accepted_usernames_displayed(self, login_page: LoginPage):
        """Test that accepted usernames are displayed on page."""
        login_page.navigate()
        usernames = login_page.get_accepted_usernames()
        
        assert len(usernames) > 0, "At least one username should be displayed"
        assert any("standard_user" in u.lower() for u in usernames), "standard_user should be in the list"
    
    def test_password_hint_displayed(self, login_page: LoginPage):
        """Test that password hint is displayed."""
        login_page.navigate()
        password_hint = login_page.get_password_hint()
        
        assert "secret_sauce" in password_hint.lower(), "Password hint should contain secret_sauce"
    
    def test_password_field_is_masked(self, login_page: LoginPage):
        """Test that password field masks input."""
        login_page.navigate()
        
        # Check password input type
        input_type = login_page.get_attribute(login_page.PASSWORD_INPUT, "type")
        assert input_type == "password", "Password field should have type='password'"


@pytest.mark.login
class TestLoginNavigation:
    """Navigation and keyboard interaction tests."""
    
    def test_tab_navigation_between_fields(self, login_page: LoginPage):
        """Test tab key navigation between input fields."""
        login_page.navigate()
        
        # Focus username
        login_page.page.locator(login_page.USERNAME_INPUT).focus()
        
        # Tab to password
        login_page.tab_to_password()
        
        # Verify password field has focus
        focused_element = login_page.page.evaluate("document.activeElement.getAttribute('data-test')")
        assert focused_element == "password", "Tab should move focus to password field"
    
    def test_page_refresh_clears_error(self, login_page: LoginPage):
        """Test that page refresh clears error message."""
        login_page.navigate()
        login_page.login("", "")
        
        assert login_page.is_error_displayed()
        
        login_page.refresh_page()
        
        assert not login_page.is_error_displayed(), "Error should be cleared after refresh"
    
    def test_browser_back_button_from_inventory(self, login_page: LoginPage, inventory_page: InventoryPage):
        """Test browser back button functionality after login."""
        username, password = settings.get_user_credentials("standard")
        
        login_page.navigate()
        login_page.login(username, password)
        assert inventory_page.is_loaded()
        
        # Go back
        inventory_page.go_back()
        
        # Should still be on inventory page (no back to login without logout)
        assert "inventory" in inventory_page.get_url()


@pytest.mark.login
@pytest.mark.security
class TestLoginSecurity:
    """Security-related login tests."""
    
    @pytest.mark.parametrize("malicious_input", test_data.generate_malicious_inputs())
    def test_login_with_malicious_inputs(self, login_page: LoginPage, malicious_input):
        """Test login handles malicious inputs safely."""
        login_page.navigate()
        login_page.login(malicious_input, malicious_input)
        
        # Should either show error or reject input, but not crash or execute code
        assert login_page.is_error_displayed() or not login_page.is_visible(login_page.ERROR_MESSAGE)
        
        # Verify no script execution
        page_source = login_page.get_page_source()
        assert "<script>alert" not in page_source, "XSS script should not be executed"
    
    def test_sql_injection_attempt(self, login_page: LoginPage):
        """Test SQL injection prevention."""
        login_page.navigate()
        login_page.login("' OR '1'='1", "' OR '1'='1")
        
        assert login_page.is_error_displayed(), "SQL injection should be prevented"
    
    def test_password_not_visible_in_url(self, login_page: LoginPage):
        """Test that password doesn't appear in URL."""
        username, password = settings.get_user_credentials("standard")
        
        login_page.navigate()
        login_page.login(username, password)
        
        current_url = login_page.get_url()
        assert password not in current_url, "Password should never appear in URL"
        assert username not in current_url, "Username should never appear in URL for POST requests"
