# 로드맵

상세 실행 보드는 [GitHub Projects][project]에서 관리한다. 이 페이지는
pccx 생태계 전체의 현재 릴리스 방향만 짧게 요약한다.

릴리스 cadence 는 공통 KV260 비트스트림 하니스 위에서 단계적으로
나뉜다. v002.0 은 베이스라인 통합, v002.1 은 동일 RTL 위에 sparsity
+ speculative decoding 스택을 얹는 단계다.

## Now — v002.0: KV260 베이스라인 통합

- `pccx-FPGA-NPU-LLM-kv260` 의 남은 RTL 통합 마무리
- v002.0 릴리스 라인의 A–F 베이스라인 단계
- `pccx-lab` 기반 trace-driven verification
- Sail execute 증분 작업
- xsim / KV260 베이스라인 bring-up 로그 정리
- 이 릴리스 라인의 처리량은 측정만 (measured-only) — 검증 근거가
  공개되기 전까지 타이밍이나 처리량을 완료 상태로 표현하지 않음

추적 이슈: [pccxai/pccx#28 — v0.2.0 umbrella][v020].

## Next — v002.1: sparsity + speculative decoding 스택

- 동일 RTL 저장소 (`pccx-FPGA-NPU-LLM-kv260`) 에서 v002.0 의 후속
- G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark 단계
- 20 tok/s 목표는 이 릴리스 라인 위에 위치
- EAGLE head 학습용 컴퓨트 예산: $70–100 (TRC TPU grant 가
  들어오면 $40)

## 링크

- GitHub Project (source of truth): <https://github.com/orgs/pccxai/projects/1>
- v0.2.0 umbrella: <https://github.com/pccxai/pccx/issues/28>

[project]: https://github.com/orgs/pccxai/projects/1
[v020]: https://github.com/pccxai/pccx/issues/28
