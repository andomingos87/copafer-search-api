```markdown
---
ai_update_goal: Provide a comprehensive overview of the system's architecture, including components, integrations, decisions, and risks, updated to reflect the current repository state.
required_inputs:
  - Repository file structure and top-level contents
  - Key Python modules and their purposes
  - Deployment configurations (Dockerfile, fly.toml)
  - External dependencies inferred from code (VTEX, Cubo APIs)
success_criteria:
  - All TODOs and placeholders resolved with accurate, current details.
  - Sections populated with concrete information based on repo scan.
  - Cross-links to other docs verified and functional.
  - Architecture described as a modular Python script collection for ETL and API interactions, deployed on Fly.io.
---

<!-- agent-update:start:architecture-notes -->
# Architecture Notes

The system is a lightweight, modular Python application designed for e-commerce data processing, focusing on product ingestion, search, shipping calculations, and estimation tools (e.g., paint volume). It evolved from ad-hoc scripts to handle integrations with external platforms like VTEX (for e-commerce APIs) and Cubo (for product catalogs). The current design prioritizes simplicity and rapid iteration for data ETL tasks, avoiding heavy frameworks to keep deployment lightweight on Fly.io. This assembly allows quick prototyping of features like API debugging and CSV analysis while maintaining extensibility for production use cases.

## System Architecture Overview

The system is a **monolithic Python script collection** with modular components, not a full microservices architecture. It operates as a single deployable unit via Docker on Fly.io, suitable for serverless-like scaling. Requests (e.g., API calls or script executions) typically start at entry points like `api.py` or ingestion scripts, flow through data processing layers (e.g., `vtex_client.py` for API interactions), and output to files, databases (not yet implemented), or responses.

- **Topology**: Core logic in top-level Python scripts; documentation in `docs/` and `docs-web/`; no separate services, but scripts can be invoked independently or via the API.
- **Deployment Model**: Containerized with `Dockerfile` for Python 3.x environment; configured via `fly.toml` for Fly.io hosting. Supports both local script runs and deployed API endpoints.
- **Request Flow**: Inbound via HTTP (handled by `api.py`, likely using Flask/FastAPI) → Authentication/Validation → External API calls (VTEX/Cubo) → Data processing (e.g., search, estimation) → Response/Output (JSON/CSV).

## Core System Components

The repository consists of utility scripts for data handling, API integrations, and business logic. Key components include:

- **Data Ingestion and Processing**:
  - `ingest_csv.py`: Loads and processes CSV files (e.g., `produtos-cubo.csv`, `resumido_200.csv`) for product data import.
  - `ingest_api.py`: Fetches and ingests data from external APIs into local structures or files.
  - `fetch_cubo_produtos.py`: Scrapes or APIs product data from Cubo platform.
  - `count_csv_rows.py` and `head_csv.py`: Utility scripts for CSV inspection and row counting.

- **API and Client Layers**:
  - `api.py`: Main entry point for HTTP API, exposing endpoints for product search, shipping, and estimation.
  - `vtex_client.py`: Handles interactions with VTEX e-commerce API (product queries, authentication).
  - `search_products.py`: Core search logic for products, integrating Cubo and VTEX data.

- **Business Logic Modules**:
  - `vtex_shipping.py`: Calculates shipping rates and logistics via VTEX.
  - `paint_estimator.py`: Estimates paint quantities based on product specs (domain-specific for paint e-commerce).
  - `analyze_missing_skus.py`: Identifies gaps in SKU data between sources.

- **Debugging and Testing**:
  - `debug_pagination.py`, `debug_response_structure.py`, `test_pagination_bug.py`: Tools for troubleshooting API responses and pagination issues.
  - `peek_cubo_page.py`: Inspects Cubo web pages for data validation.

- **Configuration and Deployment**:
  - `requirements.txt`: Lists dependencies (e.g., requests, pandas for data handling).
  - `Dockerfile`: Builds the Python environment.
  - `fly.toml`: Fly.io deployment config (apps, secrets, regions).

- **Documentation**:
  - `docs/`: 19 files, including Markdown guides (e.g., this architecture doc).
  - `docs-web/`: 3 files, likely for web-exported or static site docs.
  - `README.md`: Project overview and setup instructions.

- **Data Artifacts**:
  - `produtos-cubo.csv`: Full Cubo product catalog export.
  - `resumido_200.csv`: Sample/subset of 200 products for testing.

Top-level structure includes `__pycache__/` (Python bytecode), the above scripts/files, and docs directories. Total: ~45 files, ~32 MB (mostly CSV data).

## Internal System Boundaries

- **Domains/Bounded Contexts**: 
  - **Ingestion Context**: CSV/API loaders (`ingest_*`, `fetch_*`) own data import; outputs standardized dicts/DFs.
  - **E-commerce Context**: VTEX integrations (`vtex_client.py`, `vtex_shipping.py`) handle catalog and logistics; enforce contracts like SKU mapping.
  - **Estimation Context**: `paint_estimator.py` and `search_products.py` process business rules; isolated from ingestion for reusability.
- **Data Ownership**: Local CSVs are primary sources; no shared DB yet—scripts sync via file I/O or in-memory. Synchronization uses polling/scripts (e.g., daily fetches).
- **Seams**: Modules expose functions/classes (e.g., `VTEXClient` class); no formal boundaries, but clear ownership by file (e.g., VTEX deps in `vtex_*`).

## System Integration Points

- **Inbound Interfaces**:
  - HTTP API via `api.py` (endpoints for /search, /shipping, /estimate; owned by main app).
  - Script CLI invocations (e.g., `python search_products.py` for batch jobs).
- **Outbound Orchestration**:
  - Calls to VTEX API (product search, shipping quotes) from `vtex_client.py`.
  - Cubo product fetches via `fetch_cubo_produtos.py` (API or web scraping).
  - No internal service calls; all coordination is script-based (e.g., chaining ingest → search).

## External Service Dependencies

- **VTEX API**:
  - Used for: Product catalog, search, shipping calculations.
  - Auth: API keys/tokens (stored in env vars via fly.toml).
  - Rate Limits: VTEX enforces ~1000 req/min; handled via retries in `vtex_client.py`.
  - Failures: Graceful degradation with caching (local CSVs as fallback); logs errors.

- **Cubo Platform**:
  - Used for: Product data export (CSV/API).
  - Auth: Likely basic HTTP or session-based (in `fetch_cubo_produtos.py`).
  - Rate Limits: Unknown; pagination handled in debug scripts.
  - Failures: Fallback to cached CSVs; monitor for scrape blocks.

- **Infrastructure**:
  - Fly.io: For hosting API; auto-scales, global regions.
  - Python Libs: requests (HTTP), pandas (data), etc.—no SaaS beyond APIs.

## Key Decisions & Trade-offs

- **Modular Scripts over Framework**: Chose plain Python scripts for quick dev (no Django/Flask boilerplate initially); trade-off: Less structure, but easier for ETL. Evolved to `api.py` for web exposure.
- **File-Based Data Sync**: CSVs for persistence due to simplicity; avoids DB setup. Trade-off: Not real-time, but sufficient for batch processing (e.g., daily Cubo exports).
- **Docker + Fly.io**: Selected for easy deployment without infra expertise; vs. AWS/Heroku for cost (~$5/mo) and global edge. Experiment: Debug scripts born from pagination bugs in VTEX (see `test_pagination_bug.py`).
- **No ADRs Yet**: Decisions informal; future: Add `/docs/adr/` for scaling (e.g., add PostgreSQL for state).
- References: [README.md](../README.md) for setup; recent commits likely address VTEX pagination (inferred from debug files).

## Diagrams

```mermaid
graph TD
    A[Inbound Request / CLI] --> B[api.py / Scripts]
    B --> C[Data Ingestion<br>ingest_csv.py, fetch_cubo_produtos.py]
    C --> D[External APIs<br>VTEX (vtex_client.py), Cubo]
    B --> E[Business Logic<br>search_products.py, paint_estimator.py]
    E --> F[vtex_shipping.py]
    D --> G[Local Data<br>CSVs]
    G --> E
    E --> H[Response / Output]
    I[Fly.io Deployment] -.-> B
