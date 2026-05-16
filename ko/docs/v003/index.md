# pccx v003 — LLM 라인 후속, 별도 RTL 저장소

v003 라인은 {doc}`v002 라인 <../v002/index>` 의 **LLM 트랙**을
별도 RTL 저장소에서 이어간다. 활성 코드는 아직 이 문서 사이트에
들어오지 않았으며, 본 페이지는 업스트림 RTL 저장소가 안정될
때까지의 placeholder 다.

## 작업 상태

- 정본 v003 IP-core 계획 패키지: [`pccx-v003`](https://github.com/pccxai/pccx-v003)
  (planning / evidence-gated; 안정된 릴리스 브랜치는 아직 없음)
- 이전 feeder [`pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003)
  는 superseded / retired 상태이며 더 이상 활성 공개 트랙이 아니다.
  재사용 가능한 v003 LLM 자료는 `pccx-v003/LLM/` 아래로 들어온다
- v002 와 substrate 공유 — 동일한 KV260 보드, 동일한 W4A8
  weight × activation 비율, 동일한 L2 URAM 구성
- 첫 모델 집중 — **Gemma 4 E4B** 를 파운데이션으로 두는 계획
  (planning), 릴리스 포인트마다 (v003.0, v003.1) 아키텍처 novelty
  한 가지씩 적층
- v002.x 의 단계 (sparsity, speculative, EAGLE, SSD, Tree,
  benchmark)는 여기서 *반복하지 않습니다*; v003 는 다른 RTL
  베이스라인에서 시작합니다.

## 상태 스냅샷

```{table} v003 레이어 상태 (placeholder)
:name: tbl-v003-status-ko

| 레이어               | 상태                                                          |
|---|---|
| RTL                  | v003 저장소에 아직 commit 되지 않음                            |
| 드라이버 / 런타임    | v002 와 API 표면 공유; v003 전용 경로는 아직 없음              |
| 검증                 | v002 의 릴리스 증거 체크리스트를 게이트로 상속                 |
| 처리량 주장          | 없음 — TBD                                                    |
| 타이밍 클로저        | 없음 — TBD                                                    |
| 비트스트림           | 없음 — TBD                                                    |
```

이 페이지는 업스트림 RTL 저장소가 구축되면 확장됩니다.

## 함께 보기

- {doc}`../roadmap` — pccx 생태계의 릴리스 방향 요약
- {doc}`../v002/index` — 현재 활성 LLM 라인 (KV260)
- {doc}`../vision-v001/index` — 같은 substrate 위 평행 vision 트랙
