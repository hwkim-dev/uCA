---
orphan: true
---

# PCCX v003 — overview

> Draft / planning / evidence-gated. PCCX™ v003 is an architecture-line plan,
> not a released package. No timing, bitstream, runtime, or accuracy claims.

The v003 line is the next architecture generation after the published v002
IP-core package. Its public scope is **planning and contract drafting** until
verified RTL and a stable contract exist.

## What v003 is intended to cover

- **LLM** — Gemma 4 E4B and other transformer workloads outside the v002
  baseline (e.g. spatial decode, Eagle-3, MoE, larger context windows).
- **Vision / Voice / common** — same domain shape as `pccx-v002`
  (`LLM/`, `Vision/`, `Voice/`, `common/`, `compatibility/`, `docs/`,
  `tests/`, `scripts/`) once the v003 contract is stable.
- **Compatibility contract** — distinct from the v002 contract; consumers
  must pin to a specific v003 SHA when v003 is released.

## Current state (planning only)

- A standalone planning repo exists at
  [`pccxai/pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003) — it is
  a temporary line for v003 LLM planning and Gemma 4 E4B foundation.
- A consolidated `pccx-v003` repository **does not exist yet**. The
  consolidation decision is tracked under
  [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64).
- No v003 RTL, sim wrapper, formal harness, board integration, or
  contract has been published.

## Source-of-truth links

- v002 IP-core package (released): [`pccxai/pccx-v002`](https://github.com/pccxai/pccx-v002)
- v003 LLM planning line: [`pccxai/pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003)
- Tracker: [`pccxai/pccx#64`](https://github.com/pccxai/pccx/issues/64)
- Canonical docs: <https://pccx.pages.dev/en/>
