---
name: spyder-wsl-venv
description: >-
  Diagnose and fix Spyder + WSL2 + Python venv issues: ModuleNotFoundError,
  blank/missing IPython console, PEP 668 system pip blocks, and interpreter
  mismatches. Use when the user mentions Spyder, runcell, spyder_kernels,
  WSL2 venv, --break-system-packages, or packages that work in terminal but
  fail inside Spyder.
---

# Spyder + WSL2 + venv

Ubuntu/WSL Spyder often uses **system Python** while packages live in a **project `.venv`**. Activating the venv in a terminal does **not** change Spyder. Wrong `spyder-kernels` version makes the console never open.

For this repo's full setup walkthrough, see [AGENTS.md](../../../AGENTS.md) at the project root. Prefer project-local helper paths:

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh .
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh --point .
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh --revert-spyder
```

## Hard rules

1. **Never** `pip install` into system Python (`/usr/bin/python3`) — PEP 668. No `--break-system-packages` unless the user explicitly insists.
2. **Never** point Spyder at a venv until that venv has a **compatible** `spyder-kernels`.
3. If the console is dead, **revert to system interpreter first**, then fix the venv. Do not keep flipping prefs while Spyder is broken.
4. Prefer fixing configs under `~/.config/spyder-py3/` over guessing UI clicks when the user is stuck.

## Version matrix (critical)

| Spyder (apt/UI) | Required `spyder-kernels` in the venv |
|-----------------|----------------------------------------|
| 5.x (e.g. 5.5.1) | `2.5.*` |
| 6.x             | `3.*` |

Mismatch → console blank / no run / kernel dies immediately.

Detect Spyder version:

```bash
python3 -c "import spyder; print(spyder.__version__)"
# or
dpkg -l spyder | awk '/^ii/{print $3}'
```

## Decision tree

```
Symptom?
├─ ModuleNotFoundError in Spyder (traceback under /usr/lib/python3/...)
│  → Spyder is on system Python; packages are in .venv (or nowhere)
│  → Fix: point Spyder at .venv AFTER installing matching spyder-kernels
│
├─ pip / PEP 668 / --break-system-packages hint
│  → User tried system pip. Stop. Use .venv pip only
│
├─ No console / cannot run / kernel won't start after switching interpreter
│  → Likely spyder-kernels mismatch OR bad custom interpreter
│  → Revert to system Python, pin kernels, then re-point
│
├─ Works in terminal / Cursor .venv, fails in Spyder
│  → Expected until Spyder executable == .venv/bin/python
│
└─ SyntaxError on `pip install ...` in a cell
   → Use `!pip install ...` in notebook, or real terminal with venv active
```

## Safe setup workflow

Copy and track:

```
- [ ] 1. Create/activate project venv
- [ ] 2. Install project deps into venv
- [ ] 3. Detect Spyder major version
- [ ] 4. Install matching spyder-kernels into venv
- [ ] 5. Point Spyder at .venv/bin/python
- [ ] 6. Fully quit + reopen Spyder (or restart kernel)
- [ ] 7. Verify sys.executable and imports
```

### 1–2. Venv + deps

```bash
cd /path/to/project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install networkx matplotlib  # project packages
```

Or run the helper from the repo root (project skill) or personal skill:

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh .
# personal copy (if linked): bash ~/.cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh .
```

### 3–4. Matching kernels

Spyder 5.x:

```bash
.venv/bin/pip install 'spyder-kernels==2.5.*'
```

Spyder 6.x:

```bash
.venv/bin/pip install 'spyder-kernels>=3,<4'
```

Verify:

```bash
.venv/bin/python -c "import spyder_kernels, networkx; print(spyder_kernels.__version__)"
```

### 5. Point Spyder at the venv

**UI path**

1. Tools → Preferences → Python interpreter
2. Select **Use the following Python interpreter**
3. Path: `/path/to/project/.venv/bin/python` (Linux/WSL path, not `C:\...`)
4. Apply → OK
5. **Fully quit Spyder**, reopen (restart kernel alone is often not enough after a broken kernel)

**Config path** (when UI failed or agent is repairing)

Files:

- `~/.config/spyder-py3/config/spyder.ini`
- `~/.config/spyder-py3/config/transient.ini`

Set:

| File | Keys |
|------|------|
| `spyder.ini` `[main_interpreter]` | `custom = True`, `default = False` |
| `transient.ini` `[main_interpreter]` | `custom_interpreter = <venv>/bin/python`, `executable = <venv>/bin/python` |

Selecting the path alone while `custom = False` leaves Spyder on system Python. That is a common silent failure.

### 6–7. Verify inside Spyder

```python
import sys
print(sys.executable)
# must be: .../project/.venv/bin/python

import networkx as nx
print(nx.__version__)
```

## Emergency recovery (blank console)

Revert immediately:

| File | Keys |
|------|------|
| `spyder.ini` | `custom = False`, `default = True` |
| `transient.ini` | `executable = /usr/bin/python3` |

Then fully quit Spyder and reopen. Console should return on system Python.

After recovery:

1. Pin correct `spyder-kernels` in the venv (see matrix)
2. Re-enable custom interpreter
3. Verify `sys.executable`

Helper recovery:

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh --revert-spyder
```

## Diagnosis checklist (agent)

Run these before changing prefs:

```bash
# Who has the package?
/usr/bin/python3 -c "import networkx" 2>&1
/path/to/project/.venv/bin/python -c "import networkx; print(networkx.__file__)" 2>&1

# Spyder vs kernels
python3 -c "import spyder; print('spyder', spyder.__version__)" 2>&1
/path/to/project/.venv/bin/python -c "import spyder_kernels; print('kernels', spyder_kernels.__version__)" 2>&1

# What Spyder will launch
python3 - <<'PY'
import configparser
from pathlib import Path
b = Path.home() / ".config/spyder-py3/config"
s, t = configparser.ConfigParser(), configparser.ConfigParser()
s.read(b / "spyder.ini"); t.read(b / "transient.ini")
print("custom", s.get("main_interpreter", "custom", fallback="?"))
print("default", s.get("main_interpreter", "default", fallback="?"))
print("executable", t.get("main_interpreter", "executable", fallback="?"))
print("custom_interpreter", t.get("main_interpreter", "custom_interpreter", fallback="?"))
PY
```

If traceback shows `/usr/lib/python3/dist-packages/spyder_kernels/`, Spyder is **not** using the venv yet.

## WSL2 notes

- Paths must be WSL Linux paths (`/home/.../.venv/bin/python`), not Windows `\\wsl$\...` unless Spyder itself is a Windows app talking to WSL (unusual for apt Spyder).
- apt Spyder lives under `/usr/lib/python3/dist-packages/spyder*`.
- Kernel crash logs often under `/tmp/spyder-<user>/kernel-*.stderr`.
- Cursor/VS Code "Connected to .venv" is independent of Spyder. Fix each IDE separately.
- Zed + Jupyter is separate too — see [../zed-jupyter/SKILL.md](../zed-jupyter/SKILL.md).

## What not to do

- Do not tell the user that `source .venv/bin/activate` fixes Spyder.
- Do not install packages with system `pip` to "make Spyder work".
- Do not install `spyder-kernels` 3.x into a venv used by Spyder 5.x.
- Do not leave `custom = True` with a broken kernel; revert first.

## Extra detail

- Config keys, full scripts, and incident notes: [reference.md](reference.md)
- Setup / revert helper: [scripts/setup-spyder-venv.sh](scripts/setup-spyder-venv.sh)
