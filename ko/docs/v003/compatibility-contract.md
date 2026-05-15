---
orphan: true
---

# v003 compatibility contract (planning)

> Draft / planning / evidence-gated. 현재는 v003 frozen contract가 없다.

v003 계약은 공개되면 v002 계약 구조를 그대로 따른다.
목표 위치는 다음과 같다.

```
pccxai/pccx-v003/compatibility/v003-contract.yaml
```

계획/증빙 게이트 상태의 canonical 패키지는
[`pccxai/pccx-v003`](https://github.com/pccxai/pccx-v003)이며,
v003 frozen contract는 아직 공개되지 않았다.
통합 방향은 [repository boundary](repository-boundary.md) 페이지를 따른다.

## 계약 형태 (v002와 동일)

```yaml
arch: pccx-v003
package_repo: pccx-v003
domains:
  - LLM
  - Vision
  - Voice
isa_version: TBD
register_abi_version: TBD
driver_abi_version: TBD
top_interface_version: TBD
weight_format: TBD
activation_format: TBD
nonlinear_precision: TBD
control_bus: TBD
model_specific: false
board_specific: false
known_application_repos: []   # board/application 통합이 시작되면 갱신
```

모든 값은 evidence가 실제 값으로 증명되기 전까지 **TBD**다.
문서 freeze, 실험 로그, working integration이 준비돼야 비로소 값이 이동한다.

## v002 대비

| Field | v002 (released) | v003 (planning) |
| --- | --- | --- |
| ISA | freeze된 v002 ISA | TBD; spatial decode / MoE / longer context 확장 가능성 존재 |
| Register ABI | freeze된 v002 register map | TBD |
| Driver ABI | freeze된 v002 driver ABI | TBD |
| Weight / activation format | v002: W4A8 | TBD |
| Control bus | v002: AXI-Lite | TBD |
| Application target | v002 타겟: Gemma 3N E4B on KV260 | v003 planning: Gemma 4 E4B |

표는 의도와 차이축을 보여주며, v003 값은 구현 완료를 주장하지 않는다.

## 업데이트 규칙

v003 contract 필드는 evidence가 공개 가능한 수준(고정 ISA/spec/harness/working
integration)으로 검증되면 TBD에서 실값으로 전환한다.
값 선승격은 기존 consumer의 재-pin와 재검증을 강제한다.

## 참고

- v002 계약 서사: [`docs/reference/v002-contract.md`](../reference/v002-contract.md)
- v003 tracker: [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)
