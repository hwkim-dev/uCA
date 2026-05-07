---
orphan: true
---

# pccx-vision-v001 — current status

> Compatibility / planning track. **No committed RTL evidence.**
> No bitstream, no FPS, no mAP, no timing closure, no board runtime.

`pccxai/pccx-vision-v001` is a **vision-line compatibility track**. Its
purpose is to plan how a future vision substrate fits with the published
v002 IP-core package, not to deliver a vision NPU release today.

## What the repo holds (and does not hold)

| Asset | Status |
| --- | --- |
| Reusable Vision RTL (`rtl/...`) | **Not committed.** |
| Sim / testbench harness | Not committed. |
| Formal model | Not committed. |
| Bitstream / timing-closed implementation | Not produced. |
| FPS / mAP / accuracy benchmark | None measured. |
| Board integration | None. |
| Compatibility manifest with frozen contract values | TBD. |

The repository is therefore a **planning / coordination workspace**, not
a stable release.

## Why it exists separately from `pccx-v002`

`pccx-v002` ships LLM RTL today plus placeholder directories for
`Vision/` and `Voice/`. `pccx-vision-v001` was created so that planning
material for the vision line could move forward without polluting the
v002 package boundaries before a substrate decision is made.

## Default direction

Default direction (subject to issue
[pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)):

- Review whether the vision RTL (when it exists) shares enough common
  substrate with `pccx-v002/common/` and `pccx-v002/LLM/` that absorption
  into `pccx-v002/Vision/` is appropriate.
- If absorption is appropriate, plan the migration steps under
  [`v002-vision-absorption-plan.md`](v002-vision-absorption-plan.md).
- If absorption is not appropriate (different substrate, different
  precision / control bus / driver), the line stays standalone with its
  own contract.

## Tracker

- [pccxai/pccx#65](https://github.com/pccxai/pccx/issues/65)
