# PR BACKLOG — VEV V-Singlet Derivation Campaign

**Date:** 2026-05-02

PRs that could not be opened, with exact recovery commands.

(empty — campaign just started)

## Format for backlog entries

```text
PR slug: [physics-loop] <slug>-blockNN: <one-line summary> (<honest status>)
Branch: physics-loop/<slug>-blockNN-<date>
Base: main (or stacked-on-prior-block-branch)
Reason for backlog: <auth | network | dirty PR | other>
Recovery commands:
  git checkout physics-loop/<slug>-blockNN-<date>
  gh pr create --base main --title "..." --body "$(cat <<'EOF'
  ...
  EOF
  )"
```
