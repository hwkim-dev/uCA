# pccx-lab CLI boundary examples

This page shows how GUI, editor-adjacent, launcher-adjacent, CI, and
future tool consumers should read pccx-lab boundary data. It is a
handoff guide over the existing CLI/core contracts, not a new runtime
integration.

Use the full fixtures in [`docs/examples/`](examples/) as the source of
truth for field shape. The snippets below are intentionally partial.

## Consumer rule

All consumers should enter through the CLI or the typed Tauri IPC
wrappers backed by `pccx-core`.

| Consumer | Boundary to use | Rule |
|---|---|---|
| GUI | Tauri IPC wrappers over core structs | Render core data; do not duplicate workflow logic. |
| CI or headless worker | `pccx-lab ... --format json` | Parse deterministic JSON and keep logs bounded. |
| Future editor consumer | CLI JSON, then reviewed IPC if needed | Do not bypass pccx-lab or read private GUI state. |
| Future launcher consumer | Status, diagnostics handoff, proposals, summaries | Treat runtime bridges as separate reviewed work. |
| Future MCP/tool consumer | Descriptor and proposal JSON | Consume descriptor-only contracts until a controlled adapter exists. |

No stable plugin ABI is promised. No provider, launcher, editor, or MCP
runtime is implemented by these examples.

## Status

```bash
pccx-lab status --format json
```

Full fixture: [`run-status.example.json`](examples/run-status.example.json)

```json
{
  "schemaVersion": "pccx.lab.status.v0",
  "labMode": "cli-first-gui-foundation",
  "workspaceState": {
    "state": "host-ready",
    "traceLoaded": false,
    "source": "static-core-status"
  },
  "evidenceState": {
    "hardwareProbe": "not-run",
    "timingClosure": "not-claimed",
    "inference": "not-claimed",
    "throughput": "not-claimed"
  }
}
```

Use this for lightweight shell, GUI, CI, and future tool status. It
does not load traces or probe hardware.

## Theme

```bash
pccx-lab theme --format json
```

Full fixture: [`theme-tokens.example.json`](examples/theme-tokens.example.json)

```json
{
  "schemaVersion": "pccx.lab.theme-tokens.v0",
  "tokenSlots": [
    "background",
    "foreground",
    "mutedForeground",
    "border",
    "panelBackground",
    "accent",
    "danger",
    "warning",
    "success"
  ],
  "presets": [
    {
      "name": "native-light"
    }
  ]
}
```

Use this to keep GUI surfaces theme-neutral. Do not hardcode workflow
state into theme tokens.

## Workflow Descriptors

```bash
pccx-lab workflows --format json
```

Full fixture:
[`workflow-descriptors.example.json`](examples/workflow-descriptors.example.json)

```json
{
  "workflowId": "lab-status-contract",
  "category": "status",
  "executionState": "descriptor_only",
  "evidenceState": "metadata-only",
  "futureConsumers": [
    "GUI",
    "CI/headless worker",
    "future IDE/launcher consumer",
    "future MCP/tool consumer"
  ]
}
```

Use descriptors to discover what the lab can describe. Descriptors are
not runs and must not be treated as approval to execute anything.

## Workflow Proposals

```bash
pccx-lab workflow-proposals --format json
```

Full fixture:
[`workflow-proposals.example.json`](examples/workflow-proposals.example.json)

```json
{
  "proposalId": "proposal-lab-status-contract",
  "workflowId": "lab-status-contract",
  "proposalState": "proposal_only",
  "approvalRequired": false,
  "fixedArgsPreview": [
    "status",
    "--format",
    "json"
  ]
}
```

Use proposals to show what a later approved run would do. The preview
is structured tokens, not a raw shell string.

## Workflow Results

```bash
pccx-lab workflow-results --format json
```

Full fixture:
[`workflow-results.example.json`](examples/workflow-results.example.json)

```json
{
  "proposalId": "proposal-lab-status-contract",
  "workflowId": "lab-status-contract",
  "status": "blocked",
  "outputPolicy": "summary-only; stdout and stderr lines are omitted",
  "summary": "Workflow did not run because runner execution is disabled."
}
```

Use summaries to display bounded outcomes. Full logs, generated
artifacts, provider logs, hardware logs, and private paths stay outside
this summary contract.

## Handoff Checklist

- Prefer checked-in example fixtures over copied ad hoc JSON.
- Keep command arguments structured and bounded.
- Keep GUI and future consumers read-only until a reviewed execution
  boundary exists.
- Treat diagnostics handoff data as summaries, not as launcher runtime
  control.
- Keep future tool adapters descriptor-only until their safety boundary
  is reviewed.
