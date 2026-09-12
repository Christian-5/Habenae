---
name: user-story
description: Create or refine a Habenae user story when the user asks to formalize a product need. Write explicit rationale, verifiable acceptance criteria, and a justified story-point estimate without implementing it.
---

# User Story

Turn product intent into a reviewable Habenae user story before implementation
begins.

## Load only the required context

1. Read `AGENTS.md`, then `PROJECT.md`.
2. Read `stories/README.md` and `stories/templates/user-story.md`.
3. Search story identifiers and titles across `stories/future/`,
   `stories/current/`, and `stories/past/` to detect the next identifier and
   possible duplicates.
4. Read only specifications or decisions directly relevant to the expressed
   need.

Do not inspect or modify the product repository under `product/`. Creating a story
does not authorize implementation.

## Shape the story

Capture the following from the user's request and available context:

- the persona or beneficiary;
- the capability or outcome they need;
- the value, problem, or risk that explains why the need matters;
- known constraints, exclusions, and dependencies;
- observable acceptance criteria;
- uncertainty, complexity, and dependencies that affect the estimate.

Make reasonable, visible assumptions when the missing detail does not change
the story materially. Ask one focused question only when a missing choice would
substantially change the intent, scope, or acceptance criteria.

Write the description so a future contributor understands the problem, its
context, why it matters, and the expected behavior. Keep implementation design
out of the description unless it is already a product constraint.

Write acceptance criteria as independently verifiable outcomes. Use
Given/When/Then when it makes the behavior clearer. Cover the main successful
outcome and only the edge, error, permission, or quality cases relevant to this
story.

## Estimate in story points

Choose one value from `1, 2, 3, 5, 8, 13` by considering scope, complexity,
uncertainty, dependencies, and validation effort together:

- `1`: tiny, well understood, and isolated;
- `2`: small with limited variation;
- `3`: moderate and understood;
- `5`: several behaviors or a meaningful integration;
- `8`: broad, uncertain, or dependency-heavy;
- `13`: too large or uncertain for safe delivery as one story.

Record the value in `story_points` and explain the main factors in the
`Estimation` section. When the estimate is `13`, recommend splitting the story
and identify sensible boundaries, while still producing the requested draft.

## Create or update the artifact

For a new story:

1. Allocate the next unused `US-####` identifier across every lifecycle
   directory.
2. Use a short lowercase hyphenated slug in the filename.
3. Copy the repository template and populate every relevant field.
4. Default to `stories/future/user/` and `status: future`. Use
   `stories/current/user/` only when the user explicitly accepts or starts the
   work.
5. Leave code repository, branch, worktree, and commit fields `null`; those are
   execution references populated later.

When refining an existing story, preserve its identifier and lifecycle. Change
only fields supported by the request or necessary for internal consistency.

Do not invent specifications, ADRs, agents, or skills. Link only resources that
exist and are materially relevant.

## Verify and report

Before finishing, verify that:

- the identifier is unique and matches the heading and filename;
- frontmatter dates and lifecycle status are consistent;
- the Intent, Description, Acceptance criteria, Out of scope, and Estimation
  sections contain no template placeholders;
- every acceptance criterion can be checked without interpreting vague terms;
- the story-point value uses the documented scale and has a rationale;
- no file under `product/` changed.

Return the story path, its identifier, its estimate, and any assumptions or
open decisions. Do not begin implementation.
