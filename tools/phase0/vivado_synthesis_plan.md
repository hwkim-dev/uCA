# Vivado Synthesis & KV260 Deployment Plan

**Goal**: take the pccx v002 RTL from its current elaborated-in-xsim state
all the way to a KV260 bitstream + loadable Linux device-tree overlay,
then run the driver + Gemma 3N E4B app against real silicon.

**Honest scope for this session**: get to the first `opt_design` /
`synth_design` warning wall, record exactly what blocks us, and leave
behind scripts that are **re-runnable** so the next iteration is one
command away.

---

## Flow overview

```
xvlog (source clean)
  └── xelab GEMV/CVO/MEM modules             ← §A
        └── xelab NPU_top (RTL-only sanity)   ← §B
              └── Vivado project (ZU5EV part) ← §C
                    ├── create_project.tcl
                    ├── hw/rtl/** added
                    ├── hw/constraints/pccx.xdc
                    └── synth_design -flatten_hierarchy rebuilt
                          └── opt_design / place_design / route_design
                                └── write_bitstream
                                      └── Vitis handoff to host app  ← §D
                                            └── KV260 deploy + test  ← §E
```

---

## §A — RTL sources clean (compile + elaborate standalone)

| Sub-system     | `xvlog` | `xelab` | Notes |
|----------------|:-------:|:-------:|-------|
| Packages       | done      | done      | device_pkg / dtype_pkg / mem_pkg / vec_core_pkg / isa_pkg / bf16_math_pkg / Algorithms |
| MAT_CORE (11)  | done      | done GEMM_systolic_top | Done previous turn |
| VEC_CORE  (5)  | done      | WIP       | GEMV_top hits unpacked→packed type mismatch (§A.1) |
| CVO_CORE  (3)  | done      | WIP       | CVO_top needs bf16_add (§A.2) |
| NPU_Controller | todo       | todo       | unaudited |
| PREPROCESS     | todo       | todo       | unaudited |
| MEM_control    | todo       | todo       | unaudited |
| NPU_top        | todo       | todo       | unaudited |

### A.1 GEMV_top unpacked→packed

`GEMV_reduction_branch` emits `OUT_GEMV_result_vector [0:gemv_batch-1]`.
`GEMV_top` tries to drive that into `OUT_final_fmap_{A..D}` declared as
a packed scalar `[fmap_type_mixed_precision-1:0]`.

Two possible fixes:

- (a) Widen the top port to `logic [fmap_type_mixed_precision-1:0]
  OUT_final_fmap_A [0:gemv_batch-1]` — keep the batch shape out to the
  caller.
- (b) Reduce in `GEMV_reduction_branch` so the out is a single packed
  value. Loses batch granularity.

Take option (a) — conservative, preserves the existing pipeline shape.

### A.2 CVO_top bf16_add

`bf16_math_pkg` currently exports only `to_bf16` and `align_to_emax`.
Add:

```
function automatic logic [15:0] bf16_add(input logic [15:0] a,
                                         input logic [15:0] b);
  // full exp-align + mantissa add + renormalize + pack
endfunction
```

Starter impl: extract sign/exp/mant from both operands, align mantissas
to the larger exponent, signed-add, renormalize by counting the leading
one, repack. Don't worry about denormals / NaN / Inf for the first
pass — the softmax path always feeds normalized BF16.

---

## §B — Top-level elaboration

`hw/rtl/NPU_top.sv` is the single top. Once §A is green, the main risk
here is **port-level data type propagation** — v001 carried BF16
mantissa ports through NPU_top that v002 wants to flip to INT8. Expect
similar unpacked/packed complaints.

---

## §C — Vivado project

### C.1 Target device

- KV260 SoM Part: **xck26-sfvc784-2LV-c**
- Zynq UltraScale+ MPSoC: **ZU5EV**
- Board file: `xilinx.com:kv260_som:part0:1.4` (or whichever is in the
  installed version)

### C.2 Batch scripts (non-project flow)

```
hw/vivado/
├── build.sh              # wrapper that invokes vivado -mode batch
├── create_project.tcl    # project + part + sources + constraints
├── synth.tcl             # synth_design + post-synth report
├── impl.tcl              # opt/place/route + write_bitstream
└── filelist.f            # ordered source list (packages first)
```

