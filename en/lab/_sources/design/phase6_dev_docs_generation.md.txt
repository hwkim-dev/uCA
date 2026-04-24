# Phase 6 — Development-phase Documentation Generator

**Status:** design (2026-04-24) — future TODO captured from the scope-expansion conversation.
**Scope:** roadmap Weeks 18-24; milestones M6.1 - M6.9.
**Mission shift:** pccx-lab stops being "a tool that runs at the end of a verification cycle" and becomes "a tool the developer runs continuously throughout the dev cycle".  Writing the SV should be enough; the docs write themselves.

## 1. Why — the expanded mandate

Phases 1-5 positioned pccx-lab as a verification / analysis / evolve
tool — the thing you run after the RTL is written to check it, profile
it, explain it, or refine it.  Phase 6 expands the mandate in two
directions:

- **Into the dev phase.**  The developer writes SystemVerilog + inline
  doc comments; pccx-lab emits documentation at the quality level of
  the pccx main site (Sphinx / Furo / MyST) without further editorial
  work.  The developer stays in the editor.  Docs are a side effect
  of writing clean, commented code.

- **Universal ingest.**  The pipeline is not pccx-specific.  Any well-
  commented SystemVerilog codebase can be fed in and a pccx-style
  docs site comes out — block diagrams, FSM state charts, ISA PDFs,
  register maps, all auto-generated.  "Port this SV project to a
  documented site" reduces to `pccx-lab docs emit <path>`.

The scale target for the analytics side expands in the same breath:
raw-mode traces can legitimately reach **tens to hundreds of GiB**
(full cycle-by-cycle + waveform + bus + cache state dump), so the
reader / streaming story has to handle that without loading the whole
thing into RAM.

## 2. Architecture

```
SV source + docstrings + ISA TOML + API TOML
         │
         ▼
┌─────────────────────────────┐
│  pccx-authoring (extended)  │  ← tree-sitter-verilog AST + doc
│  SvIngest / CommentExtract  │    comment block extraction
└──────────┬──────────────────┘
           │
           │ (typed IR: Module, Port, Param, FSM, Opcode, …)
           │
 ┌─────────┼─────────────────────────────────────────┐
 ▼         ▼                                         ▼
Sphinx /   TikZ / Mermaid diagram             xelatex ISA PDF
MyST  ─▶   generator (block, FSM, bus topology)       (mirrors pccx
pages      │                                         main ISA.pdf)
 │         │
 └───┬─────┴── Chrome-trace plots / Jupyter cells ───┐
     │                                                │
     ▼                                                ▼
  Static site                                  `pccx-isa-vXXX.pdf`
 (/en + /ko)                                   (ready to publish)
```

**Doc-comment convention** — the ingest layer reads block comments
formatted as (proposal):

```systemverilog
/*! \module ctrl_npu_frontend
 *  AXI-Lite command decoder for the NPU top-level.
 *
 *  \diagram block
 *  \fsm     decode_state
 *  \cycle   1 per AXIL beat
 */
module ctrl_npu_frontend (...);
```

`\diagram block` / `\fsm name` / `\cycle ...` / `\port` / `\param` are
the seed of the doc-comment vocabulary.  Exact schema lands at M6.1.

## 3. Renderer trio

Three output backends share the same typed IR so the same code
documents three surfaces:

| Backend | Output | Lives in |
|---|---|---|
| Sphinx / MyST | Static HTML site (EN + KO) | `pccx-reports` extended |
| TikZ / Mermaid | `.svg` / `.tex` diagrams embedded in pages | new: `pccx-figures` |
| xelatex | Standalone `isa-vXXX.pdf` mirroring the pccx main ISA PDF | new: `pccx-isa-bind` |

Isolation of the PDF backend into its own crate keeps the TeX
toolchain dep optional — users on systems without xelatex get
HTML + diagrams only and the PDF target skips silently.

## 4. Milestones

### M6.1 — SV parser + docstring extraction (Week 18)

- Add `tree-sitter-verilog` dep to `pccx-authoring`.
- Extract module / port / param / always_ff / FSM declarations into
  typed IR.
- Define the docstring grammar: `\module` / `\port` / `\param` /
  `\diagram` / `\fsm` / `\cycle` / `\see`.
- Emit a `pccx-lab docs check <file.sv>` CLI that validates
  docstrings and reports missing / malformed blocks.

### M6.2 — Block diagrams (Week 19)

- Walk the module hierarchy, emit a TikZ or Mermaid block diagram
  per `\diagram block` annotation.
- Default layout via a minimal placer (rectangle-packing on boundary
  counts); manual layout hints via `\layout left | right | …`.
- Respect the `pccx-diagram-rules` skill: CUDA / Intel-SDM monochrome
  palette, no gradients, fixed block-type colour classes.

### M6.3 — FSM state diagrams (Week 19)

- Visitor over `always_ff @ (posedge clk)` bodies with a
  case-over-state-enum pattern detect.
- Render each `\fsm <name>` as a Mermaid stateDiagram-v2 or a native
  TikZ `dot2tex` chain.
- Auto-detect dead states, flag them in the doc-check output.

### M6.4 — ISA PDF pipeline (Week 20)

- Consume the `pccx-authoring` ISA TOML compiler's output.
- Drive xelatex against a mirror of the pccx main `main.tex` layout
  (shared skill: `pccx-isa-preprint`).
- Output: `_build/pdf/<project>-isa-v<N>.pdf`.
- CI target: `make isa-pdf` in the repo's `docs/Makefile`.

### M6.5 — Universal SV porting (Week 21)

