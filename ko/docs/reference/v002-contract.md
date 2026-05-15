---
orphan: true
---

# v002 contract narrative

v002 IP-core 패키지는 `pccx-v002/compatibility/v002-contract.yaml`에서
consumer-facing contract를 선언한다. 이 페이지는 각 필드의 의미와
TBD 슬롯을 채우기 위한 evidence 기준을 설명한다.

## Fixed fields

현재 아래 필드는 고정값이 확정돼 있다.

| Field | Value | 의미 |
| --- | --- | --- |
| `arch` | `pccx-v002` | 모든 consumer가 공유하는 architecture 식별자 |
| `package_repo` | `pccx-v002` | 패키지 발행 저장소 이름 |
| `domains` | `LLM`, `Vision`, `Voice` | `pccx-v002` 루트의 domain 디렉터리. Vision/Voice는 해당 트랙 흡수 전까지 placeholder |
| `model_specific` | `false` | IP-core는 특정 모델 정체성을 인코딩하지 않는다 |
| `board_specific` | `false` | IP-core는 특정 board 정체성을 인코딩하지 않는다 |
| `known_application_repos` | `pccx-FPGA-NPU-LLM-kv260` | 현재 패키지를 소비하는 application 저장소 |

## TBD fields

TBD 항목은 yaml에 슬롯이 미리 정해져 있어 consumer가 매번 스키마를 추측하지 않아도 된다.

| Field | 담을 값 | 필요 evidence |
| --- | --- | --- |
| `isa_version` | 고정 ISA revision (`0.2.0` 등) | `pccx/docs/v002/ISA/`의 frozen 문서 + 해당 revision Sail typecheck 통과 |
| `register_abi_version` | MMIO register ABI revision | `compatibility/register_map.yaml` freeze + 문서화된 레지스터 검증 harness 통과 |
| `driver_abi_version` | driver ABI revision(구조체 layout, 호출 규약) | freeze된 driver ABI 문서 + 실제 application 빌드 결과 |
| `top_interface_version` | top port revision | 실제 `pccx_v002` top module 포트를 반영한 `compatibility/top_interface.yaml` |
| `weight_format` | quantized weight format 식별자 (`W4`) | reference pack routine + 1개 이상의 round-trip golden vector |
| `activation_format` | activation format 식별자 (`INT8`) | reference quantization routine + 1개 이상의 round-trip golden vector |
| `nonlinear_precision` | nonlinear 경로의 근사 전략 및 precision 목표 | protocol 문서 + RTL 가시값을 비교할 수 있는 reference Python |
| `control_bus` | control transport 식별자 (`axi-lite`) | freeze된 control bus spec + 해당 버스를 구동하는 동작 application |

## 업데이트 규칙

TBD에서 실제 값으로 승격하려면, 이 저장소(또는 연계 저장소)에 schema 슬롯과
필요 evidence가 모두 함께 존재해야 한다.
검증이 준비되기 전에 값만 올리는 변경은 모든 consumer의 재-pin 및 재검증을
강제한다.

## 참고

- `pccx-v002/compatibility/v002-contract.yaml` — 현재 계약 본문
- `pccx-v002/compatibility/register_map.yaml`, `memory_map.yaml`, `top_interface.yaml` — 본 문서가 참조하는 supporting 파일
