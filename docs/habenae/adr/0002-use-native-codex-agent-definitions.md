---
id: ADR-0002
status: accepted
date: 2026-09-12
owners: []
supersedes: []
superseded_by: null
---

# Use native Codex agent definitions

## Context

Habenae needs specialized roles that Codex can discover and invoke as
subagents. A top-level `agents/` directory containing Markdown role descriptions
is useful to humans but is not the project-scoped custom-agent format recognized
by Codex.

## Decision

Store every executable custom-agent definition as an independent TOML file
under `.codex/agents/`. Each definition contains the three required fields:
`name`, `description`, and `developer_instructions`.

Use the agent `name` as the identifier in story metadata. Keep authoring rules
and the reusable template in
[`docs/habenae/custom-agents.md`](../custom-agents.md), outside the discovery
directory, so an unfinished template cannot be registered as an agent.

## Considered options

- **Native `.codex/agents/*.toml` files** — directly discoverable by Codex and
  scoped to the Habenae project.
- **Top-level Markdown files under `agents/`** — readable documentation but not
  executable Codex agent definitions.
- **Personal agents under `~/.codex/agents/`** — reusable by one person but not
  versioned with Habenae or shared consistently with collaborators.

## Consequences

- Agent definitions can be committed and reviewed with Habenae.
- Stories reference a stable agent name instead of a documentation filename.
- The project remains tied to Codex's current custom-agent TOML contract; future
  format changes may require a migration.
- No placeholder `.toml` file may be stored in the discovery directory.

## Validation

- Every agent file is located under `.codex/agents/`.
- Every agent file defines `name`, `description`, and
  `developer_instructions`.
- Every name used by a story resolves to exactly one agent definition.
