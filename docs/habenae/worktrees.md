# Manage the code repository from Habenae

The `bin/habenae` CLI implements the bare clone and worktree model described in
[Git worktree like a boss](https://dev.to/metal3d/git-worktree-like-a-boss-2j1b).

## Initialize `data/`

```bash
./bin/habenae data init git@github.com:organization/project.git
```

The CLI clones the history into `data/.bare`, configures tracking for all remote
branches, detects the default branch, and creates its first worktree. You can
specify the initial branch explicitly:

```bash
./bin/habenae data init <url> develop
```

## Create a worktree

Existing local or remote branch:

```bash
./bin/habenae data add feature/US-0042-authentication
```

New branch created from a selected reference:

```bash
./bin/habenae data add feature/US-0042-authentication origin/main
```

By default, the path matches the branch name. A third argument selects a
different path relative to `data/`:

```bash
./bin/habenae data add feature/US-0042-authentication origin/main work/US-0042
```

## Inspect and clean up

```bash
./bin/habenae data list
./bin/habenae data remove work/US-0042
./bin/habenae data prune
./bin/habenae doctor
```

`remove` uses `git worktree remove` without forcing it, so Git refuses to remove
a worktree with uncommitted changes. Do not delete a worktree directly with
`rm -rf`.
