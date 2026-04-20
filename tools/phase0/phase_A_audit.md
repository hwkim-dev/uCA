# Phase A Entry-Point Audit (pccx-FPGA-NPU-LLM-kv260 `main`)

Read-only snapshot — 2026-04-20. Source: `hw/rtl/Constants/…` and
`hw/rtl/MAT_CORE/…` in the external RTL repo.

Goal of this audit: identify which v002 parameters are already live vs.
which still reflect v001, so Phase A (re-parameterization, 5 weeks) can
start on the right files.

## 1. What's already v002

| Item | File | Evidence |
|---|---|---|
| INT4 weight type | `C_type_pkg/dtype_pkg.sv` | `Int4Width = 4`, range helpers |
| INT8 activation type (W4A8) | `C_type_pkg/dtype_pkg.sv` | `Int8Width = 8` with explicit "W4A8 path" comment |
| BF16 / FP32 promotion types | `C_type_pkg/dtype_pkg.sv` | `Bf16*`, `Fp32Width`, `FixedMantWidth = 27` |
| 64-bit VLIW ISA | `A_const_svh/npu_arch.svh` | `ISA_WIDTH = 64`, 4-bit opcode + 60-bit body |
| 4 × 128-bit HP ports | `A_const_svh/kv260_device.svh` | `DEVICE_HP_PORT_CNT = 4`, `DEVICE_HP_SINGLE_WIDTH_BIT = 128` |
| DSP48E2 port widths | `A_const_svh/kv260_device.svh` | A=30, B=18, P=48 (matches doc spec) |
| URAM / BRAM capacity | `A_const_svh/kv260_device.svh` | 64 URAMs × 288 Kb, 144 BRAMs × 36 Kb |
| XPM FIFO macros | `A_const_svh/kv260_device.svh` | FIFO_DEPTH=512, FIFO_DEPTH_TINY=16 |

## 2. What still needs attention

### 2.1 Systolic array shape — ✅ already correct as **32 × 16 × 2**

User-preferred framing (2026-04-20): **32 × 16 × 2 cascade-split**.
The existing RTL already implements exactly that as `32 × 32 physical
rows with a cascade break at row 16`:

- `GEMM_systolic_array.sv:135` instantiates `GEMM_dsp_unit` with
  `BREAK_CASCADE = 1` at `row == 16`. PCIN/PCOUT chain is cut there,
  and the partial sum lands on `P_fabric_out` → `V_result_in` of the
  row-16 unit via fabric, forming two independent 32 × 16 sub-arrays
  whose results are merged at the bottom.
- `ARRAY_SIZE_V = 32` is the correct **physical** total; the "× 2" is
  encoded by the cascade break, not by the constant.
- `pccx/docs/v002/…` uniformly describes the array as
  "32 × 32 systolic array (cascade break @ row 16)", which is
  mathematically identical to "32 × 16 × 2". No doc rewrite needed.

**No RTL change required for §2.1.** The earlier claim in this audit
that `ARRAY_SIZE_V` needed to go 32 → 16 was incorrect — apologies to
future readers.

**Residual risk**: the scheduler / accumulator drain cadence must match
the cascade-break depth (drain every 1024 MACs on each half
independently). That falls under §2.2 follow-ups.

### 2.2 DSP bit-packing (1 DSP = 2 MAC) — ✅ modules drafted + simulated

**Status** (2026-04-20):

- ✅ `hw/rtl/MAT_CORE/GEMM_dsp_packer.sv` — pre-DSP48E2 packer. Two signed
  INT4 weights into the 30-bit A-port at `UPPER_SHIFT = 21`, INT8
  activation sign-extended to 18-bit B-port. Uses signed arithmetic
  (shift + add), not naive concatenation, so negative weights encode
  correctly.
- ✅ `hw/rtl/MAT_CORE/GEMM_sign_recovery.sv` — post-DSP unpacker. Lower
  channel = `P[20:0]` as 21-bit signed. Upper channel = `P[41:21]` as
  21-bit signed, incremented by 1 whenever the lower channel is
  negative (carry-borrow correction).
- ✅ `hw/tb/tb_GEMM_dsp_packer_sign_recovery.sv` — closed-loop testbench
  wrapping a behavioural DSP48E2 (signed `A*B`, accumulate). Drives
  1024 random INT4 × INT8 cycles, compares against a software golden.
  **Passes on xsim (Vivado 2025.2): 1024 cycles, 0 mismatches.**

Bit-width derivation (documented in the packer header):

- Per-MAC: `|w| * |a| <= 8 * 128 = 2^10`
- 1024 accumulations: `2^20` per channel → 21 signed bits each
- `UPPER_SHIFT = 21` places two 21-bit fields exactly adjacent:
  `P[20:0]` lower, `P[41:21]` upper, `P[47:42]` sign-ext headroom.

