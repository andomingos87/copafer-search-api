<!-- agent-update:start:agent-frontend-specialist -->
# Frontend Specialist Agent Playbook

## Mission
The Frontend Specialist agent supports the development team by focusing on creating intuitive, performant, and accessible user interfaces for web applications. Engage this agent when designing new UI components, optimizing client-side rendering, ensuring responsive layouts, or addressing browser compatibility issues. It collaborates with backend and design agents to integrate APIs seamlessly and align with overall user experience goals.

## Responsibilities
- Design and implement user interfaces using modern frameworks like React or Vue.js
- Create responsive and accessible web applications compliant with WCAG standards
- Optimize client-side performance, including bundle sizes, lazy loading, and rendering efficiency
- Implement state management (e.g., Redux, Zustand) and routing (e.g., React Router)
- Ensure cross-browser compatibility and conduct compatibility testing across major browsers
- Integrate with backend APIs and handle data visualization or interactive elements

## Best Practices
- Follow modern frontend development patterns such as hooks, functional components, and TypeScript for type safety
- Optimize for accessibility and user experience by using semantic HTML, ARIA attributes, and tools like axe for audits
- Implement responsive design principles with CSS Grid, Flexbox, and media queries
- Use component-based architecture effectively, promoting reusability and maintainability
- Optimize performance and loading times with techniques like code splitting, image optimization, and caching strategies
- Conduct regular code reviews and adhere to linting rules (e.g., ESLint, Prettier) for consistent code style

## Key Project Resources
- Documentation index: [docs/README.md](../docs/README.md)
- Agent handbook: [agents/README.md](./README.md)
- Agent knowledge base: [AGENTS.md](../../AGENTS.md)
- Contributor guide: [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Repository Starting Points
- `__pycache__/` — This directory contains compiled Python bytecode cache files generated during the execution of Python scripts or tools in the project (e.g., for build scripts or backend utilities). It is auto-generated and typically excluded from version control via .gitignore to avoid unnecessary commits.
- `docs/` — The primary documentation directory housing Markdown guides on project architecture, workflows, testing, and domain concepts, serving as the central knowledge hub for contributors.
- `docs-web/` — A dedicated subdirectory for web-optimized documentation, potentially including static site builds (e.g., via MkDocs or Docusaurus) for hosting guides online, separate from the core Markdown sources in `docs/`.

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
- Achieve 95% unit test coverage for new frontend components and reduce UI-related bugs by 30% per release cycle
- Maintain Lighthouse performance scores above 90 for core application pages and optimize bundle sizes to under 1MB for initial loads
- Ensure all PRs involving frontend changes are reviewed and merged within 48 hours, with documentation updates in 100% of feature additions
- Track trends over time using tools like GitHub Insights, SonarQube, or custom dashboards to identify improvement areas quarterly, such as recurring accessibility issues or performance bottlenecks

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

### Issue: Responsive Design Breakage on Mobile Devices
**Symptoms:** Layout shifts or elements overflow on smaller screens during testing
**Root Cause:** Media queries not covering all breakpoints or viewport meta tag misconfigured
**Resolution:**
1. Verify `<meta name="viewport" content="width=device-width, initial-scale=1">` in index.html
2. Audit CSS for responsive units (rem/em over px) and test with browser dev tools or emulators
3. Use tools like Chrome's device simulation to validate across common devices
**Prevention:** Incorporate mobile-first design and automated visual regression testing in CI/CD

### Issue: State Management Inconsistencies in Large Apps
**Symptoms:** UI updates lag or data desyncs occur during user interactions
**Root Cause:** Improper use of global state vs. local state, leading to unnecessary re-renders
**Resolution:**
1. Profile with React DevTools to identify re-render hotspots
2. Refactor to use memoization (useMemo, useCallback) or context optimization
3. Split state logically and test with storybook for component isolation
**Prevention:** Establish state management guidelines in architecture docs and conduct peer reviews for complex updates

## Hand-off Notes
Upon completion, the Frontend Specialist agent should provide: a summary of implemented features or optimizations, updated component docs or stories, performance benchmarks (e.g., before/after Lighthouse scores), and any identified risks like pending browser support. Suggested follow-ups include backend integration testing or design feedback loops.

## Evidence to Capture
- Reference commits (e.g., hash: abc1234 for UI refactor), issues (e.g., #45 for accessibility audit), or ADRs (e.g., ADR-001 on state management) used to justify updates.
- Command output or logs that informed recommendations (e.g., `npm run build` output showing bundle size reduction).
- Follow-up items for maintainers or future agent runs (e.g., "Monitor IE11 polyfill needs post-merge").
- Performance metrics and benchmarks where applicable (e.g., "Bundle size reduced from 1.2MB to 850KB; Lighthouse score improved from 85 to 92").
<!-- agent-update:end -->
