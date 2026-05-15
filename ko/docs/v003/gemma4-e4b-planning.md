---
orphan: true
---

# Gemma 4 E4B planning (v003 target)

> Draft / planning / evidence-gated. 성능/bitstream/timing/ runtime 주장 없음.

PCCX™ v003 라인의 타깃 LLM 모델은 **Gemma 4 E4B**로 가정한다.
이 문서는 계획 상태만 기록하며, v003 하드웨어·runtime·driver가 현재 존재함을
의미하지 않는다.

## Gemma 4 E4B를 목표로 하는 이유

- v002는 Gemma 3N E4B를 기반으로 LLM 라인을 정렬하고 있다
  (`pccxai/pccx-FPGA-NPU-LLM-kv260` board integration 기준).
- v003는 v002를 잇는 다음 단계이며, 차세대 Gemma family를 목표로 한다.
- v003 LLM planning에서 잠재적으로 다루는 아키텍처 항목은
  spatial decode, Eagle-3 speculative decoding, MoE, longer context, revised attention 패턴이다.
  다만 오늘 상태에서는 구현 주장 없음.

## Planning 입력

- v002 ISA / register / memory / top-interface 계약은 frozen 상태로 기준이다.
  v003 divergence 발생 시 v003 contract draft 기준으로 분기 관리한다.
- v002 Sail formal model (`pccxai/pccx-v002/LLM/formal/sail/`)는 구조적 참고점이다.
- board substrate는 KV260, Kria/Versal, ASIC 중 어느 방향으로 갈지 미정이다.

## 현재 **미주장 항목**

- Gemma 4 E4B의 KV260 또는 타 보드 기반 토큰 처리량 측정값 없음
- bitstream 완성, timing-closed 구현 없음
- production-ready runtime 없음
- ABI stability claim 없음
- driver 구현 없음
- 정확도/품질 benchmark 없음

## tracker

- [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)
- compatibility contract scaffold: [`compatibility-contract.md`](compatibility-contract.md)
- open questions: [`open-questions.md`](open-questions.md)
