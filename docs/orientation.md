---
myst:
  html_meta:
    description lang=en: |
      One-page orientation to the pccx documentation repository, including
      the English and Korean source trees, release sections, and key entry
      points for contributors.
---

# Repository Orientation

This repository is the Sphinx documentation site for the pccx ecosystem.
The active RTL is kept in companion repositories; this repo explains the
architecture, ISA, driver surface, verification posture, release evidence,
and reader-facing project tracks.

## Documentation Structure

The site is built from two parallel documentation roots:

| Path | Role |
|---|---|
| `docs/` | English documentation. This is the canonical source for new content. |
| `ko/docs/` | Korean documentation. This tree is produced by external translation tooling and may trail the English source. |
| `index.rst` | English build root and sidebar toctree. It links the main reader sections. |
| `ko/index.rst` | Korean build root and sidebar toctree. It mirrors the public section layout for the KO site. |
| `conf_common.py` | Shared Sphinx configuration for both language builds. |
| `conf.py`, `ko/conf.py` | Thin language-specific wrappers around the shared config. |

When adding reader documentation, start in `docs/`. Keep path names stable
where possible because cross-references, language switching, and published
URLs depend on predictable EN/KO counterparts.

## Key Sections

| Section | Path | Purpose |
|---|---|---|
| Introduction | `docs/index.rst`, `docs/quickstart.md`, `docs/roadmap.md` | Project summary, reproducer path, and release-track direction. |
| Evidence | `docs/Evidence/index.rst` | Measured-results posture and release evidence gates. |
| v002 | `docs/v002/` | Active KV260 LLM architecture line. This is the primary technical reference. |
| v002 Architecture | `docs/v002/Architecture/` | Top-level hardware design, dataflow, memory hierarchy, floorplan, and compute cores. |
| v002 ISA | `docs/v002/ISA/` | 64-bit instruction encoding, instruction behavior, and dataflow notes. |
| v002 RTL | `docs/v002/RTL/` | Source-oriented reference pages that link to the external SystemVerilog repository. |
| v002 Drivers | `docs/v002/Drivers/` | HAL, API, and host software surface. |
| v002 Models | `docs/v002/Models/` | Gemma-3N execution notes and model-specific mapping pages. |
| Formal, Verification, Build | `docs/v002/Formal/`, `docs/v002/Verification/`, `docs/v002/Build/` | Sail model, verification status, and bitstream/build notes. |
| Target Hardware | `docs/Devices/` | Device-specific pages, currently centered on KV260. |
| pccx-lab Handbook | `docs/Lab/` | Trace, profiler, workflow facade, analyzer API, CLI, IPC, and verification workflow documentation. |
| Future Tracks | `docs/v003/`, `docs/vision-v001/` | Placeholders for the next LLM line and a parallel vision workload line. |
| Archive | `docs/archive/` | Historical v001 documentation retained for reference. |
| Toolchain Demos | `docs/samples/` | Mermaid, WaveDrom, SVG, and plotting examples for the docs toolchain. |
| Releases | `docs/releases/` | Release notes and published release summaries. |

## Source Of Truth

Treat the English docs as the edited documentation source. For v002 RTL
facts, the SystemVerilog package and modules in
`pccx-FPGA-NPU-LLM-kv260` win over this repository. Documentation tables,
instruction widths, opcodes, and enums should be copied from RTL into the
docs, not inferred in the opposite direction.

For public claims, prefer pages that carry explicit evidence gates. The
roadmap can describe planned tracks, but throughput, timing, and board-run
numbers should land only after the evidence page and release checklist can
support them.

## Build And Review Entry Points

Use `make en` for a quick English build, `make ko` for the translated tree,
and `make strict` before declaring documentation work complete. Use
`make lint` for sphinx-lint and codespell checks, and reserve
`make linkcheck` for link-heavy changes or release preparation.

Before editing diagrams or plots, follow the project-specific figure rules:
new diagrams live under `_static/diagrams/`, plots live under `plots/`,
and generated outputs should stay reproducible from source.
