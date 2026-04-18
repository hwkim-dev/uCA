pccx ISA 사양
================

**pccx** (Parallel Compute Core eXecutor) — FPGA NPU 명령어 집합.

타겟: Kria KV260 \| 워드 폭: **64-bit** \| 인코딩: **VLIW**

RTL 소스: ``hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/``

--------------

1. 명령어 포맷
---------------

모든 명령어는 64 비트 폭입니다.

::

    [63:60]   [59:0]
    OPCODE    BODY (60 bits, layout depends on opcode)

최상위 디코더(``ctrl_npu_decoder.sv``)가 4 비트 오피코드를 떼어내고
남은 60 비트 본문을 해당 실행 엔진으로 라우팅합니다.

--------------

2. 오피코드 테이블
-------------------

.. list-table::
   :header-rows: 1
   :widths: 16 24 12 48

   * - Opcode
     - 니모닉
     - 값
     - 타겟 엔진
   * - ``OP_GEMV``
     - Vector–Matrix Multiply
     - ``4'h0``
     - Vector Core (μV-Cores)
   * - ``OP_GEMM``
     - Matrix–Matrix Multiply
     - ``4'h1``
     - Matrix Core (Systolic Array)
   * - ``OP_MEMCPY``
     - Memory Copy
     - ``4'h2``
     - MEM Dispatcher
   * - ``OP_MEMSET``
     - Memory Set
     - ``4'h3``
     - MEM Dispatcher
   * - ``OP_CVO``
     - Complex Vector Op
     - ``4'h4``
     - CVO Core (μCVO-Cores)
   * - —
     - Reserved
     - ``4'h5``–``4'hF``
     - —

--------------

3. 명령어 인코딩
-----------------

