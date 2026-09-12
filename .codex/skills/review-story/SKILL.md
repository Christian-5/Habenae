---
name: review-story
description: Internal Habenae workflow for independently reviewing a story implementation after tests are available. Invoke only through the code_reviewer agent.
---

# Review Story

Independently determine whether the supplied product diff is correct, safe,
scoped, maintainable, and supported by sufficient evidence.

- Inspect relevant code directly using the story, acceptance criteria,
  approved design, complete diff, test report, linked ADRs, and worktree path.
- Report findings first, ordered by severity, with precise file and line
  references, impact, and a concrete remediation direction.
- Check correctness, regressions, security and data risks, compatibility, scope
  adherence, design consistency, test quality, and acceptance coverage.
- Explicitly state when no blocking finding remains, then list residual risks
  or missing evidence.

This role is read-only. Do not edit files, run destructive commands, commit, or
update the story. Do not expand the story into discretionary refactoring.
Distinguish blocking findings from non-blocking suggestions and stop when
required context or evidence is unavailable.
