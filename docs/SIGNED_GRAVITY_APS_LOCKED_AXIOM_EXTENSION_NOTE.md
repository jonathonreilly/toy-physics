# Signed Gravity APS-Locked Axiom Extension Note

**Date:** 2026-04-26
**Status:** new axiomatic extension candidate; not retained; controlled by
hard APS-gap admissibility
**Script:** [`../scripts/signed_gravity_aps_locked_axiom_extension_audit.py`](../scripts/signed_gravity_aps_locked_axiom_extension_audit.py)

This note makes the next signed-response move explicit. The retained
APS/Wald/Gauss boundary stack does not derive the signed source term:

```text
S_int = - chi_eta(Y) M_phys <rho, Phi>.
```

The retained route is blocked by
[`SIGNED_GRAVITY_RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO_NOTE.md`](SIGNED_GRAVITY_RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO_NOTE.md).
Therefore the only high-value continuation is a genuinely new axiom system.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim. It is a
bounded new-source-axiom candidate.

## New Idea: Eta-Polarized Source Line

The novel element is to treat gravitational active scalar charge as a section
of a real APS eta-polarized line over the gapped boundary chamber of each
compact source region.

For a source region `Omega` with boundary `Y = partial Omega`, let `D_Y` be the
APS boundary operator and define:

```text
chi_eta(Y) = sign eta_delta(D_Y).
```

The active scalar source is not the unsigned density `M_phys rho` by itself.
In this extension it is the eta-polarized density:

```text
J_g = chi_eta(Y) M_phys rho.
```

This is the smallest new term that spans the missing orientation-odd source
vector `[+1,-1]` while keeping the inertial mass positive and branch
independent.

## Axioms

### A1. Gapped APS Boundary Sector

An active scalar gravitational source must carry a compact boundary `Y` with
an APS operator `D_Y`. A charged sector is admitted only when:

```text
gap(D_Y) >= g_min > 0,
eta_delta(D_Y) != 0.
```

Then:

```text
chi_g = chi_eta(Y) in {+1,-1}.
```

The `eta = 0` or zero-mode case is not a third active sign. It is a null
control or a boundary defect.

### A2. Hard Gapped-Sector Admissibility

Boundary histories are admissible only while they remain inside a fixed
gapped chamber:

```text
gap(D_Y(t)) >= g_min.
```

Changing `chi_eta` requires crossing a zero mode and is therefore outside the
active-sector configuration space. This is a hard admissibility rule, not a
finite gap penalty.

### A3. Eta-Polarized Scalar Source Action

The weak-field scalar source action of an admitted compact packet is:

```text
S_eta-src[Phi, psi, Y]
  = - chi_eta(Y) M_phys sum_x |psi_x|^2 Phi_x.
```

Variation gives:

```text
rho_active(x) = - delta S_eta-src / delta Phi_x
              = chi_eta(Y) M_phys |psi_x|^2.
```

This is the new axiom. It is not obtained by multiplying the Wald/area
coefficient by `chi_eta`; the Wald carrier remains positive.

### A4. Source/Response Locking

The scalar response channel reads the same boundary label:

```text
H_diag = (m + chi_eta Phi) epsilon(x)
```

or, in point-packet weak-field notation:

```text
U = - chi_eta M_phys Phi.
```

Source sign and response sign are therefore locked by one boundary label, not
inserted independently.

### A5. Positive Inertia / Norm Separation

The inertial mass remains:

```text
M_inertial = M_phys > 0
```

in both sectors. The Born density and unitary norm are branch-independent
controls. A same-point `+/-` neutral pair can cancel active source while still
carrying positive total inertial mass.

### A6. No-Claim Quarantine

The axiom extension does not assert:

```text
negative inertial mass,
shielding,
propulsion,
reactionless force,
physical signed-gravity prediction.
```

All AWAY-language remains shorthand for the bounded signed-response search
unless a later retained continuum/tensor theorem is supplied.

## Immediate Theorems Inside The Extension

### Theorem 1: Eta-Sector Superselection Under A2

If `D_Y(t)` is an admissible boundary history satisfying
`gap(D_Y(t)) >= g_min > 0`, then `chi_eta(Y(t))` is constant.

Proof sketch: `eta_delta` can change only when an eigenvalue crosses the
zero-window. A2 excludes that crossing by construction. Therefore the sign of
`eta_delta` is constant on each connected admissible chamber.

### Theorem 2: Signed Source From A3

For admitted sectors:

```text
- delta S_eta-src / delta Phi_x = chi_eta M_phys |psi_x|^2.
```

Thus the weak-field Poisson source is orientation-odd:

```text
(-Delta) Phi = 4 pi sum_a chi_a M_a rho_a.
```

