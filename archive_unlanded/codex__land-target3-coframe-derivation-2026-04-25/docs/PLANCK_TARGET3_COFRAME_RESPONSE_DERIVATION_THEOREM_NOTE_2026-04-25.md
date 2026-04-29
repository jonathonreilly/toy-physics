# Planck Target 3 Coframe Response Derivation Theorem

**Date:** 2026-04-25
**Status:** conditional structural support theorem on an explicit
time-locked `Cl(3)/Z^3` coframe-response surface; not a Hilbert-only theorem,
not a proof that rank four alone forces CAR, and not an SI decimal derivation
of `hbar`
**Runner:** `scripts/frontier_planck_target3_coframe_response_derivation.py`

## Purpose

The reviewed Target 3 Clifford bridge left one explicit hinge:

```text
D(v)^2 = ||v||^2 I    on    K = P_A H_cell.
```

That hinge was intentionally not proved by rank four alone. A bare
four-dimensional Hilbert block can be interpreted as CAR, two qubits, or a
ququart. The missing input had to come from retained `Cl(3)/Z^3` primitive
coframe physics.

This note supplies a concrete coframe-response route and proves the square law
after the following explicit time-locked coframe assumptions are accepted:

1. the spatial primitive coframe response is the retained `Cl(3)` algebra;
2. the time-locked primitive event cell supplies a `Z_2` grading;
3. first-order staggered-Dirac primitive steps are grading-odd;
4. the grading-even time-space bivectors recover the retained spatial `Cl(3)`
   readout.

Those facts force the rank-four active module and the four primitive coframe
generators. The metric-compatible square law is then a theorem **inside this
coframe-response surface**. The remaining scientific boundary is the
provenance of that surface from the minimal stack; this note does not claim
that bare Hilbert/rank data alone supplies it.

## The theorem

Let `S ~= C^2` be the irreducible complex spatial spinor for the retained
spatial Clifford algebra:

```text
{sigma_i, sigma_j} = 2 delta_ij I_S,    i,j in {x,y,z}.
```

Let `T ~= C^2` be the time-lock grading space with grading `tau_z`. The
time-locked primitive event cell has active boundary packet

```text
K = P_A H_cell,    dim K = rank(P_A) = 4.
```

Identify `K` with the minimal time-locked spinor module

```text
K ~= T otimes S.
```

This identification is unique up to unitary equivalence once the time-lock
doubling and spatial spinor readout premises are imposed, because the active
packet has exactly the minimal dimension required below.

Assume the explicit first-order primitive coframe-response surface:

1. primitive one-step coframe operators are odd under the time-lock grading;
2. the time axis is the spatial-scalar odd flip;
3. the even time-space bivectors restrict on each time-lock sheet to the
   retained spatial `Cl(3)` generators.

Then, up to unitary equivalence,

```text
Gamma_t = tau_x otimes I,
Gamma_i = tau_y otimes sigma_i,    i=x,y,z.
```

Therefore for every primitive coframe vector

```text
v = v_t e_t + v_x e_x + v_y e_y + v_z e_z
```

the active coframe response

```text
D(v) = v_t Gamma_t + v_x Gamma_x + v_y Gamma_y + v_z Gamma_z
```

satisfies

```text
D(v)^2 = (v_t^2 + v_x^2 + v_y^2 + v_z^2) I_K.
```

Equivalently, as a compressed operator on the primitive event cell,

```text
D_cell(v)^2 = ||v||^2 P_A.
```

This proves the coframe-response premise used by the Target 3 Clifford bridge
conditional on the stated coframe/time-lock surface.

## Proof

### 1. Spatial `Cl(3)` is retained

The retained local algebra gives three spatial primitive coframe generators
on the irreducible spatial spinor:

```text
sigma_x, sigma_y, sigma_z,
```

with

```text
{sigma_i,sigma_j} = 2 delta_ij I.
```

No fourth independent unit coframe axis can be added on the same two
dimensional spinor: the only `2x2` matrix that anticommutes with all three
Pauli generators is zero. Therefore a time-locked four-axis first-order
coframe response forces a doubling.

### 2. Time-locking supplies exactly the required doubling

The primitive event cell has a time-lock bit. The first-order staggered-Dirac
step is odd with respect to that bit: a one-step primitive response changes
the time-lock parity, while even bivectors preserve it.

The unique spatial-scalar odd time flip is, up to phase,

```text
Gamma_t = tau_x otimes I.
```

