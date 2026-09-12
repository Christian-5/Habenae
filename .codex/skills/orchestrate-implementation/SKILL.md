---
name: orchestrate-implementation
description: Internal Habenae workflow for coordinating the complete implementation lifecycle of one accepted story. Invoke only through the developer_orchestrator agent.
---

# Orchestrate Implementation

Deliver one accepted Habenae story as a traceable product-code change by
coordinating the specialist agents.

## Qualify and prepare

- Read `AGENTS.md`, the supplied story directory's `story.md` and
  `collaboration.md`, and only linked or directly relevant context.
- Require a current, implementable story estimated below `13`.
- Choose `branch`, `base_ref`, and the optional relative path, then invoke
  `$create-story-worktree`. Record the worktree references, plus
  `implement-story` and the required agent names, before product changes.
- Do not add this internal skill or any other specialist skill to the story's
  `skills` field.
- Require `collaboration.md` to exist. Preserve it for the whole lifecycle and
  never recreate, truncate, or delete it after agents have contributed.

## Keep context packets lean

When delegating to a specialist agent:

- Pass file paths and section references, not pasted file content. The
  specialist reads them directly under its own skill's context boundary; do
  not read a file yourself only to paste it into the specialist's task.
- Order each packet with stable, shared material first — the story-directory,
  `story.md`, `collaboration.md`, `PROJECT.md`, and
  `docs/project/architecture.md` paths — followed by what is specific to this
  task. Do not paste prior findings: the specialist reads them from the shared
  journal. Do not repeat `AGENTS.md`; the specialist does not need it.
- State only the task's boundary and required inputs. Do not restate rules
  already written in the specialist's own skill.

## Scale specialist delegation to the estimate

Read the story's `story_points` before delegating and pick the matching tier.
Every tier still ends with an independent `code_reviewer` review; only the
design and development delegation change.

- **`1`**: skip `architecture_designer`, `software_developer`, and
  `test_engineer`. Implement the fix directly under the same constraints
  `$develop-story` and `$test-story` would apply — read
  `docs/project/architecture.md`, `docs/project/documentation/conventions.md`,
  and `docs/project/documentation/testing.md` first, make the smallest
  coherent change, add or adjust only the tests needed for durable coverage,
  and run focused checks. Then run phase 6 below.
- **`2` or `3`**: skip `architecture_designer` only; the scope is already
  understood at this size. Start at phase 3, asking `software_developer` to
  invoke `$develop-story` directly from the story, its acceptance criteria,
  and existing ADRs.
- **`5` or `8`**: run every phase below in order.

Record which tier applied and why in the Orchestration section of
`collaboration.md`. Recalling a
specialist for a correction (see below) may still call an agent that the tier
otherwise skips; that does not change the story's tier for later phases.

## Coordinate the phases

Run the phases below in order for the current tier, and pass each agent only
the context its task needs:

1. Ask `architecture_designer` to invoke `$design-story` and return an
   evidence-based design recorded in the Architecture section of
   `collaboration.md`. Check it against the story and existing ADRs.
   Skipped at tier `1` and `2`/`3`.
2. Decide whether the design requires a specification, product documentation,
   or a project ADR. Invoke `$write-project-knowledge` for each required
   artifact. Stop for user acceptance when a new durable architectural
   decision cannot be inferred from an existing accepted ADR.
3. Ask `software_developer` to invoke `$develop-story` with the approved design
   from the shared journal and implement the bounded product change, recording
   its handoff in the Development section. At tier `1`, perform this step
   directly and write the same section instead of delegating.
4. Ask `test_engineer` to invoke `$test-story` with the resulting diff and
   produce acceptance evidence in the Tests section. At tier `1`, this is
   already covered by the direct implementation in phase 3 and must still be
   noted there.
5. Invoke `$write-project-knowledge` again when the verified implementation
   changes the current product documentation, completes validation details in
   a specification or ADR, or when `software_developer` or `test_engineer`
   reported a verified convention missing from
   `docs/project/documentation/conventions.md` or `testing.md`.
6. Ask `code_reviewer` to invoke `$review-story` only after implementation,
   tests, and required documentation are available. It records findings in the
   Review section. Run this phase at every tier without exception.

For a correctable issue, recall the responsible agent (or, at tier `1`,
correct the change directly) with a narrow assignment and rerun affected
downstream phases. Escalate a material scope, product, or architecture
decision to the user.

## Own traceability and delivery

- Be the only agent that edits `story.md` or moves the Habenae story directory.
  Specialist agents may edit only their assigned section of
  `collaboration.md`.
- Use the Orchestration section of `collaboration.md` for phase status,
  decisions, recalls, blockers, and final handoff without rewriting specialist
  entries.
- At tier `1`, you are also the only agent that edits product code, under the
  same worktree, scope, and commit constraints `$develop-story` and
  `$test-story` would otherwise enforce.
- Keep normative intent and final evidence in `story.md`. Keep phase findings,
  decisions, handoffs, and review discussion in `collaboration.md`. Do not
  duplicate or paste verbose logs between the two files.
- Link every created or updated specification and project ADR from the story.
- Preserve unrelated and pre-existing changes in both repositories.
- Commit verified product code first, record its SHA, then move the entire
  story directory—including `collaboration.md`—to `past` and commit Habenae
  separately.
- Do not remove the worktree automatically; report when removal is safe.

Stop without claiming completion for an unaccepted story, estimate of `13`,
unsafe repository state, missing authority, failed mandatory evidence, or an
unresolved blocking review finding.

Return the story identifier, phase summaries, changed product files,
validation evidence, review findings and resolutions, product and Habenae
SHAs, and any blocker or follow-up.
