# Habenae — development orchestrator

This file is the canonical source of agentic guidance for this workspace. Every
agent or automated tool starts here, then loads only the context required for
its task.

## Mission

Turn product intent into a traceable software change:

1. understand the request and its constraints;
2. find or create the corresponding story;
3. load the relevant specifications, ADRs, skills, and agents;
4. work in a dedicated worktree under `data/`;
5. verify the result;
6. update the knowledge base and Git references.

## Boundary between the two repositories

- The **Habenae** repository contains orchestration and knowledge only.
- The **code** repository is installed locally under `data/` with its own Git
  history.
- `data/` must never be added to the Habenae repository, including as a
  submodule.
- No agentic file (`AGENTS.md`, `CLAUDE.md`, skills, prompts, or agent memory)
  may be created in the worktrees under `data/`.
- A story references code through `worktree`, `branch`, `base_ref`, and commit
  SHA fields. Commits in the two repositories are independent.

## Documentation boundary

- `docs/habenae/` documents only the orchestrator, its architecture, mechanisms,
  and decisions.
- `docs/project/` documents only the software being developed, including its
  behavior and architecture.
- Every new page must live in the domain of its primary subject.
- A change that affects both domains produces two linked documents or ADRs so
  that each history can evolve without ambiguity.

## Context loading order

1. `AGENTS.md`;
2. `PROJECT.md`;
3. the active story under `stories/current/`;
4. linked specifications under `specifications/`;
5. relevant project ADRs under `docs/project/architecture/adr/` and, when the
   work affects orchestration, those under `docs/habenae/adr/`;
6. only the skills and custom agents named by the story;
7. relevant technical documentation;
8. code from the worktree declared by the story.

Do not load the whole repository just in case. Context must remain explicit,
minimal, and traceable.

## Custom agent definitions

- Project-scoped Codex agents live in `.codex/agents/` as standalone TOML files.
- Every agent defines `name`, `description`, and `developer_instructions`.
- The `name` is the stable identifier referenced by a story's `agents` field.
- Keep each mission narrow, its expected outcome verifiable, and its boundaries
  explicit.
- Inherit the parent model and execution settings by default. Override them only
  when the role has a documented reason.
- Do not place executable agent definitions in a top-level `agents/` directory.
- Use `.toml.example` for templates so Codex does not register an unfinished
  placeholder as an available agent.

## Codex skill definitions

- Project-scoped executable skills live under `.codex/skills/<name>/`.
- Every skill defines a stable `name` and a discriminating `description` in
  `SKILL.md`.
- Stories reference that `name` in their `skills` field.
- Keep unfinished skill templates under `skills/`, outside the executable
  discovery directory.
- Follow [the Codex skill standard](docs/habenae/skills.md) when creating or
  updating a skill.

## Work lifecycle

- `future/`: qualified work that has not been committed to;
- `current/`: accepted or in-progress work;
- `past/`: completed, abandoned, or superseded work kept for history.

A story moves from `future` to `current` before any code is changed. It moves to
`past` only after its acceptance criteria have been verified and its final
references (`code_commit`, decisions, and documentation) are up to date.

## Execution contract

For every change:

1. assign a stable identifier (`US-####` or `TS-####`);
2. choose a dedicated branch and create it with `bin/habenae data add`;
3. record the worktree path in the story;
4. apply existing ADRs or propose one in the relevant domain registry when the
   decision is structural;
5. keep changes within the story's scope;
6. run validations proportionate to the risk;
7. record results and the code SHA in the story;
8. version the code first, then commit the Habenae update separately.

## Definition of done

Work is complete when:

- the acceptance criteria are satisfied;
- relevant tests and checks pass;
- no sensitive data or local artifacts are versioned;
- related documentation and ADRs are consistent;
- the story contains evidence references and the code commit;
- the worktree can be removed without losing work.

## Conventions

- Normative information has one source of truth. Other files reference it
  instead of copying it.
- Knowledge files use Markdown and relative links.
- Codex custom agent definitions use TOML and live under `.codex/agents/`.
- Executable Codex skills live under `.codex/skills/`; authoring templates live
  under `skills/`.
- Durable software decisions live under `docs/project/architecture/adr/`.
  Orchestrator decisions live under `docs/habenae/adr/`.
- Recommended branch names are `feature/<id>-<slug>`, `fix/<id>-<slug>`, and
  `chore/<id>-<slug>`.
- Secrets, execution logs, and local data stay out of Git.
