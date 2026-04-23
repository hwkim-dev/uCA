# Phase 0 — Kickoff Checklist

Source: `docs/roadmap.md` §5 (Compute) + plan drafts (gitignored local).

Phase 0 is the **pre-implementation window** before Week 1. Almost every
item needs the user's hands (browser login, credit card, HF gated repo
access). This directory hosts the helper scripts for the pieces that
can run from a local shell.

## Owner legend

| Symbol | Meaning |
|---|---|
| USER | User-only (browser / credentials / local hardware) |
| AUTO | Automatable (Claude / script) |
| LINK | User-gated, but Claude can write the helper |

## Checklist

### Compute & accounts

- [ ] USER **TRC TPU application** — submit at <https://sites.research.google/trc/>.
  - Approval window: 1–2 weeks.
  - If granted, v003 EAGLE-3 training (Phase 2, Week 27–34) runs free.
  - If denied, fall back to Vast.ai (~$30–50).
- [ ] USER **Vast.ai or RunPod account** — minimum $10 deposit.
  - Only needed starting v002 Phase H+ (Week 33), so can defer.
  - Card on file so we can burst-rent an RTX 4090 for 30–50 hours.

### Data & weights

- [ ] LINK **Gemma 3N E4B weights** — gated repo on HuggingFace.
  - User must accept the license on <https://huggingface.co/google/gemma-3n-E4B-it>.
  - After that: `python tools/phase0/download_gemma3n.py` pulls the safetensors.
- [ ] LINK **ShareGPT 50K (ko + en)** — streamed from HF dataset.
  - `python tools/phase0/prepare_sharegpt.py --target-size 50000 --out data/sharegpt_ko_en.parquet`
  - Needed for v002 Phase H+ EAGLE-3 head training.

### Local hardware

- [ ] USER **KV260 dev environment** — confirm Vivado 2023.2 + Vitis + board detected.
  - `xsct`, `vivado`, `petalinux-config` reachable in `$PATH`.
  - Board visible via `lsusb` / JTAG probe.
- [ ] USER **KV260 bootable SD card** — PetaLinux or AMD Ubuntu 22.04 image.
  - Target bitstream load path confirmed (`/lib/firmware/xilinx/…`).

## Kickoff sequence

1. Submit TRC application **today** (§ Compute). Approval is the
   long pole.
2. Accept the Gemma 3N license while the TRC application is
   pending — this unblocks `download_gemma3n.py`.
3. Run `download_gemma3n.py` + `prepare_sharegpt.py`. Verify the output
   parquet has ~50K rows and the weight safetensors checksum.
4. Meanwhile confirm KV260 tooling locally.
5. Vast.ai deposit can wait until Week ~30 (Phase H+ approaching).

Once items 1–4 are checked, Phase 0 is done — proceed to Phase A
re-parameterization. Track those in a new `tools/phaseA/` directory.

## Related

- Full roadmap: [`docs/roadmap.md`](../../docs/roadmap.md)
- Plan drafts (local-only, gitignored):
  - `pccx_master_roadmap_final.md`
  - `pccx_v002_extended_20toks_plan.md`
  - `tinynpu_v003_gemma4_e4b_plan.md`
