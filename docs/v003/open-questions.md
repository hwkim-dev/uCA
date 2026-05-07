---
orphan: true
---

# v003 open questions

> Draft / planning. Answers below are intentionally TBD until evidence
> backs a real choice.

## Scope

- Should `pccx-v003` cover only LLM, or also Vision / Voice / common from
  day one (mirroring v002)?
- If Vision/Voice are deferred, do they stay in v002 indefinitely, or
  fold into v003 once stable?
- Is the v003 line versioned per architecture refresh
  (e.g. `pccx-v003.0`, `pccx-v003.1`) like v002 was, or as a single
  package?

## Architecture

- Does v003 keep the W4A8 quantization baseline, or move to a different
  weight/activation format?
- Does v003 keep the v002 ISA encoding, or break ABI (and therefore
  require a separate driver / runtime)?
- Spatial decode, Eagle-3 speculative decoding, MoE: which are in scope
  for the first v003 release vs deferred?
- KV-cache strategy at the wider context windows Gemma 4 E4B would
  exercise.

## Board / target

- Does the first v003 board integration stay on KV260, move to a larger
  Kria / Versal target, or go straight to ASIC bring-up planning?
- What evidence is required before the first v003 board integration repo
  is created?

## Repository structure

- When does `pccxai/pccx-v003` get created? Triggered by contract
  freeze, or by first reusable RTL landing?
- When does `pccxai/pccx-LLM-v003` get folded into `pccx-v003/LLM/`?
- Does `pccx-LLM-v003` keep its own README + LICENSE while temporary,
  or pin a "TBD; absorb pending" placeholder?

## Tracker

- [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)

No claim is made about which way these questions resolve. They are open.
