"""
Login page object for Sauce Demo application.
"""
from typing import Optional

from playwright.sync_api import Page

from config import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""
    
    # Locators
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    ERROR_BUTTON = '.error-button'
    LOGIN_LOGO = '.login_logo'
    BOT_COLUMN = '.bot_column'
    LOGIN_CREDENTIALS_CONTAINER = '#login_credentials'
    LOGIN_PASSWORD_CONTAINER = '.login_password'
    
    def __init__(self, page: Page):
        """
        Initialize login page.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = settings.base_url
    
    def navigate(self) -> None:
        """Navigate to login page."""
        self.navigate_to(self.url)
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login action.
        
        Args:
            username: Username to enter
            password: Password to enter
        """
        self.logger.info(f"Logging in with username: {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def enter_username(self, username: str) -> None:
        """
        Enter username only.
        
        Args:
            username: Username to enter
        """
        self.fill(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password only.
        
        Args:
            password: Password to enter
        """
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error is visible, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    def close_error_message(self) -> None:
        """Close the error message by clicking X button."""
        self.click(self.ERROR_BUTTON)
    
    def is_error_closed(self) -> bool:
        """
        Check if error message is closed/hidden.
        
        Returns:
            True if error is hidden, False otherwise
        """
        return self.is_hidden(self.ERROR_MESSAGE, timeout=5000)
    
    def get_username_placeholder(self) -> Optional[str]:
        """
        Get username input placeholder text.
        
        Returns:
            Placeholder text or None
        """
        return self.get_attribute(self.USERNAME_INPUT, 'placeholder')
    
    def get_password_placeholder(self) -> Optional[str]:
        """
        Get password input placeholder text.
        
        Returns:
            Placeholder text or None
        """
        return self.get_attribute(self.PASSWORD_INPUT, 'placeholder')
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.
        
        Returns:
            True if enabled, False if disabled
        """
        disabled = self.get_attribute(self.LOGIN_BUTTON, 'disabled')
        return disabled is None
    
    def get_logo_text(self) -> str:
        """
        Get logo text.
        
        Returns:
            Logo text
        """
        return self.get_text(self.LOGIN_LOGO)
    
    def is_logo_visible(self) -> bool:
        """
        Check if Sauce Labs logo is visible.
        
        Returns:
            True if visible, False otherwise
        """
        return self.is_visible(self.LOGIN_LOGO)
    
    def get_accepted_usernames(self) -> list[str]:
        """
        Get list of accepted usernames from the page.
        
        Returns:
            List of accepted usernames
        """
        credentials_text = self.get_text(self.LOGIN_CREDENTIALS_CONTAINER)
        # Parse usernames from text
        lines = credentials_text.split('\n')
        usernames = [line.strip() for line in lines if line.strip() and '_user' in line.lower()]
        return usernames
    
    def get_password_hint(self) -> str:
        """
        Get password hint from the page.
        
        Returns:
            Password hint text
        """
        return self.get_text(self.LOGIN_PASSWORD_CONTAINER)
    
    def clear_username(self) -> None:
        """Clear username input field."""
        self.page.locator(self.USERNAME_INPUT).clear()
    
    def clear_password(self) -> None:
        """Clear password input field."""
        self.page.locator(self.PASSWORD_INPUT).clear()
    
    def submit_with_enter_key(self) -> None:
        """Submit login form using Enter key."""
        self.press_key('Enter')
    
    def is_username_focused(self) -> bool:
        """
        Check if username field has focus.
        
        Returns:
            True if focused, False otherwise
        """
        focused_element = self.page.evaluate("document.activeElement.getAttribute('data-test')")
        return focused_element == 'username'
    
    def tab_to_password(self) -> None:
        """Tab from username to password field."""
        self.page.locator(self.USERNAME_INPUT).press('Tab')
    
    def tab_to_login_button(self) -> None:
        """Tab from password to login button."""
        self.page.locator(self.PASSWORD_INPUT).press('Tab')
    
    def get_page_source(self) -> str:
        """
        Get page source HTML.
        
        Returns:
            Page source HTML
        """
        return self.page.content()
    
    def refresh_page(self) -> None:
        """Refresh the login page."""
        self.reload()
