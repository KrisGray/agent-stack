# Pack: agent framework

Compose with: `auth-permissions` if the agent performs actions on behalf of many users
or across multiple tenants, `infra-change` if deployment or orchestration changes
infrastructure, and `llm-integration` when provider choice or prompt assembly is part of
the work.

Building or changing an AI agent framework — orchestrators that call tools, APIs or
code, manage state, and perform tasks autonomously or semi-autonomously.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. What kinds of tasks must the agent be able to perform — code changes, data queries,
   infrastructure operations, content generation? [default: a narrow set of tasks focused
   on one domain]

2. How does the agent represent and persist state — conversations, task graphs, memory,
   logs? [default: transient in-process state; logs to disk or a simple database]

3. What safety or guardrail rules must the agent follow — what it must never do without
   human approval, and what counts as an error? [default: human in the loop for anything
   destructive or expensive]

4. Through what surfaces is the agent used — CLI, REST API, editor plug-ins, web UI?
   [default: CLI and REST API]

5. How does the agent discover and call tools — static config, dynamic registry, MCP
   servers, or something else? [default: static config checked into the repo]

## Notes for the PRD

- Q3 answers where the agent is allowed to perform destructive or high-cost operations
  without human approval are risk findings, not details. Record them in the assumptions
  table and reflect them in "done and trusted".
- Any external surfaces named in Q4 (IDEs, ticketing systems, CI/CD, cloud consoles)
  are dependencies under core Q11; treat them as such.
- A dynamic or remote tool discovery answer to Q5 implies additional failure modes
  (registry unavailability, stale tool metadata); log them explicitly in the risk
  section rather than treating them as implementation detail.
