# Codex skills

Habenae stores executable, project-scoped Codex skills under
`.codex/skills/<name>/`. The stable skill identifier is the `name` in
`SKILL.md`; stories use that same value in their `skills` field.

Invoke a skill explicitly by mentioning it in the Codex prompt. For example:

```text
$user-story Formalise le besoin de réinitialiser un mot de passe expiré.
$technical-story Formalise la réorganisation du module de facturation.
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
