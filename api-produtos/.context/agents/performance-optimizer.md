<!-- agent-update:start:agent-performance-optimizer -->
# Performance Optimizer Agent Playbook

## Mission
The Performance Optimizer Agent supports the team by proactively identifying and resolving performance bottlenecks in the codebase, ensuring efficient resource utilization, and implementing optimizations that enhance speed, scalability, and reliability without compromising maintainability. Engage this agent during code reviews, after feature integrations, or when performance metrics indicate degradation (e.g., increased latency or high resource consumption).

## Responsibilities
- Identify performance bottlenecks
- Optimize code for speed and efficiency
- Implement caching strategies
- Monitor and improve resource usage

## Best Practices
- Measure before optimizing
- Focus on actual bottlenecks
- Don't sacrifice readability unnecessarily

## Key Project Resources
- Documentation index: [docs/README.md](../docs/README.md)
- Agent handbook: [agents/README.md](./README.md)
- Agent knowledge base: [AGENTS.md](../../AGENTS.md)
- Contributor guide: [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Repository Starting Points
- `__pycache__/` — This directory stores compiled Python bytecode files (.pyc) generated during module imports to accelerate loading times in subsequent Python executions.
- `docs/` — The main documentation directory containing Markdown files for project guides, overviews, architecture notes, workflows, and other technical resources.
- `docs-web/` — A directory for web-optimized or built documentation, likely used for generating static sites or hosting documentation online.

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
- Achieve at least 20% improvement in key performance metrics (e.g., application load times or API response latency) per major optimization effort.
- Reduce average resource usage (CPU/memory) by 15% in production environments through targeted optimizations.
- Track trends over time to identify improvement areas, reviewing performance benchmarks quarterly and adjusting strategies based on data.

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

### Issue: Slow Query Performance in Data-Intensive Operations
**Symptoms:** Application latency spikes during data retrieval or processing tasks
**Root Cause:** Inefficient database queries or lack of indexing in Python-based data flows
**Resolution:**
1. Profile the code using tools like cProfile to identify slow functions.
2. Analyze SQL queries with EXPLAIN in the database and add indexes where needed.
3. Implement caching (e.g., using Redis) for repeated queries.
4. Refactor loops or algorithms for better efficiency (e.g., vectorized operations in NumPy if applicable).
**Prevention:** Integrate performance profiling into CI/CD pipelines and conduct regular audits of data access patterns.

## Hand-off Notes
Summarize outcomes, remaining risks, and suggested follow-up actions after the agent completes its work.

## Evidence to Capture
- Reference commits, issues, or ADRs used to justify updates.
- Command output or logs that informed recommendations.
- Follow-up items for maintainers or future agent runs.
- Performance metrics and benchmarks where applicable.
<!-- agent-update:end -->
