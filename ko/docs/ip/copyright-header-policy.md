---
orphan: true
---

> 초안 운영 문서입니다. 법률 자문이 아니며 계약서가 아니다.
> 적용 전에는 자격 있는 법무 검토 필요.

# Copyright header policy

PCCX 저장소의 소스 파일에는 저작권 소유자와 SPDX 라이선스를 명시하는 짧은
헤더가 들어가야 한다. 예시는 도구가 Unicode를 깨뜨릴 수 있어 ASCII 중심으로
작성한다.

## 헤더 형식 (소스 코드, 주석 형태)

| 언어군 | 주석 스타일 | 예시 |
| --- | --- | --- |
| SystemVerilog / Verilog / C / C++ / Rust / Go / Java / JS / TS | `//` 행 | `// PCCX(TM) — reusable AI accelerator project.` ... |
| Python / Shell / TOML / YAML / Make | `#` 행 | `# PCCX(TM) — reusable AI accelerator project.` ... |
| HTML / XML / SVG / CSS | 블록 주석 | `<!-- PCCX™ — reusable AI accelerator project. ... -->` |

3줄 구성:

```
PCCX(TM) — reusable AI accelerator project.
SPDX-FileCopyrightText: 2026 Hyun Woo Kim
SPDX-License-Identifier: Apache-2.0
```

첫 줄은 ASCII ` (TM)`을 쓰는 쪽이 tooling 호환성이 높다.

## 삽입 규칙

- `#!` 셰뱅은 1행 유지.
- `<?xml ... ?>`, `<!DOCTYPE>`는 1행 유지.
- 파이썬 인코딩 쿠키가 있으면 2행 유지.
- YAML frontmatter는 최상단 유지 후에 헤더 삽입.
- 특수 pragma는 1행 요구 위치를 우선.
- `SPDX-License-Identifier`가 이미 있으면 건너뜀.
- generated, vendored, third-party, submodule, lock, minified, binary는 제외.

## 적용 프로세스

헤더는 반복 가능한 스크립트로 반영된다. 실행 기록은 JSON 리포트로 남기고
필요 시 공개되지 않은 툴링 영역에서 재실행한다.

## 비고

헤더 삽입만으로 라이선스의 실질이 바뀌지 않는다. 라이선스 본문은 저장소의
`LICENSE`가 최종이다.
