---
orphan: true
---

# Milestones

Milestone list reflecting actual state. No invented timelines, no
performance targets, no market-sizing claims. Items past the present
moment are marked TBD with the gating evidence the project will need
to advance them.

## Done

- **v002 LLM IP-core extracted** — reusable LLM RTL, common
  packages, testbenches, and the formal Sail harness moved from the
  KV260 board integration repo into a standalone
  `pccxai/pccx-v002` package, consumed by the board integration
  repo through a pinned submodule. Sail typecheck workflow lives
  with the IP-core. Fresh-clone reachability verified.
- **Repository topology and boundary rule documented** — see
  [`docs/reference/repo-topology.md`](../reference/repo-topology.md)
  and
  [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md).
- **v002 contract scaffold published** — see
  [`docs/reference/v002-contract.md`](../reference/v002-contract.md).
  Most fields TBD pending evidence; structure is in place.

## In progress

- **KV260 timing closure on the v002 baseline** — synth has been
  attempted; a full closure pass with reports is the next gate.
- **W4A8 golden-vector gate population** — only smoke vectors
  currently; full fixture set TBD per
  `pccx-FPGA-NPU-LLM-kv260/docs/W4A8_GOLDEN_VECTOR_GATE.md`.
- **v003 IP-core planning** — `pccxai/pccx-v003` is the canonical v003
  IP-core planning package (planning / evidence-gated); the earlier
  feeder `pccxai/pccx-LLM-v003` is superseded / retired and reusable
  v003 LLM material now belongs under `pccx-v003/LLM/`.

## Next (gated, no dates)

- **Vision absorption into `pccx-v002/Vision/`** — gated on
  compatibility review with `pccxai/pccx-vision-v001`. Decision
  default: absorb once the vision RTL is shown to share enough with
  the v002 LLM substrate. If the substrate split is too wide,
  vision stays standalone.
- **`pccx-v003` contract freeze** — gated on the v003 contract being
  stable enough that an external consumer can pin against it. Until
  then `pccx-v003` stays in planning / evidence-gated state.
- **Voice domain population** — `pccx-v002/Voice/` is a placeholder
  directory today. Population is gated on a defined Voice contract.

## Future (no commitments)

- **ASIC / MPW exploration** — out of scope today; tracked as a
  long-term direction. No timeline, no committed silicon path.
- **Multi-board substrate beyond KV260** — depends on the IP-core
  package being exercised on at least one second board. No board
  has been chosen yet.

## What this page is not

- It is **not** a release schedule. No quarter labels, no calendar
  dates.
- It is **not** a marketing roadmap. No customer-facing promises.
- It is **not** a hiring plan. Headcount and team structure live
  outside this repository.
