---
name: test-story
description: Internal Habenae workflow for testing a completed story implementation and producing acceptance evidence. Invoke only through the test_engineer agent.
---

# Test Story

Verify the supplied implementation and add the minimum missing automated tests
needed for durable coverage.

- Read `docs/project/documentation/testing.md` for the product's verified test
  conventions before writing or changing a test.
- Use the acceptance criteria, approved design, implementation summary and
  diff, and declared product worktree.
- Map every acceptance criterion to a test, command, inspection, or other
  concrete evidence.
- Add or adjust tests only when coverage is missing. Run focused checks before
  proportionate regression checks.
- Return test files changed, commands and exact outcomes, acceptance evidence,
  uncovered risks, flaky or environment-dependent results, reproducible
  failure details, and any test convention verified in the suite but missing
  from `docs/project/documentation/testing.md`.

Modify only test code and test-support artifacts in the product worktree.
Never edit production code, the Habenae story, orchestration files, or Git
history. Do not weaken assertions or skip tests to obtain a passing result.
Report product defects to the orchestrator for correction by the developer and
distinguish infrastructure blockers from product failures.
