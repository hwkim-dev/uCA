# pccx v003 — LLM line, separate RTL repository

The v003 line continues the **LLM track** from the
{doc}`v002 line <../v002/index>` on a dedicated RTL repository.
Active code is not yet present in this docs site — this page is a
placeholder while the upstream RTL repository stabilises.

## Working state

- working repository name: `pccx-LLM-v003`, public URL TBD
- working staging repository: `pccx-LLM-v003-staging` (private)
- repositories created in evidence-tracked state; no release branch
  has stabilised yet
- shared substrate with v002 — same KV260 board, same W4A8 weight ×
  activation ratio, same L2 URAM organisation
- first model focus — **Gemma 4 E4B** as the foundation, with one
  architectural novelty layered on top per release point (v003.0,
  v003.1)
- v002.x phases (sparsity, speculative, EAGLE, SSD, Tree, benchmark)
  are *not* repeated here; v003 starts from a different RTL baseline

## Status snapshot

```{table} v003 layer status (placeholder)
:name: tbl-v003-status-en

| Layer            | State                                                           |
|---|---|
| RTL              | not yet committed in the v003 repository                        |
| Driver / runtime | shared API surface with v002; no v003-specific path yet         |
| Verification     | inherits the v002 evidence checklist as its release gate        |
| Throughput claim | none — TBD                                                      |
| Timing closure   | none — TBD                                                      |
| Bitstream        | none — TBD                                                      |
```

This page will be expanded as the upstream RTL repository lands.

## See also

- {doc}`../roadmap` — release direction across the pccx ecosystem
- {doc}`../v002/index` — current active LLM line (KV260)
- {doc}`../vision-v001/index` — parallel vision track on the same
  substrate
