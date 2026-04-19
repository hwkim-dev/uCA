==================
C API 개요
==================

v002 드라이버의 공개 C API 를 정리합니다. 구현은
``codes/v002/sw/driver/`` 아래 ``uCA_v1_api.h`` / ``uCA_v1_hal.h`` 에
위치합니다.

스택은 두 계층으로 나뉩니다.

1. **HAL** (``uca_hal_*``) — AXI-Lite / AXI-HP 레지스터와 CMD_IN /
   STAT_OUT FIFO 에 직접 접근. 일반 애플리케이션은 이 계층을 직접
   호출하지 않는다.
2. **Public API** (``uca_*``) — "CUDA 대응" 수준의 연산·메모리
   프리미티브. 모든 호출이 64-bit VLIW 명령어를 조립해
   (:doc:`../ISA/encoding`) HAL 을 통해 발행한다.

.. note::

   API 네임스페이스는 ``uca_*`` 이며 ``pccx_*`` 가 아니다. pccx 는
   아키텍처 / 문서 프로젝트 이름이고, uCA (micro Compute
   Architecture) 가 RTL·소프트웨어 계약의 네이밍이다.

1. 초기화 & 라이프사이클
=========================

.. code-block:: c

   #include "uCA_v1_api.h"

   // NPU 부팅과 STAT 응답 확인. 성공 시 0, 실패 시 -1.
   int  uca_init(void);

   // NPU 를 안전 상태로 두고 HAL 해제.
   void uca_deinit(void);

API 는 **컨텍스트 포인터를 쓰지 않는다** — 한 프로세스가 NPU 하나와
만 통신하므로 HAL 이 file-scope 싱글턴으로 상태를 보관한다.

2. 연산 프리미티브
===================

모든 연산 호출은 CMD_IN FIFO 에 명령어를 기록한 뒤 **즉시 반환** 한다.
완료를 기다리려면 ``uca_sync`` (§5) 를 호출한다.

2.1 Vector Core — ``uca_gemv``
-------------------------------

.. code-block:: c

   // y = W · x  (INT4 가중치 × BF16/INT8 액티베이션 → BF16 결과)
   void uca_gemv(uint32_t dest_reg,   // 17-bit L2 목적지
                 uint32_t src_addr,   // 17-bit L2 소스 (액티베이션)
                 uint8_t  flags,      // UCA_FLAG_* OR (§4.1)
                 uint8_t  size_ptr,   // 6-bit size 포인터
                 uint8_t  shape_ptr,  // 6-bit shape 포인터
                 uint8_t  lanes);     // 5-bit 병렬 레인 마스크 (1–4)

2.2 Matrix Core — ``uca_gemm``
-------------------------------

.. code-block:: c

   // Y = W · X 를 32 × 32 시스톨릭 어레이에서 수행.
   // 필드 레이아웃은 uca_gemv 와 동일하며, 디스패처에서 opcode 만 다르게
   // 라우팅된다.
   void uca_gemm(uint32_t dest_reg,
                 uint32_t src_addr,
                 uint8_t  flags,
                 uint8_t  size_ptr,
                 uint8_t  shape_ptr,
                 uint8_t  lanes);

2.3 CVO / SFU — ``uca_cvo``
----------------------------

.. code-block:: c

   // 비선형 연산:
   //   Softmax     (EXP, REDUCE_SUM, SCALE)
   //   RMSNorm     (SQRT, RECIP, SCALE)
   //   활성화 함수 (GELU)
   //   RoPE        (SIN / COS)
   void uca_cvo(uint8_t  cvo_func,    // UCA_CVO_* (§4.3)
                uint32_t src_addr,    // 17-bit L2 소스
                uint32_t dst_addr,    // 17-bit L2 목적지
                uint16_t length,      // 원소 개수
                uint8_t  flags,       // UCA_CVO_FLAG_* OR
                uint8_t  async);      // 1 = fire-and-forget, 0 = block

3. 메모리 프리미티브
=====================

3.1 ``uca_memcpy``
-------------------

.. code-block:: c

   // 루트 인코딩 DMA. from/to 가 묶인 enum 으로 표현 (§4.4).
   // 대표 용례: GEMM/GEMV 이전에 호스트 DDR4 → L2 로 가중치 타일 로드.
   void uca_memcpy(uint8_t  route,       // UCA_ROUTE_*
                   uint32_t dest_addr,   // 17-bit 목적지
                   uint32_t src_addr,    // 17-bit 소스
                   uint8_t  shape_ptr,   // 6-bit shape 포인터
                   uint8_t  async);

3.2 ``uca_memset``
-------------------

.. code-block:: c

   // 2 개의 descriptor 캐시 중 하나에 shape/size (16-bit × 3) 쓰기.
   void uca_memset(uint8_t  dest_cache,  // 0 = fmap_shape, 1 = weight_shape
                   uint8_t  dest_addr,   // 6-bit 포인터 슬롯
                   uint16_t a,           // 보통 M
                   uint16_t b,           // 보통 N
                   uint16_t c);          // 보통 K

4. 상수 정의
=============

헤더에서 모든 ISA 필드를 상수로 제공하므로, 애플리케이션이 비트 패턴을
하드코딩할 필요가 없다.

4.1 GEMV / GEMM 플래그 (6-bit)
-------------------------------

.. code-block:: c

   UCA_FLAG_FINDEMAX   // bit 5 — 출력 e_max 기록 (softmax 준비)
   UCA_FLAG_ACCM       // bit 4 — 결과를 누적 (덮어쓰지 않음)
   UCA_FLAG_W_SCALE    // bit 3 — MAC 중 가중치 스케일 적용

