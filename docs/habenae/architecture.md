# Habenae architecture

## Two independent planes

Habenae deliberately separates:

1. the **control plane**, this repository, which describes what to do, why, and
   how;
2. the **product repository**, under `product/`, which contains only the product code.

This separation keeps conventions tied to a particular agent out of the
application repository. It also makes it possible to change orchestrators
without rewriting the product history.

## Git model

The Habenae repository is a normal Git repository. `product/` is ignored.

The code repository uses a shared bare clone:

```text
product/.bare             shared Git history, references, and configuration
product/.git              file containing "gitdir: ./.bare"
product/main              main branch worktree
product/feature/<name>    feature branch worktree
```

All worktrees share the objects, references, and hooks from the bare repository.
A branch can be checked out in only one worktree at a time.

## Cross-repository traceability

There is no atomic commit across the two repositories. Each durable story
directory contains `story.md` for normative state and `collaboration.md` for
specialist handoffs. Together they record:

- the code repository and branch;
- the local worktree path;
- the starting reference;
- the final change SHA;
- validation evidence.

The directory moves between `future/`, `current/`, and `past/` as one unit; its
collaboration journal is never discarded after implementation.

The code must not depend on Habenae to work.
