---
orphan: true
---

# v002 docs literalinclude migration to pccx-v002

PCCX 문서 사이트는 빌드 시점에 sibling RTL 저장소를 `codes/v002/`로 clone한다.
2026년 5월 구조 개편 Phase H에서 v002 IP-core가 extraction되면서,
재사용 RTL이 `pccxai/pccx-FPGA-NPU-LLM-kv260`(보드 통합 저장소)에서
신규 패키지 `pccxai/pccx-v002`로 이동했다.

이 페이지는 경로 drift를 워크플로 diff가 아니라 문서 이력에서 확인할 수 있도록
기록한다.

## 이전

| 항목 | 값 |
| --- | --- |
| Source | `https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260` |
| Ref | `18d4631f54721684ef6747bc37cf8538653a7a9e` (v002 extraction 직전의 마지막 main commit) |
| Layout | KV260 tree의 `hw/rtl/`, `hw/sim/`, `hw/vivado/` |

## 이후

| 항목 | 값 |
| --- | --- |
| Source | `https://github.com/pccxai/pccx-v002` |
| Ref | `main` |
| Layout | reusable IP-core 패키지 구조: `LLM/rtl/...`, `common/rtl/...`, `LLM/scripts/...`, `LLM/sim/...`, `LLM/tb/...`, `LLM/formal/...` |

(`pccx-v002/SOURCE_MANIFEST.md`) 기준으로 정리된 전체 경로 전환표가 존재한다.

## path mapping (`docs/v002/` 관련 핵심 항목)

`docs/v002/RTL/`, `docs/v002/Build/`의 literalinclude는 아래 매핑을 사용한다.

| 이전 경로 | 변경 경로 |
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

## pccx-v002에 1:1 대응이 없는 항목

- `hw/vivado/npu_core_wrapper.sv`
  board 패키징 관련 로직을 포함하므로 보드 통합 저장소(KV260)에서만 관리한다.
  따라서 [`docs/v002/Build/index.md`](../Build/index.md)에서는 literalinclude 대상에서 제외하고
  보드 저장소를 가리키도록 문서를 수정했다.

## 단일 PR로 처리해야 하는 이유

`RTL_REPO_URL`을 `pccx-v002/main`으로 바꿨는데 문서 경로가 kv260로 남아 있거나,
반대로 경로는 전환했는데 워크플로가 오래된 SHA를 유지하면 모두 strict build가 즉시 깨진다.
두 변경은 반드시 함께 반영한다.

## hard-rule

- `git push --force` / `--force-with-lease` 사용 금지
- 태그 푸시 금지
- staging push 금지
- PCCX®/상표 등록주장, private filing 상세 노출 금지
- 하드웨어, runtime, timing, bitstream, 생산성 주장은 이 PR 대상이 아니다(문서 정합성 개선만 수행)
