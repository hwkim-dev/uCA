# 검증 워크플로우

> pccx-FPGA RTL 을 pccx-lab 으로 검증하는 전체 파이프라인 — 테스트벤치
> 컴파일부터 Vivado synth 리포트 수집까지.

## 아키텍처 개요

검증 파이프라인은 두 레포에 걸쳐 있습니다:

| 레포 | 역할 |
|------|------|
| `pccx-FPGA-NPU-LLM-kv260` | RTL + 테스트벤치 + `hw/sim/run_verification.sh` |
| `pccx-lab` (이 레포) | `.pccx` 포맷, Tauri 쉘, IPC 커맨드, UI |

`run_verification.sh` 가 각 testbench 를 `xsim` 으로 컴파일하고
`PASS: <N> cycles` / `FAIL: …` 의 canonical 라인을 캡처한 뒤,
`from_xsim_log` 바이너리를 통해 UI 가 로드할 수 있는 `.pccx` 파일을
생성합니다.

## End-to-end 흐름

```
┌──────────────────────┐   xvlog+xelab+xsim    ┌──────────────────┐
│  hw/tb/*.sv          │ ───────────────────▶  │  xsim.log        │
└──────────────────────┘                       └──────────────────┘
                                                       │
                                                       │ from_xsim_log
                                                       ▼
                                          ┌──────────────────────┐
                                          │  hw/sim/work/<tb>/   │
                                          │       <tb>.pccx      │
                                          └──────────────────────┘
                                                       │
                                    run_verification / │ load_pccx
                                    load_pccx IPC      ▼
                                          ┌──────────────────────┐
                                          │  pccx-lab 네이티브 앱 │
                                          │  Timeline / Synth    │
                                          └──────────────────────┘
```

## 실행 방법

`pccx-FPGA-NPU-LLM-kv260` 루트에서:

```bash
hw/sim/run_verification.sh
```

스크립트 동작:

1. 각 tb 의 `TB_DEPS` 에 나열된 RTL 의존성 컴파일
2. `xsim` 으로 elaborate + 실행 (xvlog / xelab / xsim)
3. PASS/FAIL 라인 파싱 + `from_xsim_log` 호출하여
   `hw/sim/work/<tb>/<tb>.pccx` 생성
4. 테스트벤치별 verdict 테이블 + synth 타이밍 상태 출력

### 새 testbench 추가

`run_verification.sh` 에서 두 줄만 추가:

```bash
TB_DEPS[tb_new_module]="SUB_DIR/new_module.sv"
TB_CORE[tb_new_module]=N   # 이미 사용된 core-id 와 겹치지 않게
```

`hw/tb/tb_new_module.sv` 에 testbench 파일을 두고, 다음 canonical
라인을 출력하도록 작성:

```systemverilog
$display("PASS: %0d cycles, both channels match golden.", N_CYCLES);
// 실패 시:
$display("FAIL: %0d mismatches over %0d cycles.", errors, N_CYCLES);
```

이 문자열들은 `from_xsim_log` 파서가 정확히 매칭합니다.

## pccx-lab 통합

`.pccx` 파일이 생성되면 pccx-lab 네이티브 앱에서
**Verification → Synth Status** 로 이동하면 3가지 위젯이 보입니다:

- **Run Verification Suite** — `run_verification` IPC 호출 →
  `run_verification.sh` 를 쉘로 실행하고 구조화된 summary 리턴 (테스트벤치별
  PASS/FAIL + timing-met verdict + 생성된 `.pccx` 경로들)
- **Per-row `Open` 버튼** — 각 tb 의 `.pccx` 에 대해 `load_pccx` 호출.
  Tauri 백엔드가 trace 를 캐시하고 `trace-loaded` 이벤트를 emit →
  Timeline 컴포넌트가 구독하여 캔버스가 자동으로 리프레시됨.
- **Synth Status card** —
  `hw/build/reports/{utilization,timing_summary}_post_synth.rpt` 파싱해서
  LUT / FF / RAMB / URAM / DSP 카운트 + WNS / failing endpoints /
  worst clock 의 timing-met verdict 표시.

## 주요 IPC 커맨드

| 커맨드 | 입력 | 출력 |
|--------|------|------|
| `load_pccx` | `path: String` | `PccxHeader` (+ `trace-loaded` emit) |
| `fetch_trace_payload` | — | flat binary buffer (24 B/event) |
| `get_core_utilisation` | — | 코어별 utilisation % + totals |
| `run_verification` | `repoPath: String` | tb별 결과 + synth 상태 |
| `list_pccx_traces` | `repoPath: String` | 생성된 `.pccx` 목록 |
| `load_synth_report` | `utilizationPath`, `timingPath` | `SynthReport` |

## End-to-end 테스트

`src/ui/e2e/` pytest suite 는 파이프라인 각 단계를 커버:

| 테스트 | 검증 내용 |
|--------|-----------|
| `test_smoke.py` | UI 쉘 렌더, 메뉴 + Synth Status 탭 reachable |
| `test_verify_tb_packer.py` | `load_pccx` + `get_core_utilisation` 정상 |
| `test_synth_report.py` | Vivado 리포트 파서가 NPU_top 카운트 + WNS 정확히 추출 |
| `test_run_verification.py` | 전체 suite end-to-end + `list_pccx_traces` |

실행:

```bash
cd src/ui/e2e && .venv/bin/pytest -v
```
