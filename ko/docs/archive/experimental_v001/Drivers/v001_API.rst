pccx v001 호스트 API 개발자 레퍼런스
=====================================

   [!NOTE] 이 문서는 호스트 애플리케이션이 NPU 를 제어할 때 사용하는
   High-Level C API 를 다룹니다. v001 NPU 아키텍처용으로 설계되었으며
   Hardware Abstraction Layer (HAL) 를 직접 래핑합니다.

API 아키텍처 개요
------------------

현재 API 계층은 익숙한 GPU 프로그래밍 모델의 경험을 추구합니다.
개발자는 64-bit VLIW 명령어 어셈블리를 이해할 필요 없이 ``pccx_*``
C 함수 호출만으로 비동기 하드웨어 가속기를 활용할 수 있습니다.

-  **Non-blocking (비동기)**: 모든 연산 함수는 단순히 HAL 을 통해
   NPU FIFO 에 명령어를 큐잉하고 즉시 반환합니다.
-  **Sync Point**: 호스트 실행 흐름이 하드웨어 상태와 동기화되는 건
   ``pccx_sync()`` 함수가 명시적으로 호출될 때뿐입니다.

--------------

API 레퍼런스
-------------

1. 초기화 및 종료
~~~~~~~~~~~~~~~~~~

NPU 디바이스 핸들을 초기화하고 리소스를 해제하는 기본 함수들.
계속 진행하기 전에 NPU 가 응답 가능한지 보장합니다.

=== "Header (pccx_v1_api.h)"

::

   ```c
   int  pccx_init(void);

   void pccx_deinit(void);
   ```

=== "Implementation (pccx_v1_api.c)"

::

   ```c
   int pccx_init(void) {
       return pccx_hal_init();
   }

   void pccx_deinit(void) {
       pccx_hal_deinit();
   }
   ```

2. Matrix Core 및 Vector Core
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vector Core (GEMV) 및 Matrix Core (GEMM) 연산 실행. 호스트가 C 타입으로
인자를 전달하면 API 가 내부적으로 64-bit VLIW 포맷으로 빌드하여 하드웨어
FIFO 에 푸시합니다.

**파라미터:** - ``dest_reg`` : 목적 레지스터 또는 L2 메모리 주소
(17-bit). - ``src_addr`` : 소스 피처맵 버퍼의 시작 위치 (17-bit). -
``flags`` : 설정 플래그 (``PCCX_FLAG_FINDEMAX``, ``PCCX_FLAG_ACCM``
등). - ``size_ptr`` : shape 캐시 내부 size 디스크립터 포인터 (6-bit). -
``shape_ptr`` : shape 캐시 내부 shape 디스크립터 포인터 (6-bit). -
``lanes`` : 활용할 병렬 μV-Core 레인 수 (1~4).

=== "Header (pccx_v1_api.h)"

::

   ```c
   void pccx_gemv(uint32_t dest_reg,   uint32_t src_addr,
                  uint8_t  flags,      uint8_t  size_ptr,
                  uint8_t  shape_ptr,  uint8_t  lanes);

   void pccx_gemm(uint32_t dest_reg,   uint32_t src_addr,
                  uint8_t  flags,      uint8_t  size_ptr,
                  uint8_t  shape_ptr,  uint8_t  lanes);
   ```

=== "Implementation (pccx_v1_api.c)"

::

   ```c
   static uint64_t build_compute_instr(...) {
       uint64_t instr = 0;
       instr |= ((uint64_t)(opcode    & 0xF)     << 60);
       instr |= ((uint64_t)(dest_reg  & 0x1FFFF) << 43);
       instr |= ((uint64_t)(src_addr  & 0x1FFFF) << 26);
       instr |= ((uint64_t)(flags     & 0x3F)    << 20);
       instr |= ((uint64_t)(size_ptr  & 0x3F)    << 14);
       instr |= ((uint64_t)(shape_ptr & 0x3F)    <<  8);
       instr |= ((uint64_t)(lanes     & 0x1F)    <<  3);
       return instr;
   }

   void pccx_gemv(...) {
       uint64_t instr = build_compute_instr(PCCX_OP_GEMV, dest_reg, src_addr, flags, size_ptr, shape_ptr, lanes);
       pccx_hal_issue_instr(instr);
   }
   ```

