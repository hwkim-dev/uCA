# CLAUDE.md — pccx Project Guide

_Single source of truth for the **pccx** NPU documentation site._
_Last revised: 2026-04-18 (Furo migration, `feat/sphinx-furo-migration` branch)._

이 문서는 Claude Code(또는 다른 AI 에이전트)와 사람이 **pccx** 레포에서 작업할 때
참고해야 할 모든 규약의 최상위 진실원입니다. 토큰 예산과 가독성을 위해 섹션 제목은
영어로, 설명 본문은 한국어 + 영어 기술 용어 혼용으로 작성되어 있습니다.

---

## 1. Project Context

**pccx (Parallel Compute Core eXecutor)** 는 엣지 FPGA(1차 타겟: Xilinx Kria KV260,
Zynq UltraScale+ ZU5EV) 에서 **Transformer 기반 LLM 의 자기회귀 디코딩**을 가속하기
위한 확장 가능한 NPU 아키텍처입니다.

본 레포는 **문서 사이트** 입니다. **RTL 소스**는 두 곳에 분산되어 있습니다.

| 버전 | 위치 | 상태 |
|---|---|---|
| v001 | `codes/v001/` (repo 내부) | 아카이브. 문서 수정은 원칙적으로 금지 |
| v002 | [`hwkim-dev/pccx-FPGA-NPU-LLM-kv260`](https://github.com/hwkim-dev/pccx-FPGA-NPU-LLM-kv260) | 활성. CI 시점에 `codes/v002/` 로 `git clone` |

- **문서 성격**: hardware reference manual. 튜토리얼이 아니라 사양서에 가까움.
  독자는 systolic array, AXI 프로토콜, Transformer 구조에 친숙하다고 가정.
- **독자층**: 채용 담당자 / 동료 HW 엔지니어 / 논문 보조 자료 참고자.
- **퍼블리시**: `https://hwkim-dev.github.io/pccx/` (`main` push 시 자동 배포).
- **언어**: 영어 (`/en/`) + 한국어 (`/ko/`). **한국어 먼저** (§4.1 참고).
- **버전 축**: 현재 `v002` 활성, `v001` 아카이브, `v003` 은 향후 분기 예정.

### 1.1 설계 목표 (우선순위 순)

1. **Correctness** — 숫자·비트폭·오피코드는 RTL 진실과 1:1 일치해야 함.
2. **Traceability** — 모든 기술적 주장은 RTL 커밋 SHA 로 링크 가능해야 함 (§9).
3. **Legibility at depth** — 다크/라이트 동등, 이중 언어, 다버전, 검색 가능.
4. **Low-friction contribution** — 새 페이지가 zero-warning 으로 빌드되어야 함.

---

## 2. Repository Layout

```
pccx/
│
├── conf_common.py                # 공통 Sphinx 설정 (extensions, MyST, numfig, theme 등)
├── conf.py                       # 영어 conf — conf_common 에서 import, language='en'
├── ko/
│   ├── conf.py                   # 한국어 conf — conf_common 에서 import, language='ko'
│   ├── index.rst                 # 한국어 루트 toctree
│   └── docs/                     # 한국어 원본 트리 (docs/ 와 동형)
│       ├── v002/{Architecture, ISA, Drivers, Models, RTL}
│       ├── Devices/
│       ├── archive/experimental_v001/
│       └── samples/              # Phase 4 데모
│
├── index.rst                     # 영어 루트 toctree
├── docs/                         # 영어 원본 트리
│   ├── index.rst
│   ├── v002/
│   │   ├── overview.rst
│   │   ├── Architecture/        (top_level, rationale, dsp48e2_w4a8,
│   │   │                         gemm_core, gemv_core, sfu_core,
│   │   │                         memory_hierarchy, kv_cache,
│   │   │                         floorplan, index)
│   │   ├── ISA/                 (encoding, instructions, dataflow, index)
│   │   ├── Drivers/             (api, index)
│   │   ├── Models/              (gemma3n_*, index)  — Gemma 3N 타겟 모델
│   │   └── RTL/                 (isa_pkg, npu_top, compute_cores, controller, index)
│   ├── Devices/                 (kv260, index)
│   ├── archive/experimental_v001/
│   └── samples/                 # Phase 4 데모
│
├── plots/                        # sphinx-gallery 소스 (.py) — 양 언어 공유
│   └── plot_*.py
├── auto_plots/                   # sphinx-gallery 영어 출력 (gitignored)
├── ko/auto_plots/                # sphinx-gallery 한국어 출력 (gitignored)
│
├── assets/images/                # 기존 PNG 자산 (33개). 새 도면은 _static/diagrams/ 선호
│   └── Architecture/{v001, v002}/
│
├── _static/                      # 양 언어 공유 (ko conf 는 ../\_static)
│   ├── custom.css                # Furo 테마 오버라이드
│   ├── diagrams/                 # **신규 표준: currentColor 기반 SVG**
│   ├── plots/                    # scienceplots 산출물 (필요 시)
│   ├── vendor/                   # 외부 라이브러리 (WaveDrom render-html 등)
│   ├── language-switcher.{js,css}
│   └── image-lightbox.{js,css}
│
├── _templates/                   # Furo 슬롯 오버라이드
│   └── sidebar/brand.html        # 언어 스위처 삽입 지점
│
├── refs.bib                      # sphinxcontrib-bibtex 참고문헌 (양 언어 공유)
│
├── codes/
│   ├── v001/hw/rtl/              # v001 SystemVerilog (archived)
│   ├── v001/sw/                  # v001 소프트웨어 참조
│   └── v002/                     # ⚠ gitignored. CI 가 외부 repo 에서 clone
│
├── _build/                       # gitignored
├── .venv/                        # gitignored
│
├── requirements.txt              # 런타임 + 빌드 의존성 (Furo 스택)
├── requirements-dev.txt          # 개발 전용 (autobuild, lint, 테스트)
├── Makefile                      # make en | ko | all | linkcheck | clean | dev-en | dev-ko
│
├── .github/workflows/
│   ├── lint.yml                  # sphinx-lint, codespell, strict(-W) build
│   ├── deploy.yml                # EN + KO × multi-version 빌드 → gh-pages
│   └── linkcheck.yml             # weekly cron
│
├── CLAUDE.md                     # 이 파일 (SSOT)
├── README.md                     # 프로젝트 개요 + "CLAUDE.md 참조" 링크
└── LICENSE
```

---

## 3. Toolchain

### 3.1 Core

| 패키지 | 역할 | 비고 |
|---|---|---|
| **Sphinx** `>=7.4,<8` | 빌더 | `-W` strict CI. §10.3 에 핀 이유. |
| **Furo** `>=2024.8` | HTML 테마 | 미니멀, 다크/라이트 네이티브. 포트폴리오 급 외관. |
| **myst-parser** `>=4.0,<5` | MD ↔ RST 파서 | myst-nb 가 transitively 로드 (extensions 목록엔 넣지 않음 §10.3). |
| **myst-nb** `>=1.4,<2` | `.md` / `.ipynb` 파서 | extensions 엔 `myst_nb` 만 나열; myst-parser 기능 자동 포함. |
| **linkify-it-py** `>=2.0` | URL 자동 링크화 | MyST `linkify` 확장이 런타임에 요구. |

### 3.2 UI / UX

| 패키지 | 역할 |
|---|---|
| **sphinx-design** | 그리드, 카드, 탭, 드롭다운, 배지. 레퍼런스 매뉴얼의 시각적 구조화. |
| **sphinx-copybutton** | 코드 블록 복사 버튼. |
| **sphinx-togglebutton** | `.. admonition::` 토글. |
| **sphinx-notfound-page** | 다국어 404. |
| **sphinxext-opengraph** | OG 메타태그 (LinkedIn/Twitter/Slack 링크 카드). |
| **sphinx-sitemap** | `sitemap.xml` 자동 생성. SEO. |
| **sphinx-reredirects** | 페이지 경로 변경 시 구 URL → 새 URL 리다이렉트. |

### 3.3 Diagrams

| 패키지 | 역할 | 선택 기준 |
|---|---|---|
| **sphinxcontrib-mermaid** | `mermaid` 코드 블록 렌더 | 플로우차트·시퀀스·상태머신·간트 |
| **sphinxcontrib-wavedrom** | `wavedrom` 코드 블록 렌더 | RTL 타이밍 다이어그램 |
| **sphinx.ext.graphviz** | `digraph` / `graph` DOT | 계층 구조·모듈 포함 관계 |

### 3.4 Math / Plotting

| 패키지 | 역할 |
|---|---|
| **sphinx.ext.mathjax** | LaTeX 수식 (`$...$`, `$$...$$`, 번호 매김) |
| **matplotlib** + **scienceplots** | 포트폴리오 급 IEEE 스타일 플롯 |
| **matplotlib.sphinxext.plot_directive** | 인라인 `.. plot::` 실행 |
| **sphinx-gallery** | `plots/*.py` → `auto_plots/` 페이지 자동 생성 |

### 3.5 Referencing

| 패키지 | 역할 |
|---|---|
| **sphinxcontrib-bibtex** | `refs.bib` ↔ `{cite}` 시맨틱 인용 |
| **sphinx.ext.intersphinx** | 외부 프로젝트 심볼 링크 (Python, NumPy 등) |
| **sphinx.ext.autosectionlabel** | `{ref}` 섹션 자동 레이블 |
| **sphinx-external-toc** (설치만) | 향후 `_toc.yml` 기반 TOC 로 마이그레이션 여지 |

### 3.6 Versioning

| 패키지 | 역할 | 운영 |
|---|---|---|
| **sphinx-multiversion** | Git tag/branch 별 멀티 빌드 | 언어별로 **두 번 실행** (§7.4). |

### 3.7 Dev

| 패키지 | 역할 |
|---|---|
| **sphinx-autobuild** | 파일 변경 시 라이브 리로드 |
| **sphinx-lint** | RST/MD 선제 린트 (CI) |
| **codespell** | 오탈자 탐지 (CI) |

---

## 4. Authoring Conventions

### 4.1 Language-first policy (ko → en)

- **새 문서·구조 변경은 먼저 `ko/docs/` 에 한국어로** 작성.
- 사용자 검토 후에 `docs/` 에 영어 번역 반영.
- 한쪽만 수정된 상태의 커밋은 **지시를 받지 않은 한 금지**.
- 영어 번역 스타일: 원어민 HW 엔지니어 톤. 숫자·비트폭·오피코드는 1:1. 섹션 번호 체계 유지.

정착된 용어 매핑 (기계 번역 방지):

| 한국어 | 영어 |
|---|---|
| 시스톨릭 어레이 | systolic array |
| 가중치 고정 | Weight Stationary |
| 가중치 스트리밍 | Weight Streaming |
| 부호 복원 | sign recovery |
| 승격 | promotion (BF16/FP32) |
| 직결 FIFO | direct-connect FIFO |
| 분산 배치 | distributed mapping |
| 비트 잉여 공간 | spare bits / bit headroom |
| 피연산자 | operand (never "input data") |

### 4.2 File formats

- **신규**: `.md` (MyST). 축약 문법이 편리하고 GitHub 프리뷰에도 유리.
- **기존**: `.rst` 유지. 형식 변환은 독립된 태스크로 별도 진행.
- 섹션 제목 언더라인 규칙 (RST): 페이지 `===`, 1 차 `---`, 2 차 `~~~`, 3 차 `^^^`.
- MyST 헤딩: `#`, `##`, `###`. `myst_heading_anchors = 3` 이므로 H3 까지 자동 anchor.

### 4.3 Math

- 인라인: `$\lambda$`
- 디스플레이: `$$...$$`
- 번호 매김 & 참조:
  ```markdown
  $$
  \mathrm{GMAC/s} = f_{\mathrm{core}} \times N_{\mathrm{PE}} \times 2
  $$ (eq-gmacs)

  See {eq}`eq-gmacs`.
  ```
- `amsmath` 가 활성화되어 있어 `\begin{aligned}` 등 사용 가능.

### 4.4 Figures & cross-references

- 모든 figure 에는 `:name:` 필수. 이유: `{numref}` 로 번호 참조 (§5).
- MyST 문법:
  ```markdown
  :::{figure} /_static/diagrams/pe_array.svg
  :name: fig-pe-array
  :alt: 32×16 PE 어레이 개요
  :width: 80%

  PE 어레이 상단 블록도. 각 PE 는 DSP48E2 1 기를 공유해 2 MAC/cycle 을 수행한다.
  :::

  본문에서 {numref}`fig-pe-array` 참조.
  ```
- `numfig = True` + `numfig_format` 으로 "Figure 1", "그림 1" 자동 매김.

### 4.5 Cross-reference 우선순위

1. **섹션**: `{ref}` + `autosectionlabel` (`prefix_document = True` 로 충돌 방지)
2. **그림/표/식**: `{numref}` + `:name:`
3. **외부 프로젝트**: `intersphinx_mapping`
4. **논문**: `{cite}` + `refs.bib` (§8.5)

---

## 5. Diagram Authoring Rules ★

**가장 중요한 규약.** pccx 의 시각 품질은 다이어그램 품질에 비례합니다.

### 5.1 Selection matrix

| 상황 | 권장 도구 | 저장 위치 |
|---|---|---|
| PE 어레이 / 블록도 / 데이터패스 | **SVG (수작업)** | `_static/diagrams/` |
| 상태 머신 / 파이프라인 플로우 / 시퀀스 | **Mermaid** 인라인 | 페이지 내부 |
| RTL 타이밍 (AXI handshake, read/write 트랜잭션) | **WaveDrom** 인라인 | 페이지 내부 |
| 모듈 포함/계층 트리 | **Graphviz** `digraph` 인라인 | 페이지 내부 |
| 수치 그래프 / 벤치마크 | **matplotlib + scienceplots** | `plots/*.py` → 자동 |
| 레거시 PNG (v001, v002 일부) | 유지, 다크/라이트 두 벌 | `assets/images/` |

### 5.2 SVG (신규 표준)

**절대 규칙:**

- `stroke` / `fill` 에 **절대 색 하드코딩 금지** (`#000`, `#fff`, `black`, `white` 등).
- 텍스트·선: `stroke="currentColor"` 또는 `fill="currentColor"`.
- 강조색: Furo CSS 변수 사용.
  - `var(--color-brand-primary)` — 메인 강조
  - `var(--color-brand-content)` — 본문 내 강조
  - `var(--color-foreground-secondary)` — 보조 텍스트
  - `var(--color-background-secondary)` — 음영
- `viewBox` 로 정의, `width`/`height` 속성 **생략** (CSS 로 제어).
- 파일 크기 < 50 KB. 초과 시 심볼화(`<defs>` + `<use>`).

**스켈레톤:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img">
  <title>4×4 PE array</title>
  <desc>Simplified systolic array with weight-stationary dataflow.</desc>

  <style>
    .pe    { stroke: currentColor; fill: var(--color-background-secondary); }
    .label { fill: currentColor; font: 14px ui-sans-serif, system-ui; }
    .flow  { stroke: var(--color-brand-primary); fill: none; stroke-width: 1.5; }
  </style>

  <g class="pe-grid">
    <rect class="pe" x="20" y="20" width="60" height="60" rx="6"/>
    <!-- ... -->
  </g>
  <text class="label" x="400" y="20">Activations in →</text>
</svg>
```

`_templates/sample_svg.svg` 에 빈 스켈레톤을 두고 새 도면은 복제해 시작.

### 5.3 Mermaid

- `mermaid_init_js` 로 `startOnLoad: true`, `theme: 'neutral'` (중립 팔레트 → 다크/라이트 모두 수용).
- 페이지 안에서 코드 펜스로 직접 작성:
  ````markdown
  ```{mermaid}
  flowchart LR
    HOST[Host] -->|AXI-Lite| CTRL[NPU Controller]
    CTRL --> GEMM & GEMV & SFU & DMA
    DMA -->|AXI-HP| DDR[(DDR)]
  ```
  ````
- 복잡도가 커지면 SVG 로 마이그레이션.

### 5.4 WaveDrom

- RTL 타이밍 전용. JSON 포맷:
  ````markdown
  ```{wavedrom}
  { signal: [
    {name: "clk",   wave: "p......"},
    {name: "arvalid", wave: "0.1..0."},
    {name: "arready", wave: "1.....0"},
    {name: "araddr",  wave: "x.3..x.", data: ["addr"]},
  ]}
  ```
  ````
- CI 에서 렌더하려면 `wavedrom-cli` (npm) 가 필요. `deploy.yml` 에 `npm i -g wavedrom-cli` 단계 추가.

### 5.5 Graphviz

- 인라인 `.. graphviz::` / `:::{graphviz}`. `graphviz_output_format = 'svg'` 로 다크 모드 글자 인식.
- DOT 코드 내에서 `color="#808080"` 같은 중립 회색 대신 **속성 생략** 권장 (테마 CSS 가 제어).

### 5.6 레거시 PNG 관리

- **투명 배경**: `convert -fuzz 8% -transparent white`.
- **분할**: `<base>_{N}_v002.png`. 적용 현황:
  - `Processing_Elements_GEMM_{1..5}_v002.png`
  - `Processing_Elements_GEMV_{1..2}_v002.png`
- **다크/라이트 두 벌** (새 PNG 추가 시):
  ```markdown
  ![블록도](/_static/diagrams/foo-light.png){.only-light}
  ![블록도](/_static/diagrams/foo-dark.png){.only-dark}
  ```
- 원본 백업: `assets/images/Architecture/v002/_orig_backup/`.

### 5.7 Path prefixes (경로 주의 — ★ 듀얼-소스 핵심)

**Sphinx 의 `literalinclude` / `figure` 에서 선행 `/` 는 "파일 시스템 루트"가 아니라
"srcdir 기준 절대 경로"** 입니다. 본 repo 는 EN srcdir 이 **repo root** 이고 KO srcdir
이 **`ko/`** 라서 **동일한 `/foo/bar` 표기가 양 언어에서 다른 파일을 가리킵니다.**
따라서 **모든 크로스-srcdir 참조는 상대 경로**로 작성해야 합니다.

| 참조 종류 | EN 소스 (`docs/v002/<section>/<page>`) | KO 소스 (`ko/docs/v002/<section>/<page>`) |
|---|---|---|
| `_static/…` (CSS/JS/SVG) | `../../../../_static/…` (MyST `{figure}` 는 srcdir 기준 → `/_static/...` 사용 가능) | `../../../../_static/…` (KO 는 `html_static_path=['../_static']` 이라 figure 절대 경로 불가) |
| `assets/images/…` | `../../../assets/images/…` | `../../../../assets/images/…` |
| `codes/v002/…` RTL | `../../../codes/v002/…` | `../../../../codes/v002/…` |

요약:
- **EN 루트 파일** (`docs/...`): `../../../<target>` (3 단계 상위)
- **KO 루트 파일** (`ko/docs/...`): `../../../../<target>` (4 단계 상위)
- **figure 절대 경로** `/_static/...` 는 **EN 에서만** 안정적. 듀얼 호환이 필요하면 상대 경로 사용.

pagefind/autoapi 이후 루트 통합이 되면 이 규약을 재평가.

---

## 6. Plotting Conventions

### 6.1 File layout

```
plots/                    # 양 언어 공유. 영어 주석 + 영어 축 레이블.
├── plot_bandwidth.py
├── plot_gmacs.py
└── ...
auto_plots/               # gitignored. sphinx-gallery 가 생성.
ko/auto_plots/            # gitignored. 한국어 사이트용.
```

### 6.2 Standard header

모든 `plots/*.py` 는 아래 헤더로 시작:

```python
"""
Title
=====

One-line description that becomes the gallery card subtitle.
"""

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401

plt.style.use(['science', 'ieee', 'no-latex'])  # LaTeX 없이도 IEEE 스타일
# ... 데이터 준비 ...
fig, ax = plt.subplots(figsize=(3.5, 2.2))
# ... 플로팅 ...
plt.tight_layout()
plt.show()
```

### 6.3 Output format

- `plot_formats = [('svg', 100), ('png', 200)]`
- 다크모드 대비: scienceplots 기본 팔레트는 그레이스케일 친화. 주요 라인은 브랜드 색 지정 가능.
- **절대 색 하드코딩 금지** — 반드시 matplotlib rcParams 또는 전달된 palette 사용.

### 6.4 Embedding in prose

```markdown
:::{gallery-item}
/auto_plots/plot_bandwidth
:::
```

또는 단순히 toctree 에 `auto_plots/index` 를 포함.

---

## 7. Build Commands

### 7.1 Development (live reload)

```bash
make dev-en    # sphinx-autobuild . _build/html/en  → http://localhost:8000
make dev-ko    # sphinx-autobuild ko _build/html/ko → http://localhost:8001
```

### 7.2 Single-shot production

```bash
make en        # sphinx-build -b html . _build/html/en
make ko        # sphinx-build -b html ko _build/html/ko
make all       # 양쪽
```

### 7.3 Quality gates

```bash
make strict    # sphinx-build -W ... (경고를 에러로)
make linkcheck # sphinx-build -b linkcheck ...
make lint      # sphinx-lint + codespell
make clean     # rm -rf _build auto_plots ko/auto_plots
```

### 7.4 Multi-version (sphinx-multiversion)

```bash
sphinx-multiversion . _build/mv/en
sphinx-multiversion ko _build/mv/ko
```

- `smv_tag_whitelist = r'^v\d+\.\d+.*$'`
- `smv_branch_whitelist = r'^(main|v\d+-dev)$'`
- 각 버전의 conf.py 가 당대 extensions 로 빌드되어야 하므로, **새 확장 추가 시 과거 태그 호환성 먼저 검증**.
- 현재 repo 에 해당 패턴 태그가 없으므로 당장은 `main` 만 빌드. v003 분기 시 자연스럽게 드롭다운이 생성됨.

### 7.5 Local preview

```bash
python -m http.server --directory _build/html
# → http://localhost:8000/en/  또는 /ko/
```

---

## 8. Workflow Playbooks

### 8.1 새 페이지 추가 (ko-first)

1. `ko/docs/<section>/<slug>.md` 생성. MyST 사용.
   ```markdown
   # 페이지 제목

   ```{contents}
   :local:
   :depth: 2
   ```

   ## 섹션 1
   ...
   ```
2. 상위 `index.rst` / `index.md` 의 `toctree` 에 엔트리 추가.
3. 관련 인덱스(`v002/index.rst` 등) 업데이트.
4. `make dev-ko` 로 경고 0 개 확인.
5. 사용자 승인 후 `docs/<section>/<slug>.md` 에 영어 번역.
6. `make all && make strict` 통과 확인.
7. 커밋: `docs(ko): add <slug>` → `docs(en): translate <slug>`.

### 8.2 새 SVG 다이어그램 추가

1. `_templates/sample_svg.svg` 복제 → `_static/diagrams/<slug>.svg`.
2. `stroke`/`fill` 은 `currentColor` 또는 `var(--color-brand-primary)` 만 사용.
3. `<title>` + `<desc>` 접근성 태그 포함.
4. 페이지에서:
   ```markdown
   :::{figure} /_static/diagrams/<slug>.svg
   :name: fig-<slug>
   :alt: (시각장애인을 위한 설명)
   :width: 80%

   캡션 (한 줄)
   :::
   ```
5. 다크/라이트 토글로 시각 검증. 회색 배경 단색이 뿜뿜거리면 `var(--color-background-secondary)` 재확인.

### 8.3 새 플롯 추가

1. `plots/plot_<slug>.py` 생성 (§6.2 헤더 준수).
2. 로컬: `python plots/plot_<slug>.py` 로 그림이 열리는지 확인.
3. `make en` → `_build/html/en/auto_plots/plot_<slug>.html` 자동 생성.
4. 상위 갤러리 인덱스가 자동 업데이트되므로 toctree 수동 편집 불필요.
5. 결정적 출력을 위해 난수 `seed=42` 고정.

### 8.4 새 버전 브랜치 시작 (v003 등)

1. `main` 에서 `git switch -c v003-dev`.
2. `ko/docs/v003/` 과 `docs/v003/` 스켈레톤 복제 (index + `{Architecture,ISA,Drivers,RTL,Models}/index`).
3. `index.rst` 에 `v003` 토스트리 추가 (v002 와 병행).
4. `conf_common.py` 의 `smv_branch_whitelist` 에 `v003-dev` 포함 확인.
5. 안정화되면 `git tag v3.0.0` → sphinx-multiversion 드롭다운에 자동 등장.

### 8.5 논문 인용 추가

1. `refs.bib` 에 BibTeX 엔트리 추가:
   ```bibtex
   @article{gemma3n_2024,
     title   = {Gemma 3N: ...},
     author  = {...},
     journal = {arXiv},
     year    = {2024},
     url     = {https://arxiv.org/abs/...},
   }
   ```
2. 페이지 본문: `... {cite}`gemma3n_2024` 에 따르면 ...`.
3. 참고문헌 섹션이 필요한 페이지 끝에:
   ````markdown
   ## References

   ```{bibliography}
   :filter: docname in docnames
   ```
   ````

### 8.6 RTL 참조 업데이트

§9 참고. 핵심은 **commit SHA 를 코멘트로 박아두기**.

---

## 9. Cross-repo References

### 9.1 v002 RTL 참조 패턴

`docs/v002/RTL/*.rst` 는 외부 레포 `hwkim-dev/pccx-FPGA-NPU-LLM-kv260`
를 `codes/v002/` 로 clone 한 뒤 `literalinclude` 로 인라인. 경로는 **상대**
(§5.7 참고): EN 은 `../../../codes/v002/…`, KO 는 `../../../../codes/v002/…`.

```rst
.. literalinclude:: ../../../codes/v002/hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_pkg.sv
   :language: systemverilog
   :start-at: typedef enum
   :end-before: endpackage
   :caption: isa_pkg.sv — opcode_e

.. admonition:: Last verified against
   :class: note

   Commit ``<SHA>`` @ ``hwkim-dev/pccx-FPGA-NPU-LLM-kv260``
   (YYYY-MM-DD)
```

### 9.2 규칙

1. **상대 경로** 사용. 언어별 깊이는 §5.7 표 참조. 절대 경로(`/codes/...`) 는
   srcdir 차이 때문에 KO 에서 깨짐.
2. **줄 번호 고정 금지** (`:lines: 10-30` 대신 `:start-at:` / `:end-at:` / `:start-after:` / `:end-before:`).
   - 사유: 상류 RTL 이 수정될 때 줄 번호가 쉽게 어긋남.
3. **`Last verified against: <SHA>`** 메모를 각 RTL 참조 페이지 하단에 명시.
   RTL 갱신 시 문서도 재검증해야 함을 가시화.
4. CI 가 매일/주간 RTL 업데이트를 감지해 `linkcheck` / 파일 존재 여부를 확인할 수 있도록
   `linkcheck.yml` 에서 `codes/v002` clone 유지.

### 9.3 v001 RTL (repo 내부)

- `codes/v001/` 은 아카이브. 경로는 동일 패턴 (`/codes/v001/hw/rtl/...`).
- v001 페이지는 `docs/archive/experimental_v001/` 에 한정. **수정은 원칙적으로 금지**.

### 9.4 ISA 단일 출처 (Single Source of Truth)

- 현재 권위 있는 ISA 정의: `codes/v001/hw/rtl/NPU_Controller/NPU_Control_Unit/ISA_PACKAGE/isa_pkg.sv`.
- 문서의 인코딩 표(`docs/v002/ISA/encoding.rst`)는 반드시 이 패키지와 일치.
- v002 전용 ISA 패키지가 별도로 만들어지면 본 섹션 재평가.

---

## 10. Known Caveats

### 10.1 WaveDrom CLI 의존

- 로컬 미리보기는 브라우저에서 JS 렌더로 충분.
- CI SSR 을 원하면 `deploy.yml` 에 `npm i -g wavedrom-cli` 추가 필요.
- 설치 실패 시 페이지는 **빈 공간**으로 렌더되므로 `make strict` 로 즉시 탐지 가능.

### 10.2 Mermaid 다크 모드

- `theme: 'neutral'` 로 중립 팔레트 사용 중. 테마 전환 시 **새로고침 전까지 색이 유지**되는 경우가 있음 (Mermaid 초기화 타이밍 이슈).
- 중요한 다이어그램은 SVG 로 마이그레이션.

### 10.3 Sphinx / myst-parser / myst-nb 버전 락

현재 모든 파일을 특정 버전 조합에 핀하고 있음:

- **Sphinx `7.4.x`** — Sphinx 8.0 은 `SphinxUnreferencedFootnotesDetector` 를 core
  에 통합하면서 transform registry 에서 자동 등록을 빼버렸고, myst-parser 5.0 은 이
  transform 을 조건 없이 `.remove()` 하기 때문에 setup 시 `ValueError` 로 폭사함.
- **myst-parser `4.0.x`** — 5.0 은 위 버그 외에도 myst-nb 1.4 가 내부에서
  `setup_sphinx(app)` 을 두 번째로 호출하는 경로와 충돌해 같은 `ValueError` 를 냄.
- **myst-nb `1.4.x`** — 2.x 는 아직 출시되지 않았고 myst-parser 4 API 와 맞는 마지막
  라인.

**Extensions 목록에는 `myst_nb` 만 나열하고 `myst_parser` 는 빼야 함** (myst-nb 가
transitively 로드). 둘 다 넣으면 `setup_sphinx` 가 두 번 실행돼 터짐.

재평가 시점: myst-parser 6 (Sphinx 8/9 호환) 이 릴리즈되는 시점.

### 10.4 sphinx-multiversion × historical conf.py

- 과거 태그는 **그 시점의 conf.py + 당대 extension 집합**으로 빌드됨.
- 따라서 **새 확장 추가는 과거 태그 빌드를 깨뜨릴 수 있음**.
- 실용 대책: (a) `smv_tag_whitelist` 에 최신 태그만 포함, (b) 구 태그 빌드 실패를 허용하고 `main` 만 deploy job 의 실패 조건으로 설정.

### 10.5 Furo × 커스텀 JS/CSS

- `language-switcher.js` 는 PyData DOM 전용이었으며 **Furo 용으로 재작성됨** (`_templates/sidebar/brand.html` 슬롯).
- `mermaid-theme.js` 는 Furo 의 네이티브 다크/라이트 토글과 기능 중복 → **제거**.
- `image-lightbox.js/css` 는 본문 DOM 만 사용하므로 유지.

### 10.6 검색 규모

- Furo 기본 검색은 Sphinx 의 `searchindex.js`. 페이지 500 개 수준까지는 무난.
- 그 이상 (또는 한국어 형태소 분석 필요) 이면 **pagefind** 로 전환 예정 (Phase 5 이후 로드맵).

### 10.7 CI 경고 정책

- **CI 는 `-W`**. 경고는 전부 에러.
- 회피하려면 `nitpick_ignore` 또는 해당 경고 원인 교정. 빌드 스킵은 금지.

### 10.8 codes/v002 미존재 시

- 로컬 빌드에서 `codes/v002/` 가 없으면 RTL `literalinclude` 가 실패.
- `docs/v002/RTL/*.rst` 상단의 안내에 따라 `git clone` 선행.
- `make all` 은 `codes/v002/.git` 존재를 검사해 부재 시 친절한 에러 출력.

### 10.9 i18n 구조

- 현재는 **duplicated-source**. gettext (`sphinx-intl`) 는 사용하지 않음.
- 번역 누락/드리프트 방지: CI 에 **양 언어 파일 개수 동일성 체크** 추가 (`lint.yml`).

---

## 11. Agent Guidance (Claude 전용)

> 이 섹션은 Claude Code / 다른 AI 에이전트가 pccx 에서 작업할 때의 체크리스트입니다.
> 인간 기여자는 건너뛰어도 무방합니다.

### 11.1 작업 전 체크

- [ ] `git status` 로 워킹 트리 청결 확인.
- [ ] 현재 브랜치가 `main` 이 아닌 feature 브랜치(`claude/<slug>` 또는 `feat/<slug>`) 인지 확인.
- [ ] `CLAUDE.md` 최신 버전 읽기. 이 파일이 다른 지침과 충돌하면 **이 파일이 우선**.

### 11.2 코딩 원칙

- **한쪽 언어만 수정해 커밋 요청 금지** (§4.1). 기본은 한국어 먼저, 사용자 승인 후 영어.
- **새 다이어그램은 SVG + currentColor**. PNG 신규 생성 금지 (레거시 교체는 허용).
- **색 하드코딩 금지** (§5.2, §6.3).
- **경고 0 유지**. `make strict` 가 통과하지 않으면 작업 미완료.
- **`numref` / `:name:` 누락 금지**. 모든 figure/table/eq 에 name 을 붙여 향후 cross-ref 가능.
- **기존 `.rst` 를 `.md` 로 일괄 변환 금지** (단일 task 로 별도 진행). 신규만 `.md`.

### 11.3 실수 방지

- `assets/` 와 `_static/` 혼동 금지. 새 자산은 **`_static/diagrams/`**.
- `codes/v002/` 수정 금지 (외부 repo). 수정이 필요하면 상류 repo 로 이동.
- `ko/` 와 루트 `conf.py` 의 옵션 동기화는 `conf_common.py` 하나로 끝내기. 양쪽을 각각 편집하지 말 것.
- 기존 CLAUDE.md 를 `.gitignore` 에서 제거해 커밋 대상으로 전환했음을 기억. `.gitignore` 재추가 금지.

### 11.4 Build verification rhythm

- 페이지 1개 편집 → `make dev-ko` 라이브 리로드로 확인.
- PR 직전 → `make strict` + `make lint` 모두 통과해야 함.
- 긴 작업 후 → `make linkcheck` 한 번.

### 11.5 PR / 커밋 컨벤션

- Conventional Commits 느슨 적용: `docs:`, `feat:`, `fix:`, `chore:`, `refactor:`, `style:`.
- 본문은 **왜** 를 설명. **무엇** 은 diff 로 이미 명시됨.
- Breaking change 는 `BREAKING CHANGE:` footer.

### 11.6 Tools

- GitHub 운영: `gh` CLI.
- 크로스 레포 참조 업데이트: `codes/v002/.git/HEAD` 의 SHA 를 페이지 "last verified against" 에 기록.

---

## 12. Roadmap (post-migration)

현재 브랜치(`feat/sphinx-furo-migration`) 완료 후 후속 개선 항목:

- [ ] **기존 RST → MyST MD 점진 마이그레이션** (섹션 단위, 의미 보존).
- [ ] **`sphinx-external-toc`** 활성화 (`_toc.yml` 단일 소스). 현재는 설치만.
- [ ] **pagefind** 도입 — 사이트 규모가 페이지 500+ 돌파 시.
- [ ] **v003 RTL 분기 및 문서 템플릿**.
- [ ] **sphinx-needs** 검토 — 요구사항 ↔ RTL 모듈 ↔ 테스트 traceability 매트릭스가 필요해질 때.
- [ ] **Giscus/utterances** 댓글 (사용자 피드백 수집용).
- [ ] **API 자동 문서화** — Python 드라이버가 실제 코드로 존재하면 `sphinx-autoapi`.
- [ ] **Mermaid → SVG 일괄 교체** (중요 다이어그램 순차적으로).

---

_끝. 이 문서에 없는 규약이 필요하면 먼저 여기에 추가한 뒤 행동한다._
