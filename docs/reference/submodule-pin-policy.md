---
orphan: true
---

# Submodule pin policy

Application repositories pin the IP-core package by SHA. The pin
points at a commit that must be reachable from the IP-core
repository's `main` branch. Anything else breaks fresh clones.

## The rule

`pccx-FPGA-NPU-LLM-kv260` (and any future board / application
integration repo) maintains a `third_party/pccx-v00N` submodule. The
pin SHA recorded in the submodule and in the consumer's
`COMPATIBILITY.yaml` must be reachable from `pccx-v00N/main`.

## Rebase-merge SHA-rewrite hazard

When the IP-core package PR is merged with **rebase and merge** on
GitHub, the SHAs that GitHub publishes on `main` are *new* — they are
the result of replaying the PR commits onto `main`'s tip. The
original SHAs that lived on the PR head branch are no longer
reachable from `main`.

If the consumer's submodule pin still points at the original
PR-head SHAs after the IP-core PR is merged, **fresh clones of the
consumer with `--recurse-submodules` will fail with
`fatal: remote did not send all necessary objects`**, because the
pin SHA is unreachable from the IP-core repo's published refs.

## Repair procedure (post-rebase-merge)

When the IP-core repo is freshly rebase-merged on `main`:

1. Capture the new IP-core `main` HEAD:
   ```
   PIN=$(gh api repos/pccxai/pccx-v00N/branches/main --jq .commit.sha)
   ```
2. In the consumer repo's PR branch, update the submodule pin:
   ```
   cd third_party/pccx-v00N
   git fetch origin main
   git checkout "$PIN"
   cd ../..
   git add third_party/pccx-v00N
   ```
3. Update the live text references that record the same SHA:
   - `COMPATIBILITY.yaml` field `commit:`.
   - `third_party/PINS.md` pinned-SHA column.
   - any `MIGRATION.md` / `docs/*` line that quotes the live pin
     (historical narrative SHAs are left alone).
4. Commit the pin update and the documentation update together:
   ```
   git commit -m "chore: pin pccx-v00N submodule to merged main"
   ```
5. Verify reachability with the [fresh-clone check](testing-protocol.md):
   ```
   git merge-base --is-ancestor "$PIN" origin/main   # exit=0
   ```

## Why this is documented

The May 2026 v002 extraction batch (PR1 in `pccx-v002`, PR4 in
`pccx-FPGA-NPU-LLM-kv260`) hit this hazard directly. PR1 was
rebase-merged into `pccx-v002/main`, which produced new SHAs on
`main`. PR4's submodule pin still pointed at the original PR1-head
SHA chain. The fix was the procedure above: pin to the new `main`
HEAD, update `COMPATIBILITY.yaml` and `PINS.md`, verify with a fresh
clone. This page exists so the next consumer PR does not relearn the
lesson.
