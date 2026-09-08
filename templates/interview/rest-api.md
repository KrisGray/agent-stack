# Pack: REST API

Compose with: `schema-change` if the endpoints require a change to stored data, and
`auth-permissions` when callers have different levels of access.

Building or changing an HTTP API that something else calls. Assumes the core bank has
run. Ordered by cost-of-missing; drop from the bottom.

1. Are there existing consumers, and must old clients keep working after this ships?
   [default: yes — assume you cannot make them upgrade in step with you]
   - → *if the change is breaking:* who are the clients, and who tells them?

2. How is the API versioned today? [default: unversioned, so changes have to be additive]
   *(An unversioned API with external consumers is a constraint on every requirement
   below it, not a detail. Surface it in the playback.)*

3. For write endpoints — what should happen if a client sends the same request twice?
   [default: a retry must not create a second thing]

4. Is there an existing shape for errors and for authentication that this must match?
   [default: yes, follow the existing convention]
   - → *if this is the first endpoint:* skip and let it fall to design.

5. Are any responses large or open-ended enough to need paging or filtering?
   [default: no — responses are bounded]

## Notes for the PRD

- Q1 plus Q2 decide whether "changing the API" is one deliverable or two — an additive
  change followed by a deprecation is a sequence, and that is a scope finding for the
  playback, not a design to propose.
- A Q3 answer of "don't care" is worth logging as an assumption with a sharp invalidation
  condition: it stops being true the first time a client sits behind a flaky network.
- Consumers named in Q1 that live outside this repo are PRD risks under core Q11.
