# Stories

User stories deliver observable value. Technical stories describe a necessary
internal change and explain its indirect value.

Every user story states its intent, describes the problem and expected value,
defines verifiable acceptance criteria, and records a justified estimate using
the `1, 2, 3, 5, 8, 13` story-point scale. An estimate of `13` indicates that
the story should be split before implementation.

A story is organized by lifecycle state: `future/`, `current/`, then `past/`.
Its identifier and filename remain stable when its state changes.

The `agents` frontmatter field lists the `name` values of custom Codex agents
defined under `.codex/agents/` according to the
[agent definition standard](../docs/habenae/custom-agents.md). The `skills`
field lists the reusable skills required by the story.

Templates:

- [User story](templates/user-story.md)
- [Technical story](templates/technical-story.md)
