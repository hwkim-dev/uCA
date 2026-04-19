# 모듈 개요

`pccx-lab`은 4개의 핵심 모듈로 구성됩니다.

## `core/`
가장 핵심이 되는 순수 Rust 시뮬레이션 및 사이클 예측 엔진입니다. UI나 다른 프레임워크에 대한 의존성이 전혀 없습니다.

## `ui/`
Tauri와 React 기반의 프론트엔드 쉘입니다. `core/`의 공개 API를 사용하여 시각화를 제공합니다.

## `uvm_bridge/`
SystemVerilog/UVM과 `core/` 사이의 경계를 담당합니다. DPI-C나 FFI를 통해 통신합니다.

## `ai_copilot/`
LLM 호출 래퍼 모듈입니다. `core/`의 트레이스 포맷에만 의존합니다.
