# .pccx 파일 포맷 명세

> **버전:** 0.2 (포맷 메이저: 0x01, 마이너: 0x01)  
> **상태:** 활성 (Active)  
> **진실의 원본 (Source of Truth):** `src/core/src/pccx_format.rs`

## 개요

`.pccx` 바이너리 포맷은 `pccx-lab`이 생성하는 NPU 프로파일링 트레이스,
하드웨어 설정, 세션 메타데이터를 저장하는 공식 컨테이너 형식입니다.

설계 목표:

- **Zero-copy IPC**: 페이로드는 재인코딩 없이 WebGL `ArrayBuffer`에 직접
  메모리 매핑할 수 있는 원시 바이트 블롭입니다.
- **자기 서술적 (Self-describing)**: JSON 헤더가 외부 스키마 파일 없이
  페이로드를 디코딩하는 데 필요한 모든 메타데이터를 포함합니다.
- **버전 관리**: 메이저/마이너 버전 바이트로 하위 호환성을 유지하며 발전합니다.
- **무결성 검증**: 선택적 FNV-1a 64비트 체크섬으로 빠른 훼손(tamper) 감지를 지원합니다.

---

## 바이너리 레이아웃

여러 바이트 정수는 특별한 언급이 없는 한 **리틀 엔디언(little-endian)**입니다.

| 오프셋  | 크기 | 필드            | 설명 |
|---------|------|-----------------|------|
| 0       | 4    | 매직 넘버        | `PCCX` = `0x50 0x43 0x43 0x58` |
| 4       | 1    | 메이저 버전      | 호환 불가 변경 카운터 (현재 `0x01`) |
| 5       | 1    | 마이너 버전      | 추가적 변경 카운터 (현재 `0x01`) |
| 6       | 2    | 예약 (Reserved) | `0x00 0x00` — 작성자는 반드시 0으로 채워야 합니다 |
| 8       | 8    | 헤더 길이        | `u64` — JSON 헤더의 바이트 길이 |
| 16      | N    | JSON 헤더        | UTF-8 JSON 객체 (아래 참조) |
| 16 + N  | M    | 바이너리 페이로드 | `payload.encoding` 에 선언된 인코딩 형식 |

> **호환성 규칙:** 파서는 **메이저 버전**이 기대값과 다를 경우 반드시 오류를
> 반환해야 합니다. **마이너 버전**은 어떤 값도 허용하며, 알 수 없는 필드는
> 추가적 확장으로 처리해야 합니다.

---

## JSON 헤더 필드

```json
{
  "pccx_lab_version": "v0.4.0-contention-aware",   // 문자열
  "format_minor": 1,                                 // u8

  "arch": {
    "mac_dims": [32, 32],    // 시스톨릭 MAC 어레이의 [행, 열]
    "isa_version": "1.1",    // 문자열
    "peak_tops": 2.05        // f64, 이론적 최대 성능 (참고용)
  },

  "trace": {
    "cycles":    12345678,   // u64 — 총 시뮬레이션 사이클
    "cores":     32,         // u32 — 활성 NPU 코어 수
    "clock_mhz": 1000        // u32 — 트레이스 생성 시 사용된 클록 주파수
  },

  "payload": {
    "encoding":       "bincode",          // "bincode" | "flatbuf" | "raw"
    "byte_length":    4096000,            // u64 — 페이로드의 정확한 바이트 수
    "checksum_fnv64": "0xcbf29ce4842223" // 16진수 문자열 | null — FNV-1a 64비트
  }
}
```

### 페이로드 인코딩 목록

| 값          | 설명 |
|-------------|------|
| `"bincode"` | Rust `bincode` v1으로 직렬화된 `NpuTrace` 구조체 |
| `"flatbuf"` | 24바이트 패킹 구조체 배열 (아래 플랫 버퍼 레이아웃 참조) |
| `"raw"`     | 아키텍처별 원시 바이트 (비표준) |

---

## 플랫 버퍼 레이아웃 (`"flatbuf"` 인코딩)

각 이벤트는 24바이트이며 모든 필드는 리틀 엔디언입니다:

| 오프셋 | 크기 | 타입 | 필드            |
|--------|------|------|-----------------|
| 0      | 4    | u32  | `core_id`       |
| 4      | 8    | u64  | `start_cycle`   |
| 12     | 8    | u64  | `duration`      |
| 20     | 4    | u32  | `event_type_id` |

### 이벤트 타입 ID

| ID | 이름              | 설명 |
|----|-------------------|------|
| 0  | `UNKNOWN`         | 알 수 없는 이벤트 |
| 1  | `MAC_COMPUTE`     | MAC 어레이 연산 실행 |
| 2  | `DMA_READ`        | AXI DMA 읽기 |
| 3  | `DMA_WRITE`       | AXI DMA 쓰기 |
| 4  | `SYSTOLIC_STALL`  | 시스톨릭 파이프라인 드레인 스톨 |
| 5  | `BARRIER_SYNC`    | 코어 간 동기화 배리어 |

---

## 의사 코드 (Rust)

```rust
// 읽기
let mut magic = [0u8; 4];
reader.read_exact(&mut magic)?;
assert_eq!(&magic, b"PCCX");

let mut version = [0u8; 2];
reader.read_exact(&mut version)?;
let major = version[0]; // MAJOR_VERSION (0x01)과 일치해야 함
let minor = version[1]; // 어떤 값도 허용

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

## 버전 관리 정책

- **메이저 버전**은 레이아웃 호환 불가 변경 시 증가합니다 (예: 예약 필드 크기 변경,
  헤더 필드 삭제). 파서는 불일치 시 오류를 반환해야 합니다.
- **마이너 버전**은 추가적 변경 시 증가합니다 (새 선택적 헤더 필드, 새 이벤트 타입 ID).
  파서는 알 수 없는 필드를 무시해야 합니다.
- `pccx_lab_version` 문자열은 참고용이며 파싱에 영향을 주지 않습니다.

---

## 무결성 검증

선택적 `checksum_fnv64` 필드는 원시 페이로드 바이트의 **FNV-1a 64비트** 해시를 저장합니다.
파서는 이를 사용하여 우발적 손상을 감지할 수 있습니다:

```rust
fn fnv1a_64(data: &[u8]) -> u64 {
    const BASIS: u64 = 0xcbf29ce484222325;
    const PRIME: u64 = 0x00000100000001b3;
    data.iter().fold(BASIS, |h, &b| (h ^ b as u64).wrapping_mul(PRIME))
}
```

불일치 시 기본적으로 경고를 출력하지만 치명적 오류로 처리하지는 않습니다 (설정 가능).
