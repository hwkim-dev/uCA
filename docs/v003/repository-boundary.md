---
orphan: true
---

# v003 repository boundary (planning)

> Draft / planning / evidence-gated. No published v003 RTL.

## Today

- **`pccxai/pccx-v003`** — canonical v003 IP-core planning package.
  Mirrors the `pccx-v002` shape (`LLM/`, `Vision/`, `Voice/`, `common/`,
  `compatibility/`, `docs/`, `tests/`, `scripts/`). Planning /
  evidence-gated; no v003 RTL or contract is released yet.
- **`pccxai/pccx-LLM-v003`** — historical temporary feeder for early
  v003 LLM planning. Superseded / retired; no longer an active public
  track. Reusable material belongs under `pccx-v003/LLM/`.

## Default direction (subject to issue [#64](https://github.com/pccxai/pccx/issues/64))

| Layer | Active location |
| --- | --- |
| LLM RTL / sim / tb / formal | `pccxai/pccx-v003/LLM/...` (mirroring the `pccx-v002` layout) |
| Vision RTL | `pccxai/pccx-v003/Vision/...` once a v003 vision substrate is decided |
| Voice RTL | `pccxai/pccx-v003/Voice/...` once a v003 voice substrate is decided |
| Common packages / interfaces / wrappers | `pccxai/pccx-v003/common/rtl/...` |
| Compatibility contract | `pccxai/pccx-v003/compatibility/v003-contract.yaml` |
| Build scripts, sail harness, tests | `pccxai/pccx-v003/{scripts, formal, tests, docs}/` |

## Boundary rule (unchanged from v002)

The v003 IP-core package follows the same boundary rule as v002:

- The model and the board consume the IP core. The IP core never references
  a specific model name or board name inside its `rtl/`, `compatibility/`,
  or `formal/` paths.
- Application repositories (board / model integrations) consume the
  IP-core package at a pinned SHA reachable from the package's `main`
  branch.
- See the canonical boundary rule under
  [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md).

## Migration sequence (planned)

1. Inventory historical `pccx-LLM-v003` material (now retired) and
   classify each file as IP-core / spec / model-specific before any
   reintroduction under `pccx-v003/LLM/`.
2. Define `compatibility/v003-contract.yaml` placeholders mirroring the
   v002 contract shape inside `pccxai/pccx-v003`.
3. Reintroduce reusable RTL into the `pccx-v003` layout through fresh,
   focused PRs after the v003 contract placeholders are updated.
4. When the package's contract stabilises, pin board/model repos to a
   v003 package SHA reachable from `pccx-v003/main`.

No timing, runtime, FPS/mAP, bitstream, or production-readiness claim is
made by this page.
