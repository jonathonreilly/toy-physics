# Signed Gravity Boundary Coframe `chi_g` Probe Note

**Date:** 2026-04-25
**Status:** first concrete primitive-boundary/coframe pass; algebraic
conservation target only, source locking not derived
**Script:** [`../scripts/signed_gravity_boundary_coframe_chi_probe.py`](../scripts/signed_gravity_boundary_coframe_chi_probe.py)

This note tests the top-priority nonlocal/boundary candidate from
[`SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md`](SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md):
primitive boundary coframe orientation as a possible hosted `chi_g`.

The language boundary is strict. This is not a negative-mass, shielding,
propulsion, or physical antigravity claim. The only object tested here is a
bounded signed-response selector target with positive inertial mass.

## Candidate

On a selected oriented primitive face, use the active boundary block

```text
K = P_A H_cell,    dim K = 4,
E = span(t, n, tau_1, tau_2).
```

Under the metric-compatible Clifford/coframe response premise in
[`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md),
let

```text
Gamma_a = D(e_a),
{Gamma_a, Gamma_b} = 2 delta_ab I_K.
```

The candidate branch operator is the oriented `Cl_4` volume element

```text
Q_chi = Gamma_t Gamma_n Gamma_tau1 Gamma_tau2.
```

With the Euclidean Hermitian convention used by the Target 3 bridge,

```text
Q_chi = Q_chi^dagger,
Q_chi^2 = I,
dim K_+ = dim K_- = 2.
```

The sign is therefore a valid Clifford chirality on the primitive active
boundary block.

## What Is Conserved

The algebraic conservation statement is precise:

> `Q_chi` is conserved by boundary Hamiltonians in the even Clifford algebra
> of the selected primitive coframe.

Equivalently, for retained boundary dynamics restricted to even operators,

```text
[H_boundary, Q_chi] = 0,
P_- U_boundary(t) P_+ = 0.
```

The probe constructs an even Hermitian boundary Hamiltonian from bivectors
`i Gamma_a Gamma_b` and verifies both the commutator and exact-unitary leakage
residuals. It also injects one odd coframe term `Gamma_t` as a control; the
odd term mixes sectors, as expected.

This is not yet a retained theorem, because the written proof would still have
to show that all allowed primitive boundary couplings, gluing maps, scalar
terms, and bulk-induced boundary operators are even in this coframe algebra.
If any retained allowed term is odd, this candidate lands as
`BOUNDARY_CHI_NOT_CONSERVED`.

## Orientation and Gauge/Frame Control

The probe separates proper coframe relabeling from orientation reversal:

```text
det R = +1  =>  Q_chi -> Q_chi,
det R = -1  =>  Q_chi -> -Q_chi.
```

Thus `Q_chi` is invariant under orientation-preserving primitive coframe
changes, but not under orientation-reversing relabeling. The candidate is only
meaningful if the selected boundary face carries a fixed physical orientation
from the boundary/worldtube structure. If normal reversal, tangent swap, or
face gluing is an allowed gauge relabeling rather than a sector-changing
operation, then the sign is a convention and the candidate fails as
`BOUNDARY_CHI_GAUGE_RELABEL`.

## Source/Response Locking

The required locked source form would be

```text
rho_inertial = M_phys |psi|^2 >= 0,
rho_active = chi_g M_phys |psi|^2,
response coupling = chi_g Phi,
chi_g = +/-1 from Q_chi.
```

For a pure `Q_chi` sector, an inserted `Q_chi` source density would have the
right algebraic shape:

```text
M_phys psi^dagger Q_chi psi = chi_g M_phys |psi|^2.
```

But this pass does **not** derive the variational identity

```text
delta S_source / delta Phi
  = M_phys psi^dagger Q_chi psi.
```

The retained source-action notes still identify the local candidates as:

```text
rho_B = |psi|^2,
rho_s = epsilon |psi|^2,
rho_g = chi_g |psi|^2 only if chi_g is externally supplied.
```

Therefore the primitive coframe chirality is currently source-neutral. It is a
conserved oriented Clifford label on the even boundary surface, not yet a
native signed exterior Gauss/asymptotic monopole. The missing theorem would
have to prove, on the same boundary surface,

```text
C_signed = chi_g C_abs,
delta S_boundary / delta Phi = chi_g M_phys |psi|^2,
response sign = chi_g.
```

Without that theorem, response-side insertion or source-side insertion would
repeat the source-only/response-only failure classified in
[`SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md`](SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md).

## Positive Inertial Mass

The probe keeps inertial mass independent of the chirality sign:

```text
M_inertial = M_phys ||psi||^2 > 0
```

in both `Q_chi` sectors. The `Q_chi=-1` sector is not implemented through
negative kinetic energy, negative norm, or negative rest mass.

If a source theorem is later supplied, the source-unit theorem may consume the
already-derived sign only at the final bookkeeping step:

```text
q_bare = 4 pi chi_g M_phys,
G_Newton,lat = 1,
M_inertial = M_phys > 0.
```

This follows the discipline in
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md).
It does not derive `chi_g`.

## Null, Born, Norm, and Source-Unit Controls

The script verifies the following controls:

| control | result |
|---|---|
| `Q_chi` Hermitian/involution | passes |
| sector dimensions | `dim K_+ = dim K_- = 2` |
| even-boundary conservation | passes on the constructed even surface |
| odd-term control | detects sector mixing |
| orientation-preserving relabel | leaves `Q_chi` invariant |
| orientation-reversing relabel | flips `Q_chi` |
| positive inertial norm | passes in both sectors |
| equal `+/-` inserted active monopoles | cancel |
| inertial mass of paired sectors | remains positive |
| exact-unitary norm drift | zero to numerical precision |
| fixed-branch Born three-slit identity | unchanged |
| source-unit conversion | consumes a supplied sign only |

Representative command:

```bash
python3 scripts/signed_gravity_boundary_coframe_chi_probe.py
```

Representative result:

```text
FINAL_TAG: BOUNDARY_CHI_SOURCE_NOT_LOCKED
```

## Verdict

The primitive boundary coframe orientation is a legitimate theorem target for
a conserved boundary `Z_2` label:

```text
Q_chi = Gamma_t Gamma_n Gamma_tau1 Gamma_tau2
```

on the even primitive Clifford boundary surface. It is **not** presently a
theorem candidate for signed active gravity, because the source/response
locking theorem is missing. The current status is:

```text
BOUNDARY_CHI_SOURCE_NOT_LOCKED
```

This is stronger than a note-only no-go: there is a meaningful algebraic probe,
and it isolates exactly where the candidate survives and where it remains
blocked. The next theorem, if attempted, must be a boundary action/Gauss
identity that derives the signed exterior monopole from the same oriented
coframe label while preserving positive inertial mass and branch-preserving
unitarity.
