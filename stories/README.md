# Stories

User stories deliver observable value. Technical stories describe a necessary
internal change and explain its indirect value.

Every story describes why the change matters, defines verifiable acceptance
criteria, and records a justified estimate using the `1, 2, 3, 5, 8, 13`
story-point scale. An estimate of `13` indicates that the story should be split
before implementation.

A technical story identifies the current internal friction or risk, the target
technical state, the behavior boundary to preserve, and the future development
that becomes simpler. Observable product behavior belongs in a user story.

A story is a durable directory organized by lifecycle state: `future/`,
`current/`, then `past/`. Its identifier and directory name remain stable when
its state changes. Every story directory contains:

- `story.md`, the normative intent, criteria, estimate, references, and closure
  evidence;
- `collaboration.md`, the shared journal where orchestration, architecture,
  development, testing, and review leave concise findings for the following
  phases.

The whole directory moves between lifecycle states. `collaboration.md` is part
of the story history and must not be deleted after implementation.

The `agents` frontmatter field lists the `name` values of custom Codex agents
defined under `.codex/agents/` according to the
[agent definition standard](../docs/habenae/custom-agents.md). The `skills`
field lists the reusable skills required by the story; it never names an
internal skill (see [docs/habenae/skills.md](../docs/habenae/skills.md)). The
`specifications`, `project_adrs`, and `habenae_adrs` fields hold
repository-relative paths to the linked files, for example
`docs/habenae/adr/0001-separate-orchestration-and-code.md`.

`./bin/habenae doctor --knowledge` mechanically checks that every one of these
references resolves and that story identifiers are unique; see
[docs/habenae/worktrees.md](../docs/habenae/worktrees.md#check-the-knowledge-graph).

Templates:

- [User story](templates/user-story.md)
- [Technical story](templates/technical-story.md)
- [Agent collaboration journal](templates/collaboration.md)
