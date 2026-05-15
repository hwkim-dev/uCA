# =============================================================================
# pccx — documentation build targets
#
# Convenience wrapper around sphinx-build / sphinx-autobuild for the dual
# English-Korean dual-source site.
# =============================================================================

PY             ?= python
SPHINXBUILD    ?= sphinx-build
SPHINXAUTOBLD  ?= sphinx-autobuild
SPHINXOPTS     ?=

# Source roots (per language).
EN_SRC         := .
KO_SRC         := ko

# Build output roots (kept together for a single deploy upload).
BUILD_ROOT     := _build/html
EN_OUT         := $(BUILD_ROOT)/en
KO_OUT         := $(BUILD_ROOT)/ko
ROOT_ROBOTS    := _extra/robots.txt
ROOT_SITEMAP   := $(BUILD_ROOT)/sitemap.xml
PUBLIC_BASE_URL := https://docs.pccx.ai

# Dev server ports.
DEV_PORT_EN    := 8000
DEV_PORT_KO    := 8001

# Common flags.
STRICT         := -W --keep-going -n
AUTOBLD_FLAGS  := --re-ignore '_build' --re-ignore 'auto_plots' --open-browser


# -- Phony ------------------------------------------------------------------

.PHONY: help en ko all site-root-files strict dev-en dev-ko linkcheck lint clean distclean \
        check-codes install install-dev

help:
	@echo "pccx documentation — make targets"
	@echo "  make en          Build English HTML  → $(EN_OUT)/"
	@echo "  make ko          Build Korean  HTML  → $(KO_OUT)/"
	@echo "  make all         Build both languages"
	@echo "  make strict      Build both with -W (CI mode)"
	@echo "  make dev-en      Autobuild + serve EN on :$(DEV_PORT_EN)"
	@echo "  make dev-ko      Autobuild + serve KO on :$(DEV_PORT_KO)"
	@echo "  make linkcheck   Run Sphinx linkcheck builder (EN + KO)"
	@echo "  make lint        sphinx-lint + codespell"
	@echo "  make clean       Remove _build/ and auto_plots/"
	@echo "  make distclean   clean + remove codes/v002/"
	@echo "  make install     pip install -r requirements.txt"
	@echo "  make install-dev pip install -r requirements-dev.txt"


# -- Preflight --------------------------------------------------------------
#
# v002 RTL sources live in an external repo and must be cloned into
# codes/v002/ before RTL literalinclude pages can build.

check-codes:
	@if [ ! -d "codes/v002/.git" ]; then \
	    echo "\033[33m[pccx] codes/v002 is missing.\033[0m"; \
	    echo "    Clone it with:"; \
	    echo "        git clone --depth 1 \\"; \
	    echo "            https://github.com/pccxai/pccx-FPGA-NPU-LLM-kv260 \\"; \
	    echo "            codes/v002"; \
	    exit 1; \
	fi


# -- Build targets ----------------------------------------------------------

en: check-codes
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(EN_SRC) $(EN_OUT)

ko: check-codes
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(KO_SRC) $(KO_OUT)

all: en ko site-root-files

site-root-files:
	mkdir -p $(BUILD_ROOT)
	@if [ -f "$(ROOT_ROBOTS)" ]; then \
	    cp "$(ROOT_ROBOTS)" "$(BUILD_ROOT)/robots.txt"; \
	fi
	@{ \
	    printf '%s\n' '<?xml version="1.0" encoding="UTF-8"?>'; \
	    printf '%s\n' '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'; \
	    if [ -f "$(EN_OUT)/sitemap-en.xml" ]; then \
	        printf '%s\n' '  <sitemap><loc>$(PUBLIC_BASE_URL)/en/sitemap-en.xml</loc></sitemap>'; \
	    fi; \
	    if [ -f "$(KO_OUT)/sitemap-ko.xml" ]; then \
	        printf '%s\n' '  <sitemap><loc>$(PUBLIC_BASE_URL)/ko/sitemap-ko.xml</loc></sitemap>'; \
	    fi; \
	    printf '%s\n' '</sitemapindex>'; \
	} > "$(ROOT_SITEMAP)"

strict: SPHINXOPTS += $(STRICT)
strict: all


# -- Dev servers ------------------------------------------------------------

dev-en: check-codes
	$(SPHINXAUTOBLD) $(AUTOBLD_FLAGS) --port $(DEV_PORT_EN) $(EN_SRC) $(EN_OUT)

dev-ko: check-codes
	$(SPHINXAUTOBLD) $(AUTOBLD_FLAGS) --port $(DEV_PORT_KO) $(KO_SRC) $(KO_OUT)


# -- Quality gates ----------------------------------------------------------

linkcheck: check-codes
	$(SPHINXBUILD) -b linkcheck $(EN_SRC) _build/linkcheck/en
	$(SPHINXBUILD) -b linkcheck $(KO_SRC) _build/linkcheck/ko

lint:
	@command -v sphinx-lint >/dev/null || (echo "sphinx-lint missing; pip install -r requirements-dev.txt"; exit 1)
	sphinx-lint --enable all --disable line-too-long docs ko/docs
	@command -v codespell >/dev/null || (echo "codespell missing"; exit 1)
	codespell --skip="*.svg,*.png,*.jpg,*.jpeg,*.pdf,*.js,*.css,*.html,_build,auto_plots,.venv,codes,.git,todo.md" \
	          --ignore-words-list="nd,ot,te,ans,hist,ue,som,sow,lod"


# -- Housekeeping -----------------------------------------------------------

clean:
	rm -rf _build auto_plots ko/auto_plots

distclean: clean
	rm -rf codes/v002


# -- Install shortcuts ------------------------------------------------------

install:
	$(PY) -m pip install -r requirements.txt

install-dev:
	$(PY) -m pip install -r requirements-dev.txt
