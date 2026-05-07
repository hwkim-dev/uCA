---
orphan: true
---

# vision-v001 compatibility review (template)

> Draft / planning. No vision RTL exists today; this page is a checklist
> for the future review, not a record of completed findings.

## Purpose

Before the vision line is absorbed into `pccx-v002/Vision/` or held
standalone, the project will run a structured review against the
published v002 contract. This page records the review template.

## Review axes

| Axis | What is checked | v002 reference |
| --- | --- | --- |
| Common RTL substrate | Are vision-side packages, interfaces, and wrappers compatible with `pccx-v002/common/rtl/`? Any redefinition? | `pccx-v002/common/rtl/{packages, interfaces, wrappers}/` |
| ISA | Does vision require new opcodes or different operand encodings? | `pccx-v002/LLM/rtl/packages/isa/` |
| Register ABI | Does vision share the LLM register layout, or does it need a separate map? | `pccx-v002/compatibility/register_map.yaml` |
| Memory map | Vision-side L1/L2/HP traffic — does it fit the v002 memory layout? | `pccx-v002/compatibility/memory_map.yaml` |
| Control bus | AXI-Lite shape unchanged? | `pccx-v002/compatibility/top_interface.yaml` |
| Quantization / precision | W4A8 shared? Different vision precision (e.g. INT8 only)? | `pccx-v002/LLM/rtl/core/preprocess/` |
| Driver ABI | Same driver shape, or vision-specific runtime? | `pccx-v002/compatibility/v002-contract.yaml` (`driver_abi_version`) |
| Verification | Can the v002 sim wrapper extend to vision testbenches? | `pccx-v002/LLM/sim/run_verification.sh` |
| Boundary tokens | No model / board names inside vision IP-core paths. | `pccx-v002/scripts/check_repo_boundary.sh` |

## Required artefacts (when review runs)

- Inventory of `pccx-vision-v001` files (RTL, tests, docs, scripts)
  with classification (IP-core / spec / model-specific).
- Diff vs `pccx-v002/common/rtl/` to flag overlapping modules.
- Sail / formal harness compatibility note.
- A **single decision** record: absorb / hold standalone / fork to
  `pccx-vision-v003`.

## What this page is *not*

- It is **not** a record of the finished review.
- It does **not** claim compatibility either way.
- It does **not** measure FPS, mAP, throughput, or latency.

## Tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
