---
orphan: true
---

# Submodule pin policy

Application 저장소는 IP-core 패키지를 SHA 단위로 pin 한다.
pin은 해당 IP-core 저장소의 `main`에서 도달 가능한 SHA여야 한다.
이 규칙을 어기면 새로 `--recurse-submodules`를 하는 환경에서 clone이 깨진다.

## 기본 규칙

`pccx-FPGA-NPU-LLM-kv260`를 포함한 앞으로의 board/application 통합 저장소는
`third_party/pccx-v00N`에 submodule을 둔다.
submodule과 consumer의 `COMPATIBILITY.yaml`에 기록된 pin SHA는 모두
`pccx-v00N/main`에서 도달 가능한 값이어야 한다.

## Rebase-merge SHA 재작성 위험

IP-core PR이 GitHub에서 **rebase and merge**되면, `main`에 반영되는 SHA는
원 PR head SHA와 달라진다. PR head SHA는 `main`에서 더 이상 도달 불가 상태가
될 수 있다.

병합 후에도 consumer pin이 PR head SHA를 그대로 가리키면,
`--recurse-submodules`를 수행한 신규 clone에서 다음 오류가 발생한다.

`fatal: remote did not send all necessary objects`

이 오류는 pin SHA가 `main`에서 도달 불가하기 때문이다.

## 재현 절차( rebase-merge 후 )

IP-core가 rebase-merge로 갱신된 뒤 다음 절차를 순서대로 수행한다.

1. 최신 `pccx-v00N/main` HEAD를 수집한다.
   ```bash
   PIN=$(gh api repos/pccxai/pccx-v00N/branches/main --jq .commit.sha)
   ```
2. 소비자 저장소 PR 브랜치에서 submodule pin을 새 HEAD로 이동한다.
   ```bash
   cd third_party/pccx-v00N
   git fetch origin main
   git checkout "$PIN"
   cd ../..
   git add third_party/pccx-v00N
   ```
3. 같은 SHA를 기록하는 문서를 함께 갱신한다.
   - `COMPATIBILITY.yaml`의 `commit:`
   - `third_party/PINS.md`의 pinned-SHA 컬럼
   - 역사 기록을 남기는 `MIGRATION.md`, `docs/*` 내 텍스트도 필요 시 갱신
4. pin 갱신과 문서 갱신을 함께 커밋한다.
   ```bash
   git commit -m "chore: pin pccx-v00N submodule to merged main"
   ```
5. 도달성 체크로 확인한다.
   ```bash
   git merge-base --is-ancestor "$PIN" origin/main   # exit=0
   ```

## 기록이 남는 이유

2026년 5월 v002 extraction 배치에서는 이 문제가 실제로 발생했다.
`pccx-v002` PR1이 rebase-merge되면 main에서 새 SHA가 생성되었고,
`pccx-FPGA-NPU-LLM-kv260` PR4가 기존 head SHA를 가리키던 상태였다.
위 절차대로 `main` HEAD pin 갱신, `COMPATIBILITY.yaml`, `PINS.md` 갱신을
거쳐 동일한 문제가 재발하지 않게 정리됐다.
