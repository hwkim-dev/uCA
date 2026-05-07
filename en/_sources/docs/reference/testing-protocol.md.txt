---
orphan: true
---

# Testing protocol

Verification is split between the IP-core repository and the board
integration repository. Each layer produces evidence the other layer
can read.

## Sail typecheck (in `pccx-v002`)

- **Where**: `pccxai/pccx-v002/.github/workflows/sail-typecheck.yml`,
  job `typecheck`.
- **What it does**: type-checks the formal Sail ISA model under
  `LLM/formal/sail/` using `sail 0.20.1` and `ocaml 5.1.0`. Triggers
  on push and pull_request that touches `LLM/formal/sail/**` or the
  workflow file itself.
- **Evidence**: workflow run URL on the `pccxai/pccx-v002` actions
  page. A green run is the evidence of model-level type safety for
  the ISA the IP-core declares.
- **Layer responsibility**: Sail belongs with the IP-core because the
  ISA it models belongs with the IP-core. Application repos do not
  duplicate this verification.

## KV260 simulation wrapper (in `pccx-FPGA-NPU-LLM-kv260`)

- **Where**: `scripts/v002/use_submodule_sources.sh` in the board
  integration repo.
- **What it does**: invokes the v002 simulation runner against the
  pinned submodule sources (`third_party/pccx-v002/LLM/sim/`),
  captures the result in `build/sim_v002_submodule.log`. Forwards
  every CLI argument to the underlying runner, so flags the runner
  understands (e.g. `--quick`, `--tb <name>`) work the same way.
- **Evidence**: a `PASS:` summary line in
  `build/sim_v002_submodule.log` and the corresponding per-testbench
  `PASS:` lines.
- **Layer responsibility**: the simulation harness lives with the
  board integration repo because that is where the consumer wires
  the IP-core package into a runnable build.

## Fresh-clone reachability check

- **Where**: any clean checkout under `/tmp/` or a CI runner.
- **What it does**: clones the board integration repo with
  `--recurse-submodules` against HTTPS, then verifies that the
  recorded submodule pin SHA is reachable from `pccx-v002/main`:
  ```
  git clone --recurse-submodules \
      https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260.git
  cd pccx-FPGA-NPU-LLM-kv260/third_party/pccx-v002
  git fetch origin main
  PIN=$(git rev-parse HEAD)
  git merge-base --is-ancestor "$PIN" origin/main
  echo "exit=$?"
  ```
  `exit=0` is the evidence the pin is reachable; `exit=1` is the
  signal that fresh clones will break for new contributors and the
  pin must be repaired (see [submodule pin policy](submodule-pin-policy.md)).
- **Layer responsibility**: the test is run from outside both repos
  because what it verifies is the *outside* clone path, not the
  builder's local cache.

## What evidence each layer produces

| Layer | Evidence artefact | Where it lives |
| --- | --- | --- |
| IP-core (`pccx-v002`) | Sail typecheck run | GitHub Actions on `pccxai/pccx-v002`. |
| Board integration (`pccx-FPGA-NPU-LLM-kv260`) | Sim wrapper log + per-testbench PASS | `build/sim_v002_submodule.log` and `third_party/pccx-v002/LLM/sim/work/<tb>/`. |
| Cross-repo (fresh clone) | Reachability exit code | An ad-hoc clone path; not retained, but the run is reproducible from any clean directory. |
