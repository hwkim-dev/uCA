---
orphan: true
---

# v003 repository boundary (planning)

> Draft / planning / evidence-gated. No published v003 RTL.

## Today

- **`pccxai/pccx-LLM-v003`** — temporary v003 LLM planning line. Holds
  early architecture notes and Gemma 4 E4B foundation material. The
  repository **is not** a stable v003 IP-core package.
- **`pccxai/pccx-v003`** — does **not** exist yet.

## Default direction (subject to issue [#64](https://github.com/pccxai/pccx/issues/64))

| Layer | Future location |
| --- | --- |
| LLM RTL / sim / tb / formal | `pccxai/pccx-v003/LLM/...` (mirroring the `pccx-v002` layout) |
| Vision RTL | `pccxai/pccx-v003/Vision/...` once a v003 vision substrate is decided |
| Voice RTL | `pccxai/pccx-v003/Voice/...` once a v003 voice substrate is decided |
| Common packages / interfaces / wrappers | `pccxai/pccx-v003/common/rtl/...` |
| Compatibility contract | `pccxai/pccx-v003/compatibility/v003-contract.yaml` |
| Build scripts, sail harness, tests | `pccxai/pccx-v003/{scripts, formal, tests, docs}/` |

## Boundary rule (unchanged from v002)

The v003 IP-core package, when it exists, follows the same boundary rule
as v002:

- The model and the board consume the IP core. The IP core never references
  a specific model name or board name inside its `rtl/`, `compatibility/`,
  or `formal/` paths.
- Application repositories (board / model integrations) consume the
  IP-core package at a pinned SHA reachable from the package's `main`
  branch.
- See the canonical boundary rule under
  [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md).

## Migration sequence (planned)

1. Inventory `pccx-LLM-v003` content and classify each file as
   IP-core / spec / model-specific.
2. Define `compatibility/v003-contract.yaml` placeholders mirroring the
   v002 contract shape.
3. Decide whether to create `pccxai/pccx-v003` immediately or hold the
   temporary `pccx-LLM-v003` until the contract is stable.
4. When the package is created, move reusable RTL into the new layout
   and pin board/model repos to the new package SHA.

No timing, runtime, FPS/mAP, bitstream, or production-readiness claim is
made by this page.
