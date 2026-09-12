---
id: ADR-0008
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Store stories as durable collaboration directories

## Context

A single story file can record final evidence, but specialist agents also need
a shared, durable place for design findings, implementation handoffs, test
evidence, and review comments. Returning those details only through agent
messages makes later phases and future audits depend on transient context.

## Decision

Represent every user or technical story as a directory named with its stable
identifier and slug. It contains:

- `story.md`, the normative story definition and final references;
- `collaboration.md`, a shared journal with Orchestration, Architecture,
  Development, Tests, and Review sections.

Each specialist reads earlier sections and edits only its own section. The
orchestrator uses the Orchestration section, alone edits `story.md`, and moves
the complete directory between `future/`, `current/`, and `past/`. The
collaboration journal is retained after implementation.

## Considered options

- **One story file with all execution notes** — compact, but mixes normative
  scope with agent conversation and creates a shared editing hotspot.
- **One directory with a shared collaboration journal** — keeps the story
  authoritative while providing a simple durable handoff space.
- **One file per agent** — isolates writes further, but adds structure that is
  unnecessary while implementation phases remain sequential.

## Consequences

- Story paths now identify directories; the normative document is always
  `<story-directory>/story.md`.
- Story creation, implementation skills, agents, and knowledge checks must use
  the two-file contract.
- Moving a story changes the directory path but retains all implementation
  discussion and evidence.

## Validation

- `bin/habenae doctor --knowledge` rejects flat story files or story
  directories missing either required file.
- `tests/habenae-knowledge.sh` exercises the directory contract.
- The creation and implementation skills consistently distinguish the story
  directory, `story.md`, and `collaboration.md`.