3.1 GEMV / GEMM (``OP_GEMV``, ``OP_GEMM``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

둘 다 동일한 본문 레이아웃을 공유합니다.

::

   [59:43]  dest_reg       17-bit  목적 레지스터 / 주소
   [42:26]  src_addr       17-bit  소스 주소
   [25:20]  flags           6-bit  제어 플래그 (§4 참고)
   [19:14]  size_ptr_addr   6-bit  size 디스크립터 포인터
   [13:8]   shape_ptr_addr  6-bit  shape 디스크립터 포인터
   [7:3]    parallel_lane   5-bit  활성 병렬 레인 수
   [2:0]    reserved        3-bit

3.2 MEMCPY (``OP_MEMCPY``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   [59]     from_device     1-bit  0=FROM_NPU, 1=FROM_HOST
   [58]     to_device       1-bit  0=TO_NPU,   1=TO_HOST
   [57:41]  dest_addr      17-bit  목적 주소
   [40:24]  src_addr       17-bit  소스 주소
   [23:7]   aux_addr       17-bit  보조 주소 (예약)
   [6:1]    shape_ptr_addr  6-bit  shape 디스크립터 포인터
   [0]      async           1-bit  0=sync, 1=async 전송

3.3 MEMSET (``OP_MEMSET``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   [59:58]  dest_cache      2-bit  0=fmap_shape, 1=weight_shape
   [57:52]  dest_addr       6-bit  목적 포인터 주소 (ptr_addr_t)
   [51:36]  a_value        16-bit  값 A
   [35:20]  b_value        16-bit  값 B
   [19:4]   c_value        16-bit  값 C
   [3:0]    reserved        4-bit

3.4 CVO (``OP_CVO``)
~~~~~~~~~~~~~~~~~~~~

CVO Core(2× μCVO-Cores) 로 디스패치. 각 μCVO-Core 는 CORDIC 유닛
(sin/cos) 과 SFU (exp, sqrt, GELU) 를 포함. Transformer softmax,
RMSNorm, 활성화 함수에 필수.

::

   [59:56]  cvo_func        4-bit  함수 코드 (§3.4.1 참고)
   [55:39]  src_addr       17-bit  L2 캐시 소스 주소
   [38:22]  dst_addr       17-bit  L2 캐시 목적 주소
   [21:6]   length         16-bit  원소 개수 (벡터 길이)
   [5:1]    flags           5-bit  제어 플래그 (§3.4.2 참고)
   [0]      async           1-bit  0=sync, 1=async

3.4.1 CVO 함수 코드
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 10 22 50 18

   * - 코드
     - 니모닉
     - 설명
     - HW 유닛
   * - ``4'h0``
     - ``CVO_EXP``
     - 원소별 exp(x)
     - SFU
   * - ``4'h1``
     - ``CVO_SQRT``
     - 원소별 sqrt(x)
     - SFU
   * - ``4'h2``
     - ``CVO_GELU``
     - 원소별 GELU(x)
     - SFU
   * - ``4'h3``
     - ``CVO_SIN``
     - 원소별 sin(x)
     - CORDIC
   * - ``4'h4``
     - ``CVO_COS``
     - 원소별 cos(x)
     - CORDIC
   * - ``4'h5``
     - ``CVO_REDUCE_SUM``
     - 전체 합 → dst_addr 에 스칼라
     - SFU + Adder
   * - ``4'h6``
     - ``CVO_SCALE``
     - src_addr+0 의 스칼라로 원소별 곱셈
     - SFU
   * - ``4'h7``
     - ``CVO_RECIP``
     - 원소별 1/x
     - SFU
   * - ``4'h8``–``4'hF``
     - —
     - 예약
     - —

..

   **Softmax 시퀀스** (1 번의 CVO 파이프라인 패스): 1. ``OP_GEMV`` +
   ``FLAG_FINDEMAX`` — attention score 의 e_max 탐색 2.
   ``OP_CVO CVO_EXP`` + ``FLAG_SUB_EMAX`` — 각 score 에 exp(x − e_max)
   3. ``OP_CVO CVO_REDUCE_SUM`` — exp 합 (분모) 4.
   ``OP_CVO CVO_SCALE`` + ``FLAG_RECIP_SCALE`` — 각 exp 를 합으로 나눔

   **RMSNorm 시퀀스**: 1. ``OP_GEMV`` + ``FLAG_FINDEMAX`` 를 projection
   동안 수행 (emax 추적) 2. ``OP_CVO CVO_REDUCE_SUM`` (제곱합) → 3.
   ``OP_CVO CVO_SQRT`` + ``CVO_RECIP`` → 정규화 인자 4.
   ``OP_CVO CVO_SCALE`` — 학습된 가중치 γ 적용

3.4.2 CVO 플래그 (5-bit, body 의 [5:1])
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   [5]  sub_emax      연산 전에 e_max 를 빼기 (사전 FINDEMAX 필요)
   [4]  recip_scale   SCALE 을 나눗셈으로 처리 (곱하기 대신 스칼라의 역수 사용)
   [3]  accm          dst 에 누산 (덮어쓰지 않음)
   [2:1] reserved

--------------

4. GEMV/GEMM Flags 필드 (6-bit, [25:20])
------------------------------------------

::

   [5]  findemax   출력 정규화를 위한 지수 최대값(e_max) 탐색 및 등록
   [4]  accm       결과를 목적 레지스터에 누산 (덮어쓰지 않음)
   [3]  w_scale    MAC 시 weight scale factor 적용
   [2:0] reserved

--------------

5. Memory 라우팅 테이블 (MEMCPY)
----------------------------------

``isa_memctrl.svh`` 의 ``data_route_e`` 로 정의.

.. list-table::
   :header-rows: 1
   :widths: 30 16 54

   * - 라우트 Enum
     - 인코딩 (``src[3:0]|dst[3:0]``)
     - 설명
   * - ``from_host_to_L2``
     - ``8'h01``
     - Host DDR4 → L2 캐시 (fmap DMA in via ACP)
   * - ``from_L2_to_host``
     - ``8'h10``
     - L2 캐시 → Host DDR4 (result DMA out via ACP)
   * - ``from_L2_to_L1_GEMM``
     - ``8'h12``
     - L2 → Matrix Core fmap 브로드캐스트
   * - ``from_L2_to_L1_GEMV``
     - ``8'h13``
     - L2 → Vector Core fmap 브로드캐스트
   * - ``from_L2_to_CVO``
     - ``8'h14``
     - L2 → CVO Core 입력 스트림
   * - ``from_GEMV_res_to_L2``
     - ``8'h31``
     - Vector Core 결과 → L2 캐시
   * - ``from_GEMM_res_to_L2``
     - ``8'h21``
     - Matrix Core 결과 → L2 캐시
   * - ``from_CVO_res_to_L2``
     - ``8'h41``
     - CVO Core 결과 → L2 캐시

--------------

6. 마이크로 옵 (uop) 구조체
-----------------------------

디코드 후 Global Scheduler 가 명령어 본문을 엔진별 마이크로 옵으로
분할하여 디스패치합니다.

6.1 GEMV / GEMM Control uop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: systemverilog

   typedef struct packed {
       flags_t         flags;           // 6-bit
       ptr_addr_t      size_ptr_addr;   // 6-bit
       parallel_lane_t parallel_lane;   // 5-bit
   } gemv_control_uop_t;  // = gemm_control_uop_t

6.2 Memory Control uop
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: systemverilog

   typedef struct packed {
       data_route_e data_dest;      // 8-bit  (source[3:0] | dest[3:0])
       dest_addr_t  dest_addr;      // 17-bit
       src_addr_t   src_addr;       // 17-bit
       ptr_addr_t   shape_ptr_addr; // 6-bit
       async_e      async;          // 1-bit
   } memory_control_uop_t;

6.3 Memory Set uop
~~~~~~~~~~~~~~~~~~~

.. code:: systemverilog

   typedef struct packed {
       dest_cache_e dest_cache;  // 2-bit
       ptr_addr_t   dest_addr;   // 6-bit
       a_value_t    a_value;
       b_value_t    b_value;
       c_value_t    c_value;
   } memory_set_uop_t;

6.4 CVO Control uop
~~~~~~~~~~~~~~~~~~~~

.. code:: systemverilog

   typedef struct packed {
       cvo_func_e  cvo_func;     // 4-bit
       src_addr_t  src_addr;     // 17-bit
       dst_addr_t  dst_addr;     // 17-bit
       length_t    length;       // 16-bit
       cvo_flags_t flags;        // 5-bit
       async_e     async;        // 1-bit
   } cvo_control_uop_t;

--------------

7. 분리형 데이터플로우 파이프라인
-----------------------------------

프론트엔드와 실행 엔진은 엄격히 분리되어 있습니다.

::

   Host (AXI-Lite) --> [AXIL_CMD_IN] --> ctrl_npu_decoder
                                               |
                      +----------+------+------+------+-----------+
                      v          v      v             v           v
                 GEMV FIFO  GEMM FIFO  CVO FIFO  MEM FIFO    MEMSET FIFO
                      |          |      |             |           |
                 μV-Core    Systolic  μCVO-Core  mem_dispatcher  mem_set
                (GEMV)    Array(GEMM) (CVO)

프론트엔드(``ctrl_npu_decoder``) 는 엔진별 FIFO 에 명령어를 밀어넣고
바로 반환 — 실행 완료를 기다리며 멈추지 않습니다. 각 엔진의 로컬
디스패처는 FIFO 에서 독립적으로 pop 하고 오퍼랜드가 준비되면 실행합니다.

--------------

8. AXI-Lite 레지스터 맵
------------------------

제어는 ``S_AXIL_CTRL`` (KV260 의 HPM 포트) 를 통해 이루어집니다.

.. list-table::
   :header-rows: 1
   :widths: 12 14 12 62

   * - 오프셋
     - 폭
     - 방향
     - 설명
   * - ``0x00``
     - 32-bit
     - W
     - VLIW 명령어 [31:0] (하위 워드 먼저 쓰기)
   * - ``0x04``
     - 32-bit
     - W
     - VLIW 명령어 [63:32] (이 워드를 쓰면 NPU latch 트리거)
   * - ``0x08``
     - 32-bit
     - R
     - NPU 상태 레지스터 (§9 참고)

--------------

9. 상태 레지스터 (``0x08``)
-----------------------------

====== ======== ===============================================
비트   이름     설명
====== ======== ===============================================
[0]    ``BUSY`` NPU 실행 중 — 새 명령어를 발행하지 말 것
[1]    ``DONE`` 마지막 연산이 성공적으로 완료됨
[31:2] —        예약
====== ======== ===============================================
