# Contributing to Web Automation Test Framework

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

---

## Code of Conduct

This project adheres to professional standards of conduct. By participating, you agree to:

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards other contributors

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of pytest and Playwright

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Web-Automation-Test-Framework.git
   cd Web-Automation-Test-Framework
   ```

2. **Run Setup Script**
   ```bash
   ./setup.sh
   ```

3. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

4. **Verify Installation**
   ```bash
   pytest tests/login/test_login.py -v
   ```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications

### 2. Make Your Changes

Follow the coding standards below and ensure:
- Code is well-documented
- Tests are added/updated
- All tests pass locally

### 3. Run Quality Checks

```bash
# Format code
black .
isort .

# Run linter
pylint pages utils config tests

# Run tests
pytest tests/ -v

# Check coverage
pytest --cov=pages --cov=utils --cov=config --cov-report=html
```

### 4. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git commit -m "feat: Add navigation tests for burger menu

- Add tests for menu open/close
- Test all menu links
- Verify logout functionality
- Add edge case tests"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Coding Standards

### Python Style Guide

We follow PEP 8 with these specific requirements:

**1. Code Formatting**
- Line length: 100 characters max
- Use Black for automatic formatting
- Use isort for import sorting

**2. Naming Conventions**
```python
# Classes: PascalCase
class LoginPage:
    pass

# Functions/Methods: snake_case
def get_product_name(self, index: int) -> str:
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30000

# Private methods: _leading_underscore
def _internal_helper(self):
    pass
```

**3. Type Hints**
Always use type hints:
```python
def login(self, username: str, password: str) -> None:
    """Login with credentials."""
    pass
```

**4. Docstrings**
Use Google-style docstrings:
```python
def add_product_to_cart(self, product_name: str) -> None:
    """
    Add a product to the shopping cart.
    
    Args:
        product_name: Name of the product to add
        
    Raises:
        ElementNotFoundError: If product doesn't exist
    """
    pass
```

### Page Object Model Guidelines

**1. One Page = One Class**
```python
class CartPage(BasePage):
    """Page object for shopping cart page."""
    
    # Locators as class constants
    CART_ITEM = '.cart_item'
    CHECKOUT_BUTTON = '[data-test="checkout"]'
    
    # Methods for page interactions
    def proceed_to_checkout(self) -> None:
        """Click checkout button."""
        self.click(self.CHECKOUT_BUTTON)
```

**2. Keep Page Objects Clean**
- Only page interactions in page objects
- No assertions in page objects
- No test logic in page objects
- Return data, don't assert on it

**3. Inherit from BasePage**
```python
class MyNewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
```

---

## Testing Guidelines

### Test Structure

**1. Test File Naming**
- File: `test_*.py`
- Example: `test_navigation.py`

**2. Test Class Organization**
```python
@pytest.mark.feature_name
class TestFeatureArea:
    """Tests for specific feature area."""
    
    def test_positive_scenario(self, fixtures):
        """Test successful operation."""
        pass
    
    def test_negative_scenario(self, fixtures):
        """Test error handling."""
        pass
```

**3. Test Method Naming**
- Use descriptive names
- Start with `test_`
- Be specific about what's being tested

```python
# Good
def test_login_with_valid_credentials_succeeds(self):
    pass

# Bad
def test_login(self):
    pass
```

### Test Categories (Markers)

Use pytest markers to categorize tests:

```python
@pytest.mark.smoke      # Critical path tests
@pytest.mark.regression # Full regression suite
@pytest.mark.login      # Login feature tests
@pytest.mark.cart       # Cart feature tests
@pytest.mark.slow       # Long-running tests
@pytest.mark.security   # Security tests
```

### Test Data Management

**1. Use Fixtures**
```python
@pytest.fixture
def test_product():
    """Provide test product data."""
    return Product(name="Test Product", price=9.99)
```

**2. Use Faker for Random Data**
```python
from utils import test_data

checkout_info = test_data.generate_checkout_data()
```

**3. Avoid Hardcoded Values**
```python
# Good
username, password = settings.get_user_credentials("standard")

# Bad
username = "standard_user"
```

### Assertions

**1. Be Explicit**
```python
# Good
assert cart_page.get_cart_item_count() == 3, "Cart should have 3 items"

# Bad
assert cart_page.get_cart_item_count() == 3
```

**2. One Assertion Per Concept**
```python
# Good - separate concerns
def test_login_redirects_to_inventory(self):
    login_page.login(username, password)
    assert inventory_page.is_loaded()
    
def test_login_displays_products(self):
    login_page.login(username, password)
    assert inventory_page.get_product_count() == 6

# Acceptable - related assertions
def test_successful_login(self):
    login_page.login(username, password)
    assert inventory_page.is_loaded()
    assert "/inventory.html" in inventory_page.get_url()
```

---

## Pull Request Process

### Before Submitting

1. ✅ All tests pass locally
2. ✅ Code follows style guidelines
3. ✅ New tests added for new features
4. ✅ Documentation updated
5. ✅ No merge conflicts with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. At least one approval required
2. All CI/CD checks must pass
3. Code coverage must not decrease
4. Documentation must be updated

---

## Project Structure

```
Web-Automation-Test-Framework/
├── .github/
│   └── workflows/          # CI/CD pipelines
├── config/
│   └── settings.py         # Configuration management
├── pages/
│   ├── base_page.py       # Base page class
│   ├── login_page.py      # Page objects
│   └── ...
├── tests/
│   ├── login/             # Login tests
│   ├── inventory/         # Inventory tests
│   ├── cart/              # Cart tests
│   ├── checkout/          # Checkout tests
│   └── sorting/           # Sorting tests
├── utils/
│   ├── logger.py          # Logging utilities
│   └── test_data.py       # Test data generation
├── conftest.py            # Pytest fixtures
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Container configuration
└── README.md             # Main documentation
```

### Adding New Tests

1. **Choose appropriate directory**
   - Feature-based organization
   - Create new directory if needed

2. **Create test file**
   ```bash
   touch tests/feature_name/test_feature.py
   ```

3. **Follow existing patterns**
   - Look at similar test files
   - Use same fixture patterns
   - Follow naming conventions

4. **Add markers**
   ```python
   @pytest.mark.feature_name
   @pytest.mark.smoke  # If critical
   ```

### Adding New Page Objects

1. **Create in pages/ directory**
   ```python
   # pages/new_page.py
   class NewPage(BasePage):
       def __init__(self, page: Page):
           super().__init__(page)
   ```

2. **Add to pages/__init__.py**
   ```python
   from .new_page import NewPage
   __all__ = [..., "NewPage"]
   ```

3. **Create fixture in conftest.py**
   ```python
   @pytest.fixture
   def new_page(page: Page) -> NewPage:
       return NewPage(page)
   ```

---

## Questions or Issues?

- Check existing issues on GitHub
- Create a new issue with detailed description
- Include error messages and steps to reproduce
- Tag appropriately (bug, enhancement, question)

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
