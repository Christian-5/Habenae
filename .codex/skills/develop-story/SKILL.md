---
name: develop-story
description: Internal Habenae workflow for implementing an approved story design in its dedicated product worktree. Invoke only through the software_developer agent.
---

# Develop Story

Implement the supplied approved design within the declared product-code
worktree.

- Read `docs/project/architecture.md` before modifying product code. Ensure the
  implementation follows the documented product architecture and report any
  conflict with the approved design to the orchestrator.
- Read only the code and documentation required by the assigned design,
  acceptance criteria, exclusions, and relevant project guidance.
- Make the smallest coherent production-code and directly required
  documentation changes.
- Run focused developer checks appropriate to the touched code.
- Return changed files, design deviations and reasons, commands and results,
  acceptance criteria addressed, residual risks, and remaining testing work.

Modify only the declared product worktree. Never edit the Habenae story,
orchestration repository, or agentic files. Do not commit, change branches,
rewrite unrelated code, or absorb pre-existing changes. Stop for a material
design deviation, missing decision, unsafe repository state, or blocker.
