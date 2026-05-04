# 설계 원칙

## 왜 pccx-lab은 5개가 아닌 1개의 레포지토리인가?

초기 설계에서는 시뮬레이터, 프론트엔드, UVM 브릿지, AI, 공통 라이브러리 등 5개의 개별 레포지토리로 분리하는 구조를 고려했습니다. 하지만 다음과 같은 이유로 기각되었습니다:

1. **개발 속도**: 여러 레포지토리에 걸친 변경 사항을 동기화하고 버전을 관리하는 오버헤드가 매우 큽니다.
2. **단일 목적성**: 모든 모듈이 결국 'pccx 프로파일링'이라는 단일한 목적을 향해 긴밀하게 협력합니다.

## 모듈 경계 규칙

단일 레포지토리의 단점(스파게티 코드)을 막기 위해 엄격한 모듈 경계를 강제합니다.  Phase 1 에서 원래 단일 덩어리였던 `core/` 를 `crates/` 하위의 9 개 집중형 crate 와 최상위 `ui/` 로 분리했고, 의존 간선은 단방향이며 `pccx-core` 가 워크스페이스 그래프의 유일한 sink 입니다(전체 다이어그램은 `docs/design/phase1_crate_split.md` § 3 참조).

- `pccx-core` (`crates/core/`): 순수 Rust 코어 — .pccx 포맷, 트레이스 파싱, 하드웨어 모델, 루프라인, 병목 탐지, VCD / chrome-trace writer, step-snapshot IPC, Vivado 타이밍 수집.  다른 워크스페이스 crate 에 의존하지 않으며 UI 프레임워크 import 를 엄격히 금지합니다.
- `pccx-reports` (`crates/reports/`): Markdown / HTML / PDF 리포트 렌더링.  `pccx-core` 의존.
- `pccx-verification` (`crates/verification/`): CI 와 pccx-ide 가 쓰는 golden-diff + robust reader 게이트.  `pccx-core` 의존.
- `pccx-authoring` (`crates/authoring/`): ISA / API TOML 컴파일러.  `pccx-core` 의존.
- `pccx-evolve` (`crates/evolve/`): EAGLE 계열 투기 디코딩 프리미티브 및 Phase 5 DSE + surrogate + PRM 루프의 향후 거처.  `pccx-core` 와 `pccx-verification` 의존.
- `pccx-lsp` (`crates/lsp/`): Phase 2 IntelliSense façade — sync / async provider trait, multiplexer, `NoopBackend`, `BlockingBridge`, `LspSubprocess`.  `pccx-core` 의존.
- `pccx-remote` (`crates/remote/`): Phase 3 백엔드 데몬 스캐폴드(WireGuard / OIDC / RBAC 는 이후 단계에서 착지).  `pccx-core` 의존.
- `pccx-uvm-bridge` (`crates/uvm_bridge/`): SystemVerilog/UVM 과 `pccx-core` 사이의 DPI-C / FFI 경계.
- `pccx-workflow-facade` (`crates/workflow_facade/`): LLM 호출 래퍼.  `pccx-core` 의 트레이스 표면(JSON 등)에만 의존.
- `pccx-ide` (`ui/src-tauri/`): `pccx-core`, `pccx-reports`, `pccx-workflow-facade` 을 소비하는 Tauri 쉘.
- `ui/` (비-Cargo): React + Vite 프론트엔드.  `pccx-ide` 와 Tauri IPC 만으로 통신합니다.

어느 crate 도 `pccx-ide` 또는 `pccx-remote` 에 의존하지 않습니다 — 둘 다 터미널 바이너리입니다.  React 트리는 Cargo 워크스페이스 멤버가 아니며, 설계상 워크스페이스 그래프 바깥에 위치합니다.

## 향후 분리 조건

특정 crate(예: `pccx-core` 또는 `pccx-verification`)가 pccx-lab 외부에서도 독자적으로 쓸 수 있을 만큼 범용성을 갖추면 crates.io 에 퍼블리시하거나 별도 레포지토리로 추출합니다.  Phase 1 분리는 바로 이 추출을 염두에 두고 단계화한 것이라, 각 비-core crate 는 이미 불안정 trait 표면(`ReportFormat`, `VerificationGate`, `IsaCompiler`, `ApiCompiler`, `CompletionProvider` 등)을 노출하고 있습니다.  즉 "뽑아내기" 는 아키텍처 리팩터가 아니라 릴리스 엔지니어링 작업으로 환원됩니다.
