# Playwright + pytest POM Framework — Interview Study Guide

A test-automation framework that tests **carwale.com** using **Playwright** (browser
automation) + **pytest** (test runner) + **Page Object Model** (design pattern) +
**Allure** (reports). Data is externalised in **Excel**, locators/URL in an **INI** file.

---

## 0. 30-SECOND ELEVATOR PITCH (say this if asked "tell me about your framework")
> "It's a UI automation framework in Python using Playwright and pytest, built on the
> Page Object Model. Every web page is a class that holds its locators and actions, so
> tests stay readable and locator changes happen in one place. Test data lives in Excel,
> locators and the base URL live in a config.ini, and I use pytest fixtures in conftest.py
> for browser/page setup and teardown. Tests are data-driven via pytest parametrize, and I
> generate Allure reports with screenshots, video, and Playwright traces attached on failure.
> It runs locally and in Jenkins CI."

---

## 1. ARCHITECTURE (layers, top = test, bottom = browser)

```
testcases/Test_CarWale.py     <- WHAT to test (business scenarios + assertions)
        |  uses
pages/  HomePage, NewCarsPage, CarBase, BMWCarsPage...   <- HOW to talk to each page (POM)
        |  inherit
pages/BasePage.py             <- reusable actions: click / type / move_to
        |  reads
utilities/  configReader, dataProvider, ExcelReader, LogUtil  <- helpers
        |  read
ConfigurationData/conf.ini  +  excel/testdata.xlsx           <- config + data
        |
testcases/conftest.py         <- the ENGINE: fixtures that build browser/page, tracing, video, screenshots
```

| Folder | Role |
|--------|------|
| `ConfigurationData/conf.ini` | Base URL + all locators (XPaths), grouped in sections |
| `excel/testdata.xlsx` | Test data (sheet `NewCarsTest` = carBrand + expected carTitle) |
| `utilities/configReader.py` | `readConfig(section, key)` → reads conf.ini |
| `utilities/dataProvider.py` | `get_data(sheet)` → returns Excel rows for parametrize |
| `utilities/ExcelReader.py` | Generic Excel read/write helpers |
| `utilities/LogUtil.py` | `Logger` class → writes to `logs/log<date>.txt` |
| `pages/BasePage.py` | Parent of all pages; wraps Playwright click/fill/hover |
| `pages/*Page.py` | One class per page; methods = user actions |
| `testcases/conftest.py` | pytest fixtures: browser, page, navigation, screenshot-on-fail |
| `testcases/BaseTest.py` | Parent test class; auto-applies fixtures |
| `testcases/Test_CarWale.py` | The actual tests |

---

## 2. CORE CONCEPTS (the things they WILL ask)

**Page Object Model (POM):** each page = a class holding its locators + actions. Tests call
page methods instead of touching selectors. Benefit: readable tests + change a locator in ONE
place when the UI changes (maintainability), no duplication (DRY).

**Inheritance (BasePage):** common actions (`click`, `type`, `move_to`) live in `BasePage`;
every page `class HomePage(BasePage)` inherits them. `super().__init__(page)` passes the
Playwright page up to the parent.

**Page chaining / fluent interface:** a page method returns the *next* page object, so you can
write `home.find_new_cars().go_to_BMW()`. It mirrors how a real user navigates.

**pytest fixtures (conftest.py):** functions that provide setup + teardown. Key ideas:
- `yield` splits setup (before) from teardown (after).
- `scope="function"` = fresh per test (also class/module/session).
- `autouse=True` = runs automatically without being requested (e.g. opening the URL).
- fixtures can request other fixtures → `page` requests `browser` (dependency injection).
- conftest.py is auto-discovered by pytest — no imports needed in tests.

**Data-driven testing:** `@pytest.mark.parametrize("carBrand,carTitle", dataProvider.get_data("NewCarsTest"))`
runs the same test once per Excel row. One test, many data sets.

**Externalised config & data:** no hardcoding. URL + locators in `conf.ini`; data in Excel.
Change environment/data without touching code.

**Allure reporting:** `@allure.feature`, `@allure.severity`, `with allure.step(...)` label the
report; on failure a screenshot is attached. `--alluredir=allure-results` writes raw results;
the Allure tool renders the HTML report.

---

## 3. END-TO-END FLOW (trace `test_select_cars` for BMW)

1. pytest finds `Test_CarWale(BaseTest)`; `BaseTest` has `@pytest.mark.usefixtures("log_on_failure","page")`.
2. `parametrize` expands the test into 4 runs (BMW, MG, Toyota, Honda) from Excel.
3. Fixtures resolve in order: `browser` (launch Chromium) → `page` (new context + start tracing +
   record video + new page + viewport 1920×1080) → `setup_function` (autouse → `page.goto(carwale URL)`).
