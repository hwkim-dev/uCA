---
orphan: true
---

# Boundary rule

Every artefact in the project belongs in exactly one of four classes.
A new file goes through the decision procedure below before it lands.

## Four-way classification

| Class | Owner repo | Examples |
| --- | --- | --- |
| **Spec / documentation** | `pccx` | Architecture overview, ISA reference, register/memory maps for documentation, project roadmap, public papers. |
| **IP-core (versioned package)** | `pccx-v00N` | Reusable RTL, common packages, interfaces, wrappers, testbenches, formal harnesses, compatibility manifests. |
| **Board integration** | Board integration repo (e.g. `pccx-FPGA-NPU-LLM-kv260`) | Board constraints (`.xdc`), Vivado project files, board-top wrappers, PS/PL wiring, board bring-up runbooks. |
| **Model / application integration** | Application integration repo (today the same repo as board integration; will split when an application repo without a board appears) | Model manifests, runtime drivers, application code, board run evidence. |

## Naming red flags inside IP-core paths

Inside `pccx-v00N/rtl/`, `pccx-v00N/compatibility/`, and
`pccx-v00N/formal/`, the following names are not allowed except in
README files or compatibility documentation that clearly describes a
*consumer*.

```text
gemma  gemma3n  gemma4  llama  qwen  mistral  e4b
kv260  kria  zcu104  alveo  versal
```

The `pccx-v002/scripts/check_repo_boundary.sh` script enforces this on
every push to `pccx-v002`.

## Decision procedure for a new file

1. Does the file describe what the architecture *is* (spec, ISA,
   docs, public roadmap)? → `pccx`.
2. Does the file describe what the architecture *contains*
   (RTL, package, contract field, formal model, testbench)? →
   `pccx-v00N`. Then check the naming red flags before committing.
3. Does the file describe how a specific *board* boots, gets timing
   closure, or wires PS/PL? → board integration repo.
4. Does the file describe how a specific *model* runs, what its
   driver does, or how an application binds to the IP-core? →
   application integration repo.

## Doubtful cases

If a file genuinely fits two classes (e.g. a runbook that documents a
board-specific bring-up but also references an architectural feature),
it lives in the more *concrete* repo (board > application > IP-core
> spec) and links back to the more abstract one. Documentation
duplication across boundaries is the wrong fix; cross-links are the
right one.
