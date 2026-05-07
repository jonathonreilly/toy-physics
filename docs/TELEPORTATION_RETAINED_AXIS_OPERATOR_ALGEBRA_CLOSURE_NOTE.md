# Retained-Axis Operator Algebra Closure Note

**Date:** 2026-05-07
**Type:** bounded algebraic theorem
**Claim type:** bounded_theorem
**Status:** bounded source support for the finite Retained-Axis Operator
Algebra (RALA) surface. This note does not set audit verdicts or effective
status for the three referenced gates.
**Runner:** `scripts/frontier_teleportation_retained_axis_operator_algebra_closure.py`

## Scope

This note coordinates the algebraic closure of three previously open gates in
the teleportation suite:

  - `docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md`
  - `docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md`
  - `docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md` (T1, T2, T4 axiom
    consequences only)

The closure is finite, algebraic, and bounded. It does not claim a physical
apparatus, durable measurement record, dynamical preparation, noise model,
matter transfer, charge transfer, energy transfer, object transport, or
faster-than-light signaling. Those remain open in their own gates.

## Setup

Use the Kogut-Susskind cell/taste decomposition on a hypercubic lattice with
even side `L = 2 C` in dim `d`. Site coordinates `x_i = 2 c_i + eta_i` with
`c_i in {0,...,C-1}` and `eta_i in {0,1}`. The single-site Hilbert space
factorizes as

```text
H_site = C^cells (x) C^tastes,
n_cells = C^d,    n_tastes = 2^d.
```

Pick a retained taste axis `a in {0,...,d-1}`. The logical bit is
`b = eta_a`; the environment label is `e = (c, {eta_i : i != a})`. Define

```text
RALA(a) = { O_logical (x) I_env : O_logical in M_2(C) }.
```

This is the *Retained-Axis Operator Algebra* (RALA). RALA(a) acts trivially
on the environment factor — by construction every element factors as a 2x2
block on the retained logical bit times the identity on cells and spectator
taste bits.

## Theorems

### T1 (RALA closure)

RALA(a) is a *-subalgebra of operators on the single-site Hilbert space. It
is closed under
  - linear combinations,
  - operator products,
  - Hermitian conjugation,
  - tensor products with copies of itself (yielding RALA on multi-register
    states under the appropriate basis ordering).

*Proof.* `(O1 (x) I) + alpha (O2 (x) I) = (O1 + alpha O2) (x) I`,
`(O1 (x) I)(O2 (x) I) = (O1 O2) (x) I`, and `(O (x) I)^dag = O^dag (x) I`.
Tensor products: `(O1 (x) I_envA) (x) (O2 (x) I_envB) = (O1 (x) O2) (x)
(I_envA (x) I_envB)` after reordering tensor factors. □

### T2 (axis Pauli operators are in RALA)

The retained-axis logical Z and X operators

```text
Z_axis = (taste sigma_z on eta_a) (x) I_(other axes & cells)
X_axis = (taste sigma_x on eta_a) (x) I_(other axes & cells)
```

are in RALA(a), with projected logical operators equal to `sigma_z` and
`sigma_x`.

*Proof.* By construction each operator acts only on the `eta_a` slot. Block
projection onto each `e` gives the same `sigma_z` (or `sigma_x`) on the
logical bit. □

### T3 (axis Bell projectors are in pair-RALA)

The four ideal axis Bell projectors

```text
P_zx^axis = (1/4) (I + (-1)^x Z_axis^A Z_axis^B) (I + (-1)^z X_axis^A X_axis^B),
            (z, x) in {0,1}^2,
```

defined on a two-register Hilbert space, are in the pair-RALA
`RALA(a) (x) RALA(a)` (after appropriate basis ordering). Each `P_zx^axis`
projects onto the logical 2-qubit Bell state `|beta_zx>` tensor identity on
the environment-pair, the four projectors form a partition of unity, are
mutually orthogonal, and idempotent.

*Proof.* `Z_axis^A Z_axis^B = (sigma_z (x) I_envA) (x) (sigma_z (x) I_envB)
= (sigma_z (x) sigma_z) (x) (I_envA (x) I_envB)`, similarly for XX. So
each Bell projector is `P_logical (x) I_env_pair` with `P_logical = (1/4)(
I + (-1)^x ZZ_logical)(I + (-1)^z XX_logical) = |beta_zx><beta_zx|`. □

### T4 (native-Z obstruction)

Native sublattice parity `Z_native = xi_5 = product_i sigma_z^{(eta_i)}`
acts diagonally as `Z_native|x> = (-1)^(sum_i eta_i)|x>`. On each
environment block,

```text
Z_native|_e = sigma_s Z_logical,    sigma_s = (-1)^(sum_{i != a} eta_i).
```

For dim `d > 1`, two environment sectors `s = (0,...,0)` and
`s = (1, 0, ..., 0)` give opposite signs. Therefore `Z_native` cannot equal
any single `O_logical (x) I_env` and is not in RALA. The Frobenius
projection of `Z_native` onto RALA is the environment average

