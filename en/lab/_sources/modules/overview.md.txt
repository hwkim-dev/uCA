# Module Overview

`pccx-lab` is a Tauri 2 desktop app that bundles four strictly-separated
Rust / TypeScript modules into a single verification + profiling IDE
for the **pccx** NPU architecture.

| Module | Language | Depends on | Role |
|--------|----------|------------|------|
| `core/`        | Rust       | —       | `.pccx` format, trace analysis, roofline + bottleneck + synth-report parsers |
| `ui/`          | TypeScript (React + Tauri) | `core/` (via IPC) | shell, visualisations, report dashboard |
| `uvm_bridge/`  | Rust + DPI-C | `core/` | SystemVerilog / UVM ↔ `core/` boundary |
| `ai_copilot/`  | Rust       | `core/` trace types only | LLM + UVM-strategy generator wrappers |

Dependencies flow **inwards only**. `core/` must never import a UI or
framework crate; `ui/` only uses `core/`'s public API via the Tauri
command bridge.

## Shell at a glance

The default layout mirrors a modern EDA IDE (think VTune / Nsight):
a top menu bar, a tool ribbon, a tab strip, the active work panel,
and two dockable side panels (Live Telemetry + AI Copilot).

```{image} /_static/screenshots/timeline-fullwidth.png
:alt: pccx-lab Timeline view — swim lanes of NPU events over cycles
:width: 100%
```

The capture above shows the **Timeline** tab. Each swim lane is a
core; events are colour-coded by type
(`MAC_COMPUTE` / `DMA_READ` / `DMA_WRITE` / `SYSTOLIC_STALL` /
`BARRIER_SYNC`). The right-hand stats panel is driven by the Rust
`core_utilisation` IPC.

## Main tabs (2026-04-20)

```{image} /_static/screenshots/node-editor.png
:alt: Node Editor with Blender-grade palette and pccx v002 node types
:width: 100%
```

| Tab | Component | Hot-key | Purpose |
|-----|-----------|---------|---------|
| Timeline          | `Timeline.tsx`           | — | Swim-lane event timeline over cycles |
| Flame Graph       | `FlameGraph.tsx`         | — | Hierarchical stall / compute stacks |
| Waveform          | `WaveformViewer.tsx`     | — | Signal waveforms (future VCD sink) |
| System Simulator  | `HardwareVisualizer.tsx` | — | 3D systolic array live view |
| Memory Dump       | `MemoryDump.tsx`         | — | Paginated hex view of the flat trace buffer |
| Data Flow         | `NodeEditor.tsx`         | **Shift+A** | Blender-grade block-diagram canvas |
| SV Editor         | `CodeEditor.tsx`         | — | SystemVerilog editor + AI inline gen |
| Report            | `ReportBuilder.tsx`      | — | Enterprise report composer |
| Verification      | `VerificationSuite.tsx`  | — | **4-card** pccx-FPGA verification dashboard |
| Roofline          | `Roofline.tsx`           | — | ECharts roofline chart |

## Verification dashboard (pccx-FPGA bridge)

```{image} /_static/screenshots/verification-synth-status.png
:alt: Verification -> Synth Status sub-tab with 4-card dashboard
:width: 100%
```

The **Verification → Synth Status** sub-tab is the one-stop dashboard
for pccx-FPGA RTL verification. Four cards stack top-to-bottom:

1. **Run Verification Suite** — shells out to
   `hw/sim/run_verification.sh` in the sibling pccx-FPGA repo and
   returns the per-testbench verdict table. Each row has an
   **Open** button that loads the generated `.pccx` into the
   Timeline via the `trace-loaded` event bus.
2. **Synthesis Status** — parses
   `hw/build/reports/{utilization,timing_summary}_post_synth.rpt`
   and surfaces LUT / FF / RAMB / URAM / DSP counts plus the WNS
   timing verdict.
3. **Roofline Analysis** — arithmetic intensity, achieved GOPS,
   compute-vs-memory-bound verdict, computed on the currently-cached
   trace.
4. **Bottleneck Windows** — fixed-window DMA / stall hotspot list
   with share %, event count, and core coverage (normalised).

See {doc}`../verification-workflow` for the end-to-end flow.

## Tauri IPC surface (17 commands)

| Command | Purpose |
|---------|---------|
| `load_pccx(path)` | Cache a trace + emit `trace-loaded` |
| `fetch_trace_payload()` | Flat 24-B/event buffer for the Timeline |
| `get_core_utilisation()` | Per-core MAC-utilisation stats |
| `compress_trace_context()` | LLM-prompt-sized trace summary |
| `generate_uvm_sequence_cmd(strategy)` | SV UVM sequence stub |
| `list_uvm_strategies()` | Enumerate the 5 built-in strategies |
| `generate_report()` | Legacy enterprise report |
| `generate_markdown_report(util_path, timing_path)` | Markdown summary of trace + synth |
| `analyze_roofline()` | Arithmetic intensity + bound verdict |
| `detect_bottlenecks(window_cycles?, threshold?)` | Hotspot window list |
| `load_synth_report(util_path, timing_path)` | Parsed Vivado synth report |
| `run_verification(repo_path)` | Run the full pccx-FPGA suite |
| `list_pccx_traces(repo_path)` | Enumerate `hw/sim/work/` traces |
| `validate_license(token)` | Tier + licensee + expiry |
| `get_license_info()` | Compiled-in tier |
| `get_extensions()` | Plugin catalogue (local LLM, VCD exporter, …) |

## Native-window automation

Everything above runs in a real **webkit2gtk** webview driven by
`tauri-driver` — the same E2E harness that CI uses. The
{doc}`../verification-workflow` page spells out the selenium +
tauri-driver setup; 19 pytest cases currently exercise the whole IPC
surface end-to-end.
