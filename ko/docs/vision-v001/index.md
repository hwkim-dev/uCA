# pccx vision-v001 — KV260 위 CNN 추론 트랙

vision-v001 라인은 동일한 KV260 substrate 위에서 운영되는 평행
제품 라인으로, **vision** 워크로드 (CNN 계열 분류, 객체 검출) 에
초점을 둔다. LLM 라인과 W4A8 NPU substrate 를 공유하지만 워크
로드 family 는 다르다. 활성 코드는 아직 이 문서 사이트에 들어
오지 않았으며, 본 페이지는 업스트림 RTL 저장소가 안정될 때까지의
placeholder 다.

## 작업 상태

- 저장소: [`pccxai/pccx-vision-v001`](https://github.com/pccxai/pccx-vision-v001)
- 작업 staging 저장소: `pccx-vision-v001-staging` (private)
- v002 와 substrate 공유 — 동일한 KV260 보드, 동일한 W4A8
  weight × activation 비율, 동일한 L2 URAM 구성
- 데이터플로우는 다름 — 토큰 단위 KV 스트리밍이 아니라 dense
  conv 타일 재사용. GEMM systolic + GEMV 하이브리드는 conv 에
  재사용
- 첫 모델 후보 — ResNet18, YOLOv8n, MobileNetV3
  (footprint 가 가장 작은 변종 우선; 선택은 KV260 의 L2 URAM 과
  DSP 예산에 좌우)

## 기존 FPGA vision IP 대비 위치

오늘날 KV260 vision 영역은 두 부류의 IP 가 차지한다 — 벤더 제공
DPU IP (INT8 전용) 와 양자화 인지 훈련 (QAT) 으로 구동되는 임의
비트 streaming-dataflow 가속기. vision-v001 트랙은 양쪽과 다르게
세 축에서 위치를 잡는다.

```{table} vision-v001 차별화 매트릭스 (비교 맥락, 벤치마크 아님)
:name: tbl-vision-v001-differentiation-ko

| 축                       | 상용 DPU IP (INT8 전용)     | streaming-dataflow QAT (FINN 계열) | vision-v001 (본 트랙)                |
|---|---|---|---|
| 양자화                   | INT8 weight / INT8 activation | 임의 2–8 비트, QAT                  | **W4A8** — INT4 weight × INT8 act |
| 데이터플로우             | 이종 micro-coded PE 혼합    | 레이어별 streaming dataflow        | 통합 GEMM systolic + GEMV          |
| LLM 라인과의 재사용      | 없음                        | 없음                               | **v002 와 동일 RTL substrate**     |
| 레이어별 효율 편차       | 보고된 5–9× 변동             | 모델별 빌드에 좌우                  | 타일 재사용 균일성을 설계 목표로    |
| 소스                     | 벤더 레퍼런스                | 오픈소스 (예: FINN), QAT 툴체인     | 오픈소스, KV260 네이티브           |
```

차별화는 *자세 (posture)* 이지 벤치마크가 아니다 — 릴리스 증거
체크리스트가 게이트를 통과시키기 전까지 FPS / 레이턴시 / 전력 /
정확도 수치를 이 페이지에서 주장하지 않는다. 기존 벤더 / QAT IP
참조는 풍경 맥락이지 비교 결과가 아니다.

### 공개 벤치마크 기준점

아래 수치는 위 두 family 의 **공개적으로 보고된** 벤치마크다.
**vision-v001 의 결과가 아니며**, 외부 독자가 검증 가능한 숫자로
차별화 매트릭스를 anchor 하기 위해 인용한다.

- **Vendor DPU IP on KV260 (Xilinx DPUCZDX8G B4096)** — MobileNet V1
  ≈ 187 FPS / 5.3 ms 레이턴시; ResNet-50 ≈ 62 FPS / 16.1 ms 레이턴시.
  레이어별 효율은 입력 레이어 (≈ 54–259 GOP/s) 와 중간 단계 3 × 3
  컨볼루션 (≈ 470–500 GOP/s) 사이에서 5–9 × 변동.
- **Streaming-dataflow QAT (FINN)** — ResNet-50 ≈ 2 000 FPS @ ≈ 70 W
  on Alveo U250 (~400 K LUTs). 동일 접근을 KV260 (~256 K LUTs)
  로 축소하면 일반적으로 2–4 × 낮은 영역에 자리잡는다.
- **W4A8 vision regime** — KV260 모델 zoo 는 INT8 가 지배적이며,
  sub-4-bit (binary / ternary / 2-bit) 작업은 streaming-dataflow
  계열에 등장한다. pccx v002 가 LLM 에서 사용하는 W4A8
  weight × activation 영역은 KV260 vision 벤치마크로 아직 공개되지
  않았다.

이 기준점은 차별화 매트릭스를 anchor 하는 용도이며 vision-v001
자체의 벤치마크가 아니다. 릴리스 증거 체크리스트가 게이트를
통과시키기 전까지 vision-v001 수치는 이 문서 사이트에서 주장
되지 않는다.

## 상태 스냅샷

```{table} vision-v001 레이어 상태 (placeholder)
:name: tbl-vision-v001-status-ko

| 레이어                  | 상태                                                            |
|---|---|
| RTL                     | vision-v001 저장소에 아직 commit 되지 않음                      |
| 드라이버 / 런타임       | 범위 TBD; conv 전용 경로는 v002 와 갈라질 가능성                |
| 검증                    | v002 릴리스 증거 체크리스트 상속; 모델별 골든 벡터 TBD           |
| FPS 주장                | 없음 — TBD                                                     |
| mAP / Top-1 주장        | 없음 — TBD                                                     |
| 비트스트림              | 없음 — TBD                                                     |
```

이 페이지는 업스트림 RTL 저장소가 자리 잡고 첫 모델 프로파일링이
나오면 확장된다.

## 함께 보기

- {doc}`../roadmap` — pccx 생태계의 릴리스 방향 요약
- {doc}`../v002/index` — 공유 NPU substrate (활성 LLM 라인)
- {doc}`../v003/index` — LLM 라인 후속, 별도 RTL 저장소
