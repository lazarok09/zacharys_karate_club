# Spyder + WSL2 + venv — reference

## Incident notes (zacharys_karate_club, 2026-09)

What went wrong and what fixed it:

1. `networkx` installed only in project `.venv`.
2. Spyder 5.5.1 kept using `/usr/bin/python3` → `ModuleNotFoundError` with traceback under `/usr/lib/python3/dist-packages/spyder_kernels/`.
3. User tried system `pip` → PEP 668 / `--break-system-packages` hint.
4. Agent installed `spyder-kernels==3.1.6` (Spyder **6** line) into the venv, then set custom interpreter → **console never opened**.
5. Recovery: revert Spyder to system Python; pin `spyder-kernels==2.5.2` for Spyder 5.5.1.

Lesson: match kernels to Spyder **before** switching the interpreter.

## Config file map

Base: `~/.config/spyder-py3/config/`

| File | Role |
|------|------|
| `spyder.ini` | Persistent prefs; `main_interpreter.custom` / `default` toggle |
| `transient.ini` | Runtime paths: `executable`, `custom_interpreter`, `custom_interpreters_list` |
| `backups/*.bak` | Previous copies; useful if a bad edit needs undo |
| `defaults/defaults-spyder-*.ini` | Factory defaults for the installed Spyder build |

### Effective interpreter logic

- If `spyder.ini` → `custom = False` (and `default = True`): use system / default Spyder Python even if `transient.ini` lists a venv path.
- If `custom = True`: Spyder should launch `transient.ini` → `executable` (should equal `custom_interpreter`).

Always set **both** the toggle and the path.

### Minimal safe revert snippet

```python
import configparser
from pathlib import Path

base = Path.home() / ".config/spyder-py3/config"
venv = None  # unused on revert

spyder = configparser.ConfigParser()
spyder.read(base / "spyder.ini")
spyder["main_interpreter"]["custom"] = "False"
spyder["main_interpreter"]["default"] = "True"
with open(base / "spyder.ini", "w") as f:
    spyder.write(f)

transient = configparser.ConfigParser()
transient.read(base / "transient.ini")
transient["main_interpreter"]["executable"] = "/usr/bin/python3"
with open(base / "transient.ini", "w") as f:
    transient.write(f)
```

### Minimal point-to-venv snippet

```python
import configparser
from pathlib import Path

base = Path.home() / ".config/spyder-py3/config"
venv = "/absolute/path/to/project/.venv/bin/python"

spyder = configparser.ConfigParser()
spyder.read(base / "spyder.ini")
spyder["main_interpreter"]["custom"] = "True"
spyder["main_interpreter"]["default"] = "False"
with open(base / "spyder.ini", "w") as f:
    spyder.write(f)

transient = configparser.ConfigParser()
transient.read(base / "transient.ini")
transient["main_interpreter"]["custom_interpreter"] = venv
transient["main_interpreter"]["executable"] = venv
with open(base / "transient.ini", "w") as f:
    transient.write(f)
```

Quit Spyder completely before relying on these edits if Spyder is running (it may overwrite on exit).

## Spyder vs Cursor vs terminal

| Environment | How it picks Python | User action |
|-------------|---------------------|-------------|
| Bash/zsh | `source .venv/bin/activate` or explicit `.venv/bin/python` | Activate per shell |
| Cursor / VS Code notebook | Kernel picker / status bar "Connected to .venv" | Select `.venv` kernel |
| Spyder | Preferences → Python interpreter / config files | Point at `.venv/bin/python` + matching kernels |

These three do not share activation state.

## Pip / notebook pitfalls

| Context | Correct | Wrong |
|---------|---------|-------|
| Terminal with venv active | `pip install pkg` | system `pip` without activate |
| Notebook / IPython cell | `!pip install pkg` or `%pip install pkg` | bare `pip install pkg` → `SyntaxError` |
| System Python on Ubuntu | create venv, install there | `pip install --break-system-packages` |

Prefer `%pip` inside IPython/Spyder console when installing into the **current** kernel environment.

## Log locations

- `/tmp/spyder-<username>/kernel-*.stderr` — kernel startup failures
- `/tmp/spyder-err*.txt`, `/tmp/spyder-launch.err` — launch noise
- Spyder internal history: `~/.config/spyder-py3/history*.py`

When console is blank, read the newest `kernel-*.stderr` first.

## Recommended project hygiene

```gitignore
.venv/
```

Optional `requirements.txt` (file, not a directory):

```text
networkx
matplotlib
spyder-kernels==2.5.*
```

Pin `spyder-kernels` to the Spyder major in use on that machine.

## Quick verify commands

```bash
# Package location
.venv/bin/python -c "import networkx; print(networkx.__file__)"

# Which pip
.venv/bin/pip show networkx | sed -n '1,3p;/^Location/p'

# Kernel import smoke test
.venv/bin/python -c "import spyder_kernels; print(spyder_kernels.__version__)"
```

Inside Spyder after switch:

```python
import sys, spyder_kernels
print(sys.executable)
print(spyder_kernels.__version__)
```