**Integration status (2026-04-20 continued)**:

- ✅ `GEMM_dsp_unit.sv` — refactored to v002. Two INT4 weight inputs
  (`in_H_upper` / `in_H_lower`) feed `GEMM_dsp_packer`. Packer drives
  the DSP48E2 A-port directly (`A_INPUT = DIRECT`). INT8 activation
  enters on the B-port, taking the fabric path at row 0 and at the
  cascade-break row 16 (`B_INPUT = DIRECT`), and the `BCIN/BCOUT`
  cascade chain for every other row.
- ✅ `GEMM_dsp_unit_last_ROW.sv` — same refactor as above.
- ✅ `GEMM_systolic_array.sv` — two horizontal weight chains, 8-bit
  INT8 vertical fabric, BCIN cascade chain replacing the old ACIN
  chain. Cascade-break logic at row 16 preserved.
- ✅ `GEMM_Array.svh` — collapsed to a pass-through of `npu_arch.svh`
  (removes the `ARRAY_SIZE_H`/`ARRAY_SIZE_V` redefinition warnings).
- ✅ `GEMM_systolic_top.sv` — wired to the new systolic array port
  list. Placeholder stubs for the upper-weight lane and the INT8
  activation (truncates the 27-bit mantissa to 8 bits for the time
  being — see `TODO(pccx v002 §2.2 follow-up)` in the file).

**Verified (xsim Vivado 2025.2)**:

- `xvlog -sv ...` + `xelab -L unisims_ver GEMM_systolic_array glbl`
  completes without errors. All 1024 DSP48E2 cells elaborate with
  the v002 port configuration.
- `tb_GEMM_dsp_packer_sign_recovery` still passes 1024/1024 cycles.

**Pre-existing MAT_CORE bugs fixed as a side-effect**:

- `\`INT4` → `\`INT4_WIDTH` (GEMM_systolic_top, GEMM_weight_dispatcher).
- `\`HP_WEIGHT_CNT(…)` macro did not exist → replaced with a direct
  `\`HP_PORT_SINGLE_WIDTH / \`INT4_WIDTH` expression.
- `\`AXI_DATA_WIDTH` → `\`AXI_STREAM_WIDTH` (FROM_mat_result_packer).
- `\`ACIN` → `\`DEVICE_DSP_A_WIDTH` (GEMM_fmap_staggered_delay).
- Missing comma in `GEMM_weight_dispatcher` instantiation parameters.

**Cleared this sprint**:

- ✅ `FROM_mat_result_packer.sv:62` — declaration of `send_idx` moved
  above the always-ff that clears `capture_valid`. Pre-existing bug
  resolved.
- ✅ `GEMM_weight_dispatcher.sv` — rewritten as a dual-lane pipeline
  register. Exposes `fifo_upper` + `fifo_lower` + `weight_upper` +
  `weight_lower`. Type-mismatch bugs and the undeclared `w_lane_cnt`
  are gone.
- ✅ `GEMM_systolic_top.sv` — now takes two distinct weight lanes
  (`IN_weight_upper` + `IN_weight_lower`) end-to-end into
  `H_in_upper` / `H_in_lower`. No more "same-stream" placeholder.
- ✅ `GLOBAL_CONST.svh::GEMM_MAC_UNIT_IN_H / IN_V` — retired with a
  tombstone comment. Callers now use
  `INT4_WIDTH` / `DEVICE_DSP_A_WIDTH` / `DEVICE_DSP_B_WIDTH` directly.
- ✅ Full MAT_CORE stack (11 files) compiles clean and
  `GEMM_systolic_top` + `glbl` elaborate successfully.

**Still open (deeper rework, future sprints)**:

- **PREPROCESS → INT8 path** must arrive at `GEMM_systolic_top` as a
  clean 8-bit INT8 stream, not a 27-bit BF16 mantissa. The low-8-bit
  truncation in `GEMM_systolic_top` is a placeholder until the
  PREPROCESS stage is ported to v002 (W4A8 explicit quantization).
- **Drain-every-1024 counter** in the GEMM instruction dispatcher so
  the packer's per-channel 21-bit accumulator never overflows its
  guard. Needs its own §2.2.c ticket.
- **Upstream HP0 / HP1 plumbing** — the new dual-lane dispatcher
  assumes HP0 feeds `IN_weight_upper` and HP1 feeds `IN_weight_lower`,
  pre-aligned. Weight streamer / DMA descriptors have to be updated to
  honor that pairing.
- `SYSTOLIC_TOTAL_LATENCY = 64` needs re-derivation for the v002
  pipeline (AREG=1 on weights, BREG=2 on activations, MREG=1, PREG=1
  per PE — slightly different than the v001 mantissa cascade).

