Dex,
I have a git repository at https://github.com/sealablab/AgentOS-GHDL-Gen

Like many of my repositories, I have a top level .obsidian directory, and I routinely treat the entire repository as a both an obsidian vault, and a vscode (etc) 'workspace'

I utilize obsidian for keeping the documentation up to date and consistent.

## The problem
My problem: I have an (aspirational) workflow which is, almost working. 

## The current state
I often want to 
1) edit .md files inside the vault on my iPad 
2) link to existing .py files from .md 

At present, I utilize:
- Obsidian Sync

The advantages: Simple, reliable, consistent
the workflow: On my desktop i switch between different feature branches, then
- obsidian sync pushes these filesystem changes to my ipad 
- ipad updates quickly (although perhaps, jarringly) to the filesystem changes
Changes I make on my iPad magically appear inside the desktop app
I commit them, merge them, etc, from laptop

This actually works pretty well. Minor issues with the .py files we just discussed aside.


# [hello](hello.py)

[hello2.py](./hello2.py)


---
```
2025-11-15 11:48 - Fully synced
2025-11-15 11:54 - Uploading file forge-platform/forge-platform-models/hello2.py
2025-11-15 11:54 - Upload complete forge-platform/forge-platform-models/hello2.py
2025-11-15 11:54 - Fully synced
2025-11-15 11:54 - Uploading file forge-platform/forge-platform-models/hello2.py
2025-11-15 11:54 - Upload complete forge-platform/forge-platform-models/hello2.py
```

[hello3.txt](hello3.txt)


[hello4.py.md](hello4.py.md)
