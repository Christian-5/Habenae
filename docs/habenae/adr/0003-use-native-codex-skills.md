---
id: ADR-0003
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Use project-scoped Codex skill definitions

## Context

Habenae needs reusable procedures that Codex can discover and invoke directly
from a task. The existing top-level `skills/` directory provides an authoring
template, but a template alone does not register an executable project skill or
expose a skill mention such as `$user-story`.

## Decision

Store executable Codex skills as independent directories under
`.codex/skills/`. Every skill has a `SKILL.md` with a stable `name` and a
discriminating `description`. A skill may add `agents/openai.yaml` for its
display name, short description, and default invocation prompt.

Use the frontmatter `name` as the identifier in story metadata and as the
explicit Codex mention. Keep general authoring documentation and unfinished
templates under the top-level `skills/` directory so Codex cannot register a
placeholder as a working skill.

## Considered options

- **Project-scoped definitions under `.codex/skills/`** — versioned with
  Habenae and directly available to collaborators working in the repository.
- **Templates only under `skills/`** — readable and reusable for authors, but
  not registered as Codex commands.
- **Personal skills outside the repository** — available to one user but not
  shared or reviewed with Habenae.

## Consequences

- A project skill can be invoked explicitly with `$<skill-name>`.
- Skill behavior and its user-facing invocation metadata evolve in the same
  reviewable history.
- The top-level `skills/` directory remains documentation and scaffolding, not
  an executable discovery location.
- Habenae depends on Codex's project skill contract and may require a migration
  if that contract changes.

## Validation

- Every executable skill is located under `.codex/skills/<name>/`.
- Every `SKILL.md` defines a matching `name` and a scoped `description`.
- Every `agents/openai.yaml` default prompt mentions its skill as
  `$<skill-name>`.
- Every name used by a story resolves to exactly one executable skill.
