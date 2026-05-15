---
orphan: true
---

# 개발자 레퍼런스

PCCX 각 저장소의 역할, 계약 필드, 검증 흐름을 정확히 맞추기 위한 기준 문서군이다.
온보딩 개요가 아니라 개발자가 현재 상태를 확인할 수 있는 규격 문서이다.

## 구성

- [Repository topology](repo-topology.md) — 저장소 역할 분리와 소유권 기준
- [v002 contract narrative](v002-contract.md) — `compatibility/v002-contract.yaml` 항목 해설
- [Boundary rule](boundary-rule.md) — 모델·보드·IP-core·스펙의 분류 규칙
- [Testing protocol](testing-protocol.md) — Sail typecheck, sim wrapper, fresh-clone 점검
- [Submodule pin policy](submodule-pin-policy.md) — pin 도달성 규칙과 갱신 절차

## 갱신 규칙

저장소 경계, 계약 필드, 검증 흐름, pin 정책이 변경되면 본 레퍼런스셋을
즉시 갱신한다. 제안·로드맵 내용은 `docs/roadmap/`에서 관리한다.
