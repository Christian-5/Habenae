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

Require the orchestrator to use the four specialist agents named below and to
return the final delivery report:

1. `architecture_designer` for analysis and an implementation design;
2. `software_developer` for the scoped production change;
3. `test_engineer` for tests and acceptance evidence;
4. `code_reviewer` for an independent, read-only review.

The phases are ordered. A specialist may be recalled with a narrowly scoped
correction, but no phase is skipped silently. Only the orchestrator updates the
Habenae story; specialists report their actions and evidence to it.

## Preserve repository boundaries

- Habenae contains orchestration and story evidence; product changes belong
  only in the worktree under `data/` declared by the story.
- Use `bin/habenae data add` to create a missing dedicated worktree and record
  its branch, base reference, and path before product code changes.
- Never place agentic files in `data/` and never add `data/` to Habenae Git.
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
