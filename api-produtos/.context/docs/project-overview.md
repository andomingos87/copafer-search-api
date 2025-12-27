<!-- agent-update:start:project-overview -->
# Project Overview

This project implements a Python-based API for searching and managing product data, primarily integrated with VTEX (an e-commerce platform). It solves the problem of efficiently querying and ingesting product catalogs (e.g., from CSV sources or VTEX APIs), handling pagination, SKU analysis, and custom business logic like paint estimation. Beneficiaries include e-commerce developers, product managers, and operations teams at Copager (inferred from repo path), who need reliable tools for product data synchronization, debugging, and API exposure.

## Quick Facts
- Root path: `C:\Users\Anderson Domingos\Documents\Projetos\copager_agent\api-produtos\search_products_api`
- Primary languages detected:
  - Python (.py: 15 files)
  - Markdown (.md: 19 files)
  - CSV (.csv: 2 files)
  - Text (.txt: 1 file)
  - TOML (.toml: 1 file)

## File Structure & Code Organization
- `__pycache__/` — Contains compiled Python bytecode files (.pyc) automatically generated when Python modules are imported for faster execution. This directory is auto-generated, transient, and typically ignored in version control (e.g., via .gitignore).
- `analyze_missing_skus.py` — A utility script for analyzing and identifying missing Stock Keeping Units (SKUs) in product datasets, likely by cross-referencing CSV files or API responses against expected catalogs.
- `api.py` — The core FastAPI (or similar) application file that defines the search products API endpoints, handles requests for product queries, and integrates with VTEX clients for data retrieval and shipping calculations.
- `count_csv_rows.py` — A simple utility script to count the total number of rows in CSV files, useful for data validation and ingestion monitoring.
- `debug_pagination.py` — A debugging script focused on investigating and logging pagination behavior in API responses, helping diagnose issues with large product datasets.
- `debug_response_structure.py` — A script for inspecting and printing the structure of API responses (e.g., JSON schemas from VTEX), aiding in troubleshooting data inconsistencies.
- `Dockerfile` — Defines the Docker image build process for containerizing the Python API application, including base image (e.g., Python 3.x), dependency installation, and runtime configuration for deployment.
- `docs/` — Living documentation produced by this tool, containing Markdown guides on project setup, workflows, and architecture.
- `docs-web/` — A subdirectory for web-optimized documentation, possibly generated static sites (e.g., via MkDocs or similar) or assets for hosting docs online.
- `fetch_cubo_produtos.py` — A script to fetch and download product data from an external "Cubo Produtos" source (likely a database or API), saving it as CSV for local ingestion.
- `fly.toml` — Configuration file for deploying the application to Fly.io, specifying app name, regions, environment variables, and build settings for scalable hosting.
- `head_csv.py` — A utility script mimicking the Unix `head` command to display the first N rows of a CSV file, useful for quick data previews during development or debugging.
- `ingest_api.py` — Handles ingestion of product data directly via API calls, possibly syncing updates from VTEX or other sources into local storage.
- `ingest_csv.py` — Processes and ingests CSV files (e.g., `produtos-cubo.csv`) into the system, performing parsing, validation, and database/API uploads.
- `paint_estimator.py` — Implements business logic for estimating paint quantities or costs based on product data, likely tailored to Copager's domain (e.g., construction/supplies e-commerce).
- `peek_cubo_page.py` — A lightweight script to preview or sample pages of paginated data from the "Cubo Produtos" source, useful for testing without full downloads.
- `produtos-cubo.csv` — A sample or primary CSV dataset containing product information from the "Cubo Produtos" catalog, including fields like SKUs, descriptions, prices, and categories.
- `README.md` — The main project readme file, providing an introduction, setup instructions, and links to key resources like this documentation.
- `requirements.txt` — Lists Python dependencies (e.g., fastapi, vtex-api, pandas) required for the project, used with `pip install -r requirements.txt` for environment setup.
- `resumido_200.csv` — A summarized or truncated CSV file limited to 200 rows, likely used for testing, demos, or reduced-scale data processing.
- `search_products.py` — Core module for product search functionality, including query building, filtering, and integration with VTEX for real-time searches.
- `test_pagination_bug.py` — A test script specifically targeting a known pagination bug in API responses, reproducing issues and validating fixes.
- `vtex_client.py` — A client module for interacting with the VTEX e-commerce API, handling authentication, product queries, and data extraction.
- `vtex_shipping.py` — Module for calculating and retrieving shipping information via VTEX APIs, integrated into product search responses for e-commerce workflows.

## Technology Stack Summary
- Primary runtime: Python 3.x.
- Languages: Python for backend logic and scripts; Markdown for documentation.
- Platforms: Docker for containerization; Fly.io for deployment and scaling.
- Build tooling: Pip for dependency management; no formal build step, but scripts support ad-hoc execution.
- Linting and formatting: Not explicitly configured (e.g., no .pre-commit or black setup detected); contributors should use tools like pylint or black manually.
- Data handling: Pandas (inferred from CSV scripts) for processing; requests or httpx for API calls.

## Core Framework Stack
- Backend: FastAPI (inferred from api.py structure) for RESTful API development, enforcing async patterns and OpenAPI documentation.
- Data layer: Pandas and CSV handling for ingestion; VTEX SDK/client for e-commerce integration.
- No frontend or messaging layers present; focus is on API and utility scripts.
- Architectural patterns: Modular scripts for utilities; API-first design with dependency injection (via FastAPI); stateless services suitable for container deployment.

## UI & Interaction Libraries
- No graphical UI; project is CLI and API-focused.
- CLI helpers: Custom Python scripts (e.g., debug tools) using libraries like click or argparse (if present).
- No theming, accessibility, or localization requirements, as interactions are programmatic.

## Development Tools Overview
- Essential CLIs: Python interpreter, pip for installs, Docker for building/running containers, flyctl for Fly.io management.
- Scripts: Run utilities directly (e.g., `python search_products.py`) or start API with `uvicorn api:app`.
- Link to [Tooling & Productivity Guide](./tooling.md) for deeper setup instructions.

## Getting Started Checklist
1. Install dependencies with `pip install -r requirements.txt`.
2. Explore the API by running `uvicorn api:app --reload` (assuming FastAPI setup).
3. Review [Development Workflow](./development-workflow.md) for day-to-day tasks.

## Next Steps
This project positions as a backend service for product search in VTEX-integrated e-commerce, with emphasis on data ingestion from CSV sources and custom estimators (e.g., paint). Key stakeholders: Developers at Copager for API maintenance; product teams for data accuracy. External links: VTEX API docs (https://developers.vtex.com/docs); no formal roadmap in repo—check issues for priorities. For specs, refer to CSV schemas in `produtos-cubo.csv` or API endpoints in `api.py`.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Review roadmap items or issues labelled “release” to confirm current goals.
2. Cross-check Quick Facts against `package.json` and environment docs.
3. Refresh the File Structure & Code Organization section to reflect new or retired modules; keep guidance actionable.
4. Link critical dashboards, specs, or runbooks used by the team.
5. Flag any details that require human confirmation (e.g., stakeholder ownership).

<!-- agent-readonly:sources -->
## Acceptable Sources
- Recent commits, release notes, or ADRs describing high-level changes.
- Product requirement documents linked from this repository.
- Confirmed statements from maintainers or product leads.

<!-- agent-update:end -->
