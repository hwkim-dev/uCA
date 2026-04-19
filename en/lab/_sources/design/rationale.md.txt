# Design Rationale

## Why pccx-lab is one repo, not five

In the initial design, we considered a 5-repo structure (simulator / frontend / uvm-bridge / ai / common). However, this was rejected for the following reasons:

1. **Development Speed**: The overhead of synchronizing changes and managing versions across multiple repositories is massive.
2. **Single Purpose**: All modules ultimately work closely together towards the single goal of "pccx profiling".

## Module Boundary Rules

To prevent the downside of a monorepo (spaghetti code), we enforce strict module boundaries based on directories:

- `core/`: Pure Rust module. Minimizes external dependencies and strictly forbids importing UI frameworks.
- `ui/`: Tauri + React-based module. Only uses the public APIs of `core/` to handle visualization.
- `uvm_bridge/`: The boundary between SystemVerilog/UVM and `core/`. Uses DPI-C or FFI.
- `ai_copilot/`: LLM invocation wrapper module. Depends solely on the trace format (e.g., JSON) of `core/`.

## Conditions for Future Separation

If a specific module (e.g., `core/`) becomes generic enough to be used independently in other projects outside of pccx-lab, we will then consider publishing it as a crate or separating it into its own repository.
