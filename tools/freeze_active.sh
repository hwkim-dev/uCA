#!/usr/bin/env bash
#
# freeze_active.sh — snapshot the currently-active RTL at a tag into
# pccx/codes/vNNN/ as the permanent archive for that architecture version.
#
# Usage
# -----
#   freeze_active.sh <tag> <target-version>
#
#   <tag>             a tag (or branch) in the external RTL repo
#                     hwkim-dev/pccx-FPGA-NPU-LLM-kv260 from which the
#                     snapshot is taken. Example: v2.0.0 .
#   <target-version>  vNNN triple — the pccx archive slot to populate.
#                     Example: v002 .
#
# Example
# -------
#   # Freeze the tagged v2.0.0 release as pccx/codes/v002/
#   $ tools/freeze_active.sh v2.0.0 v002
#
# Why
# ---
# Each pccx architecture version is authored live in the external repo
# hwkim-dev/pccx-FPGA-NPU-LLM-kv260. When development moves on to the
# next version, the previous version has to be frozen somewhere stable
# so the archived docs (e.g. docs/archive/experimental_v00N/) keep
# resolving their literalinclude paths years from now. That stable
# home is pccx/codes/vNNN/, committed into this repo.
#
# This script performs the mechanical half of that cutover:
#
#   1. Clone the external repo at the given tag, shallow.
#   2. Strip .git / .github so only source is preserved.
#   3. Copy the tree under codes/<target-version>/.
#   4. Stage the directory for review.
#
# The reviewer/committer is responsible for:
#
#   * Confirming the file set via `git diff --cached --stat codes/...`.
#   * Bumping `ACTIVE_VERSION` in .github/workflows/deploy.yml to the
#     next vNNN slot (the slot that will be CI-cloned from main going
#     forward).
#   * Updating the root toctrees (index.rst, ko/index.rst) to add the
#     new active version alongside the freshly-archived one.
#   * Writing the commit message. Suggested format:
#         chore(archive): freeze v002 RTL at tag v2.0.0
#
# The full cutover ceremony — including docs scaffolding and
# sphinx-multiversion whitelist updates — is documented in
# CLAUDE.md §8.4.

set -euo pipefail

RTL_REPO_URL="${RTL_REPO_URL:-https://github.com/hwkim-dev/pccx-FPGA-NPU-LLM-kv260}"

usage() {
    cat >&2 <<EOF
usage: $(basename "$0") <tag> <target-version>

  <tag>            tag/branch in pccx-FPGA-NPU-LLM-kv260 to clone
  <target-version> e.g. v002, v003

examples:
  $(basename "$0") v2.0.0 v002
  $(basename "$0") main    v002   # discouraged — prefer a signed tag

env overrides:
  RTL_REPO_URL     override the upstream RTL repo (default: \$RTL_REPO_URL)
EOF
    exit 2
}

[ $# -eq 2 ] || usage
tag="$1"
target_version="$2"

if ! [[ "$target_version" =~ ^v[0-9]{3}$ ]]; then
    echo "error: target-version must match 'vNNN' (three digits)." >&2
    echo "       got: $target_version" >&2
    exit 1
fi

# Locate the pccx repo root.
if ! repo_root=$(git rev-parse --show-toplevel 2>/dev/null); then
    echo "error: must be run from inside the pccx git repo." >&2
    exit 1
fi
codes_dir="$repo_root/codes/$target_version"

# Guard: do not clobber an already-populated slot.
if [ -d "$codes_dir" ] && [ -n "$(ls -A "$codes_dir" 2>/dev/null)" ]; then
    echo "error: $codes_dir already exists and is not empty." >&2
    echo "       remove it manually if you really intend to re-freeze." >&2
    exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

echo "== cloning $RTL_REPO_URL @ $tag (shallow) =="
git clone --depth 1 --branch "$tag" "$RTL_REPO_URL" "$tmp/rtl"

echo ""
echo "== stripping VCS / CI metadata =="
rm -rf "$tmp/rtl/.git" "$tmp/rtl/.github"

echo ""
echo "== copying tree into $codes_dir =="
mkdir -p "$codes_dir"
cp -a "$tmp/rtl/." "$codes_dir/"

echo ""
echo "== staging =="
git -C "$repo_root" add "codes/$target_version"

cat <<EOF

== done ==

Staged codes/$target_version/ from tag $tag.

Review:
    git -C "$repo_root" diff --cached --stat codes/$target_version | head -40

Then continue the cutover ceremony (CLAUDE.md §8.4):

  1. Commit:
         chore(archive): freeze $target_version RTL from tag $tag
  2. Bump ACTIVE_VERSION in .github/workflows/deploy.yml to the next
     vNNN slot so the CI step \`Clone active vNNN RTL\` targets the
     new live repo state.
  3. Scaffold docs/v(N+1)/ and ko/docs/v(N+1)/ and update root
     index.rst toctrees.
  4. Update conf_common.py smv_branch_whitelist if you are starting a
     v(N+1)-dev branch.
EOF
