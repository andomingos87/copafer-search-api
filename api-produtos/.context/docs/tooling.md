<!-- agent-update:start:tooling -->
# Tooling & Productivity Guide

Collect the scripts, automation, and editor settings that keep contributors efficient.

## Required Tooling
- Git (version 2.25 or later) — Install via your OS package manager (e.g., `apt install git` on Ubuntu, `brew install git` on macOS) or download from [git-scm.com](https://git-scm.com/). Required for version control, cloning the repository, and managing contributions via GitHub.
- Python (version 3.9 or later) — Download and install from [python.org](https://www.python.org/downloads/) or use a manager like pyenv (`pip install pyenv`). Powers the core scaffolding scripts, AI context generation, and automation tools in the repository.
- pip (included with Python 3.9+) — Upgrade with `python -m pip install --upgrade pip`. Used to install Python dependencies listed in `requirements.txt` or `pyproject.toml`.

## Recommended Automation
- Pre-commit hooks: Install via `pip install pre-commit` and run `pre-commit install` in the repo root. Configured in `.pre-commit-config.yaml` to enforce linting, formatting, and security checks before commits.
- Linting and formatting: Use Black (`pip install black`) for code formatting (`black .`) and Flake8 (`pip install flake8`) for style checks (`flake8 .`). Run these in CI or locally to maintain code quality.
- Scaffolding scripts: Execute `python scripts/scaffold.py` to generate new docs or agents; watch mode available via `python -m watchdog` for auto-reloading during development.
- Testing loop: `pytest` for unit tests (`pip install pytest`); run `pytest -v` for verbose output, or `pytest --watch` for continuous testing during iterations.

## IDE / Editor Setup
- Visual Studio Code (VS Code): Recommended editor; install the official Python extension by Microsoft for IntelliSense, debugging, and linting integration. Add Pylance for enhanced type checking and Jupyter support if working with notebooks.
- Workspace settings: Share `.vscode/settings.json` for consistent formatting (e.g., set `"python.formatting.provider": "black"`) and task runners for common commands like building docs.
- Vim/Neovim users: Install vim-plug and plugins like `vim-python` for syntax highlighting and `ale` for async linting with Flake8/Black.

## Productivity Tips
- Virtual environments: Use `python -m venv .venv` to isolate dependencies, then activate with `source .venv/bin/activate` (Unix) or `.venv\Scripts\activate` (Windows). Mirrors production isolation.
- Terminal aliases: Add to `~/.bashrc` or equivalent: `alias scaffold='python scripts/scaffold.py'`, `alias test='pytest -v'`, `alias lint='black . && flake8 .'`.
- Container workflows: If Docker is available, use the `Dockerfile` in the root for reproducible builds (`docker build -t ai-context .`); run local emulators with `docker-compose up` to simulate CI environments.
- Shared scripts: Check the `scripts/` directory for utility tools like `update-docs.py` for batch documentation refreshes; dotfiles in `.github/workflows/` for CI automation.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Verify commands align with the latest scripts and build tooling.
2. Remove instructions for deprecated tools and add replacements.
3. Highlight automation that saves time during reviews or releases.
4. Cross-link to runbooks or README sections that provide deeper context.

<!-- agent-readonly:sources -->
## Acceptable Sources
- Onboarding docs, internal wikis, and team retrospectives.
- Script directories, package manifests, CI configuration.
- Maintainer recommendations gathered during pairing or code reviews.

<!-- agent-update:end -->
