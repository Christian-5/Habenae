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

A story is organized by lifecycle state: `future/`, `current/`, then `past/`.
Its identifier and filename remain stable when its state changes.

The `agents` frontmatter field lists the `name` values of custom Codex agents
defined under `.codex/agents/` according to the
[agent definition standard](../docs/habenae/custom-agents.md). The `skills`
field lists the reusable skills required by the story.

Templates:

- [User story](templates/user-story.md)
- [Technical story](templates/technical-story.md)
