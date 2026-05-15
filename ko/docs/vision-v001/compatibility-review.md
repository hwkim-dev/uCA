---
orphan: true
---

# vision-v001 compatibility review (template)

> Draft / planning. 현재는 vision RTL이 존재하지 않으며, 이 페이지는
> 향후 review 템플릿이다.

## 목적

vision 라인을 `pccx-v002/Vision/`로 흡수할지, standalone으로 둘지 판단할 때
공개된 v002 contract 기준으로 구조화된 검토를 수행한다.

## Review axis

| 축 | 확인 항목 | v002 참고 |
| --- | --- | --- |
| 공통 RTL substrate | vision용 packages/interfaces/wrappers가 `pccx-v002/common/rtl/`와 호환되는지 | `pccx-v002/common/rtl/{packages, interfaces, wrappers}/` |
| ISA | vision에서 추가 opcode나 operand encoding이 필요한지 | `pccx-v002/LLM/rtl/packages/isa/` |
| Register ABI | vision이 LLM register layout을 그대로 쓰는지, 별도 map가 필요한지 | `pccx-v002/compatibility/register_map.yaml` |
| Memory map | vision L1/L2/HP 트래픽이 v002 memory layout에 맞는지 | `pccx-v002/compatibility/memory_map.yaml` |
| Control bus | AXI-Lite 형식이 동일한지 | `pccx-v002/compatibility/top_interface.yaml` |
| Quantization / precision | W4A8 공통 사용 여부, 혹은 vision 전용(INT8 등) 형식 필요성 | `pccx-v002/LLM/rtl/core/preprocess/` |
| Driver ABI | 같은 driver 형식을 쓰는지, vision 전용 runtime이 필요한지 | `pccx-v002/compatibility/v002-contract.yaml` (`driver_abi_version`) |
| Verification | v002 sim wrapper가 vision testbench까지 확장 가능한지 | `pccx-v002/LLM/sim/run_verification.sh` |
| Boundary token | vision IP-core 경로에 model/board token가 노출되는지 | `pccx-v002/scripts/check_repo_boundary.sh` |

## review가 실행될 때 필요한 산출물

- `pccx-vision-v001`의 모든 파일을 `rtl`, `tests`, `docs`, `scripts` 단위로
  IP-core/ spec/ model-specific으로 분류
- `pccx-v002/common/rtl/` 대비 diff로 모듈 중복/충돌 항목 추출
- Sail/formal 호환성 검토 메모
- 최종 결정 한 가지: **absorb / hold standalone / fork to pccx-vision-v003**

## 이 페이지가 말하는 바

- 완료된 검토 결과가 아니다.
- 적합/부적합을 선결정하지 않는다.
- FPS, mAP, throughput, latency 같은 성능 수치를 claims하지 않는다.

## tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
