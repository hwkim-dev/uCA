---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> 실무 적용 전에는 qualified legal review가 선행되어야 한다.
> 한국은 선출원주의가 적용되므로 후보 발명 공개 전 변리사 검토가 필요하다.

# Trade secret policy

Trade secret는 노출되면 보호가 사라지므로, 비밀 유지가 핵심인 자산을 대상으로 한다.
반대로 공개가 되면 public disclosure이 되어 patent과 trade secret의 성질이 나뉜다.

## trade secret 대상

| 카테고리 | trade secret 처리 이유 |
| --- | --- |
| **PCCX ProCore RTL bundles** | 공개되면 경쟁 우위를 잃을 수 있는 hardened RTL. OpenCore는 architectural baseline만 공개하며, ProCore는 상업 계약 아래에서 강화 기능을 제공한다. |
| **Enterprise compiler backend** | 상업 고객을 대상으로 하는 IP-core instruction stream 전용 backend. reference frontend 및 공개형 interface는 trade secret이 아니며, 폐쇄형 backend만 해당한다. |
| **Timing / PPA scripts** | 실제 실리콘에서 power/performance/area trade-off를 만들었던 누적 튜닝 스크립트. 공개형 OpenCore에는 포함되지 않는다. |
| **Customer-specific optimizations** | 특정 고객 계약 하에 제공되는 최적화 작업. 계약 조건이 추가 통제한다. |

## trade secret이 아닌 항목

- 프로젝트 공개 저장소에서 라이선스 하에 공개된 산출물
  (`pccx`, `pccx-v00N`, application 통합 저장소)은 더 이상 trade secret이 아니다.
- Architectural spec, ISA reference, register/memory map, 공개 문서.
- sim wrapper, evidence pack index, fresh-clone reachability와 같은 공개 검증 참고 흐름.

## 접근 통제

- trade secret 자료는 공개 저장소 외부에서 분리 관리한다.
- 접근은 문서화된 기밀 의무를 통해 역할별로 허가한다.
  - 평가자: NDA
  - 직원: 근로/고용 계약
  - 고객: 상용 트랙 계약
- 접근 기록과 승인 기록은 primary entity에서 보관한다.

## Open track과의 경계

Open-track 기여자는 open-track 산출물만 다루며, trade secret는 별도 트랙으로 분리한다.
경계를 넘으려면 사전의 confidentiality agreement가 필요하다.

## Patent 전략과의 경계

후보 발명은 `patent candidate`와 `trade secret candidate` 중 하나만 가능하다.
patent filing은 비밀성을 깨뜨리고, trade secret 보호는 공개를 막는다.
최종 선택은 [patent strategy](patent-strategy.md)에서 관리한다.

## 상태

구체적인 trade secret 항목, 접근 목록, 보관 기록은 공개 문서에 열거하지 않고
별도 내부 통제에서 관리한다.