### 2.3 GEMM_Array.svh duplication

`hw/rtl/MAT_CORE/GEMM_Array.svh` re-defines `ARRAY_SIZE_H` /
`ARRAY_SIZE_V` / `INT4_WIDTH` / `BFLOAT_WIDTH` that are already in
`npu_arch.svh`. This is legacy and should be demoted to a `` `include
"npu_arch.svh" `` pass-through or deleted once the downstream modules
stop referencing it.

### 2.4 Dual clock domains

Documented (AXI 250 / core 400) but not obviously visible from the
`rtl/` grep. CDC FIFOs presumably live in `MEM_control/` (not audited
in this pass). Flag for Phase A.3 — verify every async path has an XPM
CDC macro.

### 2.5 GEMV + SFU (2026-04-20, 후속 턴)

**Architecture claims confirmed**:

- `device_pkg::VecPipelineCnt = 4` → 4 µV-Core GEMV lanes. ✅
- `device_pkg::MatPipelineCnt = 1` → single Matrix Core. ✅
- `GEMV_reduction.sv`: Stage 1 DSP 32→16, Stages 2-5 LUT 16→8→4→2→1,
  total 5 pipeline stages. ✅ "32-MAC LUT pipeline + 5-stage reduction
  tree" matches the docs.
- `CVO_top.sv` instantiates exactly one `CVO_sfu_unit` + one
  `CVO_cordic_unit`. ✅ Single-SFU per NPU matches the 2026-04-20 doc
  audit.

**Compile-clean after this sprint**:

- Added missing `` `include "NUMBERS.svh" `` to `device_pkg.sv` and
  `` `include "kv260_device.svh" `` + `` `include "npu_arch.svh" `` to
  `mem_pkg.sv`. Packages now compile standalone.
- `GEMV_generate_lut.sv` — fixed typo `param.param.fixed_mant_width`
  → `param.fixed_mant_width`, and `OUT_fmap_low_LUT` → `OUT_fmap_LUT`
  (matches the port declaration).
- `GEMV_reduction.sv` — fixed the same double-`.param.` typo at the
  input port declaration.
- `GEMV_reduction_branch.sv` — the caller passed three named params
  (`fmap_cache_out_cnt`, `weight_type`, `line_cnt`) that don't exist on
  the `GEMV_reduction` interface. Replaced with `.param(param)` to
  match the struct-based signature.
- `CVO_cordic_unit.sv:180` — replaced the illegal variable-range
  part-select (`mag[leading-1:0]`) with a shift that SV permits.
- `CVO_top.sv` — moved the `is_cordic_op_wire` declaration above the
  SFU instance that gates on it.

**Still open (deferred — deeper semantic fixes)**:

- **`GEMV_top.sv:125/144` — unpacked→packed type mismatch**.
  `GEMV_reduction_branch` emits `OUT_GEMV_result_vector` as an
  unpacked array `[0:gemv_batch-1]`, but `GEMV_top` wires it into
  `OUT_final_fmap_{A..D}` declared as a packed scalar. Fix needs
  either (a) `OUT_final_fmap_*` arrays of `gemv_batch` elements per
  lane, or (b) a reduce in GEMV_reduction_branch that produces a
  single packed value. Semantics decision required.
- **`CVO_top.sv:79` — `bf16_add` symbol never defined**.
  `bf16_math_pkg` exports only `to_bf16` and `align_to_emax`. The
  CVO sub-emax path calls `bf16_add(x, ~e_max_sign, ...)` which
  never made it into the package. Needs a proper BF16 adder (exp
  alignment + mantissa add + renormalize) or a cheaper equivalent.
- The `GEMM_fmap_staggered_delay.sv` → `GEMV` branch wiring is still
  carrying the v001 BF16 mantissa assumption; v002 W4A8 path needs a
  clean INT8 datapath here too (separate from the MAT_CORE v002 work
  already landed).

## 3. Recommended Phase A sprint order

1. **Resolve §2.1** with the user. Docs vs. README conflict must
   settle before any RTL change.
2. **Write the DSP packer + sign-recovery** (§2.2) in isolation with a
   testbench — this is the biggest v002 delta and is independent of
   the array-shape decision.
3. **Clean up GEMM_Array.svh** (§2.3) so there is one source of truth
   for array dimensions.
4. **CDC audit** (§2.4) on AXI 250 ↔ core 400 boundaries.
5. **GEMV / SFU audit pass** (§2.5) so the 4-lane + single-SFU claim is
   grounded.

None of the Phase A items are currently blocked by Phase 0 external
actions. They can run in parallel with TRC approval / Vast.ai sign-up.
