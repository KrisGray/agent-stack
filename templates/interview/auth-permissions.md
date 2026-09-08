# Pack: auth permissions

Compose with: `web-app`, `rest-api`, `agent-framework` or `analytics-dashboard` whenever
roles, permissions or tenant boundaries matter.

**Usually the second pack, rarely the first** — a project is seldom only about
permissions. That is a note about position, not a restriction; see the composition rules
in `interview.md`.

Roles, permissions, and data isolation — who can do what, and to whose data.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. What roles exist today or are expected — list their names and high-level powers.
   [default: basic user/admin split]

2. How is data partitioned — single-tenant, multi-tenant with strong isolation, or
   shared with row-level permissions? [default: single-tenant]

3. What audit or compliance requirements exist — who needs to know what happened and
   when? [default: basic logs; no formal audits]

4. Are there operations that must be restricted tightly — deletes, exports, financial
   actions? [default: none beyond common-sense restrictions]

## Notes for the PRD

- Q2 answers where isolation is weak or shared must be treated as explicit risk; they
  affect schema design, query shape and caching.
- Any strong audit requirement in Q3 implies additional scope: logging, retention, and
  access to logs.
- Operations named in Q4 should become explicit permissions, not implied behaviour.
