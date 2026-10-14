# LaTeX and record workflows. Run `make` or `make help` for targets.
# Select a document with TEX=path/to/file.tex; see scripts/tex-lint.md.

.DEFAULT_GOAL := help
SHELL := /bin/bash

# GNU make predefines TEX=tex, so `TEX ?= ...` would never apply.
ifneq ($(filter default undefined,$(origin TEX)),)
TEX := templates/solution-sheet.tex
endif
DIR ?= solutions
RECORDS ?= problems
WIDTH ?= 79
NUMBERING ?= cited
REV ?= @
PYTHON ?= python3
LINT := $(PYTHON) scripts/lint-tex --width $(WIDTH) --numbering $(NUMBERING)
BUILD := $(PYTHON) scripts/build-tex
export TEX

.PHONY: help doctor setup lint lint-diff lint-fix format format-check lint-all unnumber lint-changed differentials \
	test build pdf view watch check clean records

help: ## Show this help
	@printf 'Usage: make <target> [TEX=path/to/paper.tex] [DIR=solutions] [WIDTH=79] [NUMBERING=cited|all]\n'
	@printf 'Current TEX=%s\n\n' '$(TEX)'
	@awk 'BEGIN {FS = ":.*## "} /^[a-z0-9 -]+:.*## / {printf "  %-13s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

doctor: ## Check that every required tool is installed
	@$(PYTHON) scripts/doctor

setup: ## Install latexindent's Perl modules locally in .tools/
	@./scripts/setup-tex-lint

lint: ## Check formatting, house style and ChkTeX (read-only)
	@$(LINT) "$$TEX"

lint-diff: ## Check, and show the proposed formatting changes
	@$(LINT) --diff "$$TEX"

lint-fix: ## Apply formatting, then report what is left
	@$(LINT) --fix "$$TEX"

format: ## Apply mechanical formatting only
	@$(LINT) --fix --format-only "$$TEX"

format-check: ## Check mechanical formatting only
	@$(LINT) --format-only "$$TEX"

unnumber: ## Star displays whose numbers are never cited (changes PDF numbers)
	@$(LINT) --unnumber "$$TEX"

lint-changed: ## Lint the .tex files changed in the jj change REV (default @)
	@$(LINT) --changed '$(REV)'

differentials: ## Rewrite hand-written dx, \,dm, \frac{d\theta}{..} as \dd (changes PDF)
	@$(LINT) --differentials "$$TEX"

lint-all: ## Summarize lint for every root document under DIR (report only)
	@$(LINT) --summary --roots "$(DIR)"

test: ## Run the lint, build and record-checker tests
	@$(PYTHON) -m unittest discover -s scripts -p 'test_*.py'

# Prerequisites, not sibling recipes: even make -j finishes lint first.
build: lint ## Lint, then compile TEX into build/<path>/
	@$(BUILD)

pdf: lint ## Lint, compile, and copy the PDF next to the source
	@$(BUILD) --publish

view: ## Open the built PDF (builds it first if missing)
	@$(BUILD) --view

watch: ## Recompile on every save (no lint gate)
	@$(BUILD) --watch

# Sequential on purpose: as prerequisites, test and build could run in parallel under -j.
check: ## Run the tests, then the lint-gated build
	@$(MAKE) --no-print-directory test
	@$(MAKE) --no-print-directory build

clean: ## Remove TEX's auxiliary files (keeps its PDF)
	@$(BUILD) --clean

records: ## Validate the problem records under RECORDS (default problems/)
	@$(PYTHON) tools/check_records.py "$(RECORDS)"
