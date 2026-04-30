# Planck Boundary Orientation Incidence No-Go

**Date:** 2026-04-30
**Status:** proposed_retained exact negative boundary; audit pending
**Runner:** `scripts/frontier_planck_boundary_orientation_incidence_no_go.py`
**Loop:** `physics-loop/planck-pa-retention-block01-20260430`

## Purpose

PR #228 left one repair target after the primitive Clifford-Majorana carrier
construction was audited as `audited_renaming`:

```text
derive a first-order boundary/orientation/incidence law
```

that selects

```text
P_1 = P_A
```

over its Hodge-dual rank-four partner

```text
P_3.
```

The previous two audit-ratified no-go artifacts already show:

```text
stated substrate symmetries -/-> unique P_A
stated substrate symmetries -/-> first-order P_1 over Hodge-dual P_3
```

This note tests the strongest remaining repair phrase directly: maybe an
oriented primitive four-cell boundary has incidence data that prefers normal
one-forms, and therefore forces `P_A`.

The result is negative. Oriented boundary incidence gives a perfect duality
between normal one-forms and oriented three-form faces. The normal/cochain
representation lives in `P_1`; the face/flux representation lives in `P_3`.
Hodge duality identifies them while preserving the same substrate structure.
Therefore boundary incidence does not select `P_A` unless one adds the missing
rule that normal cochains, rather than Hodge-dual faces, are primitive.

## Inputs Granted

The runner grants the same finite event-cell structure used by the PR #228
repair attempts:

- `H_cell ~= Lambda^* span(t,x,y,z) ~= (C^2)^4`;
- Hamming projectors `P_k`;
- the oriented Euclidean Hodge map on the primitive four-axis coframe;
- spatial `Cl(3)` spin-lift equivariance on `span(x,y,z)`;
- time parity, CPT grading, retained complex Hilbert structure, and
  tensor-local number operators.

Contextual neighbors, not load-bearing one-hop authorities for this note:

- `SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`;
- `FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`;
- `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`;
- `AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`;
- `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`.

The last two are useful as route context only. This note does not rely on
their audit status. Its load-bearing witness is finite-dimensional exterior
algebra on the primitive event cell.

