---
orphan: true
---

# Testing protocol

Verification은 IP-core 저장소와 board integration 저장소로 분리한다.
각 레이어는 서로가 읽을 수 있는 evidence를 남긴다.

## Sail typecheck (`pccx-v002`)

- **위치**: `pccxai/pccx-v002/.github/workflows/sail-typecheck.yml`, `typecheck` job
- **역할**: `LLM/formal/sail/` 아래 formal ISA model을 `sail 0.20.1`과 `ocaml 5.1.0`으로
  타입 체크
- **trigger**: `LLM/formal/sail/**` 또는 워크플로 자체 변경 시 push / pull_request
- **evidence**: `pccxai/pccx-v002` Actions run URL(녹색 run)
- **책임 레이어**: ISA는 IP-core의 계약으로서 Sail는 IP-core 레이어가 담당한다.

## KV260 simulation wrapper (`pccx-FPGA-NPU-LLM-kv260`)

- **위치**: `scripts/v002/use_submodule_sources.sh`
- **역할**: pinned submodule (`third_party/pccx-v002/LLM/sim/`) 기반 시뮬레이션 실행
  및 결과를 `build/sim_v002_submodule.log`에 기록
- **호환성**: wrapper는 원래 러너 인자를 그대로 전달(`--quick`, `--tb <name>` 등)
- **evidence**: `PASS: ...` 요약과 testbench별 PASS 라인
- **책임 레이어**: wrapper는 board integration에서 운영되며, 소비 레이어를 실행 가능한
  형태로 연결하는 지점이다.

## fresh-clone 검증

- **위치**: `/tmp` 또는 CI runner의 깔끔한 checkout
- **역할**: HTTPS clone + `--recurse-submodules`로 보드 통합 저장소를 가져온 뒤
  `pccx-v002/main`에서 pin SHA 도달성을 확인
  ```bash
  git clone --recurse-submodules \
      https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260.git
  cd pccx-FPGA-NPU-LLM-kv260/third_party/pccx-v002
  git fetch origin main
  PIN=$(git rev-parse HEAD)
  git merge-base --is-ancestor "$PIN" origin/main
  echo "exit=$?"
  ```
  `exit=0`이면 도달 가능, `exit=1`이면 pin 재조정이 필요하다.
- **책임 레이어**: 이 검증은 클론 경로의 재현성을 확인하므로 로컬 캐시가 아닌
  외부 재실행 환경에서 판단한다.

## 레이어별 evidence

| Layer | evidence artefact | 저장 위치 |
| --- | --- | --- |
| IP-core (`pccx-v002`) | Sail typecheck run | `pccxai/pccx-v002` GitHub Actions |
| Board integration (`pccx-FPGA-NPU-LLM-kv260`) | Sim wrapper PASS 요약, per-testbench PASS | `build/sim_v002_submodule.log`, `third_party/pccx-v002/LLM/sim/work/<tb>/` |
| Cross-repo(fresh clone) | reachability exit code | ad-hoc clone 경로(재현 가능) |
