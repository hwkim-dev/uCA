==============================
RTL 소스 레퍼런스 (v002)
==============================

이 섹션은 pccx v002 RTL 레포지토리의 핵심 SystemVerilog 모듈을
직접 임베드한다: `pccxai/pccx-FPGA-NPU-LLM-kv260
<https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260>`_.

RTL은 CI 빌드 시 :file:`codes/v002/`\ 에 자동 clone된다. 로컬 개발에서는
아래 명령으로 직접 clone한다:

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

모듈 상태 매트릭스 (릴리스 라인 v002.0)
========================================

.. list-table:: pccx v002 RTL 모듈 상태 (릴리스 라인 v002.0)
   :name: tbl-v002-rtl-status-ko
   :header-rows: 1
   :widths: 35 35 30

   * - 모듈 / 페이지
     - 단계 상태
     - 마지막 검증 대상
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
     - 진행 중 (Phase 3 step 1 마이그레이션)
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

"마지막 검증 대상" 컬럼은 각 페이지의 RTL 인용 / 동작 설명이 마지막
으로 리뷰된 업스트림 커밋을 추적한다. "진행 중" 표시는 마이그레이션
이 안정될 때까지 변경될 수 있다.