No step uses `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, or any `alpha_LM` decoration chain.

## Theorem Statement

Let

```text
W = span(t,x,y,z),        H_cell ~= Lambda^* W.
```

Let `P_1` be the one-form sector and `P_3` the three-form sector. Let

```text
Omega = t wedge x wedge y wedge z
```

be the oriented primitive four-volume form. For each primitive axis `a`, the
oriented boundary face opposite `a` is

```text
i_{e_a} Omega = * e^a.
```

Therefore the oriented face-incidence data are exactly the Hodge image of the
normal one-form data:

```text
normal one-form carrier P_1  <-->  oriented face/flux carrier P_3.
```

The incidence pairing

```text
< *e^a, i_{e_b} Omega > = delta_ab
```

is perfect. It identifies the two rank-four carriers; it does not select one.

Consequently:

```text
oriented primitive boundary incidence -/-> P_1 = P_A.
```

Selecting `P_1` requires an additional cochain-normal primitivity rule, which
is exactly the missing first-order boundary/orientation premise.

## Derivation

### 1. Boundary Faces Are Hodge-Dual Normals

The oriented four-cell has one primitive normal covector per axis:

```text
e^t, e^x, e^y, e^z.
```

It also has one oriented complementary three-face per axis:

```text
*e^t, *e^x, *e^y, *e^z.
```

The runner constructs the Hodge map and verifies:

```text
* P_1 *^{-1} = P_3.
```

It also constructs the explicit face-incidence columns
`i_{e_a} Omega` and verifies that they equal `*e^a` with the oriented signs.

### 2. Incidence Is Nondegenerate But Not Selective

The normal/face pairing is the identity:

```text
< *e^a, i_{e_b} Omega > = delta_ab.
```

This is a perfect pairing between two rank-four spaces. A perfect pairing is
not a projector selector. It proves that the normal and face data carry the
same four labels and the same local information.

### 3. Substrate Symmetry Tests Are Preserved

The runner reuses the same spin/time/CPT/local tests as the prior forcing
attempts. Both `P_1` and `P_3` have zero equivariance error under:

- spatial `Cl(3)` spin-lift generators;
- time parity;
- CPT grading.

The local number algebra is also preserved:

```text
* n_a *^{-1} = 1 - n_a.
```

Thus `P_3` is not a nonlocal or symmetry-breaking representation of boundary
incidence. It is the local oriented-face representation.

### 4. Boundary-Only Variational Language Is The Same Premise

The first homogeneous response polynomial

```text
G_1(u) = sum_a u_a
```

maps to `P_1`. The Hodge-dual third homogeneous face polynomial

```text
G_3(u) = sum_a product_{b != a} u_b
```

maps to `P_3`. The runner verifies these two local projectors are Hodge-dual.

Therefore, on the boundary-incidence surface alone, "take the first derivative
with respect to `u_a`" selects `P_1` only after `u_a` has already been chosen
as the primitive cochain variable. That is a valid conditional coframe theorem,
but it is not a substrate-only derivation of the cochain choice.

This no-go does not analyze the stronger route where the accepted microscopic
staggered/Dirac action itself supplies the one-link source variables. That
route is recorded separately in
`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`.

### 5. Noether Current And Flux Language Does Not Rescue The Route

In four dimensions a conserved current can be represented either as a one-form
current `J` or as the Hodge-dual three-form flux `*J`. The conservation law can
be written in either representation. The runner verifies the carrier-level
fact needed here:

```text
rank(P_1) = rank(P_3) = 4,
P_3 = * P_1 *^{-1}.
```

Thus Noether/current words do not distinguish the carriers unless an
additional law says that the one-form current, not its flux form, is the
primitive boundary object.

## Stuck Fan-Out

This stretch attempt checked the orthogonal repair routes that are still
plausible after PR #228:

| Route | Result |
|---|---|
| oriented cubical boundary | gives Hodge-dual `P_1`/`P_3` equivalence |
| variational first derivative, boundary-only | selects `P_1` only after choosing cochain variables |
| Noether current | one-form current and three-form flux are dual |
| reflection-positive time | supplies no `P_1`/`P_3` carrier distinction |
| intrinsic active module | needs an active rank-four block before `Cl_4(C)` can act |

None supplies a substrate-only asymmetric selector.

## Consequence For The Planck Primitive Carrier Lane

The live state after this stretch attempt is:

```text
P_A is an allowed rank-four block.
P_3 is also an allowed rank-four block.
P_1 and P_3 are exchanged by a substrate-preserving Hodge map.
oriented boundary incidence identifies normals with faces by Hodge duality.
```

Therefore the desired unconditional Planck primitive Clifford-Majorana
derivation cannot be obtained from the currently accepted substrate bank by
adding only the words "boundary orientation" or "incidence." A future positive
theorem must derive a new asymmetric primitive:

```text
normal cochain primitivity,
first-order response primitivity,
or a physical boundary/action-density law that breaks the Hodge equivalence.
```

Without such a theorem, the lane should stop as an unconditional-retention
attempt. A later loop route proposes exactly that missing asymmetric theorem
from the retained link-local action differential; this no-go remains valid on
its boundary-incidence-only surface.

## Verification

Run:

```bash
python3 scripts/frontier_planck_boundary_orientation_incidence_no_go.py
```

Current output:

```text
Summary: PASS=10  FAIL=0
Verdict: NO-GO.
```

The ten checks are:

1. construct `H_cell`, `P_1`, `P_3`, and the Hodge map;
2. verify oriented four-cell face incidence equals Hodge-dual normal data;
3. verify the normal/face incidence pairing is perfect but not selective;
4. verify `P_1` and `P_3` satisfy the same spin/time/CPT tests;
5. verify Hodge duality preserves the tensor-local number algebra;
6. verify the first homogeneous and third homogeneous face responses are dual;
7. verify current one-form and flux three-form carriers are equivalent;
8. verify `P_1` selection requires an extra cochain-normal primitive flag;
9. record stuck fan-out over the remaining route families;
10. verify the forbidden-input boundary.
