---
id: ADR-0004
status: accepted
date: 2026-09-12
owners: []
supersedes: [ADR-0001]
superseded_by: null
---

# Name the local product repository `product/`

## Context

ADR-0001 separates Habenae from the software repository and originally names
its local directory `data/`. That name suggests application data and the term
"data plane" obscures that the directory contains product source code and Git
worktrees.

## Decision

Keep the two independent Git repositories defined by ADR-0001, but store the
local product repository under `product/`:

- `product/.bare` contains its shared Git history;
- `product/<branch>` contains its worktrees;
- the Habenae repository ignores all of `product/`.

Expose repository operations through `bin/habenae product`. The `data` command
and `data/` path are no longer part of the current interface.

## Considered options

- **`product/`** — identifies the functional boundary without exposing the Git
  implementation as the primary concept.
- **`worktrees/`** — technically precise for working directories, but
  misleading because the bare repository also lives there.
- **`data/`** — short, but easily confused with product or execution data.

## Consequences

- Commands and documentation use product-oriented vocabulary.
- Existing local installations must move or recreate `data/` as `product/`.
- Stories continue to reference a concrete worktree path and code commit.

## Validation

- `git check-ignore product/example` confirms that Habenae ignores `product/`.
- `tests/habenae-cli.sh` verifies `habenae product` and its worktree lifecycle.
- Current documentation and executable skills contain no functional reference
  to `habenae data` or `data/` outside the superseded ADR-0001.
