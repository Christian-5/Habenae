---
id: ADR-0001
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: ADR-0004
---

# Separate agentic orchestration from product code

## Context

Habenae must centralize agents, skills, specifications, stories, documentation,
and decisions without imposing these artifacts on the repository of the software
being developed. Multiple code branches must also support parallel work.

## Decision

Use two independent Git repositories:

- a normal Git repository at the root for Habenae;
- a bare clone of the code repository under `data/.bare`, exposed through
  sibling worktrees under `data/`.

The Habenae repository ignores all of `data/`. Stories link the two histories
through explicit branch, worktree, and commit references.

## Considered options

- **Two independent repositories with worktrees** — clear separation, parallel
  work, and a locally shared code history.
- **Git submodule** — provides a strong version relationship but couples Habenae
  to a code revision and exposes orchestration mechanics in the workflow.
- **Agentic artifacts in the code repository** — initially simple but pollutes
  the product with tool-specific and agent-specific conventions.

## Consequences

- The application repository remains usable without Habenae or agentic files.
- Multiple branches share Git objects and can remain open in parallel.
- Changes across the two repositories are not atomic, so the story must retain
  their cross-references.
- `data/` must be rebuilt with `bin/habenae data init` after every new Habenae
  clone.

## Validation

- `git check-ignore data/example` confirms that the root repository ignores
  `data/`.
- `tests/habenae-cli.sh` verifies initialization and the worktree lifecycle
  against a temporary repository.
