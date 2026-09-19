---
name: zed-jupyter
description: >-
  Set up and diagnose Zed + Jupyter (REPL and .ipynb) on WSL2 with a project
  venv and registered ipykernel. Use when the user mentions Zed, Jupyter,
  ipykernel, kernelspec, LOCAL_NOTEBOOK_DEV, .ipynb in Zed, REPL cells, or
  notebooks opening as raw JSON.
---

# Zed + Jupyter (WSL2 + project venv)

Zed's REPL uses Jupyter kernels. Native `.ipynb` editing is still preview and
needs both a **feature flag** and **`LOCAL_NOTEBOOK_DEV=1`**. On this machine
Zed is a **Windows** app; the project and kernel live in **WSL**.

For this repo's full walkthrough, see [AGENTS.md](../../../AGENTS.md).

## Hard rules

1. Install `ipykernel` into the **project `.venv`**, never system Python.
2. Register a named kernelspec so Zed can pick it reliably (`myenv` here).
3. Open the repo as a **WSL workspace** in Zed so Linux kernels resolve.
4. After changing Windows user env vars, **fully quit and reopen Zed**.
5. If `.ipynb` shows raw JSON, the preview gate is incomplete — check env + flags.

## This repo's expected setup

| Piece | Expected |
|-------|----------|
| Venv Python | `.../zacharys_karate_club/.venv/bin/python` |
| Kernel name | `myenv` |
| Display name | `Python (myenv)` |
| Kernelspec | `~/.local/share/jupyter/kernels/myenv` |
| Project Zed settings | `.zed/settings.json` → `jupyter.kernel_selections.python = myenv` |
| User Zed settings (Windows) | `%APPDATA%\Zed\settings.json` |
| Notebook preview env | Windows user env `LOCAL_NOTEBOOK_DEV=1` |

## Safe setup workflow

```
- [ ] 1. Create .venv and pip install -r requirements.txt (includes ipykernel)
- [ ] 2. Register kernelspec myenv from .venv
- [ ] 3. Add .zed/settings.json kernel selection
- [ ] 4. Enable notebooks feature_flags in Zed user settings
- [ ] 5. Set LOCAL_NOTEBOOK_DEV=1 (Windows user env when Zed is Windows)
- [ ] 6. Fully quit + reopen Zed; open project via WSL
- [ ] 7. repl: refresh kernelspecs; pick Python (myenv)
```

### 1–2. Venv + kernelspec

```bash
cd /home/lazarok/github/zacharys_karate_club
source .venv/bin/activate
pip install -r requirements.txt   # includes ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
jupyter kernelspec list
# myenv must point at .../zacharys_karate_club/.venv/bin/python
```

### 3. Project settings

`.zed/settings.json`:

```json
{
  "jupyter": {
    "kernel_selections": {
      "python": "myenv"
    }
  }
}
```

### 4–5. User Zed settings + env (Windows Zed)

In `%APPDATA%\Zed\settings.json` merge:

```json
{
  "feature_flags": {
    "tabular-data-preview": "on",
    "notebooks": "on"
  },
  "jupyter": {
    "kernel_selections": {
      "python": "myenv"
    }
  }
}
```

Set user env (PowerShell), then **fully restart Zed**:

```powershell
[Environment]::SetEnvironmentVariable('LOCAL_NOTEBOOK_DEV','1','User')
```

Or launch once: `$env:LOCAL_NOTEBOOK_DEV=1; zed`

### 6–7. Use it

| File | How to run |
|------|------------|
| `main.py` with `# %%` | `repl: run` (default `ctrl-shift-enter`) |
| `main.ipynb` | Notebook UI after preview flags + env |

Commands: `repl: refresh kernelspecs`, `repl: sessions`, `toolchain: select`.

## Decision tree

```
Symptom?
├─ .ipynb opens as raw JSON
│  → LOCAL_NOTEBOOK_DEV unset for the Zed process, and/or feature_flags.notebooks off
│  → Set both; fully quit Zed; reopen
│
├─ Kernel missing / wrong Python
│  → Re-register from .venv; refresh kernelspecs
│  → Confirm kernel.json argv is .venv/bin/python
│
├─ Works in Cursor/terminal, fails in Zed
│  → Open WSL remote workspace; Windows-local kernel won't see WSL .venv
│
├─ REPL runs but plots / notebook preview odd
│  → Preview is WIP; # %% REPL in main.py is the stable path
│
└─ ModuleNotFoundError inside kernel
   → Deps missing in .venv; pip install -r requirements.txt in that venv
```

## Diagnosis checklist (agent)

```bash
# Kernel registration
.venv/bin/python -c "import ipykernel, sys; print(sys.executable, ipykernel.__version__)"
jupyter kernelspec list
cat ~/.local/share/jupyter/kernels/myenv/kernel.json

# Project Zed config
cat .zed/settings.json

# Windows Zed user settings + env (from WSL)
cat /mnt/c/Users/*/AppData/Roaming/Zed/settings.json 2>/dev/null | head -80
powershell.exe -NoProfile -Command \
  "[Environment]::GetEnvironmentVariable('LOCAL_NOTEBOOK_DEV','User')"
```

## What not to do

- Do not register the kernel with Windows Python while the project runs in WSL.
- Do not expect `source .venv/bin/activate` alone to change Zed's kernel.
- Do not skip the full Zed restart after setting `LOCAL_NOTEBOOK_DEV`.
- Do not confuse Cursor's notebook kernel picker with Zed's REPL kernel picker.

## Extra detail

- Paths, incident notes, verify commands: [reference.md](reference.md)
