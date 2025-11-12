# Web Automation Framework: Build Journey

## Why I Built This

I wanted to build a real web automation framework—not just a collection of brittle Selenium scripts that break every time the UI changes. This project uses Playwright (modern, fast, stable) and follows the Page Object Model so tests stay maintainable as the app evolves.

I tested [Sauce Demo](https://www.saucedemo.com) because it's a publicly available e-commerce app with real workflows: login, inventory browsing, cart management, and checkout. It's stable enough to not flake randomly, and realistic enough to demonstrate proper test automation patterns.

---

## Timeline

### Week 1: Foundation

**Goal:** Get Playwright working with a basic test structure.

- Set up project: pages/, tests/, utils/, config/
- Built BasePage with common methods (wait, click, type, assert)
- Created first page objects: LoginPage, InventoryPage
- Wrote first 20 tests (login flows, basic inventory checks)
- Added pytest fixtures in conftest.py for browser setup/teardown

**Problem I Hit:** Playwright's auto-wait wasn't enough for some dynamic elements. Tests were flaking on slow network.

**Fix:** Added explicit waits for specific elements that load async. Used `page.wait_for_selector()` with timeout fallbacks. Tests stabilized.

### Week 2: Test Coverage

**Goal:** Get to 100+ tests across all major flows.

- Added CartPage and CheckoutPage objects
- Wrote cart tests (28 tests): add/remove items, price calculations, persistence
- Wrote checkout tests (11 tests): E2E purchase flows, form validation
- Added sorting tests (23 tests): name/price sorting, accuracy verification
- Implemented test data generation with Faker

**Problem I Hit:** Parallel tests were stepping on each other. Multiple tests trying to use the same user account.

**Fix:** Made tests generate unique test data per run. Each test uses its own data (Faker generates random names, addresses). No shared state between tests.

### Week 3: Multi-Browser + CI/CD

**Goal:** Get tests running across browsers and automate in CI.

- Added multi-browser support: Chromium, Firefox, WebKit (Safari)
- Created GitHub Actions workflow with browser matrix
- Added smoke tests marker for fast feedback
- Set up Allure reporting auto-published to GitHub Pages
- Added screenshot-on-failure with cleanup

**Problem I Hit:** WebKit (Safari) handles some elements differently than Chromium. Tests passing in Chrome but failing in Safari.

**Fix:** Added browser-specific waits where needed. Identified elements that render slower in WebKit and added explicit waits. All browsers green now.

### Week 4: Polish + Parallel Execution

**Goal:** Make it production-ready.

- Added pytest-xdist for parallel execution (4 workers)
- Docker containerization with headless browser support
- Type hints everywhere (mypy)
- Code quality: black, isort, pylint
- HTML reports for local debugging
- Pydantic config for type-safe settings
- Full documentation

**Problem I Hit:** Tests failing in CI left hundreds of screenshots cluttering the repo.

**Fix:** Added cleanup logic to delete screenshots after successful runs. Only keep screenshots for failures. Added `.gitignore` rules for local screenshots.

---

## Decisions I Made (and Why)

### Playwright over Selenium

I tried Selenium first. Spent 2 days fighting flaky waits and stale element exceptions. Playwright has auto-waiting built-in, faster execution, and better debugging tools. No regrets switching.

### Page Object Model

I didn't want to copy-paste locators across 118 tests. Page objects centralize locators and page logic. If a button ID changes, I update one file, not 30 tests.

Example:
- LoginPage has all login form locators and methods (login, check_error_message)
- Tests just call `login_page.login(username, password)` and assert on outcomes
- Clean separation: tests focus on behavior, page objects handle DOM interaction

### pytest-xdist for Parallel Execution

Sequential runs took 15+ minutes. pytest-xdist splits tests across workers. With 4 workers, full suite runs in 5-7 minutes. CI feedback is much faster.

### Multi-Browser CI Matrix

Instead of running browsers sequentially (Chromium → Firefox → WebKit), I run them in parallel as separate jobs. Full cross-browser suite finishes in ~7 minutes instead of 20+.

### Faker for Test Data

Hard-coded test data is brittle. Faker generates realistic names, addresses, emails per test run. Makes tests more robust and easier to read.

---

## What Was Hard

### Flaky Waits

Playwright auto-waits for elements, but some dynamic content (lazy-loaded images, async API calls) still caused flakes. I added explicit waits for specific elements and tuned timeouts.

### Browser Differences

WebKit (Safari) renders some elements differently than Chromium. Had to add browser-specific logic in a few places. Not ideal, but necessary for cross-browser coverage.

### Parallel Test Pollution

When tests run in parallel, they can step on each other's data. I made tests stateless by generating unique data per run and avoiding shared state.

### Screenshot Management

Tests failing in CI left hundreds of screenshots. I added cleanup logic to delete screenshots after successful runs. Only keep failures for debugging.

---

## What I'd Do Differently

- **Visual Regression**: Add Playwright screenshot comparison for UI consistency checks.
- **Accessibility**: Integrate axe-core for WCAG compliance testing.
- **Performance**: Add Lighthouse profiling to catch performance regressions.
- **More Negative Cases**: Simulate network failures, timeouts, malformed responses.
- **Better Reporting**: Custom Allure categories and trends for better failure analysis.

---

## Stats

- Total Tests: 118+
- Test Suites: 5 (Login, Inventory, Cart, Checkout, Sorting)
- Browsers: 3 (Chromium, Firefox, WebKit)
- Page Objects: 6 (Base + 5 specific)
- Execution Time: 5-7 minutes (parallel), 15+ minutes (sequential)
- CI Jobs: 5 (code quality, multi-browser matrix, smoke, Allure, notifications)

---

## Tools I Used

- Python 3.11 (type hints, async/await)
- Playwright (browser automation)
- Pytest (test framework, fixtures, markers)
- pytest-xdist (parallel execution)
- Faker (test data generation)
- Pydantic (type-safe config)
- Black, isort, pylint, mypy (code quality)
- GitHub Actions (CI/CD)
- Docker (containerization)
- Allure (reporting)

---

## What I Learned

- Playwright is vastly better than Selenium for modern web apps
- Page Object Model is non-negotiable for maintainability at scale
- Parallel execution saves massive amounts of time (15 min → 5 min)
- Cross-browser testing catches real issues (WebKit quirks)
- Stateless tests are critical for parallel execution
- Auto-waiting is powerful but not magic (still need explicit waits sometimes)
- Screenshot management matters in CI (cleanup after success)

---

## Why Playwright Over Selenium

Tried Selenium first. Problems I hit:
- Flaky waits everywhere (WebDriverWait hell)
- Stale element exceptions constantly
- Slow execution (no connection reuse)
- No auto-waiting (had to write custom wait logic)

Playwright fixed all of this:
- Auto-waits for elements (smart detection)
- Connection reuse (faster execution)
- Better debugging (Playwright Inspector, trace viewer)
- Modern API (async/await, cleaner syntax)
- Multi-browser support out of the box

---

Coffee consumed: A lot.

Times I rewrote page objects: 2 (refactored after hitting 50 tests).

Times I cursed WebKit: Too many.

Worth it? Absolutely.
