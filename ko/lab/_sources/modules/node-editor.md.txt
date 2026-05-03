# 노드 에디터

**Data Flow** 탭은 pccx-v002 토폴로지 노드들을 드래그·와이어·설정
할 수 있는 Blender 풍 블록 다이어그램 캔버스입니다.

```{image} ../../_static/screenshots/node-editor.png
:alt: 기본 NPU 데이터플로우 + 미니맵이 떠 있는 pccx-lab Node Editor
:width: 100%
```

## 레이아웃

| 영역 | 역할 |
|------|------|
| **좌측 팔레트**  | 카테고리화 + 접기 + 검색 가능한 노드 라이브러리 (Input / Memory / Compute / Output) |
| **캔버스**       | 무한 pan/zoom, 미니맵 오버레이, 줌 컨트롤 |
| **Quick-add**    | `Shift+A` 로 커서 위치에 플로팅 팝오버 — Blender 컨벤션 |

## 노드 카탈로그

기본 빌드에 13개 노드 타입이 동봉됩니다. 그 중 5개는 pccx-v002
전용으로 설정된 가속기 토폴로지를 반영합니다.

### Input

- **Host CPU** — AXI-Lite 마스터, PCIe / CXL 인터페이스 선택 가능.

### Memory

- **DRAM** — 오프-칩: LPDDR5 / HBM2E / DDR5 / GDDR6X, BW + 용량 조정
- **AXI Fabric** — 128-bit 인터커넥트, 버스트 길이 / 오버헤드 / 포트 수
- **BRAM L1** — 온-칩 스크래치패드, 포트별 BW + 뱅크 수
- **URAM L2** (v002) — 64 URAM, 1.75 MB, 2-사이클 read
- **HP Buffer** (v002) — 4-포트 HP AXI pre-fetch FIFO, upper/lower 웨이트 채널 분리
- **fmap Cache** (v002) — 27 b × 2048 엔트리, 32-레인 브로드캐스트

### Compute

- **GEMM MAC Array** (v002) — 32 × 32 W4A8 systolic, 1 GHz 에 65.5 TOPS
- **GEMV Engine** (v002) — 4 레인 × 32 MAC, 5-stage 파이프라인
- **CVO SFU** (v002) — 단일 인스턴스, CORDIC + LUT (exp / sqrt / GELU / sin / cos / softmax)
- **Accumulator** — 레지스터 파일 + 애더 트리

### Output

- **Post-Proc** — activation / normaliser / quantiser / softmax 토글
- **Write-back DMA** — 1 / 2 / 4 / 8-채널 egress

## 키보드 단축키

| 단축키 | 동작 |
|--------|------|
| `Shift+A`              | 커서 위치에 quick-add 메뉴 열기 |
| `Esc`                  | quick-add 메뉴 닫기 |
| `Delete` / `Backspace` | 선택된 노드 / 엣지 삭제 |
| Scroll                 | 줌 인 / 아웃 |
| 캔버스 드래그          | pan |
| 팔레트 엔트리 드래그   | 드롭 위치에 스폰 |
| 엔트리 더블클릭        | 캔버스 중앙에 스폰 |

Ctrl-Scroll / pinch-zoom 도 동작합니다. 팔레트 접기 상태는
카테고리별이며 세션 단위는 아닙니다 — 새로고침 시 모두 펼쳐진 상태로
돌아갑니다.

## 타입별 소켓 (컬러 범례)

각 노드는 하나 이상의 색상 핸들을 노출합니다:

| 색상 | 데이터 타입 |
|------|-------------|
| `#94a3b8` 회색       | 커맨드 / 제어 |
| `#60a5fa` 블루       | AXI read / 스트림 |
| `#818cf8` 인디고     | AXI 패브릭 / 인터커넥트 |
| `#22d3ee` 시안       | fmap / 브로드캐스트 채널 |
| `#34d399` 그린       | 타일 A / 주 컴퓨트 스트림 |
| `#a78bfa` 바이올렛   | 타일 B / MAC partial sum |
| `#f59e0b` 앰버       | 누산기 / stall |
| `#fb923c` 오렌지     | post-proc 출력 |
| `#f472b6` 핑크       | DMA egress / write-back |
| `#e879f9` 푸시아     | SFU / 비선형 |
| `#f87171` 레드       | HP buffer 입력 |
| `#14b8a6` 틸         | URAM read / L2 |
| `#eab308` 옐로우     | fmap cache 브로드캐스트 |

기본 배선은 pccx v002 의 데이터플로우 (Host → AXI → BRAM →
MAC → Accumulator → Post-Proc → Write-back) 를 반영하므로 캔버스는
이미 실험 시작에 적합한 지점입니다.

## 로드맵

- Frame / group (Blender 스타일 중첩 서브그래프).
- 타입 검증 — 부적합 소켓 드롭은 툴팁과 함께 거부.
- 현재 캔버스의 SVG / PNG 내보내기.
- 로드된 `.pccx` 에 동기화된 데이터플로우 애니메이션 재생.
