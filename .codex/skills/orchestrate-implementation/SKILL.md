---
name: orchestrate-implementation
description: Internal Habenae workflow for coordinating the complete implementation lifecycle of one accepted story. Invoke only through the developer_orchestrator agent.
---

# Orchestrate Implementation

Deliver one accepted Habenae story as a traceable product-code change by
coordinating the specialist agents.

## Qualify and prepare

- Read `AGENTS.md`, the supplied story, and only its linked or directly
  relevant context.
- Require a current, implementable story estimated below `13`.
- Choose `branch`, `base_ref`, and the optional relative path, then invoke
  `$create-story-worktree`. Record the worktree references, plus
  `implement-story` and the required agent names, before product changes.
- Do not add this internal skill or any other specialist skill to the story's
  `skills` field.

## Coordinate the phases

Run these phases in order and pass each agent only the context its task needs:

1. Ask `architecture_designer` to invoke `$design-story` and return an
   evidence-based design. Check it against the story and existing ADRs.
2. Decide whether the design requires a specification, product documentation,
   or a project ADR. Invoke `$write-project-knowledge` for each required
   artifact. Stop for user acceptance when a new durable architectural
   decision cannot be inferred from an existing accepted ADR.
3. Ask `software_developer` to invoke `$develop-story` with the approved design
   and implement the bounded product change.
4. Ask `test_engineer` to invoke `$test-story` with the resulting diff and
   produce acceptance evidence.
5. Invoke `$write-project-knowledge` again when the verified implementation
   changes the current product documentation or completes validation details
   in a specification or ADR.
6. Ask `code_reviewer` to invoke `$review-story` only after implementation,
   tests, and required documentation are available.

For a correctable issue, recall the responsible agent with a narrow assignment
and rerun affected downstream phases. Escalate a material scope, product, or
architecture decision to the user.

## Own traceability and delivery

- Be the only agent that edits or moves the Habenae story.
- Record design and decisions in the planning section, phase summaries in
  `Execution log`, evidence in `Validation`, and review results and follow-up
  debt in `Closure log`. Do not paste verbose logs.
- Link every created or updated specification and project ADR from the story.
- Preserve unrelated and pre-existing changes in both repositories.
- Commit verified product code first, record its SHA, then move the story to
  `past` and commit Habenae separately.
- Do not remove the worktree automatically; report when removal is safe.

Stop without claiming completion for an unaccepted story, estimate of `13`,
unsafe repository state, missing authority, failed mandatory evidence, or an
unresolved blocking review finding.

Return the story identifier, phase summaries, changed product files,
validation evidence, review findings and resolutions, product and Habenae
SHAs, and any blocker or follow-up.
