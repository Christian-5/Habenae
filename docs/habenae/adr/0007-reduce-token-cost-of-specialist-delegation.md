---
id: ADR-0007
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Reduce the token cost of specialist delegation

## Context

Each specialist agent in `$orchestrate-implementation` starts without memory
of the orchestrator's own context. Two costs were not yet addressed by
ADR-0005's tiering: `$design-story` and `$develop-story` each independently
scanned the product code to infer conventions (naming, structure, test
layout) that a prior story had already established, and nothing constrained
how the orchestrator built a specialist's context packet — leaving it free to
paste full file content into a prompt that the specialist's own skill already
instructs it to read directly, loading the same material twice.

## Decision

- Record product conventions once they are verified, instead of re-deriving
  them per story: `docs/project/documentation/conventions.md` for coding
  conventions and `docs/project/documentation/testing.md` for test
  conventions. `$design-story` and `$develop-story` read `conventions.md`
  before inspecting code; `$test-story` reads `testing.md` instead of the
  previously undefined "test conventions". Both skills return any verified
  convention missing from these pages, and `$orchestrate-implementation`
  invokes `$write-project-knowledge` to record it, replacing superseded
  guidance rather than accumulating it.
- `$orchestrate-implementation` states a "Keep context packets lean" rule:
  pass file paths, not pasted content, since the specialist reads them itself
  under its own skill's context boundary; order each packet with stable,
  shared material first (story path, `PROJECT.md`,
  `docs/project/architecture.md`) followed by what is specific to the task;
  and do not restate rules already written in the specialist's own skill.
  `implement-story` states the same rule for its own delegation to
  `developer_orchestrator`.

## Considered options

- **Leave conventions implicit in the code, re-derived each story** — no new
  file to maintain, but the same exploration cost repeats on every
  `$design-story` or `$develop-story` invocation for the life of the product.
- **Record conventions once in `docs/project/documentation/`, as decided** —
  a short page read once costs less than repeatedly re-scanning the codebase,
  and fits the existing `docs/project/documentation/` structure without a new
  concept.
- **Leave context-packet construction unconstrained** — flexible, but nothing
  stopped an orchestrator from pasting large file content that the specialist
  would also read itself, doubling that cost with no benefit.

## Consequences

- A story that verifies a new convention pays a small recording cost once;
  every later story reads a short page instead of re-scanning the code for
  the same fact.
- `conventions.md` and `testing.md` start empty and grow only from verified
  evidence; an orchestrator must still invoke `$write-project-knowledge` to
  keep them current, and a stale, unrecorded convention is only a lost
  optimization, not a correctness risk, since specialists still read the code
  directly when a page section is empty.
- Context packets built by `$orchestrate-implementation` and `implement-story`
  are smaller and do not duplicate content the specialist would read anyway.

## Validation

- `docs/project/documentation/conventions.md` and `testing.md` exist and are
  linked from `docs/project/documentation/README.md`.
- `$design-story`, `$develop-story`, and `$test-story` name the relevant page
  in their required reading and their return contract includes a missing
  convention.
- `$orchestrate-implementation` states the context-packet rule before its
  phase list, and `implement-story` states the same rule for its own
  delegation.
- `./bin/habenae doctor --knowledge` still exits `0` after these changes.
