---
orphan: true
---

# Milestones

현재 진행 상태를 기준으로 정리한 milestone 목록이다. 임의의 일정 예측,
성능 목표, 시장성 수치는 넣지 않는다. 미래 단계는 TBD로 남겨두고,
진척을 가로막는 증빙 게이트를 함께 표기한다.

## Done

- **v002 LLM IP-core extraction**
  KV260 board integration 저장소에서 재사용 가능한 LLM RTL, 공통 패키지,
  testbench, formal Sail harness를 분리해 `pccxai/pccx-v002` 패키지로 전환하고,
  board integration 저장소에서 pinned submodule로 사용하게 했다.
  Sail typecheck workflow는 IP-core 레이어로 이전했고,
  fresh-clone 도달성도 점검했다.

- **Repository topology와 boundary rule 정합성 정리**
  [`docs/reference/repo-topology.md`](../reference/repo-topology.md),
  [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md) 정합

- **v002 contract scaffold 발행**
  [`docs/reference/v002-contract.md`](../reference/v002-contract.md) 공개.
  다수 항목은 evidence 대기(TBD)이며, 구조 자체는 완료.

## In progress

- **v002 baseline 기준 KV260 timing closure**
  합성 시도는 완료되었으나 완전한 timing closure 보고는 다음 gate를 기다린다.

- **W4A8 golden-vector gate**
  현재 smoke vector만 존재하고, full fixture 세트는 별도 항목에서 TBD.
  기준 문서는 `pccx-FPGA-NPU-LLM-kv260/docs/W4A8_GOLDEN_VECTOR_GATE.md`.

- **v003 IP-core planning**
  `pccxai/pccx-v003`가 canonical planning 패키지.
  선행 feeder `pccxai/pccx-LLM-v003`는 retired 상태이며,
  재사용 가능한 v003 LLM 산출물은 `pccx-v003/LLM/`에 둔다.

## Next (gated, no dates)

- **`pccx-v002/Vision/` 흡수**
  `pccxai/pccx-vision-v001`와의 compatibility review 후 진행.
  흡수가 성립되면 흡수, 아니면 standalone/다음 단계로 이동.
- **`pccx-v003` contract freeze**
  외부 consumer가 pin을 걸 수 있을 정도로 계약이 안정화되어야 한다.
  조건 미충족 시 planning+evidence-gated 상태 유지.
- **Voice domain population**
  `pccx-v002/Voice/`은 현재 placeholder 디렉터리.
  Voice contract 확정 후에만 실제 산출물 채택.

## Future (no commitments)

- **ASIC / MPW 탐색**
  현재 범위를 벗어난 장기 방향성. 일정·실물 silicon 경로는 확정하지 않는다.
- **KV260 외 board 확장**
  최소한 두 번째 board에서 IP-core가 반복 동작해야 다음 단계를 검토한다.
  아직 대상을 확정하지 않는다.

## 본 문서가 아닌 것

- release schedule이 아니다. quarter 라벨이나 달력 일정은 없다.
- 마케팅 roadmap이 아니다. 고객 대상 약속 문구를 넣지 않는다.
- 인력 계획이 아니다. headcount 및 조직 구조는 저장소 외부에서 관리한다.
