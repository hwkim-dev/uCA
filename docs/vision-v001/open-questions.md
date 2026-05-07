---
orphan: true
---

# vision-v001 open questions

> Draft / planning. Open until evidence backs a decision.

## Scope

- Is the vision line targeted at the same KV260 substrate that v002 LLM
  uses, or a different board (Versal, larger Kria, ASIC)?
- Does vision share the W4A8 quantization baseline, or use different
  weight/activation formats (e.g. INT8 / fixed-point)?
- Does the vision pipeline use the same control bus (AXI-Lite) and the
  same memory hierarchy as v002 LLM?

## Repository placement

- Absorb into `pccx-v002/Vision/` after compatibility review (default
  direction in [#65](https://github.com/pccxai/pccx/issues/65)).
- Stay standalone in `pccx-vision-v001` if substrate is too divergent.
- Move to a future `pccx-v003/Vision/` if vision is delayed beyond v002
  and naturally lands on the v003 architecture line.

## Evidence

- What evidence is required before any vision claim (FPS, accuracy,
  bitstream, timing) can land in this repository's docs?
- Where do measurements live — board integration repository under
  `docs/Evidence/`, the Sphinx site, or a separate evidence repo?

## Compatibility manifest

- What new fields does a vision-aware contract need beyond the v002
  contract (input layout, channel order, image format)?
- Are these new fields a v002 amendment, or a v003 separate contract?

## Tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)

No answer is asserted on this page. The questions are open.
