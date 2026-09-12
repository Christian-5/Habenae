---
name: technical-story
description: Create or refine a Habenae technical story for refactoring, code reorganization, or internal simplification. Define the technical motivation, verifiable acceptance criteria, and a justified story-point estimate without implementing the change.
---

# Technical Story

Turn an internal engineering need into a reviewable Habenae technical story
that makes later product development safer or simpler.

## Confirm that the need is technical

Use a technical story when the primary outcome is an internal improvement such
as clearer module boundaries, reduced duplication or coupling, safer extension
points, simpler tests, easier maintenance, or code reorganization that
preserves product behavior.

If the requested outcome adds or changes observable user behavior, propose a
user story or a separate user story for that behavior. Do not hide feature work
inside a refactoring story.

## Load only the required context

1. Read `AGENTS.md`, then `PROJECT.md`.
2. Read `stories/README.md` and `stories/templates/technical-story.md`.
3. Search story identifiers and titles across `stories/future/`,
   `stories/current/`, and `stories/past/` to find the next identifier and
   possible duplicates.
4. Read only the project specifications, ADRs, documentation, and product code
   needed to understand the affected area and existing constraints.

Inspection of the product repository under `data/` is read-only at this stage.
Do not create a worktree, change code, or begin the refactoring while drafting
the story.

## Explain why the change matters

Describe the current technical state with concrete evidence when available.
Explain the friction, risk, or repeated cost it creates and name the future
development activities that should become simpler. Avoid unsupported claims
such as "cleaner", "better", or "more maintainable".

Define the expected technical outcome as a target state rather than a list of
edits. Record known behavior, compatibility, dependency, performance, data, or
deployment constraints that must remain true.

Capture assumptions explicitly. Ask one focused question only when missing
information would materially change the target boundary, the safety
constraints, or the estimate.

## Write verifiable acceptance criteria

Each criterion must describe evidence that can be checked after implementation.
Select only criteria relevant to the requested change, such as:

- preserved externally observable behavior and passing regression tests;
- an explicit dependency direction or module ownership boundary;
- removal of identified duplication or obsolete paths;
- a named extension or maintenance operation becoming localized;
- stable public interfaces, migrations, or compatibility guarantees;
- updated tests, architecture documentation, or decision records;
- measurable performance, build-time, complexity, or reliability limits.

State exact modules, interfaces, commands, or thresholds only when supported by
the repository or the user's request. Do not invent metrics merely to make a
criterion look precise.

## Estimate in story points

Choose one value from `1, 2, 3, 5, 8, 13` by considering the affected surface,
coupling, migration risk, uncertainty, dependencies, and validation effort:

- `1`: tiny, isolated, and mechanically safe;
- `2`: small, understood, with limited callers;
- `3`: moderate scope with known boundaries;
- `5`: multiple modules or a meaningful compatibility concern;
- `8`: broad coupling, migration work, or substantial uncertainty;
- `13`: too broad or uncertain for safe delivery as one story.

Record the value in `story_points` and justify the main factors in the
`Estimation` section. For `13`, recommend splitting the story and identify
coherent boundaries, while still producing the requested draft.

## Create or update the artifact

For a new technical story:

1. Allocate the next unused `TS-####` identifier across every lifecycle
   directory.
2. Use a short lowercase hyphenated filename slug.
3. Copy `stories/templates/technical-story.md` and populate every relevant
   field.
4. Default to `stories/future/technical/` and `status: future`. Use
   `stories/current/technical/` only when the user explicitly accepts or starts
   the work.
5. Leave branch, worktree, and commit fields `null`; execution references are
   populated only when implementation begins.

When refining an existing story, preserve its identifier and lifecycle. Change
only fields supported by the request or required for internal consistency.

Link only specifications, ADRs, agents, and skills that exist and materially
affect the work. Propose a project ADR when the target introduces or changes a
durable architectural boundary; do not create that ADR while drafting unless
the user also requests it.

## Verify and report

Before finishing, verify that:

- the identifier is unique and matches the heading and filename;
- frontmatter dates, lifecycle status, and `motivation` are consistent;
- Description, Expected technical outcome, Constraints, Acceptance criteria,
  Out of scope, Approach, and Estimation contain no template placeholders;
- the future-development benefit is concrete and the product behavior boundary
  is clear;
- every acceptance criterion has observable evidence;
- the estimate uses the documented scale and has a rationale;
- no file under `data/` changed.

Return the story path, identifier, estimate, affected technical area, and any
assumptions or open decisions. Do not begin implementation.
