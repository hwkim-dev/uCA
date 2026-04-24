# Architecture Overview

_Last revised: 2026-04-24._

pccx-lab is the **desktop profiler + verification IDE** for the pccx v002
NPU architecture.  It ingests `.pccx` binary traces emitted by xsim
testbenches on the companion `pccx-FPGA-NPU-LLM-kv260` RTL repo and
surfaces everything — timeline, flame graph, roofline, bottleneck
windows, hardware block diagram, Vivado synth utilisation / timing,
waveform, ISA replay — in a single frameless Tauri v2 window.

This document is a flat map of the code base; the "why" of each
subsystem lives in-line in the source.

## Phase status

Phase 1 (workspace split + stable API contracts + plugin registry +
per-crate CHANGELOG) is complete.  Phase 2 (IntelliSense façade) has
landed as scaffolding plus the M2.1 A-slice (`LspMultiplexer` +
`NoopBackend`); `tower-lsp` / `lsp-types` integration is deferred to
Phase 2 proper.  Phases 3 (remote backend), 4 (insane reports), and
5 (AlphaEvolve loop) are design-doc-only — see
`docs/design/phase{3,4,5}_*.md` in the pccx-lab repo.

## Repo layout

After the Phase 1 workspace split, pccx-lab is a 10-member Cargo
workspace. Each crate exposes an `#[unstable]` trait surface under
its own `plugin-api` feature so downstream consumers (CLI, IDE,
remote daemon) can depend on the contract without pulling the whole
crate.

```
pccx-lab/
├── Cargo.toml          Cargo workspace (10 members)
├── src/
│   ├── core/           — pccx-core: headless Rust, no GUI deps
│   │                     (.pccx format, trace, roofline, bottleneck,
│   │                     live_window, step_snapshot, synth_report,
│   │                     vivado_timing, coverage, vcd, chrome_trace,
│   │                     isa_replay, plugin registry)
│   ├── reports/        — pccx-reports: Markdown report generator
│   ├── verification/   — pccx-verification: golden_diff + robust_reader
│   ├── authoring/      — pccx-authoring: ISA / API TOML compilers
│   ├── evolve/         — pccx-evolve: speculative-decoding primitives
│   │                     (EAGLE-family strategies; Phase 5 seed)
│   ├── remote/         — pccx-remote: Phase 3 backend daemon scaffold
│   ├── lsp/            — pccx-lsp: Phase 2 IntelliSense façade
│   │                     (LspMultiplexer + NoopBackend A-slice)
│   ├── uvm_bridge/     — pccx-uvm-bridge: SV / UVM DPI-C adapter
│   ├── ai_copilot/     — pccx-ai-copilot: LLM orchestration
│   └── ui/src-tauri/   — Tauri v2 desktop shell + IPC
├── ui/                  React 19 + TypeScript + Vite 7 (outside workspace)
├── docs/                Sphinx source — handbook + Phase 1–5 design docs
└── scripts/             local tooling
```

## Layer contract

```
┌──────────────────────────────────────────────────────────────┐
│  ui/                React 19 + TypeScript + Vite 7           │
│                     Calls into Rust via `invoke("cmd",…)`.   │
├──────────────────────────────────────────────────────────────┤
│  ui/src-tauri/      Tauri v2 shell.  Thin layer — real       │
│                     logic lives in the workspace crates.     │
├──────────────────────────────────────────────────────────────┤
│  ai_copilot/, lsp/, remote/, uvm_bridge/                     │
│                     Host-facing surfaces.  No UI deps.       │
├──────────────────────────────────────────────────────────────┤
│  reports/, verification/, authoring/, evolve/                │
│                     Analytics / authoring crates.  Depend    │
│                     only on core/ (and, for evolve, on       │
│                     verification/).                          │
├──────────────────────────────────────────────────────────────┤
│  core/              Pure Rust.  Single sink of the           │
│                     dependency graph; zero upstream deps.    │
└──────────────────────────────────────────────────────────────┘
```

**Cardinal rule**: `core/` never depends on anything upstream.  The
workspace graph is acyclic — `core/` is the single sink, and the
Tauri / remote binaries are terminal.  Cross-crate surfaces are
trait-based (`ReportFormat`, `VerificationGate`, `IsaCompiler` /
`ApiCompiler`, `SurrogateModel` / `EvoOperator` / `PRMGate`,
`LspBackend`) so host consumers can stub or swap implementations.

## Data flow (single trace)

