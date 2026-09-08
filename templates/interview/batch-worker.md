# Pack: batch worker

Compose with: `data-pipeline` when the worker ingests or transforms data, and
`schema-change` when it writes to tables whose shape is changing.

Background workers, job processors, queue consumers, scheduled jobs — anything that runs
outside request/response flows.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. What triggers the work — a schedule, a queue, an event from another system? [default:
   a schedule]

2. What delivery semantics are required — at-most-once, at-least-once, or best-effort?
   [default: at-least-once; assume retries are allowed]

3. How many workers run and at what concurrency, and can they scale up or down? [default:
   a single worker at fixed concurrency]

4. What happens when work fails — retries, dead-letter queues, manual intervention?
   [default: a small number of retries, then log and drop]

5. How does the worker interact with databases and other services — transactions, locks,
   rate limits? [default: same conventions as the rest of the application]

## Notes for the PRD

- Q2 answers determine whether idempotency is a requirement; an at-least-once system
  without idempotency is a data-integrity risk.
- Q4 answers that mention dead-letter or manual processes imply operational load; record
  who bears it and how often it is acceptable.
- The interaction patterns named in Q5 should be checked against `schema-change` and
  `data-pipeline` findings rather than treated as independent.