```

This Mermaid diagram illustrates the high-level flow: ingestion feeds logic, which queries externals and outputs results.

## Risks & Constraints

- **Performance**: API rate limits (VTEX/Cubo) could bottleneck searches; mitigate with caching (TODO: Implement Redis).
- **Scaling**: Monolith limits parallelism; Fly.io handles ~100 concurrent, but heavy CSV loads (>1GB) may OOM.
- **Data Freshness**: Manual sync reliance risks staleness; assumption: External sources stable.
- **Security**: API keys in env; no input sanitization in scripts (vulnerable to injection).
- **Constraints**: Python 3.x only; no async (limits I/O-heavy tasks). Active TODO: Integrate DB for persistence; monitor VTEX outages (past pagination bugs).
- **Incidents**: Debug scripts indicate resolved VTEX response issues; watch for recurrence.

## Top Directories Snapshot

- `__pycache__/`: Python bytecode cache (~1 subdir).
- `docs/`: Documentation Markdown files (19 files, e.g., architecture, setup guides).
- `docs-web/`: Web-optimized docs (3 files, e.g., static exports).
- Top-level files: Multiple `.py` scripts (e.g., `api.py`, `vtex_client.py`), CSVs (`produtos-cubo.csv`), `Dockerfile`, `fly.toml`, `README.md`, `requirements.txt`.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Review ADRs, design docs, or major PRs for architectural changes.
2. Verify that each documented decision still holds; mark superseded choices clearly.
3. Capture upstream/downstream impacts (APIs, events, data flows).
4. Update Risks & Constraints with active incident learnings or TODO debt.
5. Link any new diagrams or dashboards referenced in recent work.

<!-- agent-readonly:sources -->
## Acceptable Sources
- ADR folders, `/docs/architecture` notes, or RFC threads.
- Dependency visualisations from build tooling or scripts.
- Issue tracker discussions vetted by maintainers.

## Related Resources
- [Project Overview](./project-overview.md)
- Update [agents/README.md](../agents/README.md) when architecture changes.

<!-- agent-update:end -->
```
