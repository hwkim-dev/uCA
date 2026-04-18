검증
=====

.. admonition:: Placeholder
   :class: note

   본 섹션은 현재 의도적으로 비어 있는 스텁입니다. pccx v002 의 검증 계획,
   테스트벤치 아키텍처, 커버리지 목표, 정적 속성 (formal property) 결과가
   완성되는 대로 여기 채워질 예정입니다.

계획된 범위
-------------

전체 섹션은 다음을 다룰 예정입니다:

* **검증 계획** — 모듈별 기능 커버리지 목표와 sign-off 기준.
* **테스트벤치 아키텍처** — UVM / cocotb harness 레이아웃, 참조 모델,
  자극 생성기 (``llm-lite`` CPU 참조 구현에서 가져온 골든 데이터).
* **커버리지 대시보드** — 기능 · 코드 · 단언 커버리지를 코어별
  (GEMM / GEMV / CVO / MEM) 롤업.
* **Formal 결과** — 컨트롤러, ISA 디코더, 메모리 중재기에 대한
  SymbiYosys / JasperGold property.
* **실리콘 레벨 검증** — post-implementation 시뮬레이션, 보드 bring-up
  스크립트, :doc:`호스트 C 드라이버 </docs/v002/Drivers/api>` 대비
  골든 트레이스 비교.

.. seealso::

   :doc:`/docs/v002/Architecture/index`
       이 섹션이 검증하는 아키텍처 계약.
   :doc:`/docs/v002/ISA/index`
       테스트벤치가 확인하는 ISA 레벨 불변식.
   :doc:`/docs/v002/RTL/index`
       검증 대상 RTL 모듈.
