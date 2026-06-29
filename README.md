# Inventory and Sales Management System (FastAPI Scaffold)

A clean-architecture oriented project scaffold for an inventory and sales management system.

## Tech Stack
- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2 templates

## Architecture Overview
This scaffold follows clean architecture principles by organizing responsibilities into layers:
- Routers: HTTP and REST endpoint definitions
- Schemas: API contracts and validation models
- Services: application use-case orchestration
- Models: persistence entities
- Database: engine and session management

Dependency direction is intended to be:
`routers -> services -> models/database`

## Project Structure

```text
app/
  core/
  database/
  models/
  routers/
  schemas/
  services/
  static/
  templates/
tests/
```

## Run Locally

1. Create and activate a Python 3.13 virtual environment.

   **Windows**

   ```bash

   python -m venv .venv

   .venv\Scripts\activate

   ```

   **macOS / Linux**

   ```bash

   python3.13 -m venv .venv

   source .venv/bin/activate

   ```

   Once activated, your terminal should display the virtual environment name (e.g., `(.venv)`), indicating that all dependencies will be installed in an isolated environment.

2. Install dependencies:

   ```bash

   pip install -r requirements.txt

   ```

3. Run the application:

   ```bash

   uvicorn app.main:app --reload

   ```

   Or run it directly with Python:

   ```bash

   python -m app.main

   ```

## Testing Environment

This project uses `pytest` as the primary test runner with API, unit, and negative-case coverage.

### Installation

1. Activate the project virtual environment.

    **Windows**

    ```bash
    .venv\Scripts\activate
    ```

    **macOS / Linux**

    ```bash
    source .venv/bin/activate
    ```

2. Install all dependencies (including test tools):

    ```bash
    pip install -r requirements.txt
    ```

Test tooling included in the project:
- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `httpx`

### Running Tests

Run the entire test suite:

```bash
source .venv/bin/activate && pytest -q
```

Run only API integration tests:

```bash
source .venv/bin/activate && pytest tests/api -q
```

Run only unit service tests:

```bash
source .venv/bin/activate && pytest tests/unit/services -q
```

Run one specific test module:

```bash
source .venv/bin/activate && pytest tests/api/test_products_api.py -q
```

### Coverage

Coverage is configured through `pytest.ini` and `.coveragerc`.

Run tests with terminal coverage + HTML output:

```bash
source .venv/bin/activate && pytest --cov-report=term-missing --cov-report=html -q
```

Run with a minimum coverage threshold (example 85%):

```bash
source .venv/bin/activate && pytest --cov-report=term-missing --cov-report=html --cov-fail-under=85 -q
```

Coverage output locations:
- Terminal summary after test execution
- HTML report at `htmlcov/index.html`

### Test Folder Structure

```text
tests/
   conftest.py                     # shared fixtures: test DB, clients, overrides
   factories.py                    # reusable model and payload builders
   test_health.py                  # basic health endpoint test
   api/
      test_categories_api.py        # categories API integration tests
      test_products_api.py          # products API integration tests
      test_sales_api.py             # sales API integration tests
      test_negative_cases_api.py    # negative and edge-case API scenarios
   unit/
      services/
         test_category_service.py    # CategoryService unit tests
         test_product_service.py     # ProductService unit tests
         test_sale_service.py        # SaleService unit tests
```

### Troubleshooting

#### `pytest: command not found`

- Activate the virtual environment first:

   ```bash
   source .venv/bin/activate
   ```

- Reinstall dependencies:

   ```bash
   pip install -r requirements.txt
   ```

#### Tests fail due to stale environment packages

Reinstall from scratch in the active environment:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### SQLite / test isolation concerns

- Tests use a temporary SQLite database and dependency overrides in `tests/conftest.py`.
- If behavior looks inconsistent, run tests again from a clean process:

   ```bash
   source .venv/bin/activate && pytest -q
   ```

#### Coverage report not generated

- Ensure tests are run with `--cov-report=html`.
- Open `htmlcov/index.html` after execution.

#### Deprecation warnings from async fixtures

- The repository sets `asyncio_default_fixture_loop_scope = function` in `pytest.ini`.
- If warnings still appear, confirm you are running tests from this repository root and active `.venv`.