```text
Pi(Z_native) = (1 / n_env) sum_e sigma_s Z_logical
             = Z_logical (1 / 2^(d-1)) sum_s (-1)^|s|
             = 0    for d > 1.
```

The relative residual is `1.000` (full operator norm).

For `d = 1`, the spectator tuple is empty, so `sigma_s = 1` and
`Z_native = Z_logical (x) I_env`, i.e., `Z_native in RALA(0)`.

### T5 (fixed pair-hop X membership)

The "current fixed pair-hop X" used by previous teleportation runners is
`X_fixed = I_cells (x) sigma_x on the last taste axis (eta_{d-1})`. Then

```text
X_fixed in RALA(a) iff a = d - 1.
```

*Proof.* If `a = d - 1`, `X_fixed = X_axis`, in RALA(a) by T2. If
`a != d - 1`, `X_fixed` flips `eta_{d-1}` while leaving `eta_a` unchanged;
it maps each encoded basis state `|b>_logical (x) |s>_env` to
`|b>_logical (x) |s'>_env` with `s'_{d-1} = 1 - s_{d-1}`, an orthogonal env
state. Therefore each block restriction of `X_fixed` to a fixed-env
2-dimensional encoded subspace is zero, the average projection is zero, and
the relative residual is `1.000`. □

### T6 (base/fiber separation; transport theory T1)

Every `C in RALA(a)` commutes with every `I_logical (x) L_env` ledger
observable on the same site:

```text
[C, I_logical (x) L] = 0  for every L on the env factor.
```

*Proof.* `C = O (x) I_env`; `I_logical (x) L = (I_2 (x) L)`. So
`C (I_logical (x) L) = O (x) L = (I_logical (x) L) C`. □

Thus a Bob correction in RALA(a) cannot change the value of any
base-ledger observable on the same site. This is precisely T1 of the
native transport theory note: corrections live in `A_F`, ledgers in `L_B`,
and `[C_B, L] = 0`.

### T7 (Pauli XOR composition; transport theory T2)

The four single-register axis Paulis `{ I_n, Z_axis, X_axis, Z_axis X_axis }`
form a Z_2 x Z_2 group under operator product up to phase. Specifically,
labeling each by `(z, x) in {0,1}^2` such that the logical operator is
`Z^z X^x`,

```text
(Z^z1 X^x1) (Z^z2 X^x2) = phase * Z^(z1 xor z2) X^(x1 xor x2),
```

where `phase in {+1, -1, +i, -i}`. This is the Bell-frame Z_2 x Z_2
connection algebra of the native transport theory T2.

### T8 (RALA teleportation closure)

Choose a fixed environment label `e0`. Define encoded basis states
`|b_L> = |b>_logical (x) |e0>_env` and the encoded Bell resource
`|Phi+>_AR_B = (|0_L 0_L> + |1_L 1_L>)/sqrt(2)`. Run the standard qubit
teleportation protocol with axis Bell projectors `P_zx^axis` and Pauli
corrections `U_zx = X_axis^x Z_axis^z`. Then for every input state
`|psi>_logical = alpha|0> + beta|1>`:

  (a) each Bell branch has probability exactly `1/4`;
  (b) the four branch probabilities sum to `1`;
  (c) Bob's pre-record marginal density matrix on the encoded subspace is
      independent of the input;
  (d) after the corresponding Pauli correction, Bob's encoded state has
      fidelity `1` with the input on every branch.

*Proof.* By T2, T3, T6, and the standard teleportation calculation. The
encoded basis is two-dimensional, RALA(a) acts on this subspace as the full
M_2(C) algebra of single-qubit Paulis, the encoded Bell state is the
standard Bell resource on this 2-qubit logical space, and the axis Bell
projectors equal the standard Bell projectors on it. The standard textbook
identity

```text
(P_zx^axis (x) I_B) [|psi>_A (x) |Phi+>_RB]
  = (1/2) |beta_zx>_AR (x) (Z^z X^x |psi>)_B
```

then applies, giving branch probability `1/4` and corrected fidelity `1`. □

## Verification

The runner enumerates every `(dim, side, retained_axis)` triple in
`{1,2,3} x {2,4} x {0,...,d-1}` (12 cases for axes-all) and verifies all
eight theorems numerically. Each PASS uses 2x2 block projection and
operator-norm residuals at tolerance `1e-12`.

Default observed run:

```text
PASS=96 FAIL=0    (dims=1,2,3, sides=2,4, all axes)
```

Sample output (dim=3, side=4, retained_axis=2 — the standard prior-runner
configuration):

