# .pccx File Format Specification

> **Version:** 0.2 (format major: 0x01, minor: 0x01)  
> **Status:** Active  
> **Source of truth:** `src/core/src/pccx_format.rs`

## Overview

The `.pccx` binary format is the official container for storing NPU profiling
traces, hardware configurations, and session metadata produced by `pccx-lab`.

Design goals:

- **Zero-copy IPC**: The payload is a raw byte blob that can be memory-mapped
  directly into a WebGL `ArrayBuffer` without re-encoding.
- **Self-describing**: The JSON header contains all metadata needed to decode
  the payload without out-of-band schema files.
- **Versioned**: Major/minor version bytes allow backward-compatible evolution.
- **Integrity-checked**: An optional FNV-1a 64-bit checksum enables fast
  tamper detection.

---

## Binary Layout

All multi-byte integers are **little-endian** unless otherwise noted.

| Offset  | Size | Field            | Description |
|---------|------|------------------|-------------|
| 0       | 4    | Magic            | `PCCX` = `0x50 0x43 0x43 0x58` |
| 4       | 1    | Major version    | Breaking-change counter (currently `0x01`) |
| 5       | 1    | Minor version    | Additive-change counter (currently `0x01`) |
| 6       | 2    | Reserved         | `0x00 0x00` — must be zeroed by writers |
| 8       | 8    | Header length    | `u64` — byte length of the JSON header |
| 16      | N    | JSON header      | UTF-8 JSON object (see below) |
| 16 + N  | M    | Binary payload   | Encoding declared in `payload.encoding` |

> **Compatibility rule:** Parsers MUST reject files whose **major version** does
> not match the expected value. Parsers SHOULD accept any **minor version**,
> treating unknown fields as additive extensions.

---

## JSON Header Fields

```json
{
  "pccx_lab_version": "v0.4.0-contention-aware",   // string
  "format_minor": 1,                                 // u8

  "arch": {
    "mac_dims": [32, 32],    // [rows, cols] of the systolic MAC array
    "isa_version": "1.1",    // string
    "peak_tops": 2.05        // f64, theoretical peak (informational)
  },

  "trace": {
    "cycles":    12345678,   // u64 — total simulation cycles
    "cores":     32,         // u32 — number of active NPU cores
    "clock_mhz": 1000        // u32 — clock frequency used to generate the trace
  },

  "payload": {
    "encoding":       "bincode",           // "bincode" | "flatbuf" | "raw"
    "byte_length":    4096000,             // u64 — exact payload byte count
    "checksum_fnv64": "0xcbf29ce4842223" // hex string | null — FNV-1a 64-bit
  }
}
```

### Payload Encodings

| Value       | Description |
|-------------|-------------|
| `"bincode"` | Rust `bincode` v1 serialisation of `NpuTrace` struct |
| `"flatbuf"` | 24-byte packed struct array (see Flat Buffer Layout below) |
| `"raw"`     | Architecture-specific raw bytes (not standardised) |

---

## Flat Buffer Layout (`"flatbuf"` encoding)

Each event is 24 bytes, all fields little-endian:

| Offset | Size | Type | Field          |
|--------|------|------|----------------|
| 0      | 4    | u32  | `core_id`      |
| 4      | 8    | u64  | `start_cycle`  |
| 12     | 8    | u64  | `duration`     |
| 20     | 4    | u32  | `event_type_id`|

### Event Type IDs

| ID | Name              |
|----|-------------------|
| 0  | `UNKNOWN`         |
| 1  | `MAC_COMPUTE`     |
| 2  | `DMA_READ`        |
| 3  | `DMA_WRITE`       |
| 4  | `SYSTOLIC_STALL`  |
| 5  | `BARRIER_SYNC`    |

---

## Pseudocode (Rust)

```rust
// Reading
let mut magic = [0u8; 4];
reader.read_exact(&mut magic)?;
assert_eq!(&magic, b"PCCX");

let mut version = [0u8; 2];
reader.read_exact(&mut version)?;
let major = version[0]; // must equal MAJOR_VERSION (0x01)
let minor = version[1]; // any value accepted

let mut reserved = [0u8; 2];
reader.read_exact(&mut reserved)?;

let mut hlen_buf = [0u8; 8];
reader.read_exact(&mut hlen_buf)?;
let header_len = u64::from_le_bytes(hlen_buf);

let mut json_bytes = vec![0u8; header_len as usize];
reader.read_exact(&mut json_bytes)?;
let header: PccxHeader = serde_json::from_slice(&json_bytes)?;

let mut payload = vec![0u8; header.payload.byte_length as usize];
reader.read_exact(&mut payload)?;
```

---

## Versioning Policy

- **Major version** increments on incompatible layout changes (e.g. changing the
  reserved field size, removing header fields). Parsers must reject mismatches.
- **Minor version** increments on additive changes (new optional header fields,
  new event type IDs). Parsers must ignore unknown fields gracefully.
- The `pccx_lab_version` string is informational only and does not affect parsing.

---

## Integrity Check

The optional `checksum_fnv64` field stores the **FNV-1a 64-bit** hash of the
raw payload bytes. Parsers may use it to detect accidental corruption:

```rust
fn fnv1a_64(data: &[u8]) -> u64 {
    const BASIS: u64 = 0xcbf29ce484222325;
    const PRIME: u64 = 0x00000100000001b3;
    data.iter().fold(BASIS, |h, &b| (h ^ b as u64).wrapping_mul(PRIME))
}
```

A mismatch produces a warning but is not fatal by default (configurable).
