# Zed + Jupyter — reference

## Incident notes (zacharys_karate_club, 2026-09)

What was set up on this host:

1. Project venv at `.venv` already had `ipykernel` via `requirements.txt`.
2. Registered user kernelspec:
   - name: `myenv`
   - display: `Python (myenv)`
   - argv Python: `/home/lazarok/github/zacharys_karate_club/.venv/bin/python`
   - path: `~/.local/share/jupyter/kernels/myenv`
3. Zed is installed under Windows (`AppData\Local\Programs\Zed`); settings live in `%APPDATA%\Zed\settings.json`.
4. Enabled preview notebooks with `feature_flags.notebooks` / `tabular-data-preview` and Windows user env `LOCAL_NOTEBOOK_DEV=1`.
5. Project `.zed/settings.json` selects kernel `myenv` for Python.

Lesson: on WSL projects, Zed must open the **WSL** workspace so it sees the Linux kernelspec; Windows-local kernels will not match this `.venv`.

## Config file map

| Path | Purpose |
|------|---------|
| `.zed/settings.json` | Project kernel selection (`jupyter.kernel_selections`) |
| `%APPDATA%\Zed\settings.json` | User Zed prefs + `feature_flags` (Windows host) |
| `~/.local/share/jupyter/kernels/myenv/kernel.json` | Kernelspec pointing at `.venv/bin/python` |
| `.venv/share/jupyter/kernels/python3/` | Default env-local `python3` kernelspec (also fine) |
| Windows user env `LOCAL_NOTEBOOK_DEV` | Required for native `.ipynb` UI (preview) |

WSL path to Windows Zed settings (this machine):

`/mnt/c/Users/lazar/AppData/Roaming/Zed/settings.json`

## Verify kernelspec

```bash
cat ~/.local/share/jupyter/kernels/myenv/kernel.json
```

Expected shape:

```json
{
  "argv": [
    "/home/lazarok/github/zacharys_karate_club/.venv/bin/python",
    "-Xfrozen_modules=off",
    "-m",
    "ipykernel_launcher",
    "-f",
    "{connection_file}"
  ],
  "display_name": "Python (myenv)",
  "language": "python"
}
```

Re-register if the path is wrong:

```bash
.venv/bin/python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

## Zed commands

| Command | Use |
|---------|-----|
| `repl: run` | Run selection / `# %%` cell (`ctrl-shift-enter`) |
| `repl: clear outputs` | Clear inline REPL outputs |
| `repl: refresh kernelspecs` | After installing/registering a kernel |
| `repl: sessions` | List active sessions / available kernels |
| `toolchain: select` | Align Python toolchain with the env |

## Official docs

- REPL / kernels: https://zed.dev/docs/repl
- Preview `.ipynb` still needs `LOCAL_NOTEBOOK_DEV=1` + `feature_flags.notebooks` (community-confirmed as of mid-2026)
