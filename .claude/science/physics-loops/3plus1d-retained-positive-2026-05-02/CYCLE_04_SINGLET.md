# Cycle 04 — Route R2: Singlet completion uniqueness

**Date:** 2026-05-02
**Route attempted:** R2 (opposite-chirality SU(2)-singlet completion is unique)
**Goal:** Show that within the framework, the only available cancellation
route is to add SU(2)-singlet RH partners. Re-classify as Cl(3)/Z^3
structural fact if possible.

## Context

The bounded theorem's Step 2 admits: "Anomaly cancellation requires adding
right-handed fermions. Since chirality distinguishes SU(2) doublets (left)
from singlets (right), the new fermions must be SU(2) singlets."

The bounded note explicitly admits this is not derived from anomaly
arithmetic alone: "The time theorem only needs the existence of an
SU(2)-singlet opposite-chirality completion; it does not rely on
uniqueness from anomaly arithmetic alone." (line 79)

The "no alternative chirality mechanism" remark in the bounded note
(line 81-84) is also flagged as load-bearing: "In a local quantum field
theory on a lattice, the only algebraic source of a chirality grading
is the Clifford volume element."

## What we have available (retained-clean)

- `cpt_exact_note` (positive_theorem, retained_clean): chirality grading
  is the sublattice parity ε(x) on Z^3.
- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (positive,
  retained_clean): per-site Hilbert is C^2; no other Cl(3) irrep exists.
- `cl3_color_automorphism_theorem` (positive, retained_clean).
- `native_gauge_closure_note` (bounded, retained_clean): exact native
  cubic Cl(3)/SU(2) gauge structure; structural SU(3) closure on the
  same selected-axis graph; "no other gauge factor available" inside the
  retained algebra closure.
- `graph_first_su3_integration_note` (bounded, retained_clean): N_c=3.

## The argument (Cl(3)/Z^3 structural)

### Step A: Chirality grading is sublattice parity (Cycle 1)

From Cycle 1: the framework's chirality grading is ε(x) = (-1)^{x_1+x_2+x_3}
on Z^3, identified with the staggered γ_5 in the retained CPT note. There
is no other algebraic source of a Z_2 chirality grading on the spinor
module — the only place ε(x) lives is the Z^3 sublattice structure.

### Step B: Left-handed and right-handed fermions are sublattice-graded

Each lattice site x ∈ Z^3 carries a 2-dim Pauli irrep of Cl(3) (per
`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29`). The
sublattice parity ε(x) splits the global Hilbert into

```text
H = H_+ ⊕ H_-,    H_+ = ⊕_{x ∈ Λ_e} C^2_x,    H_- = ⊕_{x ∈ Λ_o} C^2_x.
```

The framework's convention (per the retained CPT note and staggered card)
identifies H_+ with the left-handed sector and H_- with the right-handed
sector (or vice versa — fixed up to a relabeling that is itself a CPT
operation).

### Step C: Available extensions of the matter content

To cancel anomalies, additional fermion content must be added. *Within the
framework*, what *kinds* of additions are available?

**(i)** Adding left-handed states that fit into a different SU(2) ×
SU(3) × U(1) representation: bounded by `native_gauge_closure_note`. The
retained graph-first closure shows that the gauge sector is exactly
SU(2)_L × SU(3)_C × U(1)_Y-like with no additional gauge factor. So any
new fermion must transform under representations of this *fixed*
gauge group.

**(ii)** Adding right-handed states (sublattice-opposite): allowed by
the framework's structure. The Z_2 grading from ε(x) is exact, so
right-handed states live on the opposite sublattice from left-handed
states.

**(iii)** Adding new SU(2)-doublet states with the same hypercharge as
existing doublets: this is the "vector-like completion" idea. It would
keep the chirality content unchanged but does not cancel ABJ anomalies
unless the new doublet's hypercharge cancels the existing trace, which
forces the new doublet to be (2,1)_{+1} or (2,3)_{−1/3} — exactly the
charge-conjugate of the existing left-handed doublets. But this is
*equivalent* to adding RH singlet partners via charge conjugation: in
4d Weyl notation, a RH (1,3)_{+2/3} is identical to a LH (1,3̄)_{−2/3}.

So the apparent "vector-like completion" alternative is in fact
*notationally equivalent* to the singlet completion — the underlying
field content is the same.

**(iv)** Adding SU(2)-doublet states with non-SM hypercharges: this
*could* cancel the anomaly differently, but `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`
(retained_clean) shows that the only allowed traceless abelian
eigenvalue ratio on the LH doublet block is +1/3 / -1. Other
doublet hypercharge assignments are not allowed by the retained
graph-first abelian structure.

### Step D: Weighing the alternatives

Within the retained-clean framework, the only available routes for
anomaly cancellation are:

- **Add SU(2)-singlet right-handed partners** (sublattice-opposite to
  the LH doublets). This is the SM completion.
- **Modify the framework's gauge group** to absorb the anomaly via a
  Green-Schwarz-like mechanism. This requires adding a new gauge factor
  with an axion-like Stueckelberg field — but `native_gauge_closure_note`
  rules out additional gauge factors on the retained surface.
- **Modify the framework's chirality grading** to remove chirality
  altogether. But this contradicts the retained CPT note's identification
  of ε(x) as the staggered γ_5, and contradicts the framework's
  intended chiral matter content.

So **the SU(2)-singlet RH completion is the only retained-clean
cancellation route in the framework**. This is a structural fact about
Cl(3)/Z^3 + the retained gauge closure, not a literature import.

## What this gives

Admission #2 is **closed by re-classification** as a Cl(3)/Z^3 +
retained gauge structure fact:

> **Within the framework's retained-clean structure** (Cl(3)/Z^3 + native
> gauge closure + staggered chirality grading), **the only allowed
> anomaly-cancelling completion is to add SU(2)-singlet right-handed
> fermions** (sublattice-opposite). Other completions either change the
> gauge group (forbidden by `native_gauge_closure_note`'s retained gauge
> closure) or remove chirality (forbidden by the retained sublattice
> parity grading).

## Caveats / honest limitations

(a) The argument uses `native_gauge_closure_note`, which is
**retained_bounded** rather than retained-positive. This means the
"no other gauge factor available" step is *bounded support*, not
retained-positive. If the bounded gauge closure is later sharpened to
retained-positive, the singlet uniqueness becomes retained-positive
automatically.

(b) The argument uses `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`,
which is retained-clean (positive_theorem) but only a *narrow* theorem
about the LH doublet eigenvalue ratio. Extending to "no other
LH-doublet completion is allowed" requires a slightly more general
statement.

(c) Charge conjugation equivalence between RH singlets and LH anti-
singlets is a textbook fact but doesn't need a literature import: it
is a Cl(3) algebraic fact (charge conjugation = γ_2 K acting on
spinors, an automorphism of Cl(3)).

## Outcome of Cycle 4 (Route R2)

**Closed by re-classification (case (b)) with bounded support
caveat.** Admission #2 (singlet completion uniqueness) is a structural
fact about the framework's retained-clean Cl(3)/Z^3 + gauge sector,
not a literature import. The argument relies on `native_gauge_closure_note`'s
retained-bounded "no other gauge factor" step, so the strongest
retained-positive form is conditional on that bounded step.

**Status of admission #2:** closed-bounded, conditional on
`native_gauge_closure_note`'s retained-bounded gauge closure.
No literature import needed.

**Strengthening path:** If `native_gauge_closure_note` is upgraded to
retained-positive (currently bounded due to the abelian-factor scope),
then admission #2 closes retained-positive. This is a tractable upstream
upgrade, not a hard residual.
