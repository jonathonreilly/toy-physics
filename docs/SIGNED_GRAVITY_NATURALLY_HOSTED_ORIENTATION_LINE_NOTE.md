# Signed Gravity Naturally Hosted Orientation-Line Note

**Date:** 2026-04-26
**Status:** determinant-line orientation is naturally hosted as a `Z2` torsor;
canonical signed selector remains unforced; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py)

This note answers the last clean escape hatch after
`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md` (upstream
predecessor; backticked to avoid length-4/5 cycle through
nature_grade_closure_blocker_audit and cl3z3_source_character_derivation)
and
`SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md`
(upstream predecessor; backticked for cluster citation-graph hygiene):

> If the raw Hodge and retained-compatible staggered boundary operators do not
> contain an unpaired APS eta mode, can the determinant-line package still
> naturally host the orientation line?

The finite answer is:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## The Distinction

There are three different statements:

| statement | status |
|---|---|
| determinant-line package hosts a real orientation line | yes |
| raw boundary operators contain an unpaired APS eta selector | no |
| hosted orientation line canonically selects `chi_eta` and forces `chi_eta rho Phi` | no |

The result is therefore not a full no-go and not a selector theorem. It is a
sharp middle classification:

```text
naturally hosted as a line/torsor, not canonically selected as an active source.
```

## Determinant-Line Host

The finite Grassmann Gaussian supplies determinant lines. Under disjoint sewing:

```text
Det(D_1 direct-sum D_2) = Det(D_1) tensor Det(D_2).
```

The harness checks determinant multiplication, `log|det|` additivity, and
orientation multiplication:

```text
det_mult_err=3.6e-16
log_add_err=4.4e-16
orientation_product=+1
orientation_total=+1
```

So the orientation line is not arbitrary decoration. It is naturally hosted by
the same determinant-line functor that carries the retained magnitude
generator.

## Torsor, Not Section

The hosted line is a `Z2` torsor. It has two unit sections, and the determinant
magnitude cannot choose between them.

The harness uses an odd basis relabeling:

```text
operator_det_same=True
line_basis_orientation=+1 -> -1
canonical_section_forced=False
```

This is the key obstruction. A real line can be naturally present without a
canonical positive section. The retained `log|det|` observable sees only the
magnitude side:

```text
|Det| -> log|det|.
```

The signed source would need a chosen oriented section:

```text
Or(Det) -> {+1,-1}.
```

That chosen section is not forced by the determinant functor alone.

## Flat Local System Host

If an orientation line is chosen, it transports cleanly as a flat `Z2` local
system over a finite atlas/refinement proxy:

```text
cocycle=[1,1,1]
refinement_pullback=True
gauge_changed_sections=True
flat_host=True
canonical_section=False
```

This supports the "naturally hosted" wording. The line is a legitimate local
system host. But local trivialization gauge changes alter section signs, so
the host does not by itself provide a physical branch label.

## Operator Containment Still Negative

The hosted line is not contained in the audited boundary operators:

```text
raw_hodge_contains_line=False
staggered_contains_line=False
raw_hodge_eta_neutral=True
staggered_eta_neutral=True
```

This preserves the earlier no-go results:

```text
SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

## Source Term Not Forced

A hosted torsor does not force the active source cross term:

```text
positive retained source: [ +1, +1 ]
torsor existence only:    [  0,  0 ]
desired signed source:    [ +1, -1 ]
```

Harness readout:

```text
residual_without_section=1.414e+00
residual_with_chosen_section=3.1e-16
flipped_section_equally_coherent=0.0e+00
source_term_forced=False
```

Interpretation:

- once a section is chosen, the signed source can be written;
- the opposite section is equally coherent unless a normalization/source
  principle fixes it;
- the source term `chi_eta rho Phi` is therefore not derived by hosting alone.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_naturally_hosted_orientation_line.py
```

Result:

```text
[PASS] finite Grassmann determinant functor naturally hosts a real orientation line
[PASS] orientation line is a Z2 torsor, not a canonical signed section
[PASS] chosen orientation line transports as a flat local system
[PASS] audited raw boundary operators do not contain the hosted APS line
[PASS] hosted orientation torsor does not force chi_eta rho Phi source term
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

## Boundary Verdict

The determinant-line package naturally hosts the orientation line. That keeps
the source-character grammar mathematically meaningful and not merely
phenomenological.

But hosting is not selection:

```text
canonical_chi_section_forced=False
operator_realization_contained=False
chi_rho_phi_source_forced=False
```

So the signed-response lane now has a sharp status:

```text
orientation line naturally hosted, active signed selector not derived.
```

To promote the lane, future work would need a retained theorem that fixes a
canonical section of this orientation local system and derives the corresponding
source action. Without that theorem, this is a controlled source-line extension
or no-go/control package, not a physical signed-gravity sector.

No physical signed-gravity claim follows from this note.
