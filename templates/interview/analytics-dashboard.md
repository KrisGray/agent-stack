# Pack: analytics dashboard

Compose with: `data-pipeline` when the dashboard sits on ingested data, and `schema-change`
when it introduces new tables or aggregates.

Dashboards and reporting interfaces — metrics, charts, filters, drill-downs.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. What are the key metrics or views this dashboard must provide — list the top three?
   [default: a small set of core metrics]

2. How fresh must the data be — real-time, near-real-time, daily, or less frequent?
   [default: daily]

3. Who can see which data — are metrics global, per-user, per-tenant? [default: global]

4. How heavy can queries be — are long-running queries acceptable, and is there a
   performance budget? [default: reasonable performance; no explicit budget]

5. What interactions must exist — filters, drill-downs, exports, alerts? [default:
   basic filters and drill-downs]

## Notes for the PRD

- Freshness in Q2 is a requirement, not a wish; it should be reflected in pipeline and
  storage design.
- Visibility in Q3 must be aligned with `auth-permissions` where loaded; mismatches are
  security risks.
- Heavy queries implied by Q4 should be cross-checked against `schema-change` and infra
  packs to ensure indexes and capacity match.
