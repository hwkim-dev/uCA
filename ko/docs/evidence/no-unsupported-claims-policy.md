---
orphan: true
---

> 초안 운영 방침입니다. 법률 검토 전 문구의 구속력 없음.
> 근거가 없거나 재현 불가한 성능·타이밍·bitstream·정확도 주장을 금지.

# 미검증 주장 금지 정책

PCCX 공개 문서와 PR은 아래 항목을 **재현 가능한 증거** 없이 쓰면 안 된다.

- 보드 상 KV260 infer 동작 보장
- Gemma 3N E4B end-to-end runtime on KV260
- 토큰 초당 값(예: 20 tok/s) 주장
- timing-closure 완료 주장
- bitstream 성공 결과
- production-ready 주장
- 안정적인 API/Application binary 호환성 주장
- conformance 인증 배지(“공식”, “PCCX-Compatible”) 부여 문구
- FPS 수치
- mAP 수치

요약하면, 하드웨어·runtime·타이밍·bitstream·지연·정확도·인증 결과가
있다는 문장은 측정 근거로 뒷받침되거나 `TBD`로 표시해야 한다.

릴리스/문서/메타데이터 PR 병합 전에는 금지어 검사 CI가 실행된다.
자세한 절차는 `docs/evidence/release-evidence-gate.md`를 따른다.
