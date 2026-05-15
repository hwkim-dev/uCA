---
orphan: true
---

# Risk register

현재 프로젝트가 보유한 엔지니어링/도입 리스크를 항목으로 정리한다.
확정 수치 예측은 넣지 않는다. TBD 표시는 미확정 항목임을 뜻한다.

## Engineering risks

- **KV260 timing closure** — 합성은 진행되었으나 timing-closed bitstream은
  미완료 상태다. 종료되기 전 모든 보드 주장 값은 TBD.
- **W4A8 golden-vector gate** — 산술 RTL 변경은 재현 가능한 golden vector
  기반 검증 게이트 후에만 반영한다. 현재 fixture는 smoke 수준이며,
  전체 세트는 추후 보강 예정.
- **Rebase merge 후 submodule pin drift** — [submodule pin policy](../reference/submodule-pin-policy.md)에
  대응 절차가 있다. 동일 위험은 앞으로의 재정렬에서도 동일하게 존재.
- **KO 문서 품질 편차** — 영어 원문을 기준 문서로 사용하므로 CI에서 EN/KO
  수치 동기성은 확인하지만, 문장 톤·표현 정합은 사람 리뷰가 계속 필요하다.
- **Vivado 버전 편차** — board 통합은 실무적으로 특정 Vivado 버전으로
  검증되어 왔으며, 새 버전에 대한 재현은 아직 제한적.

## Adoption risks

- **`--recurse-submodules` 누락한 새 클론** — shallow 한 형태는 빌드 가능해 보이나
  실제로는 실패한다. onboarding에서 필수 조건으로 안내.
- **CLA 미공개** — 상용 사용 가능 레포에서의 기여는 기존 오픈 라이선스로
  수용되며, 프로젝트 CLA는 확정 전이다.
  [contribution rules (draft)](../onboarding/contribution-rules.md) 참고.
- **Sphinx 의존성 잠금** — 현재 흐름은 Sphinx+MyST+멀티랭귀지이다.
  문서 시스템 전환 시 `pccx`, `pccx-v002`, board repo 문서 동기화를
  모두 해야 한다.

## 전략적 미확정 항목 (디자인)

- v003 IP 패키지 일정 미확정.
- `pccx-v002/Vision/` 흡수 여부는 호환성 리뷰 후 결정.
- Voice 도메인 아직 placeholder 상태.
- ASIC/MPW 탐색은 장기 항목으로 현재는 범위 밖.
- 상용/스폰서/투자 약관은 모두 [commercial](../commercial/)에서 DRAFT 상태.

## 이 페이지의 범위

- 확률 추정이 아니다. 영향도 등급과 점수도 아니다.
- 완화 계획 자체도 아니다. 완화는 실제 담당 저장소의 CI, runbook, 계약에서 수행.
- 근거가 생기면 즉시 항목 삭제/이동한다.
