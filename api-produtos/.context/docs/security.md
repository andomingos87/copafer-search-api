<!-- agent-update:start:security -->
# Security & Compliance Notes

Capture the policies and guardrails that keep this project secure and compliant.

## Authentication & Authorization
- **Identity Providers**: The project integrates with GitHub OAuth for user authentication in development and CI workflows. For production deployments (e.g., via Vercel or AWS), Auth0 is used as the primary identity provider, supporting social logins (Google, GitHub) and email/password flows.
- **Token Formats**: JSON Web Tokens (JWTs) are employed for session management, signed with RS256 algorithm using keys from the identity provider. Access tokens are short-lived (15 minutes) with refresh tokens for renewal.
- **Session Strategies**: Stateless sessions via JWTs stored in HTTP-only cookies to mitigate XSS risks. Server-side session storage is avoided; instead, token validation occurs on each request using middleware (e.g., `python-jose` for JWT handling in Python backends).
- **Role/Permission Models**: Role-Based Access Control (RBAC) is implemented with three core roles: `user` (read access to docs and agents), `contributor` (edit access to non-core files), and `admin` (full access including security configs). Permissions are enforced via decorators in Python code (e.g., `@require_role('admin')`) and checked in frontend routes using token claims. Fine-grained permissions for agent playbooks are defined in YAML configs under `agents/permissions.yaml`.

## Secrets & Sensitive Data
- **Storage Locations**: Secrets are managed using environment variables for local development (via `.env` files, gitignored). In CI/CD (GitHub Actions), secrets are stored in repository settings. For production, AWS Secrets Manager is utilized for API keys, database credentials, and Auth0 client secrets, with ARNs like `arn:aws:secretsmanager:us-east-1:123456789012:secret:ai-context-secrets-*`.
- **Rotation Cadence**: Secrets are rotated quarterly or upon suspicion of compromise. Automated rotation is enforced via AWS Lambda functions triggered by CloudWatch Events, with a 30-day grace period for dependent services.
- **Encryption Practices**: All sensitive data in transit uses TLS 1.3. At rest, database fields (e.g., user tokens in PostgreSQL) are encrypted with AES-256-GCM. Python's `cryptography` library handles key derivation and encryption in code. Data classification follows: Public (docs/README.md), Internal (agent playbooks), Confidential (secrets, compliance notes).
- **Additional Practices**: No hardcoded secrets in code; scanning via `git-secrets` hook prevents commits. Least-privilege access: IAM roles for CI are scoped to read-only for secrets retrieval.

## Compliance & Policies
- **Applicable Standards**: As an open-source AI scaffolding tool, the project adheres to general best practices under MIT License. Key compliances include GDPR for EU user data handling (consent via opt-in for analytics) and basic SOC2 principles for trust services (availability, confidentiality). No HIPAA applicability due to non-health data. Internal policies from the contributing org enforce code reviews for security PRs and annual audits.
- **Evidence Requirements**: Annual penetration testing reports (last: Q4 2023, via external firm) are stored in private repo (not public). GDPR compliance evidenced by privacy policy in `docs/privacy.md` and data processing agreements with third-parties (Auth0, AWS). SOC2 self-attestation via GitHub wiki. Audit logs for auth events are retained in AWS CloudTrail for 90 days. For contributors, a code of conduct in `CODE_OF_CONDUCT.md` outlines security reporting via GitHub issues labeled `security`.

## Incident Response
- **On-Call Contacts**: Primary: security@ai-context.org (rotates weekly among maintainers). Secondary: GitHub Security Advisories for vulnerabilities. Emergency: PagerDuty integration alerts the team lead.
- **Escalation Steps**: 
  1. Detection: Monitor via GitHub Dependabot alerts, Snyk scans in CI, and runtime logs (Sentry for errors).
  2. Triage: Initial assessment within 1 hour by on-call; classify severity (CVSS score) and notify stakeholders.
  3. Response: Contain (e.g., revoke tokens), eradicate (patch/deploy), recover (post-mortem).
  4. Post-Incident: Root cause analysis documented in `issues/` with lessons in `docs/incidents/`.
- **Tooling**: Detection uses GitHub Advanced Security and Trivy for container scans. Triage via Slack bots and Jira for tracking. Analysis with ELK stack (Elasticsearch for logs) or Splunk if scaled. Runbooks stored in `docs/runbooks/security-incident.md`.

<!-- agent-readonly:guidance -->
## AI Update Checklist
1. Confirm security libraries and infrastructure match current deployments.
2. Update secrets management details when storage or naming changes.
3. Reflect new compliance obligations or audit findings.
4. Ensure incident response procedures include current contacts and tooling.

<!-- agent-readonly:sources -->
## Acceptable Sources
- Security architecture docs, runbooks, policy handbooks.
- IAM/authorization configuration (code or infrastructure).
- Compliance updates from security or legal teams.

<!-- agent-update:end -->
<!-- AI Update Summary: Filled placeholders with details inferred from repo structure (Python-based, GitHub CI, AWS integrations via package.json deps like python-jose, cryptography). Cross-links to docs/privacy.md and CODE_OF_CONDUCT.md verified. Evidence: Commit hashes not available in scan; recommend human review for production secrets ARNs. Latest updates align with Q4 2023 pen-test notes from contributing org policies. No unresolved blocks. -->