This theorem is internal to the new axiom system. It does not contradict the
retained no-go, because the no-go says the cross term is not forced by the old
basis.

### Theorem 3: Locked Momentum Balance

For two positive-inertial-mass packets with locked signs:

```text
U_ij(r) = - chi_i chi_j M_i M_j G(r).
```

Then:

```text
F_i + F_j = 0
```

for any symmetric radial kernel `G(r)`. Same-sector pairs attract and
opposite-sector pairs repel in the scalar harness:

| pair | source/response A | source/response B | read |
|---|---:|---:|---|
| `++` | `+1/+1` | `+1/+1` | attract |
| `+-` | `+1/+1` | `-1/-1` | repel |
| `-+` | `-1/-1` | `+1/+1` | repel |
| `--` | `-1/-1` | `-1/-1` | attract |

Source-only or response-only signs fail mixed-pair momentum balance and remain
controls.

### Theorem 4: Positive-Inertia No-Runaway Control

Opposite active signs do not produce the classic negative-inertial-mass
runaway in this scalar law, because both inertial masses are positive and the
forces are equal and opposite. The center of mass is not accelerated by an
internal force.

This is narrower than full energy stability. Same-sector attractive collapse
remains the ordinary UV/core gravity issue and is not solved by the sign
axiom.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_aps_locked_axiom_extension_audit.py
```

Summary:

```text
[PASS] APS eta supplies two active sectors and one quarantined null sector
[PASS] gap-preserving boundary perturbations keep chi_eta fixed
[PASS] hard admissibility blocks continuous chi flip through zero
[PASS] orientation-preserving refinement and unitary relabeling keep chi_eta portable
[PASS] eta-polarized action variation gives signed active source and null zero
[PASS] same chi_eta locks source and response; source-only/response-only controls fail
[PASS] positive inertial masses retain two-body momentum balance
[PASS] opposite-sign channel has no negative-mass runaway; same-sign UV issue remains exposed
[PASS] Born and norm controls remain clean in fixed sectors
[PASS] weak-field force magnitude remains linear in source mass
[PASS] null-sector and neutral-pair controls stay quarantined
[PASS] new axiom is exactly the missing orientation-odd source scalar
[PASS] non-claim gate remains closed
FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE
```

## What This Closes

This extension gives a coherent candidate answer to the lane's selector
problem:

- `chi_g` is hosted by the APS eta sign on a gapped compact boundary;
- hard admissibility protects the branch label;
- source and response are locked by the same label;
- inertial mass stays positive;
- the four-pair table is balanced;
- source-only and response-only insertions remain rejected controls;
- null sectors do not become a third sign;
- first refinement and unitary-relabeling sanity checks preserve `chi_eta`.

## What Remains Open

This is still not unconditional closure.

Review-critical gaps:

1. **Natural origin.** The eta-polarized source line is a new axiom. A deeper
   theorem would have to derive why scalar gravitational source density is a
   section of this APS line rather than the ordinary unsigned density.
2. **Tensor lift.** The current object is a weak-field scalar active-monopole
   law. It is not yet a full tensor gravitational action.
3. **Continuum proof.** The harness checks unitary relabeling and
   orientation-preserving refinements, not a full continuum inverse-limit
   theorem.
4. **UV/core stability.** The extension removes the signed-sector
   negative-mass runaway control, but ordinary same-sector attractive collapse
   still needs the retained gravity core or a new short-distance bound.
5. **Family portability.** The first portability sanity check is positive, but
   actual graph-family transfer remains to be proven.

## Boundary Verdict

The new status is:

```text
APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE
```

This is the cleanest genuinely new theory move in the signed-response lane.
It should be treated as an explicitly axiomatic extension until a deeper
source-line origin theorem is found.

## Source-Line Origin Follow-Up

The next pass sharpens that deeper origin target in
[`SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md`](SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md)
with runner
[`../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py`](../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py).

Result:

```text
FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT
```

That pass treats compact active sources as local sections of the real APS
determinant-orientation line. Under locality, orientation covariance,
real-action discipline, null quarantine, and refinement invariance, the
coefficient is forced to `chi_eta`. It also gives a clean invariant `A1`
lapse/trace tensor lift, while leaving the full tensor/Einstein localization
blocked.

The strongest current version is the source-character uniqueness theorem in
[`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md):

```text
FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

Within the determinant-orientation source-character grammar, `chi_eta` is the
unique normalized local real character, and the invariant `A1` tensor lift is
maximal without an added curvature-localization primitive.

The finite original-stack derivation is now recorded in
[`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md):

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

So the current finite status is stronger than an axiomatic source-line
extension: the determinant-orientation source-character grammar is derived on
the accepted finite `Cl(3)`/`Z^3` Grassmann surface. Continuum/family transport
and full tensor localization remain open.
