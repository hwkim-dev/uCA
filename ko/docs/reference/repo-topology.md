---
orphan: true
---

# Repository topology

PCCX는 문서 기준 저장소, 버전별 IP-core 패키지 저장소, 보드 통합 저장소로
구성된다. model과 board는 모두 IP-core 패키지를 소비하지만, 패키지 내부에는
특정 model명이나 board명이 `rtl/`, `compatibility/` 경로에 노출되지 않는다.

## 활성 저장소

| Repository | 역할 |
| --- | --- |
| `pccxai/pccx` | 정본 spec, 공개 문서 사이트, 프로젝트 인덱스 |
| `pccxai/pccx-v002` | v002 IP-core 패키지. LLM과 공유 서브시스템을 model/board 무관하게 재사용한다. Vision·Voice 도메인은 해당 트랙이 통합될 때까지 placeholder 디렉터리로 유지 |
| `pccxai/pccx-v003` | v003 IP-core 계획 패키지. v002와 동일한 구조(`LLM`, `Vision`, `Voice`, `common`, `compatibility`, `docs`, `tests`, `scripts`). 계약이 확정될 때까지 evidence-gated 상태 |
| `pccxai/pccx-vision-v001` | v002 KV260 위에 얹히기 전 vision 라인을 실험/조율하는 독립 저장소 |
| `pccxai/pccx-FPGA-NPU-LLM-kv260` | KV260 + LLM application 통합. `third_party/pccx-v002`를 서브모듈로 pin 하여 v002 패키지를 사용 |

## 과거 / 종료 저장소

| Repository | 역할 |
| --- | --- |
| `pccxai/pccx-LLM-v003` | v003 초기 실험을 위한 과거 임시 feeder. 현재는 `pccxai/pccx-v003`로 대체되어 더 이상 활성 public track으로 사용하지 않는다. |

## 배치 규칙

| 콘텐츠 | 저장소 |
| --- | --- |
| Architecture spec, ISA, register/memory map, 공개 문서 | `pccx` |
| 재사용 RTL, 패키지, 인터페이스, wrapper, testbench, formal harness | `pccx-v00N` |
| Board constraints, Vivado 프로젝트 파일, board-top wrapper, PS/PL wiring | Board integration repo (예: `pccx-FPGA-NPU-LLM-kv260`) |
| Model manifest, application runtime 코드, driver HAL, board 실행 evidence | application 통합 저장소 (현재는 board 통합 저장소와 동일) |

## 불변 규칙

> Model과 board는 IP-core를 소비한다. IP-core는 `rtl/`, `compatibility/`,
> `formal/` 경로에서 특정 model명 또는 board명을 넣지 않는다.

Application 저장소는 IP-core RTL의 두 번째 사본을 보유하지 않는다.
최신 `pccx-v002/main`에서 도달 가능한 pin SHA를 통해 소비한다.
