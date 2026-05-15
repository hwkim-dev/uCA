# pccx vision-v001 — CNN inference track on KV260

The vision-v001 line is a parallel product line on the same KV260
substrate, scoped to **vision** workloads (CNN-class classification,
object detection). It shares the W4A8 NPU substrate with the LLM
line but covers a distinct workload family. Active code is not yet
present in this docs site — this page is a placeholder while the
upstream RTL repository stabilises.

## Working state

- repository: [`pccxai/pccx-vision-v001`](https://github.com/pccxai/pccx-vision-v001)
- shared substrate with v002 — same KV260 board, same W4A8 weight ×
  activation ratio, same L2 URAM organisation
- distinct dataflow — dense-conv tile reuse instead of token-by-token
  KV streaming; the GEMM systolic + GEMV hybrid is reused for conv
- first model candidates — ResNet18, YOLOv8n, MobileNetV3
  (smallest-footprint variants first; choice is driven by the L2
  URAM and DSP budget on KV260)

## Position relative to existing FPGA vision IPs

The KV260 vision landscape today is occupied by two large families
of IP: vendor-supplied DPU IP (INT8-only) and arbitrary-bit
streaming-dataflow accelerators driven by quantisation-aware training
(QAT). The vision-v001 track positions itself differently from both,
on three axes.

```{table} vision-v001 differentiation matrix (landscape context, not a benchmark)
:name: tbl-vision-v001-differentiation-en

| Axis                    | Commodity DPU IP (INT8-only) | Streaming-dataflow QAT (FINN-class) | vision-v001 (this track)               |
|---|---|---|---|
| Quantisation            | INT8 weights / INT8 activations | arbitrary 2–8 bit, QAT              | **W4A8** — INT4 weight × INT8 act   |
| Dataflow                | heterogeneous micro-coded PE mix | per-layer streaming dataflow        | unified GEMM systolic + GEMV         |
| Reuse with LLM line     | none                            | none                                | **same RTL substrate as v002**       |
| Per-layer efficiency    | reported 5–9× variance across stages | high but model-specific build       | designed for tile-reuse uniformity   |
| Source                  | vendor reference                | open-source (e.g. FINN), QAT toolchain | open-source, KV260-native            |
```

The differentiation is *posture*, not a benchmark — no FPS, latency,
power, or accuracy figure is claimed on this page until the release
evidence checklist gates it in. References to existing vendor / QAT
IPs are landscape context only.

### Reference points from public benchmarks

The figures below are **publicly reported** benchmarks of the two
families above. They are **not** vision-v001 results; they exist
solely to anchor the differentiation matrix in numbers external
readers can verify.

- **Vendor DPU IP on KV260 (Xilinx DPUCZDX8G B4096)** — MobileNet V1
  ≈ 187 FPS / 5.3 ms latency; ResNet-50 ≈ 62 FPS / 16.1 ms latency.
  Per-layer efficiency varies between input layers (≈ 54–259 GOP/s)
  and mid-stage 3 × 3 convolutions (≈ 470–500 GOP/s) — a 5–9 ×
  spread on the same model.
- **Streaming-dataflow QAT (FINN)** — ResNet-50 ≈ 2 000 FPS at
  ≈ 70 W on Alveo U250 (~400 K LUTs); the same approach scaled
  down to KV260 (~256 K LUTs) typically lands 2–4 × lower.
- **W4A8 vision regime** — INT8 dominates the KV260 model zoo;
  sub-4-bit (binary / ternary / 2-bit) work appears under the
  streaming-dataflow line. The W4A8 weight × activation regime that
  pccx v002 uses for LLMs has not yet been published as a KV260
  vision benchmark.

These reference points anchor the differentiation matrix; they do
not constitute a benchmark of vision-v001 itself, and no
vision-v001 figure is claimed on this docs site until the release
evidence checklist gates it in.

## Status snapshot

```{table} vision-v001 layer status (placeholder)
:name: tbl-vision-v001-status-en

| Layer              | State                                                            |
|---|---|
| RTL                | not yet committed in the vision-v001 repository                  |
| Driver / runtime   | scope TBD; conv-specific path likely diverges from v002          |
| Verification       | inherits the v002 evidence checklist; per-model golden vectors TBD |
| FPS claim          | none — TBD                                                       |
| mAP / Top-1 claim  | none — TBD                                                       |
| Bitstream          | none — TBD                                                       |
```

This page will be expanded as the upstream RTL repository lands and
the first model is profiled.

## See also

- {doc}`../roadmap` — release direction across the pccx ecosystem
- {doc}`../v002/index` — shared NPU substrate (active LLM line)
- {doc}`../v003/index` — LLM line continued, separate RTL repository