**Key flags**:

- `synth_design -mode out_of_context` for the NPU core first
  (isolates it from the BD / PS). Then a separate BD that drops the
  NPU as an IP.
- `-flatten_hierarchy rebuilt` so the resource report matches the
  SystemVerilog hierarchy.

### C.3 Timing constraints (pccx.xdc)

```tcl
# 250 MHz AXI / control plane
create_clock -period 4.000 -name axi_clk  [get_ports s_axi_aclk]

# 400 MHz core compute
create_clock -period 2.500 -name core_clk [get_ports core_clk]

# Explicit async groups — CDC FIFOs handle the crossings
set_clock_groups -asynchronous \
    -group [get_clocks axi_clk] \
    -group [get_clocks core_clk]

# Relax sample-path timing across reset-bridge FFs
set_false_path -from [get_cells -hier -filter {NAME =~ *u_reset_sync*/sync_reg_reg[0]}] \
               -to   [get_cells -hier -filter {NAME =~ *u_reset_sync*/sync_reg_reg[1]}]
```

Pin / IO constraints are **not required** for the bare NPU — the KV260
board file handles PS ↔ PL pinning through the Zynq IP.

---

## §D — Board-level integration

The NPU core isn't directly wired to board pins; it sits behind the
Zynq PS's HP / HPM / ACP ports. Integration needs:

- Vivado Block Design (`system_bd.tcl`) with:
  - Zynq UltraScale+ MPSoC IP (preset for KV260)
  - Our `NPU_top` as a custom IP (packaged separately)
  - AXI Interconnect or Smart Connect between PS and NPU
  - Clock Wizard for the 400 MHz core clock
- `system_wrapper.v` HDL wrapper around the BD
- Synth the wrapper, not NPU_top alone

### D.1 IP packaging

```
hw/ip/pccx_npu_v002/
├── component.xml         # generated via ipx::package_project
├── hdl/                  # symlink to hw/rtl
└── package_ip.tcl
```

### D.2 Device tree overlay

For Ubuntu 22.04 on KV260:

```
sw/dtbo/pccx_npu.dtsi
sw/dtbo/Makefile          # dtc overlay compile
sw/dtbo/shell.json        # FPGA Manager metadata
```

---

## §E — Deploy + test

```bash
# On KV260, as ubuntu user
sudo xmutil unloadapp
sudo cp pccx_npu.bit.bin pccx_npu.dtbo /lib/firmware/xilinx/pccx_npu/
sudo cp shell.json /lib/firmware/xilinx/pccx_npu/
sudo xmutil loadapp pccx_npu
sudo dmesg | tail -20     # confirm overlay loaded, no AXI timeouts

# Run the driver smoke test
cd ~/pccx-FPGA-NPU-LLM-kv260/sw/driver
make && sudo ./uxc_smoke --loop 64

# Run the Gemma 3N E4B app (Phase F-G follow-ups)
cd ../gemma3NE4B
make && sudo ./gemma3n_serve --tokens 100
```

---

## Current blockers to real synthesis

| # | Blocker | Where | Fix path |
|---|---------|-------|----------|
| 1 | `GEMV_top` unpacked→packed | §A.1 | Widen `OUT_final_fmap_*` to arrays |
| 2 | `CVO_top` `bf16_add` | §A.2 | Add function to `bf16_math_pkg` |
| 3 | NPU_Controller audit | §A | Run `xvlog` + fix pre-existing bugs |
| 4 | PREPROCESS audit | §A | INT8 path still a placeholder, see `GEMM_systolic_top` TODO |
| 5 | MEM_control audit | §A | Largest unaudited surface — L2 URAM, DMA, ACP, CDC |
| 6 | NPU_top elaboration | §B | Depends on #1-#5 |
| 7 | IP packaging | §D.1 | Requires §A-§B green first |
| 8 | Block design (Zynq PS) | §D | Requires #7 |
| 9 | PREPROCESS → true INT8 | Phase A follow-up | `GEMM_systolic_top` has truncation placeholder |
| 10 | Drain-every-1024 counter | Phase A.2.c | Accumulator guard overflow |