4. Test body:
   - `home = HomePage(page)`
   - `home.find_new_cars()` → hover "NEW CARS", click "Find New Cars" → returns `NewCarsPage`
   - `.go_to_BMW()` → click "BMW" → returns `BMWCarsPage`
   - `title = CarBase(page).get_title()` → reads `<h1>` text
   - `assert title == carTitle` (expected "BMW Cars")
5. Teardown: wait 2s → stop tracing → `trace.zip` → if test failed, attach screenshot to Allure →
   close page/context → close browser.
6. `allure-results` filled → Allure report generated.

---

## 4. PLAYWRIGHT API USED (quick reference)

| Code | Meaning |
|------|---------|
| `sync_playwright()` | Start Playwright (sync API) |
| `p.chromium.launch(headless=False)` | Launch a visible Chromium browser |
| `browser.new_context(record_video_dir=...)` | Isolated session (like incognito) + video |
| `context.tracing.start/stop` | Record a trace (screenshots/snapshots) → debug in trace viewer |
| `context.new_page()` | Open a tab |
| `page.goto(url)` | Navigate |
| `page.locator(xpath)` | Find element(s) — Playwright auto-waits |
| `.click() / .fill(v) / .hover()` | Actions |
| `.inner_text()` | Read text |
| `.nth(i) / .count()` | Work with lists of elements |

> Playwright **auto-waits** for elements to be actionable — so `time.sleep()` in the tests is an
> anti-pattern (see §6).

---

## 5. LIKELY INTERVIEW Q&A

**Q: What is POM and why use it?**
A: Page Object Model — each page is a class with its locators + actions. Improves readability,
reusability, and maintainability (locator changes in one place).

**Q: Difference between `browser`, `context`, and `page`?**
A: Browser = the app; context = an isolated session (cookies/storage/incognito-like); page = a tab.
One browser → many contexts → many pages. Contexts keep tests isolated.

**Q: What is conftest.py?**
A: A special pytest file auto-discovered for sharing fixtures/hooks across tests without importing.

**Q: Fixture scopes?**
A: function (default), class, module, session — controls how often setup/teardown runs.

**Q: What does `yield` do in a fixture?**
A: Code before `yield` = setup, code after = teardown. pytest runs teardown even if the test fails.

**Q: How is your test data-driven?**
A: `@pytest.mark.parametrize` fed by `dataProvider.get_data()` which reads Excel via openpyxl.

**Q: How do you handle waits?**
A: Playwright auto-waits for elements; I prefer `expect()`/`wait_for_*` over hard `sleep()`.

**Q: How do you report failures?**
A: Allure: steps, severity, feature tags, plus screenshot + video + trace attached on failure.

**Q: How do you run cross-browser?**
A: The `browser` fixture is parametrised (`params=["chrome"]`); add "firefox"/"webkit" to fan out.

**Q: How do you run in parallel / in CI?**
A: `pytest-xdist` (`pytest -n 4`); Jenkins runs `pytest ... --alluredir` and an Allure post-build step.

---

## 6. GOTCHAS & "WHAT WOULD YOU IMPROVE" (shows senior thinking)

- **`time.sleep(3)` everywhere** → replace with Playwright auto-wait / `expect()` (faster, less flaky).
- **`CarBase` doesn't extend `BasePage`** → inconsistent; could inherit for reuse.
- **Brand pages (BMW/Toyota/...) are empty** → placeholders for future brand-specific actions.
- **`global page` in conftest** → a hack so `log_on_failure` can see the page; cleaner to request the `page` fixture.
- **`log_on_failure` reads `item.rep_call`** → that attribute needs a `pytest_runtest_makereport`
  hook (standard pattern). If it's not in conftest, screenshot-on-failure won't fire — worth fixing.
- **`ExcelReader.py` has code at the bottom that runs on import** (and even writes "DOB" into the
  file). Side-effecting imports are bad practice — that logic belongs under `if __name__ == "__main__":`.
- **Excel typo `"Toyota Carss"`** (double s) → makes the Toyota assertion FAIL. That's a *data* bug,
  not a framework/browser bug. (The course author blamed the mouse — it's actually this.)
- **Fragile XPaths** like `//div/div/div/div/a/h3` → prefer role/text/test-id locators.

---

## 7. COMMANDS

```bash
pytest -v -s testcases/Test_CarWale.py --alluredir=allure-results   # run + collect
allure serve allure-results                                          # open report
pytest -n 4                                                          # parallel (xdist)
```
