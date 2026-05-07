# Workflow Facade

_Page in flux. Refreshed 2026-04-24 to match pccx-lab HEAD._

This page documents the current pccx-lab workflow facade: static helpers
used by the Tauri UI for trace summaries, UVM sequence scaffolds, extension
catalogue data, and SystemVerilog editor integration. The surface is still
pre-stable and should be treated as an implementation boundary until the
pccx-lab v0.3 work settles.

## Static Helpers

Four helpers are callable without constructing a long-lived service object:

| Helper | Purpose |
|---|---|
| `compress_context` | Reduce trace statistics into a concise LLM context string. |
| `generate_uvm_sequence` | Return a SystemVerilog UVM sequence stub for a named mitigation strategy. |
| `list_uvm_strategies` | Enumerate strategy slugs accepted by the UVM sequence generator. |
| `get_available_extensions` | Return the extension catalogue rendered by the Tauri UI. |

Current UVM strategy slugs:

| Slug | Body |
|---|---|
| `l2_prefetch` | Stagger DMA reads by AXI transaction overhead. |
| `barrier_reduction` | Use a wavefront barrier in place of global sync. |
| `dma_double_buffer` | Ping-pong compute and DMA across adjacent tiles. |
| `systolic_pipeline_warmup` | Pre-roll the MAC array before the first real tile. |
| `weight_fifo_preload` | Front-load HP weight FIFOs during the setup window. |

The richer strategy set (`back_pressure_gate`, `kv_cache_thrash_probe`,
`speculative_draft_probe`, and related probes) has not been re-landed. Track
progress in the pccx-lab design notes under `docs/design/phase5_alphaevolve.md`.

## Provider Traits

Two unstable scaffolds sit behind the `plugin-api` feature for future workflow
extensions: a context compressor for trace or document excerpts, and a task
runner for bounded analysis jobs. No concrete implementations ship with
pccx-lab v0.2.x. Downstream consumers should treat the signatures as subject
to change until pccx-lab v0.3.

## pccx-lsp

The LSP facade is where editor routing lives going forward. The current slice
includes `LspMultiplexer`, `NoopBackend`, async bridge helpers, JSON-RPC wire
framing, and SystemVerilog keyword/hover providers. External LSP servers such
as verible, rust-analyzer, and clangd spawn through `SpawnConfig` and
`LspSubprocess`; the remaining pipe codec work lands in a follow-on slice.

`CompletionSource` distinguishes results from an upstream LSP, a fast runtime
predictor, a deeper runtime predictor, or an AST-hash cache so the UI can show
provenance next to each suggestion.

## UI-Facing Commands

Until the full facade lands, the Tauri UI calls directly into static helpers
through `invoke("compress_context", ...)`, `invoke("generate_uvm_sequence", ...)`,
and `invoke("list_uvm_strategies")`. The bridge is a thin command layer in
`ui/src-tauri/src/lib.rs`.

The full Tauri command catalogue lives at [IPC reference](ipc.md), along with
the IPC boundary rules for u64-as-string, `generation_id`, and keeping raw
traces out of IPC payloads.

## Related

- [Analyzer API](analyzer_api.md) - the plugin-registry primitive used by
  per-crate plugin traits.
- [CLI reference](cli.md) - the binaries currently shipping; the old
  `pccx_analyze` umbrella does not exist today.

## Cite This Page

```bibtex
@misc{pccx_lab_workflow_facade_2026,
  title        = {pccx-lab workflow facade and SystemVerilog editor boundary after Phase 1},
  author       = {Kim, Hyunwoo},
  year         = {2026},
  howpublished = {\url{https://pccx.pages.dev/en/docs/Lab/workflow_facade.html}},
  note         = {Part of pccx: \url{https://pccx.pages.dev/}}
}
```

The LSP facade is implemented in
<https://github.com/pccxai/pccx-lab/blob/main/crates/lsp/src/lib.rs>.
