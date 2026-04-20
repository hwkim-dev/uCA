#!/usr/bin/env python3
"""Prepare a mixed Korean + English ShareGPT slice for EAGLE-3 training.

Output: parquet with columns `id`, `conversations` (list of {role, content}),
`language` (`ko` | `en` | `mixed`), `turn_count`, `char_count`.

The sampling is deterministic (fixed seed) so reruns are reproducible.

Phase 0 of the pccx roadmap — see ``tools/phase0/README.md``. This script
runs offline on a laptop; training itself happens later on rented GPU.
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    from datasets import load_dataset
except ImportError as exc:  # pragma: no cover - clear install hint
    sys.stderr.write(
        "datasets is required: pip install 'datasets[parquet]' pyarrow\n"
    )
    raise SystemExit(1) from exc

DATASET_NAME = "anon8231489123/ShareGPT_Vicuna_unfiltered"
DATASET_SPLIT = "train"
DATASET_FILES = "ShareGPT_V3_unfiltered_cleaned_split.json"

HANGUL_RE = re.compile(r"[\uAC00-\uD7A3]")
LATIN_RE = re.compile(r"[A-Za-z]")


def classify_language(text: str) -> str:
    has_ko = bool(HANGUL_RE.search(text))
    has_en = bool(LATIN_RE.search(text))
    if has_ko and has_en:
        return "mixed"
    if has_ko:
        return "ko"
    if has_en:
        return "en"
    return "other"


def normalize_conversation(raw: list[dict]) -> list[dict] | None:
    """Collapse the raw ShareGPT turn format into {role, content}.

    Returns None if the conversation is malformed or empty.
    """
    out: list[dict] = []
    for turn in raw:
        role = turn.get("from") or turn.get("role")
        content = turn.get("value") or turn.get("content")
        if not role or not content:
            return None
        role = {"human": "user", "gpt": "assistant", "system": "system"}.get(
            role, role
        )
        out.append({"role": role, "content": content.strip()})
    return out or None


def iter_records(
    ko_quota: int, en_quota: int, mixed_quota: int
) -> Iterable[dict]:
    ds = load_dataset(
        DATASET_NAME,
        data_files=DATASET_FILES,
        split=DATASET_SPLIT,
        streaming=True,
    )

    buckets = {"ko": [], "en": [], "mixed": []}
    quotas = {"ko": ko_quota, "en": en_quota, "mixed": mixed_quota}

    for row in ds:
        conv = normalize_conversation(row.get("conversations") or [])
        if conv is None:
            continue
        joined = "\n".join(t["content"] for t in conv)
        if len(joined) < 128:  # skip near-empty chats
            continue

        lang = classify_language(joined)
        if lang not in buckets or len(buckets[lang]) >= quotas[lang]:
            if all(len(buckets[k]) >= quotas[k] for k in buckets):
                break
            continue

        buckets[lang].append(
            {
                "id": row.get("id") or f"{lang}-{len(buckets[lang])}",
                "conversations": conv,
                "language": lang,
                "turn_count": len(conv),
                "char_count": len(joined),
            }
        )

    for lang in buckets:
        yield from buckets[lang]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target-size", type=int, default=50_000)
    ap.add_argument("--ko-ratio", type=float, default=0.40)
    ap.add_argument("--mixed-ratio", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("data/sharegpt_ko_en.parquet"),
    )
    args = ap.parse_args()

    ko_quota = int(args.target_size * args.ko_ratio)
    mixed_quota = int(args.target_size * args.mixed_ratio)
    en_quota = args.target_size - ko_quota - mixed_quota

    random.seed(args.seed)
    records = list(iter_records(ko_quota, en_quota, mixed_quota))
    random.shuffle(records)

    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as exc:  # pragma: no cover
        sys.stderr.write("pyarrow is required: pip install pyarrow\n")
        raise SystemExit(1) from exc

    args.out.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(records)
    pq.write_table(table, args.out, compression="zstd")

    by_lang: dict[str, int] = {}
    for r in records:
        by_lang[r["language"]] = by_lang.get(r["language"], 0) + 1
    print(f"wrote {len(records):,} rows -> {args.out}")
    for lang, count in sorted(by_lang.items()):
        print(f"  {lang:<6s} {count:>6,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
