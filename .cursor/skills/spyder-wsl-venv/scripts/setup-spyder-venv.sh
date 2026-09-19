#!/usr/bin/env bash
# setup-spyder-venv.sh — prepare a project venv for Ubuntu/WSL Spyder, or revert Spyder.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  setup-spyder-venv.sh [PROJECT_DIR]
  setup-spyder-venv.sh --revert-spyder
  setup-spyder-venv.sh --point PROJECT_DIR
  setup-spyder-venv.sh --help

Default: create/use PROJECT_DIR/.venv, install matching spyder-kernels for the
installed Spyder major version. Does not change Spyder prefs unless --point.

  --revert-spyder   Force Spyder back to /usr/bin/python3 (fixes blank console)
  --point DIR       After kernels are OK, point Spyder at DIR/.venv/bin/python
EOF
}

SPYDER_INI="${HOME}/.config/spyder-py3/config/spyder.ini"
TRANSIENT_INI="${HOME}/.config/spyder-py3/config/transient.ini"

spyder_major() {
  python3 - <<'PY' 2>/dev/null || true
try:
    import spyder
    print(spyder.__version__.split(".")[0])
except Exception:
    pass
PY
}

detect_kernels_spec() {
  local major
  major="$(spyder_major)"
  if [[ -z "${major}" ]]; then
    # apt package fallback
    if dpkg -l spyder 2>/dev/null | grep -q '^ii'; then
      major="$(dpkg -l spyder | awk '/^ii/{print $3}' | cut -d. -f1)"
    fi
  fi
  case "${major}" in
    5) echo 'spyder-kernels==2.5.*' ;;
    6) echo 'spyder-kernels>=3,<4' ;;
    *)
      echo "WARN: could not detect Spyder version; defaulting to 2.5.* (Spyder 5)" >&2
      echo 'spyder-kernels==2.5.*'
      ;;
  esac
}

revert_spyder() {
  [[ -f "${SPYDER_INI}" ]] || { echo "No Spyder config at ${SPYDER_INI}"; exit 1; }
  python3 - <<PY
import configparser
from pathlib import Path

base = Path("${SPYDER_INI}").parent
spyder = configparser.ConfigParser()
spyder.read(base / "spyder.ini")
spyder["main_interpreter"]["custom"] = "False"
spyder["main_interpreter"]["default"] = "True"
with open(base / "spyder.ini", "w") as f:
    spyder.write(f)

transient = configparser.ConfigParser()
transient.read(base / "transient.ini")
if "main_interpreter" not in transient:
    transient["main_interpreter"] = {}
transient["main_interpreter"]["executable"] = "/usr/bin/python3"
with open(base / "transient.ini", "w") as f:
    transient.write(f)
print("Reverted Spyder to /usr/bin/python3")
print("Fully quit and reopen Spyder.")
PY
}

point_spyder() {
  local project="$1"
  local py="${project}/.venv/bin/python"
  [[ -x "${py}" ]] || { echo "Missing executable: ${py}"; exit 1; }

  # Refuse to point if kernels missing/wrong major vs Spyder when detectable
  local need major kver
  need="$(detect_kernels_spec)"
  major="$(spyder_major)"
  kver="$("${py}" -c "import spyder_kernels; print(spyder_kernels.__version__)" 2>/dev/null || true)"
  if [[ -z "${kver}" ]]; then
    echo "ERROR: spyder-kernels not importable in ${py}"
    echo "Run: ${project}/.venv/bin/pip install '${need}'"
    exit 1
  fi
  if [[ "${major}" == "5" && "${kver}" != 2.* ]]; then
    echo "ERROR: Spyder 5 needs spyder-kernels 2.5.*, found ${kver}"
    exit 1
  fi
  if [[ "${major}" == "6" && "${kver}" != 3.* ]]; then
    echo "ERROR: Spyder 6 needs spyder-kernels 3.*, found ${kver}"
    exit 1
  fi

  python3 - <<PY
import configparser
from pathlib import Path

base = Path("${SPYDER_INI}").parent
venv = "${py}"

spyder = configparser.ConfigParser()
spyder.read(base / "spyder.ini")
spyder["main_interpreter"]["custom"] = "True"
spyder["main_interpreter"]["default"] = "False"
with open(base / "spyder.ini", "w") as f:
    spyder.write(f)

transient = configparser.ConfigParser()
transient.read(base / "transient.ini")
if "main_interpreter" not in transient:
    transient["main_interpreter"] = {}
transient["main_interpreter"]["custom_interpreter"] = venv
transient["main_interpreter"]["executable"] = venv
with open(base / "transient.ini", "w") as f:
    transient.write(f)
print(f"Pointed Spyder at {venv}")
print("Fully quit and reopen Spyder, then: import sys; print(sys.executable)")
PY
}

setup_venv() {
  local project="$1"
  local py="${project}/.venv/bin/python"
  local need
  need="$(detect_kernels_spec)"

  mkdir -p "${project}"
  if [[ ! -x "${py}" ]]; then
    python3 -m venv "${project}/.venv"
    echo "Created ${project}/.venv"
  fi

  "${py}" -m pip install -U pip
  "${py}" -m pip install "${need}"

  echo
  echo "OK. Venv: ${py}"
  "${py}" -c "import spyder_kernels; print('spyder-kernels', spyder_kernels.__version__)"
  echo
  echo "Install project deps with:"
  echo "  ${project}/.venv/bin/pip install <packages>"
  echo
  echo "When ready to switch Spyder:"
  echo "  $0 --point ${project}"
  echo "If console breaks:"
  echo "  $0 --revert-spyder"
}

main() {
  case "${1:-}" in
    -h|--help) usage; exit 0 ;;
    --revert-spyder) revert_spyder; exit 0 ;;
    --point)
      [[ -n "${2:-}" ]] || { usage; exit 1; }
      point_spyder "$(cd "$2" && pwd)"
      exit 0
      ;;
    "")
      setup_venv "$(pwd)"
      ;;
    *)
      setup_venv "$(cd "$1" && pwd)"
      ;;
  esac
}

main "$@"
