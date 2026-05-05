# Roadmap

The detailed execution board lives in [GitHub Projects][project]. This page
only summarizes the current release direction across the pccx ecosystem.

The release cadence is staged on a shared KV260 bitstream harness.
v002.0 is the baseline integration; v002.1 layers sparsity and
speculative decoding on the same RTL.

## Now — v002.0: baseline integration on KV260

- finish remaining RTL integration on `pccx-FPGA-NPU-LLM-kv260`
- A–F baseline phases on the v002.0 release line
- trace-driven verification on `pccx-lab`
- Sail execute increments
- xsim / KV260 baseline bring-up logs
- throughput is measured-only on this release line — no timing or
  throughput signoff claim until the verification evidence is published

Tracking issue: [pccxai/pccx#28 — v0.2.0 umbrella][v020].

## Next — v002.1: sparsity + speculative decoding stack

- same RTL repository (`pccx-FPGA-NPU-LLM-kv260`), continued from v002.0
- G sparsity / H–H+ EAGLE-3 / I SSD / J Tree / K benchmark phases
- 20 tok/s target lives on this release line
- compute budget for EAGLE head training: $70–100 ($40 if a TRC TPU
  grant lands)

## Links

- GitHub Project (source of truth): <https://github.com/orgs/pccxai/projects/1>
- v0.2.0 umbrella: <https://github.com/pccxai/pccx/issues/28>

[project]: https://github.com/orgs/pccxai/projects/1
[v020]: https://github.com/pccxai/pccx/issues/28
