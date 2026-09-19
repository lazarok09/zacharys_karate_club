# AGENTS.md — Zachary's Karate Club

Guide for humans and coding agents configuring this repo on **WSL2 / Ubuntu** with a project **venv**, **Cursor**, and optional **Spyder**.

## What this project is

Social-network analysis notebook/script around NetworkX's `karate_club_graph()`:

| File | Role |
|------|------|
| `main.py` | Primary script (Spyder `# %%` cells / Cursor) |
| `main.ipynb` | Notebook variant |
| `requirements.txt` | Python deps for the project venv |
| `.cursor/skills/spyder-wsl-venv/` | Skill for Spyder + WSL2 + venv diagnosis |

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
# or open main.py / main.ipynb in Cursor or Spyder and run cells
```

Typical imports: `networkx`, `matplotlib.pyplot`.

## Agent checklist for this repo

```
- [ ] .venv exists and is selected in Cursor
- [ ] pip install -r requirements.txt succeeded inside .venv
- [ ] Do not pip into /usr/bin/python3
- [ ] Spyder only after spyder-kernels 2.5.* is in .venv (Spyder 5)
- [ ] If Spyder dies, --revert-spyder before more preference thrashing
- [ ] Prefer editing main.py cells; keep changes minimal and match existing style
```

## Config file map (Spyder on this host)

| Path | Purpose |
|------|---------|
| `~/.config/spyder-py3/config/spyder.ini` | `main_interpreter.custom` / `default` |
| `~/.config/spyder-py3/config/transient.ini` | `executable`, `custom_interpreter` |
| `.vscode/settings.json` | Cursor/VS Code interpreter |
| `.gitignore` | ignores `.venv/`, `.spyproject` |

Selecting a custom path while `custom = False` leaves Spyder on system Python — a common silent failure. See the skill for the exact keys.
