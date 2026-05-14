# Roadmap

The detailed execution board lives in [GitHub Projects][project]. This page
only summarizes the current release direction across the pccx ecosystem.

The release cadence is staged on a shared KV260 bitstream harness.
v002.0 is the baseline integration; v002.1 layers sparsity and
speculative decoding on the same RTL; v003.x moves to a separate RTL
repository as architectural novelties land. A parallel **vision-v001**
track shares the same KV260 substrate but covers CNN-class workloads
(classification / detection) and lives on its own repository.

## Now — v002.0: baseline integration on KV260

- finish remaining RTL integration on `pccx-FPGA-NPU-LLM-kv260`
- A–F baseline phases on the v002.0 release line
  - in progress: Phase 3 step 1 (shape constant RAM unification, see
    {doc}`v002/RTL/shape_const_ram`) and Stage C cleanup (counters,
    constants, `GLOBAL_CONST` consolidation)
- trace-driven verification on `pccx-lab`
- Sail execute increments
- xsim / KV260 baseline bring-up logs
- release evidence checklist (`docs/RELEASE_EVIDENCE_CHECKLIST.md`
  in `pccx-FPGA-NPU-LLM-kv260`) gates timing / throughput / bring-up
  wording before any claim lands in this docs site
- throughput is measured-only on this release line — no timing or
  throughput signoff claim until the verification evidence is published

```{figure} ../_static/diagrams/v002_evidence_flow.svg
:name: fig-v002-evidence-flow-en
:alt: pccx v002 release evidence flow

RTL source → xsim testbenches → synthesis / implementation →
KV260 bring-up `[HW]` → runtime `[HW]` → release evidence checklist
(`RELEASE_EVIDENCE_CHECKLIST.md`) acting as the tag gate. Hardware-gated
stages do not produce numbers that are quoted on this docs site until
the checklist gates them in.
```

Tracking issue: [pccxai/pccx#28 — v0.2.0 umbrella][v020].

## Next — v002.1: sparsity + speculative decoding stack

- same RTL repository (`pccx-FPGA-NPU-LLM-kv260`), continued from v002.0
- v002.1 v12d bitstream + sw/runtime Gemma port (experimental,
  golden-vector gated); see {doc}`v002/gemma3n-e4b-integration`
- G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark phases
- 20 tok/s target lives on this release line
- compute budget for EAGLE head training: $70–100 ($40 if a TRC TPU
  grant lands)

## Later — v003.x: separate RTL repository (LLM line continued)

- v003+ active RTL development lives in
  [`pccx-v003`](https://github.com/pccxai/pccx-v003), the canonical
  v003 IP-core planning package; no v003 release branch has stabilised
  yet (the earlier feeder
  [`pccx-LLM-v003`](https://github.com/pccxai/pccx-LLM-v003) is
  superseded / retired)
- this docs repo will cross-link the v003 IP-core package and CI-clone
  it into `codes/v003/` at build time, the same way it currently
  CI-clones `pccx-FPGA-NPU-LLM-kv260` into `codes/v002/`
- v003.0 — Gemma 4 E4B foundation + first architectural novelty (planning);
  throughput TBD
- v003.1 — second novelty + KV / decoding co-design; throughput TBD
- placeholder track index: {doc}`v003/index`

## Parallel — vision-v001: CNN inference track on KV260

A second product line scoped to **vision** workloads shares the same
KV260 board and the W4A8 NPU substrate but covers a distinct workload
family from the LLM line. Active RTL development will live in a
dedicated repository.

- [`pccx-vision-v001`](https://github.com/pccxai/pccx-vision-v001)
- shared substrate with the LLM line — same KV260 board, same W4A8
  weight × activation ratio, same L2 URAM organisation
- distinct dataflow — dense-conv tile reuse instead of token-by-token
  KV streaming; the GEMM systolic + GEMV hybrid is reused for conv
- first model candidates — ResNet18 / YOLOv8n / MobileNetV3
  (smallest-footprint variants first)
- evidence posture — the same release evidence checklist gates
  timing / throughput / bring-up before any FPS or mAP figure lands
  on this docs site
- placeholder track index: {doc}`vision-v001/index`

## Family overview

```{figure} ../_static/diagrams/pccx_family_tree.svg
:name: fig-pccx-family-tree-en
:alt: pccx product family tree across versions and tracks

v001 (archived) → v002 (active KV260 LLM line: v002.0 → v002.1) →
v003.x (LLM line continued, separate RTL repository). The
**vision-v001** track branches at the v002 KV260 substrate and runs
in parallel on its own repository. Hover any node for status and
scope.
```

## Links

- GitHub Project (source of truth): <https://github.com/orgs/pccxai/projects/1>
- v0.2.0 umbrella: <https://github.com/pccxai/pccx/issues/28>

[project]: https://github.com/orgs/pccxai/projects/1
[v020]: https://github.com/pccxai/pccx/issues/28
