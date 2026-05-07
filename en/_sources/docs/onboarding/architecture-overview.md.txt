---
orphan: true
---

# Architecture overview

A short reading order for someone who has never seen the project.
This page only points; authoritative details live elsewhere.

## Reading order

1. **What this project is.** Read the front page of `pccx` (the
   public site root). Skim the topology section.
2. **Where each thing lives.** Read
   [`docs/reference/repo-topology.md`](../reference/repo-topology.md).
3. **What an IP-core package contains.** Read
   [`docs/reference/v002-contract.md`](../reference/v002-contract.md)
   and skim `pccx-v002/SOURCE_MANIFEST.md` in the IP-core repo.
4. **How the boundary is enforced.** Read
   [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md).
5. **How verification works.** Read
   [`docs/reference/testing-protocol.md`](../reference/testing-protocol.md).
6. **How the application repo consumes the IP-core.** Read
   [`docs/reference/submodule-pin-policy.md`](../reference/submodule-pin-policy.md).

## Layers in one paragraph

`pccx` holds the spec and the public site. `pccx-v00N` holds the
versioned IP-core package — reusable RTL, packages, interfaces,
testbenches, formal harnesses, and a contract manifest. A
board integration repo (today `pccx-FPGA-NPU-LLM-kv260`) consumes a
specific `pccx-v00N` at a pinned SHA and adds the board-specific
parts: constraints, Vivado project files, board-top wrappers,
PS/PL wiring, runbooks. Models bind to the application layer through
manifests and runtime code; the IP-core never names a model or a
board inside its `rtl/` paths.

## What this page is not

Detailed architecture diagrams, ISA descriptions, register/memory
maps, and quantization schemes belong on the spec pages
(`docs/v002/`). This page only provides a reading order; do not
rewrite spec details here.
