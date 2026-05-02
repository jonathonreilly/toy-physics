# Signed Gravity APS-Locked Source Action Proposal

**Date:** 2026-04-25
**Status:** conditional action candidate; not derived from the retained stack
**Script:** [`../scripts/signed_gravity_aps_locked_source_action_proposal.py`](../scripts/signed_gravity_aps_locked_source_action_proposal.py)

This note proposes the smallest action that would close the remaining
APS/source-locking gap identified in
[`SIGNED_GRAVITY_APS_WALD_GAUSS_BRIDGE_AUDIT_NOTE.md`](SIGNED_GRAVITY_APS_WALD_GAUSS_BRIDGE_AUDIT_NOTE.md).

The boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim. It is a
conditional action ansatz: if accepted or later derived, it supplies the
missing `chi_eta` variation by construction. Until then it is a proposal and a
test harness, not a retained theorem.

## Proposed Action

For each compact source region `Omega_a` with gapped APS boundary
`Y_a = partial Omega_a`, define:

```text
chi_a = chi_eta(Y_a) = sign eta_delta(D_Ya)
```

only when:

```text
h_delta(D_Ya) = 0
eta_delta(D_Ya) != 0.
```

The `eta = 0` or zero-window sector is a null/control sector, not a third
active sign.

Let `rho_a(x) = |psi_a(x)|^2` be normalized:

```text
sum_x rho_a(x) = 1,
M_a > 0.
```

The proposed weak-field source action is:

```text
S_APS-lock[Phi, psi, Y]
  = (1/(8 pi)) sum_<xy> (Phi_x - Phi_y)^2
    - sum_a chi_a M_a sum_x rho_a(x) Phi_x
    + sum_a S_matter,0[psi_a; M_a]
    + sum_a S_APS-gap[D_Ya]
    + S_Wald^+[Y_a].
```

The positive boundary carrier remains:

```text
S_Wald^+[Y] / k_B = (1/4) A(Y)/a^2.
```

The sign is not placed in the Wald/area coefficient. Putting `chi/4` there
would make the `chi=-1` branch a negative-area-coefficient branch, which is
rejected.

For the staggered parity-correct response implementation, the same branch
label would enter the scalar channel as:

```text
H_diag,a = (m_a + chi_a Phi) epsilon(x),
```

or, in the point-particle weak-field readout:

```text
U_a = - chi_a M_a Phi.
```

The source and response signs are therefore locked by the same APS boundary
label.

## Variation

The active source is defined as:

```text
rho_active(x) = - delta S_int / delta Phi_x.
```

For the proposed interaction term,

```text
S_int = - sum_a chi_a M_a sum_x rho_a(x) Phi_x,
```

the variation gives:

```text
rho_active(x) = sum_a chi_a M_a rho_a(x).
```

Stationarity of `Phi` gives the physical-source Poisson equation:

```text
(-Delta) Phi = 4 pi sum_a chi_a M_a rho_a.
```

The source-unit theorem then consumes the already supplied signed active
source:

```text
q_bare,a = 4 pi chi_a M_a.
```

This is exactly what the earlier bridge audit could not derive from the
existing retained APS/Wald/Gauss stack.

## What Is New

Existing retained ingredients:

- the APS eta sign as a basis-invariant, gap-stable boundary label
- the positive Wald/Gauss/source-unit scale:
  `c_cell = 1/4`, `lambda = 1`, `M_phys = C_abs`,
  `q_bare = 4 pi M_phys`
- positive inertial mass from the ordinary norm and kinetic term

New premise:

```text
S_int = - chi_eta M_phys <rho, Phi>.
```

That premise is the whole proposal. It should not be hidden. It is not derived
by source-unit normalization, and it is not obtained by multiplying the
positive Wald coefficient by `chi_eta`.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_aps_locked_source_action_proposal.py
```

Summary:

```text
[PASS] source variation gives +M rho in chi=+ sector
       residual=1.628e-12, active=+2.750000
[PASS] source variation gives -M rho in chi=- sector
       residual=1.628e-12, active=-2.750000
[PASS] positive Wald/area carrier is not multiplied by chi
[PASS] positive inertial mass is branch independent
       M_+=M_-=2.750
