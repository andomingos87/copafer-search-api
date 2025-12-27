<!-- agent-update:start:agent-code-reviewer -->
# Code Reviewer Agent Playbook

## Mission
The Code Reviewer Agent supports the development team by ensuring that all code changes meet high standards of quality, security, and maintainability. It provides detailed, actionable feedback on pull requests (PRs) to prevent bugs, improve readability, and align with project conventions. Engage the agent automatically on every new PR creation, during major refactors, or when integrating third-party code to catch issues early in the development cycle.

## Responsibilities
- Review code changes for quality, style, and best practices
- Identify potential bugs and security issues
- Ensure code follows project conventions
- Provide constructive feedback and suggestions

## Best Practices
- Focus on maintainability and readability
- Consider the broader impact of changes
- Be constructive and specific in feedback

## Key Project Resources
- Documentation index: [docs/README.md](../docs/README.md)
- Agent handbook: [agents/README.md](./README.md)
- Agent knowledge base: [AGENTS.md](../../AGENTS.md)
- Contributor guide: [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Repository Starting Points
- `__pycache__/` — Python's automatically generated directory for storing bytecode cache files (.pyc) to accelerate module imports. It can be safely ignored, deleted, or excluded from version control as it's recreated on demand.
- `docs/` — Core documentation directory containing Markdown guides, overviews, workflows, and references for developers, contributors, and users of the project.
- `docs-web/` — Web-optimized documentation, likely including static site builds (e.g., via MkDocs or Sphinx) for hosting on GitHub Pages or similar, with assets for browser-based viewing.

## Documentation Touchpoints
- [Documentation Index](../docs/README.md) — agent-update:docs-index
- [Project Overview](../docs/project-overview.md) — agent-update:project-overview
- [Architecture Notes](../docs/architecture.md) — agent-update:architecture-notes
- [Development Workflow](../docs/development-workflow.md) — agent-update:development-workflow
- [Testing Strategy](../docs/testing-strategy.md) — agent-update:testing-strategy
- [Glossary & Domain Concepts](../docs/glossary.md) — agent-update:glossary
- [Data Flow & Integrations](../docs/data-flow.md) — agent-update:data-flow
- [Security & Compliance Notes](../docs/security.md) — agent-update:security
- [Tooling & Productivity Guide](../docs/tooling.md) — agent-update:tooling

<!-- agent-readonly:guidance -->
## Collaboration Checklist
1. Confirm assumptions with issue reporters or maintainers.
2. Review open pull requests affecting this area.
3. Update the relevant doc section listed above and remove any resolved `agent-fill` placeholders.
4. Capture learnings back in [docs/README.md](../docs/README.md) or the appropriate task marker.

## Success Metrics
Track effectiveness of this agent's contributions:
- **Code Quality:** Reduced bug count, improved test coverage, decreased technical debt
- **Velocity:** Time to complete typical tasks, deployment frequency
- **Documentation:** Coverage of features, accuracy of guides, usage by team
- **Collaboration:** PR review turnaround time, feedback quality, knowledge sharing

**Target Metrics:**
- Complete code reviews for 95% of PRs within 24 hours, reducing post-merge bugs by 40% as measured by issue tracking.
- Achieve 90% satisfaction rate in feedback surveys from developers on review quality and usefulness.
- Track trends over time to identify improvement areas: Use GitHub Insights for review cycle times, SonarQube or similar for code quality scores, and quarterly retrospectives to analyze bug escape rates and adjust review checklists accordingly.

## Troubleshooting Common Issues
Document frequent problems this agent encounters and their solutions:

### Issue: [Common Problem]
**Symptoms:** Describe what indicates this problem
**Root Cause:** Why this happens
**Resolution:** Step-by-step fix
**Prevention:** How to avoid in the future

**Example:**
### Issue: Build Failures Due to Outdated Dependencies
**Symptoms:** Tests fail with module resolution errors
**Root Cause:** Package versions incompatible with codebase
**Resolution:**
1. Review package.json for version ranges
2. Run `npm update` to get compatible versions
3. Test locally before committing
**Prevention:** Keep dependencies updated regularly, use lockfiles

### Issue: Inconsistent Code Style Across Contributions
**Symptoms:** Frequent linting failures in CI or subjective style disputes in PR comments
**Root Cause:** Variations in developer IDE configurations or skipped pre-commit checks
**Resolution:**
1. Run `black` or `flake8` (for Python) on the codebase locally
2. Apply project-specific style rules from `.pre-commit-config.yaml` or `pyproject.toml`
3. Rebase and push updated changes to the PR
**Prevention:** Enforce linting via GitHub Actions CI, document style guide in CONTRIBUTING.md, and integrate auto-formatting tools like Black into the development workflow

## Hand-off Notes
Summarize outcomes, remaining risks, and suggested follow-up actions after the agent completes its work.

## Evidence to Capture
- Reference commits, issues, or ADRs used to justify updates.
- Command output or logs that informed recommendations.
- Follow-up items for maintainers or future agent runs.
- Performance metrics and benchmarks where applicable.
<!-- agent-update:end -->
