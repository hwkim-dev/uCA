Verification
=============

.. admonition:: Placeholder
   :class: note

   This section is intentionally a stub for now. It will host the
   verification plan, testbench architecture, coverage goals, and
   formal-property results for pccx v002 as they land.

Planned scope
-------------

The full section will cover:

* **Verification plan** — per-module functional coverage targets and
  sign-off criteria.
* **Testbench architecture** — UVM / cocotb harness layout, reference
  model, and stimulus generators (golden data from the ``llm-lite``
  CPU reference).
* **Coverage dashboard** — functional + code + assertion coverage,
  rolled up by core (GEMM / GEMV / CVO / MEM).
* **Formal results** — SymbiYosys / JasperGold properties for the
  controller, ISA decoder, and memory arbitration.
* **Silicon-level checks** — post-implementation simulation, on-board
  bring-up scripts, and golden-trace comparison against the
  :doc:`host-side C driver </docs/v002/Drivers/api>`.

.. seealso::

   :doc:`/docs/v002/Architecture/index`
       The architectural contracts this section verifies.
   :doc:`/docs/v002/ISA/index`
       ISA-level invariants the testbench checks.
   :doc:`/docs/v002/RTL/index`
       RTL modules under test.
