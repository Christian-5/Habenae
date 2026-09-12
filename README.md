# Habenae

Habenae is an orchestration workspace for agentic software development. It keeps
working knowledge—agents, skills, specifications, stories, documentation, and
decisions—in a Git repository separate from the application code.

Product source code lives under `product/`. This directory is a local container for Git
worktrees and is never versioned by the Habenae repository.

## Quick start

```bash
git init
git add .
git commit -m "chore: initialize Habenae"

./bin/habenae product init <code-repository-url>
./bin/habenae product add feature/my-story
./bin/habenae product list
```

After initializing the code repository, the tree looks like this:

```text
Habenae/
├── AGENTS.md               # canonical Habenae orchestrator
├── CLAUDE.md -> AGENTS.md  # discovery adapter for Claude
├── HABENAE.md              # human-facing entry point
├── PROJECT.md              # project purpose and important links
├── .codex/
│   └── agents/             # project-scoped Codex agent definitions
├── skills/                 # reusable procedures
├── specifications/         # current, future, past
├── stories/                # user stories and technical stories
├── docs/
│   ├── habenae/            # orchestrator architecture and ADRs
│   └── project/            # software documentation and architecture
├── bin/habenae             # code repository management
└── product/                # ignored by Habenae Git
    ├── .bare/              # shared Git history for the code
    ├── .git                # pointer to .bare
    ├── main/               # main branch worktree
    └── feature/...         # other worktrees
```

Agents start with [AGENTS.md](AGENTS.md). The human-facing introduction remains
available in [HABENAE.md](HABENAE.md), while [PROJECT.md](PROJECT.md) defines the
software project. Custom agents follow the
[Codex agent definition standard](docs/habenae/custom-agents.md). Then read
[docs/habenae/worktrees.md](docs/habenae/worktrees.md).
