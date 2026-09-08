# Pack: LLM integration

Compose with: `rest-api` for HTTP-facing services, `web-app` or `website` for UI
frontends, and `data-pipeline` when the integration depends on curated datasets.

Wiring an application or service into an LLM API — prompts, context assembly, response
handling, and provider selection.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. Which providers and models are in scope, and are there preferences or constraints
   around them — cost, latency, licensing, data residency? [default: your current stack
   of models and providers]

2. What prompt structure is expected — system prompts, reusable templates, per-request
   instructions, or free-form user input? [default: a stable system prompt plus
   task-specific templates]

3. What context can or must be provided to the model — database records, files, repo
   content, prior conversations? [default: minimal context: just the current request]

4. How strict must the integration be about latency, throughput and error handling —
   retries, timeouts, fallbacks to other models? [default: best-effort, with basic
   retries on transient errors]

5. How are usage and behaviour monitored — metrics, logs of prompts and responses,
   human review loops? [default: basic logging; manual review only when something breaks]

## Notes for the PRD

- Q1 answers that mention specific providers and models constrain cost, speed and
  capabilities; treat them as fixed decisions rather than background.
- Q3 answers where sensitive data is fed into prompts must be cross-checked against
  core Q12 (sensitivity, retention, licensed data); do not treat this pack as independent
  of that risk.
- Observability named in Q5 should become part of "done and trusted" under core Q10:
  an integration without metrics or logs is not trustworthy even if it functions.
