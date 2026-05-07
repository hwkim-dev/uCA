# pccx v003 — LLM IP-core line

The v003 line continues the **LLM track** from the
{doc}`v002 line <../v002/index>` as a future IP-core package named
`pccx-v003`. Active code is not yet present in this docs site; this page
is a placeholder while the architecture contract is still TBD.

## Working state

- package repository: `pccx-v003` (future)
- repository is not created in this phase
- board and model consumers remain outside the IP-core package
- first-application note — **Gemma 4 E4B** is non-binding until the
  v003 contract is established
- v002.x phases (sparsity, speculative, EAGLE, SSD, Tree, benchmark)
  are *not* repeated here; v003 starts from a different RTL baseline

## Status snapshot

```{table} v003 layer status (placeholder)
:name: tbl-v003-status-en

| Layer            | State                                                           |
|---|---|
| RTL              | TBD                                                             |
| Driver / runtime | shared API surface with v002; no v003-specific path yet         |
| Verification     | inherits the v002 evidence checklist as its release gate        |
| Throughput claim | none — TBD                                                      |
| Timing closure   | none — TBD                                                      |
| Bitstream        | none — TBD                                                      |
```

This page will be expanded as the `pccx-v003` contract lands.

## See also

- {doc}`../roadmap` — release direction across the pccx ecosystem
- {doc}`../v002/index` — current active LLM line (KV260)
- {doc}`../vision-v001/index` — parallel vision track on the same
  substrate
