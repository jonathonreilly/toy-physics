# Planck Substrate-to-Carrier Forcing — Reflection-Positivity Route

**Date:** 2026-05-10
**Status:** bounded_theorem candidate (source-only); audit verdict and effective status are owned by the independent audit lane
**Claim type:** bounded_theorem
**Loop:** `physics-loop/planck-pa-retention-block01-20260510`
**Runner:** `scripts/cl3_planck_substrate_to_carrier_forcing_2026_05_10_planckP1.py`
**Cached output:** `logs/runner-cache/cl3_planck_substrate_to_carrier_forcing_2026_05_10_planckP1.txt`

## Purpose

PR #228's Planck primitive Clifford-Majorana edge derivation
([PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md](./PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md))
was audited as `audited_renaming` because the algebraic carrier construction did
not derive that the substrate action selects the rank-four
Hamming-weight-one packet `P_A` as the active boundary block. Two follow-up
no-gos sharpened the obstruction:

- [SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  shows that the listed substrate symmetries (spatial `Cl(3)` spin lift, time
  parity, CPT grading, complex Hilbert structure, tensor-local number algebra)
  admit 17 rank-four equivariant projector classes, including the
  Hamming-weight-three projector `P_3 = E_{tVV} + E_{VVV}`, so symmetry alone
  does not force `P_A`.
- [FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md](./FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
  shows that the oriented Hodge complement on `Lambda^* span(t,x,y,z)`
  exchanges `P_1 <-> P_3` while preserving spin-lift equivariance, time
  parity (up to central sign), CPT grading, and tensor-local number algebra.

A subsequent positive route through the action source domain
([PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md))
selects `P_A` from the support of the link-local first variation. That
route is conditional on accepting the staggered-Dirac/Grassmann action source
domain as substrate content — which is currently an open gate per
[MINIMAL_AXIOMS_2026-05-03.md](./MINIMAL_AXIOMS_2026-05-03.md).

This note records an **independent** positive route through a different
cited support surface: **reflection positivity** as recorded by the axiom-first
RP support theorem
[AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md](./AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md).
The OS factorization that underlies RP is sesquilinear in field-algebra
generators: the bilinear `<Theta(F) F>_{vac}` is non-negative when F is degree
one in the field algebra, and the OS Cauchy-Schwarz manipulation does not
extend to degree-three composites. On the primitive event cell, "degree one in
the field algebra" coincides with Hamming-weight-one boundary support. So the
cited RP positivity bilinear singles out `P_A` over `P_3` as the unique
RP-compatible rank-four equivariant carrier.

## Bounded scope and named admissions

This is a **bounded_theorem** because the load-bearing input — the OS
sesquilinear factorization — is currently carried at the support level on the
staggered+Wilson sector via a runner-supported `det(M) >= 0` exhibit (E6 in
the parent RP note), not as a closed-form derivation across the full canonical
action. The parent note carries RP on the staggered-only sector by
closed-form derivation and on the staggered+Wilson sector with the named
runner-supported residual.

The named admissions of this note are:

- **Admission RP1.** OS sesquilinear factorization (eqs. (7) and (10) of the
  parent RP note) holds at the canonical normalization surface. This is
  derived on the staggered-only sector by closed-form derivation in the
  parent note,
  and runner-supported via E6 for the full staggered+Wilson sector.
- **Admission RP2.** The Sharatchandra fermion-reflection convention
  `Theta chi_x = chi-bar_{theta x}^T`,
  `Theta chi-bar_x = chi_{theta x}^T` defines the field-algebra grading
  faithfully on the primitive cell.

Under RP1+RP2, this note's main claim is a bounded positive calculation.
The bounded label records the staggered+Wilson runner-supported residual
on RP1 and leaves status authority to the independent audit lane.

This note does NOT use:

- PDG observed values or fitted parameters;
- the staggered-Dirac action *source domain* `U = span(u_t,u_x,u_y,u_z)` as
  substrate content (that is the link-local first-variation route);
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`;
- `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`;
- `alpha_LM` decoration chains.

## Inputs (cited)

The proof uses these cited framework inputs:

- [MINIMAL_AXIOMS_2026-05-03.md](./MINIMAL_AXIOMS_2026-05-03.md):
  physical `Cl(3)` local algebra and `Z^3` spatial substrate baseline.
- [AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md](./AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md):
  the cited RP support theorem on the canonical action surface.
  Specifically, the **OS sesquilinear factorization** of `<Theta(F)*F>` for
  field-degree-one F.
- [CL3_SM_EMBEDDING_THEOREM.md](./CL3_SM_EMBEDDING_THEOREM.md):
  cited `Cl(3)` automorphism and Cl⁺(3) ~= H structure on the
  primitive event cell.
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md):
  conditional time-axis from anomaly cancellation, completing the local
  primitive star to four axes.
- [CPT_EXACT_NOTE.md](./CPT_EXACT_NOTE.md):
  CPT grading action on the primitive event cell.
- [SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  and
  [FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md](./FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md):
  the prior no-gos enumerate the 17 rank-four equivariant candidates and
  exhibit the Hodge-dual `P_3` counterexample to symmetry-only forcing. This
  note's job is to show that, **over the same 17 candidates**, the cited
  RP positivity bilinear selects exactly one: `P_A`.

## Theorem Statement

Let

```text
W = span(t, x, y, z),     H_cell = Lambda^* W ~= C^16,
```

be the time-locked primitive event cell. Let

```text
{P_alpha : alpha = 1, ..., 17}
```

be the 17 rank-four local equivariant projector classes enumerated by the
substrate-to-`P_A` no-go (each is a sum of irreducible local spin/time blocks
`{E_0, E_t, E_V, E_{tV}, E_{VV}, E_{tVV}, E_{VVV}, E_{tVVV}}`). Let `Theta`
denote the temporal-link reflection of the parent RP note.

For each candidate `P_alpha` define the **vacuum-reachable degree-1 sector**

```text
V_1(P_alpha) := P_alpha . span{ chi^a |Omega>, chi-bar^a |Omega>  :  a in {t,x,y,z} }
```

i.e. the subspace of `P_alpha . H_cell` reachable from the canonical vacuum
`|Omega> = |0,0,0,0>` by ONE field-algebra generator. The OS Cauchy-Schwarz
manipulation in equation (10) of the parent RP note expresses
`<Theta(F) F>` as a squared norm whose vector `v` is built from a single
field generator acting on the half-action vacuum; therefore the OS bilinear
form is non-trivial only when `V_1(P_alpha)` is non-empty, and the
RP-positivity certificate certifies positivity exactly on
`A_+(P_alpha)` constructed from these vectors.

Define the candidate's **RP positivity bilinear**

```text
G_alpha(F, F') := <Theta(F) F'>_{can},
F, F' in A_+(P_alpha) := span(V_1(P_alpha)).
```

**Theorem (RP-route substrate-to-carrier forcing, bounded).** Under
admissions RP1 and RP2:

1. **Maximal degree-1 vacuum sector on `P_A`.** `V_1(P_A)` is full-rank:
   `dim V_1(P_A) = 4 = rank(P_A)`. Every basis state of
   `P_A . H_cell` is reached from the vacuum by exactly one field
   generator `chi^a` (`a in {t,x,y,z}`). The induced bilinear `G_A` on
   `A_+(P_A)` is positive semidefinite by statement (R1)+(R2) of the
   parent RP note specialized to `P_A`.
2. **Empty degree-1 vacuum sector on `P_3`.** `V_1(P_3) = {0}`: no
   field-algebra generator (a single `chi^a` or `chi-bar^a`) acting on
   the vacuum produces a state with support in
   `P_3 . H_cell = E_{tVV} + E_{VVV}`. `chi^a |Omega>` is always a
   weight-1 state, never weight-3. Therefore `P_3` has no
   OS-Cauchy-Schwarz-active observable algebra at the field-degree-1
   level: it is not an RP-compatible carrier.
3. **Sub-maximal degree-1 vacuum sectors on the other 15 candidates.**
   For each of the remaining 15 rank-four equivariant projectors
   `P_alpha` (`alpha != A, 3`), `dim V_1(P_alpha) in {0, 1, 3}`,
   strictly less than `rank(P_alpha) = 4`. So no other candidate has
   the maximal-rank degree-1 vacuum sector required for a faithful
   irreducible `Cl_4(C)` carrier on the active block.
4. **Uniqueness as the maximal RP-compatible rank-four equivariant
   carrier.** Among the 17 candidates, `P_A` is the unique class such
   that `dim V_1(P_alpha) = rank(P_alpha) = 4`. The induced RP bilinear
   `G_A` on `A_+(P_A)` is positive semidefinite by the parent RP
   theorem, and the carrier passes the OS-Cauchy-Schwarz factorization
   test (10) at full rank.

Therefore: under RP1 and RP2, the cited RP positivity bilinear, applied
through the OS Cauchy-Schwarz factorization, singles out `P_A` as the
unique full-rank-four RP-compatible active carrier. The PR #228 algebraic
Clifford-Majorana edge construction then applies on the so-selected
rank-four packet.

## Derivation

### 1. Field-algebra generators are weight-1 ladders on `H_cell`

The primitive event cell algebra `H_cell ~= Lambda^* W` carries field-algebra
generators `chi^a` (creation in axis `a`) and `chi-bar^a` (annihilation in
axis `a`), both of which act as **Hamming-weight ±1 ladders**:

```text
chi^a : Lambda^k W -> Lambda^{k+1} W    (raises Hamming weight by 1)
chi-bar^a : Lambda^k W -> Lambda^{k-1} W  (lowers Hamming weight by 1)
```

In particular, applied to the vacuum `|Omega> = |0,0,0,0>`:

```text
chi^a |Omega>  =  pm |a>,   weight(|a>) = 1
chi-bar^a |Omega>  =  0     (vacuum is the lowest-weight state)
```

This is the load-bearing structural fact for the OS Cauchy-Schwarz: the
vacuum-reachable single-generator sector is exactly `P_A . H_cell = H_1`.

### 2. The OS Cauchy-Schwarz active sector lives in the vacuum-reachable
degree-1 image

The cited RP bilinear is sesquilinear: equation (10) of the parent RP
note,

```text
Z_F  =  Sigma_{links}  || exp(-(1/2) Q_+) v ||^2,
```

is a positive squared norm of a vector `v` constructed by **one application
of a half-action field generator to the half-action vacuum**. The
Cauchy-Schwarz manipulation does not extend to multi-generator composites
because the sum-over-links structure of `S_+` couples one Grassmann pair per
crossing temporal link.

The active block `P_alpha` therefore must satisfy:

```text
V_1(P_alpha) := P_alpha . span{ chi^a |Omega>, chi-bar^a |Omega> } != {0}
```

and to host a **faithful** irreducible complex `Cl_4(C)` carrier on the
selected rank-four packet, must satisfy:

```text
dim V_1(P_alpha) = rank(P_alpha) = 4.
```

### 3. `V_1(P_3) = {0}`

`P_3 = E_{tVV} + E_{VVV}` is the Hamming-weight-three block. A field-algebra
generator acting on the vacuum produces a weight-1 (or zero) state, never a
weight-3 state. Therefore

```text
{ chi^a |Omega>, chi-bar^a |Omega> } cap (P_3 . H_cell) = {}
```

so `V_1(P_3) = {0}`. The candidate `P_3` has no OS-Cauchy-Schwarz-active
observable algebra at the field-degree-1 level, and cannot host the
irreducible `Cl_4(C)` carrier under cited RP. Therefore `P_3` is excluded
as the active RP carrier.

### 4. Exhaustion across the 17 candidates

The 17 rank-four equivariant projector classes from the substrate-to-`P_A`
no-go partition into four groups by the dimension of their vacuum-reachable
degree-1 sector `V_1(P_alpha)` (verified explicitly by the runner):

| `dim V_1(P_alpha)` | Number of classes | Example | Match `rank(P_alpha)`? |
|---:|---:|---|---|
| 4 | 1 | `(Et, EV) = P_A` | YES (full-rank match) |
| 3 | 3 | `(E0, EV)`, `(EV, EVVV)`, `(EV, EtVVV)` | NO (sub-rank, 3 < 4) |
| 1 | 5 | `(Et, EtV)`, `(Et, EVV)`, `(Et, EtVV)`, `(EVV, Et)`, `(E0, Et, EVVV, EtVVV)` | NO (sub-rank, 1 < 4) |
| 0 | 8 | `(E0, EtV)`, `(EtV, EVVV)`, `(EtVV, EVVV) = P_3`, ... | NO (vacuum-reachable sector is empty) |

**Only the candidate `P_A = (Et, EV)` has `dim V_1(P_A) = rank(P_A) = 4`.**
This is the unique class that:

- supports a faithful rank-four field-degree-1 vacuum-reachable sector;
- on which the cited RP bilinear `G_A` (statement R1+R2 of the parent
  RP note specialized to `P_A`) is positive semidefinite at full rank;
- can host an irreducible 4-dimensional `Cl_4(C)` module after the prior
  PR #228 algebraic construction.

All other 16 candidates fail the rank-match: either `V_1(P_alpha) = {0}`
(no RP-active sector at all) or `dim V_1(P_alpha) < 4` (sub-faithful, the
OS bilinear sees less than the full rank-four packet).

### 5. RP positivity bilinear restricted to `P_A` is PSD

The cited RP bilinear `G_A(F, F') = <Theta(F) F'>` on
`A_+(P_A) = span V_1(P_A)` is positive semidefinite: this is statement (R2)
of the parent RP note specialized to the field-degree-1 sector reachable
from the vacuum within `P_A`. The eigenvalue multiplicities are exactly
those of the canonical staggered-fermion transfer matrix on `H_cell`. This
is the load-bearing OS Cauchy-Schwarz statement; the parent RP note carries
it at the support level (staggered-only: derived; staggered+Wilson:
runner-supported via E6).

This passes the RP-positivity test: `P_A` is an RP-compatible rank-four
carrier.

### 6. Hodge-image observation: RP breaks the Hodge degeneracy

The Hodge complement `*` exchanges `P_1 = P_A <-> P_3`. The runner verifies
explicitly that under `*`, weight-1 states map to weight-3 states. At the
field-algebra level, weight-3 states correspond to **degree-3 composite
operators** (three Grassmann creations from the vacuum). So the Hodge image
of the OS sesquilinear sector (degree-1) is a degree-3 sector, which lies
**outside** the OS Cauchy-Schwarz factorization in equation (10) of the
parent RP note.

This sharpens the FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO: the Hodge
exchange that "preserves substrate symmetries" does NOT preserve RP
compatibility. RP breaks the Hodge degeneracy at the level of field
grading.

### 7. Combination with the PR #228 algebraic construction

Once `P_A` is selected by the RP positivity criterion, the prior PR #228
algebraic construction
([PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md](./PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md))
applies without needing rank equality as a selector. The cited spatial
`Cl(3)` bivectors plus the anomaly-forced time axis construct four primitive
coframe axes, and the unique irreducible complex `Cl_4(C) ~= M_4(C)` module
has dimension four matching `rank(P_A) = 4`. The PR #228 runner verifies the
eight construction checks; this note's runner re-verifies the eighth check
(`c_Widom = c_cell = 1/4`) under the new selector for cross-validation.

## Honest Status

**Bounded support theorem under cited RP.** The selector criterion
("single-link bilinear sector has full rank-four primitive-cell support") is
derived from cited RP positivity (admissions RP1, RP2) and not assumed.
Under those admissions, `P_A` is the unique rank-four equivariant projector
class compatible with the cited RP positivity bilinear. The bounded label
records the staggered+Wilson runner-supported residual on RP1 carried over
from the parent note; the staggered-only sector is fully derived.

**Independence from the link-local route.** This route does not use the
staggered-Dirac action source domain `U = span(u_t,u_x,u_y,u_z)` as
substrate content. The selector is the OS Cauchy-Schwarz field-degree
constraint, which is intrinsic to RP at the canonical surface. The two routes
arrive at the same conclusion (`P_A` is the active block) by independent
load-bearing primitives.

**What this note does not claim:**

- the SI decimal value of `hbar`;
- a physical-units derivation of `G_Newton`;
- strong-field continuum gravity or black-hole interior statements;
- closure of the **other two** missing theorems for Planck-from-structure:
  (i) action-density identification, (ii) Wald/area carrier identification.
  These remain explicit bridge premises.

**What this note does claim:** the substrate-to-carrier forcing step — the
*first* of three missing theorems for the Planck-from-structure cascade — has
an audit-ready bounded route through cited RP, distinct from the prior
link-local first-variation route. Both routes select `P_A`. Independent audit
of either route promotes the substrate-to-`P_A` question from "renaming" to
"derived support".

## Connection to the Existing No-Gos

This theorem does not overturn the prior no-gos. It changes the premise
surface by bringing in cited RP as an additional load-bearing primitive
not present in the prior symmetry-only enumeration.

| Prior result | Still valid? | What changes here |
|---|---:|---|
| symmetry-only substrate-to-`P_A` no-go | yes | RP is a positivity bilinear, not a discrete symmetry; it is extra cited content |
| first-order coframe unconditionality no-go | yes | RP breaks the Hodge degeneracy: the Hodge image of `B_1(P_A)` lives outside the OS sesquilinear sector |
| boundary-incidence stretch no-go | yes | RP is not a boundary-orientation law; it is a positivity bilinear on the field algebra |
| link-local first-variation route | independent | this note uses RP, not the action source domain; the two routes are mutually consistent and arrive at the same `P_A` |

## Verification

Run:

```bash
python3 scripts/cl3_planck_substrate_to_carrier_forcing_2026_05_10_planckP1.py
```

The runner checks:

1. construct `H_cell = (C^2)^4` and the 17 rank-four equivariant projector
   classes (matches substrate-to-`P_A` no-go enumeration);
2. construct the field-algebra ladder operators and verify they raise/lower
   Hamming weight by 1;
3. compute the single-link bilinear sector `B_1(P_alpha)` for each candidate;
4. verify that `B_1(P_A)` has full rank-four support (16 single-link
   bilinears spanning a rank-four-supported algebra);
5. verify that `B_1(P_3) = {0}` (no single-link bilinear with `P_3`-support);
6. verify that for the other 15 candidates, `B_1(P_alpha) subset B_1(P_A)`,
   none is strictly larger;
7. verify the Hodge image of a single-link bilinear is a three-link
   composite (not a primitive RP-bilinear);
8. cross-validate `c_Widom = c_cell = 1/4` after `P_A` selection (matches
   PR #228).

Expected output:

```text
=== TOTAL: PASS=N, FAIL=M ===
```

with PASS=8 and FAIL=0 if the bounded theorem holds.

## Citations

- A_min: [MINIMAL_AXIOMS_2026-05-03.md](./MINIMAL_AXIOMS_2026-05-03.md)
- parent RP support theorem:
  [AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md](./AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Clifford structure on the primitive cell:
  [CL3_SM_EMBEDDING_THEOREM.md](./CL3_SM_EMBEDDING_THEOREM.md),
  [NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md)
- time axis: [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
- CPT grading: [CPT_EXACT_NOTE.md](./CPT_EXACT_NOTE.md)
- prior no-gos:
  [SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md),
  [FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md](./FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
- companion route through link-local action:
  [PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
- downstream consumer (the algebraic Clifford-Majorana edge construction):
  [PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md](./PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md)
