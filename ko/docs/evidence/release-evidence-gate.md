---
orphan: true
---

> 초안 운영 방침입니다. 투자 안내·증권 제안이 아니라 공개-safe 정책 문서.
> 법률 검토 후 운영.

# 릴리스 evidence 게이트(정책)

릴리스는 evidence-gated이다. 하드웨어·runtime·타이밍·bitstream 관련 증거를
언급하는 공개 릴리스는 다음을 반드시 포함한다.

- 정확한 재현 명령
- 측정값 또는 `TBD`
- CI/sim/formal run URL
- source manifest / SHA pin
- 알려진 한계

이 항목이 빠지면 해당 릴리스는 그 증거 주장을 내지 않는다. 단락별 릴리스
일정은 목표치이며 production 주장으로 해석하지 않는다.
