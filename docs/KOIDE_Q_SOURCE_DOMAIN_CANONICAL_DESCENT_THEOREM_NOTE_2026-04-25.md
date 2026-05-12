# Koide Q Source-Domain Canonical Descent Theorem

**Date:** 2026-04-25
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** exact support / criterion theorem for the charged-lepton `Q`
source-domain problem; not retained Koide closure
**Primary runner:** `scripts/frontier_koide_q_source_domain_canonical_descent.py`
**Scope:** source-domain descent from the retained `C3`-commutant grammar to
strict onsite scalar source functions

## Purpose

The current charged-lepton `Q = 2/3` residual is not another numerical Koide
calculation. The already-landed criterion theorem proves, on the admitted
normalized reduced carrier, that

```text
source-free <=> Z-erasure <=> Q = 2/3.
```

The remaining problem is physical:

```text
why should the undeformed charged-lepton source domain erase the reduced
traceless source coordinate Z?
```

This note proves an exact source-domain theorem that moves that problem
forward without closing it:

> if the retained `C3`-commutant source grammar is descended to strict onsite
> scalar source functions by a trace-preserving local source-domain map, the
> descent is unique and it kills the reduced traceless `Z` coordinate modulo
> the common scalar/background coordinate.

So a nonzero `Z` can remain an allowed projected probe deformation, but it
cannot survive as a dimensionless undeformed onsite background after canonical
local descent.

## Algebraic setup

Let

```text
V = complex^3
```

with site basis `(e_0,e_1,e_2)` for the physical three-generation orbit. Let
`R` be the cyclic shift

```text
R e_i = e_{i+1 mod 3}.
```

The strict onsite scalar source algebra is

```text
D = {diag(a,b,c)}.
```

Its `C3`-fixed part is

```text
D^C3 = span{I}.
```

The retained projected `C3`-commutant two-block source algebra is

```text
A = span{P_plus, P_perp} = span{I, Z},
```

where

```text
P_plus = (I + R + R^2)/3,
P_perp = I - P_plus,
Z = P_plus - P_perp = 2 P_plus - I.
```

In the site basis,

```text
P_plus = (1/3) all_ones_matrix,
P_perp = I - (1/3) all_ones_matrix.
```

Therefore

```text
diag(P_plus) = (1/3) I,
diag(P_perp) = (2/3) I,
diag(Z) = -(1/3) I.
```

This restates the already-known obstruction: `Z` is `C3`-invariant and lives in
the projected commutant, but it is not an onsite diagonal source function.

## Theorem 1: unique local descent

Let

```text
E_loc : A -> D^C3
```

be a linear source-domain descent satisfying:

1. scalar preservation: `E_loc(I) = I`;
2. trace preservation on source observables:
   `Tr(E_loc(X)) = Tr(X)` for every `X in A`;
3. strict onsite target: `E_loc(X) in D^C3 = span{I}`.

Then `E_loc` is unique and equals

```text
E_loc(X) = (Tr X / 3) I.
```

In particular,

```text
E_loc(P_plus) = (1/3) I,
E_loc(P_perp) = (2/3) I,
E_loc(Z) = -(1/3) I.
```

### Proof

Because the target is `D^C3 = span{I}`, every value has the form

```text
E_loc(X) = lambda(X) I
```

for a linear functional `lambda`. Trace preservation gives

```text
3 lambda(X) = Tr(lambda(X) I) = Tr(E_loc(X)) = Tr(X).
```

Hence

```text
lambda(X) = Tr(X)/3
```

for every `X in A`. This proves uniqueness and the displayed formula. Applying
it to `P_plus`, `P_perp`, and `Z` gives the three explicit values because

```text
Tr(P_plus) = 1,
Tr(P_perp) = 2,
Tr(Z) = -1.
```

QED.

## Theorem 2: canonical diagonal compression gives the same descent

Let

```text
Diag : End(V) -> D
```

be the site-local conditional expectation that deletes offsite matrix entries:

```text
Diag(X)_{ij} = delta_ij X_ii.
```

Then the restriction of `Diag` to `A` lands in `D^C3` and equals the unique
descent from Theorem 1:

```text
Diag(X) = E_loc(X) = (Tr X / 3) I,    X in A.
```

### Proof

Every `X in A` has the form

```text
X = alpha P_plus + beta P_perp.
```

Using the explicit site-basis diagonals,

```text
Diag(X)
  = alpha Diag(P_plus) + beta Diag(P_perp)
  = (alpha/3 + 2 beta/3) I.
```

Also

```text
Tr(X) = alpha Tr(P_plus) + beta Tr(P_perp)
      = alpha + 2 beta.
```

Therefore

```text
Diag(X) = (Tr X / 3) I.
```

QED.

## Consequence for the reduced `Z` coordinate

