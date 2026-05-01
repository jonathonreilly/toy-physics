# PR Backlog

This block is being added to the existing PR #230 branch rather than opened as
a separate physics-loop PR, because the user explicitly asked to re-scope the
PR #230 `y_t` path.

If split later, suggested title:

```text
[physics-loop] yt-nonmc-criticality-reset conditional-support
```

Suggested PR body summary:

- Adds a Planck double-criticality selector runner.
- Reports `y_t(v)=0.9208739295` at 3-loop order.
- Does not use top mass, `H_unit`, or the Ward identity.
- Blocks on deriving `beta_lambda(M_Pl)=0` from the substrate.

