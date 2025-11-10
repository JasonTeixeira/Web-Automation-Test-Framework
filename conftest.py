"""
Pytest configuration and fixtures for the test framework.
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config import settings
from pages import (
    CartPage,
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    InventoryPage,
    LoginPage,
)
from utils import get_logger, test_data

logger = get_logger(__name__)


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")
    config.addinivalue_line("markers", "login: Login functionality tests")
    config.addinivalue_line("markers", "inventory: Inventory/product tests")
    config.addinivalue_line("markers", "cart: Shopping cart tests")
    config.addinivalue_line("markers", "checkout: Checkout flow tests")
    config.addinivalue_line("markers", "sorting: Sorting and filtering tests")
    config.addinivalue_line("markers", "navigation: Navigation tests")
    config.addinivalue_line("markers", "accessibility: Accessibility tests")
    config.addinivalue_line("markers", "visual: Visual regression tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "security: Security tests")


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """
    Session-scoped Playwright instance.
    
    Yields:
        Playwright instance
    """
    logger.info("Starting Playwright session")
    with sync_playwright() as p:
        yield p
    logger.info("Playwright session ended")


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """
    Session-scoped browser instance.
    
    Args:
        playwright_instance: Playwright instance from fixture
        
    Yields:
        Browser instance
    """
    logger.info(f"Launching {settings.browser} browser (headless={settings.headless})")
    
    browser_type = getattr(playwright_instance, settings.browser)
    browser = browser_type.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
    )
    
    yield browser
    
    logger.info("Closing browser")
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """
    Function-scoped browser context for test isolation.
    
    Args:
        browser: Browser instance from fixture
        
    Yields:
        Browser context
    """
    context = browser.new_context(
        viewport={
            "width": settings.viewport_width,
            "height": settings.viewport_height
        },
        record_video_dir="reports/videos" if settings.video_on_failure else None,
    )
    
    # Enable tracing if configured
    if settings.trace_on_failure:
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
        except Exception as e:
            logger.warning(f"Could not start tracing: {e}")
    
    yield context
    
    # Save trace on failure
    if settings.trace_on_failure:
        try:
            context.tracing.stop(path="reports/trace.zip")
        except Exception as e:
            logger.warning(f"Could not stop tracing: {e}")
    
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, request) -> Page:
    """
    Function-scoped page instance with automatic screenshot on failure.
    
    Args:
        context: Browser context from fixture
        request: Pytest request object
        
    Yields:
        Page instance
    """
    page = context.new_page()
    
    yield page
    
    # Take screenshot on test failure
    try:
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed and settings.screenshot_on_failure:
            screenshot_name = f"failure_{request.node.name}"
            screenshot_path = settings.screenshots_path / f"{screenshot_name}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.warning(f"Could not capture screenshot: {e}")
    
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution status for screenshot on failure.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# Page Object Fixtures

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """
    Login page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        LoginPage instance
    """
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """
    Inventory page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        InventoryPage instance
    """
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """
    Cart page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        CartPage instance
    """
    return CartPage(page)


@pytest.fixture
def checkout_step_one_page(page: Page) -> CheckoutStepOnePage:
    """
    Checkout step one page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        CheckoutStepOnePage instance
    """
    return CheckoutStepOnePage(page)


@pytest.fixture
def checkout_step_two_page(page: Page) -> CheckoutStepTwoPage:
    """
    Checkout step two page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        CheckoutStepTwoPage instance
    """
    return CheckoutStepTwoPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    """
    Checkout complete page object fixture.
    
    Args:
        page: Page instance
        
    Returns:
        CheckoutCompletePage instance
    """
    return CheckoutCompletePage(page)


# Helper Fixtures

@pytest.fixture
def logged_in_user(login_page: LoginPage, inventory_page: InventoryPage):
    """
    Fixture that provides a logged-in user session.
    
    Args:
        login_page: LoginPage instance
        inventory_page: InventoryPage instance
        
    Yields:
        Tuple of (login_page, inventory_page) after successful login
    """
    username, password = settings.get_user_credentials("standard")
    login_page.navigate()
    login_page.login(username, password)
    assert inventory_page.is_loaded(), "Failed to login"
    yield login_page, inventory_page


@pytest.fixture
def cart_with_items(logged_in_user, inventory_page: InventoryPage, cart_page: CartPage):
    """
    Fixture that provides a cart with items added.
    
    Args:
        logged_in_user: Logged in user fixture
        inventory_page: InventoryPage instance
        cart_page: CartPage instance
        
    Yields:
        Tuple of (inventory_page, cart_page, added_product_names)
    """
    # Add 2 products to cart
    product_names = inventory_page.get_all_product_names()[:2]
    for name in product_names:
        inventory_page.add_product_to_cart_by_name(name)
    
    inventory_page.click_shopping_cart()
    assert cart_page.is_loaded(), "Failed to navigate to cart"
    
    yield inventory_page, cart_page, product_names


@pytest.fixture
def checkout_data():
    """
    Fixture that provides randomized checkout data.
    
    Returns:
        CheckoutData instance with random data
    """
    return test_data.generate_checkout_data()


# Parameterized Fixtures for Different User Types

@pytest.fixture(params=["standard", "problem", "performance", "error", "visual"])
def user_type(request):
    """
    Parameterized fixture for different user types.
    
    Args:
        request: Pytest request object
        
    Returns:
        User type string
    """
    return request.param


@pytest.fixture
def user_credentials(user_type):
    """
    Fixture that provides credentials for specified user type.
    
    Args:
        user_type: User type string
        
    Returns:
        UserCredentials instance
    """
    return test_data.get_user_credentials(user_type)
