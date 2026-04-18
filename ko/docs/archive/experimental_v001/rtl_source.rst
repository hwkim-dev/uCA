================================
RTL 소스 레퍼런스 (v001)
================================

이 페이지는 :file:`codes/v001/hw/rtl/` 의 v001 RTL 트리에서 핵심
SystemVerilog 소스 파일을 임베드합니다. 모든 파일은 읽기 전용 아카이브
이며, v001 은 더 이상 활발한 개발 대상이 아닙니다.

.. note::

   v002 RTL 은 별도 레포지토리에 있습니다:
   `hwkim-dev/pccx-FPGA-NPU-LLM-kv260
   <https://github.com/hwkim-dev/pccx-FPGA-NPU-LLM-kv260>`_.
   v002 소스는 :doc:`/docs/v002/RTL/index` 참고.

1. ISA 타입 패키지
===================

``isa_pkg.sv`` 는 모든 명령어 인코딩, 오피코드 열거형, 마이크로 옵 구조체의
권위 있는 정의입니다. 모든 RTL 모듈이 ``import isa_pkg::*;`` 로 가져옵니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_pkg.sv
   :language: systemverilog
   :caption: codes/v001/hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_pkg.sv

2. NPU 최상위 모듈
===================

``NPU_top.sv`` 는 모든 서브코어를 연결하고 AXI-Lite 제어 포트, 4 개의
HP 가중치 포트, ACP 피처맵 버스를 노출합니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/NPU_top.sv
   :language: systemverilog
   :lines: 1-80
   :caption: codes/v001/hw/rtl/NPU_top.sv (포트 선언, 첫 80줄)

3. Matrix Core — Systolic Top
==============================

``GEMM_systolic_top.sv`` 는 2-D 시스톨릭 어레이를 감쌉니다. HP0/HP1 에서
가중치 타일을, L2 캐시에서 활성화 행을 받고 결과를 normalizer 에
스트리밍합니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/MAT_CORE/GEMM_systolic_top.sv
   :language: systemverilog
   :caption: codes/v001/hw/rtl/MAT_CORE/GEMM_systolic_top.sv

4. Vector Core — GEMV Top
==========================

``GEMV_top.sv`` 는 4 개의 병렬 GEMV 레인을 인스턴스화합니다. 각 레인은
자기 L1 캐시 슬라이스에서 활성화를, HP2/HP3 에서 가중치를 읽습니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/VEC_CORE/GEMV_top.sv
   :language: systemverilog
   :caption: codes/v001/hw/rtl/VEC_CORE/GEMV_top.sv

5. CVO Core (SFU) Top
======================

``CVO_top.sv`` 는 비선형 연산(Softmax, GELU, RMSNorm, RoPE) 을 위한
CORDIC 및 LUT 기반 함수 유닛을 조율합니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/CVO_CORE/CVO_top.sv
   :language: systemverilog
   :caption: codes/v001/hw/rtl/CVO_CORE/CVO_top.sv

6. NPU Controller Top
======================

``npu_controller_top.sv`` 는 AXI-Lite 프론트엔드, 명령어 디코더,
디스패처, 글로벌 스케줄러를 통합합니다.

.. literalinclude:: ../../../../codes/v001/hw/rtl/NPU_Controller/npu_controller_top.sv
   :language: systemverilog
   :caption: codes/v001/hw/rtl/NPU_Controller/npu_controller_top.sv
