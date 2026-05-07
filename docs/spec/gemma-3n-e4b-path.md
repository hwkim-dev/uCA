---
orphan: true
---

# Gemma 3N E4B Software Path Overview

This page summarizes the current software path for the Gemma 3N E4B
bring-up lane on KV260. The useful public status is narrow: the launcher
scaffold is in place with mock coverage and typed contracts, while
bitstream evidence, a board run, and real model inference evidence are
still pending.

The release-line performance language remains **20 tok/s target** only.
This page does not present a measured throughput number.

## Current State

The software path is staged in
[`pccxai/pccx-llm-launcher`][launcher-repo]. As of 2026-05-07, the public
evidence is a set of open launcher PRs that define data preparation,
configuration, token I/O, and mock orchestration surfaces. They are
useful because they make the future board path concrete without
claiming that hardware execution has happened.

| Slice | Public evidence | Current interpretation |
| --- | --- | --- |
| Weight preparation | [pccxai/pccx-llm-launcher#84][launcher-84] | Adds caller-supplied BF16-shaped array preparation, grouped `e_max` / BFP power-of-two scaling, signed W4 quantization, packed-byte output, and manifest metadata. |
| Tokenizer | [pccxai/pccx-llm-launcher#87][launcher-87] | Adds an offline tokenizer surface with a local JSON config path and miniature placeholder vocabulary fixture; it does not include real Gemma tokenizer data. |
| Architecture spec | [pccxai/pccx-llm-launcher#89][launcher-89] | Adds a config-only `GemmaArchSpec` loader and validation surface, plus packed-size math for W4 manifest invariants. |
| Token streaming | [pccxai/pccx-llm-launcher#83][launcher-83] | Adds first-pass token streaming over a KV260 serial TTY boundary using marker-wrapped, length-prefixed chunks and mock/no-device coverage. |
| End-to-end orchestration | [pccxai/pccx-llm-launcher#88][launcher-88] | Wires prompt encode, W4 prep, scripted token stream, AXI mock polling, output receive, and decode into a deterministic mock-only path. |

The claim guard for this page follows the project public-wording list in
`manual/06_PUBLIC_WORDING_AND_CLAIMS.md`: target-only performance
wording, no hardware inference claim, no bitstream readiness claim, and
no production readiness claim.

## Data Path

The current software path can be read as five handoffs:

1. **Model-side shape and weight material** enters the launcher as
   caller-supplied arrays and local config files. The W4 preparation
   slice defines the packed representation and manifest fields that the
   later hardware path must consume.
2. **Tokenizer input and output** are represented by an offline tokenizer
   contract. The fixture is intentionally small and synthetic, so it is
   contract coverage rather than a claim about real model assets.
3. **Gemma architecture metadata** is loaded through a config-only spec
   object. That gives the launcher a place to validate dimensions and
   compute packed-size expectations before any board command exists.
4. **Token transport** is framed over serial as marker-wrapped binary
   chunks. The current tests cover framing, timeouts, mock AXI behavior,
   and no-TTY skips; they do not replace a board capture.
5. **The orchestrator** joins those pieces with mock KV260 connection
   surfaces. It can exercise the intended flow end to end in software,
   but the real serial Gemma chat path remains a stub pending board
   evidence.

## What Is Complete

The current scaffold covers:

- W4 quantization contract code and deterministic local tests.
- Tokenizer and architecture-spec contracts with local fixtures.
- Serial token-framing code and mock/no-device test paths.
- A mock end-to-end orchestrator and CLI route for deterministic local
  output.
- Claim-scan-clean PR evidence on the launcher side.

This is enough to make the software boundary reviewable. It is not
enough to publish board execution, real inference, timing, or throughput
claims.

## Gates Still Open

The public gates that remain open are:

- Full bitstream build evidence from the KV260 hardware repository.
- Board programming and smoke-capture evidence.
- Real serial transport evidence against a connected KV260.
- Real Gemma tokenizer and weight asset handoff under the model license
  boundary.
- End-to-end inference evidence with captured logs and reproducible
  commands.
- Any measured throughput statement; only the **20 tok/s target** is
  public at this stage.

Until those gates land, public wording should stay in the scaffold,
mock, contract, pending-evidence, and target vocabulary.

[launcher-repo]: https://github.com/pccxai/pccx-llm-launcher
[launcher-83]: https://github.com/pccxai/pccx-llm-launcher/pull/83
[launcher-84]: https://github.com/pccxai/pccx-llm-launcher/pull/84
[launcher-87]: https://github.com/pccxai/pccx-llm-launcher/pull/87
[launcher-88]: https://github.com/pccxai/pccx-llm-launcher/pull/88
[launcher-89]: https://github.com/pccxai/pccx-llm-launcher/pull/89
