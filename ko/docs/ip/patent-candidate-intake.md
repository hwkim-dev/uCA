---
orphan: true
---

> 초안 운영 문서입니다. 법률 자문이 아니며 계약서가 아닙니다.
> 후보 발명 공개 전에는 한국 특허법 전문가 검토가 필요합니다.

# Patent candidate intake

후보 발명은 공개 artefact(커밋, 문서, 발표, 데모, 릴리스)에 반영되기 전에
이 절차를 통과한다.

## 기동 기준

아래 중 하나라도 해당되면 intake로 처리:

- 기여 결과가 신규성 있을 수 있다고 판단되는 경우
- 리뷰어가 신규성 의심을 제기한 경우
- 공개 초안에서 아직 미공개 작업을 설명하는 문서가 준비되는 경우

## 처리 단계

1. 최솟의 새로운 claim을 식별하고 선행기술 대비 구분.
2. 다음 중 하나로 분류:
   - already-publicly-disclosed
   - not-public-yet
   - patent-candidate
   - trade-secret-candidate
   - defensive-publication-candidate
   불명확하면 기본 `not-public-yet`으로 두고 legal review 선행.
3. private docket에 기록하고, 공개 저장소에는 카테고리만 공개(`patent-strategy.md`).
4. 공개 전 처리 결정:
   - patent-candidate: 출원 선행
   - trade-secret-candidate: 공개 보류 및 `trade-secret-policy.md` 적용
   - defensive: 공개 타임스탬프와 저자성을 확보해 선행기술로 공표

## 공개 전 점검

- 신규 claim이 문장으로 명확히 정의되었는가?
- 단계별 분류가 완료되었는가?
- patent 후보면 출원 또는 보류 승인 문서가 있는가?
- trade-secret 후보면 비공개가 제거되었는가?
- defensive publication이면 timestamp/저자성은 확보되었는가?
- private-disclosure 경계를 준수했는가?

## 실패 패턴

- 분류 전에 공개: 신선한 patent novelty를 놓칠 수 있음.
- trade secret 분류가 누락된 상태로 공개: trade secret 상실.
- 방어 공개의 timestamp/저자성 미비: 증거력 저하.
