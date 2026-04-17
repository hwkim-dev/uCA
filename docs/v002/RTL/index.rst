==============================
RTL Source Reference (v002)
==============================

This section embeds key SystemVerilog modules from the pccx v002 RTL
repository: `hwkim-dev/NPU-FPGA-Transformer-Accelerator-KV260
<https://github.com/hwkim-dev/NPU-FPGA-Transformer-Accelerator-KV260>`_.

The RTL is cloned into :file:`codes/v002/` at CI build time. Local
development requires a manual clone:

.. code-block:: bash

   git clone https://github.com/hwkim-dev/NPU-FPGA-Transformer-Accelerator-KV260 codes/v002

.. toctree::
   :maxdepth: 1

   isa_pkg
   npu_top
   compute_cores
   controller
