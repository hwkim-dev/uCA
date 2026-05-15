---
orphan: true
---

# v003 repository boundary (planning)

> Draft / planning / evidence-gated. 공개된 v003 RTL 없음.

## 오늘의 정리

- `pccxai/pccx-v003`
  v003 IP-core planning 패키지의 canonical repo이다.
  현재 `LLM/`, `Vision/`, `Voice/`, `common/`, `compatibility/`,
  `docs/`, `tests/`, `scripts/` 구조를 v002 방식으로 mirror 한다.
  planning/evidence-gated 상태이므로 공개된 v003 RTL과 contract는 없다.
- `pccxai/pccx-LLM-v003`
  과거 초기 v003 LLM planning feeder. 이제 retired 상태이며 현재 active public track이 아니다.
  재사용 가능한 LLM material은 `pccx-v003/LLM/`로 이동한다.

## 기본 배치 방향 (issue [#64](https://github.com/pccxai/pccx/issues/64))

| 레이어 | 활성 위치 |
| --- | --- |
| LLM RTL / sim / tb / formal | `pccxai/pccx-v003/LLM/...` (v002 layout을 기반으로 mirror) |
| Vision RTL | `pccxai/pccx-v003/Vision/...` (v003 Vision substrate가 정해지면) |
| Voice RTL | `pccxai/pccx-v003/Voice/...` (v003 Voice substrate가 정해지면) |
| 공통 패키지 / 인터페이스 / wrapper | `pccxai/pccx-v003/common/rtl/...` |
| Compatibility contract | `pccxai/pccx-v003/compatibility/v003-contract.yaml` |
| Build scripts, sail harness, tests | `pccxai/pccx-v003/{scripts, formal, tests, docs}/` |

## boundary rule

v003 IP-core 패키지는 v002와 동일한 boundary rule을 따른다.

- model과 board가 IP core를 소비한다.
- IP core의 `rtl/`, `compatibility/`, `formal/` 경로에는 특정 model명이나 board명을 넣지 않는다.
- application 저장소(board / model 통합)는 `pccx-v003/main`에서 도달 가능한 SHA를 pin한다.
- canonical 규칙은 [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md) 참고.

## migration sequence (planned)

1. retired된 `pccx-LLM-v003` material을 분류해 v003 패키지로 재도입할 항목만 추출
2. `compatibility/v003-contract.yaml`을 v002 구조와 맞춰 placeholder 상태로 먼저 정의
3. board/model 통합 이전, PR 단위로 `pccx-v003/LLM/` 재도입
4. contract 안정 이후 board/application 저장소가 v003 SHA로 pin

no timing, runtime, FPS/mAP, bitstream, production-readiness claim는 이 문서에서 하지 않는다.
