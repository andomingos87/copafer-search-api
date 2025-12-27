<!-- agent-update:start:data-flow -->
# Data Flow & Integrations

Explain how data enters, moves through, and exits the system, including interactions with external services.

## High-level Flow
The primary pipeline begins with data ingestion from external sources, such as CSV files (e.g., `produtos-cubo.csv` or `resumido_200.csv`) or API endpoints from Cubo and VTEX. Data is fetched and processed through dedicated scripts like `fetch_cubo_produtos.py`, `ingest_csv.py`, and `ingest_api.py`. Processing involves searching products (`search_products.py`), analyzing missing SKUs (`analyze_missing_skus.py`), counting rows (`count_csv_rows.py`), and handling pagination/debugging issues (`debug_pagination.py`, `test_pagination_bug.py`). Outputs include processed datasets, debug logs, or estimates (e.g., via `paint_estimator.py`). The flow is script-driven, orchestrated manually or via Docker (`Dockerfile`) for deployment on platforms like Fly.io (`fly.toml`).

No embedded diagrams are currently available; refer to `README.md` for setup instructions.

## Internal Movement
The system is composed of standalone Python scripts that collaborate through file I/O, shared CSV outputs, and direct function calls rather than formal queues, events, or RPC. For example:

- Ingestion scripts (`ingest_csv.py`, `ingest_api.py`) read from CSV files or API responses and write processed data to intermediate CSVs (e.g., `resumido_200.csv`).
- Analysis modules like `analyze_missing_skus.py` and `search_products.py` load these CSVs or API data via `vtex_client.py` and perform computations, outputting results to console, logs, or new files.
- Debug utilities (`debug_response_structure.py`, `peek_cubo_page.py`, `head_csv.py`) inspect data mid-flow without altering it, aiding troubleshooting.
- No shared database is evident; movement relies on filesystem interactions. The `__pycache__` directory caches compiled Python modules for efficiency across script runs. Deployment via `Dockerfile` encapsulates the environment, ensuring consistent execution.

## External Integrations
- **Cubo API** — Purpose: Fetch product catalog data (e.g., SKUs, descriptions) for ingestion and analysis. Authentication: API key or token-based (inferred from `fetch_cubo_produtos.py` and `peek_cubo_page.py`). Payload shapes: Primarily GET requests to endpoints like `/produtos` with pagination params (e.g., `page=1&limit=100`); responses in JSON with fields like `id`, `sku`, `name`. Retry strategy: Exponential backoff on HTTP 429/5xx errors, with delays starting at 1s up to 60s, implemented in fetching scripts.
- **VTEX API** — Purpose: Search and retrieve product/shipping details for cross-referencing with Cubo data (e.g., via `vtex_client.py` and `vtex_shipping.py`). Authentication: AppKey/AppToken pair for REST API access. Payload shapes: POST/GET to `/api/catalog_system/pub/products/search` with query params (e.g., `{ "query": "sku:123" }`); responses in JSON arrays with `Id`, `Name`, `ShippingEstimates`. Retry strategy: Linear backoff with jitter on rate limits (e.g., 10 req/min), plus circuit breaker for repeated failures; logs errors to stdout.
- **CSV File Sources** — Purpose: Bulk import of product data (e.g., `produtos-cubo.csv`). Authentication: None (local files). Payload shapes: Standard CSV with headers like `sku, name, price`; processed row-by-row in `ingest_csv.py` and `count_csv_rows.py`. Retry strategy: N/A, but includes validation for malformed rows with skip-on-error.

## Observability & Failure Modes
- Metrics, traces, or logs: Scripts use Python's `logging` module (via `requirements.txt` dependencies) for stdout/stderr output, including row counts, API response times, and error stacks. Debug scripts (`debug_pagination.py`, `debug_response_structure.py`) provide ad-hoc tracing. No centralized metrics (e.g., Prometheus) or tracing (e.g., Jaeger) are integrated; monitor via Docker logs on Fly.io.
- Backoff, dead-letter, or compensating actions: API calls implement retries as noted above. On failures (e.g., pagination bugs in `test_pagination_bug.py`), scripts halt and log details; no dead-letter queues, but partial CSV outputs serve as recovery points. Compensating actions include re-running ingestion from checkpoints (e.g., last processed row in CSV).

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Validate flows against the latest integration contracts or diagrams.
2. Update authentication, scopes, or rate limits when they change.
3. Capture recent incidents or lessons learned that influenced reliability.
4. Link to runbooks or dashboards used during triage.

<!-- agent-readonly:sources -->
## Acceptable Sources
- Architecture diagrams, ADRs, integration playbooks.
- API specs, queue/topic definitions, infrastructure code.
- Postmortems or incident reviews impacting data movement.

<!-- agent-update:end -->
