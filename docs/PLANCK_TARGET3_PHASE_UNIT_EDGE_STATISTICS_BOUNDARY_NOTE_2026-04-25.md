# Planck Target 3 Phase-Unit / Edge-Statistics Boundary Note

**Date:** 2026-04-25
**Status:** retained Target 3 boundary theorem on the **stripped Hilbert-only
surface**; positive dimensionless phase unit, negative absolute-action/CAR
derivation on the bare Hilbert-only surface
**Runner:** `scripts/frontier_planck_target3_phase_unit_edge_statistics.py`
**Resolved on the retained surface by:**
[`PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md)
-- on the framework's actual retained surface (Cl(3) on Z^3 + anomaly-time
+ time-locked event coframe), the metric-compatible Clifford coframe
response on `P_A H_cell` is forced, not assumed; the rank-four ambiguity
is removed and the primitive Clifford-CAR edge carrier closes
unconditionally.

## Purpose

Target 3 asks whether the one-axiom Hilbert/information-flow reduction can
derive one irreducible physical action/phase unit and connect it to the
gravity/action normalization. The Target 2 area-law packet sharpened the
question: if Target 3 can derive the primitive Clifford-Majorana/CAR
edge-statistics principle on `P_A H_cell`, then the last conditional premise
in the positive `c=1/4` horizon-entropy carrier is removed.

This note records the bounded result.

The current one-axiom surface does derive a native dimensionless phase unit:
the `U(1)` turn of Hilbert amplitudes. It does not derive an absolute
dimensional action unit, and it does not force the primitive CAR edge
statistics. Thus Target 3 is sharpened, not closed.

## The theorem

Let the accepted Target 3 input be the existing one-axiom Hilbert/information
flow surface:

```text
finite complex Hilbert space + local tensor/support structure
Hermitian sparse generator H
unitary flow U(t) = exp(-i H t)
```

and let the primitive horizon-active block be

```text
V = P_A H_cell,    dim H_cell = 16,    dim V = rank(P_A) = 4.
```

Assume no additional spin-statistics, reflection-positivity, local-Lorentz, or
primitive Majorana/CAR edge-response axiom.

Then:

1. the one-axiom surface supplies a dimensionless phase unit, namely
   `theta in R / 2 pi Z`;
2. it cannot fix an absolute dimensional action quantum `kappa`, because all
   amplitudes depend only on `S/kappa` and are invariant under
   `(S,kappa) -> (lambda S, lambda kappa)`;
3. it cannot derive the primitive CAR edge statistics, because the same
   rank-four Hilbert block `V ~= C^4` supports both the two-mode CAR/Fock
   semantics and non-CAR two-qubit or ququart semantics while satisfying the
   same Hilbert-flow axioms.

Therefore the current one-axiom information/action bridge cannot remove the
last conditional premise in Target 2. A positive Target 3 closure must add or
derive a stronger edge-statistics/action-unit principle.

## Lemma 1: the native unit is phase, not dimensional action

Hilbert amplitudes are complex. Their intrinsic phase lives in

```text
U(1) ~= R / 2 pi Z.
```

If a path or local action variable contributes to an amplitude, the invariant
object has the form

```text
exp(i S/kappa).
```

Thus the one-axiom surface naturally gives an irreducible dimensionless phase
unit: one full `U(1)` turn. This is real structure. It is not yet an SI or
dimensional value of `hbar`.

Proof: for any integer `n`,

```text
exp(i(theta + 2 pi n)) = exp(i theta).
```

All projective Hilbert predictions are functions of this phase class. The
runner checks the phase periodicity and the dependence on `S/kappa`.

## Lemma 2: the absolute action scale is rescaling-invariant

For any positive scale `lambda`,

```text
exp(i (lambda S)/(lambda kappa)) = exp(i S/kappa).
```

The same obstruction appears in Hamiltonian form:

```text
exp(-i (lambda H)(t/lambda)) = exp(-i H t).
```

Adding a scalar action density also changes only a global phase:

```text
exp(-i(H + a I)t) = exp(-iat) exp(-iHt).
```

So the internal Hilbert-flow data fix a dimensionless phase history, not the
absolute conversion from that phase history to a dimensional action unit. A
physical clock/source/metrology map, or a separate normalization theorem, is
needed to name a particular dimensional `kappa`.

This is consistent with the older finite-response obstruction: finite static
matrices cannot realize an exact nonzero canonical commutator

```text
[X,P] = i kappa I
```

because `Tr([X,P]) = 0` while `Tr(i kappa I) != 0` for `kappa != 0`.

## Lemma 3: rank-four Hilbert flow does not force CAR statistics

The primitive active block has the right dimension for two complex CAR modes:

```text
dim F(C^2) = 2^2 = 4 = rank(P_A).
```

On `V ~= C^2 otimes C^2`, define

```text
c_0 = sigma_- otimes I,
c_1 = Z otimes sigma_-.
```

These obey

```text
{c_i,c_j} = 0,
{c_i,c_j^dagger} = delta_ij I.
```

The four Majoranas

```text
gamma_0 = c_0 + c_0^dagger,
gamma_1 = -i(c_0 - c_0^dagger),
gamma_2 = c_1 + c_1^dagger,
gamma_3 = -i(c_1 - c_1^dagger)
```

obey the complex Clifford relations and generate `M_4(C)`. This is exactly
the primitive Clifford-Majorana/CAR edge semantics used by the positive
Target 2 carrier theorem.

But the same Hilbert block also supports non-CAR semantics. For example,

```text
X otimes I,    I otimes X
```

are commuting two-qubit spin factors, not CAR generators. The ququart
clock-shift pair also gives a valid `C^4` Hilbert system:

```text
Z_4 X_4 = i X_4 Z_4.
```

These alternatives satisfy the same finite Hilbert-space and unitary-flow
requirements. They can even use the same Hermitian matrix `H` and the same
unitary `exp(-iHt)`. The matrix algebra alone is `M_4(C)` in each case; the
CAR odd/even grading and anticommutation semantics are extra structure.

Thus:

```text
rank(P_A)=4 + Hilbert flow + locality
```

does not imply

```text
primitive edge = irreducible Clifford-Majorana/CAR edge.
```

## Consequence for Target 2

The Target 2 status remains exactly conditional:

```text
if primitive Clifford-Majorana/CAR edge statistics are native,
then the primitive parity-gated carrier gives c_Widom = 1/4;
otherwise the positive Target 2 bridge has not been promoted.
```

This note does not weaken the Target 2 positive carrier. It identifies which
part Target 3 still has to derive.

## Consequence for Target 3

The current one-axiom bridge reaches the following boundary:

```text
Hilbert/information flow  ->  U(1) phase unit
Hilbert/information flow  -/-> absolute dimensional action quantum
Hilbert/information flow  -/-> primitive CAR edge statistics
```

The positive route is therefore not obtained by bare Hilbert flow. It is the
conditional bridge in
`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`: if the
primitive active block carries the metric-compatible Clifford/coframe response,
then metric compatibility gives the `Cl_4` anticommutator on `P_A H_cell`, and
the rank-four irreducible module is equivalent to two-mode CAR.

Before the Clifford bridge was added, a positive Target 3 theorem had to do at
least one of the following:

1. derive irreducible Clifford-Majorana/CAR edge statistics from a stronger
   native principle, such as a lattice spin-statistics theorem, reflection
   positivity plus local horizon orientation, or a local Lorentz/Majorana
   response law;
2. derive the physical action unit by adding a real clock/source/metrology map
   that breaks the `(S,kappa)` rescaling degeneracy;
3. state the primitive edge-statistics principle as an added carrier axiom and
   keep Target 3 as a separate open normalization lane.

The Clifford bridge follows the first route on the retained package surface.

## Package wording

Safe wording:

> The one-axiom Hilbert/information-flow bridge supplies a native dimensionless
> `U(1)` phase unit. On its current surface it does not derive either the
> absolute dimensional action quantum or the primitive Clifford-Majorana/CAR
> edge statistics required to make the Target 2 `c=1/4` carrier unconditional.

Unsafe wording:

> The one-axiom bridge alone derives `hbar` and the primitive CAR horizon
> carrier.

That stronger statement is blocked by the rescaling and rank-four semantics
underdetermination above.

## Verification

Run:

```bash
python3 scripts/frontier_planck_target3_phase_unit_edge_statistics.py
```

The runner checks:

1. the primitive `4/16 = 1/4` active trace;
2. `U(1)` phase periodicity;
3. dependence of amplitudes only on `S/kappa`;
4. invariance under `(S,kappa)` rescaling;
5. invariance under inverse `H`/`t` rescaling;
6. global-phase behavior of scalar action shifts;
7. the finite commutator trace obstruction;
8. two-mode CAR on the rank-four active block;
9. Clifford-Majorana generation of `M_4(C)`;
10. CAR parity grading;
11. non-CAR two-qubit semantics on the same block;
12. non-CAR ququart clock-shift semantics on the same block;
13. identical unitary matrix flow under CAR and non-CAR readings;
14. the final Target 3 boundary verdict.
