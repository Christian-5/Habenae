#!/usr/bin/env python3
"""Mechanical integrity checks for the Habenae knowledge graph.

Validates invariants stated in AGENTS.md, docs/habenae/*.md, and the story
templates that would otherwise depend only on an agent's self-discipline:
unique identifiers, dangling references between stories/agents/skills/ADRs,
unfinished templates registered as executable definitions, and bidirectional
ADR supersession links.

Invoked via `bin/habenae doctor --knowledge`. Exit code is non-zero if any
check fails.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

OK, FAIL, INFO = "OK  ", "FAIL", "INFO"

ADR_STATUSES = {"proposed", "accepted", "rejected"}
STORY_POINT_SCALE = {"1", "2", "3", "5", "8", "13"}
TEMPLATE_AGENT_DESCRIPTION = "Use this agent when a narrowly defined responsibility is needed."
TEMPLATE_AGENT_MISSION = "Mission:\n- Produce one bounded and verifiable outcome."
TEMPLATE_SKILL_NAME = "skill-name"
TEMPLATE_SKILL_DESCRIPTION = "When to use this skill and what outcome it produces."


class Report:
    def __init__(self) -> None:
        self.failed = False

    def ok(self, msg: str) -> None:
        print(f"{OK}{msg}")

    def fail(self, msg: str) -> None:
        print(f"{FAIL} {msg}", file=sys.stderr)
        self.failed = True

    def info(self, msg: str) -> None:
        print(f"{INFO} {msg}")


def _unquote(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value in ("null", "~", ""):
        return None
    return value


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the flat YAML frontmatter used by stories, skills, and ADRs.

    Supports plain scalars, inline lists (`key: [a, b]`), and block lists
    (`key:` followed by `  - item` lines). Nested mappings are not needed by
    any file in this repository and are not supported.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text
    body = "\n".join(lines[end + 1 :])
    data: dict = {}
    fm = lines[1:end]
    i = 0
    while i < len(fm):
        line = fm[i]
        if not line.strip():
            i += 1
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2).strip()
        if value == "":
            items = []
            j = i + 1
            while j < len(fm) and re.match(r"^\s*-\s*(.*)$", fm[j]):
                items.append(_unquote(re.match(r"^\s*-\s*(.*)$", fm[j]).group(1)))
                j += 1
            data[key] = items
            i = j
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_unquote(x) for x in inner.split(",")] if inner else []
        else:
            data[key] = _unquote(value)
        i += 1
    return data, body


def check_agents(root: Path, report: Report) -> dict[str, Path]:
    agents: dict[str, Path] = {}
    agents_dir = root / ".codex" / "agents"
    for path in sorted(agents_dir.glob("*.toml")):
        try:
            with open(path, "rb") as handle:
                data = tomllib.load(handle)
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            report.fail(f"agent {path.relative_to(root)}: invalid TOML ({exc})")
            continue

        missing = [k for k in ("name", "description", "developer_instructions") if not data.get(k)]
        if missing:
            report.fail(f"agent {path.relative_to(root)}: missing or empty {', '.join(missing)}")
            continue

        name = data["name"]
        if name != path.stem:
            report.fail(f"agent {path.relative_to(root)}: name '{name}' does not match filename")

        if data["description"].strip() == TEMPLATE_AGENT_DESCRIPTION or TEMPLATE_AGENT_MISSION in data["developer_instructions"]:
            report.fail(f"agent {path.relative_to(root)}: looks like the unfinished template; rename to *.toml.example or complete it")
            continue

        if name in agents:
            report.fail(f"agent name '{name}' is defined twice: {agents[name].relative_to(root)} and {path.relative_to(root)}")
        else:
            agents[name] = path

    if agents:
        report.ok(f"agents: {len(agents)} valid definition(s) under .codex/agents/")
    return agents


def check_skills(root: Path, report: Report) -> tuple[dict[str, Path], set[str]]:
    skills: dict[str, Path] = {}
    internal: set[str] = set()
    skills_dir = root / ".codex" / "skills"
    for entry in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            report.fail(f"skill directory {entry.relative_to(root)}: missing SKILL.md")
            continue

        data, _ = parse_frontmatter(skill_md.read_text())
        name, description = data.get("name"), data.get("description")
        if not name or not description:
            report.fail(f"{skill_md.relative_to(root)}: missing name or description in frontmatter")
            continue

        if name != entry.name:
            report.fail(f"{skill_md.relative_to(root)}: name '{name}' does not match directory '{entry.name}'")

        if name == TEMPLATE_SKILL_NAME or description.strip() == TEMPLATE_SKILL_DESCRIPTION:
            report.fail(f"{skill_md.relative_to(root)}: looks like the unfinished template; keep it under skills/ or complete it")
            continue

        if name in skills:
            report.fail(f"skill name '{name}' is defined twice: {skills[name].relative_to(root)} and {skill_md.relative_to(root)}")
            continue
        skills[name] = skill_md

        is_internal = "Invoke only through" in description
        openai_yaml = entry / "agents" / "openai.yaml"
        raw = openai_yaml.read_text() if openai_yaml.is_file() else ""

        if is_internal:
            internal.add(name)
            allow_match = re.search(r"allow_implicit_invocation:\s*(true|false)", raw)
            if not openai_yaml.is_file() or not allow_match or allow_match.group(1) != "false":
                report.fail(f"internal skill '{name}': agents/openai.yaml must set allow_implicit_invocation: false")
        else:
            prompt_match = re.search(r"default_prompt:\s*(.+)", raw)
            if prompt_match and f"${name}" not in prompt_match.group(1):
                report.fail(f"skill '{name}': agents/openai.yaml default_prompt does not mention ${name}")

    if skills:
        report.ok(f"skills: {len(skills)} valid definition(s) under .codex/skills/ ({len(internal)} internal)")
    return skills, internal


def _story_directories(root: Path, report: Report):
    for lifecycle in ("future", "current", "past"):
        for kind, prefix in (("user", "US-"), ("technical", "TS-")):
            directory = root / "stories" / lifecycle / kind
            if not directory.is_dir():
                continue
            for path in sorted(directory.glob("*.md")):
                report.fail(
                    f"story {path.relative_to(root)}: stories must be directories "
                    "containing story.md and collaboration.md"
                )
            for story_dir in sorted(path for path in directory.iterdir() if path.is_dir()):
                yield lifecycle, prefix, story_dir


def check_stories(root: Path, report: Report, agents: dict, skills: dict, internal: set[str]) -> set[str]:
    seen_ids: dict[str, Path] = {}
    referenced_agents: set[str] = set()
    referenced_skills: set[str] = set()
    count = 0

    for lifecycle, prefix, story_dir in _story_directories(root, report):
        path = story_dir / "story.md"
        collaboration = story_dir / "collaboration.md"
        story_rel = story_dir.relative_to(root)
        count += 1

        if not path.is_file():
            report.fail(f"story {story_rel}: missing story.md")
            continue
        if not collaboration.is_file():
            report.fail(f"story {story_rel}: missing collaboration.md")
        else:
            collaboration_text = collaboration.read_text()
            for section in ("Orchestration", "Architecture", "Development", "Tests", "Review"):
                if not re.search(rf"^##\s+{section}\s*$", collaboration_text, re.MULTILINE):
                    report.fail(f"story {story_rel}: collaboration.md is missing the '{section}' section")

        data, body = parse_frontmatter(path.read_text())
        story_id = data.get("id")
        rel = path.relative_to(root)

        if not story_id or not re.fullmatch(rf"{prefix}\d{{4}}", story_id):
            report.fail(f"story {rel}: missing or malformed id (expected {prefix}NNNN)")
            continue

        if story_id in seen_ids:
            report.fail(f"duplicate story id '{story_id}': {seen_ids[story_id].relative_to(root)} and {rel}")
        else:
            seen_ids[story_id] = path

        if not story_dir.name.startswith(story_id):
            report.fail(f"story {rel}: directory does not start with its id '{story_id}'")

        if not re.search(rf"^#\s+{re.escape(story_id)}\b", body, re.MULTILINE):
            report.fail(f"story {rel}: heading does not start with '# {story_id}'")

        if data.get("status") != lifecycle:
            report.fail(f"story {rel}: status '{data.get('status')}' does not match its '{lifecycle}/' directory")

        points = data.get("story_points")
        if points is not None and str(points) not in STORY_POINT_SCALE:
            report.fail(f"story {rel}: story_points '{points}' is outside the 1,2,3,5,8,13 scale")

        if lifecycle == "future":
            for field in ("branch", "base_ref", "worktree", "code_commit"):
                if data.get(field) is not None:
                    report.fail(f"story {rel}: '{field}' must be null while status is future")
        if lifecycle == "past":
            for field in ("branch", "base_ref", "worktree", "code_commit"):
                if not data.get(field):
                    report.fail(f"story {rel}: '{field}' is required once status is past")

        for name in data.get("agents") or []:
            referenced_agents.add(name)
            if name not in agents:
                report.fail(f"story {rel}: references unknown agent '{name}'")

        for name in data.get("skills") or []:
            referenced_skills.add(name)
            if name not in skills:
                report.fail(f"story {rel}: references unknown skill '{name}'")
            elif name in internal:
                report.fail(f"story {rel}: '{name}' is an internal skill and must not appear in the skills field")

        for field, subdir in (("specifications", "specifications"), ("project_adrs", "docs/project/architecture/adr"), ("habenae_adrs", "docs/habenae/adr")):
            for link in data.get(field) or []:
                if not (root / link).is_file():
                    report.fail(f"story {rel}: '{field}' entry '{link}' does not resolve to a file")

    if count:
        report.ok(f"stories: {count} directories checked, {len(seen_ids)} unique id(s)")
    return referenced_agents | referenced_skills


def check_adr_registry(root: Path, report: Report, relative_dir: str) -> dict[str, dict]:
    directory = root / relative_dir
    adrs: dict[str, dict] = {}
    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        data, _ = parse_frontmatter(path.read_text())
        adr_id, status = data.get("id"), data.get("status")
        rel = path.relative_to(root)

        number_match = re.match(r"(\d{4})-", path.name)
        if not adr_id or not number_match or adr_id != f"ADR-{number_match.group(1)}":
            report.fail(f"{rel}: id '{adr_id}' does not match its filename number")
            continue

        if status not in ADR_STATUSES:
            report.fail(f"{rel}: status '{status}' is not one of {sorted(ADR_STATUSES)}")

        if adr_id in adrs:
            report.fail(f"duplicate ADR id '{adr_id}' in {relative_dir}: {adrs[adr_id]['path'].relative_to(root)} and {rel}")
            continue

        adrs[adr_id] = {
            "path": path,
            "supersedes": [x for x in (data.get("supersedes") or []) if x],
            "superseded_by": data.get("superseded_by"),
        }

    for adr_id, adr in adrs.items():
        rel = adr["path"].relative_to(root)
        if adr["superseded_by"]:
            target = adrs.get(adr["superseded_by"])
            if not target:
                report.fail(f"{rel}: superseded_by '{adr['superseded_by']}' does not exist in {relative_dir}")
            elif adr_id not in target["supersedes"]:
                report.fail(f"{rel}: superseded_by '{adr['superseded_by']}' does not list '{adr_id}' back in its supersedes")
        for predecessor_id in adr["supersedes"]:
            predecessor = adrs.get(predecessor_id)
            if not predecessor:
                report.fail(f"{rel}: supersedes '{predecessor_id}' does not exist in {relative_dir}")
            elif predecessor["superseded_by"] != adr_id:
                report.fail(f"{rel}: '{predecessor_id}' does not record superseded_by '{adr_id}' back")

    if adrs:
        report.ok(f"ADRs: {len(adrs)} valid record(s) under {relative_dir}")
    return adrs


def check_skill_mentions(root: Path, report: Report, skills: dict[str, Path]) -> None:
    sources = [root / "AGENTS.md"]
    sources += sorted((root / "docs" / "habenae").rglob("*.md"))
    sources += sorted((root / ".codex" / "skills").rglob("SKILL.md"))
    text = "\n".join(p.read_text() for p in sources if p.is_file())
    mentioned = set(re.findall(r"\$([a-z][a-z0-9]*-[a-z0-9-]*)", text))
    unknown = sorted(m for m in mentioned if m not in skills)
    for name in unknown:
        report.fail(f"'${name}' is mentioned but does not resolve to a skill under .codex/skills/")
    if mentioned and not unknown:
        report.ok(f"skill mentions: {len(mentioned)} '$name' reference(s) resolve correctly")


def check_phantoms(root: Path, report: Report, agents: dict, skills: dict, referenced: set[str]) -> None:
    prose_sources = [root / "AGENTS.md"]
    prose_sources += sorted((root / "docs" / "habenae").rglob("*.md"))
    text = "\n".join(p.read_text() for p in prose_sources if p.is_file())
    for name in sorted(agents):
        if name not in referenced and not re.search(rf"\b{re.escape(name)}\b", text):
            report.info(f"agent '{name}' is not referenced by any story or documented in docs/habenae/")
    for name in sorted(skills):
        if name not in referenced and not re.search(rf"[$`]{re.escape(name)}\b", text):
            report.info(f"skill '{name}' is not referenced by any story or documented in docs/habenae/")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = args.root.resolve()

    report = Report()
    agents = check_agents(root, report)
    skills, internal = check_skills(root, report)
    referenced = check_stories(root, report, agents, skills, internal)
    check_adr_registry(root, report, "docs/habenae/adr")
    check_adr_registry(root, report, "docs/project/architecture/adr")
    check_skill_mentions(root, report, skills)
    check_phantoms(root, report, agents, skills, referenced)

    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
