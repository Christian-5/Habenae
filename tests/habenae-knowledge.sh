#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

COPY="$TEMP_ROOT/habenae"
mkdir -p "$COPY"
cp -R "$PROJECT_ROOT/AGENTS.md" "$PROJECT_ROOT/.codex" "$PROJECT_ROOT/docs" "$PROJECT_ROOT/stories" "$COPY/"

run() {
  python3 "$PROJECT_ROOT/bin/habenae_knowledge.py" --root "$COPY"
}

# The current repository state must pass every check.
run >/dev/null
printf 'clean repository: OK\n'

# A malformed agent (unfinished template copied verbatim) must be rejected.
cat > "$COPY/.codex/agents/broken.toml" <<'EOF'
name = "broken"
description = "Use this agent when a narrowly defined responsibility is needed."

developer_instructions = """
Mission:
- Produce one bounded and verifiable outcome.
"""
EOF
if run >/tmp/habenae-knowledge-out 2>&1; then
  echo "expected failure for unfinished agent template, got success" >&2
  exit 1
fi
grep -q "unfinished template" /tmp/habenae-knowledge-out
rm "$COPY/.codex/agents/broken.toml"
printf 'unfinished agent template rejected: OK\n'

# A flat story file must be rejected.
touch "$COPY/stories/current/user/US-9998-flat.md"
if run >/tmp/habenae-knowledge-out 2>&1; then
  echo "expected failure for flat story file, got success" >&2
  exit 1
fi
grep -q "stories must be directories" /tmp/habenae-knowledge-out
rm "$COPY/stories/current/user/US-9998-flat.md"
printf 'flat story file rejected: OK\n'

# A story directory missing its collaboration journal must be rejected.
mkdir -p "$COPY/stories/future/user/US-0000-missing-journal"
cp "$COPY/stories/templates/user-story.md" \
   "$COPY/stories/future/user/US-0000-missing-journal/story.md"
if run >/tmp/habenae-knowledge-out 2>&1; then
  echo "expected failure for missing collaboration journal, got success" >&2
  exit 1
fi
grep -q "missing collaboration.md" /tmp/habenae-knowledge-out
rm -r "$COPY/stories/future/user/US-0000-missing-journal"
printf 'missing collaboration journal rejected: OK\n'

# A story directory referencing an unknown agent must be rejected.
mkdir -p "$COPY/stories/current/user/US-9999-example"
cp "$COPY/stories/templates/collaboration.md" \
   "$COPY/stories/current/user/US-9999-example/collaboration.md"
cat > "$COPY/stories/current/user/US-9999-example/story.md" <<'EOF'
---
id: US-9999
title: Example
status: current
owners: []
created: 2026-09-12
updated: 2026-09-12
story_points: 1
specifications: []
project_adrs: []
habenae_adrs: []
agents: [does_not_exist]
skills: []
code_repository: null
branch: null
base_ref: null
worktree: null
code_commit: null
---

# US-9999 — Example

## Intent

As a **tester**, I want **coverage** so that **the checker is verified**.
EOF
if run >/tmp/habenae-knowledge-out 2>&1; then
  echo "expected failure for unknown agent reference, got success" >&2
  exit 1
fi
grep -q "unknown agent 'does_not_exist'" /tmp/habenae-knowledge-out
rm -r "$COPY/stories/current/user/US-9999-example"
printf 'dangling agent reference rejected: OK\n'

# Two ADR files sharing the same numeric prefix (and therefore the same id) must be rejected.
cp "$COPY/docs/habenae/adr/0004-name-local-product-repository.md" \
   "$COPY/docs/habenae/adr/0004-duplicate-slug.md"
if run >/tmp/habenae-knowledge-out 2>&1; then
  echo "expected failure for duplicate ADR id, got success" >&2
  exit 1
fi
grep -q "duplicate ADR id 'ADR-0004'" /tmp/habenae-knowledge-out
printf 'duplicate ADR id rejected: OK\n'

printf 'habenae-knowledge: OK\n'
