---
name: create-story-worktree
description: Internal Habenae workflow for creating the dedicated product-code worktree of one accepted story with bin/habenae. Invoke only through the implementation orchestrator.
---

# Create Story Worktree

Receive `branch`, `base_ref`, and optionally `relative_path` from the
orchestrator. Create the worktree with:

```text
bin/habenae data add <branch> <base_ref> [relative_path]
```

Do not choose the values, edit the story, or modify product code. Return the
command output or its error to the orchestrator.
