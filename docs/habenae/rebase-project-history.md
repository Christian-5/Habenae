# Rebase a project history onto Habenae

`Habenae` is the upstream repository for the harness. A project history such
as `Belisama-MTS-History` is a separate repository whose commits contain the
project definition, stories, specifications, and project documentation. It is
rebased onto the harness when the harness evolves.

## Initial setup

Create the project history from the exact Habenae revision that should be its
initial baseline, then add the project-specific files and push it to its own
GitHub repository:

```bash
git clone git@github.com:Christian-5/Habenae.git Belisama-MTS-History
cd Belisama-MTS-History
git remote rename origin habenae
git remote add origin git@github.com:Christian-5/Belisama-MTS-History.git
git push -u origin master
```

Do not add `product/` to either repository. The application code remains in
the separate `Belisama-MTS` repository managed through `bin/habenae product`.

## Update the project history

On a clean project branch, run:

```bash
./bin/habenae harness rebase
git push --force-with-lease origin master
```

The command fetches `habenae/master` and rebases the current branch onto it.
The first invocation can instead configure the remote explicitly:

```bash
./bin/habenae harness rebase \
  git@github.com:Christian-5/Habenae.git master
```

Resolve conflicts normally, run the relevant checks, then use
`--force-with-lease` because rebase rewrites the project branch history. The
upstream `Habenae` repository must never be force-pushed as part of this flow.

## Boundary for future commits

Harness improvements belong in `Habenae`. Belisama-specific stories and
project documentation belong in `Belisama-MTS-History`. When a harness change
also needs a project-specific adaptation, make the harness commit first, then
rebase the project history and add the adaptation there.