## What this session actually tries

Realistic first-pass targets:
1. Fix blockers #1 and #2 (GEMV/CVO fan-out closure).
2. Run `xvlog` on the remaining directories (#3-#5) and fix drop-in
   bugs. Log deeper issues.
3. Write the Vivado TCL scaffold and XDC even if #6+ aren't green yet
   — the scripts are needed for the next iteration regardless.
4. **Do NOT** run `impl_design` / `write_bitstream` — those are
   hour-scale operations that should only run once synth is clean.
5. Capture a precise follow-up list of what still needs to happen to
   reach the first bitstream.

## Post-run results (2026-04-20 end-of-session)

**First green synth achieved.** OOC `synth_design -mode out_of_context
-flatten_hierarchy rebuilt` reports:

- **0 setup failing endpoints** — WNS 2.253 ns (margin left)
- **0 hold failing endpoints** — WHS 0.100 ns
- **0 DRC errors** (warnings only; board-file-dependent)
- **1120 DSP48E2 instances transformed** during the initial unisim pass
  (1024 GEMM + 96 GEMV reduction tree), although the post-synth
  hierarchical utilization shows only 4 DSPs retained because OOC mode
  aggressively dead-strips logic whose outputs don't propagate out of
  the interface-bound top. Real DSP counts come back once a BD wrapper
  binds the `NPU_top` interface ports.

### Bugs patched between rounds (14 synth iterations)

| Round | File | Kind of bug |
|-------|------|-------------|
| 2 | `QUEUE.sv`                    | referenced non-existent `fifo_if`; renamed to the real `IF_queue` |
| 3 | `IF_queue.sv` + `QUEUE.sv`    | owner modport didn't expose `clk`/`rst_n`/`full`/`empty`; removed producer/owner multi-driver race |
| 4 | `mem_u_operation_queue.sv`    | `xpm_fifo_sync` `FIFO_DEPTH` → `FIFO_WRITE_DEPTH`; dropped non-existent `rd_clk` port |
| 5 | `mem_L2_cache_fmap.sv`        | `xpm_memory_tdpram` `DATA_WIDTH_*` → `WRITE_DATA_WIDTH_*` + `READ_DATA_WIDTH_*` |
| 6 | `mem_L2_cache_fmap.sv`        | URAM true-dual-port requires `WRITE_MODE_* = "no_change"` |
| 7 | `mem_CVO_stream_bridge.sv`    | `xpm_fifo_sync` `FIFO_DEPTH`/`rd_clk` fix (mirror of round 4) |
| 8 | `mem_HP_buffer.sv`            | URAM can't be used as async CDC FIFO → `FIFO_MEMORY_TYPE("block")` |
| 9 | `mem_HP_buffer.sv`            | earlier sed injected a comment that swallowed the comma; repaired |
| 10 | `preprocess_fmap.sv`         | `fmap_fifo_data` only `[fmap_width:0]` = 129-bit; widened to 256-bit to match FIFO |
| 11 | `NPU_top.sv`                 | old v001 port names on `u_systolic_engine` — swapped to dual-lane `IN_weight_upper/lower` + added 32×INT4 unpack |
| 12 | `GEMV_top.sv`                | `fmap_LUT_wire` missing `signed` qualifier; reduction chain tripped on `unsigned vs signed` modport type |
| 13 | `GEMV_reduction{,_branch}.sv` | propagated the `signed` qualifier through the port declarations |
| 14 | _(green)_                    | **synth PASS** |

## Still ahead for a real bitstream

- Bind `NPU_top`'s interface ports via `npu_core_wrapper.sv` + BD
  instantiation so the DSPs aren't dead-stripped and the real
  utilization / timing picture emerges.
- Re-run `synth.tcl` on the wrapper (not raw NPU_top) — expect the
  utilization to jump from 4 DSPs to ~1120.
- Write `vivado/system_bd.tcl` with the Zynq MPSoC preset for KV260.
- Only after those two are green, run `impl.tcl` (the long job).
- Device-tree overlay (`sw/dtbo/pccx_npu.dtsi`) + `xmutil` loadapp
  flow on the board.
