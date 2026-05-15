---
orphan: true
---

# vision-v001 open questions

> Draft / planning. 증거 기반 판단 전까지 open 상태이다.

## Scope

- vision line이 v002 LLM과 동일한 KV260 substrate를 쓰는지,
  아니면 Versal/Kria/ASIC 등 다른 board가 필요할지
- vision이 W4A8 quantization baseline을 공유하는지, 아니면 INT8/고정소수점
  등 별도 포맷이 필요한지
- 제어 버스(AXI-Lite)와 memory hierarchy를 v002 LLM과 동일하게 가져갈 수 있는지

## Repository placement

- 기본 방향은 v002의 compatibility review에서 흡수 가능 시 `pccx-v002/Vision/`로
  이동한다.
- substrate가 다르면 `pccx-vision-v001` standalone을 유지한다.
- v002 기간을 넘기고 v003로 연기되는 경우 `pccx-v003/Vision/`로 이동한다.

## Evidence

- 이 저장소에서 어떤 근거가 있어야 vision 성능/정확도/KV260 관련 주장을
  문서화할 수 있는가.
- 측정 데이터의 저장 위치는 어디가 되는가. board integration의 `docs/Evidence/`, Sphinx 사이트,
  또는 별도 evidence 저장소 중 어디를 기준으로 둘지

## Compatibility manifest

- v002 contract를 넘어가야 하는 새 필드(입력 레이아웃, 채널 순서, image format)는 어떤 것인지
- 해당 필드는 v002 contract의 확장으로 처리할지, v003 독립 contract로 분리할지

## tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)

이 문서는 단지 질문을 남긴다. 특정 방향을 선결정하지 않는다.
