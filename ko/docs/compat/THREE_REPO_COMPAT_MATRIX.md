---
orphan: true
---

# Three-repo compatibility matrix

Scope: `systemverilog-ide`, `pccx-launcher`, and `pccx-lab`.

This page mirrors the English source page for the current EN/KO file-set
check. The canonical source for compatibility review is
`docs/compat/THREE_REPO_COMPAT_MATRIX.md`.

## Goals

- Keep cross-repo integration data-only unless a separate reviewed boundary
  explicitly allows something stronger.
- Make the public surfaces easy for external users to understand, test, and
  extend without needing private coordination notes.
- Grow the user pool by making each repository useful on its own: editor
  diagnostics/navigation, launcher status/readiness views, and lab
  verification/status summaries can evolve independently.
- Keep every status, readiness, and evidence payload evidence-gated. A field
  may describe a blocked, planned, unavailable, or descriptor-only state; it
  must not imply execution, device success, performance, or production
  readiness.
- Prefer small JSON contracts with checked fixtures, schema versions, strict
  validators, bounded text, no secret leakage, and explicit safety flags.

## Source evidence snapshot

This matrix was surveyed from the local public repo checkouts at:

| Repo | Commit surveyed | Public surface examples |
| --- | --- | --- |
| `systemverilog-ide` | `992fb0f24d5d` | `docs/EDITOR_BRIDGE_CONTRACT.md`, `docs/SYSTEMVERILOG_WORKFLOW_BOUNDARY.md`, `editors/vscode-prototype/docs/*consumer*.md`, `src/pccx_ide_cli/` |
| `pccx-launcher` | `d3313ac0a590` | `contracts/fixtures/*.json`, `docs/LAUNCHER_IDE_BRIDGE_CONTRACT.md`, `docs/RUNTIME_READINESS_STATUS.md`, `docs/DIAGNOSTICS_HANDOFF_CONTRACT.md`, device/session status docs |
| `pccx-lab` | `53388ef2cc2d` | `docs/CLI_CORE_BOUNDARY.md`, `docs/CLI_BOUNDARY_EXAMPLES.md`, `docs/examples/*.json`, `crates/core/src/bin/pccx_lab.rs` |

## Repo roles

| Repo | Role |
| --- | --- |
| `systemverilog-ide` | Editor cockpit for diagnostics, navigation, bounded context, and reviewed proposal presentation. |
| `pccx-launcher` | User-facing launcher/status surface that emits local, read-only device/session, readiness, chat, and diagnostics-handoff data. |
| `pccx-lab` | CLI/core-first verification, diagnostics, workflow, trace/report, plugin-plan, and future tool-boundary backend. |

## Surveyed public surfaces

### `systemverilog-ide`

Emits:

- `EditorProblemsEnvelope` from `problems from-check` and
  `problems from-xsim-log`.
- `DeclarationIndex`, `DeclarationList`, and `LocateResult` from scanner
  commands.
- `ModuleOrganizationReport`, `ModuleGraphHealth`, `RefactorImpact`,
  `RefactorPlan`, and `RefactorReview` from read-only organization flows.
- `WorkflowContextBundle`, `SelectedSymbolContext`, `ValidationProposal`,
  `ValidationResultSummary`, `ValidationPatchContextSeed`, and
  `PatchProposal` from the VS Code prototype boundary.
- `PccxLabCommandDescriptor` and launcher status summaries as data-only
  prototype descriptors.

Consumes:

- `LabDiagnosticsEnvelope` from the explicit `pccx-lab` diagnostics backend
  path.
- `LauncherDiagnosticsHandoff`, `LauncherDeviceSessionStatus`, and
  `LauncherRuntimeReadinessStatus` as local checked JSON fixtures for
  prototype status/context consumers.

Must not own or execute:

- Launcher commands, launcher sessions, model loading, device access, provider
  calls, MCP runtime, marketplace packaging, repository mutation, or raw shell
  command strings.
- Reusable lab analysis or verification behavior. That stays behind the
  `pccx-lab` CLI/core boundary.

### `pccx-launcher`

Emits:

