# Shape 상수 RAM

`shape_const_ram` 은 **fmap** 과 **weight** MEMSET descriptor 가
공유하는 (X, Y, Z) 텐서 shape 상수의 단일 출처(single source of
truth) 다. 바이트 단위로 중복되던 `fmap_array_shape` +
`weight_array_shape` 쌍 (Stage E 분석 §6.3.1, Stage C 결정 메모 item
5) 을 대체하며, {doc}`memory_dispatch` 의 MEMSET 쓰기 경로의 새
타겟으로 연결된다.

이 마이그레이션은 두 레거시 모듈을 하나의 파라미터화된 RAM 으로
합친다. v002.0 릴리스 라인에서 마이그레이션 검증 및 리뷰는 진행
중이며, 단계 맥락은 로드맵의 "Now" 섹션을 참고한다.

## 지오메트리

모듈은 `Depth` 로 파라미터화된다. `Depth = 64` 인 경우 저장 footprint
는 정확히 `64 × shape_xyz_t = 64 × 51 비트` 로, 두 레거시 모듈의 합
footprint 와 일치한다.

`shape_xyz_t` 는 세 개의 `shape_dim_t` 필드를 `{ Z, Y, X }` 순서로
패킹한 구조체이며, 해당 typedef 는 `isa_pkg` 가 소유하고 dispatcher
및 MEMSET 디코더가 함께 사용한다.

## 인터페이스

```{table} shape_const_ram 포트 (Depth = 64)
:name: tbl-shape-const-ram-ports-ko

| 방향 | 신호      | 폭                  | 의미                                       |
|---|---|---|---|
| 입력 | `clk`        | 1                       | 코어 클럭 @ 400 MHz                          |
| 입력 | `rst_n`      | 1                       | 액티브-로우 동기 리셋                        |
| 입력 | `wr_en`      | 1                       | 현재 사이클의 쓰기 인에이블                  |
| 입력 | `wr_addr`    | `$clog2(Depth)`         | 쓰기 엔트리 인덱스                           |
| 입력 | `wr_xyz`     | 51                      | `{ Z, Y, X }` 패킹된 쓰기 페이로드           |
| 입력 | `rd_addr`    | 6 (`ptr_addr_t`)        | 읽기 포인터 (`Depth = 64` 와 일치)           |
| 출력 | `rd_xyz`     | 51                      | 엔트리의 컴비네이셔널 읽기 결과              |
```

레이턴시:

- 쓰기 — 1 사이클 (`clk` 에 동기).
- 읽기 — 0 사이클 (컴비네이셔널). 읽기 포인터가 바뀌는 사이클에 곧바로
  새 값을 본다.

처리량: 사이클당 쓰기 1 + 읽기 1.

리셋 상태: `rst_n` 이 로우로 어서트되면 모든 엔트리가 동기적으로 `'0`
으로 클리어된다.

## `mem_dispatcher` 와의 와이어링

{doc}`memory_dispatch` 에 설명된 디스패치 경로는 이전에 MEMSET
페이로드를 레거시 `fmap_array_shape` / `weight_array_shape` 쌍으로
보냈다. Phase 3 step 1 이후에는 단일 `shape_const_ram` 인스턴스로
보내며, fmap / weight 선택은 주소 디코드에 흡수된다. 포트 폭 계약
(3 × 17 비트 팬아웃) 은 유지되므로, dispatcher 측 마이그레이션은 한
줄짜리 swap + 포트 이름 변경에 그친다.

스펙 참조: pccx v002 §3.3 (MEMSET) 및 §5.4 (shape pointer routing).

## 데이터 플로우

```{figure} ../../../../_static/diagrams/v002_shape_const_ram.svg
:name: fig-shape-const-ram-ko
:alt: shape_const_ram 의 MEMSET 쓰기 경로 및 shape pointer 읽기 경로

쓰기 경로: dispatcher 의 MEMSET 디코더가 `wr_en` / `wr_addr` /
`wr_xyz` 를 동기적으로 구동한다. 읽기 경로: ISA shape pointer 필드의
6-비트 `rd_addr` 가 컴퓨트 경로 consumer 에 `rd_xyz` 를
컴비네이셔널로 반환한다.
```

## 소스

```{literalinclude} ../../../../codes/v002/LLM/rtl/core/memory/Constant_Memory/shape_const_ram.sv
:language: systemverilog
:start-at: module shape_const_ram
:end-before: endmodule
```

```{admonition} 마지막 검증 대상
:class: note
커밋 `18d4631` @ `pccxai/pccx-FPGA-NPU-LLM-kv260` (2026-05-06)
```
