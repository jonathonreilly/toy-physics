# Signed Gravity Remaining Closure Gates Note

**Date:** 2026-04-26
**Status:** remaining nature-grade gates reduced to precise conditional
surfaces; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_remaining_closure_gates.py`](../scripts/signed_gravity_remaining_closure_gates.py)

This note goes after the four items left outside
[`SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md`](SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md):

1. global nonlinear PDE existence;
2. actual retained graph-family APS extraction;
3. sector dynamics and preparation;
4. UV/core stability.

The result is not an all-green nature-grade closure. It is a sharper boundary:
one gate upgrades to finite small-data theorem status, and the other gates are
now constrained no-go/conditional surfaces.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Gate 1: Nonlinear Dynamics

The formal graded theorem already gives the odd/even jet:

```text
H_chi(eps) = eps chi h_1 + eps^2 h_2 + eps^3 chi h_3 + ...
```

The remaining nonlinear question is global existence. The new harness proves a
finite Galerkin small-data contraction theorem for the stationary nonlinear
map:

```text
h = K^-1 (eps J - Q_2(h,h) - Q_3(h,h,h)).
```

Readout:

```text
eps=2.0e-03
radius=7.901e-03
self_bound/r=0.568
lip_bound=0.136
sample_lip=0.003
global_pde_claim=False
```

So finite Galerkin small-data existence/uniqueness is positive. This still
does not prove a global continuum nonlinear PDE theorem.

## Gate 2: Actual Graph-Family APS Extraction

The retained graph/lattice boundary check was the most important obstruction.
The raw graph Hodge-Dirac boundary operator:

```text
D_H = [[0, B], [B^T, 0]]
```

is spectrally symmetric. On representative graph boundaries it gives:

```text
cycle8:  eta=0, zero=2, chi=0
cycle12: eta=0, zero=2, chi=0
```

This is the right no-go: a raw retained graph Hodge boundary is eta-neutral.
Adding an orientation-line mode can create a signed eta count, but the raw
Hodge kernels remain zero-window modes, so the result is still quarantined
until the retained boundary complex supplies or removes the needed mode
natively.

Harness readout:

```text
raw_hodge_eta_neutral=True
orientation_extension_has_eta=True
zero_modes_quarantine=True
actual_extraction_closed=False
```

So actual-family APS extraction is not closed. It is reduced to a specific
target:

> derive a retained orientation-line APS boundary mode on actual graph
> families, with zero modes quarantined or lifted by retained structure.

The decisive native-containment follow-up is now recorded in
`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md` (sibling
artifact; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_native_boundary_complex_containment.py`](../scripts/signed_gravity_native_boundary_complex_containment.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

The answer is negative for the raw retained cochain/Hodge boundary complex:
`D_Y=d+d^*` is cochain-parity odd, has paired spectrum, and gives
`eta=0`. Edge or face orientation reversal is a relabeling control, not an APS
source character. The previous signed APS carrier appears only after adding an
oriented one-dimensional line and quarantining the raw Hodge zero modes.

The staggered-Dirac boundary escape hatch is now audited in
`SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md` (downstream
follow-up artifact; cross-reference only — that note cites
`native_boundary_complex_containment` as its predecessor, not this note)
with runner
[`../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py`](../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

Retained-compatible staggered boundary operators are gapped but eta-neutral.
Odd open faces can produce an unpaired eta, but the sign flips under a
staggering-origin shift and disappears under even refinement, so it is not a
retained selector.

The hosted-versus-selected follow-up is now recorded in
`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md` (downstream
follow-up artifact; cross-reference only — that note cites
`native_boundary_complex_containment` as its predecessor, not this note)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

So the determinant-line package does naturally host the orientation line as a
`Z2` torsor/local system, but hosting does not choose a canonical `chi_eta`
section or force the `chi_eta rho Phi` source term.

## Gate 3: Sector Preparation

The finite sector check is now sharper:

```text
sectors=(chi+=+1, chi-=-1)
chi_path=[1,1,1,1,1,1,0,-1,-1,-1,-1,-1,-1]
block_leak=0.0e+00
mixing_control=1.9e-02
physical_prep_claim=False
```

Interpretation:

- fixed `+` and `-` APS sectors are nonempty;
- block-diagonal retained sector dynamics have zero leakage;
- explicit sector-mixing perturbations are detected;
- a sign change crosses a zero-mode defect;
- therefore opposite-sector preparation is boundary-data or defect
  preparation unless a physical preparation channel is derived.

This is a superselection result, not a physical preparation theorem.

## Gate 4: UV/Core Stability

The finite softened core does what it should for any fixed number of particles:

```text
fixed_N_core_bound=True
max_bound_violation=0.0e+00
```

But pair softening alone does not give thermodynamic/Ruelle stability for
arbitrary same-sector particle number:

```text
min_same_sector_E_per_particle_N80=-38.0
ruelle_stability_from_softening_alone=False
```

So the signed lane does not have a special negative-mass runaway, but it also
does not solve ordinary attractive-gravity global stability. A genuine global
stability mechanism would need an additional density, core, cosmological,
constraint, or quantized many-body input.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_remaining_closure_gates.py
```

Result:

```text
[PASS] global nonlinear gate reduces to finite Galerkin small-data contraction
[PASS] actual graph-family APS extraction boundary is classified
[PASS] sector dynamics classify preparation as boundary-data/defect, not ordinary mixing
[PASS] UV/core stability boundary separates fixed-N boundedness from thermodynamic failure
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS
```

## Boundary Verdict

The current remainder status is:

```text
SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS
```

The remaining blockers are now sharply stated:

1. global PDE existence is not needed for the formal local tensor theorem, but
   would be a separate small-data-to-continuum theorem if demanded;
2. actual graph-family APS extraction must find a retained orientation-line
   boundary mode, because neither the raw cochain/Hodge boundary complex nor
   the retained-compatible staggered-Dirac boundary operator currently
   contains the orientation-line APS source character; the determinant-line
   host supplies only a torsor until a canonical section/source theorem is
   derived;
3. sector preparation is boundary-data/defect preparation until a physical
   channel is derived;
4. UV/core stability needs a true global stability mechanism because pair
   softening alone is fixed-N bounded but not thermodynamically stable.

No physical signed-gravity claim follows from this note.
