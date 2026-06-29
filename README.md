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

## Notes
- This project intentionally contains no business logic yet.
- Authentication is intentionally left as placeholders for future implementation.
- Database schema initialization is executed on application startup.
