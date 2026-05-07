---
orphan: true
---

> Draft operational policy; not legal advice; not a contract.
> Subject to qualified legal review before any binding use.

# Copyright header policy

Source files in PCCX repositories carry a short header asserting
the copyright holder and the SPDX licence. The header form below is
deliberately ASCII so it does not break HDL / Verilog / Vivado /
toolchain parsers that treat unusual Unicode characters as errors.

## Header form (source code, comment-style)

| Language family | Comment syntax | Header |
| --- | --- | --- |
| SystemVerilog / Verilog / C / C++ / Rust / Go / Java / JS / TS | `//` line | `// PCCX(TM) — reusable AI accelerator project.` … |
| Python / Shell / TOML / YAML / Make | `#` line | `# PCCX(TM) — reusable AI accelerator project.` … |
| HTML / XML / SVG / CSS | block comment | `<!-- PCCX™ — reusable AI accelerator project. ... -->` |

Three lines per header:

```
PCCX(TM) — reusable AI accelerator project.
SPDX-FileCopyrightText: 2026 Hyun Woo Kim
SPDX-License-Identifier: Apache-2.0
```

The first line uses ASCII `(TM)` in source comments to keep the
mark visible to SPDX parsers and HDL toolchains that may normalise
or reject Unicode. Documentation prose, README files, website pages,
and HTML/CSS comment blocks may use the Unicode `PCCX™` form
because those contexts are Unicode-safe.

## Placement rules

- Preserve `#!` shebangs as line 1.
- Preserve `<?xml ... ?>` declarations as line 1.
- Preserve `<!DOCTYPE>` as line 1.
- Preserve Python encoding cookies on line 2 if present.
- Preserve YAML frontmatter as the first block; insert header after.
- Preserve any tool-required pragma that must be on line 1; insert
  after.
- Skip files that already carry an `SPDX-License-Identifier`.
- Skip generated, vendored, third-party, submodule, lock, minified,
  and binary files.

## Application script

Headers are applied by a deterministic script that is reviewed by
the project before each rollout. The script writes a JSON report
listing every file changed, every file skipped, and the skip reason.
The script is not committed to the repository; it lives under the
project's tooling directory or a local `/tmp` workspace and is
re-runnable from the report.

## Not legal advice

Adding an SPDX header does not change the underlying licence; the
licence text in the repository's `LICENSE` file is authoritative.