```text
PASS  T1 RALA closure: all 7 closure checks pass
PASS  T2 axis-Z/axis-X in RALA: matches sigma_z and sigma_x
PASS  T3 axis-Bell projectors in pair-RALA: pair-RALA residual 0, partition sum = I, mutually orthogonal idempotent
PASS  T4 native-Z obstruction: not_in_rala, Frobenius projection = 0, relative residual = 1.000
PASS  T5 fixed pair-hop X: in_rala (a = d-1) and matches sigma_x
PASS  T6 base/fiber separation: max commutator norm = 0
PASS  T7 Pauli XOR composition: closed Z_2 x Z_2 algebra up to phase
PASS  T8 RALA teleportation closure: min fidelity = 1.0, branch probabilities = 1/4, pre-record marginal input-independent
```

## What This Supports

The RALA theorem supplies bounded algebraic support for three previously open
teleportation gates in the following finite sense. Independent audit must
decide any later status change.

### Gate 1: Encoding portability (T5)

The encoding portability note documents that the existing
`current_fixed_x = row-major pair-hop` operator equals the retained-axis
logical X only when the retained axis is the last taste axis. T5 supplies
the algebraic necessary-and-sufficient condition: `current_fixed_x` is an
element of `RALA(a)` iff `a = d - 1`.

This is structural support. The earlier note enumerated the result; this
theorem characterizes it as RALA membership and proves it algebraically.

### Gate 2: Taste readout/operator model (T1, T2, T4)

The taste readout note documents that native sublattice parity Z is not
taste-only in dim > 1 because of `xi_5` spectator dependence. T1 + T2 + T4
supply the algebraic structure: the retained operator algebra RALA(a) is
the *unique* closed *-subalgebra of single-site operators that factors as
`O_logical (x) I_env`; native-Z is in this algebra iff dim = 1, and the
finite block-decomposition argument is now framework-cited rather than
case-by-case.

The "operational conditions for ignoring cells/spectators" listed at the end
of that note are precisely the conditions for restricting the protocol's
preparation, readout, and Bell measurement operators to RALA(a). The
RALA-only protocol (T8) realizes those conditions algebraically.

### Gate 3: Native transport theory (T1, T2 axiom consequences only)

The native transport theory note proposes T1 (base/fiber separation),
T2 (Bell connection), T3 (causal record section), T4 (flatness or recorded
holonomy), T5 (branch records as gauge data), and T6 (preparation
curvature). The RALA theorem supplies bounded algebraic support for the
*algebraic content* of T1 and T2:

  - T1 base/fiber separation is realized exactly by RALA(a): every
    correction commutes with every base-ledger observable (T6 of this
    note).
  - T2 Bell connection is realized exactly by the four axis Bell
    projectors `P_zx^axis`, which form a partition of unity, project to
    the four Bell sectors of the logical 2-qubit subspace, and compose via
    XOR up to phase (T3 + T7 of this note).

T3 (causal record section), T4 (loop holonomy bookkeeping), T5 (branch
records), and T6 (preparation curvature) of the transport theory note
require physical content beyond the RALA algebra — they are not resolved by
this theorem.

## What Remains Open

The following gates are *not* resolved by RALA and remain open:

  - `TELEPORTATION_3D1_CAUSAL_RECORD_CHANNEL_NOTE` — needs a derived
    record carrier and apparatus (transport theory T3).
  - `TELEPORTATION_3D_INITIAL_RAMP_PROBE_NOTE` — needs a scalable native
    G=0 preparation, control/noise, and readout proof.
  - `TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE` — needs a physical
    native gate schedule with quantified imperfections.
  - `TELEPORTATION_LOGICAL_READOUT_AUDIT` — needs a native apparatus
    proven blind to environment labels under finite-time noise.

The RALA theorem supplies the *algebraic backbone* shared by all four; the
*physical implementation* of the axis primitives remains genuinely deep
research.

## Limitations

  - Finite-grid algebraic theorem only: dims 1, 2, 3 and sides 2, 4 are
    audited; the proofs go through for any even side and any dim, but are
    not exhaustively numerically verified beyond the audited surface.
  - The `O_logical` projection used by the runner is the trace average over
    the environment block; the residual norm is the standard Frobenius
    distance to the projected operator. This is exact for diagonal
    environment structure (which RALA elements automatically have); for a
    general operator the projection captures only the RALA-component.
  - The RALA-only protocol uses ideal axis Bell projectors and ideal Pauli
    corrections. No physical detector, pulse sequence, decoherence model,
    or fault-tolerant primitive is constructed.
  - The Bell resource is supplied by an encoded `|Phi+>` on a fixed
    environment; deriving the resource from native dynamics remains an
    open gate.
  - Scope remains ordinary qubit teleportation. No matter, mass, charge,
    energy, or object transport, and no faster-than-light signaling, is
    claimed.

## Audit boundary

Claim type: `bounded_theorem`. The source content is the finite algebraic
theorem set T1-T8 above. RALA(a) is the *-subalgebra of single-site
operators on the KS-decomposed Hilbert space whose elements act trivially on
the environment; the standard teleportation primitives sit inside it exactly
when the retained-axis matches; and this is algebraic support shared across
the physical-implementation gates listed above. Effective status is
pipeline-derived after independent audit.
