---
name: implement-story
description: Implement an accepted Habenae user or technical story through a dedicated product-code worktree. Use the developer orchestrator to coordinate architecture, development, tests, review, and story traceability; do not use it to draft or merely estimate a story.
---

# Implement Story

Deliver one accepted story as a traceable product-code change. The primary
agent delegates lifecycle ownership to `developer_orchestrator`; it does not
replace the specialist agents or implement the change itself.

## Select and qualify the story

1. Read `AGENTS.md`, `PROJECT.md`, and `stories/README.md`.
2. Resolve the story from an explicit path or identifier. If none is given,
   select it only when exactly one story exists under `stories/current/`.
3. Require `status: current`, a complete intent or technical outcome,
   verifiable acceptance criteria, and an estimate below `13`.
4. Read only the specifications, project ADRs, skills, and technical
   documentation linked by the story.
5. Stop and report the missing decision when scope, acceptance criteria,
   repository state, or authorization makes safe implementation impossible.

Do not silently promote a future story, split a story, change its product
intent, or implement a story estimated at `13`.

## Delegate orchestration

Delegate the complete execution to the `developer_orchestrator` custom agent.
Provide a compact context packet containing:

- the absolute story path and identifier;
- the linked context paths already qualified;
- the acceptance criteria and explicit exclusions;
- the repository, base reference, branch, and worktree fields;
- relevant user decisions and current repository-state observations.

Pass paths, not pasted file content — `developer_orchestrator` and its
specialists read what they need directly — and list this stable material
before anything specific to this delegation.

The `developer_orchestrator` loads its private `$orchestrate-implementation`
skill. Require it to draw from the specialist agents named below, scaled to
the story's `story_points` estimate, and to return the final delivery report:

1. `architecture_designer`, which loads `$design-story` — stories of `5` or
   `8` points only;
2. `software_developer`, which loads `$develop-story` — stories of `2` points
   or more; the orchestrator implements directly for a `1`-point story;
3. `test_engineer`, which loads `$test-story` — stories of `2` points or more;
   covered by the direct implementation for a `1`-point story;
4. `code_reviewer`, which loads `$review-story` — every story, regardless of
   estimate.

The phases run in order for the applicable tier; no required phase is skipped
silently, and `code_reviewer` always runs. A specialist may be recalled with a
narrowly scoped correction. Only the orchestrator updates the Habenae story;
specialists report their actions and evidence to it.
These internal skills are execution details: do not add them to the story's
`skills` field.

## Preserve repository boundaries

- Habenae contains orchestration and story evidence; product changes belong
  only in the worktree under `product/` declared by the story.
- Use `bin/habenae product add` to create a missing dedicated worktree and record
  its branch, base reference, and path before product code changes.
- Never place agentic files in `product/` and never add `product/` to Habenae Git.
- Preserve unrelated changes. Stop before overwriting ambiguous or conflicting
  user work.
- Commit product code first. Record that SHA in the story, then commit the
  corresponding Habenae evidence separately.

## Completion gate

Do not declare the story complete until the orchestrator reports that:

- every acceptance criterion has concrete evidence;
- appropriate automated checks pass, or each exception is explicit;
- the review has no unresolved blocking finding;
- relevant documentation and ADRs are consistent;
- the story records commands, results, decisions, follow-up debt, and the
  final product-code commit;
- the story has moved to `stories/past/` only after all completion conditions
  are satisfied.

Return the story identifier, worktree and branch, product-code commit, Habenae
commit, validation summary, review outcome, and any remaining non-blocking
follow-up. If delivery stops early, return the completed phases, evidence, and
the exact blocker without claiming completion.
