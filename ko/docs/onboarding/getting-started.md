---
orphan: true
---

# 시작 가이드

클린 환경에서 재현 가능한 확인 경로를 가장 짧게 정리한 문서다.

## 하위 모듈과 함께 clone

```
git clone --recurse-submodules \
    https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260.git
cd pccx-FPGA-NPU-LLM-kv260
```

`--recurse-submodules`는 필수다. board 통합 저장소는 `third_party/pccx-v002`
submodule을 통해 v002 패키지를 사용하므로 누락 시 빌드가 불완전하다.
빠진 경우 다음으로 복구한다.

```
git submodule update --init --recursive
```

## 도구 기대치

| 도구 | 용도 | 비고 |
| --- | --- | --- |
| `git` | 저장소/서브모듈 관리 | 로컬 |
| `bash` | wrapper 스크립트 | 로컬 |
| `gh` (GitHub CLI) | PR/Actions 조회 | 로컬 |
| Vivado xsim (`xvlog`, `xelab`, `xsim`) | KV260 sim wrapper | 로컬 PATH |
| `opam` + `sail 0.20.1` + `ocaml 5.1.0` + `z3` | Sail typecheck | CI 기준 |
| `python3` | 보조 스크립트 | 로컬 |

`pccx-FPGA-NPU-LLM-kv260`는 `PCCX_LAB_DIR` 혹은 `pccx-lab` 동기화가
없어도 wrapper 실행은 가능하나, trace 시각화는 별도 작업이 필요하다.

## v002 시뮬레이션 실행

```
bash scripts/v002/use_submodule_sources.sh
tail -n 5 build/sim_v002_submodule.log
```

래퍼는 하위 런너 인자를 그대로 전달한다.

```
bash scripts/v002/use_submodule_sources.sh --quick
bash scripts/v002/use_submodule_sources.sh --tb tb_v002_runtime_smoke_program
```

성공 시 `PASS: submodule simulation complete` 로그와 각 테스트벤치의
`Summary: <N> passed, 0 failed` 를 확인할 수 있다.

## Sail typecheck(옵션)

`pccx-v002`에서

```
cd third_party/pccx-v002/LLM/formal/sail
make check
```

를 실행하려면 `sail`, `z3`, `opam`이 필요하다. CI가 기본 환경을 제공하므로
로컬은 반복 실험 위주로 사용한다.

## submodule pin 검증

```
cd third_party/pccx-v002
git fetch origin main
PIN=$(git rev-parse HEAD)
git merge-base --is-ancestor "$PIN" origin/main
echo "exit=$?"
```

`exit=0`이면 도달 가능하며 정상이다. `exit=1`이면 pin 갱신이 필요하다.
