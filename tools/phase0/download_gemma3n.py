#!/usr/bin/env python3
"""Pull Gemma 3N E4B weights from HuggingFace into a local cache.

Gated repo: accept the license on
https://huggingface.co/google/gemma-3n-E4B-it first, then make sure a
token with read permission is available via either ``HF_TOKEN`` or
``huggingface-cli login``.

Phase 0 of the pccx roadmap — see ``tools/phase0/README.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

try:
    from huggingface_hub import snapshot_download
    from huggingface_hub.utils import GatedRepoError, HfHubHTTPError
except ImportError as exc:  # pragma: no cover - clear install hint
    sys.stderr.write("huggingface_hub is required: pip install huggingface_hub\n")
    raise SystemExit(1) from exc

DEFAULT_REPO = "google/gemma-3n-E4B-it"

# Files we actually need for inference + quantize_and_save. Strip out the
# original PyTorch .bin shards so we don't burn bandwidth on duplicates.
DEFAULT_ALLOW_PATTERNS = [
    "*.safetensors",
    "*.safetensors.index.json",
    "config.json",
    "generation_config.json",
    "tokenizer.*",
    "special_tokens_map.json",
    "preprocessor_config.json",
    "processor_config.json",
    "chat_template.*",
]


def sha256_of(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument(
        "--dest",
        type=Path,
        default=Path("data/weights/gemma-3n-E4B-it"),
        help="Local snapshot directory (created if missing).",
    )
    ap.add_argument(
        "--revision",
        default="main",
        help="Branch or commit SHA to pin. Use a commit SHA once you are "
        "sure of the exact weights you want to reproduce.",
    )
    ap.add_argument(
        "--show-hashes",
        action="store_true",
        help="After download, print SHA-256 of every .safetensors file.",
    )
    args = ap.parse_args()

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")

    args.dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        local_path = snapshot_download(
            repo_id=args.repo,
            revision=args.revision,
            local_dir=args.dest,
            allow_patterns=DEFAULT_ALLOW_PATTERNS,
            token=token,
        )
    except GatedRepoError:
        sys.stderr.write(
            f"\n{args.repo} is gated.\n"
            "  1. Open https://huggingface.co/{repo} and accept the license.\n"
            "  2. export HF_TOKEN=<your read token>  (or huggingface-cli login)\n"
            "  3. Re-run this script.\n".format(repo=args.repo)
        )
        return 2
    except HfHubHTTPError as exc:
        sys.stderr.write(f"download failed: {exc}\n")
        return 3

    print(f"snapshot at {local_path}")

    if args.show_hashes:
        for shard in sorted(Path(local_path).glob("*.safetensors")):
            digest = sha256_of(shard)
            print(f"  {digest}  {shard.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