[PASS] same-point +/- active source cancels with positive inertia
       C_signed_sum=+0.000e+00, M_sum=5.500
[PASS] source-unit conversion consumes the proposed signed source
       q_bare=4*pi*chi_eta*M_phys
FINAL_TAG: APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE
```

The proposed action passes the local algebraic gates because it was built to
do so. That is useful as a target, but it is not a derivation.

## Four-Pair Table

The harness compares the proposed action with controls:

| law | max balance residual | table | derived without new action | reads |
|---|---:|---|---|---|
| retained positive | `0.000e+00` | fail | yes | all pairs attract |
| APS eta spectator | `0.000e+00` | fail | yes | zero active source |
| APS source-only inserted | `2.000e+00` | fail | no | mixed pairs unbalanced |
| APS response-only inserted | `2.000e+00` | fail | no | mixed pairs unbalanced |
| APS locked action ansatz | `0.000e+00` | pass | no | same-sector attract, opposite-sector repel |

The proposed action is the first APS route that gives the desired locked table,
but only because the new action term puts `chi_eta` into both source and
response.

## Controls

The proposal keeps the basic controls clean in the finite harness:

```text
Born I3, chi=+ sector: +1.794e-43
Born I3, chi=- sector: +1.794e-43
max norm drift: 2.887e-15
same-point +/- q_bare sum: 0
same-point +/- inertial mass sum: positive
```

The branch sign does not alter Born linearity, unitary norm preservation, or
positive inertial mass in the fixed-sector harness.

## Proof Obligations

To promote this from action proposal to retained theorem, the lane must still
prove:

1. **Origin.** Derive `S_int = -chi_eta M_phys <rho,Phi>` from retained
   APS/Wald/Gauss boundary structure, rather than adding it as a new axiom.
2. **Superselection.** Prove the eta sector is protected under admissible
   boundary dynamics. Zero crossings must remain classified defects.
3. **Energy stability.** Supply a bounded Hamiltonian/constraint argument that
   prevents runaway production of positive-inertial-mass opposite active
   signs.
4. **Scalar/tensor discipline.** Keep this as a scalar active-monopole action
   unless a separate tensor-valued gravity theorem is supplied.
5. **Continuum and family portability.** Only after the first four gates pass,
   test refinement, graph families, and two-packet dynamics.

## Boundary Verdict

The proposed action is:

```text
APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE
```

It is the cleanest concrete action target found so far. It also makes the
remaining scientific burden sharper:

> The signed-response lane now needs a derivation of this APS-locked source
> term, or a no-go showing that no retained APS/Wald/Gauss source action can
> produce it without adding a new sign axiom.

Until that derivation exists, the action remains a conditional candidate and
the signed-gravity claim surface remains blocked.

## Follow-Up Audit

The origin, superselection, and stability gates are audited in
[`SIGNED_GRAVITY_APS_ACTION_ORIGIN_SUPERSELECTION_STABILITY_NOTE.md`](SIGNED_GRAVITY_APS_ACTION_ORIGIN_SUPERSELECTION_STABILITY_NOTE.md)
with runner
[`../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py`](../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py).

Result:

```text
FINAL_TAG: APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED
```

The proposal remains the cleanest target action, but it is not retained:
separable APS/Wald/Gauss terms cannot produce the signed source without the
new `chi_eta rho Phi` cross term, eta superselection is conditional on a
protected boundary gap, and full boundedness still needs an ordinary
short-distance gravity UV/core or constraint argument.

## Axiomatic Extension Follow-Up

The retained route is blocked, so the next honest move is to name the new
structure directly. That pass is recorded in
[`SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md)
with runner
[`../scripts/signed_gravity_aps_locked_axiom_extension_audit.py`](../scripts/signed_gravity_aps_locked_axiom_extension_audit.py).

Result:

```text
FINAL_TAG: APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE
```

The axiom extension treats `chi_eta M_phys rho` as an eta-polarized source
line on gapped APS boundary sectors and imposes hard gap admissibility. It is
coherent as a controlled candidate, but it is not a retained theorem or a
physical signed-gravity claim.