The even time-space bivectors must recover the retained spatial coframe
readout. Thus define

```text
B_i = -i Gamma_t Gamma_i.
```

The retained readout condition is

```text
B_i = tau_z otimes sigma_i.
```

Solving for the odd spatial coframe steps gives

```text
Gamma_i = i Gamma_t B_i
        = tau_y otimes sigma_i.
```

So the four coframe generators are forced:

```text
Gamma_t = tau_x otimes I,
Gamma_i = tau_y otimes sigma_i.
```

This is the minimal doubled module `T otimes S`, and it has dimension `4`,
exactly matching `rank(P_A)`.

### 3. The square law follows

The Pauli relations give

```text
Gamma_t^2 = I,
Gamma_i^2 = I,
{Gamma_t,Gamma_i} = 0,
{Gamma_i,Gamma_j} = 2 delta_ij I.
```

Hence for

```text
D(v) = sum_a v_a Gamma_a
```

all mixed terms cancel and the diagonal terms remain:

```text
D(v)^2
  = sum_a v_a^2 I
  = ||v||^2 I.
```

This is the reviewed Target 3 coframe-response premise.

### 4. Compression to `P_A H_cell`

Let `W: C^4 -> H_cell` be the isometry whose columns are the four
Hamming-weight-one primitive event states:

```text
(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1).
```

Then

```text
W W^dagger = P_A,    W^dagger W = I_4.
```

Define the active-cell operator

```text
D_cell(v) = W D(v) W^dagger.
```

Then

```text
D_cell(v)^2 = ||v||^2 P_A.
```

So the square law holds directly on the active primitive boundary packet.

## Consequences

The reviewed Target 3 Clifford bridge has a precise positive support route:

```text
retained Cl(3) spatial response
  + time-lock grading
  + first-order staggered-Dirac oddness
  + spatial Cl(3) recovery in time-space bivectors
  -> D(v)^2 = ||v||^2 I on P_A H_cell.
```

Combining this theorem with the existing bridge gives, on that same conditional
coframe surface:

```text
P_A H_cell ~= irreducible Cl_4(C) module ~= F(C^2),
c_Widom = 3/12 = 1/4,
c_cell = 4/16 = 1/4,
c_Widom = c_cell.
```

If the source-unit normalization support theorem is also accepted on this same
conditional carrier, the package algebra gives:

```text
lambda = 4 c_cell = 1,
G_Newton,lat = 1,
a/l_P = 1
```

in natural phase/action units. This is a same-surface conditional map, not a
new SI metrology theorem.

## Scope Guardrails

This theorem does not say that a bare rank-four Hilbert space forces CAR. It
does not derive an SI decimal value of `hbar`. It uses the explicit
time-locked `Cl(3)/Z^3` staggered-Dirac coframe-response surface stated above;
the minimal-stack provenance of that surface remains the open scientific
boundary.

Safe wording:

> On the explicit time-locked `Cl(3)/Z^3` primitive coframe-response surface,
> the time-lock grading and spatial `Cl(3)` bivector readout force
> `D(v)^2=||v||^2 I` on `P_A H_cell`. Therefore the coframe/CAR premise in the
> Target 3 Clifford bridge is derived on that surface.

Unsafe wording:

> Rank four alone, or Hilbert flow alone, derives the Clifford/CAR horizon
> response.

That statement remains blocked by the Hilbert-only boundary theorem.

## Verification

Run:

```bash
python3 scripts/frontier_planck_target3_coframe_response_derivation.py
```

The runner checks:

1. `P_A` is the rank-four Hamming-weight-one active packet in `H_cell=C^16`;
2. the retained spatial Pauli generators satisfy `Cl(3)`;
3. no fourth unit coframe axis fits on the two-dimensional spatial spinor;
4. time-locking doubles the module to dimension four;
5. the time-space bivectors recover the spatial `Cl(3)` readout;
6. the odd coframe steps are forced from the time axis and bivectors;
7. the forced generators satisfy `Cl_4`;
8. `D(v)^2=||v||^2 I_K`;
9. the compressed active-cell operator obeys `D_cell(v)^2=||v||^2 P_A`;
10. two-qubit, ququart, and commuting-time alternatives fail the retained
    coframe square law;
11. the existing `c_Widom=c_cell=1/4` and `a/l_P=1` consequences follow.

Current output:

```text
Summary: PASS=27  FAIL=0
```
