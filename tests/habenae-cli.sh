#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEMP_ROOT"' EXIT

SOURCE="$TEMP_ROOT/source"
REMOTE="$TEMP_ROOT/remote.git"
COPY="$TEMP_ROOT/habenae"

mkdir -p "$SOURCE" "$COPY"
git -C "$SOURCE" init -b main >/dev/null
git -C "$SOURCE" config user.name Test
git -C "$SOURCE" config user.email test@example.invalid
printf 'hello\n' > "$SOURCE/README.md"
git -C "$SOURCE" add README.md
git -C "$SOURCE" commit -m initial >/dev/null
git clone --bare "$SOURCE" "$REMOTE" >/dev/null

git -C "$COPY" init -b master >/dev/null
git -C "$COPY" config user.name Test
git -C "$COPY" config user.email test@example.invalid
printf 'harness\n' > "$COPY/HISTORY.md"
git -C "$COPY" add HISTORY.md
git -C "$COPY" commit -m harness >/dev/null
git -C "$COPY" remote add origin "$REMOTE"

mkdir -p "$COPY/bin"
cp "$PROJECT_ROOT/bin/habenae" "$COPY/bin/habenae"
cp "$PROJECT_ROOT/AGENTS.md" "$COPY/AGENTS.md"
cp "$PROJECT_ROOT/PROJECT.md" "$COPY/PROJECT.md"
cp "$PROJECT_ROOT/.gitignore" "$COPY/.gitignore"
chmod +x "$COPY/bin/habenae"

"$COPY/bin/habenae" doctor >/dev/null
"$COPY/bin/habenae" product init "$REMOTE" main >/dev/null
[[ -f "$COPY/product/main/README.md" ]]
"$COPY/bin/habenae" product add feature/TS-0001 origin/main >/dev/null
[[ -f "$COPY/product/feature/TS-0001/README.md" ]]
"$COPY/bin/habenae" product list | grep -q 'feature/TS-0001'
"$COPY/bin/habenae" product remove feature/TS-0001
[[ ! -e "$COPY/product/feature/TS-0001" ]]
"$COPY/bin/habenae" doctor >/dev/null

git -C "$COPY" branch -m master project
"$COPY/bin/habenae" harness rebase "$REMOTE" main >/dev/null
[[ -f "$COPY/README.md" && -f "$COPY/HISTORY.md" ]]

printf 'habenae-cli: OK\n'
