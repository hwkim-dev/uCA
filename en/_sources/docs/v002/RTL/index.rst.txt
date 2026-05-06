==============================
RTL Source Reference (v002)
==============================

This section embeds key SystemVerilog modules from the pccx v002 RTL
repository: `pccxai/pccx-FPGA-NPU-LLM-kv260
<https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260>`_.

The RTL is cloned into :file:`codes/v002/` at CI build time. Local
development requires a manual clone:

.. code-block:: bash

   git clone https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260 codes/v002

.. toctree::
   :maxdepth: 1

   isa_pkg
   npu_top
   compute_cores
   controller
   frontend
   memory_l2
   memory_dispatch
   shape_const_ram
   preprocess
   packages
   library

Module status matrix (release-line v002.0)
==========================================

.. list-table:: pccx v002 RTL module status (release-line v002.0)
   :name: tbl-v002-rtl-status-en
   :header-rows: 1
   :widths: 35 35 30

   * - Module / page
     - Phase status
     - Last verified against
   * - :doc:`isa_pkg`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`npu_top`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`compute_cores`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`controller`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`frontend`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`memory_l2`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`memory_dispatch`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`shape_const_ram`
     - in progress (Phase 3 step 1 migration)
     - ``18d4631`` (2026-05-06)
   * - :doc:`preprocess`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`packages`
     - landed
     - ``8c09e5e`` (2026-04-29)
   * - :doc:`library`
     - landed
     - ``8c09e5e`` (2026-04-29)

The "Last verified against" column tracks the upstream commit at which
each page's RTL excerpt and behaviour description were last reviewed.
"in progress" entries are subject to change while the migration lands.
