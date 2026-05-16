---
myst:
  html_meta:
    description lang=ko: |
      pccx NPU의 원-커맨드(one-command) 재현 가이드 — clone, build, 샘플 .pccx 트레이스
      로딩, Sail 형식 모델 실행, pccx-lab 프로파일러 열기.  Docker
      레시피 + 네이티브 bare-metal 경로 모두 Ubuntu 24.04 에서 검증.
---

# 퀵스타트

`git clone` 에서 "pccx 트레이스를 보고 있다" 까지의 최단 경로.
이 페이지는 **재현 가이드**입니다. `docker compose up` 명령어 한 번으로 샘플
캡처가 로딩된 프로파일러가 실행 상태로 구동되어야 합니다.

## 0. 얻게 되는 산출물

```{mermaid}
flowchart LR
    A[RTL Repository<br>Vivado Synth] -->|생성| B(16-토큰 .pccx 트레이스)
    A -->|산출| C(Sail ISA 모델)
    
    B -.->|로딩| D{pccx-lab 프로파일러}
    C -.->|타입체크| E[OCaml / opam]
    
    D --> F[CLI Analytics<br>roofline / report]
    D --> G[Tauri Desktop 앱<br>Visual IDE]
    
    style D fill:#ff7a00,stroke:#fff,color:#fff
```

| 산출물 | 생성 주체 | 여는 도구 |
|---|---|---|
| `.pccx` 트레이스 (16-토큰 Gemma-3N 디코드) | `pccx-FPGA-NPU-LLM-kv260/hw/sim/run_verification.sh` | `pccx-lab` (Tauri 앱), `pccx_cli` |
| Sail ISA 모델 (타입체크 완료) | `pccx-FPGA-NPU-LLM-kv260/formal/sail/` | `sail`, `sail --doc` |
| Vivado synth + timing 리포트 | `pccx-FPGA-NPU-LLM-kv260/vivado/build.sh synth` | `pccx-lab` IDE → Verification → Synth Status |
| 트레이스 분석 | `pccx-lab` 워크스페이스 | `pccx_cli --roofline --report-md`, IDE 분석기 탭 |

## 1. 사전 조건

단일 64-bit Linux 머신 (Ubuntu 24.04 검증):

- `git` ≥ 2.40
- `opam` + `ocaml` ≥ 4.14 — Sail 용
- `docker` ≥ 24 — 재현기 컨테이너 용
- `rustup` (stable toolchain) — `pccx-core` + Tauri 용
- *(선택)* Xilinx Vivado 2024.1 — RTL 합성 경로
- *(선택)* Xilinx Kria KV260 보드 — 실측 토큰 생성

앞의 4개로만 **소프트웨어** 절반을 재현할 수 있습니다. 보드 접근은 선택입니다.

## 2. 세 레포 클론

pccx는 **3-레포 연합**입니다. ({doc}`index` 의 에코시스템 섹션 참고).
형제 디렉토리에 클론:

```bash
mkdir -p ~/pccx-ws && cd ~/pccx-ws
git clone https://github.com/pccxai/pccx.git                    # docs (이 사이트)
git clone https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260.git  # RTL + Sail 모델
git clone https://github.com/pccxai/pccx-lab.git                 # 프로파일러 + UVM workflow facade
```

## 3. 원-커맨드 재현기 (Docker)

```{admonition} 계획 단계 — 아직 미반영
:class: warning

Docker 재현기 (`scripts/docker/quickstart.yml`) 는 pccx-lab 로드맵에
올라가 있으나 아직 `main` 에 반영되지 않았습니다.  반영 전까지는 아래의
[네이티브 경로](#4-네이티브-경로-docker-없음)를 따르십시오 — 컨테이너가
내부적으로 실행할 내용과 동일합니다.
```

## 4. 네이티브 경로 (Docker 없음)

```bash
# ── Sail 모델 ───────────────────────────────────────────────────
eval $(opam env)
cd ~/pccx-ws/pccx-FPGA-NPU-LLM-kv260/formal/sail
make check                           # 타입체크; < 5 초

# ── pccx-core + CLI ────────────────────────────────────────────
cd ~/pccx-ws/pccx-lab
cargo build -p pccx-reports --bin pccx_cli --release
./target/release/pccx_cli \
    samples/gemma3n_16tok_smoke.pccx \
    --roofline --report-md          # 헤더 + roofline + bottleneck

# ── pccx-lab (Tauri 데스크톱 앱) ────────────────────────────────
cd ui
npm ci && npm run tauri dev
```

``samples/`` 디렉토리는 두 개의 사전 캡처 트레이스를 제공합니다 —
[`samples/README.md`](https://github.com/pccxai/pccx-lab/blob/main/samples/README.md) 참고:

- ``gemma3n_16tok_smoke.pccx``   (101 KB, 2,568 events)  — CI smoke.
- ``gemma3n_128tok_decode.pccx`` (797 KB, 20,488 events) — steady-state decode.

## 5. 보드 경로 (선택)

```bash
# 비트스트림 플래시 후 KV260 에서 16-토큰 디코드.
cd ~/pccx-ws/pccx-FPGA-NPU-LLM-kv260/scripts/board
./bringup.sh kv260.local
# .pccx를 호스트로 자동 가져오며, pccx-lab 에서 열기.
```

## 6. 다음 단계

- 프로파일러 API surface 는 [pccx-lab 핸드북](Lab/index).
- Sail 스캐폴드는 [형식 모델(Formal Model) 페이지](v002/Formal/index).
- 실측 tok/s + 지연 수치는 [Evidence 페이지](Evidence/index) (보드
  실행 및 측정 진행 중).

## 이 페이지 인용

```bibtex
@misc{pccx_quickstart_2026,
  title        = {pccx Quickstart: one-command reproducer for the open NPU},
  author       = {Kim, Hyunwoo},
  year         = {2026},
  howpublished = {\url{https://pccx.ai/ko/docs/quickstart.html}},
  note         = {Part of pccx: \url{https://pccx.ai/}}
}
```
