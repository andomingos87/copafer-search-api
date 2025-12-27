```markdown
---
ai_update_goal: Ensure the testing strategy documentation reflects the current codebase testing setup, including frameworks, commands, thresholds, and known issues, to guide contributors on maintaining code quality.
required_inputs:
  - package.json scripts section
  - CI configuration files (e.g., .github/workflows/)
  - Test configuration files (e.g., jest.config.js, cypress.config.js)
  - Open issues labeled 'testing' or 'flaky-tests'
success_criteria:
  - All placeholder text (e.g., TODOs, agent-fill markers) replaced with specific, actionable details.
  - Commands verified against package.json and CI workflows.
  - Coverage thresholds and quality gates match current requirements.
  - Troubleshooting section includes links to relevant issues or ADRs if applicable.
  - Cross-references to other docs (e.g., [development-setup.md](development-setup.md)) are valid.
---

<!-- agent-update:start:testing-strategy -->
# Testing Strategy

This document outlines how quality is maintained across the codebase through various testing layers, ensuring reliability in both the Python backend (using pytest) and JavaScript frontend (using Jest and Cypress). Tests are integral to the development workflow, with automation via GitHub Actions in CI/CD pipelines.

## Test Types

- **Unit**: Focus on individual functions, classes, or modules in isolation. For the Python backend, use pytest with fixtures for mocking dependencies; test files follow the convention `test_*.py` in a `tests/` directory (e.g., `tests/test_utils.py`). For the JavaScript frontend, Jest is the primary framework, with tests colocated as `*.test.js` or `*.spec.js` alongside source files (e.g., `src/components/Button.test.js`). Coverage targets isolated logic without external I/O.

- **Integration**: Test interactions between modules or services, such as API endpoints calling database layers or frontend components integrating with backend APIs. Scenarios include validating data flow in FastAPI routes (Python) with pytest and httpx for HTTP mocking, or React component integration with Redux stores using Jest and React Testing Library. Tooling includes Docker for spinning up test databases (e.g., PostgreSQL via `docker-compose.test.yml`) and environment variables like `TEST_DB_URL`.

- **End-to-End**: Simulate full user workflows across the application stack. Use Cypress for browser-based E2E tests on the frontend, targeting scenarios like user authentication flows or form submissions that interact with the live backend. Tests run in a dedicated CI environment with headless Chrome; harnesses include a test server setup via `npm run start:test` and `pytest` for backend validation. No dedicated E2E for pure backend at this time, but API contracts are verified via integration tests.

Additional categories include:
- **Smoke Tests**: Quick sanity checks post-deployment, run via `npm run test:smoke` in CI.
- **Accessibility Tests**: Integrated into E2E with Cypress-axe plugin for WCAG compliance.

## Running Tests

- Execute all tests (unit, integration) with `npm run test` for frontend (Jest) or `pytest` for backend; use `npm run test:all` to run both via concurrently.
- Use watch mode locally: `npm run test -- --watch` (Jest) or `pytest -vv --tb=short` with plugins like pytest-watch.
- Add coverage runs before releases: `npm run test -- --coverage` (generates reports in `coverage/`) or `pytest --cov=src --cov-report=html` for backend. Thresholds are enforced in CI.

For full suite including E2E: `npm run test:e2e` (starts test server and runs Cypress). Local development setup requires Node.js >=18 and Python >=3.10; see [development-setup.md](development-setup.md) for prerequisites.

## Quality Gates

- **Coverage Expectations**: Minimum 80% line coverage for new code (enforced via Jest's `--coverage --collectCoverageFrom` and pytest-cov); overall project target is 75%. Branch coverage at 70% for critical paths. Reports are uploaded as artifacts in CI and visualized in GitHub Actions.
- **Linting and Formatting**: Pre-merge requirements include ESLint (with Airbnb ruleset, extended for React) via `npm run lint`, Prettier for JS/TS formatting (`npm run format:check`), and Black/Flake8 for Python (`black --check .` and `flake8 src/`). Husky hooks run these on commit/push.
- **CI Checks**: All PRs must pass GitHub Actions workflows (`test.yml` for unit/integration, `e2e.yml` for end-to-end). Security scans (e.g., npm audit, bandit for Python) are also gated. Merges to main require at least one approval and passing status checks.

## Troubleshooting

- **Flaky Suites**: The E2E test `user-login.spec.js` occasionally fails due to race conditions in Cypress network stubs; mitigate by increasing timeouts (`cy.visit({ timeout: 10000 })`) or retrying in CI (configured with `cypress-plugin-retries`). Track in [issue #42](https://github.com/repo/issues/42).
- **Long-Running Tests**: Backend integration tests involving database fixtures can take >30s; optimize by using in-memory SQLite for local runs (`export TEST_DB_URL=sqlite:///:memory:`) or parallelize with pytest-xdist (`pytest -n auto`).
- **Environment Quirks**: On Windows, Python path issues may arise with pytest; use WSL or virtualenv. Jest snapshots fail if line endings differ—run `npm run format` before updating. For CI failures, check logs for OOM errors in large E2E suites and scale runners if needed.
- **Common Errors**: "Module not found" in Jest often due to missing `moduleNameMapper` in config; refer to `jest.config.js`. If coverage reports are incomplete, ensure `collectCoverageFrom` excludes `node_modules/` and tests.

For ongoing issues, monitor labels like "flaky-tests" in the issue tracker and contribute fixes via PRs.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Review test scripts and CI workflows to confirm command accuracy.
2. Update Quality Gates with current thresholds (coverage %, lint rules, required checks).
3. Document new test categories or suites introduced since the last update.
4. Record known flaky areas and link to open issues for visibility.
5. Confirm troubleshooting steps remain valid with current tooling.

<!-- agent-readonly:sources -->
## Acceptable Sources
- `package.json` scripts and testing configuration files.
- CI job definitions (GitHub Actions, CircleCI, etc.).
- Issue tracker items labelled “testing” or “flaky” with maintainer confirmation.

<!-- agent-update:end -->
```