3. CVO (Complex Vector Operations)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Softmax, RMSNorm, GELU, RoPE 같은 attention weight scaling 에 사용되는
비선형 수학 함수(SFU 및 CORDIC) 를 제어합니다.

**파라미터:** - ``cvo_func`` : 함수 코드 상수, 예 ``PCCX_CVO_EXP``,
``PCCX_CVO_SQRT``. - ``src_addr`` : 소스 캐시 주소. - ``dst_addr`` :
목적 캐시 주소. - ``length`` : 순차 처리할 벡터 연산 횟수.

=== "Header (pccx_v1_api.h)"

::

   ```c
   void pccx_cvo(uint8_t  cvo_func,  uint32_t src_addr,
                 uint32_t dst_addr,  uint16_t length,
                 uint8_t  flags,     uint8_t  async);
   ```

=== "Implementation (pccx_v1_api.c)"

::

   ```c
   static uint64_t build_cvo_instr(...) {
       uint64_t instr = 0;
       instr |= ((uint64_t)(PCCX_OP_CVO & 0xF)   << 60);
       instr |= ((uint64_t)(cvo_func  & 0xF)    << 56);
       instr |= ((uint64_t)(src_addr  & 0x1FFFF)<< 39);
       instr |= ((uint64_t)(dst_addr  & 0x1FFFF)<< 22);
       instr |= ((uint64_t)(length    & 0xFFFF) <<  6);
       instr |= ((uint64_t)(flags     & 0x1F)   <<  1);
       instr |= ((uint64_t)(async     & 0x1)    <<  0);
       return instr;
   }

   void pccx_cvo(...) {
       uint64_t instr = build_cvo_instr(cvo_func, src_addr, dst_addr, length, flags, async);
       pccx_hal_issue_instr(instr);
   }
   ```

4. 메모리 제어 (DMA 전송)
~~~~~~~~~~~~~~~~~~~~~~~~~~

호스트 DDR, NPU L2 캐시, L1 엔진 로컬 캐시 간의 데이터 라우팅과 버스
전송을 파이프라인화합니다.

**DMA 전송 파라미터:** - ``route`` : 흐름 소스·목적을 식별하는 라우팅
버스 상수. - ``dest_addr`` : 전송 목적 로컬 주소. - ``src_addr`` :
소스 버퍼 주소.

=== "Header (pccx_v1_api.h)"

::

   ```c
   void pccx_memcpy(uint8_t route, uint32_t dest_addr, uint32_t src_addr, uint8_t shape_ptr, uint8_t async);

   void pccx_memset(uint8_t dest_cache, uint8_t dest_addr, uint16_t a, uint16_t b, uint16_t c);
   ```

=== "Implementation (pccx_v1_api.c)"

::

   ```c
   void pccx_memcpy(...) {
       uint8_t from_dev = (route >> 4) & 0xF;
       uint8_t to_dev   = (route >> 0) & 0xF;

       uint64_t instr = 0;
       instr |= ((uint64_t)(PCCX_OP_MEMCPY & 0xF) << 60);
       instr |= ((uint64_t)(from_dev  & 0x1)      << 59);
       instr |= ((uint64_t)(to_dev    & 0x1)      << 58);
       instr |= ((uint64_t)(dest_addr & 0x1FFFF)  << 41);
       instr |= ((uint64_t)(src_addr  & 0x1FFFF)  << 24);
       instr |= ((uint64_t)(shape_ptr & 0x3F)     <<  1);
       instr |= ((uint64_t)(async     & 0x1)      <<  0);
       pccx_hal_issue_instr(instr);
   }
   ```

5. 동기화
~~~~~~~~~~

FIFO 큐에 등록된 모든 비동기 NPU 파이프라인이 작업을 완료할 때까지
blocking 으로 대기합니다.

**파라미터:** - ``timeout_us`` : 에러 상태를 반환하기 전 기다릴 타임아웃
(마이크로초).

=== "Header (pccx_v1_api.h)"

::

   ```c
   int pccx_sync(uint32_t timeout_us);
   ```

=== "Implementation (pccx_v1_api.c)"

::

   ```c
   int pccx_sync(uint32_t timeout_us) {
       return pccx_hal_wait_idle(timeout_us);
   }
   ```
