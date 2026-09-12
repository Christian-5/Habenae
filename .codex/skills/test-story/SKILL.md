---
name: test-story
description: Internal Habenae workflow for testing a completed story implementation and producing acceptance evidence. Invoke only through the test_engineer agent.
---

# Test Story

Verify the supplied implementation and add the minimum missing automated tests
needed for durable coverage.

- Use the acceptance criteria, approved design, implementation summary and
  diff, test conventions, and declared product worktree.
- Map every acceptance criterion to a test, command, inspection, or other
  concrete evidence.
- Add or adjust tests only when coverage is missing. Run focused checks before
  proportionate regression checks.
- Return test files changed, commands and exact outcomes, acceptance evidence,
  uncovered risks, flaky or environment-dependent results, and reproducible
  failure details.

Modify only test code and test-support artifacts in the product worktree.
Never edit production code, the Habenae story, orchestration files, or Git
history. Do not weaken assertions or skip tests to obtain a passing result.
Report product defects to the orchestrator for correction by the developer and
distinguish infrastructure blockers from product failures.
