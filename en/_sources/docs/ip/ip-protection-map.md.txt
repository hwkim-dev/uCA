---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use.

# IP protection map

PCCX layers its intellectual property protection so that no single
mechanism is overloaded.

## Layered map

| Layer | What it protects | Where | Status |
| --- | --- | --- | --- |
| Trademark | The `PCCX™` mark and its product designators (`PCCX OpenCore`, `PCCX ProCore`, `PCCX ASICKit`, `PCCX Compatible`) | KIPRIS (KR) | Pending applications: KR Class 09 (`40-2026-0091497`) and Class 42 (`40-2026-0091498`) |
| Copyright | Source code, RTL, documentation | Repository LICENSE + per-file SPDX headers | Apache-2.0 unless otherwise stated; rolled out per [`source-header-inventory.md`](source-header-inventory.md) |
| Patent (categories) | Architectural / quantization / scheduling / compiler / verification *categories* of candidate inventions | Public docs describe categories only | See [`patent-strategy.md`](patent-strategy.md) and [`patent-candidate-intake.md`](patent-candidate-intake.md). Specific candidates live in a private docket. |
| Trade secret | ProCore RTL bundles, enterprise compiler backend, PPA / timing-closure scripts, customer-specific optimisations | Outside this repository, under separate confidentiality controls | See [`trade-secret-policy.md`](trade-secret-policy.md). |
| Contract | CLA, sponsorship terms, commercial-track contracts, investor agreements | Separate executed instruments under applicable law | All draft and pending qualified legal review. |
| Layout-design right | ASIC layout / GDS / mask work | Korea Layout-Designs of Semiconductor ICs Act | Not applicable today (RTL stage); applies once an ASIC layout exists. |

## Public / private boundary

The mapping above is consistent with [`IP_POLICY.md`](../../IP_POLICY.md)
and [`private-disclosure-boundary.md`](private-disclosure-boundary.md).

- Public: Standard, ISA, SDK, simulator, OpenCore, conformance
  harness, documentation.
- Private / commercial: ProCore, Enterprise SDK / compiler backend,
  ASICKit, customer optimisations, PPA / timing scripts, patent
  candidates, trade secrets, layout artefacts.

## When does a layer trigger?

| Trigger | Layer that activates |
| --- | --- |
| New name used in commerce | Trademark — refresh canonical [`TRADEMARKS.md`](../../TRADEMARKS.md) |
| New source file | Copyright — apply header per [`copyright-header-policy.md`](copyright-header-policy.md) |
| Novel idea identified | Patent intake per [`patent-candidate-intake.md`](patent-candidate-intake.md) |
| Information whose value depends on confidentiality | Trade-secret per [`trade-secret-policy.md`](trade-secret-policy.md) |
| New money / IP relationship | Contract — separate written agreement, qualified legal review |
| ASIC layout produced | Layout-design right — register and notice in repo + private docket |
