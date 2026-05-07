# Design Decisions

This page records public architecture decisions that affect the pccx
documentation line. It is a decision log, not an implementation-status
or performance-evidence page.

## v002.1 Datapath Decisions

Source: [pccxai/pccx-FPGA-NPU-LLM-kv260#80][kv260-80].

`kv260#80` resolves three defaults for follow-on v002.1 RTL, testbench,
software, and synthesis work. The upstream PR is docs-only: it does not
change datapath behavior, timing constraints, utilization evidence, or
measured throughput.

### Activation Quantization

**Decision:** use `e_max` / block-floating-point power-of-two activation
scaling as the v002.1 default. The parameter handle is
`ACT_SCALE_POLICY`, with the default mode `ACT_SCALE_EMAX_BFP`.

**Rationale:** the current preprocess direction already has an exponent
scan path, so this default gives the BF16-to-INT8 conversion a small,
deterministic first target. True symmetric INT8 and driver-provided scale
tables remain useful reviewed modes, but they require extra policy and
hardware/software interface work before they should become the default.

**Boundary:** this decision selects the first default policy. It does
not claim final task accuracy for quantized activations, and it does
not close later work on symmetric INT8, scale tables, saturation
conventions, or activation-scale restore.

### K-Drain Limit

**Decision:** make the K-split accumulator drain cadence parameterized,
with `K_DRAIN_LIMIT = 1024` as the v002.1 default.

**Rationale:** `1024` matches the current W4A8 packer and sign-recovery
bit-width budget and the existing smoke-test assumptions. Keeping the
value as a parameter leaves room for `4096` or another reviewed limit
after the packer, sign recovery, scheduler, and testbench bounds all
derive from the same setting.

**Boundary:** this decision does not assert that every long-K tile is
already drained by a completed scheduler path. It sets the default and
the parameter name that later RTL and tests should consume.

### DSP Accounting Baseline

**Decision:** report the v002.1 architectural DSP baseline as
`DSP_BASELINE_GEMM + DSP_BASELINE_GEMV + DSP_BASELINE_ALPHA`, with
`DSP_BASELINE_GEMM = 1024`, `DSP_BASELINE_GEMV = 64`, and
implementation extras reported under `DSP_BASELINE_ALPHA`.

**Rationale:** the baseline should describe the intended compute-core
geometry: a 32 x 32 GEMM grid plus four GEMV lanes that each use 16
DSP48E2 slices in the first reduction stage. Extra DSP use from final
accumulators, CVO/SFU, post-process, debug, or synthesis side effects
should be visible as alpha instead of hidden inside the denominator.

**Boundary:** this decision is an accounting convention. It does not
claim a final utilization number or timing-closed device fit; synthesis
reports remain the evidence source for actual DSP usage.

[kv260-80]: https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/pull/80
