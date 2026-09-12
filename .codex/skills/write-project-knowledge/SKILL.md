---
name: write-project-knowledge
description: Internal Habenae workflow for writing or updating product documentation, specifications, and project ADRs during story implementation. Invoke only through the implementation orchestrator.
---

# Write Project Knowledge

Write only the artifact required by the orchestrator:

- **Documentation** under `docs/project/` describes the product's current,
  valid behavior or architecture. Keep it task-oriented, concise, and aligned
  with the verified implementation. Record a newly verified coding or test
  convention in `docs/project/documentation/conventions.md` or `testing.md`
  under its existing heading, replacing any statement it supersedes rather
  than accumulating both.
- **Specification** under `specifications/` defines expected product behavior
  independently of its implementation. State scope, rules, constraints, and
  verifiable outcomes; link the related story and ADRs.
- **Project ADR** under `docs/project/architecture/adr/` records a durable
  architectural decision. Start from `docs/templates/adr.md`; explain context,
  decision, considered alternatives, consequences, and validation. Never
  rewrite an accepted ADR—create a superseding ADR instead.

Use repository-relative links and keep each normative fact in one place.
Reference it elsewhere instead of duplicating it. Do not document assumptions
as decisions or claim behavior that has not been verified. Keep Habenae
orchestrator documentation out of `docs/project/`.

Return the files created or updated, what changed, and any missing decision or
evidence. Do not edit the story; the orchestrator records the references.
