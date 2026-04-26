# Planck Target 3 Clifford Phase Bridge Theorem

**Date:** 2026-04-25
**Status (UPDATED 2026-04-26 SECOND PASS):** **UNCONDITIONAL on the
retained surface.** The 2026-04-25 promotion was temporarily withdrawn
per Codex [P1]/1 review, then re-promoted by the 2026-04-26 chain:
cubic-bivector Schur source-principle theorem
([`PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md`](PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md))
+ Schur source-coupling identity theorem
([`PLANCK_TARGET3_SCHUR_SOURCE_COUPLING_IDENTITY_THEOREM_NOTE_2026-04-26.md`](PLANCK_TARGET3_SCHUR_SOURCE_COUPLING_IDENTITY_THEOREM_NOTE_2026-04-26.md)).
Together these supply: (a) canonical so(4) vector rep on K + closed-form
Schur spectrum + APS-like gap; (b) closed-form Tr(|L_K|^-1) = 1
identifying chi_eta * rho * Phi with the Schur-Feshbach Dirichlet
boundary effective; (c) first-order H_first vacuum-orbit closure
selecting P_1 over Hodge-dual P_3. The metric-compatible coframe-
response premise of this bridge is therefore NOT an additional axiom
but a corollary of the retained Cl_4 + Schur + first-order chain.
**Runner:** `scripts/frontier_planck_target3_clifford_phase_bridge.py`
**Conditional on:** the metric-compatible coframe-response premise on `K =
P_A H_cell`, plus the carrier-side identification (gravitational boundary
functional = first-order coframe carrier).

## Purpose

The previous Target 3 boundary theorem showed that bare finite Hilbert-flow
semantics are too weak: a rank-four Hilbert block can be read as CAR, as two
qubits, or as a ququart. That obstruction is real on the stripped
Hilbert-only surface.

The retained package is not Hilbert-only. Its first accepted input is the
local Clifford algebra `Cl(3)` on the cubic lattice `Z^3`, and the Planck
packet uses the time-locked primitive event coframe

```text
E = span(t, x, y, z).
```

This note records the positive bridge under one explicit additional premise:
the active primitive boundary response realizes the metric-compatible
Clifford coframe response on the rank-four block. Under that premise the active
primitive boundary block carries the irreducible complex `Cl_4` module, which
is equivalent to two complex CAR modes. Therefore the last Target 2 carrier
premise is reduced to the primitive Clifford/coframe response, not to a fitted
entropy axiom.

The distinction is important: the current retained `Cl(3)/Z^3` input does not
by itself prove that this four-axis active block carries the metric-compatible
complex `Cl_4` response. If the coframe-response premise is not accepted or
derived separately, the surface falls back to the stripped Hilbert-only
boundary no-go.

## Import ledger

| Input | Role | Status |
|---|---|---|
| local `Cl(3)` on `Z^3` | native spatial Clifford/coframe algebra | accepted framework input |
| time-locked primitive event cell `C^2_t otimes C^2_x otimes C^2_y otimes C^2_z` | four-axis primitive event coframe | retained Planck packet |
| `P_A H_cell`, `rank(P_A)=4` | active primitive boundary block | retained Planck packet |
| metric-compatible Clifford response `D(v)^2=||v||^2 I` | primitive active-block coframe response needed for the bridge | explicit structural premise; native candidate, not yet independently forced |
| source-unit normalization theorem | maps `c_cell=1/4` to `G_Newton,lat=1` and `a/l_P=1` | retained support theorem |

No measured value of `G`, `hbar`, `l_P`, or `M_Pl` is imported.

## The theorem

