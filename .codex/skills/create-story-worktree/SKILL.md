---
name: create-story-worktree
description: Internal Habenae workflow for creating the dedicated product-code worktree of one accepted story with bin/habenae. Invoke only through the implementation orchestrator.
---

# Create Story Worktree

Create or resolve the dedicated product-code worktree for the supplied current
story.

1. Read the story fields `id`, `branch`, `base_ref`, and `worktree`.
2. Run `bin/habenae doctor` and stop if the product repository is not
   initialized.
3. Run `bin/habenae data list` to avoid duplicating an existing branch or
   worktree.
4. If the story already identifies a valid dedicated worktree for its branch,
   return it without creating another one.
5. Otherwise, require or derive a branch from the story identifier and slug:
   use `feature/<id>-<slug>` for a user story and
   `chore/<id>-<slug>` for a technical story. Use the story's `base_ref` when
   present; otherwise use `origin/HEAD`.
6. Create it only with:

   ```text
   bin/habenae data add <branch> <base_ref> <relative-path>
   ```

   Keep `<relative-path>` equal to the branch unless the story already defines
   another safe path relative to `data/`.
7. Run `bin/habenae data list` again and verify the resulting branch and
   absolute worktree path.

Do not initialize the product repository, edit the story, modify product code,
remove a worktree, or invoke Git worktree commands directly. Stop on an
ambiguous existing branch/path, invalid story state, dirty conflicting
worktree, or failed `bin/habenae` command.

Return the exact `branch`, resolved `base_ref`, worktree path relative to
Habenae, absolute worktree path, whether it was created or reused, and the
verification command result. The orchestrator records these values in the
story.
