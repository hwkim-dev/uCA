# .pccx 파일 포맷

## 개요

`.pccx` 파일 포맷 공개 스펙 v0.1

이 포맷은 pccx-lab에서 NPU 프로파일링 데이터 및 관련 상태를 단일 바이너리로 압축 저장하기 위한 공식 스펙입니다.

## 바이트 레이아웃

| Offset | Size | Field | Notes |
|--------|------|-------|-------|
| 0 | 4 | Magic | `PCCX` (0x50 0x43 0x43 0x58) |
| 4 | 1 | Spec version | 현재 0x01 |
| 5 | 3 | Reserved | 0x00 0x00 0x00 |
| 8 | 8 | Header length | u64 Little-Endian — 바이트 단위의 JSON 헤더 길이 |
| 16 | N | JSON header | UTF-8 JSON |
| 16+N | M | Binary payload | raw 트레이스 바이트, 인코딩은 헤더에 명시 |

## JSON 헤더 필드

헤더는 시스템 구성 및 페이로드 메타데이터를 설명하는 JSON 객체입니다.

- `pccx_lab_version`: 생성한 툴의 버전.
- `arch.mac_dims`: MAC 어레이 크기 (예: `[32, 32]`).
- `arch.isa_version`: 타겟 ISA 버전.
- `trace.cycles`: 트레이스에 포함된 총 시뮬레이션 사이클 수.
- `trace.cores`: 사용된 활성 코어 수.
- `payload.encoding`: 바이너리 페이로드의 인코딩 방식.
- `payload.byte_length`: 바이너리 페이로드의 정확한 길이.

## 의사 코드 예제 (Rust)

```rust
let magic = read_bytes(4);
assert_eq!(magic, b"PCCX");
let version = read_byte();
let reserved = read_bytes(3);
let header_len = read_u64_le();
let json_header_bytes = read_bytes(header_len);
let payload = read_bytes(json_header.payload.byte_length);
```

## 버저닝 정책
포맷에 비호환성 변경이 발생할 때마다 Spec version 바이트가 증가합니다. 파서는 알 수 없는 버전을 만나면 읽기를 거부해야 합니다.