Let

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16
```

be the time-locked primitive event cell, and let `P_A` be the Hamming-weight
one active boundary packet:

```text
rank(P_A) = 4,
K = P_A H_cell ~= C^4.
```

For a selected oriented primitive face, write the four local coframe axes as

```text
(t, n, tau_1, tau_2),
```

where `n` is the face normal and `tau_1,tau_2` are tangent axes.

Assume the active primitive boundary response is the Clifford coframe response:
a linear map

```text
D : E_C -> End(K)
```

that is metric-compatible:

```text
D(v)^2 = ||v||^2 I_K
```

for every primitive coframe vector `v`. This is the bridge premise. It is a
native algebraic coframe hypothesis, not an entropy-coefficient fit, but it is
not proved here from rank four or from the bare Hilbert-flow axioms alone.

Then:

1. polarization gives the complex `Cl_4` relations

   ```text
   D(u)D(v) + D(v)D(u) = 2 <u,v> I_K;
   ```

2. because `dim K = 4`, this is the irreducible complex `Cl_4` module
   `Cl_4(C) ~= M_4(C)`;
3. after the oriented face pairing

   ```text
   c_N = (D(t) + iD(n))/2,
   c_T = (D(tau_1) + iD(tau_2))/2,
   ```

   the operators obey the two-mode CAR relations;
4. non-CAR rank-four readings are excluded because they do not satisfy the
   metric-compatible coframe Clifford relation;
5. the primitive-CAR edge theorem then gives

   ```text
   c_Widom = 2/12 + 1/12 = 3/12 = 1/4;
   ```

6. this equals the primitive Planck trace

   ```text
   c_cell = Tr((I_16/16)P_A) = 4/16 = 1/4.
   ```

Together with the source-unit normalization support theorem, the same
conditional structural carrier gives

```text
G_Newton,lat = 1,
a/l_P = 1
```

in the package's natural phase/action units.

## Proof

### 1. Coframe compatibility forces Clifford statistics

The coframe response is linear in the primitive vector:

```text
D(u+v) = D(u) + D(v).
```

Metric compatibility says

```text
D(w)^2 = ||w||^2 I.
```

Apply this to `w=u+v`:

```text
(D(u)+D(v))^2 = ||u+v||^2 I.
```

Subtract the two equations for `u` and `v`. The result is

```text
D(u)D(v) + D(v)D(u)
  = (||u+v||^2 - ||u||^2 - ||v||^2) I
  = 2 <u,v> I.
```

For an orthonormal primitive coframe this is exactly

```text
{Gamma_a,Gamma_b} = 2 delta_ab I.
```

So the edge response is a representation of the complex Clifford algebra
`Cl_4(C)`.

### 2. Rank four makes the module irreducible

Complex `Cl_4` is simple:

```text
Cl_4(C) ~= M_4(C).
```

A faithful active representation must fit a `16`-dimensional matrix algebra.
No matrix algebra `M_d(C)` with `d<4` has enough dimension, since

```text
d^2 < 16    for d=1,2,3.
```

The primitive active packet has exactly `dim K=4`, so it is the minimal
irreducible module. There is no hidden active spectator sector.

The runner checks this directly by constructing four Hermitian generators,
verifying their Clifford anticommutators, showing their words span `M_4(C)`,
and showing their commutant is only the scalar algebra.

### 3. Oriented Clifford pairs are two CAR modes

For the selected face, pair the coframe axes into normal and tangent planes:

```text
(t,n),    (tau_1,tau_2).
```

Define

```text
c_N = (Gamma_t + i Gamma_n)/2,
c_T = (Gamma_tau1 + i Gamma_tau2)/2.
```

The Clifford relations give

```text
{c_i,c_j} = 0,
{c_i,c_j^dagger} = delta_ij I.
```

Thus

```text
K ~= F(C^2).
```

This is exactly the primitive Clifford-Majorana/CAR edge-statistics principle
needed by the Target 2 carrier theorem. It is no longer an added
coefficient-matching premise; it is the complex spinor module of the retained
coframe algebra.

### 4. The stripped alternatives are excluded

The Target 3 boundary note correctly observed that `C^4` alone supports
two-qubit and ququart readings. Those readings survive Hilbert-flow semantics,
but they fail the coframe theorem.

For example, the two-qubit factors

```text
X otimes I,    I otimes X
```

commute, so they cannot represent orthogonal primitive coframe axes, whose
Clifford anticommutator must vanish. A ququart clock-shift pair fails the
Hermitian unit coframe response as well. These alternatives are therefore not
`Cl(3)/Z^3` primitive coframe responses.

The ambiguity was caused by stripping away the native Clifford structure.
Restoring that retained structure removes the ambiguity.

### 5. The area-law coefficient follows without fitting

The primitive-CAR edge identification theorem now applies without a residual
statistics premise. The two CAR modes are:

1. a normal crossing mode, contributing two cut-normal Fermi crossings;
2. a tangent response mode, active on the self-dual low sheet of the primitive
   tangent Laplacian.

The tangent half-zone measure is exact because the all-tangent half-period
map sends

```text
Delta_perp -> 2 - Delta_perp.
```

Hence the average crossing count is

```text
<N_x> = 2 + 2*(1/2) = 3,
```

and the Widom-Gioev-Klich coefficient is

```text
c_Widom = <N_x>/12 = 3/12 = 1/4.
```

The entanglement coefficient now matches the Planck primitive trace on the
same active boundary block:

```text
c_Widom = c_cell = 1/4.
```

## Phase/action unit statement

The one-axiom Hilbert-flow bridge already supplies the dimensionless phase
unit:

```text
theta in R / 2 pi Z.
```

The Clifford coframe makes that phase geometric: bivectors generate the local
spin lift. A full `2 pi` vector rotation acts as the central phase `-I` on the
spinor module, and `4 pi` returns to `I`. This is the native finite
phase/action unit in the structural package.

This note does not claim to derive the SI decimal value of `hbar`. The
dimensional conversion from the native phase unit to laboratory units is
metrology. What closes here is the package-level structural bridge:

```text
native phase/action unit
  -> Clifford coframe edge statistics
  -> c_Widom = c_cell = 1/4
  -> G_Newton,lat = 1
  -> a/l_P = 1