- `pccx-lab docs port <existing-sv-project>` — migration helper that
  scans an unannotated codebase, generates a `docstrings.toml`
  skeleton with empty `\module` / `\port` blocks for the developer
  to fill in, and emits a baseline docs tree so the first `docs
  emit` run produces something coherent even before annotation.
- Ships with a `pccx-lab` self-port as the canonical example.

### M6.6 — Raw analytics mode (Week 22)

- `--raw` flag on the analytics CLI emits full cycle-by-cycle +
  waveform + bus + cache state into a streamable container
  (Zstd-compressed columnar format).
- Expected output size: **tens to hundreds of GiB** on realistic
  transformer-decode traces.  The raw container MUST be mmap-readable
  so downstream tools (Jupyter, polars, duckdb) can query without
  loading.
- A companion `pccx-raw-reader` binary streams rows matching a
  cycle / core / event filter without materialising the whole file.

### M6.7 — CLI / GUI parity (Week 23)

- Guarantee: every CLI subcommand has a GUI affordance, and every
  GUI action dispatches the same underlying Tauri command that the
  CLI invokes (shared `pccx_cli::cmd` dispatcher in `pccx-core`).
- Contract test in CI: a `parity_check` integration test that
  enumerates both surfaces and fails on any asymmetry.
- Command palette in pccx-ide surfaces CLI names directly.

### M6.8 — AI-augmented prose pass (Week 23)

- After ingest, a Sonnet pass proposes prose around the extracted
  structure — "this module is the AXI-Lite command decoder feeding
  the NPU top-level; stalls are expected when the command queue is
  full because …" — gated on the developer accepting each proposal
  inside pccx-ide (no silent prose injection).
- Prose proposals diffed against existing docstrings so nothing is
  ever overwritten without consent.

### M6.9 — Release — v0.6 dev-phase bundle (Week 24)

- Ship `pccx-lab docs emit` / `docs check` / `docs port` as first-
  class binary commands.
- Ship the Phase 6 handbook page describing the docstring schema
  and a worked example.
- Example: re-run the whole pipeline against pccx-FPGA-NPU-LLM-kv260
  + pccx-lab itself, publish the outputs, use them as the v0.6
  launch artefact.

## 5. Scale / resource notes

- Raw analytics output: tens to hundreds of GiB per long-running
  trace.  Zstd columnar → ~10-20x compression typical, still GiB-
  scale.  Storage is user-provisioned; pccx-lab never assumes disk
  beyond what the user points at.
- AI prose passes cost the Sonnet budget — expect ~1-5 K tokens
  per module for non-trivial bodies; cache by AST hash.
- Sphinx full-site rebuild: target < 30 s on a 100-module codebase
  via incremental build + sphinx-autobuild.

## 6. CLI / GUI parity principle

The parity target is stronger than "the GUI can do everything the CLI
can".  It is bidirectional:

- Any CLI invocation is a single-line equivalent of a GUI flow, with
  deterministic output suitable for scripting.
- Any GUI interaction prints (and copies to clipboard) the CLI
  invocation that would replay it exactly — "what did I just do?" is
  always answerable with a one-liner.

This is the affordance that makes pccx-lab trustworthy as a dev
tool: everything the human does in the IDE, the CI can repeat.

## 7. Out of scope

- Synthesis.  Compile / elab / place-and-route stays in the RTL repo;
  Phase 6 reads SV but does not synthesise it.
- pccx-main site editorial control.  Phase 6 generates pccx-style
  docs *for the user's own project*; pccx's editorial site keeps its
  hand-authored pages.
- PDF typography beyond xelatex's native capabilities.  No custom
  InDesign-grade layout.
- Live HDL simulation inside the docs generator.  Traces come in
  through the existing `.pccx` format; Phase 6 does not run a sim.

## 8. Dependencies

Existing (from earlier phases):

- `pccx-authoring` — ISA / API TOML compilers; extended here for SV
  ingest.
- `pccx-reports` — MD / HTML / PDF rendering plumbing extended for
  Sphinx-driven output.
- `pccx-lsp` — comment-extraction seam reuses the provider trait
  pipeline for incremental doc-gen as the developer types.
- `pccx-ide` — GUI affordance surface; CLI parity contract lives
  here.

New:

- `tree-sitter-verilog` — fast incremental SV parser.
- Either `typst` or an extended `xelatex` toolchain (via the
  `pccx-isa-preprint` skill's pipeline).
- `zstd` / columnar writer (`arrow-rs` or a minimal bespoke format)
  for raw analytics.

## 9. Open questions

- **Docstring vocabulary** — Doxygen-style `\module` vs Rust-style
  `/// #[module]` vs a fresh DSL.  Decide at M6.1 review.
- **Mermaid vs TikZ primary.**  Mermaid is friendlier for HTML /
  onboarding; TikZ is better for print.  Emit both from the same IR
  and let the renderer pick per-output.
- **ISA TOML vs directly parsed SV `enum`.**  Today `pccx-authoring`
  is TOML-driven; some projects define opcodes inline in SV.  M6.4
  needs to read both.
- **Auto-emit cadence.**  Run on every save (expensive) vs on-demand
  (staler) vs git pre-commit hook (middle ground).  Ship all three
  behind a config flag.

---

_Drafted 2026-04-24 from scope-expansion conversation.  See
`docs/design/rationale.md` for the module-boundary implications: this
phase extends existing crates rather than adding new workspace members,
so the 10-crate layout is unchanged.  Only crates that gain surface
are `pccx-authoring` (SV ingest), `pccx-reports` (Sphinx driver) and
`pccx-ide` (CLI/GUI parity contract)._
