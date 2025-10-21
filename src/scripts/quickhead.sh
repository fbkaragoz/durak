#!/usr/bin/env bash

set -euo pipefail
shopt -s inherit_errexit 2>/dev/null || true

# -*-*-*-*- colors & logs -*-*-*-*- #

RED=$'\033[31m'; GRN=$'\033[32m'; YLW=$'\033[33m'; RST=$'\033[0m'
log() { printf '%b\n' "${GRN}[INFO]${RST} $*"; }
warn() { printf '%b\n' "${YLW}[WARN]${RST} $*"; }
die() { printf '%b\n' "${RED}[ERROR]${RST} $*"; exit 1; }



# -*-*-*-*- quick checks -*-*-*-*- #

log "Does Python exist?"
command -v python >/dev/null 2>&1 || die "Python is not installed."

log "Is pytest installed?"
python -m pytest --version >/dev/null 2>&1 || die "pytest is not installed."

log "Collect only test"
python -m pytest --collect-only -q 2>&1 | grep -E "test_" >/dev/null || die "No tests found."

log "Listing tests (ruff)"
python -m ruff check src/tests --select PT --quiet || die "Ruff test listing failed."

log "Type checking (mypy)"
python -m mypy src --exclude 'src/scripts' || die "Mypy type checking failed."

log "All quick checks passed."