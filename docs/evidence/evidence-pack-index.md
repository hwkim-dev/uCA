---
orphan: true
---

# Evidence pack index

Index of artefacts that constitute the project's verification and
integration evidence today. Each entry links to the source that
produced the artefact; runs and logs are reproducible from a clean
checkout.

## Verification evidence

| Artefact | Source | Where to look |
| --- | --- | --- |
| Sail typecheck pass on the v002 ISA model | `pccxai/pccx-v002/.github/workflows/sail-typecheck.yml`, job `typecheck`. | GitHub Actions on `pccxai/pccx-v002`; the most recent run on `main` is the live evidence. |
| KV260 sim wrapper PASS summary (11 testbenches) | `pccxai/pccx-FPGA-NPU-LLM-kv260/scripts/v002/use_submodule_sources.sh`. | `build/sim_v002_submodule.log` after a local run. The Phase D2 evidence count was `11 passed / 0 failed`; the same wrapper is what produces the live evidence on main today. |
| Per-testbench artefacts (`xsim.log`, `.pccx`) | Same wrapper; output lands inside the submodule. | `third_party/pccx-v002/LLM/sim/work/<tb>/`. |

## Integration evidence

| Artefact | Source | Where to look |
| --- | --- | --- |
| Submodule pin reachable from `pccx-v002/main` | Cross-repo fresh-clone test. | Reproducible from any clean directory; see [testing protocol](../reference/testing-protocol.md). |
| `repo-validate` gate passing on `pccx-FPGA-NPU-LLM-kv260` | `.github/workflows/validate.yml`. | GitHub Actions on `pccxai/pccx-FPGA-NPU-LLM-kv260`, `repo-validate` job. |
| EN/KO doc set parity, strict Sphinx build, sphinx-lint + codespell, repo-validate | `pccxai/pccx/.github/workflows/`. | GitHub Actions on `pccxai/pccx`. |

## What this page does not contain

- Performance numbers (throughput, latency, area, power). The
  project does not have validated numbers yet; do not infer them
  from intermediate notes.
- Timing closure evidence on KV260. Synth has been attempted; a
  full closure run is pending.
- Application-level model evidence (Gemma 3N E4B end-to-end). The
  runtime handoff smoke is verification of the runtime path, not
  of model accuracy or throughput on hardware.

When the absent items move from TBD to evidence, this index should
gain a new row pointing at the producing source.
