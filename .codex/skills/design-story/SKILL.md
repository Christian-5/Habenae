---
name: design-story
description: Internal Habenae workflow for producing the architecture and implementation design of one accepted story. Invoke only through the architecture_designer agent.
---

# Design Story

Translate the supplied accepted story into an evidence-based technical design
that a developer can implement safely.

- Read `docs/project/architecture.md` and
  `docs/project/documentation/conventions.md` before inspecting the product
  code. Treat the architecture page as the entry point for the product
  architecture and follow its references that are relevant to the story.
- Use the story, acceptance criteria, exclusions, linked specifications and
  ADRs, and declared product worktree as the context boundary.
- Inspect only relevant product code and documentation.
- Describe current-state findings, proposed component and dependency changes,
  affected interfaces and files, data or migration implications,
  compatibility constraints, implementation sequence, risks, rollback
  considerations, and required tests.
- Map design elements to the acceptance criteria they support and distinguish
  repository evidence from assumptions.
- State whether an existing ADR governs the choice or a new project ADR is
  required.

This is a read-only design role. Do not modify code, tests, stories, or Git
history. Prefer the smallest design satisfying the story. Stop when a durable
architectural choice lacks authority, relevant context is missing, or the
request conflicts with an ADR or acceptance criterion.
