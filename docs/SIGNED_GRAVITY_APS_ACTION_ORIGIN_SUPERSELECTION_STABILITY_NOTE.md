# Signed Gravity APS Action Origin / Superselection / Stability Note

**Date:** 2026-04-25
**Status:** APS-locked source action remains conditional, not retained
**Script:** [`../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py`](../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py)

This note audits the three proof obligations left by
[`SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md):

1. origin of the proposed action term;
2. eta-sector superselection;
3. energy-stability / no-runaway behavior.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Proposed Action Under Audit

The conditional action target is:

```text
S_int = - chi_eta(Y) M_phys <rho, Phi>,
rho = |psi|^2,
chi_eta(Y) = sign eta_delta(D_Y).
```

It was introduced because the retained APS/Wald/Gauss bridge audit found:

```text
APS_WALD_GAUSS_BRIDGE_NOT_DERIVED
```

The proposal itself passes the finite source/response harness:

```text
APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE
```

This note asks whether the remaining proof obligations close.

## Origin Audit

The audit models the current retained source-side ingredients as a finite
source-current basis over the two eta sectors:

| ingredient | source vector over `(chi=+, chi=-)` |
|---|---:|
| retained positive Born/Gauss source | `[+1, +1]` |
| APS eta spectator term | `[0, 0]` |
| positive Wald/area carrier | `[0, 0]` |

The required signed source is:

```text
[+1, -1].
```

Result:

```text
[PASS] retained separable APS/Wald/Gauss terms cannot produce signed source
       least-squares residual=1.414e+00
[PASS] adding the chi*rho*Phi cross term exactly produces signed source
       residual=1.110e-16, coeffs=[0. 0. 0. 1.]
```

So, within this retained separable action class, the proposed action is not
derived. It requires exactly the new cross term:

```text
chi_eta rho Phi.
```

That is useful because it sharpens the target. It is also a no-go for claiming
that the current retained APS/Wald/Gauss stack already contains the term.

## Eta Superselection Audit

The finite APS boundary model gives:

```text
[PASS] eta sign is stable under sampled gap-preserving perturbations
       min_gap_after=0.367
[PASS] eta sign changes through explicit zero-crossing defect if gap is not protected
       chi_path=[1, 1, 1, 1, 0, -1, -1, -1, -1]
```

Therefore the eta label is conditionally stable:

```text
gap_0(D_Y(t)) >= g > 0  =>  chi_eta constant.
```

But this is not yet a retained superselection theorem. The action proposal
still needs a proof that admissible boundary dynamics preserve the APS gap, or
that zero crossings are excluded/classified defects on the sector surface.

## Energy / Runaway Audit

The locked sign law uses positive inertial mass and pair energy:

```text
U_ij(r) = - chi_i chi_j M_i M_j / sqrt(r^2 + a_core^2).
```

The force law has exact action-reaction only when source and response signs are
locked. The controls reproduce the expected failures:

```text
[PASS] locked signs have exact two-body force balance
[PASS] source-only control fails mixed-pair balance
[PASS] response-only control fails mixed-pair balance
```

For opposite locked signs:

```text
F_A = -1,
F_B = +1,
F_A + F_B = 0.
```

So the classic negative-inertial-mass runaway control is avoided. The bodies
accelerate apart with equal and opposite forces; the center of mass does not
run away in one direction.

The pair-creation check is also clean for opposite signs:

```text
[PASS] opposite-sign pair creation has positive rest-energy infimum
       E_opp,min(core=1)=2.100
```

What remains is not a signed-sector-specific runaway. It is ordinary
short-distance Newtonian collapse in the attractive same-sector channel:

```text
[PASS] ordinary same-sector Newtonian collapse remains a UV/core issue
       E_same,min(core=1)=1.001,
       E_same,min(core=0.25)=-1.922
```

Thus the stability read is:

- no negative-mass runaway appears in the locked positive-inertial-mass sign
  law;
- opposite-sign pair production is not energetically favored in the finite
  softened audit;
- full boundedness still requires a UV/core or constraint input of the same
  kind ordinary attractive gravity needs.

## Verdict

Command:

```bash
python3 scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py
```

Current tag:

```text
FINAL_TAG: APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED
```

Interpretation:

1. **Origin:** no-go within the current retained separable APS/Wald/Gauss
   action class. The proposed term is a new `chi_eta rho Phi` cross term.
2. **Superselection:** conditional on a protected APS boundary gap; not yet
   derived for all admissible boundary dynamics.
3. **Energy stability:** no negative-inertial-mass runaway in the locked
   positive-mass table, but ordinary same-sector short-distance collapse still
   needs a UV/core or constraint argument.

## Next Decision

The lane is now sharply bounded:

```text
NO_GO_STRICT_SELECTOR
SOURCE_PRIMITIVE_BLOCKED_LOCAL
APS_WALD_GAUSS_BRIDGE_NOT_DERIVED
APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED
```

The only way to promote the APS-locked action is to derive the cross term:

```text
S_int = - chi_eta M_phys <rho, Phi>
```

from a retained boundary source principle. Otherwise the signed-response lane
should remain a documented consequence/control and no-go-boundary packet.

## Retained Source-Principle Follow-Up

The retained boundary source-principle route is now audited directly in
`SIGNED_GRAVITY_RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO_NOTE.md`
(downstream consumer in same lane; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_retained_boundary_source_principle_nogo.py`](../scripts/signed_gravity_retained_boundary_source_principle_nogo.py).

Result:

```text
FINAL_TAG: RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO
```

The retained source-current basis has only the positive source vector
`[+1,+1]` plus source-neutral APS/Wald terms. It cannot span the required
orientation-odd source `[+1,-1]`. The cross term `chi_eta rho Phi` is therefore
new, and APS gap protection requires a new hard admissibility constraint or a
new dynamical zero-crossing exclusion theorem.

## New-Axiom Continuation

The explicit new-axiom package is recorded in
`SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md` (downstream follow-up
artifact; cross-reference only — that note cites the retained-boundary
no-go as its predecessor, not this audit)
with runner
[`../scripts/signed_gravity_aps_locked_axiom_extension_audit.py`](../scripts/signed_gravity_aps_locked_axiom_extension_audit.py).

It promotes the missing pieces to named axioms:

```text
J_g = chi_eta(Y) M_phys rho,
gap(D_Y(t)) >= g_min on admissible active-source histories.
```

Result:

```text
FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE
```

This is an internally coherent extension candidate, not a retained origin
theorem.

The follow-up source-line pass then sharpens the origin premise in
`SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md` (downstream
follow-up artifact; cross-reference only — that note cites
`aps_locked_axiom_extension` as its predecessor, not this audit)
with runner
[`../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py`](../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py):

```text
FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT
```

It treats active compact sources as local sections of the real APS
determinant-orientation line. Within that principle, the signed coefficient is
forced to `chi_eta`; outside that principle, the original retained-origin
block remains.

The stronger source-character uniqueness theorem is recorded in
[`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md):

```text
FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

This is still conditional on the determinant-orientation source-character
grammar, but within that grammar `chi_eta` is unique and the tensor lift is
maximal at invariant `A1`.

The finite original-stack derivation is now recorded in
[`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md):

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

It derives the source-character grammar itself on the finite accepted
`Cl(3)`/`Z^3` determinant-line surface. This upgrades the source-origin side
but does not close continuum/family transport, full tensor localization, or
ordinary UV/core stability.
