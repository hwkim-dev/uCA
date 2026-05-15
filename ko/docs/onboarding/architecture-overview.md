---
orphan: true
---

# 아키텍처 개요

프로젝트를 처음 보는 사람이 단계적으로 읽을 수 있도록 한눈에 정리한 문서다.
권한 있는 기준은 아래 페이지에서 확인한다.

## 읽기 순서

1. 프로젝트 소개: `pccx` 루트와 topology 개요.
2. 저장소 구성: [`docs/reference/repo-topology.md`](../reference/repo-topology.md).
3. `v002` 계약 의미: [`docs/reference/v002-contract.md`](../reference/v002-contract.md)와
   `pccx-v002/SOURCE_MANIFEST.md`.
4. 경계 규칙: [`docs/reference/boundary-rule.md`](../reference/boundary-rule.md).
5. 검증 흐름: [`docs/reference/testing-protocol.md`](../reference/testing-protocol.md).
6. submodule pin 구조: [`docs/reference/submodule-pin-policy.md`](../reference/submodule-pin-policy.md).

## 한 문단 요약

`pccx`는 공개 문서와 사양을 운영하고, `pccx-v00N`은 재사용 가능한
버전형 IP-core 패키지를 제공한다. 보드 통합 저장소(현재 기준 `pccx-FPGA-NPU-LLM-kv260`)
는 고정된 SHA로 `pccx-v00N`을 pin 받아 소비하며, 보드 제약/하드웨어 파일을
담당한다.
모델 계열은 매니페스트와 runtime 코드로 바인딩되며, IP-core 경로에는
특정 모델명·보드명이 들어가지 않는다.

## 제외 범위

ISA 상세, 레지스터 맵, 메모리 맵, quantization 스키마 등 기술 본문은
`docs/v002/`로 이동한다. 이 페이지는 탐색과 진입 순서를 제공하는 목적으로만 사용한다.
