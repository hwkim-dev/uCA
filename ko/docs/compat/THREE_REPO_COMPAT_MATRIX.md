---
orphan: true
---

# 3개 저장소 호환성 매트릭스

범위: `systemverilog-ide`, `pccx-launcher`, `pccx-lab`.

이 페이지는 에디터 cockpit, launcher surface, lab backend 간 data-only
boundary의 정본이다. 새 호환성 문안에는 공개명칭 `pccx-launcher`를 사용한다.

## 목표

- 별도의 검토된 경계에서 더 강한 연계가 명시되지 않는 한, 저장소 간 통합은
  data-only로 유지한다.
- 외부 사용자가 프라이빗 조정 노트 없이도 공개 surface를 이해하고,
  테스트하고 확장할 수 있어야 한다.
- 각 저장소를 독립적으로 유용하게 만들어 사용자 규모를 키운다.
  예를 들어 에디터 진단/네비게이션, launcher 상태/적합성(ready) 뷰,
  lab 검증/상태 요약이 각각 독립적으로 진화할 수 있어야 한다.
- 모든 상태, 적합성, evidence payload는 evidence-gated여야 한다. `blocked`,
  `planned`, `unavailable`, `descriptor-only` 상태를 설명할 수는 있지만
  실행 완료, 디바이스 성공, 성능, 상용 출시 readiness를 암시하면 안 된다.
- 작은 JSON 계약과 검증된 fixture, 스키마 버전, strict validator, 제한된 텍스트,
  비밀 누출 방지, 명시적 안전 플래그를 선호한다.

## 소스 evidence 스냅샷

이 매트릭스는 다음 로컬 공개 저장소 체크아웃을 바탕으로 조사했다:

| 저장소 | 조사 커밋 | 공개 surface 예시 |
| --- | --- | --- |
| `systemverilog-ide` | `992fb0f24d5d` | `docs/EDITOR_BRIDGE_CONTRACT.md`, `docs/SYSTEMVERILOG_WORKFLOW_BOUNDARY.md`, `editors/vscode-prototype/docs/*consumer*.md`, `src/pccx_ide_cli/` |
| `pccx-launcher` | `d3313ac0a590` | `contracts/fixtures/*.json`, `docs/LAUNCHER_IDE_BRIDGE_CONTRACT.md`, `docs/RUNTIME_READINESS_STATUS.md`, `docs/DIAGNOSTICS_HANDOFF_CONTRACT.md`, 디바이스/세션 상태 문서 |
| `pccx-lab` | `53388ef2cc2d` | `docs/CLI_CORE_BOUNDARY.md`, `docs/CLI_BOUNDARY_EXAMPLES.md`, `docs/examples/*.json`, `crates/core/src/bin/pccx_lab.rs` |

## 저장소 역할

| 저장소 | 역할 |
| --- | --- |
| `systemverilog-ide` | 진단, 네비게이션, bounded context, 제안 제시를 담당하는 에디터 cockpit. |
| `pccx-launcher` | 사용자용 launcher/status surface. 로컬 read-only 디바이스/세션, 적합성, 채팅, diagnostics-handoff 상태를 제공한다. |
| `pccx-lab` | CLI/core-first 검증, diagnostics, workflow, trace/report, plugin-plan, 향후 tool-boundary backend를 담당한다. |

## 조사가 끝난 공개 surface

### `systemverilog-ide`

방출 데이터:

- `problems from-check`와 `problems from-xsim-log`에서 나오는
  `EditorProblemsEnvelope`.
- scanner 명령에서 나오는 `DeclarationIndex`, `DeclarationList`, `LocateResult`.
- read-only 조직화 flow에서 생성되는 `ModuleOrganizationReport`,
  `ModuleGraphHealth`, `RefactorImpact`, `RefactorPlan`, `RefactorReview`.