- `LauncherIdeStatus` for future editor consumers.
- `ModelRuntimeDescriptor` as descriptor-only model/runtime metadata.
- `RuntimeReadinessStatus` as evidence-aware blocked/planned status data.
- `DeviceSessionStatus` as status-panel, discovery, flow, and error-taxonomy
  data.
- `DiagnosticsHandoff` for future `pccx-lab` validation.
- `ChatStatusSummary`, `ChatSession`, `ChatReadiness`, `ChatComposer`,
  `ChatModelStatus`, `ChatPolicy`, `ChatEvidenceManifest`, and related
  standalone chat surface fixtures as disabled/read-only data.

Consumes:

- `LabRunStatus` through an explicit, read-only `pccx-lab status --format json`
  backend path.

Must not own or execute:

- RTL/provider work, lab verification flows, editor workflows, hardware access,
  model loading, provider calls, network scans, telemetry, uploads, write-back,
  repository mutation, release/tag actions, or performance claims.

### `pccx-lab`

Emits:

- `LabRunStatus`, `ThemeTokens`, `WorkflowDescriptors`,
  `WorkflowProposals`, `WorkflowResultSummaries`, and
  `LabDiagnosticsEnvelope` through CLI/core commands.
- `JsonBoundaryHealthSummary` for fixture/inventory health reporting.
- `McpReadOnlyToolPlan`, `McpToolList`, `McpToolDetail`,
  `McpPermissionModel`, `McpApprovalRequest`, `McpInvocationRequest`,
  `McpClientSessionState`, `McpBlockedInvocationResult`, and
  `McpAuditEvent` as descriptor-only or blocked-gate planning data.
- `PluginBoundaryPlan`, `PluginPermissionModel`, `PluginLoadRequest`,
  `PluginHostSessionState`, `PluginInvocationRequest`,
  `PluginReviewPacket`, `PluginDryRunFlow`, `PluginInputContract`,
  `PluginOutputContract`, and `PluginAuditEvent` as descriptor-only or
  blocked-gate planning data.

Consumes:

- `LauncherDiagnosticsHandoff` through
  `pccx-lab diagnostics-handoff validate --file <path> --format json`.
- `LauncherDeviceSessionStatus` through
  `pccx-lab device-session-status validate --file <path> --format json`.
- SystemVerilog source files for local `analyze` diagnostics.

Must not own or execute:

- Launcher runtime/session behavior, editor command UX, provider calls,
  network flows, hardware control, sibling repo mutation, plugin-interface
  compatibility promises, or GUI-only workflow logic. The GUI remains a thin
  surface over CLI/core or typed IPC data.

## Producer / consumer matrix

Cells list the data classes that may cross from a producer repo to a consumer
repo. Empty or `None today` cells are intentional boundaries.

| Producer \ Consumer | `systemverilog-ide` | `pccx-launcher` | `pccx-lab` |
| --- | --- | --- | --- |
| `systemverilog-ide` | `EditorProblemsEnvelope`, `DeclarationIndex`, `LocateResult`, `WorkflowContextBundle`, `ValidationProposal`, `PatchProposal`, `ValidationResultSummary` | None today. Future candidates must be proposal/context data only, such as `BoundedEditorContextSummary`. | None today for direct consumption. Lab-owned analysis remains exposed from `pccx-lab`, not pushed from the IDE. |
| `pccx-launcher` | `LauncherIdeStatus`, `ModelRuntimeDescriptor`, `RuntimeReadinessStatus`, `DeviceSessionStatus`, `DiagnosticsHandoff`, `ChatStatusSummary` | `LauncherStatusSummary`, `DeviceSessionStatus`, `RuntimeReadinessStatus`, `ChatSurfaceFixtures` | `DiagnosticsHandoff`, `DeviceSessionStatus` |
| `pccx-lab` | `LabDiagnosticsEnvelope`, `LabRunStatus`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries`, `PccxLabCommandDescriptor` | `LabRunStatus` | `LabRunStatus`, `ThemeTokens`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries`, `JsonBoundaryHealthSummary`, `McpDescriptorFixtures`, `PluginDescriptorFixtures` |

## Forbidden cross-repo behaviors

### Execution

- The IDE must not execute `pccx-launcher`, start launcher sessions, load
  models, probe devices, or turn launcher JSON into a command channel.
