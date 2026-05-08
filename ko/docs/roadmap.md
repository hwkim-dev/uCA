# 로드맵

상세 실행 보드는 [GitHub Projects][project]에서 관리한다. 이 페이지는
pccx 생태계 전체의 현재 릴리스 방향만 짧게 요약한다.

릴리스 cadence 는 공통 KV260 비트스트림 하니스 위에서 단계적으로
나뉜다. v002.0 은 베이스라인 통합, v002.1 은 동일 RTL 위에 sparsity
+ speculative decoding 스택을 얹는 단계, v003.x 는 새로운 아키텍처
novelty 가 등장하면서 별도 RTL 저장소로 옮겨가는 단계다. 또
하나의 평행 트랙 **vision-v001** 은 같은 KV260 기반 위에 CNN 계열
워크로드 (분류 / 검출) 를 얹으며, 자체 저장소를 가진다.

## Now — v002.0: KV260 베이스라인 통합

- `pccx-FPGA-NPU-LLM-kv260` 의 남은 RTL 통합 마무리
- v002.0 릴리스 라인의 A–F 베이스라인 단계
  - 진행 중: Phase 3 step 1 (shape constant RAM 통합,
    {doc}`v002/RTL/shape_const_ram` 참고) 및 Stage C 정리
    (카운터 / 상수 / `GLOBAL_CONST` 합치기)
- `pccx-lab` 기반 trace-driven verification
- Sail execute 증분 작업
- xsim / KV260 베이스라인 bring-up 로그 정리
- 릴리스 증거 체크리스트 (`pccx-FPGA-NPU-LLM-kv260` 의
  `docs/RELEASE_EVIDENCE_CHECKLIST.md`) 가 타이밍 / 처리량 /
  bring-up 표현이 이 문서 사이트에 등장하기 전 단계의 게이트 역할
- 이 릴리스 라인의 처리량은 측정만 (measured-only) — 검증 근거가
  공개되기 전까지 타이밍이나 처리량을 완료 상태로 표현하지 않음

```{figure} ../../_static/diagrams/v002_evidence_flow.svg
:name: fig-v002-evidence-flow-ko
:alt: pccx v002 릴리스 증거 흐름

RTL 소스 → xsim 테스트벤치 → synthesis / implementation →
KV260 bring-up `[HW]` → 런타임 `[HW]` → 릴리스 증거 체크리스트
(`RELEASE_EVIDENCE_CHECKLIST.md`) 가 태그 게이트 역할. 하드웨어
게이트 단계는 체크리스트가 게이트를 통과시킨 시점에만 이 문서
사이트에서 수치로 인용된다.
```

추적 이슈: [pccxai/pccx#28 — v0.2.0 umbrella][v020].

## Next — v002.1: sparsity + speculative decoding 스택

- 동일 RTL 저장소 (`pccx-FPGA-NPU-LLM-kv260`) 에서 v002.0 의 후속
- G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark 단계
- 20 tok/s 목표는 이 릴리스 라인 위에 위치
- EAGLE head 학습용 컴퓨트 예산: $70–100 (TRC TPU grant 가
  들어오면 $40)

## Later — v003.x: 별도 RTL 저장소 (LLM 라인 후속)

- v003+ 의 활성 RTL 개발은
  [`pccx-v003`](https://github.com/pccxai/pccx-v003) — 정본 v003
  IP-core 계획 패키지 — 에서 진행되며, 안정된 릴리스 브랜치는 아직
  없다 (이전 feeder
  [`pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003) 은
  superseded / retired)
- 이 문서 저장소는 v003 IP-core 패키지를 cross-link 하고 빌드 시
  `codes/v003/` 로 CI-clone 한다 — 현재
  `pccx-FPGA-NPU-LLM-kv260` 를 `codes/v002/` 로 CI-clone 하는 것과
  같은 방식
- v003.0 — Gemma 4 E4B 파운데이션 + 첫 아키텍처 novelty (planning); 처리량 TBD
- v003.1 — 두 번째 novelty + KV / 디코딩 co-design; 처리량 TBD
- 트랙 placeholder 인덱스: {doc}`v003/index`

## Parallel — vision-v001: KV260 위 CNN 추론 트랙

LLM 라인과는 별개로, **vision** 워크로드 전용 두 번째 제품 라인을
운영한다. 동일한 KV260 보드와 W4A8 NPU 기반을 공유하면서도 워크
로드 family 는 다르다. 활성 RTL 개발은 전용 저장소에서 진행된다.

- [`pccx-vision-v001`](https://github.com/pccxai/pccx-vision-v001)
- LLM 라인과 substrate 공유 — 같은 KV260 보드, 같은 W4A8
  weight × activation 비율, 같은 L2 URAM 구성
- 데이터플로우는 다름 — 토큰 단위 KV 스트리밍이 아니라 dense conv
  타일 재사용. GEMM systolic + GEMV 하이브리드는 conv 에 재사용
- 첫 모델 후보 — ResNet18 / YOLOv8n / MobileNetV3
  (footprint 가 가장 작은 변종 우선)
- 증거 자세 — 동일한 릴리스 증거 체크리스트가 타이밍 / 처리량 /
  bring-up 게이트 역할. FPS / mAP 수치는 게이트 통과 시점에만 이
  문서 사이트에 등장
- 트랙 placeholder 인덱스: {doc}`vision-v001/index`

## Family overview

```{figure} ../../_static/diagrams/pccx_family_tree.svg
:name: fig-pccx-family-tree-ko
:alt: pccx 제품군 트리 — 버전과 트랙별 분기

v001 (archived) → v002 (활성 KV260 LLM 라인: v002.0 → v002.1) →
v003.x (LLM 라인 후속, 별도 RTL 저장소). **vision-v001** 트랙은
v002 KV260 substrate 에서 분기되어 자체 저장소에서 평행하게
진행된다. 노드에 hover 하면 상태와 범위가 표시된다.
```

## 링크

- GitHub Project (source of truth): <https://github.com/orgs/pccxai/projects/1>
- v0.2.0 umbrella: <https://github.com/pccxai/pccx/issues/28>

[project]: https://github.com/orgs/pccxai/projects/1
[v020]: https://github.com/pccxai/pccx/issues/28
