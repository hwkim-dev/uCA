# Module Overview

`pccx-lab` is composed of 4 core modules.

## `core/`
The pure Rust simulation and cycle prediction engine. It has absolutely no dependencies on UI or other frameworks.

## `ui/`
The Tauri and React-based frontend shell. It uses the public APIs of `core/` to provide visualization.

## `uvm_bridge/`
Handles the boundary between SystemVerilog/UVM and `core/`. Communicates via DPI-C or FFI.

## `ai_copilot/`
The LLM invocation wrapper module. Depends only on the trace format of `core/`.
