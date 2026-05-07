---
orphan: true
---

# Getting started

The shortest reproducible path from a clean checkout to a passing
verification run.

## Clone the application repo with submodules

```
git clone --recurse-submodules \
    https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260.git
cd pccx-FPGA-NPU-LLM-kv260
```

The `--recurse-submodules` flag is mandatory. The board integration
repo consumes the v002 IP-core through the
`third_party/pccx-v002` submodule and a clone without it will not
build. If you forgot the flag, run `git submodule update --init
--recursive` from inside the working tree.

## Toolchain expectations

| Tool | Used for | Where |
| --- | --- | --- |
| `git` | repo + submodule operations | local |
| `bash` | wrapper scripts | local |
| `gh` (GitHub CLI) | PR / Actions queries | local |
| Vivado xsim (`xvlog`, `xelab`, `xsim`) | KV260 sim wrapper | local; expected on `PATH` |
| `opam` + `sail 0.20.1` + `ocaml 5.1.0` + `z3` | Sail typecheck (CI) | runs in `pccx-v002` GitHub Actions; local install optional |
| `python3` | helper scripts (smoke program generator etc.) | local |

The `pccx-FPGA-NPU-LLM-kv260` repo expects a sibling `pccx-lab`
checkout (or `PCCX_LAB_DIR` set) for trace inspection; its absence
does not block the sim wrapper, only the trace viewing.

## Run the v002 simulation suite via the wrapper

```
bash scripts/v002/use_submodule_sources.sh
tail -n 5 build/sim_v002_submodule.log
```

The wrapper forwards arguments to the v002 runner inside the
submodule. Quick smoke and per-testbench modes work the same way:

```
bash scripts/v002/use_submodule_sources.sh --quick
bash scripts/v002/use_submodule_sources.sh --tb tb_v002_runtime_smoke_program
```

A successful run prints `PASS: submodule simulation complete` and the
log tail shows a per-testbench `Summary: <N> passed, 0 failed` block.

## Check the formal Sail model (optional, normally CI-only)

The Sail typecheck runs in `pccxai/pccx-v002` GitHub Actions on every
push that touches `LLM/formal/sail/**`. To run it locally:

```
cd third_party/pccx-v002/LLM/formal/sail
make check
```

This requires `sail`, `z3`, and `opam` available on `PATH`. The CI
job does the cold opam build for you; running locally is mainly
useful when iterating on the Sail model.

## Verify the submodule pin is reachable from `pccx-v002/main`

```
cd third_party/pccx-v002
git fetch origin main
PIN=$(git rev-parse HEAD)
git merge-base --is-ancestor "$PIN" origin/main
echo "exit=$?"
```

`exit=0` is the expected outcome. `exit=1` means the pin needs
repair; see [submodule pin policy](../reference/submodule-pin-policy.md).

## Where evidence lives

| Evidence | Where to look |
| --- | --- |
| Sail typecheck run | GitHub Actions on `pccxai/pccx-v002`. |
| Sim wrapper summary | `build/sim_v002_submodule.log` in the board integration checkout. |
| Per-testbench artefacts | `third_party/pccx-v002/LLM/sim/work/<tb>/` after a wrapper run. |
| CI status of any open PR | `gh pr checks <number> --repo <repo>`. |
