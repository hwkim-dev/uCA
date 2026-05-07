---
orphan: true
---

# Developer reference

Authoritative descriptions of how the PCCX repositories fit together,
what each architectural contract means, and how verification flows
between repos. The reference set is the source of truth for developers
who need exact, current state — not an onboarding guide.

## Pages

- [Repository topology](repo-topology.md) — which repo owns what, how
  the IP-core / board / model split is enforced.
- [v002 contract narrative](v002-contract.md) — every field in
  `compatibility/v002-contract.yaml` and what evidence will fill its
  TBD slots.
- [Boundary rule](boundary-rule.md) — four-way classification (model /
  board / IP-core / spec) plus the naming red flags inside IP-core
  paths.
- [Testing protocol](testing-protocol.md) — Sail typecheck, KV260 sim
  wrapper, fresh-clone reachability check; what evidence each produces
  and where it lives.
- [Submodule pin policy](submodule-pin-policy.md) — why kv260 pins to
  `pccx-v002/main`, the rebase-merge SHA-rewrite lesson, the
  fresh-clone verification step.

## When to update this set

Update this set whenever a repository boundary, contract field,
verification flow, or pin policy actually changes. It is not a place
for proposals or roadmap items — those live under `docs/roadmap/`.
