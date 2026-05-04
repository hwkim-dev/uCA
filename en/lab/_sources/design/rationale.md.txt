# Design Rationale

## Why pccx-lab is one repo, not five

In the initial design, we considered a 5-repo structure (simulator / frontend / uvm-bridge / ai / common). However, this was rejected for the following reasons:

1. **Development Speed**: The overhead of synchronizing changes and managing versions across multiple repositories is massive.
2. **Single Purpose**: All modules ultimately work closely together towards the single goal of "pccx profiling".

## Module Boundary Rules

To prevent the downside of a monorepo (spaghetti code), we enforce strict module boundaries.  Phase 1 split the original monolithic `core/` into nine focused crates under `crates/` plus a top-level `ui/`; dependency edges are unidirectional and `pccx-core` is the single sink of the workspace graph (see `docs/design/phase1_crate_split.md` § 3 for the full diagram).

- `pccx-core` (`crates/core/`): pure Rust core — .pccx format, trace parsing, hardware model, roofline, bottleneck detection, VCD / chrome-trace writers, step-snapshot IPC, Vivado timing ingest.  Depends on no other workspace crate.  Strictly forbids importing UI frameworks.
- `pccx-reports` (`crates/reports/`): Markdown / HTML / PDF report rendering.  Depends on `pccx-core`.
- `pccx-verification` (`crates/verification/`): golden-diff + robust reader gates used by CI and pccx-ide.  Depends on `pccx-core`.
- `pccx-authoring` (`crates/authoring/`): ISA and API TOML compilers.  Depends on `pccx-core`.
- `pccx-evolve` (`crates/evolve/`): speculative-decoding primitives for EAGLE-family strategies; future home of the Phase 5 DSE + surrogate + PRM loop.  Depends on `pccx-core` and `pccx-verification`.
- `pccx-lsp` (`crates/lsp/`): Phase 2 IntelliSense façade — sync and async provider traits, multiplexers, `NoopBackend`, `BlockingBridge`, `LspSubprocess`.  Depends on `pccx-core`.
- `pccx-remote` (`crates/remote/`): Phase 3 backend-daemon scaffold (WireGuard / OIDC / RBAC land later).  Depends on `pccx-core`.
- `pccx-uvm-bridge` (`crates/uvm_bridge/`): DPI-C / FFI boundary between SystemVerilog/UVM and `pccx-core`.  Depends on `pccx-core`.
- `pccx-workflow-facade` (`crates/workflow_facade/`): workflow facade support.  Depends only on `pccx-core`'s trace surface (JSON or typed).
- `pccx-ide` (`ui/src-tauri/`): Tauri shell that consumes `pccx-core`, `pccx-reports`, and `pccx-workflow-facade`.
- `ui/` (non-Cargo): React + Vite frontend; reads from `pccx-ide` over Tauri IPC only.

No crate depends on `pccx-ide` or `pccx-remote` — both are terminal binaries.  The React tree is not a Cargo member; it is outside the workspace graph by design.

## Conditions for Future Separation

If a specific crate (e.g. `pccx-core` or `pccx-verification`) becomes generic enough to be used independently outside pccx-lab, we will publish it to crates.io or extract it into its own repository.  The Phase 1 split was done with this in mind: every non-core crate already exposes an unstable trait surface (`ReportFormat`, `VerificationGate`, `IsaCompiler`, `ApiCompiler`, `CompletionProvider`, etc.), so "carve out" is a follow-on release task rather than an architectural refactor.
