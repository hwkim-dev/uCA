<div align="center">

# pccx — Parallel Compute Core eXecutor

**A scalable NPU architecture for Transformer LLM inference on edge FPGAs**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Target](https://img.shields.io/badge/Target-Xilinx_Kria_KV260-red)](https://www.xilinx.com/products/som/kria/kv260-vision-starter-kit.html)
[![Architecture](https://img.shields.io/badge/Architecture-v002_Active-purple)](#architecture)
[![Precision](https://img.shields.io/badge/Precision-W4A8_→_BF16%2FFP32-green)](#precision)
[![Docs](https://img.shields.io/badge/Docs-Online-brightgreen)](https://pccx.pages.dev/)

**[Full Documentation →](https://pccx.pages.dev/)**

</div>

---

## Project status

**Public alpha** — `v0.1.0-alpha` is published as a prerelease. Core
architecture and ISA are stable; verification, KV260 bring-up, and
documentation polish are in progress. Expect rough edges; feedback and
issues are welcome.

| Entry point | Link |
| --- | --- |
| Documentation | <https://pccx.pages.dev/> |
| Releases | <https://github.com/pccxai/pccx/releases> |
| `v0.1.0-alpha` notes | [docs/releases/v0.1.0-alpha.md](docs/releases/v0.1.0-alpha.md) |
| Roadmap (project board) | <https://github.com/orgs/pccxai/projects/1> |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| How to cite | [CITATION.cff](CITATION.cff) |
| Discussions | <https://github.com/pccxai/pccx/discussions> |
| Good first issues | <https://github.com/pccxai/pccx/labels/good%20first%20issue> |

---

## v002.1 evidence-gated pointers

| Item | Link | Guard |
| --- | --- | --- |
| Architecture explainer | [`docs/spec/v002.1-architecture-explainer.md` (PR #48)](https://github.com/pccxai/pccx/blob/docs/v002.1-architecture-explainer/docs/spec/v002.1-architecture-explainer.md) | Draft explainer; no board-run, closed-timing, deployable-bitstream, or measured-throughput claim. |
| Evidence inventory | [`pccx-FPGA-NPU-LLM-kv260` evidence inventory (PR #95)](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/blob/docs/v002.1-evidence-inventory/docs/evidence/v002.1-evidence-inventory.md) | Inventory of landed and pending evidence; release claims remain gated by measured artifacts. |
| Bitstream runbook | [`pccx-FPGA-NPU-LLM-kv260` bitstream runbook (PR #82)](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/blob/build/v002-kv260-bitstream-runbook/docs/runbooks/v002.1-bitstream-build.md) | Pre-flight runbook; Vivado and KV260 board execution are not claimed by this link. |
| Project board | [PCCX Roadmap project board](https://github.com/orgs/pccxai/projects/1) | Planning tracker; status must be read with the evidence gates above. |

---

## What is pccx?

pccx is a hardware-software co-design framework that accelerates **autoregressive decoding** of Transformer-based LLMs on resource-constrained edge devices. The primary target is the **Xilinx Kria KV260** SOM.

Rather than reusing a generic matrix accelerator, pccx is sized around the dominant bottleneck of LLM decoding: **memory bandwidth-bound GEMV**, not compute-bound GEMM. The architecture separates matrix (GEMM) and vector (GEMV) datapaths, supplies weights through dedicated HP AXI ports, and uses a custom 64-bit VLIW ISA to reduce dispatch-side stalls.

---

## Architecture (v002)

<table>
<tr>
<th>Core</th>
<th>Configuration</th>
<th>Peak Throughput</th>
<th>Primary Use</th>
</tr>
<tr>
<td><b>GEMM (Matrix)</b></td>
<td>32 × 32 systolic array (cascade split @ row 16)</td>
<td><b>819 GMAC/s @ 400 MHz</b></td>
<td>Prefill, Q·Kᵀ, score·V</td>
</tr>
<tr>
<td><b>GEMV (Vector)</b></td>
<td>4 cores × 32-MAC LUT pipeline + 5-stage reduction tree</td>
<td>Weight-streaming limited (~51.2 GMAC/s @ 400 MHz)</td>
<td>Autoregressive decoding</td>
</tr>
<tr>
<td><b>SFU / CVO</b></td>
<td>CORDIC + LUT hybrid</td>
<td>BF16 / FP32 promoted</td>
<td>Softmax, GELU, RMSNorm, RoPE</td>
</tr>
</table>

**Key design decisions:**

- **W4A8 precision** — INT4 weights × INT8 activations via DSP48E2 dual-channel bit packing (1 DSP = 2 MACs)
- **Precision promotion** — non-linear ops (Softmax, GELU, RMSNorm, RoPE) automatically upcast to BF16/FP32 for numerical stability
- **Custom 64-bit VLIW ISA** — 5 opcodes: `GEMV`, `GEMM`, `MEMCPY`, `MEMSET`, `CVO`; decoupled decode/dispatch eliminates front-end stalls
- **Shared L2 (URAM 1.75 MB)** — all three cores share a central SRAM cache; GEMV↔SFU are connected via a direct-connect FIFO, bypassing L2 round-trips
- **Dual clock domains** — 250 MHz AXI/control plane, 400 MHz core compute (×1.6 frequency gain over v001)
- **3.125× total throughput gain** vs. v001 (frequency × dual-MAC DSP packing)

```
External AXI (250 MHz)          Core Domain (400 MHz)
─────────────────────           ──────────────────────────────────────────────────────
S_AXIL_CTRL (HPM)    ────────►  npu_controller_top
                                  ├─ ctrl_npu_decoder   (64-bit VLIW → opcode + body)
S_AXI_HP0/HP1        ────────►  GEMM_systolic_top      (32×16×2, W-Stationary)
S_AXI_HP2/HP3        ────────►  GEMV_top               (4 cores × 32-MAC LUT, 5-stage tree)
S_AXIS_ACP_FMAP      ────────►  ┌─────────────────────────────────┐
M_AXIS_ACP_RESULT    ◄────────  │  Shared L2 Cache (URAM 1.75 MB)│
                                │  GEMV ──FIFO──► CVO_top (SFU)  │
                                └─────────────────────────────────┘
```

---

## Memory Hierarchy

| Level | Technology | Size | Access |
|-------|-----------|------|--------|
| L1 (Activation row buffer) | Block RAM | per-core | Systolic / GEMV lanes |
| L2 (Shared cache) | URAM | 1.75 MB (114,688 × 128-bit) | All cores + mem_dispatcher |
| Weight stream | HP AXI port × 4 | DDR4 bandwidth | HP0/1 → GEMM, HP2/3 → GEMV |
| KV Cache | External / off-chip memory model | System-dependent capacity | ACP / coherent access path |

> **KV cache bandwidth wall:** At 32K context (Gemma 3N E4B), the accumulated KV cache reaches ~1.31 GB. Mitigation: KV quantization (FP16→INT8/INT4), attention sink eviction, and a driver-enforced `KV_MAX_TOKENS` hard cap.
>
> The capacity field above is a system-level memory model, not a guaranteed on-board KV260 figure. Reproducible board measurements will be reported separately with the board configuration, model, context length, precision, and benchmark command.

---

## Repository topology

| Repository | Role |
| --- | --- |
| `pccx` | Canonical specification, documentation, and project index. |
| `pccx-v002` | v002 IP-core package for LLM, Vision, Voice, and common reusable sources. |
| `pccx-v003` | Future v003 IP-core package. |
| `pccx-FPGA-NPU-LLM-kv260` | KV260 + LLM application integration; consumes `pccx-v002`. |

The reusable IP-core line is board- and model-agnostic. Board and model
repositories consume the IP-core package; IP-core RTL and compatibility
contracts do not name a specific board or model.

For the authoritative version of this table, the boundary rule, and the
submodule pin policy, see [`docs/reference/repo-topology.md`](docs/reference/repo-topology.md).

### Local documentation layout

```
pccx/
├── conf.py / index.rst          # English Sphinx config & root toctree
├── ko/                          # Korean Sphinx subsite (ko-first authoring)
│   ├── conf.py
│   └── docs/                    # Korean documentation source
├── docs/                        # English documentation source
│   ├── v002/                    # Active architecture docs
│   │   ├── Architecture/        # Core design, DSP48E2, KV cache, rationale
│   │   ├── ISA/                 # 64-bit VLIW instruction set reference
│   │   ├── Drivers/             # Host API & driver documentation
│   │   └── RTL/                 # Embedded RTL source reference
│   └── archive/experimental_v001/
├── assets/images/               # Architecture diagrams (PNG)
├── _static/                     # JS/CSS (language switcher, Mermaid theme)
└── codes/
    ├── v001/hw/rtl/             # v001 RTL (archived, reference only)
    └── v002/                    # external RTL checkout used by docs builds
```

Sibling repositories:

- **`pccx-v002`** — reusable v002 IP-core package.
- **`pccx-v003`** — future reusable v003 IP-core package.
- **[pccxai/pccx-FPGA-NPU-LLM-kv260](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260)** — KV260 + LLM application integration that consumes `pccx-v002`.
- **[pccxai/pccx-lab](https://github.com/pccxai/pccx-lab)** — performance simulator, CLI-first verification lab, and trace profiler. The public Lab documentation lives on `https://labs.pccx.ai/`.

---

## Roadmap — Staged release track

pccx is developed across staged releases. v002.0 is the baseline KV260
integration; v002.1 layers sparsity and speculative decoding on the v002
line; v003.x belongs to the future `pccx-v003` IP-core package. A
long-term auto-porting compiler begins once the v002 / v003 lines are
stable.

| Release | RTL Repo | Target Model | Scope | Throughput Target | Status |
|---------|----------|--------------|-------|-------------------|--------|
| **v002.0** | `pccx-v002` + [`pccxai/pccx-FPGA-NPU-LLM-kv260`](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260) | Gemma 3N E4B | A–F baseline integration | measured-only | In progress |
| **v002.1** | `pccx-v002` + [`pccxai/pccx-FPGA-NPU-LLM-kv260`](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260) | Gemma 3N E4B | G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark | evidence-only | Planned |
| **v003.0** | `pccx-v003` | Gemma 4 E4B | foundation + first architectural novelty | TBD | Planned |
| **v003.1** | `pccx-v003` | Gemma 4 E4B | second novelty + KV/decoding co-design | TBD | Planned |
| **Auto-Porting α** | [`pccxai/pccx`](https://github.com/pccxai/pccx) | Arbitrary Transformer | `config.json` → pccx ISA codegen | n/a | Planned (Y2) |

**v002.1 compute budget**: $70–100 total for EAGLE head training ($40 if
a TRC TPU grant lands). The training plan is scoped to v002.1, where
the speculative-decoding stack is integrated.

→ **[Full roadmap (EN)](https://pccx.pages.dev/en/docs/roadmap.html)**
&nbsp;·&nbsp; [**한국어**](https://pccx.pages.dev/ko/docs/roadmap.html)

---

## Ecosystem

### pccx-lab — Simulator & Verification Lab

Performance simulator, CLI-first verification lab, and trace profiler for the pccx NPU. Pre-RTL bottleneck detection, UVM co-simulation, and testbench/trace workflow support share one workflow.

- Repository: https://github.com/pccxai/pccx-lab
- Documentation: https://labs.pccx.ai/
- Status: Work in Progress

---

## Documentation

The full technical documentation — architecture deep-dives, ISA encoding tables, DSP48E2 bit-packing derivation, driver API, and embedded RTL source — is published at:

### **[pccx.pages.dev/](https://pccx.pages.dev/)**

Available in **English** and **한국어 (Korean)**.

Highlights:
- [Architecture Overview](https://pccx.pages.dev/en/docs/v002/Architecture/top_level.html) — block diagram, design rationale, 3.125× gain breakdown
- [DSP48E2 W4A8 Derivation](https://pccx.pages.dev/en/docs/v002/Architecture/dsp48e2_w4a8.html) — dual-channel bit packing math
- [Custom ISA Reference](https://pccx.pages.dev/en/docs/v002/ISA/index.html) — 64-bit VLIW encoding, opcode table, dataflow
- [RTL Source Reference](https://pccx.pages.dev/en/docs/v002/RTL/index.html) — embedded SystemVerilog with live syntax highlighting

### Documentation map

In-repo developer-facing documentation:

- [`docs/reference/`](docs/reference/README.md) — repository topology, v002 contract narrative, boundary rule, testing protocol, submodule pin policy.
- [`docs/onboarding/`](docs/onboarding/README.md) — getting started, architecture overview reading order, contribution rules (draft).
- [`docs/evidence/`](docs/evidence/evidence-pack-index.md) — evidence pack index and risk register.
- [`docs/roadmap/`](docs/roadmap/milestones.md) — milestones reflecting actual state.
- [`docs/commercial/`](docs/commercial/README.md) — open / commercial / capital track separation **(DRAFT, not legal advice)**.
- [`docs/ip/`](docs/ip/README.md) — patent strategy, trademarks, trade secret policy, contributor licence agreement intent **(DRAFT, not legal advice)**.

---

## Building the Docs Locally

```bash
pip install -r requirements.txt
sudo apt-get install graphviz   # for Graphviz diagrams

# Clone v002 RTL (required for literalinclude directives)
git clone --depth 1 \
  https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260 \
  codes/v002

# Build English site
sphinx-build -b html . _build/html/en

# Build Korean site
sphinx-build -b html ko _build/html/ko

# Serve locally
python -m http.server --directory _build/html
# → open http://localhost:8000/en/ or /ko/
```

---

## v001 → v002 Migration

| Pain point (v001) | v002 solution |
|---|---|
| Core role ambiguity (Matrix/Vector/CVO blurred) | Strict separation: GEMM / GEMV / SFU |
| Excessive intermediate bus paths | Shared L2 + direct-connect FIFO for GEMV↔SFU |
| L2 ↔ Global Cache responsibility overlap | Single unified L2 (URAM) |
| Single HP port → one systolic array bottleneck | HP0/HP1 for GEMM, HP2/HP3 for GEMV (distributed) |
| 1 DSP = 1 MAC (bit headroom wasted) | Dual-channel packing → 1 DSP = 2 MACs |
| 250 MHz ceiling (AXI clock) | Decoupled 400 MHz core domain |

---

## License

Licensed under the **[Apache License 2.0](LICENSE)**.

## Trademark

`PCCX™` is a mark used by the PCCX project. Korean trademark
applications are pending for PCCX in Classes 09 and 42 (application
numbers `40-2026-0091497` and `40-2026-0091498`). Registration has
not been granted; do not use `PCCX®` until this policy is updated.
See [`TRADEMARKS.md`](TRADEMARKS.md) for permitted use, restricted
use, and the public-safe filing docket.

<div align="center">

Built by [@hkimw](https://hkimw.github.io/hkimw/) · [Documentation](https://pccx.pages.dev/) · [Issues](https://github.com/pccxai/pccx/issues)

</div>
