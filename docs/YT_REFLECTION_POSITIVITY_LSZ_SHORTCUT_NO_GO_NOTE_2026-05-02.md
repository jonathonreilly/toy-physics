# PR #230 Reflection-Positivity LSZ Shortcut No-Go

```yaml
actual_current_surface_status: exact negative boundary / reflection positivity not scalar LSZ closure
proposal_allowed: false
bare_retained_allowed: false
```

This block checks a narrow possible repair to the scalar LSZ blocker: use
reflection positivity / OS reconstruction to certify the scalar pole residue.

It does not work.  Reflection positivity supplies a positive spectral
representation.  The existing positive pole-plus-continuum family from the
Stieltjes obstruction can also be represented as a reflection-positive
Euclidean time correlator:

```text
C(t) = Z_h exp(-m_h t)/(2 m_h) + sum_j w_j exp(-M_j t)/(2 M_j)
```

with all weights nonnegative.  Its OS reflection matrices
`M_ij = C(t_i + t_j)` are positive semidefinite, but the same finite
same-source shell data and pole location remain compatible with different
`Z_h`.  The inverse-propagator derivative and FH/LSZ readout factor still move.

## Runner

```text
python3 scripts/frontier_yt_reflection_positivity_lsz_shortcut_no_go.py
# SUMMARY: PASS=9 FAIL=0
```

Certificate:

```text
outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json
```

## Boundary

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  It only blocks a shortcut.  A positive closure still
needs pole saturation / continuum-threshold control, a microscopic scalar
denominator theorem, production continuum evidence, and the canonical-Higgs
source-pole identity.

This block does not set `kappa_s = 1`, does not infer pole saturation from
OS positivity, and does not use `H_unit`, `yt_ward_identity`, observed target
values, `alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.

## Exact Next Action

Process seed-controlled production chunks if the foreground jobs finish, or
derive a microscopic scalar-denominator / canonical-Higgs identity theorem
that is stronger than positive spectral reconstruction.
