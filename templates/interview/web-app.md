# Pack: web app

Compose with: `auth-permissions` for roles and data isolation, and `schema-change` for
apps backed by a database whose shape changes.

Authenticated, multi-user web application — Angular front-end, NestJS back-end, shared
state via NgRx or similar.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. Who uses the app and what main roles exist — admin, normal users, read-only, etc.?
   [default: a small set of roles with clear boundaries]

2. What are the core user journeys — list two or three flows that must work end-to-end?
   [default: one primary journey and one secondary]

3. How is authentication and session management handled today — OAuth/OIDC, JWT,
   custom? [default: existing corporate standard or whatever the repo already uses]

4. What expectations exist around responsiveness — real-time updates, offline support,
   mobile behaviour? [default: reasonably responsive SPA; no offline]

5. How is front-end state managed — NgRx or similar, local storage, server-side state?
   [default: NgRx with server as source of truth]

## Notes for the PRD

- Q1 and Q2 answers become the backbone of the scope list; missing or vague roles and
  journeys are why apps become platforms unexpectedly.
- Q3 answers must be cross-checked against any auth requirements from `auth-permissions`;
  treat mismatches as risks, not trivia.
- Front-end state handling named in Q5 should be reflected in non-functional requirements:
  performance, caching, and consistency.