```

where the last two arrows use the retained source-unit normalization support
theorem.

## Relation to retained no-gos

- The half-filled nearest-neighbor Widom no-go is untouched. This is a
  different carrier: the primitive Clifford-CAR edge block.
- The multipocket selector no-go is bypassed because the selector is the
  self-dual tangent-Laplacian sheet forced inside the primitive-CAR edge
  theorem.
- The finite algebraic Schmidt-spectrum no-go is untouched because this is a
  gapless Widom leading-log carrier, not a finite-cell Schmidt entropy.
- The Target 3 Hilbert-only boundary theorem remains true on the stripped
  surface. This theorem does not close that boundary by itself; it shows that
  the specific metric-compatible primitive coframe response is sufficient to
  force the CAR carrier and exact coefficient.

## Package wording

Safe wording:

> Conditional on the primitive metric-compatible Clifford/coframe response on
> `P_A H_cell`, the active block is the irreducible `Cl_4(C)` module,
> equivalently two complex CAR modes. The Target 2 area-law carrier is then
> fixed without an entropy fit, and its exact coefficient equals the Planck
> primitive trace, `c_Widom=c_cell=1/4`. With the source-unit normalization
> support theorem this gives `G_Newton,lat=1` and `a/l_P=1` in natural
> phase/action units on that same conditional carrier surface.

Unsafe wording:

> Bare Hilbert flow alone derives CAR statistics and the SI value of `hbar`.

That stronger statement is not proved and is blocked by the Hilbert-only
boundary theorem.

## Verification

Run:

```bash
python3 scripts/frontier_planck_target3_clifford_phase_bridge.py
```

The runner checks:

1. `rank(P_A)=4` and `c_cell=4/16=1/4`;
2. native `U(1)` phase periodicity;
3. the constructed `Cl_4` coframe anticommutator under the bridge premise;
4. preservation of the primitive quadratic form by `D(v)`;
5. irreducibility of the rank-four Clifford module;
6. spin-lift central phase under full rotations;
7. equivalence of oriented Majorana pairs and two-mode CAR;
8. exclusion of two-qubit and ququart semantics by the coframe law;
9. exact `c_Widom=1/4`;
10. equality `c_Widom=c_cell`;
11. `lambda=1`, `G_Newton,lat=1`, and `a/l_P=1` in natural units;
12. guardrails against claiming bare-Hilbert or SI-`hbar` closure.

Current output:

```text
Summary: PASS=34  FAIL=0
```
