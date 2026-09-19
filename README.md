<h1 align="center"> Covering all the basics of social network analysis </h1>




<figure align="center">

<img width="1468" height="1211" alt="A graph describing the connections between nodes and it's edges using Karate's club nodes without the leader output (read the script)" src="https://github.com/user-attachments/assets/d28575d2-b6ac-4d05-a32a-819a3c4b3adc" />

<figcaption align="center">
Karate's club nodes without the leader 
</figcaption>
  
</div>

<hr />
 

<h2>Concepts</h2>

- [x]  **Nodes and edges** 
- [x]  **Degree** and degree distribution
- [x]  **Density**
- [x]  **Paths and shortest paths**
- [x]  **Connected components**
- [ ]  **Clustering coefficient**
- [x]  **Centrality**
- [x]  Degree
- [x]  Betweenness
- [ ]  Closeness
- [ ]  **Communities and factions**
- [ ]  **Modularity**
- [ ]  **Greedy modularity detection**

## Quick start (from the repo root)

```bash
cd /home/lazarok/github/zacharys_karate_club
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
python main.py
```

Or with the project helper (venv + Spyder-compatible `spyder-kernels`):

```bash
bash .cursor/skills/spyder-wsl-venv/scripts/setup-spyder-venv.sh .
source .venv/bin/activate
pip install -r requirements.txt
```

### Zed + Jupyter (optional)

Register the project venv as a Jupyter kernel (already covered by `requirements.txt` → `ipykernel`):

```bash
source .venv/bin/activate
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

Project kernel pick lives in [`.zed/settings.json`](.zed/settings.json). Native `.ipynb` in Zed still needs preview flags + `LOCAL_NOTEBOOK_DEV=1` (Windows user env when Zed is a Windows app). Open this repo as a **WSL** workspace so the Linux kernel resolves.

Full Cursor / Spyder / Zed setup: see [`AGENTS.md`](AGENTS.md). Zed skill: [`.cursor/skills/zed-jupyter/SKILL.md`](.cursor/skills/zed-jupyter/SKILL.md).

### What is gitignored

| Path | Ignore? | Why |
|------|---------|-----|
| `.venv/` | yes | Local virtualenv; recreate with the steps above |
| `.spyproject/` | **yes** | Spyder per-machine IDE prefs (workspace, encoding). Not shared source — keep ignored |
| `.zed/` | **no** | Shared Zed project settings (kernel selection); commit `.zed/settings.json` |

## Sources

- https://networkx.org/documentation/stable/index.html
- https://en.wikipedia.org/wiki/Zachary%27s_karate_club
