# Lane 5 `(C1)` A2 Action-Unit Metrology Obstruction Note

**Date:** 2026-04-29
**Status:** support / current-surface negative boundary result on
`main`; does not close `(C1)` and does not promote any theorem or
claim.
**Runner:** `scripts/frontier_hubble_lane5_c1_a2_action_unit_metrology_obstruction.py`
**Lane:** 5 -- Hubble constant derivation, `(C1)` absolute-scale gate

## Purpose

The A1 stretch attempt showed that bulk Grassmann/CAR structure does not
descend to `P_A H_cell` without a projection/morphism theorem. A2 tests the
other half of the `(C1)` residual:

```text
Can retained g_bare = 1, the accepted plaquette/u_0 surface, and the
minimal APBC hierarchy block pin the absolute action unit on P_A H_cell?
```

The answer is no on the current surface. Those inputs are real support for
dimensionless lattice normalization, coupling transport, and hierarchy
scaling. They do not break the Target 3 `(S, kappa)` rescaling degeneracy.

## Minimal Premises Used

- `g_bare = 1` from the two-Ward / structural-normalization `g_bare` packet.
- Wilson plaquette surface at `beta = 2 N_c / g_bare^2 = 6`.
- Same-surface plaquette constant `<P> = 0.5934` and
  `u_0 = <P>^(1/4)`.
- Minimal APBC hierarchy block, including the dimensionless factor
  `(7/8)^(1/4)` and the exact `m/u_0` homogeneity statement.
- `P_A H_cell` with `rank(P_A)=4` and `c_cell = 4/16 = 1/4`.

No measured value of `G`, `hbar`, `M_Pl`, `l_P`, `H_0`, or any cosmological
observable enters this obstruction.

## Result

The A2 inputs pin dimensionless data:

```text
g_bare = 1,
beta = 6,
u_0 = <P>^(1/4),
C_APBC = (7/8)^(1/4),
c_cell = 1/4.
```

They do not pin an absolute dimensional action quantum `kappa`. For any
positive scale `lambda`, the replacement

```text
S_dim -> lambda S_dim,
kappa -> lambda kappa
```

leaves all Hilbert phases and all Euclidean lattice weights determined by the
dimensionless action unchanged:

```text
exp(i S_dim/kappa) = exp(i lambda S_dim / lambda kappa).
```

The plaquette and APBC constants remain unchanged because they are
dimensionless observables of the lattice partition function. The primitive
trace `c_cell = 1/4` also remains unchanged. Therefore the A2 input set
admits a one-parameter family of action-unit readings with identical
dimensionless physics.

## Runner Witness

The runner checks eight facts.

1. `g_bare = 1` fixes the Wilson gauge point `beta = 6`.
2. The canonical plaquette surface gives dimensionless `u_0`, `alpha_LM`,
   and `alpha_s(v)`.
3. The APBC hierarchy factor is dimensionless.
4. Hilbert phases are invariant under common `(S_dim, kappa)` rescaling.
5. The Wilson/plaquette Boltzmann weight depends on the dimensionless
   lattice action, not on an external `kappa`.
6. The primitive `P_A` coefficient stays `1/4` under all action-unit readings.
7. A family of different `kappa` values gives the same projected phase on
   `P_A H_cell`.
8. Finite matrices still cannot realize a nonzero exact canonical action
   commutator on the rank-four block.

Current output:

```text
TOTAL: PASS=8, FAIL=0
```

## Claim Boundary

This note does **not** weaken the retained `g_bare` packet, the plaquette
surface, the APBC hierarchy support theorem, or the conditional Planck packet.
It only closes the direct A2 shortcut:

```text
g_bare = 1 + plaquette/u_0 + APBC hierarchy + c_cell = 1/4
  => absolute action-unit metrology on P_A H_cell.
```

The missing import is now explicit:

```text
a physical clock/source/action metrology map tying the dimensionless lattice
action and P_A boundary carrier to a particular dimensional kappa.
```

Equivalently, A2 can become positive only if a new theorem couples the
canonical dimensionless lattice action to the primitive boundary/action
carrier in a way that is not invariant under
`(S_dim, kappa) -> (lambda S_dim, lambda kappa)`.

## Surviving Routes

- A4 parity-gate-to-CAR audit: test whether the primitive parity-gate carrier
  route supplies a stronger bridge to the native CAR/coframe response.
- Prove the missing A1 `P_A` Clifford/CAR module-morphism theorem.
- Add a minimal carrier/metrology axiom and keep `(C1)` conditional rather
  than promoted.

## Review Boundary

Safe wording:

> The A2 stretch attempt exposes an action-metrology import: retained
> dimensionless lattice normalizations (`g_bare`, `beta`, `u_0`, APBC) do not
> by themselves choose the dimensional action quantum on `P_A H_cell`.

Unsafe wording:

> The canonical plaquette/u_0 surface derives `hbar` or the absolute Planck
> action unit.

That stronger statement is blocked by the rescaling witness above.
