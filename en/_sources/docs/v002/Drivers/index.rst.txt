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

.. toctree::
   :maxdepth: 1

   api
