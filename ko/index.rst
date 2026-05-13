================================
pccx 문서
================================

**pccx** (Parallel Compute Core eXecutor) 문서에 오신 것을 환영합니다.
pccx는 엣지 디바이스에서 Transformer 기반 LLM을 가속하기 위한
확장 가능한 NPU 아키텍처입니다. 사이드바에서 섹션을 선택하세요.

에코시스템
----------

.. grid:: 1 1 2 2
   :gutter: 3 4 4 4
   :class-container: pccx-ecosystem-grid

   .. grid-item-card:: :octicon:`cpu;1.5em;sd-mr-2` RTL 구현체
      :columns: 12 12 8 8
      :class-card: pccx-hero-card
      :link: https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260
      :link-type: url
      :link-alt: pccx-FPGA-NPU-LLM-kv260 저장소를 GitHub 에서 열기

      **github.com/pccxai/pccx-FPGA-NPU-LLM-kv260**

      활성 **v002** SystemVerilog 원본 — ISA 패키지, 컨트롤러,
      컴퓨트 코어 (GEMM / GEMV / CVO), 메모리 계층. 타겟 디바이스는
      Xilinx Kria **KV260** (Zynq UltraScale+ ZU5EV).

      **현재 지원 (집중):** Gemma-3N E4B @ W4A8KV4 — KV260 보드 실측
      tok/s 는 :doc:`docs/Evidence/index` 에서 추적. 그 외 (v003 /
      Gemma-4 / Llama) 는 :doc:`docs/roadmap` 에.

      이 사이트의 모든 v002 RTL 레퍼런스 페이지는 해당 ``.sv`` 파일로
      직접 연결됩니다.

   .. grid-item::
      :columns: 12 12 4 4

      .. grid:: 1
         :gutter: 3

         .. grid-item-card:: :octicon:`book;1em;sd-mr-1` 문서 소스
            :link: https://github.com/pccxai/pccx
            :link-type: url
            :link-alt: pccx 문서 저장소를 GitHub 에서 열기

            **github.com/pccxai/pccx** — 이 사이트를 빌드하는 Sphinx 프로젝트.

         .. grid-item-card:: :octicon:`telescope;1em;sd-mr-1` pccx-lab (검증 / 프로파일)
            :link: https://labs.pccx.ai/
            :link-type: url
            :link-alt: pccx-lab 검증·프로파일링 허브 열기

            **pccx-lab** — Tauri 2 IDE. ``.pccx`` 트레이스 로딩,
            ``run_verification`` 러너, Roofline / Bottleneck 카드,
            Vivado synth 리포트 뷰.
            `검증 문서 사이트 <https://labs.pccx.ai/>`_

         .. grid-item-card:: :octicon:`person;1em;sd-mr-1` 저자 포트폴리오
            :link: https://hkimw.github.io/hkimw/
            :link-type: url
            :link-alt: hkimw 포트폴리오 사이트 열기

            **hkimw.github.io/hkimw** — 블로그, 다른 프로젝트, 소개.

공개 `pccxai/pccx-v003 <https://github.com/pccxai/pccx-v003>`_ 저장소는
현재 v003 IP-core planning package 역할을 합니다. 이는 evidence-gated
planning package이며, stable RTL release가 아닙니다. 이전 feeder
`pccxai/pccx-LLM-v003 <https://github.com/pccxai/pccx-LLM-v003>`_ 은
superseded / retired 상태이며 더 이상 활성 공개 트랙이 아닙니다.
재사용 가능한 v003 LLM 자료는 ``pccx-v003/LLM/`` 아래로 들어옵니다.
보드/모델 저장소는 명시적인 compatibility contract 를 통해서만 v003
산출물을 소비합니다.

도구 & 랩
---------

.. grid:: 1 1 2 2
   :gutter: 3 4 4 4
   :class-container: pccx-toolchain-grid

   .. grid-item-card:: :octicon:`beaker;1.2em;sd-mr-1` pccx-lab
      :link: https://labs.pccx.ai/
      :link-type: url
      :link-alt: pccx-lab 시뮬레이터 & 프로파일러 열기
      :class-card: pccx-lab-card

      pccx NPU 전용 성능 시뮬레이터 + AI 통합 프로파일러.
      RTL 이전 병목 탐지, UVM co-simulation, LLM 기반 테스트벤치 생성을
      한 워크플로우로 통합.

      :bdg-warning:`Work in Progress`

      소스: github.com/pccxai/pccx-lab

   .. grid-item-card:: :octicon:`rocket;1.2em;sd-mr-1` PCCX Launcher
      :link: https://launcher.pccx.ai/
      :link-type: url
      :link-alt: PCCX Launcher 문서 열기

      Launcher contracts, runtime-readiness status, device/session summaries,
      diagnostics handoff records.

      :bdg-warning:`Private source`

   .. grid-item-card:: :octicon:`terminal;1.2em;sd-mr-1` SystemVerilog IDE
      :link: https://ide.pccx.ai/
      :link-type: url
      :link-alt: SystemVerilog IDE 문서 열기

      Editor diagnostics, validation context, declaration navigation,
      proposal-only workflow surfaces.

      :bdg-warning:`Private source`

   .. grid-item-card:: :octicon:`verified;1.2em;sd-mr-1` 형식 모델 — Sail
      :link: docs/v002/Formal/index
      :link-type: doc
      :link-alt: pccx Sail ISA 모델 읽기

      **pccx 는** `Sail <https://sail-lang.org/>`_ **로 형식적으로
      정의된다** — **RISC-V**, **Arm**, **CHERI**, **Morello** 의
      공식 사양을 기술하는 것과 동일한 ISA 시맨틱 언어. 64-bit /
      4-bit-opcode v002 ISA 는 RTL 레포의 ``formal/sail/`` 하위에
      거주하며, SystemVerilog 의 각 ``typedef`` 는 Sail 측에 1:1
      대응이 있어 폭 오류가 실리콘 전에 Sail 타입 체커에서 먼저
      잡힌다.

.. toctree::
   :maxdepth: 2
   :caption: 소개

   docs/index
   docs/quickstart
   docs/Evidence/index
   docs/roadmap

.. toctree::
   :maxdepth: 1
   :caption: v002 아키텍처

   docs/v002/index

.. toctree::
   :maxdepth: 1
   :caption: 타겟 하드웨어

   docs/Devices/index

.. toctree::
   :maxdepth: 1
   :caption: 아카이브

   docs/archive/index

.. toctree::
   :maxdepth: 1
   :caption: 툴체인 데모

   docs/samples/index

.. toctree::
   :maxdepth: 1
   :caption: 도구

   pccx-lab — 시뮬레이터 & AI 프로파일러 <https://labs.pccx.ai/>
   PCCX Launcher <https://launcher.pccx.ai/>
   SystemVerilog IDE <https://ide.pccx.ai/>
