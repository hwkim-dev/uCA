# Workflow Facade

_페이지 과도기 상태. pccx-lab HEAD 기준 2026-04-24 재정비._

이 페이지는 현재 pccx-lab workflow facade 를 문서화한다. Tauri UI 가
사용하는 트레이스 요약, UVM 시퀀스 스캐폴드, 확장 카탈로그 데이터,
SystemVerilog 편집기 연동이 이 경계에 놓인다. 이 표면은 아직
pre-stable 이며 pccx-lab v0.3 작업이 정리될 때까지 구현 경계로
취급해야 한다.

## 정적 헬퍼

네 가지 헬퍼는 장기 실행 서비스 객체 없이 호출된다.

| Helper | 목적 |
|---|---|
| `compress_context` | 트레이스 통계를 간결한 LLM context 문자열로 축약. |
| `generate_uvm_sequence` | 명명된 완화 전략에 대한 SystemVerilog UVM 시퀀스 스텁 반환. |
| `list_uvm_strategies` | UVM 시퀀스 생성기가 받는 전략 slug 열거. |
| `get_available_extensions` | Tauri UI 가 렌더하는 확장 카탈로그 반환. |

현재 UVM 전략 slug:

| Slug | 동작 |
|---|---|
| `l2_prefetch` | DMA 읽기를 AXI 트랜잭션 오버헤드 기준으로 분산. |
| `barrier_reduction` | 글로벌 sync 대신 wavefront barrier 사용. |
| `dma_double_buffer` | 인접 타일에서 compute 와 DMA 를 ping-pong. |
| `systolic_pipeline_warmup` | 첫 실제 타일 전 MAC 배열 pre-roll. |
| `weight_fifo_preload` | 설정 구간 동안 HP weight FIFO front-load. |

더 풍부한 전략 세트 (`back_pressure_gate`, `kv_cache_thrash_probe`,
`speculative_draft_probe` 등)는 아직 재착륙하지 않았다. 진행 상황은
pccx-lab `docs/design/phase5_alphaevolve.md` 설계 노트에서 추적한다.

## Provider Traits

향후 workflow 확장을 위해 `plugin-api` 피처 뒤에 두 가지 unstable
스캐폴드가 있다. 하나는 트레이스나 문서 발췌를 압축하는 context
compressor 이고, 다른 하나는 제한된 분석 작업용 task runner 이다.
pccx-lab v0.2.x 에는 구체 구현이 동봉되지 않는다. 다운스트림 소비자는
pccx-lab v0.3 까지 시그니처가 변경될 수 있다고 봐야 한다.

## pccx-lsp

LSP facade 는 편집기 라우팅이 놓이는 경계다. 현재 슬라이스에는
`LspMultiplexer`, `NoopBackend`, async bridge helper, JSON-RPC wire framing,
SystemVerilog keyword/hover provider 가 포함된다. verible, rust-analyzer,
clangd 같은 외부 LSP 서버는 `SpawnConfig` 와 `LspSubprocess` 를 통해
실행되며, 남은 pipe codec 작업은 후속 슬라이스에서 다룬다.

`CompletionSource` 는 upstream LSP, fast runtime predictor, deeper runtime
predictor, AST-hash cache 결과를 구분해 UI 가 각 제안 옆에 provenance 를
표시할 수 있게 한다.

## UI 지향 커맨드

전면 facade 도입 전까지 Tauri UI 는 `invoke("compress_context", ...)`,
`invoke("generate_uvm_sequence", ...)`, `invoke("list_uvm_strategies")` 로
정적 헬퍼를 직접 호출한다. 브리지는 `ui/src-tauri/src/lib.rs` 의 얇은
커맨드 계층이다.

전체 Tauri 커맨드 카탈로그와 u64-as-string, `generation_id`, 원시
트레이스의 IPC payload 제외 규칙은 [IPC 레퍼런스](ipc.md)에 있다.

## 관련 문서

- [분석기 API](analyzer_api.md) - 크레이트별 플러그인 트레이트가
  사용하는 플러그인 레지스트리 프리미티브.
- [CLI 레퍼런스](cli.md) - 현재 출하 중인 바이너리. 과거
  `pccx_analyze` 우산은 오늘 존재하지 않는다.

## 이 페이지 인용

```bibtex
@misc{pccx_lab_workflow_facade_2026,
  title        = {pccx-lab workflow facade and SystemVerilog editor boundary after Phase 1},
  author       = {Kim, Hyunwoo},
  year         = {2026},
  howpublished = {\url{https://pccx.pages.dev/ko/docs/Lab/workflow_facade.html}},
  note         = {Part of pccx: \url{https://pccx.pages.dev/}}
}
```

LSP facade 구현은
<https://github.com/pccxai/pccx-lab/blob/main/crates/lsp/src/lib.rs> 에 있다.
