# Roadmap

The detailed execution board lives in [GitHub Projects][project]. This page
only summarizes the current release direction across the pccx ecosystem.

The release cadence is staged on a shared KV260 bitstream harness. v002.0
is the baseline integration; v002.1 layers sparsity and speculative
decoding on the same RTL; v003.x moves to a separate RTL repository as
architectural novelties land.

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
- G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark phases
- 20 tok/s target lives on this release line
- compute budget for EAGLE head training: $70–100 ($40 if a TRC TPU
  grant lands)

## Later — v003.x: separate RTL repository

- v003+ active RTL development moves to a dedicated repository, working
  name `pccx-FPGA-NPU-LLM-v003`, public URL TBD; the v003 RTL
  repository has not been created yet
- this docs repo will cross-link the v003 RTL repository and CI-clone it
  into `codes/v003/` at build time, the same way it currently CI-clones
  `pccx-FPGA-NPU-LLM-kv260` into `codes/v002/`
- v003.0 — Gemma 4 E4B foundation + first architectural novelty;
  throughput TBD
- v003.1 — second novelty + KV/decoding co-design; throughput TBD

## Links

- GitHub Project (source of truth): <https://github.com/orgs/pccxai/projects/1>
- v0.2.0 umbrella: <https://github.com/pccxai/pccx/issues/28>

[project]: https://github.com/orgs/pccxai/projects/1
[v020]: https://github.com/pccxai/pccx/issues/28
