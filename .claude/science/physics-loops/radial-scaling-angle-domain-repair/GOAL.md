# Goal

Close the missing-derivation prompt for
`docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md`.

The audit failure was narrow: the pure radial-scaling identities were valid,
but the `(1,0)`-based tangent counter-protection statement omitted the finite
tangent domain exclusions `rho != 1` and `mu*rho != 1`.

Target outcome: a branch-local `proposed_retained` algebraic-support repair
that is ready for independent audit. This branch does not assign an audit
verdict.
