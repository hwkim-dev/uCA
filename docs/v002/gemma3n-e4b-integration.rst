==========================================
v002 Gemma 3N E4B Integration Milestone
==========================================

This page records the coordinated v002 Gemma 3N E4B target path across
the canonical PCCX docs site and the four live debugging surfaces:
pccx-lab Live Run, pccx-trace Live Capture, systemverilog-ide Board
Health, and pccx-launcher chat.

This milestone is evidence-gated — no measured tok/s claims. It documents
target wiring, runtime readiness checks, and golden-vector gates. It does
not claim production readiness or a completed Gemma 3N E4B runtime.

Code and review references:

- KV260 integration code branch:
  https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/tree/docs/v002-gemma-integration
- Canonical docs branch:
  https://github.com/pccxai/pccx/tree/docs/v002-gemma-integration
- PCCX docs issues:
  https://github.com/pccxai/pccx/issues
- KV260 integration issues:
  https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/issues

Milestone Boundary
==================

The coordinated milestone is Stage 1 of staged release:

- pccx-launcher chat provides the user-facing command surface.
- pccx-lab Live Run shows readiness, backend, and NPU status.
- pccx-trace Live Capture streams timeline events from the daemon.
- systemverilog-ide Board Health verifies board status and bitstream
  identity.

Later stages cover NPU GEMM offload and W4A8 golden-vector verification.
Until those gates are reviewed, use "Gemma 3N E4B target path" rather
than production-runtime wording.

Shared Daemon Contract
======================

The live surfaces consume an aiohttp HTTP+WS daemon on port ``7860``. The
common readiness endpoint is ``GET /api/status``.

.. code-block:: json

   {
     "schemaVersion": "pccx.kv260.status.v0",
     "daemon": {
       "transport": "aiohttp",
       "httpPort": 7860,
       "websocketAvailable": true
     },
     "target": {
       "device": "KV260",
       "model": "Gemma 3N E4B target path"
     },
     "bitstream": {
       "candidate": "v12d",
       "sha256": "59558c5f86968be2cd968212be3519afeb7afd148809079a314af29a50cf0c6c",
       "verified": false
     },
     "backend": {
       "mode": "cpu",
       "allowedModes": ["cpu", "npu_uca", "hybrid"]
     },
     "readiness": {
       "state": "blocked",
       "stage": "Stage 1 of staged release",
       "goldenVectorGate": "pending",
       "evidenceGate": "no measured tok/s claims"
     }
   }

Backend modes are interpreted conservatively:

``cpu``
   Numpy or host-side baseline for command and protocol validation.

``npu_uca``
   v002 NPU target path through the PCCX ISA. This stays experimental
   until bitstream identity and golden-vector gates are reviewed.

``hybrid``
   CPU orchestration with selected NPU offload targets. Each offload
   remains separately gated.

The current v12d candidate SHA256 is
``59558c5f86968be2cd968212be3519afeb7afd148809079a314af29a50cf0c6c``.
A SHA match identifies the candidate bitstream only; it is not a
throughput, timing, or runtime signoff.

Live Surface Map
================

.. list-table::
   :header-rows: 1
   :widths: 22 30 28 20

   * - Surface
     - Public route
     - Daemon dependency
     - Issue tracker
   * - pccx-lab Live Run
     - https://labs.pccx.ai/live-run/
     - ``/api/status`` plus optional status WebSocket frames.
     - https://github.com/pccxai/pccx-lab/issues
   * - pccx-trace Live Capture
     - https://trace.pccx.ai/live-capture/
     - ``/api/trace`` NDJSON timeline stream.
     - https://github.com/pccx-internal/pccx-trace/issues
   * - systemverilog-ide Board Health
     - https://ide.pccx.ai/board-health/
     - ``/api/status`` board, backend, and SHA fields.
     - https://github.com/pccxai/systemverilog-ide/issues
   * - pccx-launcher chat
     - https://launcher.pccx.ai/chat/
     - ``/api/status`` preflight plus chat WebSocket events.
     - https://github.com/pccxai/pccx-launcher/issues

Release Wording Rules
=====================

Use the following wording while this milestone is under review:

- "Gemma 3N E4B target path"
- "runtime readiness checks"
- "experimental"
- "golden-vector gated"
- "Stage 1 of staged release"
- "evidence-gated — no measured tok/s claims"

Avoid wording that says or implies:

- measured token rate or latency;
- production readiness;
- completed on-board model execution;
- timing, bitstream, or runtime signoff;
- FPS or application benchmark results.

Where to File Issues
====================

File canonical documentation issues in:
https://github.com/pccxai/pccx/issues

File daemon, board integration, bitstream, and golden-vector evidence
issues in:
https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260/issues

When filing an issue, include the daemon URL pattern, backend mode,
``/api/status`` payload, v12d SHA match state, and which live debug
surface exposed the problem. Do not include secrets, private model paths,
or unreviewed measurements.
