# .pccx File Format

## Overview

`.pccx` file format open specification v0.1

This format is the official specification for compactly storing NPU profiling data and associated states into a single binary for pccx-lab.

## Byte Layout

| Offset | Size | Field | Notes |
|--------|------|-------|-------|
| 0 | 4 | Magic | `PCCX` (0x50 0x43 0x43 0x58) |
| 4 | 1 | Spec version | Currently 0x01 |
| 5 | 3 | Reserved | 0x00 0x00 0x00 |
| 8 | 8 | Header length | u64 Little-Endian — length of JSON header in bytes |
| 16 | N | JSON header | UTF-8 JSON |
| 16+N | M | Binary payload | raw trace bytes, encoding per header |

## JSON Header Fields

The header is a JSON object describing the system configuration and payload metadata.

- `pccx_lab_version`: The version of the tool that generated it.
- `arch.mac_dims`: MAC array dimensions (e.g., `[32, 32]`).
- `arch.isa_version`: Target ISA version.
- `trace.cycles`: Total simulation cycles included in the trace.
- `trace.cores`: Number of active cores used.
- `payload.encoding`: Encoding method of the binary payload.
- `payload.byte_length`: Exact length of the binary payload.

## Pseudocode Example (Rust)

```rust
let magic = read_bytes(4);
assert_eq!(magic, b"PCCX");
let version = read_byte();
let reserved = read_bytes(3);
let header_len = read_u64_le();
let json_header_bytes = read_bytes(header_len);
let payload = read_bytes(json_header.payload.byte_length);
```

## Versioning Policy
The Spec version byte increments whenever incompatible changes occur in the format. Parsers must reject reading if they encounter an unknown version.
