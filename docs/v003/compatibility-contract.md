---
orphan: true
---

# v003 compatibility contract (planning)

> Draft / planning / evidence-gated. No frozen v003 contract exists yet.

The v003 contract, when it lands, will mirror the v002 contract shape and
is intended to live at:

```
pccxai/pccx-v003/compatibility/v003-contract.yaml
```

(The package repository `pccxai/pccx-v003` does not exist today. See the
[repository boundary](repository-boundary.md) page for the consolidation
direction.)

## Contract shape (mirrors v002)

```yaml
arch: pccx-v003
package_repo: pccx-v003
domains:
  - LLM
  - Vision
  - Voice
isa_version: TBD
register_abi_version: TBD
driver_abi_version: TBD
top_interface_version: TBD
weight_format: TBD
activation_format: TBD
nonlinear_precision: TBD
control_bus: TBD
model_specific: false
board_specific: false
known_application_repos: []   # populated when board/model integrations consume v003
```

Every field is **TBD** until evidence backs a real value. Fields are
populated only when the supporting evidence is reproducible (frozen
documents, passing harnesses, working integrations).

## Compared with v002

| Field | v002 (released) | v003 (planning) |
| --- | --- | --- |
| ISA | frozen v002 ISA | TBD; may diverge for spatial decode / MoE / longer context |
| Register ABI | frozen v002 register map | TBD |
| Driver ABI | frozen v002 driver ABI | TBD |
| Weight / activation format | W4A8 (v002) | TBD |
| Control bus | AXI-Lite (v002) | TBD |
| Application target | Gemma 3N E4B on KV260 | Gemma 4 E4B (planning) |

The table records *intent and divergence axes* only. None of the v003
column values are claimed as implemented.

## Update rule

A v003 contract field flips from TBD to a real value only when the
supporting evidence is publishable (frozen ISA / spec / harness /
working integration). Promoting fields before the evidence forces every
consumer to re-pin and re-verify.

## Linked

- v002 contract narrative: [`docs/reference/v002-contract.md`](../reference/v002-contract.md)
- v003 tracker: [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)
