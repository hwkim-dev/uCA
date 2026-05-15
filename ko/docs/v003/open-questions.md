---
orphan: true
---

# v003 open questions

> Draft / planning. 아래 답변은 evidence 확보 전까지는 비확정이다.

## Scope

- `pccx-v003`이 LLM만 다룰지, day one부터 Vision/Voice/common까지 확장할지
- Vision/Voice가 지연될 경우 v002에 장기 유지할지, 아니면 v003로 이관할지
- v003 라인 버전 전략: `pccx-v003.0` 계열처럼 여러 patch 버전으로 나눌지,
  또는 단일 패키지 라인으로 고정할지(v002에서의 버전 방식과 비교)

## Architecture

- v003에서 W4A8 양자화 baseline를 유지할지, 다른 weight/activation format으로 갈지
- v002 ISA encoding을 유지할지, ABI 분리를 허용할지(별도 driver/runtime 필요 여부에 영향)
- spatial decode / Eagle-3 speculative decoding / MoE를 첫 릴리스 범위로 포함할지
- Gemma 4 E4B에 맞는 KV-cache 전략을 어떻게 구성할지

## Board / target

- v003 첫 board integration은 KV260 지속 여부, larger Kria/Versal로 이전, ASIC bring-up
  우선순위 중 어디에서 시작할지
- 최초 v003 board integration repo를 만들기 위한 증빙 기준은 무엇인지

## Repository structure

- `pccx-v003` 계약 freeze는 어느 시점에서 일어날지
  (contract stability 기반인지, reusable RTL 최초 반영 시점인지)
- 히스토리 feeder였던 `pccx-LLM-v003` 재도입 규칙은 어떻게 정리할지
  (`pccx-v003/LLM/`로 가져오는 시점/기준)

## tracker

- [pccxai/pccx#64](https://github.com/pccxai/pccx/issues/64)

현재는 위 질문 모두 open 상태다.
