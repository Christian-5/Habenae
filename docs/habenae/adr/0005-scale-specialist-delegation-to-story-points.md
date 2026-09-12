---
id: ADR-0005
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Scale specialist delegation to the story's point estimate

## Context

`$orchestrate-implementation` always ran the same four-phase specialist
pipeline — architecture and design, development, tests, independent review —
regardless of story size. For a `1`-point story, this added four agent hops
and four separate context loads to deliver a change smaller than any single
one of those loads. For a `2`- or `3`-point story, the dedicated design phase
largely repeated reasoning already implied by the story's own definition of
that estimate ("small, understood" or "moderate and understood" in
`user-story` and `technical-story`).

## Decision

Scale specialist delegation in `$orchestrate-implementation` to the story's
`story_points`:

- `1`: the orchestrator implements and tests the change directly, under the
  same worktree, scope, and evidence constraints `$develop-story` and
  `$test-story` would otherwise enforce. It does not delegate to
  `architecture_designer`, `software_developer`, or `test_engineer`.
- `2` or `3`: skip `architecture_designer` only. `software_developer` and
  `test_engineer` are delegated as before.
- `5` or `8`: run the complete four-phase pipeline unchanged.

`code_reviewer` always runs an independent review, regardless of tier. Both
`$orchestrate-implementation` and `implement-story` state the same tiers so
neither drifts from the other.

## Considered options

- **Fixed four-phase pipeline for every story** — maximum specialization and
  independence at every step, but a disproportionate agent-hop and
  context-loading cost for stories the estimation scale already classifies as
  small or well understood.
- **Scale delegation to `story_points`, as decided** — reuses the estimation
  scale already bounding story size instead of introducing a new dimension,
  and keeps the rule verifiable from a field already recorded on every story.
- **Let the orchestrator decide ad hoc whether to skip a phase** — flexible,
  but unverifiable and inconsistent across runs; two stories of the same size
  could be delivered through different pipelines for no recorded reason.

## Consequences

- Small stories close with fewer agent transitions and less duplicated
  context loading.
- `story_points` now governs both scope safety (the existing `13` ceiling) and
  delegation depth, so an inaccurate estimate has a second consequence beyond
  scope risk: a `1`-point story that turns out to be larger loses the design
  and development specialists that would otherwise have caught it earlier.
- Independent review is preserved at every tier, keeping at least one check
  that is never the author of the change.
- `implement-story` and `docs/habenae/skills.md` must be updated together with
  `$orchestrate-implementation` if the tiers change again.

## Validation

- `$orchestrate-implementation` states the tier rule before its phase list;
  `implement-story` names the same scaling next to each of its four agents.
- A `1`-point story's `Execution log` names the orchestrator, not a
  specialist, for architecture and design, development, and tests, while
  still recording an independent review.
- A `2`- or `3`-point story's `Execution log` has no architecture-and-design
  entry from `architecture_designer` while development, tests, and review are
  all delegated and recorded.
- A `5`- or `8`-point story's `Execution log` records all four phases as
  before this decision.
