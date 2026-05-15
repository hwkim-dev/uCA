---
orphan: true
---

> 초안 운영 문서입니다. 법률 자문이 아니며 계약서가 아니다.
> 적용 전에는 법무 검토가 필요합니다.

# IP protection map

PCCX IP는 단일 수단에 과중을 두지 않도록 레이어를 나누어 운영한다.

## 레이어 맵

| 레이어 | 보호 대상 | 적용 위치 | 상태 |
| --- | --- | --- | --- |
| Trademark | `PCCX™`, `PCCX OpenCore`, `PCCX ProCore`, `PCCX ASICKit`, `PCCX Compatible` | KIPRIS (KR) | KR Class 09 `40-2026-0091497`, Class 42 `40-2026-0091498`는 출원 대기 |
| Copyright | 소스, RTL, docs | `LICENSE` + 파일 헤더 정책 | 기본 `Apache-2.0` |
| Patent (categories) | 아키텍처/quantization/scheduling/compiler/검증의 후보 | 공개 docs는 카테고리만 설명 | 자세한 후보는 private docket |
| Trade secret | ProCore RTL, enterprise compiler backend, timing/PPA scripts, 고객 특화 최적화 | 공개 저장소 외부 | 상세는 trade-secret 정책 |
| Contract | CLA, sponsorship, commercial 계약, investor 계약 | 별도 실행 문서 | 초안/법무 검토 단계 |
| Layout-design right | ASIC layout/GDS/mask work | 반도체 레이아웃 법 | 현재 미적용, RTL 단계에서는 미적용 |

## 공개/비공개 경계

공개: Standard, ISA, SDK, simulator, OpenCore, conformance harness, 문서
비공개: ProCore, Enterprise compiler backend, ASICKit, customer optimization, PPA/timing script,
patent 후보, trade secret, layout 산출물

## 레이어 트리거

- 상표 사용 출현: `TRADEMARKS.md` 갱신
- 신규 소스 파일: `copyright-header-policy.md` 적용
- 신규 아이디어 식별: `patent-candidate-intake.md`로 분류
- 기밀 가치가 있는 정보: `trade-secret-policy.md`
- 자금·지분 계약 변화: 별도 계약 갱신
- ASIC layout 생성: layout-design right 등록 및 repo 경고 반영
