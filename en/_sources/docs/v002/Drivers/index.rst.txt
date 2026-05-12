==================
Software Stack
==================

The pccx v002 driver is a C/C++ hardware abstraction layer (HAL)
plus a thin public API. Its responsibilities:

- Encoding and dispatching 64-bit VLIW instructions via the CMD_IN FIFO.
- Preloading shape / size pointers and scale factors through ``MEMSET``.
- Driving DMA between the host DDR4 and the NPU L2 cache.
- Polling ``STAT_OUT`` for async completion.

The implementation lives under
:file:`codes/v002/sw/driver/uCA_v1_api.h` /
:file:`uCA_v1_api.c` and carries forward the v001 design with minor
comment updates for the pccx v002 ISA reference URL.

.. admonition:: Implementation status
   :class: warning

   v002 driver is at **bring-up** stage: the public ``uca_*`` API
   surface compiles and the AXI-Lite HAL skeleton exists, but the
   end-to-end ``MEMSET → MEMCPY → GEMV → MEMCPY readback`` flow has
   not yet been validated against the RTL on hardware. See
   :doc:`../Verification/index` §2 for the open verification items.

.. admonition:: Local LLM launcher — status surface boundary
   :class: note

   Driver bring-up is being mirrored at the launcher boundary by
   ``pccx-launcher``. The launcher's chat surface gates inputs and
   outputs through a documented set of boundaries — chat status
   summary, evidence manifest, gap matrix, review packet, redaction
   policy, clipboard policy, accessibility, and empty-state — none of
   which produce hardware-measured numbers at this stage. The launcher
   is referenced here so contributors can locate the workflow
   boundary; runtime / inference numbers will appear here only after
   the release evidence checklist gates them in.

.. toctree::
   :maxdepth: 1

   api
   hal