4.2 CVO 플래그 (5-bit)
-----------------------

.. code-block:: c

   UCA_CVO_FLAG_SUB_EMAX     // bit 4 — 연산 전 e_max 차감
   UCA_CVO_FLAG_RECIP_SCALE  // bit 3 — SCALE 이 1 / scalar 사용
   UCA_CVO_FLAG_ACCM         // bit 2 — 결과를 dst 에 누적

4.3 CVO 함수 코드 (4-bit)
--------------------------

.. code-block:: c

   UCA_CVO_EXP          // 0x0  element-wise exp(x)            [SFU]
   UCA_CVO_SQRT         // 0x1  element-wise sqrt(x)           [SFU]
   UCA_CVO_GELU         // 0x2  element-wise GELU(x)           [SFU]
   UCA_CVO_SIN          // 0x3  element-wise sin(x)            [CORDIC]
   UCA_CVO_COS          // 0x4  element-wise cos(x)            [CORDIC]
   UCA_CVO_REDUCE_SUM   // 0x5  sum-reduction → scalar         [SFU + adder]
   UCA_CVO_SCALE        // 0x6  element-wise × scalar          [SFU]
   UCA_CVO_RECIP        // 0x7  element-wise 1/x               [SFU]

4.4 메모리 루트 (8-bit)
-------------------------

.. code-block:: c

   UCA_ROUTE_HOST_TO_L2       // 0x01  호스트 DDR4 → L2
   UCA_ROUTE_L2_TO_HOST       // 0x10  L2 → 호스트 DDR4
   UCA_ROUTE_L2_TO_L1_GEMM    // 0x12  L2 → GEMM L1 (입력)
   UCA_ROUTE_L2_TO_L1_GEMV    // 0x13  L2 → GEMV L1 (입력)
   UCA_ROUTE_GEMM_RES_TO_L2   // 0x21  GEMM 결과 → L2
   UCA_ROUTE_GEMV_RES_TO_L2   // 0x31  GEMV 결과 → L2
   UCA_ROUTE_CVO_RES_TO_L2    // 0x41  SFU / CVO 결과 → L2

5. 동기화
==========

.. code-block:: c

   // UCA_STAT_BUSY 가 내려갈 때까지 폴링. 정상 idle 이면 0, 타임아웃 -1.
   int uca_sync(uint32_t timeout_us);

pccx 컨트롤러는 fully decoupled 이므로 ``uca_init`` 한 번이면 디코더
설정이 끝나고, 이후 ``uca_*`` 발행은 서로 독립적이다. 결과를 호스트
메모리로 돌려받기 전에 ``uca_sync`` 를 한 번 호출해 레이턴시 파이프
라인을 비운 뒤 ``uca_memcpy(UCA_ROUTE_L2_TO_HOST, …)`` 을 수행한다.

6. 예제 — FFN 블록
===================

``y = W_down · GELU(W_up · x)`` 최소 예시:

.. code-block:: c

   // 0) NPU 초기화
   if (uca_init() != 0) return -1;

   // 1) shape descriptor 프리셋
   //    slot 0: W_up   (M, N, K) = (1, 4096, 4096)
   //    slot 1: W_down (M, N, K) = (1, 4096, 4096)
   uca_memset(/*cache*/ 1, /*slot*/ 0, 1, 4096, 4096);
   uca_memset(/*cache*/ 1, /*slot*/ 1, 1, 4096, 4096);

   // 2) W_up · x  → 0x0100 (GEMV)
   uca_gemv(/*dest*/ 0x0100, /*src*/ 0x0000,
            /*flags*/ 0, /*size_ptr*/ 0, /*shape_ptr*/ 0,
            /*lanes*/ 0x0F);                 // 4 개 코어 모두 활성

   // 3) 0x0100 에서 GELU → 0x0200
   uca_cvo(UCA_CVO_GELU,
           /*src*/ 0x0100, /*dst*/ 0x0200,
           /*length*/ 4096,
           /*flags*/ 0, /*async*/ 0);

   // 4) W_down · activation → 0x0300
   uca_gemv(/*dest*/ 0x0300, /*src*/ 0x0200,
            /*flags*/ 0, /*size_ptr*/ 0, /*shape_ptr*/ 1,
            /*lanes*/ 0x0F);

   // 5) 완료 대기
   uca_sync(/*timeout_us*/ 100000);

7. 에러 처리
=============

``uca_init`` 와 ``uca_sync`` 는 성공 시 ``0``, 실패 시 ``-1`` 을
반환한다. 나머지 ``uca_*`` 호출은 ``void`` 이며, CMD_IN FIFO 에
명령어를 푸시하는 동작만 수행한다. 실제 실패 상황은 다음
``uca_sync`` 호출에서 ``UCA_STAT_*`` 비트로 드러난다.

대표 실패 패턴:

* ``uca_init`` 가 STAT 레지스터에서 기대하는 부팅 패턴을 읽지 못하면
  ``-1`` 반환.
* ``uca_sync`` 가 ``BUSY`` 비트를 ``timeout_us`` 동안 해제하지 못하면
  ``-1`` 반환.
* 필드 오버플로 (예: 주소가 17-bit 를 초과) 는 인코더가 단순 마스킹
  하므로, 애플리케이션이 문서화된 비트 폭을 스스로 지켜야 한다.

.. seealso::

   - 명령어 인코딩: :doc:`../ISA/encoding`
   - opcode 별 dataflow: :doc:`../ISA/dataflow`
   - ISA 의 RTL 측: :doc:`../RTL/isa_pkg`
