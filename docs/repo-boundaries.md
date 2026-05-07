# Repository boundaries

The model and the board consume the IP core. The IP core never references
a specific model name or board name in `rtl/` or `compatibility/`.

## Repository roles

| Repository | Role |
| --- | --- |
| `pccx` | Canonical specification, documentation, and project index. |
| `pccx-v002` | v002 IP-core package for LLM, Vision, Voice, and common reusable sources. |
| `pccx-v003` | Future v003 IP-core package. |
| `pccx-FPGA-NPU-LLM-kv260` | KV260 + LLM application integration; consumes `pccx-v002`. |

## Placement rule

| Content | Owner |
| --- | --- |
| Architecture contracts, register maps, memory maps, and top interfaces | Versioned IP-core package, mirrored here for documentation. |
| Reusable RTL, packages, interfaces, wrappers, testbenches, and formal harnesses | `pccx-v00N` IP-core package. |
| Board constraints, Vivado project files, board top wrappers, and PS/PL wiring | Board integration repository. |
| Model manifests, application runtime code, driver HALs, and board run evidence | Application integration repository. |

## Naming red flags

These names are not allowed inside IP-core `rtl/` or `compatibility/`
paths, except in README files or compatibility documentation that clearly
describes a consumer.

```text
gemma  gemma3n  gemma4  llama  qwen  mistral  e4b
kv260  kria  zcu104  alveo  versal
```
