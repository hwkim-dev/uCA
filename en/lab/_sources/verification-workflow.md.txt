# Verification Workflow

> Complete pipeline for verifying the pccx-FPGA RTL via pccx-lab: from
> testbench compilation through Vivado synthesis report ingestion.

## Architecture overview

The verification pipeline is split across two repositories:

| Repo | Role |
|------|------|
| `pccx-FPGA-NPU-LLM-kv260` | RTL + testbenches + `hw/sim/run_verification.sh` |
| `pccx-lab` (this repo)    | `.pccx` format, Tauri shell, IPC commands, UI |

A shell bridge (`run_verification.sh`) compiles each testbench under
`xsim`, captures the canonical `PASS: <N> cycles` / `FAIL: …` line, and
hands it to the `from_xsim_log` binary which emits a `.pccx` trace
file the UI can load.

## End-to-end flow

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
                                          │  pccx-lab native app │
                                          │  Timeline / Synth    │
                                          └──────────────────────┘
```

## Running the suite

From the `pccx-FPGA-NPU-LLM-kv260` root:

```bash
hw/sim/run_verification.sh
```

The script:

1. Compiles each tb's RTL deps listed in `TB_DEPS` (associative array).
2. Elaborates + runs under `xsim` (xvlog / xelab / xsim in sequence).
3. Parses the PASS/FAIL footer and invokes `pccx-lab`'s
   `from_xsim_log` converter to emit `hw/sim/work/<tb>/<tb>.pccx`.
4. Prints the per-testbench verdict table plus the current synth
   timing status from `hw/build/reports/timing_summary_post_synth.rpt`.

### Adding a new testbench

Only two lines in `run_verification.sh` need changing:

```bash
TB_DEPS[tb_new_module]="SUB_DIR/new_module.sv"
TB_CORE[tb_new_module]=N   # distinct core-id for the emitted trace
```

Place `tb_new_module.sv` under `hw/tb/`. Emit the canonical line:

```systemverilog
$display("PASS: %0d cycles, both channels match golden.", N_CYCLES);
// or on failure:
$display("FAIL: %0d mismatches over %0d cycles.", errors, N_CYCLES);
```

Those are the exact strings the `from_xsim_log` parser matches.

## pccx-lab integration

Once the `.pccx` files exist, open the pccx-lab native app and navigate
to **Verification → Synth Status**. Three widgets appear:

- **Run Verification Suite** — invokes `run_verification` IPC which
  shells out to `run_verification.sh` and returns a structured summary
  (per-tb PASS/FAIL + timing-met verdict + generated `.pccx` paths).
- **Per-row `Open` buttons** — call `load_pccx` on each tb's
  `.pccx`. The Tauri backend caches the trace and emits a
  `trace-loaded` event that the Timeline component subscribes to,
  so the canvas refreshes automatically.
- **Synth Status card** — parses
  `hw/build/reports/{utilization,timing_summary}_post_synth.rpt` and
  surfaces LUT / FF / RAMB / URAM / DSP counts plus WNS / failing
  endpoints / timing-met verdict on the worst clock.

## Available IPC commands

| Command | Input | Output |
|---------|-------|--------|
| `load_pccx` | `path: String` | `PccxHeader` (+ emits `trace-loaded`) |
| `fetch_trace_payload` | — | flat binary buffer (24 B/event) |
| `get_core_utilisation` | — | per-core utilisation % + totals |
| `run_verification` | `repoPath: String` | per-tb results + synth status |
| `list_pccx_traces` | `repoPath: String` | list of generated `.pccx` artefacts |
| `load_synth_report` | `utilizationPath`, `timingPath` | `SynthReport` |
| `generate_uvm_sequence_cmd` | `strategy: String` | SV stub text |
| `generate_report` | — | enterprise-mode PDF summary |
| `compress_trace_context` | — | LLM-sized summary string |

## End-to-end testing

The `ui/e2e/` pytest suite covers every step of the pipeline:

| Test | What it proves |
|------|----------------|
| `test_smoke.py`              | UI shell renders, menu + Synth Status tab reachable |
| `test_verify_tb_packer.py`   | `load_pccx` + `get_core_utilisation` report the right trace |
| `test_synth_report.py`       | Vivado report parser extracts the right NPU_top counts + WNS |
| `test_run_verification.py`   | Full suite runs end-to-end + `list_pccx_traces` reflects the output |

Run with:

```bash
cd ui/e2e && .venv/bin/pytest -v
```

## Failure modes and debugging

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `SessionNotCreatedException: Failed to match capabilities` in E2E | Selenium caps missing `browserName=wry` | Already wired in `conftest.py` — if reproduced, inspect `tauri-driver --native-driver` |
| `Tauri IPC not available` in a UI widget | Running via Vite browser preview, not native window | Expected — open via `npm run tauri dev` |
| xvlog `cannot open include file 'FOO.svh'` | Missing `-i` path for the header's directory | Add `-i "$HW_DIR/rtl/<dir>"` to `xvlog` call in `run_verification.sh` |
| `PASS: 0 cycles` on a previously-passing bench | Scoreboard underrun — golden queue empty when `valid_out` asserts | Adjust stimulus / reset timing in the testbench |
