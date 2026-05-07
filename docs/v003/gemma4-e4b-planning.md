---
orphan: true
---

# Gemma 4 E4B planning (v003 target)

> Draft / planning / evidence-gated. No measured performance, no
> bitstream, no timing closure, no runtime claim. PCCX™ v003 is not
> released.

Gemma 4 E4B is the named target for the v003 LLM line. This page records
the planning posture only. It does not assert that any v003 hardware,
runtime, or driver exists today.

## Why Gemma 4 E4B

- The v002 line is anchored to Gemma 3N E4B as its application target
  (board integration: `pccxai/pccx-FPGA-NPU-LLM-kv260`). v003 succeeds
  v002 on the LLM side and is sized for the next-generation Gemma family.
- Gemma 4 E4B is a foundation candidate, not a guaranteed deployment.
- Architectural features potentially exercised by v003 LLM planning:
  spatial decode, Eagle-3 speculative decoding, mixture-of-experts (MoE),
  longer context windows, and updated attention patterns. None of these
  are claimed as implemented today.

## Inputs to planning

- The v002 ISA / register / memory / top-interface contracts (frozen for
  v002). v003 may diverge; divergence will be recorded against the v003
  contract once drafted.
- The v002 Sail formal model (in `pccxai/pccx-v002/LLM/formal/sail/`)
  serves as the structural reference.
- The board substrate question: KV260 vs a different Kria / Versal /
  ASIC target. No board commitment for v003.

## What is *not* claimed

- No measured tokens-per-second on KV260 or any other board for Gemma 4
  E4B.
- No bitstream, no timing-closed implementation.
- No production-ready runtime.
- No ABI stability.
- No driver implementation.
- No accuracy / quality benchmarks.

## Tracker

- [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)
- Compatibility contract scaffold: [`compatibility-contract.md`](compatibility-contract.md)
- Open questions: [`open-questions.md`](open-questions.md)
