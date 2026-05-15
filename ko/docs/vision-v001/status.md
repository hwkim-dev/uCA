---
orphan: true
---

# pccx-vision-v001 — current status

> Compatibility / planning track. **No committed RTL evidence.**
> KV260 bitstream, FPS, mAP, timing, board runtime은 모두 미확정.

`pccxai/pccx-vision-v001`는 미래 vision 라인의
`v002` IP-core 패키지 적합성 리뷰를 준비하는 트랙이다.
현재 이 저장소는 vision NPU를 즉시 배포하지 않는다.

## 현재 보유 / 미보유 항목

| Asset | Status |
| --- | --- |
| 재사용 Vision RTL (`rtl/...`) | **미커밋** |
| Sim / testbench harness | 미커밋 |
| Formal model | 미커밋 |
| Bitstream / timing-closed 구현 | 미생성 |
| FPS / mAP / accuracy benchmark | 미측정 |
| Board integration | 미실행 |
| 고정 contract값의 compatibility manifest | TBD |

따라서 이 저장소는 **계획·조율 workspace**이지 안정 릴리스 저장소가 아니다.

## 왜 `pccx-v002`와 분리되어 있는가

`pccx-v002`는 현재 LLM RTL을 제공하며, Vision/Voice 디렉터리는 placeholder이다.
vision 라인 계획이 먼저 가시화되어야 substrate 결정을 섣불리 주입하지 않아야 해서
`pccx-vision-v001`을 분리했다.

## 기본 방향

방향은 [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65) 기반이다.

- vision RTL이 준비되면 `pccx-v002/common/` 및 `pccx-v002/LLM/`와
  공통 substrate 공유 정도를 평가해 흡수 여부를 판단한다.
- 흡수가 성립되면 [`v002-vision-absorption-plan.md`](v002-vision-absorption-plan.md)에서
  전환 절차를 따른다.
- 흡수가 어렵다면 standalone 유지하고 자체 contract를 따로 설계한다.

## tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
