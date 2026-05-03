# Launcher Diagnostics Handoff Consumer

This note describes the first pccx-lab-side boundary for launcher
diagnostics handoff JSON. It is a read-only schema reader and validator.
It does not execute pccx-llm-launcher, load plugins, call providers,
probe hardware, start GUI workflows, or write files.

The implementation lives in:

- `crates/core/src/diagnostics_handoff.rs`
- `crates/core/tests/diagnostics_handoff_cli.rs`
- `docs/examples/launcher-diagnostics-handoff.example.json`

## What Is Implemented

pccx-lab can parse a local launcher diagnostics handoff JSON document,
validate the expected shape, and produce a deterministic summary. The
summary includes:

- handoff identity
- producer and consumer ids
- target kind
- diagnostic counts by severity
- diagnostic counts by category
- read-only and privacy flags
- launcher/model/runtime descriptor references
- transport sketch kinds
- limitations carried by the handoff

The validator is deliberately strict about the current placeholder
fixture. It checks required fields, diagnostic severity/category values,
descriptor reference fields, transport sketch kinds, read-only flags,
and privacy flags.

## CLI Boundary

The CLI command is:

```bash
pccx-lab diagnostics-handoff validate --file <path> --format json
```

`--format json` is the only supported output format. The command reads
the file supplied by the caller and emits a JSON validation summary. The
summary does not echo the input path, so a private local path is not
copied into the output.

The command exits:

- `0` for a valid handoff
- `1` for invalid JSON shape or unsafe handoff content
- `2` for CLI usage or read errors

## Fixture Scope

The checked fixture mirrors the launcher-side placeholder handoff from
pccx-llm-launcher. It is sanitized and local:

- no raw full logs
- no prompts
- no source code
- no private absolute paths
- no secrets or tokens
- no provider configuration
- no model weight paths
- no generated blobs or hardware dumps

Fixture sync is manual for now. That keeps the consumer boundary
reviewable while the launcher contract is still pre-compatibility.

## Non-Goals

This boundary does not add:

- launcher execution
- pccx-lab execution of launcher flows
- provider calls
- network calls
- telemetry
- automatic upload
- automatic write-back
- plugin loading
- MCP implementation
- GUI workflow ownership
- IDE integration
- hardware access
- model execution
- marketplace or publisher flow
- a versioned API or ABI commitment

Future integration should remain CLI/core-first. GUI or editor surfaces
may display the resulting summary later, but the validation logic should
stay in pccx-core or an explicit CLI boundary rather than becoming a GUI
logic island.
