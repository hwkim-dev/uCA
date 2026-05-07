---
orphan: true
---

# Repository topology

PCCX is split into a documentation-of-record repo, versioned IP-core
package repos, and per-board application integration repos. The model
and the board both consume the IP-core package; the IP-core never
references a specific model or board name in `rtl/` or
`compatibility/`.

## Active repositories

| Repository | Role |
| --- | --- |
| `pccxai/pccx` | Canonical specification, public documentation site, project index. |
| `pccxai/pccx-v002` | v002 IP-core package — board- and model-agnostic reusable RTL for LLM and shared subsystems. Vision and Voice domains exist as placeholder directories until those tracks absorb their respective repos. |
| `pccxai/pccx-LLM-v003` | Placeholder line for the v003 LLM IP-core. Will fold into a future `pccx-v003/LLM/` once the v003 contract is stable. |
| `pccxai/pccx-vision-v001` | Standalone vision line on the v002 KV260 substrate. Will fold into `pccx-v002/Vision/` after compatibility review. |
| `pccxai/pccx-FPGA-NPU-LLM-kv260` | KV260 + LLM application integration. Consumes `pccx-v002` through `third_party/pccx-v002` submodule pinned at `pccx-v002/main`. |

## Future repositories

| Repository | Role |
| --- | --- |
| `pccxai/pccx-v003` | Future v003 IP-core package — same shape as `pccx-v002` (LLM, Vision, Voice, common). Created when the v003 contract is stable enough to support a separate package boundary. |

## Placement rule

| Content | Repository |
| --- | --- |
| Architecture spec, ISA, register map, memory map, public documentation | `pccx` |
| Reusable RTL, packages, interfaces, wrappers, testbenches, formal harnesses | `pccx-v00N` |
| Board constraints, Vivado project files, board top wrappers, PS/PL wiring | Board integration repo (e.g. `pccx-FPGA-NPU-LLM-kv260`) |
| Model manifests, application runtime code, driver HALs, board run evidence | Application integration repo (same as board integration today) |

## Invariant

> The model and the board consume the IP core. The IP core never
> references a specific model name or board name inside its `rtl/`,
> `compatibility/`, or `formal/` paths.
>
> Application repositories do not own a second copy of IP-core RTL or
> verification flow. They depend on the IP-core package at a pinned
> SHA reachable from that package's `main`.
