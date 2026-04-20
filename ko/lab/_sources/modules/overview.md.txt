# 모듈 개요

`pccx-lab` 은 Tauri 2 데스크톱 앱으로, 엄격히 분리된 4개의 Rust /
TypeScript 모듈을 하나의 **pccx** NPU 검증·프로파일링 IDE 로 묶어줍니다.

| 모듈 | 언어 | 의존 | 역할 |
|------|------|------|------|
| `core/`        | Rust       | —       | `.pccx` 포맷, 트레이스 분석, roofline / bottleneck / synth-report 파서 |
| `ui/`          | TypeScript (React + Tauri) | `core/` (IPC 경유) | 쉘, 시각화, 리포트 대시보드 |
| `uvm_bridge/`  | Rust + DPI-C | `core/` | SystemVerilog / UVM ↔ `core/` 경계 |
| `ai_copilot/`  | Rust       | `core/` 트레이스 타입만 | LLM + UVM-전략 생성기 래퍼 |

의존성은 **내부 방향으로만** 흐릅니다. `core/` 는 UI / 프레임워크
크레이트를 절대 import 하지 않고, `ui/` 는 `core/` 의 공개 API 를
Tauri 커맨드 브릿지 경유로만 사용합니다.

## 쉘 한눈에

기본 레이아웃은 모던 EDA IDE (VTune / Nsight 스타일) 를 모방합니다.
상단 메뉴바, 툴바, 탭 스트립, 활성 작업 패널, 2개의 도킹 가능한
사이드 패널 (Live Telemetry + AI Copilot).

```{image} ../../_static/screenshots/timeline-fullwidth.png
:alt: pccx-lab Timeline 뷰 — 사이클 축 위의 NPU 이벤트 스윔 레인
:width: 100%
```

위 캡처는 **Timeline** 탭입니다. 각 스윔 레인이 하나의 코어이고,
이벤트는 타입별 색상 코드 (`MAC_COMPUTE` / `DMA_READ` / `DMA_WRITE` /
`SYSTOLIC_STALL` / `BARRIER_SYNC`) 로 표시됩니다. 우측 통계 패널은
Rust 의 `core_utilisation` IPC 가 채웁니다.

## 주요 탭 (2026-04-20 기준)

```{image} ../../_static/screenshots/node-editor.png
:alt: Blender 급 팔레트 + pccx v002 노드 타입을 갖춘 Node Editor
:width: 100%
```

| 탭 | 컴포넌트 | 단축키 | 용도 |
|----|----------|--------|------|
| Timeline          | `Timeline.tsx`           | — | 사이클 축 스윔-레인 이벤트 타임라인 |
| Flame Graph       | `FlameGraph.tsx`         | — | 계층적 stall / compute 스택 |
| Waveform          | `WaveformViewer.tsx`     | — | 시그널 웨이브폼 (향후 VCD sink) |
| System Simulator  | `HardwareVisualizer.tsx` | — | 3D 시스톨릭 어레이 라이브 뷰 |
| Memory Dump       | `MemoryDump.tsx`         | — | flat trace buffer 의 페이지화된 hex 뷰 |
| Data Flow         | `NodeEditor.tsx`         | **Shift+A** | Blender 급 블록 다이어그램 캔버스 |
| SV Editor         | `CodeEditor.tsx`         | — | SystemVerilog 에디터 + AI 인라인 생성 |
| Report            | `ReportBuilder.tsx`      | — | 엔터프라이즈 리포트 컴포저 |
| Verification      | `VerificationSuite.tsx`  | — | **4-카드** pccx-FPGA 검증 대시보드 |
| Roofline          | `Roofline.tsx`           | — | ECharts 루프라인 차트 |

## 검증 대시보드 (pccx-FPGA 브릿지)

```{image} ../../_static/screenshots/verification-synth-status.png
:alt: Verification -> Synth Status 서브탭의 4-카드 대시보드
:width: 100%
```

**Verification → Synth Status** 서브탭은 pccx-FPGA RTL 검증을 위한
원스톱 대시보드입니다. 4개 카드가 위에서 아래로 쌓입니다:

1. **Run Verification Suite** — 인접한 pccx-FPGA 레포의
   `hw/sim/run_verification.sh` 를 shell 실행하고 테스트벤치별
   verdict 테이블을 반환. 각 행의 **Open** 버튼은 생성된 `.pccx`
   를 `trace-loaded` 이벤트로 Timeline 에 로드합니다.
2. **Synthesis Status** —
   `hw/build/reports/{utilization,timing_summary}_post_synth.rpt`
   를 파싱, LUT / FF / RAMB / URAM / DSP 카운트와 WNS 타이밍 verdict
   를 보여줍니다.
3. **Roofline Analysis** — 현재 캐시된 트레이스의 arithmetic intensity,
   achieved GOPS, compute-vs-memory-bound verdict 를 계산합니다.
4. **Bottleneck Windows** — 고정 윈도우 기반 DMA / stall hotspot 목록,
   share %, 이벤트 수, 코어 커버리지 (정규화) 포함.

End-to-end 흐름은 {doc}`../verification-workflow` 참고.

## Tauri IPC 표면 (17 커맨드)

| 커맨드 | 용도 |
|--------|------|
| `load_pccx(path)` | 트레이스 캐시 + `trace-loaded` emit |
| `fetch_trace_payload()` | Timeline 용 flat 24-B/event 버퍼 |
| `get_core_utilisation()` | 코어별 MAC-이용률 통계 |
| `compress_trace_context()` | LLM-프롬프트 사이즈 트레이스 요약 |
| `generate_uvm_sequence_cmd(strategy)` | SV UVM 시퀀스 stub |
| `list_uvm_strategies()` | 5개 내장 전략 열거 |
| `generate_report()` | 레거시 엔터프라이즈 리포트 |
| `generate_markdown_report(util_path, timing_path)` | 트레이스 + synth 의 Markdown 요약 |
| `analyze_roofline()` | Arithmetic intensity + bound verdict |
| `detect_bottlenecks(window_cycles?, threshold?)` | Hotspot 윈도우 목록 |
| `load_synth_report(util_path, timing_path)` | 파싱된 Vivado synth 리포트 |
| `run_verification(repo_path)` | 전체 pccx-FPGA 스위트 실행 |
| `list_pccx_traces(repo_path)` | `hw/sim/work/` 트레이스 열거 |
| `validate_license(token)` | Tier + licensee + 만료 |
| `get_license_info()` | 컴파일-인 tier |
| `get_extensions()` | 플러그인 카탈로그 (로컬 LLM, VCD exporter, …) |

## Native-window 자동화

위의 모든 것은 진짜 **webkit2gtk** 웹뷰 안에서 `tauri-driver` 로
구동되며 — CI 가 쓰는 동일한 E2E 하네스입니다.
{doc}`../verification-workflow` 페이지가 selenium + tauri-driver
셋업을 설명하며, 현재 19개 pytest 케이스가 IPC 표면 전체를
end-to-end 로 검증합니다.
