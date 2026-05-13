================================
pccx Documentation
================================

Welcome to the **pccx** (Parallel Compute Core eXecutor) documentation.
pccx is a scalable NPU architecture for accelerating Transformer-based LLMs
on edge devices. Select a section from the sidebar to begin.

Ecosystem
---------

.. grid:: 1 1 2 2
   :gutter: 3 4 4 4
   :class-container: pccx-ecosystem-grid

   .. grid-item-card:: :octicon:`cpu;1.5em;sd-mr-2` KV260 integration
      :columns: 12 12 8 8
      :class-card: pccx-hero-card
      :link: https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260
      :link-type: url
      :link-alt: Open the pccx-FPGA-NPU-LLM-kv260 repository on GitHub

      **github.com/pccxai/pccx-FPGA-NPU-LLM-kv260**

      KV260 + LLM application integration for the **v002** line. Reusable
      IP-core sources live in ``pccx-v002``; this repository owns board
      flow, driver handoff, and application wiring.

      **Current focus:** Gemma-3N E4B @ W4A8KV4 remains an evidence-gated
      target. Token-rate, board-run, and timing-closure results are pending
      measured KV260 evidence (see :doc:`docs/Evidence/index`). Everything
      else (v003 / Gemma-4 / Llama) lives on the :doc:`docs/roadmap`.

      Every v002 RTL reference page on this site links back to the exact
      ``.sv`` file in that repository.

   .. grid-item::
      :columns: 12 12 4 4

      .. grid:: 1
         :gutter: 3

         .. grid-item-card:: :octicon:`book;1em;sd-mr-1` Documentation source
            :link: https://github.com/pccxai/pccx
            :link-type: url
            :link-alt: Open the pccx documentation repository on GitHub

            **github.com/pccxai/pccx** — the Sphinx project powering this site.

         .. grid-item-card:: :octicon:`person;1em;sd-mr-1` Author portfolio
            :link: https://hkimw.github.io/hkimw/
            :link-type: url
            :link-alt: Open the hkimw portfolio site

            **hkimw.github.io/hkimw** — blog, other projects, about.

The public ``pccx-v003`` repository now serves as the v003 IP-core
planning package. It is an evidence-gated planning package, not a
stable RTL release. The earlier ``pccx-LLM-v003`` feeder is superseded
/ retired and is no longer an active public track; new reusable v003
LLM material belongs under ``pccx-v003/LLM/``. Board and model
repositories consume v003 material only through explicit compatibility
contracts.

Tooling & Lab
-------------

.. grid:: 1 1 2 2
   :gutter: 3 4 4 4
   :class-container: pccx-toolchain-grid

   .. grid-item-card:: :octicon:`beaker;1.2em;sd-mr-1` pccx-lab
      :link: https://labs.pccx.ai/
      :link-type: url
      :link-alt: Open the pccx-lab verification lab
      :class-card: pccx-lab-card

      CLI-first verification lab for pccx traces, reports, diagnostics,
      and workflow boundaries. GUI, IDE, launcher, and future MCP surfaces
      should reuse the same CLI / core boundary instead of duplicating logic.

      :bdg-warning:`Work in Progress`

      Source: github.com/pccxai/pccx-lab

   .. grid-item-card:: :octicon:`rocket;1.2em;sd-mr-1` PCCX Launcher
      :link: https://launcher.pccx.ai/
      :link-type: url
      :link-alt: Open the PCCX Launcher documentation

      Launcher contracts, runtime-readiness status, device/session summaries,
      and diagnostics handoff records.

      :bdg-warning:`Private source`

   .. grid-item-card:: :octicon:`terminal;1.2em;sd-mr-1` SystemVerilog IDE
      :link: https://ide.pccx.ai/
      :link-type: url
      :link-alt: Open the SystemVerilog IDE documentation

      Editor diagnostics, validation context, declaration navigation, and
      proposal-only workflow surfaces.

      :bdg-warning:`Private source`

   .. grid-item-card:: :octicon:`verified;1.2em;sd-mr-1` Formal model — Sail
      :link: docs/v002/Formal/index
      :link-type: doc
      :link-alt: Read the pccx Sail ISA model

      **pccx is formally specified in** `Sail <https://sail-lang.org/>`_ —
      the same ISA-semantics language used for **RISC-V**, **Arm**,
      **CHERI**, and **Morello**. The 64-bit / 4-bit-opcode v002 ISA
      lives under ``formal/sail/`` in the RTL repo; each SystemVerilog
      ``typedef`` has a 1:1 Sail counterpart so width drift fails
      Sail's type checker before it fails silicon.

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   docs/index
   docs/quickstart
   docs/Evidence/index
   docs/repo-boundaries
   docs/roadmap

.. toctree::
   :maxdepth: 1
   :caption: v002 Architecture

   docs/v002/index

.. toctree::
   :maxdepth: 1
   :caption: Target Hardware

   docs/Devices/index

.. toctree::
   :maxdepth: 1
   :caption: Archive

   docs/archive/index

.. toctree::
   :maxdepth: 1
   :caption: Toolchain Demos

   docs/samples/index

.. toctree::
   :maxdepth: 1
   :caption: Tools

   pccx-lab — Verification Lab <https://labs.pccx.ai/>
   PCCX Launcher <https://launcher.pccx.ai/>
   SystemVerilog IDE <https://ide.pccx.ai/>
