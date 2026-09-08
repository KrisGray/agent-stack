# Pack: infra change

Compose with: `schema-change` when database shape changes, and `batch-worker` when
jobs or workers are added or altered.

Changes to infrastructure-as-code, environments, or cloud services — Terraform, Docker,
Google Cloud Run, Compute Engine, Cloud SQL, networking.

Assumes the core bank has run. Ordered by cost-of-missing; drop from the bottom.

1. Which environments are affected — dev, staging, production, others — and what is the
   blast radius if something goes wrong? [default: dev and staging only]

2. Is Terraform or another IaC tool already the source of truth, and must that remain
   the case after this change? [default: Terraform is source of truth]

3. What runtime surfaces are involved — Docker images, Cloud Run services, Compute Engine
   instances, Kubernetes clusters? [default: Docker images on Cloud Run]

4. What are the rollback expectations if a deploy breaks — git revert, Terraform state
   manipulation, manual changes? [default: forward-only once data has changed]

5. How are infrastructure health and changes currently observed — logging, metrics,
   alerts, dashboards? [default: basic metrics and logs; limited alerting]

## Notes for the PRD

- Q2 answers where IaC is not the source of truth, or where manual changes are common,
  are risks around drift and reproducibility; surface them clearly.
- Q3 and Q4 together decide how risky a deploy is and how expensive recovery will be;
  they should be reflected in the risk and assumptions sections explicitly.
- Observability named in Q5 becomes part of "done and trusted": infra changes that
  cannot be seen or alerted on are not fully done.