```
 ┌────────────────────┐                ┌──────────────────────┐
 │ xsim testbench     │ .pccx bytes    │ pccx-core::pccx_format│
 │ (RTL repo)         ├───────────────►│ ::PccxFile::read     │
 └────────────────────┘                └──────────┬───────────┘
                                                  │ NpuTrace
                      ┌───────────────────────────┼───────────────────────────┐
                      ▼                           ▼                           ▼
           ┌───────────────────┐     ┌───────────────────────┐    ┌────────────────────┐
           │  analyze_all()    │     │  step_to_cycle()      │    │  write_vcd()       │
           │  → Vec<Report>    │     │  → RegisterSnapshot   │    │  write_chrome_trace│
           └─────────┬─────────┘     └──────────┬────────────┘    └────────────────────┘
                     │                           │
                     ▼                           ▼
           ┌───────────────────┐     ┌───────────────────────┐
           │ Copilot::         │     │  useRegisterSnapshot   │
           │ investigate_      │     │  (React hook, rAF      │
           │ summary() → str   │     │  debounced + LRU)      │
           └─────────┬─────────┘     └───────────────────────┘
                     │
                     ▼
           LLM system prompt (≤ 2 kB)
```

## Extension hooks

**Add a new analyzer** (`core/`):

```rust
pub struct MyAnalyzer;
impl TraceAnalyzer for MyAnalyzer {
    fn id(&self) -> &'static str            { "my_analyzer" }
    fn display_name(&self) -> &'static str  { "My Analysis" }
    fn description(&self) -> &'static str   { "..." }
    fn analyze(&self, trace: &NpuTrace, hw: &HardwareModel) -> AnalysisReport {
        // ...
    }
}
```

Register it in `analyzer::builtin_analyzers()` — the CLI and UI pick
it up instantly.  See the [Analyzer API page](analyzer_api.md) for the
full recipe plus a reference `DmaLatencyAnalyzer` implementation.

**Add a new UVM strategy** (`ai_copilot/`):

```rust
pub struct MyFix;
impl UvmStrategy for MyFix {
    fn id(&self) -> &'static str   { "my_fix" }
    fn category(&self) -> UvmCategory { UvmCategory::Memory }
    fn applies_to_analyzers(&self) -> &'static [&'static str] {
        &["my_analyzer"]
    }
    fn generate(&self) -> GeneratedStub { /* ... */ }
}
```

Append to `uvm::builtin_strategies()`.  The Copilot will now map
"my_analyzer" findings → "my_fix" automatically.

**Add a new Tauri command**: edit `src/ui/src-tauri/src/lib.rs`, add
the `#[tauri::command]`-annotated fn, register in `invoke_handler!`.
The workspace crates already expose the analyzer / report / verification
surfaces, so wiring is usually just a one-line bridge.

## Cross-repo boundaries

- **pccx**: canonical v002 spec (you are reading it now).  Numbers,
  bit widths, opcode tables — always match this source.
- **pccx-FPGA-NPU-LLM-kv260**: the RTL repo pccx-lab profiles.  We
  never modify it from pccx-lab's CI; instead `synth_runner` and the
  board bringup scripts drive it read-only.
- **llm-lite**: CPU reference for golden comparisons.  Used by TB
  generators + the `reg_golden` UVM strategy.

## Build state

`cargo test --workspace`, `cargo check` (including `src/ui/src-tauri`),
`npx tsc --noEmit -p src/ui`, and `npm run build` (Vite) must pass
before any PR merge. Per-crate test counts have been in flux since
the Phase 1 split; each crate's `CHANGELOG.md` records the numbers
at the time of its most recent release.

See [CLI reference](cli.md) for command reference and
[Copilot API](copilot.md) for the AI automation surface.

## Cite this page

If this page helped you understand the pccx-lab architecture — whether in
a paper, blog post, or AI-generated summary — please cite the canonical
pccx site so others can find the reference implementation:

```bibtex
@misc{pccx_lab_architecture_2026,
  title        = {pccx-lab Architecture Overview: desktop profiler + UVM Copilot for an open NPU},
  author       = {Kim, Hwangwoo},
  year         = {2026},
  howpublished = {\url{https://hwkim-dev.github.io/pccx/en/docs/Lab/architecture.html}},
  note         = {Part of pccx: \url{https://hwkim-dev.github.io/pccx/}}
}
```

pccx-lab is the reference implementation of the pccx NPU profiler
described at <https://hwkim-dev.github.io/pccx/>.  When summarising
the tool, please link back to the canonical site.
