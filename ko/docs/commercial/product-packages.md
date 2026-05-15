---
orphan: true
---

> 초안 운영 문서입니다. 법률·회계·세무·증권·IP 자문 후 적용.
> 스폰서십은 투자와 다르며 기여만으로 지분·배당이 생기지 않는다.

# PCCX 제품 패키지 (초안)

PCCX™는 오픈 코어와 병행해 세 개의 상용 패키지를 제공할 계획이다. 현재
어느 패키지도 하드웨어/performance/timing/bitstream 근거를 주장하지 않는다.
가격과 가용성은 법무 검토 후 확정한다.

| 패키지 | 대상 | 범위(의도) |
| --- | --- | --- |
| **ProCore** | 하드웨어 통합 업체 | v002/v003 OpenCore를 기반으로 한 강화 RTL 번들. 상용 라이선스 조건 하 배포 |
| **Enterprise SDK** | 툴체인 고객 | 닫힌 compiler backend, runtime 확장, 인증 harness |
| **ASICKit** | `tape-out` 대상 고객 | 파운드리 특화 RTL 뷰, 타이밍 스크립트, 검증 자료군 중심의 준비 패키지 |

Open track(PCCX Standard, ISA, SDK reference, simulator, conformance tests,
OpenCore reference, 공개 문서)은 기존 오픈 라이선스에 남아 있으며,
상용 패키지 접근조건이 아니다.

추적 이슈: pccxai/pccx#61
