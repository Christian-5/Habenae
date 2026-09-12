# Codex agent definition standard

Habenae custom agents are project-scoped Codex agents. Executable definitions
live as standalone TOML files under `.codex/agents/`.

This standard follows the official
[Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## File contract

Each `.toml` file must define these fields:

| Field | Purpose |
| --- | --- |
| `name` | Stable identifier used by Codex and by a story's `agents` field. |
| `description` | Selection guidance explaining when this agent should be used. |
| `developer_instructions` | Mission, context, constraints, expected result, and stop conditions. |

Use lowercase `snake_case` for both the filename and `name`, and keep them
identical. The `name` field remains the authoritative identifier.

## Definition template

Create `.codex/agents/<agent_name>.toml` from this template and replace every
placeholder:

```toml
name = "agent_name"
description = "Use this agent when a narrowly defined responsibility is needed."

developer_instructions = """
Mission:
- Produce one bounded and verifiable outcome.

Required context:
- List only the inputs needed to complete the mission.

Expected result:
- Describe the artifact, change, or report to return.

Boundaries:
- Stay within the assigned scope.
- Preserve unrelated work.
- Report missing authority, required decisions, and blockers explicitly.
- Verify the result before completion.
"""
```

## Optional configuration

Codex can also accept session configuration such as `model`,
`model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, and `skills.config` in
an agent definition. Omit these keys by default so the agent inherits the
parent session configuration. Add an override only when the role requires it
and document the reason next to the definition.

Do not keep an unfinished template with a `.toml` extension inside
`.codex/agents/`: Codex may register it as an available agent.

## Authoring checklist

- The agent owns one responsibility, not an entire workflow.
- The description states a concrete selection condition.
- The expected result can be inspected or tested.
- Required inputs are explicit and minimal.
- Allowed actions and scope boundaries are unambiguous.
- Stop conditions cover success, blockers, and decisions requiring a human.
- The agent does not duplicate rules already defined in `AGENTS.md` or a skill.
- At least one story names the agent, or its intended future use is documented.

## Review and activation

1. Review the TOML syntax and every instruction for ambiguity.
2. Confirm that the declared `name` is unique.
3. Add the name to the relevant story's `agents` field.
4. Start a new Codex session so the project-scoped definition is discovered.
5. Delegate a bounded trial task and verify the returned result.
