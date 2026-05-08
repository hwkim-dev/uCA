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

- The canonical v003 IP-core planning package is
  [`pccxai/pccx-v003`](https://github.com/pccxai/pccx-v003). It mirrors
  the published `pccx-v002` layout (`LLM/`, `Vision/`, `Voice/`,
  `common/`, `compatibility/`, `docs/`, `tests/`, `scripts/`) and is the
  single predictable location for v003 architecture planning material.
- The earlier temporary feeder
  [`pccxai/pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003)
  is superseded / retired and is no longer an active public track.
  Any reusable v003 LLM material belongs under `pccx-v003/LLM/`.
- The consolidation decision is tracked under
  [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64).
- No v003 RTL, sim wrapper, formal harness, board integration, or
  contract has been published.

## Source-of-truth links

- v002 IP-core package (released): [`pccxai/pccx-v002`](https://github.com/pccxai/pccx-v002)
- v003 IP-core planning package (canonical): [`pccxai/pccx-v003`](https://github.com/pccxai/pccx-v003)
- v003 LLM feeder (historical / retired): [`pccxai/pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003)
- Tracker: [`pccxai/pccx#64`](https://github.com/pccxai/pccx/issues/64)
- Canonical docs: <https://pccx.pages.dev/en/>
