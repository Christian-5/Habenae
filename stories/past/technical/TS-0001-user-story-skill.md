---
id: TS-0001
title: Créer le skill de rédaction des user stories
status: past
owners: []
created: 2026-09-12
updated: 2026-09-12
motivation: Formaliser les besoins produit de façon homogène et traçable avant leur réalisation.
specifications: []
project_adrs: []
habenae_adrs:
  - ../../../docs/habenae/adr/0003-use-native-codex-skills.md
agents: []
skills:
  - skill-creator
  - openai-docs
code_repository: null
branch: null
base_ref: null
worktree: null
code_commit: null
---

# TS-0001 — Créer le skill de rédaction des user stories

## Expected technical outcome

Habenae fournit un skill Codex propre au dépôt, invocable avec
`$user-story`, qui transforme un besoin produit en user story traçable. La
story produite explique le besoin et sa valeur, définit des critères
d'acceptation vérifiables et propose une estimation en points justifiée.

## Constraints

- Le skill appartient à l'orchestrateur Habenae et ne crée aucun fichier dans
  le dépôt produit sous `data/`.
- Le skill respecte le cycle de vie et le modèle de user story de Habenae.
- Le format reste lisible et modifiable directement en Markdown.

## Acceptance criteria

- [x] Le skill est découvert comme skill de dépôt et peut être invoqué avec
  `$user-story`.
- [x] Une user story produite contient une description qui expose le problème,
  le contexte et la valeur recherchée.
- [x] Une user story produite contient des critères d'acceptation observables
  et vérifiables.
- [x] Une user story produite contient une estimation en points issue d'une
  échelle documentée et accompagnée d'une justification.
- [x] Le modèle de user story et la documentation Habenae reflètent ce contrat.

## Out of scope

- Exécuter ou implémenter la user story créée.
- Modifier le dépôt produit sous `data/`.
- Créer un connecteur ou un plugin distribué hors du dépôt Habenae.

## Approach

Créer un skill d'instructions sans script, aligner le modèle de user story sur
sa sortie, puis documenter son emplacement natif et son mode d'invocation.

## Validation

- Commands run: `quick_validate.py .codex/skills/user-story`,
  `codex debug prompt-input`, `bin/habenae doctor`, `git diff --check`.
- Results: the skill validator passes; Codex lists `user-story` from the
  repository skill root; the Habenae diagnostic and whitespace checks pass.
- Before/after measurements: Not applicable.

## Closure log

- Decisions made: ADR-0003 registers executable skills under `.codex/skills/`;
  new user stories default to `future` and use the `1, 2, 3, 5, 8, 13` scale.
- Debt or follow-up work: validate the drafting guidance against real product
  needs and refine it only when observed behavior warrants a change.
- Final code commit: Not applicable; this change concerns only Habenae.
