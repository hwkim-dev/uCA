# HAL — AXI-Lite MMIO Layer

The `uca_hal_*` function set is the AXI-Lite MMIO layer that sits
between the public C API (`uca_*`, see :doc:`api`) and the NPU hardware.
No code above this layer accesses physical addresses or register offsets
directly.

The implementation lives in
`codes/v002/sw/driver/uCA_v1_hal.c` / `uCA_v1_hal.h`.

## HAL Position

The driver stack is organized into two layers.

```{list-table} Driver layer structure
:header-rows: 1
:name: tbl-driver-layers

* - Layer
  - Symbol prefix
  - Role
* - Public API
  - `uca_*`
  - Compute and memory primitives. Assembles 64-bit VLIW instructions
    and passes them through the HAL. See :doc:`api`.
* - HAL
  - `uca_hal_*`
  - AXI-Lite register reads and writes, 64-bit instruction latching,
    status polling. Depends directly on KV260 bare-metal pointer MMIO.
```

The HAL stores all state in a single file-scope singleton,
`g_mmio_base` (`volatile uint32_t *`). No context pointer is used;
a single process is expected to communicate with one NPU instance.

The KV260 bare-metal HAL source files (`sw/driver/uCA_v1_hal.{c,h}`)
remain in the board integration repository,
[`pccxai/pccx-FPGA-NPU-LLM-kv260`](https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260),
because they encode KV260 board-side bare-metal pointer MMIO. The
authoritative reading is the source files in that repo; this page
no longer embeds the listing inline.

## Register Map

The MMIO base address is `UCA_MMIO_BASE_ADDR = 0xA0000000`. This value
must match the AXI-Lite slave address assigned in the Vivado block
design.

(see the linked KV260 board integration repo above for the source listing)

```{list-table} Register map
:header-rows: 1
:name: tbl-hal-regmap

* - Name
  - Offset
  - Access
  - Description
* - `UCA_REG_INSTR_LO`
  - `0x00`
  - Write
  - Lower 32 bits of the 64-bit VLIW instruction. Written first.
* - `UCA_REG_INSTR_HI`
  - `0x04`
  - Write
  - Upper 32 bits of the 64-bit VLIW instruction. Writing this register
    triggers the NPU instruction latch.
* - `UCA_REG_STATUS`
  - `0x08`
  - Read
  - NPU status register (read-only). Contains `UCA_STAT_BUSY` and
    `UCA_STAT_DONE` bits.
```

A 64-bit instruction is written as a pair, **LO first, HI second**.
The HI write triggers the controller's instruction latch.

(see the linked KV260 board integration repo above for the source listing)

## CMD_IN / STAT_OUT Mechanics

`uca_hal_issue_instr` submits a 64-bit instruction to the NPU's CMD_IN
path by writing the register pair. The call returns immediately; the
NPU controller executes the instruction independently inside its
pipeline.

Status register `UCA_REG_STATUS` bit fields:

(see the linked KV260 board integration repo above for the source listing)

- **`UCA_STAT_BUSY` (bit 0)** — NPU is executing an instruction. Do not
  issue a new instruction while this bit is set.
- **`UCA_STAT_DONE` (bit 1)** — Last operation completed successfully.

Polling is performed by `uca_hal_wait_idle`. Because no hardware timer
driver is yet available on the bare-metal KV260, the current
implementation uses a busy-wait loop with an iteration count estimated
at the 400 MHz core rate.

(see the linked KV260 board integration repo above for the source listing)

When `timeout_us` decrements to zero, -1 is returned. The NPU state is
not forced-reset on timeout; the caller is responsible for error
recovery.

## uca_init Flow

`uca_hal_init` performs three operations in sequence.

1. Sets `g_mmio_base` to `(volatile uint32_t *)UCA_MMIO_BASE_ADDR`.
   Physical addresses are directly accessible in the KV260 bare-metal
   environment.
2. Calls `uca_hal_read32(UCA_REG_STATUS)` to read the status register.
3. If the return value is `0xFFFFFFFF`, the AXI bus is not responding;
   returns `-1`. Otherwise returns `0`.

(see the linked KV260 board integration repo above for the source listing)

`uca_hal_deinit` sets `g_mmio_base` to `NULL`. Any subsequent
`uca_hal_write32` or `uca_hal_read32` call will dereference a null
pointer; the caller must ensure no HAL calls follow `uca_hal_deinit`.

:::{seealso}

- Public API primitives: :doc:`api`
- AXI-Lite command path architecture: :doc:`../Architecture/top_level`
- ISA instruction encoding: :doc:`../ISA/encoding`
:::

:::{admonition} Last verified against
:class: note

Commit `8c09e5e` @ `pccxai/pccx-FPGA-NPU-LLM-kv260` (2026-04-29)
:::