- VS Code prototype boundary에서 나오는 `WorkflowContextBundle`,
  `SelectedSymbolContext`, `ValidationProposal`,
  `ValidationResultSummary`, `ValidationPatchContextSeed`, `PatchProposal`.
- prototype descriptor로서 `PccxLabCommandDescriptor` 및 launcher 상태 요약.

소비 데이터:

- 명시적 `pccx-lab` diagnostics backend 경로에서 받는
  `LabDiagnosticsEnvelope`.
- prototype 상태/컨텍스트 소비자를 위한 로컬 검증 fixture로
  `LauncherDiagnosticsHandoff`, `LauncherDeviceSessionStatus`,
  `LauncherRuntimeReadinessStatus`.

소유/실행 금지:

- launcher 명령 실행, launcher 세션 시작, 모델 로드, 디바이스 접근, provider
  호출, MCP 런타임, marketplace 패키징, 저장소 변경, raw shell 명령 문자열은
  처리하지 않는다.
- 재사용 가능한 lab 분석/검증 동작은 수행하지 않는다. 이 부분은 `pccx-lab` CLI/core
  경계 뒤에서 처리한다.

### `pccx-launcher`

방출 데이터:

- 향후 에디터 소비자를 위한 `LauncherIdeStatus`.
- descriptor-only 모델/런타임 메타데이터인 `ModelRuntimeDescriptor`.
- evidence-aware한 blocked/planned 상태 데이터인 `RuntimeReadinessStatus`.
- status panel, discovery, flow, 오류 분류에 쓰이는 `DeviceSessionStatus` 데이터.
- 향후 `pccx-lab` 검증을 위한 `DiagnosticsHandoff`.
- 비활성화/read-only로 제공되는 `ChatStatusSummary`, `ChatSession`,
  `ChatReadiness`, `ChatComposer`, `ChatModelStatus`, `ChatPolicy`,
  `ChatEvidenceManifest` 및 관련 standalone chat fixture.

소비 데이터:

- 명시적 read-only 백엔드 경로 `pccx-lab status --format json`를 통해
  `LabRunStatus`를 수신한다.

소유/실행 금지:

- RTL/provider 작업, lab 검증 flow, 에디터 workflow, 디바이스 접근, 모델 로드,
  provider 호출, 네트워크 스캔, 텔레메트리, 업로드, write-back,
  저장소 변경, release/tag 동작, 성능 수치 주장은 수행하지 않는다.

### `pccx-lab`

방출 데이터:

- CLI/core 명령으로 `LabRunStatus`, `ThemeTokens`, `WorkflowDescriptors`,
  `WorkflowProposals`, `WorkflowResultSummaries`, `LabDiagnosticsEnvelope`.
- fixture/inventory 건강성 보고를 위한 `JsonBoundaryHealthSummary`.
- descriptor-only 또는 blocked-gate planning 데이터인
  `McpReadOnlyToolPlan`, `McpToolList`, `McpToolDetail`,
  `McpPermissionModel`, `McpApprovalRequest`, `McpInvocationRequest`,
  `McpClientSessionState`, `McpBlockedInvocationResult`, `McpAuditEvent`.
- descriptor-only 또는 blocked-gate planning 데이터인
  `PluginBoundaryPlan`, `PluginPermissionModel`, `PluginLoadRequest`,
  `PluginHostSessionState`, `PluginInvocationRequest`,
  `PluginReviewPacket`, `PluginDryRunFlow`, `PluginInputContract`,
  `PluginOutputContract`, `PluginAuditEvent`.

소비 데이터:

- `pccx-lab diagnostics-handoff validate --file <path> --format json` 경유로
  `LauncherDiagnosticsHandoff` 수신.
- `pccx-lab device-session-status validate --file <path> --format json` 경유로
  `LauncherDeviceSessionStatus` 수신.
- 로컬 `analyze` 진단을 위한 SystemVerilog 소스 파일.

소유/실행 금지:

- launcher 런타임/세션 동작, 에디터 커맨드 UX, provider 호출, 네트워크 flow,
  하드웨어 제어, 형제 저장소 변경, plugin-interface 적합성 보장, GUI-only
  workflow 로직은 수행하지 않는다. GUI는 CLI/core 또는 typed IPC 데이터에 대한
  얇은 surface로 유지한다.

## 생산자/소비자 매트릭스

Cells는 특정 producer 저장소에서 consumer 저장소로 넘어갈 수 있는 데이터
클래스 목록이다. 빈 칸 또는 `None today`는 의도된 boundary다.

| Producer \ Consumer | `systemverilog-ide` | `pccx-launcher` | `pccx-lab` |
| --- | --- | --- | --- |
| `systemverilog-ide` | `EditorProblemsEnvelope`, `DeclarationIndex`, `LocateResult`, `WorkflowContextBundle`, `ValidationProposal`, `PatchProposal`, `ValidationResultSummary` | 현재는 없음. 향후 후보는 `BoundedEditorContextSummary`와 같은 제안/컨텍스트 데이터만 허용. | 현재는 직접 소비 대상 없음. lab 소유 분석은 `pccx-lab`에서만 노출되고 IDE에서 직접 푸시하지 않음. |
| `pccx-launcher` | `LauncherIdeStatus`, `ModelRuntimeDescriptor`, `RuntimeReadinessStatus`, `DeviceSessionStatus`, `DiagnosticsHandoff`, `ChatStatusSummary` | `LauncherStatusSummary`, `DeviceSessionStatus`, `RuntimeReadinessStatus`, `ChatSurfaceFixtures` | `DiagnosticsHandoff`, `DeviceSessionStatus` |
| `pccx-lab` | `LabDiagnosticsEnvelope`, `LabRunStatus`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries`, `PccxLabCommandDescriptor` | `LabRunStatus` | `LabRunStatus`, `ThemeTokens`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries`, `JsonBoundaryHealthSummary`, `McpDescriptorFixtures`, `PluginDescriptorFixtures` |

## 금지된 저장소 간 동작

### 실행(Execution)

- IDE는 `pccx-launcher`를 실행하지 않고, launcher 세션을 시작하지 않으며
  모델 로드, 디바이스 probe, launcher JSON의 명령 채널 변환을 수행하지 않는다.
- IDE는 명시적인 CLI/core 또는 descriptor 경계를 통해서만 `pccx-lab` 출력을
  사용한다. raw shell 문자열, 전이적 launcher 실행, 숨은 폴백 동작을 허용하지
  않는다.
- `pccx-launcher`는 status 렌더링의 부수효과로 lab 워크플로, RTL/provider
  flow, 에디터 명령, 모델/런타임 경로, 하드웨어 동작, provider 호출,
  MCP tool, release/tag 작업을 실행하지 않는다.
- `pccx-lab`는 launcher flow, 에디터 flow, provider flow 또는
  descriptor-only MCP/plugin 플랜을 실행하지 않는다.
- descriptor-only MCP/plugin 데이터는 MCP 런타임, plugin loader, tool invocation
  경로, 버전별 호환성 보장의 구현으로 간주되지 않는다.

### 변경(Mutation)

- 어떤 저장소도 데이터 계약을 통해 다른 저장소의 작업 트리로 파일을 쓰거나
  스테이징/커밋/푸시/tag/release를 수행하지 않는다. 설정 변경이나 공개
  조정 산출물 작성도 금지.
- Proposal 객체는 검토된 변경 제안을 바운디드 미리보기로 설명할 수 있지만,
  실제 패치를 적용하지 않는다.
- handoff 및 상태 payload는 모델 가중치, 생성된 blob, 바이너리 아티팩트,
  bitstream, 전체 로그, private absolute path, 토큰, 시크릿 유사 값이 포함되지
  않아야 한다.

### 네트워크와 개인정보

