# AGENTS.md — Zachary's Karate Club

Guide for humans and coding agents configuring this repo on **WSL2 / Ubuntu** with a project **venv**, **Cursor**, optional **Spyder**, and optional **Zed + Jupyter**.

## What this project is

Social-network analysis notebook/script around NetworkX's `karate_club_graph()`:

| File | Role |
|------|------|
| `main.py` | Primary script (`# %%` cells / Cursor / Zed REPL / Spyder) |
| `main.ipynb` | Notebook variant (Cursor / Zed preview) |
| `requirements.txt` | Python deps for the project venv (`ipykernel`, `jupyter`, …) |
| `.zed/settings.json` | Zed project kernel selection (`myenv`) |
| `.cursor/skills/spyder-wsl-venv/` | Skill for Spyder + WSL2 + venv diagnosis |
| `.cursor/skills/zed-jupyter/` | Skill for Zed + Jupyter / REPL / `.ipynb` preview |

## One-time setup (recommended)

From the repo root:

```bash
cd /home/lazarok/github/zacharys_karate_club
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

Or use the project skill helper (creates venv + matching `spyder-kernels`):

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh .
source .venv/bin/activate
pip install -r requirements.txt
```

Confirm:

```bash
which python
# .../zacharys_karate_club/.venv/bin/python

python -c "import networkx, matplotlib; print('ok', networkx.__version__)"
```

`.venv/` is gitignored. Recreate it on any new machine with the steps above.

## Cursor / VS Code

Workspace setting (already in repo):

```json
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
```

After creating `.venv`:

1. Command Palette → **Python: Select Interpreter**
2. Choose `.venv/bin/python`
3. For `main.ipynb`, pick the same kernel in the notebook kernel picker

Status bar should show something like **Connected to .venv**.

### Notebook `pip` gotcha

In a Python cell, bare `pip install ...` is a `SyntaxError`. Use:

```python
%pip install -r requirements.txt
```

or install from a terminal with the venv active.

## Zed + Jupyter (optional, Windows Zed + WSL project)

Zed's REPL uses Jupyter kernels. This repo registers the venv as kernel **`myenv`** (display name **Python (myenv)**).

### One-time kernel registration

With the project venv active (after `pip install -r requirements.txt`):

```bash
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
jupyter kernelspec list
# myenv → .../zacharys_karate_club/.venv/bin/python
```

### Project + user config

| Piece | Expected |
|-------|----------|
| `.zed/settings.json` | `jupyter.kernel_selections.python = "myenv"` |
| `%APPDATA%\Zed\settings.json` | `feature_flags.notebooks` / `tabular-data-preview` = `"on"`; same kernel selection |
| Windows user env | `LOCAL_NOTEBOOK_DEV=1` (needed for native `.ipynb` UI; full Zed restart after setting) |

Open this repo as a **WSL** workspace in Zed so Linux kernelspecs resolve. Then:

1. Command palette → **`repl: refresh kernelspecs`**
2. Pick **Python (myenv)** if prompted
3. Run `main.py` `# %%` cells with **`repl: run`** (`ctrl-shift-enter`), or open `main.ipynb`

If `.ipynb` shows raw JSON, the preview gate is incomplete (env and/or feature flags). Stable path: `# %%` REPL in `main.py`.

### Agent skill

When diagnosing Zed / Jupyter / kernel / `.ipynb` preview issues, agents should follow:

`.cursor/skills/zed-jupyter/SKILL.md`

Extra detail: `.cursor/skills/zed-jupyter/reference.md`

## Spyder (optional, apt Spyder 5.x on WSL)

**Activating the venv in a terminal does not change Spyder.**

This machine pattern (from setup incidents here):

| Component | Expected |
|-----------|----------|
| Spyder | 5.5.1 (system apt) |
| Venv `spyder-kernels` | `2.5.*` (pinned in `requirements.txt`) |
| Interpreter path | `/home/lazarok/github/zacharys_karate_club/.venv/bin/python` |

### Point Spyder at the venv (safe order)

1. Ensure deps + kernels are installed (`pip install -r requirements.txt`).
2. Prefer the helper (checks kernel major before switching):

   ```bash
   bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh --point .
   ```

3. Or UI: **Tools → Preferences → Python interpreter** → use  
   `.../zacharys_karate_club/.venv/bin/python`
4. **Fully quit and reopen Spyder** (restart kernel alone is not always enough).
5. Verify in the Spyder console:

   ```python
   import sys
   print(sys.executable)
   # must end with .../zacharys_karate_club/.venv/bin/python
   import networkx as nx
   ```

### If Spyder console is blank / nothing runs

Kernels mismatch or bad custom interpreter. Revert first:

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh --revert-spyder
```

Fully quit Spyder, reopen (system Python). Then reinstall `spyder-kernels==2.5.*` in `.venv` and `--point` again.

Do **not** use `pip install --break-system-packages` on system Python (PEP 668).

### Agent skill

When diagnosing Spyder / venv / `ModuleNotFoundError` / blank console, agents should follow:

`.cursor/skills/spyder-wsl-venv/SKILL.md`

Extra detail: `.cursor/skills/spyder-wsl-venv/reference.md`

## Run the analysis

With venv active:

```bash
python main.py
# or open main.py / main.ipynb in Cursor, Zed, or Spyder and run cells
```

Typical imports: `networkx`, `matplotlib.pyplot`.

## Agent checklist for this repo

```
- [ ] .venv exists and is selected in Cursor
- [ ] pip install -r requirements.txt succeeded inside .venv
- [ ] Do not pip into /usr/bin/python3
- [ ] Spyder only after spyder-kernels 2.5.* is in .venv (Spyder 5)
- [ ] If Spyder dies, --revert-spyder before more preference thrashing
- [ ] Zed: myenv kernelspec registered; .zed/settings.json present; WSL workspace
- [ ] Zed .ipynb preview: LOCAL_NOTEBOOK_DEV=1 + feature_flags.notebooks=on (full restart)
- [ ] Prefer editing main.py cells; keep changes minimal and match existing style
```

## Config file map (this host)

| Path | Purpose |
|------|---------|
| `~/.config/spyder-py3/config/spyder.ini` | `main_interpreter.custom` / `default` |
| `~/.config/spyder-py3/config/transient.ini` | `executable`, `custom_interpreter` |
| `.vscode/settings.json` | Cursor/VS Code interpreter |
| `.zed/settings.json` | Zed Jupyter kernel selection (`myenv`) |
| `%APPDATA%\Zed\settings.json` | Zed user prefs + notebook feature flags (Windows) |
| `~/.local/share/jupyter/kernels/myenv/` | Registered Jupyter kernelspec → `.venv` |
| `.gitignore` | ignores `.venv/`, `.spyproject` (not `.zed/`) |

Selecting a custom Spyder path while `custom = False` leaves Spyder on system Python — a common silent failure. See the Spyder skill for the exact keys.