Write a projected commutant source as

```text
K = s I + z Z.
```

The local descent gives

```text
E_loc(K) = (s - z/3) I.
```

Thus the descent can change the common scalar/background coordinate, but it
annihilates the reduced traceless coordinate:

```text
K mod span{I} = z Z
    -> E_loc(K) mod span{I} = 0.
```

This is the exact sense in which local source-domain descent erases `Z`.

The scalar shift `(s - z/3)I` belongs to the separate common-background or
overall-scale lane. It carries no dimensionless reduced `Q` information.

## Corollary: conditional Koide Q implication

Combine this theorem with the existing background-zero / `Z`-erasure criterion
on the admitted normalized reduced carrier:

```text
Z-erasure <=> source-free reduced carrier <=> Q = 2/3.
```

Then:

```text
canonical onsite descent of the retained C3-commutant source grammar
  -> reduced Z-erasure
  -> Q = 2/3
```

inside the admitted second-order `Q` route.

The implication is conditional on the physical charged-lepton source-domain
law using this onsite descent before the dimensionless readout. This note does
not prove that physical law.

## Why this matters

The April 25 onsite source-domain synthesis proved that strict onsite
`C3`-invariant source functions erase `Z`, while the retained projected
commutant grammar still admits `Z`.

This note adds a sharper bridge between those statements:

1. there is not a family of equally natural trace-preserving onsite descents;
2. the unique trace-preserving descent is the ordinary site-local diagonal
   compression restricted to the commutant source algebra;
3. that unique descent sends every commutant background to a common onsite
   scalar;
4. hence the only part of a projected `Z` background that survives strict
   onsite descent is a common scalar shift, not the dimensionless source
   coordinate that changes `Q`.

So a future positive `Q` proof no longer has to invent a value law on the
one-parameter `Z` family. It can instead try to prove the physical source
domain principle:

```text
undeformed charged-lepton scalar backgrounds are strict onsite source
functions, or projected commutant sources must be locally descended before
dimensionless readout.
```

## Reviewer-pressure checks

### Does this silently assume `Z = 0`?

No. `Z` is allowed in the projected commutant algebra `A`. The theorem says
that when a source is required to be strict onsite data, the unique
trace-preserving local descent maps `Z` to a common scalar. The reduced
traceless source coordinate is erased only after quotienting common scalar
backgrounds.

### Does this prove charged-lepton Koide?

No. It proves a canonical descent criterion. The physical theorem selecting
onsite descent for the undeformed charged-lepton lane remains open.

### Is the scalar remnant a hidden source?

Not for dimensionless `Q`. The scalar remnant is proportional to `I`; it shifts
only the common background/source coordinate. The already-landed criterion
theorem identifies the dangerous hidden datum as the reduced traceless `Z`
coordinate, and that coordinate is killed.

### Could a reviewer choose a different map from `A` to `D^C3`?

Only by abandoning trace preservation, scalar preservation, or strict onsite
target. With those conditions fixed, Theorem 1 proves uniqueness.

### Does this conflict with the commutant-source counterdomain?

No. The counterdomain reads `sI + zZ` directly as projected commutant source
data. This theorem classifies what happens under strict onsite local descent.
The difference between those two readings is exactly the remaining physical
source-domain question.

## Claim boundary

What is proved:

- exact uniqueness of the trace-preserving descent `A -> D^C3`;
- exact identification of that descent with site-local diagonal compression;
- exact erasure of the reduced traceless `Z` coordinate modulo common scalar
  background;
- conditional implication to `Q = 2/3` inside the already-admitted normalized
  reduced-carrier route.

What is not proved:

- that the physical charged-lepton source-domain law must use strict onsite
  descent;
- that projected commutant `Z` is impossible as a probe deformation;
- retained native Koide closure;
- the separate selected-line boundary-source / based-endpoint theorem for
  `delta = 2/9`;
- the overall charged-lepton scale `v_0`.

## Closeout flags

```text
KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT=TRUE
UNIQUE_TRACE_PRESERVING_ONSITE_DESCENT=TRUE
CANONICAL_DESCENT_ERASES_REDUCED_Z=TRUE
CONDITIONAL_Q_CLOSES_IF_PHYSICAL_SOURCE_DOMAIN_USES_ONSITE_DESCENT=TRUE
Q_RETAINED_NATIVE_CLOSURE=FALSE
DELTA_RETAINED_NATIVE_CLOSURE=FALSE
FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE
RESIDUAL_Q=derive_physical_source_domain_uses_strict_onsite_descent_or_excludes_Z_as_undeformed_background
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- [koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
- [koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
- [koide_dimensionless_objection_closure_review_packet_2026-04-24](KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md)
- [koide_q_delta_closure_package_readme_2026-04-21](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md)
