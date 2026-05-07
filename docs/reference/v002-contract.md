---
orphan: true
---

# v002 contract narrative

The v002 IP-core package declares its consumer-facing contract in
`pccx-v002/compatibility/v002-contract.yaml`. This page describes what
each field means and what evidence will fill its TBD slot.

## Fixed fields

These fields are fully specified in the contract yaml today.

| Field | Value | Meaning |
| --- | --- | --- |
| `arch` | `pccx-v002` | Architecture identifier shared by every consumer. |
| `package_repo` | `pccx-v002` | The repository name the package is published under. |
| `domains` | `LLM`, `Vision`, `Voice` | Top-level RTL domain directories inside `pccx-v002/`. Vision and Voice exist as placeholders until the corresponding tracks absorb. |
| `model_specific` | `false` | The IP-core does not encode any specific model identity. |
| `board_specific` | `false` | The IP-core does not encode any specific board identity. |
| `known_application_repos` | `pccx-FPGA-NPU-LLM-kv260` | Application repositories known to consume this package. |

## TBD fields

Each TBD field has a defined slot in the yaml so consumers do not have
to invent the schema later. The values below describe what the field
will hold and what evidence will be required to fill it.

| Field | Will hold | Evidence required |
| --- | --- | --- |
| `isa_version` | Encoded ISA revision (e.g. `0.2.0`) | A frozen ISA revision document under `pccx/docs/v002/ISA/` and a passing Sail typecheck against that revision. |
| `register_abi_version` | Encoded MMIO register ABI revision | A frozen `compatibility/register_map.yaml` plus a passing harness that exercises every documented register. |
| `driver_abi_version` | Encoded driver ABI revision (struct layout, calling convention) | A frozen driver ABI document plus a build of one application repo against that ABI. |
| `top_interface_version` | Encoded top-port revision | A frozen `compatibility/top_interface.yaml` matching the actual ports of the IP-core top module. |
| `weight_format` | Quantized weight format identifier (e.g. `W4`) | A reference packing routine and at least one round-trip golden vector. |
| `activation_format` | Activation format identifier (e.g. `INT8`) | A reference quantization routine and at least one round-trip golden vector. |
| `nonlinear_precision` | Approximation strategy and precision target for the nonlinear path | A protocol document plus reference Python that produces RTL-visible values to compare against. |
| `control_bus` | Identifier for the control transport (e.g. `axi-lite`) | A frozen control bus spec and a working application that drives it. |

## Update rule

A TBD field flips to a real value only when both the schema slot and
the supporting evidence are present in this repository (or a sibling
repo it links to). Avoid promoting a field to a non-TBD value before
the evidence is reproducible — promoting early forces every consumer
to re-pin and re-verify.

## Sources

- `pccx-v002/compatibility/v002-contract.yaml` — the live contract.
- `pccx-v002/compatibility/register_map.yaml`,
  `memory_map.yaml`, `top_interface.yaml` — the supporting files this
  page refers to.
