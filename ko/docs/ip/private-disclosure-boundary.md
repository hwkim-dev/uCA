---
orphan: true
---

> 초안 운영 문서입니다. 법률 자문이 아니며 계약서가 아니다.
> 공개 전 검토가 필요합니다.

# Private disclosure boundary

PCCX 공개 저장소에 올라가지 말아야 할 항목을 정의한다.

## 항상 비공개

다음 항목은 공개 레포에 두지 않는다.

| 항목 | 보관 위치 | 이유 |
| --- | --- | --- |
| 상표 출원 세부자료(고객 번호, XML, 영수증, 연락처) | private docket | 공개된 KIPRIS 수준은 허용, 원본은 미공개 |
| 미공개 후보 발명의 상세 claim | private docket | 공개 선행으로 특허성 상실 위험 |
| ProCore/Enterprise/ASICKit 구현 상세 | private 통합 엔지니어링 저장소 | trade secret |
| 고객별 최적화·통합 상세 | 고객 계약 경로 저장 | contract + trade secret |
| 확정되지 않은 legal draft(스폰서/투자자/고객) | private legal 저장소 | 공개 템플릿과 구분 |
| 재무 지표, burn-rate, cap table | private finance 저장소 | 프로젝트 수준 자료 |
| 개인 연락처 | repository 외부 | 개인정보보호 |
| NDA로 지정된 기밀정보 | NDA 보관소 | 계약상 의무 |

## 공개 가능한 대응 항목

| 비공개 항목 | 공개-safe 대응 |
| --- | --- |
| raw trademark filing | 번호, class, 접수일, 상태 |
| patent claim 상세 | 후보 카테고리 |
| ProCore RTL 묶음 | OpenCore 패키지(`pccx-v00N`) |
| 고객 최적화 레포트 | 일반화된 아키텍처 패턴 공개 |
| 투자 termsheet | commercial track 구조 설명 |

## 검사

PR 병합 전, private-disclosure 누출 패턴과 소스헤더/라이선스 위반 패턴을
기본 스캔한다. 다만 사람 검토를 대체하지 않는다.

## 비고

경계 판단이 애매하면 기본은 private로 둔다.
