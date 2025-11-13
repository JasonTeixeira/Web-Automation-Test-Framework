# Web Automation Test Framework

[![Tests](https://github.com/JasonTeixeira/Web-Automation-Test-Framework/actions/workflows/tests.yml/badge.svg)](https://github.com/JasonTeixeira/Web-Automation-Test-Framework/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.41.0-45ba4b.svg)](https://playwright.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web automation framework I built to test the [Sauce Demo](https://www.saucedemo.com) e-commerce app. Built with Python + Playwright, featuring 118+ tests, Page Object Model, multi-browser support, and a complete CI/CD pipeline.

```
╔══════════════════════════════════════════════════════════════╗
║                  WHAT I ACTUALLY BUILT                       ║
╠══════════════════════════════════════════════════════════════╣
║  118+ Tests        Login, inventory, cart, checkout, sorting ║
║  Page Objects      Clean separation: pages, tests, utils     ║
║  3 Browsers        Chromium, Firefox, WebKit (Safari)        ║
║  Parallel Exec     pytest-xdist, 4 workers by default        ║
║  CI/CD Pipeline    Multi-browser matrix, smoke tests first   ║
║  Docker Ready      Containerized with headless browser       ║
║  Auto Screenshots  On failure, saved to screenshots/         ║
║  Type-Safe         Pydantic config, full type hints          ║
╚══════════════════════════════════════════════════════════════╝
```

## Why This Exists

I wanted to build a real web automation framework—not just a pile of Selenium scripts. This project uses Playwright (faster, more stable than Selenium) and follows the Page Object Model so tests stay maintainable.

I tested [Sauce Demo](https://www.saucedemo.com) because it's a public e-commerce app with login, inventory, cart, and checkout flows. Real enough to be interesting, stable enough to not break randomly.

## Test Breakdown

```
┌──────────────────────────────────────────────────────────────┐
│  Test Suite          Tests   What They Cover                 │
├──────────────────────────────────────────────────────────────┤
│  Login               23      Auth flows, validation, security │
│                               Standard, problem, locked users │
│                               XSS/SQL injection attempts      │
│                                                              │
│  Inventory           33      Product display, add to cart    │
│                               Cart badge updates, UI state    │
│                               Data integrity checks           │
│                                                              │
│  Cart                28      Add/remove items, persistence   │
│                               Price calculations, workflows   │
│                               Multi-item scenarios            │
│                                                              │
│  Checkout            11      E2E purchase flows              │
│                               Form validation, price totals   │
│                               Cancel/back navigation          │
│                                                              │
│  Sorting             23      Name/price sorting              │
│                               Accuracy verification           │
│                               Sort state persistence          │
├──────────────────────────────────────────────────────────────┤
│  TOTAL               118+    Full e-commerce flow coverage   │
└──────────────────────────────────────────────────────────────┘
```

## Architecture

Built around the Page Object Model:

```
   Tests (118+)                   pytest markers + fixtures
        │
        v
   Page Objects                   clean abstraction layer
   ├── BasePage                    common methods (wait, click, type)
   ├── LoginPage                   login form, error messages
   ├── InventoryPage               product grid, add to cart
   ├── CartPage                    cart items, quantity, remove
   └── CheckoutPage                checkout forms, order complete
        │
        v
   Playwright Browser              Chromium / Firefox / WebKit
        │
        v
   Sauce Demo App                  https://www.saucedemo.com
```

### Why Page Objects?

I didn't want tests to break every time a button changed. Page objects isolate locators and page logic from tests. If the UI changes, I update one file, not 30 tests.

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- Docker (optional)

### Installation

```bash
git clone https://github.com/JasonTeixeira/Web-Automation-Test-Framework.git
cd Web-Automation-Test-Framework

python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

pip install --upgrade pip
pip install -r requirements.txt

# Install browsers (Chromium, Firefox, WebKit)
playwright install chromium firefox webkit

cp .env.example .env  # Edit if needed
```

## Configuration

Set via `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | App URL | `https://www.saucedemo.com` |
| `BROWSER` | Browser | `chromium` |
| `HEADLESS` | Headless mode | `false` |
| `PARALLEL_WORKERS` | Parallel workers | `4` |
| `TIMEOUT` | Timeout (ms) | `30000` |
| `SCREENSHOT_ON_FAILURE` | Auto-screenshot | `true` |
| `LOG_LEVEL` | Log level | `INFO` |

## Running Tests

```bash
# All tests
pytest tests/

# Specific suite
pytest tests/login/
pytest tests/inventory/
pytest tests/cart/
pytest tests/checkout/

# By marker
pytest -m smoke       # Fast smoke tests
pytest -m regression  # Full suite
pytest -m security    # Security tests

# Parallel (4 workers)
pytest tests/ -n 4

# Parallel (auto-scaling)
pytest tests/ -n auto

# HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Allure report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results

# Specific browser
BROWSER=chromium pytest tests/
BROWSER=firefox pytest tests/
BROWSER=webkit pytest tests/

# Headless
HEADLESS=true pytest tests/
```

## CI/CD Pipeline

GitHub Actions workflow runs on:
- Push to `main` or `develop`
- Pull requests
- Daily at 2 AM UTC
- Manual trigger

Jobs:
1. Code Quality: black, isort, pylint
2. Multi-Browser Matrix: Chromium, Firefox, WebKit in parallel
3. Smoke Tests: fast feedback (~2 min)
4. Allure Reports: auto-published to GitHub Pages
5. Notifications: Slack on failures

Smoke runs first. If it passes, the full suite fires across all browsers in parallel.

## Reporting

### HTML Reports

```bash
pytest tests/ --html=reports/report.html --self-contained-html
open reports/report.html
```

### Allure Reports

```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Screenshots on Failure

Automatically saved to `screenshots/` directory. Timestamped, includes test name.

### Logs

Colored console logs + file logs in `logs/`.

## Docker

```bash
# All tests
docker-compose up test-runner

# Smoke only
docker-compose --profile smoke up smoke-tests

# Specific suite
TEST_COMMAND="pytest tests/login/ -v" docker-compose --profile custom up specific-suite

# Build image
docker build -t web-automation-tests .

# Run with volume mounts
docker run --rm \\
  -v $(pwd)/reports:/app/reports \\
  -v $(pwd)/screenshots:/app/screenshots \\
  web-automation-tests
```

## What was hard (and how I fixed it)

- **Flaky waits**: Elements loading at different speeds. Fixed with Playwright's auto-waiting and smart locators.
- **Browser differences**: WebKit handles some elements differently than Chromium. Added browser-specific waits where needed.
- **Parallel test pollution**: Tests stepping on each other's data. Made tests generate unique user data per run (Faker).
- **Screenshot clutter**: Tests failing in CI left hundreds of screenshots. Added cleanup after successful runs.

## Decisions I made

- **Playwright over Selenium**: Auto-waits, faster, fewer flakes. Selenium felt ancient.
- **Page Object Model**: I didn't want to repeat locators across 118 tests. Centralize in page classes.
- **pytest-xdist for parallel**: Cuts execution time from 15 minutes to 5-7 minutes.
- **Pydantic for config**: Type-safe settings, catch misconfigurations early.
- **Multi-browser CI matrix**: Run all browsers in parallel, not sequentially. Faster feedback.

## Roadmap

- Visual regression tests (Playwright screenshots + pixel diff)
- Accessibility tests (axe-core integration)
- Performance profiling (Lighthouse)
- More negative edge cases (network failures, timeouts)

## License

MIT — see LICENSE.

## Docs

- Build Story: JOURNEY.md
