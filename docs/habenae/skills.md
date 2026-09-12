# Codex skills

Habenae stores executable, project-scoped Codex skills under
`.codex/skills/<name>/`. The stable skill identifier is the `name` in
`SKILL.md`; stories use that same value in their `skills` field.

Invoke a skill explicitly by mentioning it in the Codex prompt. For example:

```text
$user-story Formalise le besoin de réinitialiser un mot de passe expiré.
$technical-story Formalise la réorganisation du module de facturation.
$implement-story Implémente la story courante sélectionnée.
```

Codex may also select a skill automatically when the request matches its
description. `agents/openai.yaml` supplies the display metadata and the default
prompt shown by the Codex interface.

The top-level `skills/` directory contains authoring guidance and a template.
It is intentionally outside the executable discovery directory so an
unfinished template is never exposed as a usable skill.

## User story skill

The `user-story` skill creates or refines a user story without implementing it.
It defaults new stories to `stories/future/user/` and produces:

- an intent naming the beneficiary, capability, and value;
- a description of the problem, context, motivation, and expected behavior;
- verifiable acceptance criteria;
- explicit exclusions and dependencies;
- a justified estimate on the `1, 2, 3, 5, 8, 13` story-point scale.

An estimate of `13` signals that the story should be split before delivery.

## Technical story skill

The `technical-story` skill creates or refines a technical story without
implementing it. It targets refactoring, code reorganization, and internal
simplification that preserve product behavior while making later development
safer or easier. It defaults new stories to `stories/future/technical/` and
produces:

- a description of the current technical friction, risk, and timing;
- a target technical state and an explicit behavior boundary;
- verifiable acceptance criteria tied to repository evidence;
- explicit constraints, exclusions, migration concerns, and validation needs;
- a justified estimate on the `1, 2, 3, 5, 8, 13` story-point scale.

Feature behavior remains in user stories. An estimate of `13` signals that the
technical work should be split before delivery.

## Implementation skill

The `implement-story` skill is the primary delivery entry point for an accepted
user or technical story. It delegates lifecycle ownership to the
`developer_orchestrator` agent, which coordinates four narrow specialists in
order: architecture and design, development, tests, then independent review.

Each custom agent is intentionally thin and invokes one internal role skill:

- `developer_orchestrator` invokes `$orchestrate-implementation`;
- `architecture_designer` invokes `$design-story`;
- `software_developer` invokes `$develop-story`;
- `test_engineer` invokes `$test-story`;
- `code_reviewer` invokes `$review-story`.

Before delegating the specialist phases, `$orchestrate-implementation` invokes
the internal `$create-story-worktree` skill. The orchestrator chooses the
arguments; the skill only runs `bin/habenae data add` and returns its result.

The orchestrator invokes `$write-project-knowledge` when a story requires
product documentation, a specification, or a project ADR. This internal skill
keeps the three artifacts distinct: documentation describes the verified
current state, specifications define expected behavior independently of code,
and ADRs preserve durable architectural decisions and their consequences.

These internal skills set `allow_implicit_invocation: false`. They remain
explicitly callable by their owning agent but are not selected automatically
from a user request and must not be listed in story metadata. Only
`implement-story` is the public implementation skill referenced by a story.

Specialists work from context packets and return structured action and evidence
reports. Only the orchestrator edits the Habenae story, records the execution
trail, manages lifecycle transitions, and coordinates the independent commits
between the product repository and Habenae. Both story templates provide a
four-phase `Execution log` for concise specialist action summaries; detailed
commands and acceptance evidence remain in `Validation`.

The implementation skill refuses future stories, stories estimated at `13`,
and stories whose acceptance boundary or repository state is unsafe. Newly
added custom agents are discovered when a new Codex session starts.
