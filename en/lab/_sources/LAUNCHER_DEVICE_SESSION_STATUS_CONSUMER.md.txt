# Launcher Device/Session Status Consumer

This note describes the pccx-lab-side reader for launcher
device/session status JSON. It is a read-only schema reader and
validator. It does not execute pccx-llm-launcher, open serial ports,
scan networks, attempt authentication, probe hardware, load models,
start GUI workflows, stream logs, or write files.

The implementation lives in:

- `crates/core/src/device_session_status.rs`
- `crates/core/tests/device_session_status_cli.rs`
- `docs/examples/launcher-device-session-status.example.json`

## What Is Implemented

pccx-lab can parse a local launcher device/session status JSON document,
validate the expected shape, and produce a deterministic summary. The
summary includes:

- status identity
- target device, board, and model
- connection, discovery, authentication, runtime, model-load, session,
  log-stream, diagnostics, and readiness states
- status-panel row ids and states
- discovery path, flow step, and error counts
- read-only safety flags
- limitations and issue references carried by the input

The validator is deliberately strict about the current placeholder
fixture. It checks required fields, status-panel rows, discovery path
transports, contiguous flow-step ordering, error taxonomy values,
pccx-lab diagnostics flags, and read-only safety flags.

## CLI Boundary

The CLI command is:

```bash
pccx-lab device-session-status validate --file <path> --format json
```

`--format json` is the only supported output format. The command reads
the file supplied by the caller and emits a JSON validation summary. The
summary does not echo the input path, so a private local path is not
copied into the output.

The command exits:

- `0` for a valid status document
- `1` for invalid JSON shape or unsafe status content
- `2` for CLI usage or read errors

## Fixture Scope

The checked fixture mirrors the launcher-side placeholder status from
pccx-llm-launcher. It is sanitized and local:

- no raw logs
- no prompts
- no private absolute paths
- no secrets or tokens
- no provider configuration
- no model weight paths
- no generated blobs or hardware dumps
- no serial, network, SSH, authentication, runtime, or launcher action

Fixture sync is manual for now. That keeps the consumer boundary
reviewable while the launcher contract is still pre-compatibility.

## Non-Goals

This boundary does not add:

- launcher execution
- pccx-lab execution of launcher flows
- serial or network access
- authentication
- provider calls
- telemetry
- automatic upload
- automatic write-back
- plugin loading
- MCP implementation
- GUI workflow ownership
- IDE integration
- hardware access
- model loading or model execution
- log streaming
- marketplace or publisher flow
- a versioned API or ABI commitment

Future integration should remain CLI/core-first. GUI or editor surfaces
may display the resulting summary later, but the validation logic should
stay in pccx-core or an explicit CLI boundary rather than becoming a GUI
logic island.