- 어떤 호환성 payload도 네트워크 스캔, 텔레메트리, 업로드, provider 호출,
  외부 API 호출, marketplace 공개, 원격 에디터/lab/launcher 제어를 허용하지
  않는다.
- 소비자는 향후 검토된 계약에서 해당 필드가 명시 허용된 경우를 제외하고,
  private home 경로, credentials, provider 설정, raw prompts, raw transcripts,
  source dumps, artifact 경로를 제거하거나 차단해야 한다.
- JSON 파일 handoff, stdout JSON handoff, read-only 로컬 산출물 참조는
  전달 방식 샘플일 뿐, watcher/daemon/uploader/background service가 아니다.

## 버전 관리와 호환성 창

세 저장소는 **release lock이 없다**. 각 저장소는 자체 SemVer 라인으로 배포할 수
있다. 호환성은 contract schema 버전과 이 매트릭스로 추적되며, 동시 릴리스를
요구하지 않는다.

규칙:

- additive, backwards-compatible JSON field는 기존 소비자가 안전하게 무시하거나
  명시적으로 검증할 수 있을 때만 최소 릴리스에서 반영된다.
- 필드 제거, enum 변경, 의미 변경, safety flag 제거는 schema 버전 상승과
  새 호환성 행 추가를 요구한다.
- `v0` 및 placeholder fixture는 초기 경계에서 허용되며, 공개 문서에는 필요에
  따라 pre-stable, descriptor-only, blocked, planned 상태가 명시돼야 한다.
- 동시 검증 행에서는 정확한 저장소 SHA, schema 버전, 데이터 클래스,
  검증 명령, known exclusions가 모두 명시돼야 한다.
- 하나의 호환성 행은 런타임/하드웨어/성능/marketplace/API/ABI 안정성
  보장으로 해석되지 않는다.

### 같이 검증한 행(Tested-together registry)

| Compat row | `systemverilog-ide` window | `pccx-launcher` window | `pccx-lab` window | Data classes in scope | Evidence state |
| --- | --- | --- | --- | --- | --- |
| `compat-2026-05-data-v0` | `0.x` pre-stable editor JSON consumers @ `992fb0f24d5d` | `0.x` pre-stable status/handoff fixtures @ `d3313ac0a590` | `0.x` pre-stable CLI/core JSON validators @ `53388ef2cc2d` | `DiagnosticsHandoff`, `DeviceSessionStatus`, `RuntimeReadinessStatus`, `LauncherIdeStatus`, `LabRunStatus`, `LabDiagnosticsEnvelope`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries` | 소스 조사 기반 후보 행. release 지원으로 분류하려면 정식 상위 검토에서 검증 로그를 함께 첨부해야 함. |

## 오픈 질문

최상위 검토를 위한 TODO:

- `RuntimeReadinessStatus`를 `DiagnosticsHandoff`, `DeviceSessionStatus`와 같이
  lab 검증을 거친 consumer contract로 둘지 아니면 launcher/IDE status 데이터로
  둘지 결정.
- `LauncherIdeStatus`를 에디터 소비자용 상위 launcher 상태 계약으로 삼을지,
  readiness/device/session/diagnostics-handoff/chat-status fixture와 분리할지
  결정.
- repo-local fixture 및 문서에 남아 있는 구버전 launcher 식별자를
  `pccx-launcher` 네임으로 스키마 의미를 바꾸지 않고 이전.
- 첫 번째 공개 호환성 행 기준을 결정: 정확한 검증 명령, 필수 CI job,
  fixture 복사 정책, 리뷰 책임자(owner) 설정.
- 이 umbrella 페이지를 검토 동안 orphan 상태로 둘지, 승인 후 공개 repo-boundary/
  reference 탐색에서 링크할지 결정.
- `v0` fixture를 스키마 bump 이후 얼마만큼 보관할지와 폐기 공지 위치를
  producer 문서, consumer 문서, 아니면 이 매트릭스 중 어디로 넣을지 결정.
