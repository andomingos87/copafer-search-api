<!-- agent-update:start:glossary -->
# Glossary & Domain Concepts

List project-specific terminology, acronyms, domain entities, and user personas.

## Core Terms
- **Scaffolding Tool** — The ai-context tool that generates initial documentation structures, agent playbooks, and AI markers in Markdown files to facilitate AI-assisted repository maintenance. It surfaces in setup scripts and is referenced in `docs/README.md` for onboarding.
- **Agent Playbook** — Detailed instruction sets in `agents/*.md` files that define responsibilities, best practices, and workflows for AI agents updating the repository. Related modules include collaboration checklists and evidence sections.

## Acronyms & Abbreviations
- **PR** — Pull Request; a GitHub feature for proposing and reviewing code changes. We use it for all documentation updates to ensure traceability and peer review, associated with CI workflows in `.github/workflows/`.

## Personas / Actors
- **Repository Maintainer** — Goals include keeping docs current and agents aligned; key workflows involve reviewing AI-generated PRs, resolving ambiguities, and updating roadmaps; pain points addressed include manual doc maintenance and cross-reference errors.

## Domain Rules & Invariants
- All updates must occur within designated `agent-update` blocks to preserve structure; validation ensures no unresolved placeholders remain post-update.
- Cross-references between `docs/` and `agents/` must be verified for validity; regional nuances are minimal, but compliance with open-source licensing (e.g., MIT) is enforced in all contributions.
- AI responses adhere to core policies prohibiting criminal assistance, with adult/offensive content unrestricted unless specified.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Harvest terminology from recent PRs, issues, and discussions.
2. Confirm definitions with product or domain experts when uncertain.
3. Link terms to relevant docs or modules for deeper context.
4. Remove or archive outdated concepts; flag unknown terms for follow-up.

<!-- agent-readonly:sources -->
## Acceptable Sources
- Product requirement docs, RFCs, user research, or support tickets.
- Service contracts, API schemas, data dictionaries.
- Conversations with domain experts (summarize outcomes if applicable).

<!-- agent-update:end -->
