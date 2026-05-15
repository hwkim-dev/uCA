---
orphan: true
---

# PCCX v003 — overview

> Draft / planning / evidence-gated. PCCX™ v003은 아키텍처 라인 설계 문서이며
> 공개된 릴리스 패키지가 아니다.

v003은 v002 이후의 다음 아키텍처 세대로, 현재는 planning과 contract drafting이
주요 범위다. 검증된 RTL과 고정된 contract가 나오기 전까지 public scope는
계획 수립과 정합성 유지이다.

## v003의 대상 범위

- **LLM**: v002 baseline을 넘어서는 워크로드(예: spatial decode, Eagle-3,
  MoE, longer context)를 포함. Gemma 4 E4B 및 유사 transformer workloads.
- **Vision / Voice / common**: v002의 도메인 구조(`LLM/`, `Vision/`, `Voice/`,
  `common/`, `compatibility/`, `docs/`, `tests/`, `scripts/`)를
  contract 안정 시점에 맞춰 확장 적용.
- **Compatibility contract**: v002와 다른 공개 contract가 필요하며,
  v003 발행 시 소비자가 특정 v003 SHA를 pin해야 한다.

## 현재 상태 (planning only)

- v003 canonical 패키지 저장소는
  [`pccxai/pccx-v003`](https://github.com/pccxai/pccx-v003)이다.
  현재 구조는 v002를 그대로 반영하며(`LLM/`, `Vision/`, `Voice/`, `common/`,
  `compatibility/`, `docs/`, `tests/`, `scripts/`) planning의 기준점이 된다.
- 과거 `pccxai/pccx-LLM-v003`는 feeder 역할로 쓰이다가 retired 되었고,
  더 이상 active public track이 아니다. 재사용 LLM 산출물은 `pccx-v003/LLM/`로 이관해야 한다.
- consolidation direction은 [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)에 추적한다.
- 현재 v003 RTL, sim wrapper, formal harness, board integration, contract은 공개되지 않았다.

## 정합성 참조

- v002 IP-core package(배포 완료): [`pccxai/pccx-v002`](https://github.com/pccxai/pccx-v002)
- v003 IP-core planning package(계획 단계): [`pccxai/pccx-v003`](https://github.com/pccxai/pccx-v003)
- 종료된 v003 feeder: [`pccxai/pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003)
- tracker: [`pccxai/pccx#64`](https://github.com/pccxai/pccx/issues/64)
- canonical docs: <https://pccx.ai/en/>
