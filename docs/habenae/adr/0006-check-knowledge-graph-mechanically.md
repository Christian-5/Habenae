---
id: ADR-0006
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Check the knowledge graph mechanically

## Context

Several invariants stated in `AGENTS.md`, `docs/habenae/custom-agents.md`, and
`docs/habenae/skills.md` are critical but only enforced by the discipline of
whichever agent executes the relevant skill: unique story, agent, and ADR
identifiers; a story's `agents`/`skills` fields resolving to an existing
definition and never naming an internal skill; an unfinished `.toml` or
`SKILL.md` template never being registered as a complete definition; and a
consistent `supersedes`/`superseded_by` pairing between ADRs. `bin/habenae
doctor` verifies the product repository's integrity but not this knowledge
graph, so a violation currently surfaces only if an agent's own "verify before
finishing" step catches it — a check whose reliability depends on the LLM that
performs it, run after the same session already produced the violation.

## Decision

Add `bin/habenae_knowledge.py`, a dependency-light Python 3 (standard library
only) script that mechanically checks:

- every `.codex/agents/*.toml` and `.codex/skills/*/SKILL.md` parses, declares
  its required fields, and does not match the unfinished-template boilerplate;
- agent and skill `name` values are unique and match their filename or
  directory;
- every internal skill's `agents/openai.yaml` sets
  `allow_implicit_invocation: false`, and every public skill's `default_prompt`
  mentions its own `$name`;
- every story's `id` is unique and consistent with its filename, heading, and
  lifecycle directory, its `story_points` sits on the documented scale, its
  `future`/`past` execution-reference fields match the lifecycle contract, and
  its `agents`/`skills`/`specifications`/`project_adrs`/`habenae_adrs`
  references all resolve, with no internal skill listed;
- ADR identifiers are unique per registry, and `supersedes`/`superseded_by`
  pairs reference each other consistently in both directions.

Expose it as `./bin/habenae doctor --knowledge`, which requires `python3` only
when this flag is used; the default `doctor` keeps its existing `git`-only
requirement. Findings that indicate a broken invariant are reported as `FAIL`
and make the command exit non-zero; an agent or skill that no story or
`docs/habenae/` page yet references is reported as `INFO` rather than `FAIL`,
since `docs/habenae/custom-agents.md` explicitly allows a documented future
use with no story reference yet.

## Considered options

- **Rely on each skill's own "verify before finishing" step, as before** —
  requires no new tooling, but the check's reliability depends on the
  executing LLM and runs only inside the session that may have introduced the
  violation.
- **A mechanical Python 3 checker exposed through `bin/habenae doctor
  --knowledge`, as decided** — independent of any LLM's diligence, reusable
  from any session or a future CI job, and colocated with the existing
  `doctor` mental model.
- **A mechanical checker requiring PyYAML or another third-party package** —
  more general YAML parsing, but adds a dependency not guaranteed present
  wherever `bin/habenae` runs; the frontmatter this repository uses is a flat
  subset that a small dependency-free parser already covers.

## Consequences

- Identifier collisions, dangling references, unfinished templates registered
  as real definitions, and inconsistent ADR supersession links are now
  detectable without trusting the agent that last touched the file.
- `bin/habenae` gains a second required tool, `python3`, but only when
  `--knowledge` is requested; the default `doctor` invocation is unaffected.
- No CI currently runs this repository's checks, since no Git remote or CI
  provider is configured yet; `--knowledge` is run manually or from a local
  hook until one exists. Wiring it into CI is a follow-up, not part of this
  decision.
- The checker assumes `specifications`, `project_adrs`, and `habenae_adrs`
  frontmatter fields hold repository-relative paths; `stories/README.md` now
  states this explicitly so the assumption stays documented rather than
  implicit in the checker's code.

## Validation

- `./bin/habenae doctor --knowledge` exits `0` and reports only `OK`/`INFO`
  lines against this repository's current state.
- `tests/habenae-knowledge.sh` copies the repository's knowledge files into a
  temporary directory and asserts: the clean copy passes; an unfinished agent
  template is rejected; a story referencing an unknown agent is rejected; and
  two ADR files sharing a numeric prefix are rejected as a duplicate id.
