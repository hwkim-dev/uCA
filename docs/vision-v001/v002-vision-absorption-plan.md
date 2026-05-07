---
orphan: true
---

# Absorption plan — vision-v001 → `pccx-v002/Vision/`

> Draft / planning / evidence-gated.
> No vision RTL has been committed yet. The plan below is a framework
> for the day vision RTL exists, not a current migration in flight.

## Pre-conditions for absorption

Absorption is only justified if **all** of the following hold:

1. Vision RTL exists in `pccx-vision-v001` (or in a private staging
   workspace) at a level of completeness comparable to the v002 LLM
   substrate.
2. The vision RTL shares the v002 common substrate
   (`pccx-v002/common/rtl/packages/`,
   `pccx-v002/common/rtl/interfaces/`,
   `pccx-v002/common/rtl/wrappers/`) without conflicting redefinitions.
3. The vision-side ISA, register ABI, and control bus are compatible
   with the v002 contract — or the divergence is small enough that a
   single shared contract still describes both.
4. No KV260- / model-specific tokens inside the to-be-absorbed RTL paths
   (the IP-core boundary rule still applies).

If any of (1)–(4) fail, the line stays standalone and the package
target moves to `pccx-v003/Vision/` (or `pccx-vision-vNNN`) instead.

## Migration outline (when triggered)

1. **Inventory**: list every file in `pccx-vision-v001` and classify
   it as IP-core / spec / model-specific.
2. **Dependency audit**: identify which `common/rtl/` modules are
   shared with v002, which are vision-only.
3. **Boundary review**: confirm no `kv260`, `kria`, `gemma`, model
   weights, or board names appear in candidate `rtl/` paths.
4. **Branch in `pccx-v002`** with new `Vision/rtl/`, `Vision/sim/`,
   `Vision/tb/`, `Vision/formal/` directories populated from the
   reviewed inventory.
5. **Source manifest**: update `pccx-v002/SOURCE_MANIFEST.md` with
   the new mappings.
6. **Compatibility contract**: extend `compatibility/v002-contract.yaml`
   with vision-relevant fields (input formats, weight format if
   different, control bus revision).
7. **Verification**: run the existing Sail typecheck workflow, the
   sim harness (extended for vision testbenches), and a fresh-clone
   reachability check.
8. **Pin update**: any consumer that depends on a future vision
   integration pins the new `pccx-v002` SHA after the merge.

## What this plan is *not*

- It is **not** an implementation schedule.
- It does **not** claim a pre-decided absorption.
- It does **not** assume vision RTL exists today.

## Tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
