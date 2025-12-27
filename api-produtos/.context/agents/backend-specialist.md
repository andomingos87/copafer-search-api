<!-- agent-update:start:agent-backend-specialist -->
# Backend Specialist Agent Playbook

## Mission
The Backend Specialist agent supports the team by handling server-side development, ensuring robust, scalable, and secure backend systems. Engage this agent for tasks involving API design, database management, authentication implementation, deployment, and performance optimization, particularly in Python-based environments with potential integrations to web technologies.

## Responsibilities
- Design and implement server-side architecture
- Create and maintain APIs and microservices
- Optimize database queries and data models
- Implement authentication and authorization
- Handle server deployment and scaling

## Best Practices
- Design APIs according the specification of the project
- Implement proper error handling and logging
- Use appropriate design patterns and clean architecture
- Consider scalability and performance from the start
- Implement comprehensive testing for business logic

## Key Project Resources
- Documentation index: [docs/README.md](../docs/README.md)
- Agent handbook: [agents/README.md](./README.md)
- Agent knowledge base: [AGENTS.md](../../AGENTS.md)
- Contributor guide: [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Repository Starting Points
- `__pycache__/` — Python bytecode cache directory, automatically generated when Python modules are imported and compiled. It contains temporary files for faster execution and should be excluded from version control (e.g., via .gitignore) to avoid unnecessary commits.
- `docs/` — Core documentation directory containing Markdown files for project guides, architecture overviews, workflows, testing strategies, and other resources to onboard contributors and maintain knowledge.
- `docs-web/` — Web-specific documentation subdirectory, likely holding guides for frontend integration, web deployment, API client usage, or browser-related configurations.

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
- Achieve 90% unit test coverage for backend APIs and reduce average API response time to under 200ms under load.
- Track trends over time using tools like GitHub Actions reports, pytest coverage summaries, or performance benchmarks in CI pipelines to identify and address bottlenecks quarterly.

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

### Issue: Database Connection Timeouts in Development
**Symptoms:** Queries hang or raise connection errors during local testing
**Root Cause:** Misconfigured environment variables or firewall blocking local DB access
**Resolution:**
1. Verify DATABASE_URL in .env file points to a running local instance (e.g., PostgreSQL via Docker)
2. Check if the database service is started: `docker-compose up db`
3. Run `python manage.py migrate` to ensure schema is up to date
4. Test connection with a simple script or tool like psql
**Prevention:** Use Docker Compose for consistent local environments and include DB health checks in CI workflows

## Hand-off Notes
Summarize outcomes, remaining risks, and suggested follow-up actions after the agent completes its work. For example: "Implemented scalable API endpoints with JWT auth; risk of high traffic untested—recommend load testing in next sprint; follow-up: Update deployment docs with new scaling configs."

## Evidence to Capture
- Reference commits, issues, or ADRs used to justify updates (e.g., commit hash abc123 for API optimizations).
- Command output or logs that informed recommendations (e.g., pytest coverage report showing 85% baseline).
- Follow-up items for maintainers or future agent runs (e.g., "Human review needed for prod DB migration plan").
- Performance metrics and benchmarks where applicable (e.g., "API latency reduced from 500ms to 150ms per load test").
<!-- agent-update:end -->