- The IDE may only use `pccx-lab` outputs through explicit CLI/core or
  descriptor boundaries. No raw shell strings, transitive launcher execution,
  or hidden fallback behavior.
- `pccx-launcher` must not execute lab workflows, RTL/provider flows, editor
  commands, model/runtime paths, hardware actions, provider calls, MCP tools,
  or release/tag operations as a side effect of status rendering.
- `pccx-lab` must not execute launcher flows, editor flows, provider flows, or
  descriptor-only MCP/plugin plans.
- Descriptor-only MCP/plugin data is not an implementation of an MCP runtime,
  plugin loader, tool invocation path, or versioned compatibility promise.

### Mutation

- No repo may write into another repo's working tree, stage files, commit,
  push, tag, release, change settings, or write public coordination artifacts
  through these data contracts.
- Proposal objects may describe reviewed edits with bounded previews, but they
  do not apply patches.
- Handoff and status payloads must not contain model weights, generated blobs,
  binary artifacts, bitstreams, full logs, private absolute paths, tokens, or
  secret-like assignments.

### Network and privacy

- No compatibility payload grants permission for network scans, telemetry,
  uploads, provider calls, external API calls, marketplace publishing, or
  remote editor/lab/launcher control.
- Consumers should reject or redact private home paths, credentials, provider
  configuration, raw prompts, raw transcripts, source dumps, and artifact
  paths unless a later reviewed contract explicitly allows the exact field.
- JSON file handoff, stdout JSON handoff, and read-only local artifact
  references are transport sketches only; they are not watchers, daemons,
  uploaders, or background services.

## Versioning and compatibility windows

The three repos are **not release-locked**. Each repo may release on its own
SemVer line. Compatibility is tracked by contract schema versions and by this
matrix, not by requiring simultaneous repo releases.

Rules:

- Additive, backwards-compatible JSON fields may ship in a repo minor release
  only when existing consumers either ignore them safely or validate them
  explicitly.
- Breaking field removals, enum changes, semantic meaning changes, or safety
  flag removals require a schema-version bump and a new compatibility row.
- `v0` and placeholder fixtures are allowed for early boundaries, but public
  docs must keep them marked pre-stable, descriptor-only, blocked, or planned
  as appropriate.
- Tested-together rows must name exact repo SHAs, schema versions, data
  classes, validation commands, and known exclusions.
- A compatibility row is not a runtime, hardware, performance, marketplace, or
  API/ABI stability claim.

### Tested-together registry

| Compat row | `systemverilog-ide` window | `pccx-launcher` window | `pccx-lab` window | Data classes in scope | Evidence state |
| --- | --- | --- | --- | --- | --- |
| `compat-2026-05-data-v0` | `0.x` pre-stable editor JSON consumers at `992fb0f24d5d` | `0.x` pre-stable status/handoff fixtures at `d3313ac0a590` | `0.x` pre-stable CLI/core JSON validators at `53388ef2cc2d` | `DiagnosticsHandoff`, `DeviceSessionStatus`, `RuntimeReadinessStatus`, `LauncherIdeStatus`, `LabRunStatus`, `LabDiagnosticsEnvelope`, `WorkflowDescriptors`, `WorkflowProposals`, `WorkflowResultSummaries` | Candidate row from source survey. Top review must attach exact validation logs before this is described as release-supported. |

## Open questions

TODO for top review:

- Decide whether `RuntimeReadinessStatus` should be a lab-side validated
  consumer contract like `DiagnosticsHandoff` and `DeviceSessionStatus`, or
  remain launcher/IDE status data only.
- Decide whether `LauncherIdeStatus` should become the umbrella launcher
  status contract for editor consumers, or stay separate from readiness,
  device/session, diagnostics-handoff, and chat-status fixtures.
- Audit remaining legacy launcher identifiers in repo-local fixtures and docs
  and migrate them to `pccx-launcher` without changing schema semantics.
- Pick the first public compatibility row criteria: exact validation commands,
  required CI jobs, fixture-copy policy, and review owner per repo.
- Decide whether this umbrella page should stay orphaned during review or be
  linked from the public repo-boundary/reference navigation after approval.
- Define how long each repo must keep old `v0` fixtures available after a
  schema bump, and whether deprecation notices live in producer docs,
  consumer docs, or this matrix.
