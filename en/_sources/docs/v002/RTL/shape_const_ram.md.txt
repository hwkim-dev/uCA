# Shape Constant RAM

`shape_const_ram` provides a single source of truth for the (X, Y, Z)
tensor-shape constants used by both the **fmap** and **weight** MEMSET
descriptors. It replaces the byte-for-byte duplicate pair
`fmap_array_shape` + `weight_array_shape` (Stage E analysis §6.3.1,
Stage C decisions memo item 5) and is wired into {doc}`memory_dispatch`
as the new target of the MEMSET write path.

The migration consolidates the two legacy modules into one parameterised
RAM. Migration validation and review are still in progress on the v002.0
release line — see the roadmap "Now" section for the broader phase
context.

## Geometry

The module is parameterised by `Depth`. With `Depth = 64`, the storage
footprint is exactly `64 × shape_xyz_t = 64 × 51 bits`, matching the
combined footprint of the two legacy modules.

`shape_xyz_t` is a packed struct of three `shape_dim_t` fields ordered
`{ Z, Y, X }`. The typedefs are owned by `isa_pkg` and reused by the
dispatcher and the MEMSET decoder.

## Interface

```{table} shape_const_ram ports (Depth = 64)
:name: tbl-shape-const-ram-ports-en

| Direction | Signal     | Width              | Meaning                                |
|---|---|---|---|
| input  | `clk`        | 1                       | Core clock @ 400 MHz                     |
| input  | `rst_n`      | 1                       | Active-low synchronous reset             |
| input  | `wr_en`      | 1                       | Write enable for the current cycle       |
| input  | `wr_addr`    | `$clog2(Depth)`         | Write entry index                        |
| input  | `wr_xyz`     | 51                      | Packed `{ Z, Y, X }` write payload       |
| input  | `rd_addr`    | 6 (`ptr_addr_t`)        | Read pointer (matches `Depth = 64`)      |
| output | `rd_xyz`     | 51                      | Combinational read of the entry          |
```

Latency:

- write — 1 cycle (synchronous to `clk`).
- read — 0 cycles (combinational). Consumers see the new value in the
  same cycle the read pointer changes.

Throughput: 1 write + 1 read per cycle.

Reset state: all entries cleared to `'0` synchronously when `rst_n` is
asserted low.

## Wiring into `mem_dispatcher`

The dispatch path described on {doc}`memory_dispatch` previously routed
MEMSET payloads into the legacy `fmap_array_shape` / `weight_array_shape`
pair. After Phase 3 step 1 they are routed into a single
`shape_const_ram` instance, with the fmap-vs-weight selector folded into
the address decode. The port-width contract (3 × 17-bit fan-out) is
preserved, so the dispatcher migration is a one-line swap and a port
name change.

Spec reference: pccx v002 §3.3 (MEMSET) and §5.4 (shape pointer
routing).

## Data flow

```{figure} ../../../_static/diagrams/v002_shape_const_ram.svg
:name: fig-shape-const-ram-en
:alt: shape_const_ram with MEMSET write and shape-pointer read paths

Write path: the dispatcher's MEMSET decoder drives `wr_en` / `wr_addr`
/ `wr_xyz` synchronously. Read path: the 6-bit `rd_addr` from the ISA
shape-pointer field returns `rd_xyz` combinationally to the compute-path
consumers.
```

## Source

```{literalinclude} ../../../codes/v002/hw/rtl/MEM_control/memory/Constant_Memory/shape_const_ram.sv
:language: systemverilog
:start-at: module shape_const_ram
:end-before: endmodule
```

```{admonition} Last verified against
:class: note
Commit `18d4631` @ `pccxai/pccx-FPGA-NPU-LLM-kv260` (2026-05-06).
```
