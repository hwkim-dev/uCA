---
orphan: true
---

# Boundary rule

프로젝트의 산출물은 반드시 네 분류 중 정확히 하나에만 배치한다.
새 파일은 최종 반영 전에 아래 분류 절차를 거친다.

## 네 분류

| 분류 | 소유 저장소 | 예시 |
| --- | --- | --- |
| **Spec / documentation** | `pccx` | Architecture overview, ISA reference, register/memory map 문서, project roadmap, 공개 논문 |
| **IP-core (versioned package)** | `pccx-v00N` | 재사용 가능한 RTL, 공통 패키지, 인터페이스, wrapper, testbench, formal harness, compatibility manifest |
| **Board integration** | 보드 통합 저장소 (예: `pccx-FPGA-NPU-LLM-kv260`) | board constraints(`.xdc`), Vivado 프로젝트 파일, board-top wrapper, PS/PL 배선, 보드 bring-up runbook |
| **Model / application integration** | Application integration repo (현재는 보드 통합 저장소와 동일, 추후 보드가 없는 모델 저장소가 생기면 분리) | Model manifest, runtime driver, application 코드, 보드 실행 evidence |

## IP-core 경로의 네이밍 금지어

`pccx-v00N/rtl/`, `pccx-v00N/compatibility/`, `pccx-v00N/formal/`에서는
README 또는 compatibility 문서에서 소비자 관점(`consumer`)을 명확히 설명하는
경우를 제외하고 아래 토큰을 사용하지 않는다.

```text
gemma  gemma3n  gemma4  llama  qwen  mistral  e4b
kv260  kria  zcu104  alveo  versal
```

`pccx-v002/scripts/check_repo_boundary.sh`는 `pccx-v002`로의 push마다 이
검증 규칙을 적용한다.

## 신규 파일 분류 절차

1. 파일이 architecture의 정체성(architecture 자체, ISA, 문서, 공개 roadmap)을
   설명하면 `pccx`.
2. 파일이 architecture의 구성 요소(RTL, package, contract field, formal model, testbench)를
   설명하면 `pccx-v00N`이며 commit 전 네이밍 금지어를 점검한다.
3. 파일이 특정 *board*의 부팅, timing closure, PS/PL 배선 실행법을 다루면
   board 통합 저장소.
4. 파일이 특정 *model*의 실행 방식, driver 동작, application의 IP-core 결합 방법을 다루면
   application integration 저장소.

## 경계가 애매한 경우

파일이 두 분류에 모두 자연스럽게 걸릴 때(예: board-specific bring-up runbook이
architecture feature도 함께 설명하는 경우)는 더 구체적인 레이어로 옮긴다.
우선순위는 `board > application > IP-core > spec`이다.
경계를 넘는 문서 복제는 오히려 오류를 키운다. 대신 추상 레이어로
크로스 링크를 유지한다.
