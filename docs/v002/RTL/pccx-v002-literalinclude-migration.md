---
orphan: true
---

# v002 docs literalinclude migration to pccx-v002

The PCCX documentation site clones a sibling RTL repository at build
time into `codes/v002/`. After the v002 IP-core extraction (Phase H
of the May 2026 restructure), the reusable RTL moved from
`pccxai/pccx-FPGA-NPU-LLM-kv260` (board integration repo) into the
new IP-core package
[`pccxai/pccx-v002`](https://github.com/pccxai/pccx-v002).

This page records the migration so the file path drift is visible
in the docs history rather than buried in workflow diffs.

## Before

| Item | Value |
| --- | --- |
| Source | `https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260` |
| Ref | `18d4631f54721684ef6747bc37cf8538653a7a9e` (last main commit before the v002 extraction) |
| Layout | KV260 in-tree `hw/rtl/`, `hw/sim/`, `hw/vivado/` directories |

## After

| Item | Value |
| --- | --- |
| Source | `https://github.com/pccxai/pccx-v002` |
| Ref | `main` |
| Layout | reusable IP-core package: `LLM/rtl/...`, `common/rtl/...`, `LLM/scripts/...`, `LLM/sim/...`, `LLM/tb/...`, `LLM/formal/...` per [`pccx-v002/SOURCE_MANIFEST.md`](https://github.com/pccxai/pccx-v002/blob/main/SOURCE_MANIFEST.md) |

## Path mapping (subset relevant to `docs/v002/`)

The full kv260→pccx-v002 path mapping lives in
`pccx-v002/SOURCE_MANIFEST.md`. The mappings consumed by
`docs/v002/RTL/` and `docs/v002/Build/` literalincludes are:

| Old path | New path |
| --- | --- |
| `hw/rtl/CVO_CORE/CVO_top.sv` | `LLM/rtl/core/cvo/CVO_top.sv` |
| `hw/rtl/MAT_CORE/GEMM_dsp_unit.sv` | `LLM/rtl/core/mat/GEMM_dsp_unit.sv` |
| `hw/rtl/MAT_CORE/GEMM_systolic_top.sv` | `LLM/rtl/core/mat/GEMM_systolic_top.sv` |
| `hw/rtl/NPU_Controller/Global_Scheduler.sv` | `LLM/rtl/core/controller/Global_Scheduler.sv` |
| `hw/rtl/NPU_Controller/npu_controller_top.sv` | `LLM/rtl/core/controller/npu_controller_top.sv` |
| `hw/rtl/NPU_Controller/NPU_Control_Unit/ctrl_npu_decoder.sv` | `LLM/rtl/core/controller/ctrl_npu_decoder.sv` |
| `hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_pkg.sv` | `LLM/rtl/packages/isa/isa_pkg.sv` |
| `hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_x64.svh` | `LLM/rtl/packages/isa/isa_x64.svh` |
| `hw/rtl/NPU_top.sv` | `LLM/rtl/top/pccx_npu_top.sv` |
| `hw/rtl/VEC_CORE/GEMV_top.sv` | `LLM/rtl/core/vec/GEMV_top.sv` |
| `hw/rtl/PREPROCESS/preprocess_fmap.sv` | `LLM/rtl/core/preprocess/preprocess_fmap.sv` |
| `hw/rtl/PREPROCESS/preprocess_bf16_fixed_pipeline.sv` | `LLM/rtl/core/preprocess/preprocess_bf16_fixed_pipeline.sv` |
| `hw/rtl/PREPROCESS/fmap_cache.sv` | `LLM/rtl/core/preprocess/fmap_cache.sv` |
| `hw/rtl/NPU_Controller/NPU_frontend/AXIL_CMD_IN.sv` | `LLM/rtl/core/controller/AXIL_CMD_IN.sv` |
| `hw/rtl/NPU_Controller/NPU_frontend/AXIL_STAT_OUT.sv` | `LLM/rtl/core/controller/AXIL_STAT_OUT.sv` |
| `hw/rtl/NPU_Controller/NPU_frontend/ctrl_npu_frontend.sv` | `LLM/rtl/core/controller/ctrl_npu_frontend.sv` |
| `hw/rtl/NPU_Controller/npu_interfaces.svh` | `common/rtl/interfaces/npu_interfaces.svh` |
| `hw/rtl/MEM_control/memory/mem_GLOBAL_cache.sv` | `LLM/rtl/core/memory/mem_GLOBAL_cache.sv` |
| `hw/rtl/MEM_control/memory/Constant_Memory/shape_const_ram.sv` | `LLM/rtl/core/memory/Constant_Memory/shape_const_ram.sv` |
| `hw/rtl/Constants/compilePriority_Order/B_device_pkg/device_pkg.sv` | `common/rtl/packages/device_pkg.sv` |
| `hw/rtl/Library/Algorithms/Algorithms.sv` | `common/rtl/packages/Algorithms.sv` |
| `hw/rtl/Library/Algorithms/BF16_math.sv` | `common/rtl/packages/BF16_math.sv` |
| `hw/rtl/Library/Algorithms/QUEUE/IF_queue.sv` | `common/rtl/interfaces/IF_queue.sv` |
| `hw/vivado/filelist.f` | `LLM/scripts/filelist.f` |

## Items without a 1:1 counterpart in pccx-v002

- `hw/vivado/npu_core_wrapper.sv` — the Vivado IP-packaging wrapper
  remains in the board integration repository (KV260) because it
  encodes board-side packaging concerns. The corresponding section
  in [`docs/v002/Build/index.md`](../Build/index.md) was rewritten
  to point at the board integration repo rather than embed the file
  literally.

## Why a single PR

Flipping `RTL_REPO_URL` to `pccx-v002/main` while the docs still
reference kv260 paths breaks every Sphinx strict build immediately.
Flipping the docs paths first while the workflow still pins the old
kv260 SHA breaks every Sphinx strict build immediately. The two
changes ship together so there is no half-state.

## Hard-rule confirmation

- No `git push --force` or `--force-with-lease`.
- No tags pushed.
- No staging push.
- No registered-mark claim, no private
  trademark filings exposed.
- No hardware/runtime/timing/bitstream claim is made by this PR;
  it is documentation-only.
