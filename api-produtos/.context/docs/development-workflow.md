<!-- agent-update:start:development-workflow -->
# Development Workflow

Outline the day-to-day engineering process for this repository.

## Branching & Releases
This repository follows a simplified GitHub Flow branching model, emphasizing trunk-based development with short-lived feature branches merged into the `main` branch via pull requests (PRs).

- **Branching**: Develop on `main` for small changes. For features or fixes, create a branch from `main` (e.g., `git checkout -b feature/add-docs-update` or `git checkout -b fix/bug-123`). Keep branches short-lived (<1 week) to minimize merge conflicts.
- **PRs and Merges**: All changes require a PR to `main`. Use squash-and-merge or rebase-and-merge for clean history. Branch protection rules (enforced via repository settings) require passing CI checks and at least one approval before merging.
- **Releases**: Releases are manual or triggered via GitHub Releases. Tag versions semantically (e.g., `git tag v1.2.0` and `git push origin v1.2.0`). Cadence: Patch releases (vX.Y.Z) as needed for fixes; minor/major releases (vX.Y.0 or vX.0.0) aligned with documentation updates or significant scaffolding tool enhancements, approximately bi-monthly based on recent activity. No automated release pipeline is currently configured, but tags are scanned in CI for build artifacts.

## Local Development
The repository is primarily Node.js-based for the ai-context scaffolding tool, with potential Python scripts (inferred from `__pycache__`). Focus on Node.js setup unless specified.

- **Clone and Install Dependencies**: `git clone <repo-url>` followed by `npm install` to set up Node.js dependencies from `package.json`. For Python components (if present), run `pip install -r requirements.txt` in relevant subdirectories.
- **Run the CLI Locally**: Use `npm run dev` for development mode, which starts the scaffolding tool in watch mode. Add flags like `--watch` if supported by the script.
- **Build for Distribution**: `npm run build` compiles the tool for production (outputs to `dist/` or similar). Verify with `npm run lint` and `npm test` beforehand.
- **Additional Notes**: The repository includes `docs` and `docs-web` for documentation; build the web docs with any site generator script if defined (e.g., `npm run docs:build`). Total repo size is ~32 MB with 45 files, so clones are lightweight.

## Code Review Expectations
Pull requests (PRs) are the gateway for contributions, ensuring code quality and alignment with project goals.

- **Review Checklists**: 
  - Does the PR have a clear title, description, and linked issues?
  - Run CI checks (linting, tests) – must pass before approval.
  - Code changes: Follow existing style (e.g., ESLint for JS), add tests for new features, update docs if impacted.
  - Security/Accessibility: Scan for vulnerabilities (e.g., via `npm audit`).
- **Required Approvals**: At least one approval from a maintainer (configured in repo settings). For documentation changes, self-approval is allowed if no code impact.
- Reference [AGENTS.md](../../AGENTS.md) for agent collaboration tips, including how AI agents handle PR reviews and playbook alignments.

## Onboarding Tasks
New contributors should start with low-barrier tasks to familiarize with the codebase.

- **First Issues**: Look for "good first issue" or "help wanted" labels on the GitHub issues page. Current starters include updating placeholder docs or testing local scaffolding runs.
- **Setup Runbook**: After local dev setup (above), run `npm run scaffold --help` to explore the tool. Join the project board at [GitHub Projects](https://github.com/orgs/<org>/projects) for triage (if enabled; otherwise, use the default Issues view).
- **Dashboards and Resources**: Monitor CI status on GitHub Actions tab. For deeper onboarding, review `docs/README.md` for the document map and CONTRIBUTING.md for guidelines. No dedicated Slack/dashboard; use GitHub Discussions for questions.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Confirm branching/release steps with CI configuration and recent tags.
2. Verify local commands against `package.json`; ensure flags and scripts still exist.
3. Capture review requirements (approvers, checks) from contributing docs or repository settings.
4. Refresh onboarding links (boards, dashboards) to their latest URLs.
5. Highlight any manual steps that should become automation follow-ups.

<!-- agent-readonly:sources -->
## Acceptable Sources
- CONTRIBUTING guidelines and `AGENTS.md`.
- Build pipelines, branch protection rules, or release scripts.
- Issue tracker boards used for onboarding or triage.

<!-- agent-update:end -->
