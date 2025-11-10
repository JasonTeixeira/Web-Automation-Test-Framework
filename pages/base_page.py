"""
Base page class providing common functionality for all page objects.
"""
from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, expect

from config import settings
from utils.logger import get_logger


class BasePage:
    """Base class for all page objects with common functionality."""
    
    def __init__(self, page: Page):
        """
        Initialize base page.
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.timeout = settings.timeout
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
    
    def get_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title
        """
        return self.page.title()
    
    def get_url(self) -> str:
        """
        Get current URL.
        
        Returns:
            Current page URL
        """
        return self.page.url
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click an element.
        
        Args:
            selector: Element selector
            timeout: Optional timeout override
        """
        self.logger.debug(f"Clicking element: {selector}")
        self.page.click(selector, timeout=timeout or self.timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Fill an input field.
        
        Args:
            selector: Input selector
            value: Value to fill
            timeout: Optional timeout override
        """
        self.logger.debug(f"Filling '{selector}' with: {value}")
        self.page.fill(selector, value, timeout=timeout or self.timeout)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get element text content.
        
        Args:
            selector: Element selector
            timeout: Optional timeout override
            
        Returns:
            Element text content
        """
        return self.page.locator(selector).text_content(timeout=timeout or self.timeout) or ""
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get element attribute value.
        
        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Optional timeout override
            
        Returns:
            Attribute value or None
        """
        return self.page.locator(selector).get_attribute(attribute, timeout=timeout or self.timeout)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: Element selector
            timeout: Optional timeout override
            
        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False
    
    def is_hidden(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is hidden.
        
        Args:
            selector: Element selector
            timeout: Optional timeout override
            
        Returns:
            True if hidden, False otherwise
        """
        try:
            self.page.locator(selector).wait_for(state="hidden", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False
    
    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> None:
        """
        Wait for element to reach specified state.
        
        Args:
            selector: Element selector
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Optional timeout override
        """
        self.logger.debug(f"Waiting for '{selector}' to be {state}")
        self.page.locator(selector).wait_for(state=state, timeout=timeout or self.timeout)
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern to match (can be substring or regex)
            timeout: Optional timeout override
        """
        self.logger.debug(f"Waiting for URL to contain: {url_pattern}")
        self.page.wait_for_url(f"**/*{url_pattern}*", timeout=timeout or self.timeout)
    
    def get_element_count(self, selector: str) -> int:
        """
        Get count of elements matching selector.
        
        Args:
            selector: Element selector
            
        Returns:
            Number of matching elements
        """
        return self.page.locator(selector).count()
    
    def get_all_texts(self, selector: str) -> list[str]:
        """
        Get text content of all elements matching selector.
        
        Args:
            selector: Element selector
            
        Returns:
            List of text contents
        """
        return self.page.locator(selector).all_text_contents()
    
    def screenshot(self, name: str, full_page: bool = False) -> Path:
        """
        Take a screenshot.
        
        Args:
            name: Screenshot filename (without extension)
            full_page: Whether to capture full page
            
        Returns:
            Path to screenshot file
        """
        screenshot_path = settings.screenshots_path / f"{name}.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Taking screenshot: {screenshot_path}")
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        return screenshot_path
    
    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll element into view.
        
        Args:
            selector: Element selector
        """
        self.logger.debug(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def select_option(self, selector: str, value: str) -> None:
        """
        Select option from dropdown.
        
        Args:
            selector: Select element selector
            value: Option value to select
        """
        self.logger.debug(f"Selecting option '{value}' from {selector}")
        self.page.select_option(selector, value)
    
    def press_key(self, key: str) -> None:
        """
        Press a keyboard key.
        
        Args:
            key: Key to press (e.g., 'Enter', 'Escape')
        """
        self.logger.debug(f"Pressing key: {key}")
        self.page.keyboard.press(key)
    
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over an element.
        
        Args:
            selector: Element selector
            timeout: Optional timeout override
        """
        self.logger.debug(f"Hovering over: {selector}")
        self.page.hover(selector, timeout=timeout or self.timeout)
    
    def reload(self) -> None:
        """Reload the current page."""
        self.logger.info("Reloading page")
        self.page.reload(timeout=self.timeout)
    
    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.logger.info("Navigating back")
        self.page.go_back(timeout=self.timeout)
    
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.logger.info("Navigating forward")
        self.page.go_forward(timeout=self.timeout)
