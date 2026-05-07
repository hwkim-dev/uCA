---
myst:
  html_meta:
    description lang=en: |
      Reader quickstart for the pccx v002.1 path: resolve the spec,
      inventory public evidence, run the local docs checks, understand
      deployment, and answer common review questions without treating
      targets as measured results.
---

# Quickstart

This page is the shortest reader path through the active pccx line.
It is not a benchmark recipe. Use it to decide what is specified, what
is evidenced, what remains pending, and which commands keep a docs
change honest.

## 1. Read the spec resolution

Start by separating release-line intent from measured evidence:

- {doc}`v002/overview` defines the active architecture line. v002.0 is
  the baseline KV260 integration line; v002.1 layers sparsity and
  speculative decoding on top of that baseline.
- {doc}`roadmap` is the release-line map. It records the v002.1
  throughput figure as a target, not as an achieved result.
- {doc}`v002/Models/gemma3n_overview` and
  {doc}`v002/Models/gemma3n_pipeline` describe the Gemma 3N E4B model
  path that v002.1 is meant to exercise.
- {doc}`v002/ISA/index` and {doc}`v002/Formal/index` explain the ISA
  contract and the Sail model. Encoding details still resolve back to
  the active RTL package when documentation and implementation differ.

Reader rule: a claim about a planned v002.1 mechanism can live in the
architecture or model docs; a claim that it has run on KV260 belongs on
the evidence page only after the release checklist gates it in.

## 2. Inventory the evidence

Read {doc}`Evidence/index` before interpreting any performance wording.
That page is the public inventory of measured, reproducible artefacts
and pending gates.

Use this checklist while reading:

| Question | Where to check |
|---|---|
| Is the value measured, pending, or a target? | {doc}`Evidence/index` and {doc}`roadmap` |
| Which testbench or tool produced it? | {doc}`v002/Verification/index` and {doc}`Lab/verification-workflow` |
| Does it depend on Vivado synth, implementation, or board bring-up? | {doc}`v002/Build/index` |
| Is it a model-mapping claim rather than hardware evidence? | {doc}`v002/Models/gemma3n_execution` |

If a number is not present in {doc}`Evidence/index`, treat it as design
intent or release planning text. Do not quote it as a measured result.

## 3. Run the local docs runbook

For docs-only review, clone this repository and run the strict build:

```bash
git clone https://github.com/pccxai/pccx.git
cd pccx
make strict
make lint
```

`make strict` builds the English and Korean Sphinx sites with warnings
as errors. `make lint` runs the lightweight prose and Sphinx lint pass.
For longer-lived branches, run `make linkcheck` before release or when
adding external URLs.

For trace and lab workflow reproduction, use the existing pccx-lab
handbook instead of this page:

- {doc}`Lab/quickstart` for opening sample `.pccx` traces.
- {doc}`Lab/verification-workflow` for the xsim-to-trace verification
  path.
- {doc}`Lab/cli` for headless trace inspection and golden-diff gates.

## 4. Read the deploy runbook

The public site is generated from this docs repository and deployed by
GitHub Actions after changes land on `main`.

Operationally, a docs PR should keep this order:

1. Build locally with `make strict`.
2. Run `make lint`; run `make linkcheck` when URLs changed.
3. Merge only evidence wording that has a named source artefact or a
   pending gate.
4. Let the Pages workflow publish `https://pccxai.github.io/pccx/`.
5. Check the deployed page for the exact path you changed.

Deployment does not convert a target into evidence. The deploy check
only proves the site built and published; the evidence page still owns
measurement status.

## 5. FAQ

### Is v002.1 already released?

No. v002.1 is the planned sparsity and speculative-decoding ramp on the
same KV260 RTL line. The baseline v002.0 integration and evidence gates
remain visible dependencies.

### Does the 20 tok/s figure mean measured throughput?

No. It is a v002.1 target. The docs may discuss it as a target, but it
must not be phrased as achieved throughput until KV260 evidence lands in
{doc}`Evidence/index`.

### Which repository is the source of truth for RTL?

The active v002 RTL lives in
`pccxai/pccx-FPGA-NPU-LLM-kv260`. This docs repository cross-references
that source and builds a public narrative around it. For ISA encodings,
the RTL `isa_pkg.sv` package wins over prose.

### Should a reader start with the lab app?

Start with this page if you are reviewing claims. Start with
{doc}`Lab/quickstart` if you want to open traces or inspect the pccx-lab
UI.

### Do English and Korean docs both need manual edits?

No for new work. English is the canonical source; the Korean tree is
produced by external translation tooling and may trail the English
source.

### What makes a quickstart or release note misleading?

The common failure mode is mixing target, simulator, synthesis, and
board evidence in one sentence. Keep each claim tied to its source:
roadmap for targets, architecture/model pages for design intent,
verification pages for testbench status, and {doc}`Evidence/index` for
published measurement status.

## Cite this page

```bibtex
@misc{pccx_reader_quickstart_2026,
  title        = {pccx Quickstart: reader path for the v002.1 release line},
  author       = {Kim, Hyunwoo},
  year         = {2026},
  howpublished = {\url{https://pccxai.github.io/pccx/en/docs/quickstart.html}},
  note         = {Part of pccx: \url{https://pccxai.github.io/pccx/}}
}
```
