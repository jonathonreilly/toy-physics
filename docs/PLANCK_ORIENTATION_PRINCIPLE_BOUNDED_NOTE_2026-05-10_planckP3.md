# Planck Orientation Principle from Retained 3+1 Single-Clock Time-Asymmetry

**Date:** 2026-05-10
**Type:** bounded_theorem
**Claim scope:** On the time-locked Boolean coframe register
`H_cell ~= Lambda^* span(t, x, y, z)`, the action-level temporal-axis Z_2
grading
`Theta_RP := (-1)^{n_t}` (the exterior 1-form lift of the
staggered-Dirac RP staggered-phase sign rule
`eta_t(theta x) = - eta_t(x)`, `eta_i(theta x) = + eta_i(x)`)
breaks the Hodge `P_1 <-> P_3` degeneracy:
`dim(P_1 cap E_-) = 1` (just the time 1-form `e^t`) versus
`dim(P_3 cap E_-) = 3` (the time-mixed 3-forms, none of which is `e^t`).
Combined with the cited single-clock theorem's identification of the
forward-time generator with the unique infinitesimal time-translation 1-form,
the orientation principle uniquely selects `P_1` as the first-order
boundary/orientation carrier over its Hodge-dual `P_3`.

**Status:** source-note proposal — bounded_theorem. Effective `effective_status`
is set only by the independent audit lane.
**Authority role:** source-note. Audit verdict and downstream status owned by
the independent audit lane.
**Loop:** physics-loop / planck-pa-retention-block01-20260430 (third missing
theorem of three, this round)
**Primary runner:** [`scripts/cl3_planck_orientation_principle_2026_05_10_planckP3.py`](../scripts/cl3_planck_orientation_principle_2026_05_10_planckP3.py)
**Cache:** [`logs/runner-cache/cl3_planck_orientation_principle_2026_05_10_planckP3.txt`](../logs/runner-cache/cl3_planck_orientation_principle_2026_05_10_planckP3.txt)

## Authority disclaimer

This is a source-note proposal. The independent audit lane has full
authority to retag, narrow, or reject. The author does NOT propose a
positive_theorem promotion at this time; the bounded label is intrinsic
because the action-level identification of `Theta_RP` with the exterior
1-form temporal-axis sign is itself a conditional bridge from the
staggered-Dirac action surface (currently `bounded_theorem` substep 4)
to the exterior algebra `Lambda^* span(t, x, y, z)`.

## Question

The Planck primitive coframe boundary-carrier theorem
[`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
proves the conditional implication

```text
first-order coframe response  =>  P_A = P_1.
```

The first-order coframe unconditionality no-go
[`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`](FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
showed that the substrate symmetries previously catalogued (spatial
`Cl(3)` spin-lift, time parity, CPT grading, tensor-local number algebra)
are preserved by the Hodge complement, hence do not select `P_1` over
`P_3`.

The Planck boundary orientation incidence no-go
[`PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`](PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md)
extended that to oriented boundary incidence: under Hodge,
`*e^a = i_{e_a} Omega` exchanges `P_1` with `P_3`; oriented incidence
does not select.

This note asks whether the cited 3+1 single-clock time-asymmetry chain —
specifically the action-level distinguishing sign on TEMPORAL links
carried by the staggered phase rule

```text
eta_t(theta x) = - eta_t(x),    eta_i(theta x) = + eta_i(x)   (i = x, y, z)
```

(cited from
[`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
proof and
[`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
Step 4) — is enough to break the `P_1`/`P_3` Hodge degeneracy and
supply the missing first-order boundary/orientation principle.

## Answer

**Yes, conditionally.** Under the cited {RP staggered phase rule;
single-clock theorem Step 4 uniqueness of the temporal reflection
axis; microcausality forward-time `alpha_t`; anomaly-forces-time 3+1
split}, the exterior 1-form lift of the action-level temporal-axis
sign rule is the Z_2 grading

```text
Theta_RP  :=  (-1)^{n_t}  otimes  I_x  otimes  I_y  otimes  I_z
```

on `H_cell`. This grading

1. exchanges no `P_k` projectors (it is diagonal in the Hamming-weight basis),
2. but ANTICOMMUTES with the Hodge star `*` on `Lambda^* W` (because
   Hodge sends `n_a -> 1 - n_a`, hence `(-1)^{n_t} -> -(-1)^{n_t}`),
3. and gives ASYMMETRIC (-1)-eigenspace dimensions inside the rank-four
   carriers:

```text
dim(P_1 cap E_-)  =  1     (the unique time 1-form e^t)
dim(P_1 cap E_+)  =  3     (the spatial 1-forms e^x, e^y, e^z)
dim(P_3 cap E_-)  =  3     (the time-mixed 3-forms e^t ^ e^i ^ e^j)
dim(P_3 cap E_+)  =  1     (the spatial volume 3-form e^x ^ e^y ^ e^z)
```

The Hodge image `*e^t = e^x ^ e^y ^ e^z` is in `P_3 cap E_+`
(spatial-volume eigenspace, NOT the time direction), so Hodge does
NOT identify "the time direction" between `P_1` and `P_3`.

Combined with the cited single-clock theorem's identification of
the forward-time generator with the unique infinitesimal
time-translation 1-form `dt`, the orientation principle

> Pick the rank-four carrier whose unique (-1)-`Theta_RP` eigenvector
> is the infinitesimal time direction `dt = e^t`.

UNIQUELY selects `P_1` over `P_3`. This is the missing first-order
boundary/orientation theorem.

## Status (bounded_theorem)

The label is `bounded_theorem` because the action-level identification

```text
"sign rule on temporal links of the staggered-Dirac action"
   <-->   Theta_RP = (-1)^{n_t} on Lambda^* W
```

is itself a conditional bridge from the staggered-Dirac action surface
to the exterior algebra. Three audit-pending authorities supply that bridge:

- **(R-RP)** `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29`
  loads the staggered phase rule `eta_t(theta x) = - eta_t(x)`,
  `eta_i(theta x) = + eta_i(x)` directly into its proof of (R1)–(R4).
- **(R-SC)** `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03`
  Step 4 proves the temporal direction is the UNIQUE RP-admissible
  reflection axis on the staggered-Dirac action; no spatial direction
  carries the same sign rule.
- **(R-LR)** `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01`
  identifies the forward-time evolution generator with `H = -log(T)/a_tau`,
  whose infinitesimal action `iH dt` carries `dt` as a 1-form (not as
  a 3-form), giving the canonical "infinitesimal time direction" carrier.

These three are present on `main` (as `proposed_retained` /
`audit-pending` aggregator chain). The full positive_theorem
identification that ties the lattice action's `eta_t` rule directly to
the abstract exterior 1-form `e^t` requires the substep 4 staggered-Dirac
realization gate to ratchet from `bounded_theorem` to `positive_theorem`
([`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
Until that gate closes, this orientation principle is `bounded_theorem`.

## Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| RP | Action-level temporal-axis sign rule `eta_t(theta x) = - eta_t(x)`, `eta_i(theta x) = + eta_i(x)` | cited support from `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29` (`proposed_retained`, audit-pending) |
| SC | Temporal direction is the unique RP-admissible reflection axis on the staggered-Dirac action | cited support from `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03` Step 4 (`proposed_retained`, audit-pending; PR 418) |
| LR | Forward-time `alpha_t(O) = e^{itH} O e^{-itH}` with `v_LR < infty`; `H = -log(T)/a_tau` | cited support from `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01` (`proposed_retained`, audit-pending) |
| AT | Definite 3+1 time direction with single-clock structure | per `ANOMALY_FORCES_TIME_THEOREM` (bounded_theorem on main; admission (i) is open ABJ-on-lattice) |
| EVCELL | `H_cell = tensor_a C^2_a ~= Lambda^* span(t, x, y, z)` (Boolean coframe register) | branch context per `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25` |

### Forbidden inputs

- NO PDG observed values (no `M_Pl`, `G_N`, `c`, `hbar`)
- NO new repo-wide axioms
- NO fitted matching coefficients
- NO lattice MC empirical inputs
- NO observable-principle / YT Ward identity / `alpha_LM` decoration chain

### Notation

- `BASIS = {|S> : S subseteq E}` for `E = {t, x, y, z}`,
- `n_a` is the local number operator on axis `a`,
- `P_k = sum_{|S| = k} |S><S|` is the Hamming-weight-`k` projector,
- `*` is the oriented Euclidean Hodge star on `Lambda^* W`,
- `Theta_RP := (-1)^{n_t}` is the action-level temporal-axis Z_2 grading.

## Theorem

**(O1) `Theta_RP` is a Hermitian unitary involution.**
`Theta_RP^2 = I`, `Theta_RP^dagger = Theta_RP`, hence `Theta_RP` defines
a Z_2-grading `H_cell = E_+ oplus E_-` with eigenvalues `+/-1`.

**(O2) `Theta_RP` is diagonal in the Hamming-weight basis** and commutes
with each `P_k` separately:
`[Theta_RP, P_k] = 0` for all `k = 0, 1, 2, 3, 4`. Therefore the
intersection `P_k cap E_{+/-}` is well-defined.

**(O3) Asymmetric eigenspace dimensions inside the rank-four sectors:**

```text
dim(P_1 cap E_-)  =  1,    spanned by  |t> (i.e. e^t)
dim(P_1 cap E_+)  =  3,    spanned by  |x>, |y>, |z>  (i.e. e^x, e^y, e^z)
dim(P_3 cap E_-)  =  3,    spanned by  |txy>, |txz>, |tyz>
dim(P_3 cap E_+)  =  1,    spanned by  |xyz| (i.e. e^x ^ e^y ^ e^z)
```

**(O4) Hodge anticommutes with `Theta_RP`.**
`{*, Theta_RP} = 0` on `Lambda^* W`. Equivalently `* Theta_RP *^{-1} = -Theta_RP`.

**(O5) Orientation principle (the load-bearing pick).**
Under the cited {RP, SC, LR, AT} support chain, the rank-four boundary/orientation
carrier whose unique (-1)-`Theta_RP` eigenvector is the infinitesimal
time direction `dt = e^t` is uniquely `P_1`. Hodge of that eigenvector
is the spatial volume 3-form `*e^t = e^x ^ e^y ^ e^z`, which is in
`P_3 cap E_+`, NOT a time-direction object.

**(O6) Hodge does NOT identify "the time direction" between `P_1` and
`P_3`.** Although `* P_1 *^{-1} = P_3`, the Hodge star sends the unique
1-d (-1)-`Theta_RP` eigenvector of `P_1` (namely `e^t`) to the unique
1-d (+1)-`Theta_RP` eigenvector of `P_3` (namely `e^x ^ e^y ^ e^z`),
NOT to a (-1)-eigenvector of `P_3`. So the orientation principle has
asymmetric `(-1)`-eigenspace content in the two carriers, and the
unique time-direction object lives in `P_1`.

Statements (O1)–(O6) together constitute the Planck orientation principle
on the cited 3+1 single-clock time-asymmetry chain.

## Proof

### Step 1 — Construction of `Theta_RP` and Z_2-grading structure (proves O1, O2)

Define `Theta_RP` on the basis vectors of `H_cell` by

```text
Theta_RP |S>  :=  (-1)^{[t in S]} |S>,   S subseteq {t, x, y, z}.
```

Equivalently `Theta_RP = (-1)^{n_t} otimes I_x otimes I_y otimes I_z` in
the Boolean number-occupation basis. By construction:

1. `Theta_RP^2 = I` (involution), `Theta_RP^dagger = Theta_RP` (Hermitian),
   `Theta_RP^dagger Theta_RP = I` (unitary). This is (O1).
2. `Theta_RP` is diagonal in the Boolean number-occupation basis, and
   each Hamming-weight projector `P_k = sum_{|S| = k} |S><S|` is also
   diagonal in this basis, so `[Theta_RP, P_k] = 0` for all `k`. Hence
   `P_k cap E_{+/-}` is the projector onto the basis vectors `|S>` with
   `|S| = k` and the appropriate value of `[t in S]`. This is (O2).

The action-level identification of `Theta_RP` with the exterior 1-form
lift of the staggered-Dirac sign rule is the load-bearing bridge
(see "Status" section above): under cited RP and SC, the staggered
phases satisfy `eta_t(theta x) = - eta_t(x)`, `eta_i(theta x) = + eta_i(x)`.
The exterior algebra `Lambda^* span(t, x, y, z)` carries the
multiplicative lift of the same sign rule on its 1-form basis, which
extends multiplicatively to higher-degree forms. The Boolean
number-occupation basis `|S>` is in bijection with the exterior basis
`e^{S} = e^{a_1} ^ ... ^ e^{a_k}` for `S = {a_1 < ... < a_k}`, and the
sign carried by `Theta_RP` is exactly the parity of the number of
temporal axis-indices in `S`. ∎

### Step 2 — Eigenspace dimension count inside `P_1` and `P_3` (proves O3)

By Step 1, `P_k cap E_{+/-}` is diagonalised by the Boolean basis. The
rank is the number of basis vectors with the prescribed Hamming-weight
`k` and prescribed temporal occupation `[t in S]`.

**`P_1 cap E_-`:** `|S| = 1` and `t in S`. The unique such `S` is `{t}`.
Rank `= 1`. The basis vector is `|t>`, identified with `e^t in Lambda^1 W`.

**`P_1 cap E_+`:** `|S| = 1` and `t notin S`. The three such `S` are
`{x}, {y}, {z}`. Rank `= 3`. The basis vectors are `|x>, |y>, |z>`,
identified with `e^x, e^y, e^z in Lambda^1 W`.

**`P_3 cap E_-`:** `|S| = 3` and `t in S`. The three such `S` are
`{t, x, y}, {t, x, z}, {t, y, z}`. Rank `= 3`. The basis vectors
correspond to the time-mixed 3-forms.

**`P_3 cap E_+`:** `|S| = 3` and `t notin S`. The unique such `S` is
`{x, y, z}`. Rank `= 1`. The basis vector is `|xyz>`, identified with
`e^x ^ e^y ^ e^z in Lambda^3 W` (the spatial volume 3-form).

This is (O3). ∎

### Step 3 — Hodge anticommutes with `Theta_RP` (proves O4)

The Euclidean oriented Hodge star on the four-axis exterior basis acts
by

```text
* |S>  =  sign(S, E\S) |E\S>.
```

Hence `*` sends each axis occupation to its complement:
`n_a -> 1 - n_a` for each `a`. Therefore

```text
Theta_RP (* |S>)  =  (-1)^{[t in E\S]} (* |S>)  =  (-1)^{1 - [t in S]} (* |S>)
                  =  -(-1)^{[t in S]} (* |S>)  =  -* Theta_RP |S>.
```

So `Theta_RP * = -* Theta_RP`, equivalently `{*, Theta_RP} = 0`. This
is (O4). The runner verifies `||{*, Theta_RP}||_F < TOL` and
`||[*, Theta_RP]||_F = 8 > 1`. ∎

### Step 4 — Orientation principle (proves O5)

The cited microcausality / Lieb-Robinson theorem (R-LR) gives the
forward-time evolution

```text
alpha_t(O)  =  e^{itH} O e^{-itH},      H = -(1/a_tau) log(T)
```

with `H` the unique self-adjoint generator (Stone, on finite-dim
`H_phys`; cf. the single-clock theorem (S1)) and the framework spectrum
condition `H >= 0` (R-SC). The infinitesimal action of `alpha_t` is
`d alpha_t (O) / dt |_0 = i [H, O]`, with the time differential `dt`
appearing as a 1-form (not a 3-form): the infinitesimal Heisenberg
flow contracts a 1-form `dt` to produce an operator increment
`i [H, O] dt`.

Identifying that 1-form `dt` with the abstract exterior 1-form `e^t`
inside `Lambda^* W` (this is the action-level bridge at issue) places
`dt` in `Lambda^1 W subset H_cell`. By Step 2 it lies in `P_1`. By
Step 1 it lies in the (-1)-`Theta_RP` eigenspace (because under the
staggered-phase sign rule, the temporal-axis 1-form picks up the
distinguishing sign).

Therefore: the infinitesimal time direction `dt` lives canonically in
`P_1 cap E_-`, which by Step 2 is rank 1.

Now compare with `P_3`:
- The 1-d (+1)-eigenspace `P_3 cap E_+` is spanned by `e^x ^ e^y ^ e^z`,
  which is the **spatial volume 3-form**, not a 1-form, not a
  time-direction object.
- The 3-d (-1)-eigenspace `P_3 cap E_-` is spanned by the three
  time-mixed 3-forms `e^t ^ e^x ^ e^y`, `e^t ^ e^x ^ e^z`,
  `e^t ^ e^y ^ e^z`. These are 3-forms, not 1-forms; they cannot carry
  the canonical "infinitesimal time direction" of the forward-time
  evolution generator, which is intrinsically a 1-form.

Hence the orientation principle

> Pick the rank-four carrier whose unique (-1)-`Theta_RP` eigenvector
> is the infinitesimal time direction `dt = e^t`.

uniquely selects `P_1`. This is (O5). ∎

### Step 5 — Hodge does not preserve the time-direction identification (proves O6)

The Hodge image of `e^t` is

```text
*e^t  =  e^x ^ e^y ^ e^z   (up to overall sign convention).
```

By Step 2, this lies in `P_3 cap E_+`. So Hodge sends the unique
(-1)-`Theta_RP` eigenvector of `P_1` to the unique (+1)-`Theta_RP`
eigenvector of `P_3`. The (-1)-eigenspace of `P_3` (which one would
need to "be the time direction in `P_3`") is rank 3 and consists
entirely of time-mixed 3-forms — none of these is `*e^t`, and none
of these is canonically distinguished as "the time direction" by the
cited forward-time generator.

Therefore Hodge does NOT carry the time-direction identification from
`P_1` to `P_3`. The cited 3+1 single-clock time-asymmetry chain breaks
the Hodge degeneracy, and the orientation principle uniquely selects
`P_1`. This is (O6). ∎

### Step 6 — Conclusion

Steps 1–5 establish the orientation principle: under the cited
{RP staggered phase rule; single-clock theorem Step 4 uniqueness of
the temporal reflection axis; microcausality forward-time `alpha_t`
with `H >= 0`; anomaly-forces-time 3+1 split with definite time
direction}, the rank-four boundary/orientation carrier of the
first-order coframe response is uniquely

```text
P_1
```

over its Hodge-dual

```text
P_3.
```

This is the missing first-order boundary/orientation theorem; it
discharges (modulo the bounded action-level bridge) the open premise
of `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25`.
QED. ∎

## Hypothesis set used

- The existing minimal-framework surfaces named in
  `MINIMAL_AXIOMS_2026-05-03.md`,
  including the repo baseline physical `Cl(3)` local algebra and
  `Z^3` spatial substrate, with no fitted parameters and no observed
  values.
- (R-RP) cited reflection-positivity support theorem
  (action-level temporal-axis sign rule).
- (R-SC) cited single-clock codimension-1 evolution theorem,
  Step 4 (uniqueness of the temporal reflection axis).
- (R-LR) cited microcausality / Lieb-Robinson support theorem
  (forward-time `alpha_t = e^{itH}` with finite `v_LR`).
- (R-AT) `ANOMALY_FORCES_TIME_THEOREM` (bounded_theorem on main with
  one open ABJ admission; the load-bearing content used here is the
  3+1 split with a definite time direction, which holds on the
  cited gauge content + chirality + single-clock cascade
  independently of the open ABJ admission status).
- Boolean coframe event-cell identification
  `H_cell ~= Lambda^* span(t, x, y, z)` per
  `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25`.

No fitted parameters. No observed values used as proof inputs.
No new repo-wide axioms.

## Honest claim-status fields

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  On the time-locked Boolean coframe register H_cell ~= Lambda^* span(t,x,y,z),
  the action-level temporal-axis Z_2 grading Theta_RP := (-1)^{n_t} (the
  exterior 1-form lift of the staggered-Dirac RP staggered-phase sign rule)
  breaks the Hodge P_1 <-> P_3 degeneracy: dim(P_1 cap E_-) = 1 (the unique
  time 1-form e^t) versus dim(P_3 cap E_-) = 3 (the time-mixed 3-forms,
  none of which is e^t). Combined with the cited single-clock theorem's
  identification of the forward-time generator with the unique
  infinitesimal time-translation 1-form dt, the orientation principle
  uniquely selects P_1 over P_3. The bounded label reflects that the
  action-level identification of Theta_RP with the exterior 1-form
  temporal-axis sign is itself a conditional bridge from the staggered-Dirac
  action surface (substep 4 currently bounded_theorem) to the exterior
  algebra Lambda^* W.
proposed_load_bearing_step_class: B (conditional bridge through the
  staggered-Dirac action surface; positive_theorem promotion conditional
  on the substep 4 staggered-Dirac realization gate ratcheting from
  bounded_theorem to positive_theorem).
status_authority: independent audit lane only
actual_current_surface_status: support
conditional_surface_status: derived support theorem on cited RP +
  cited single-clock + cited microcausality + bounded
  anomaly-forces-time + branch-local Boolean coframe event-cell
  identification
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  The load-bearing inputs are cited support surfaces (or bounded_theorem)
  on the current authority surface. The proof proceeds entirely by exterior-
  algebra eigenspace arithmetic on H_cell ~= Lambda^* span(t,x,y,z).
  The action-level identification of Theta_RP with the exterior 1-form
  temporal-axis sign is the bounded conditional bridge from the
  staggered-Dirac action surface to the exterior algebra; until that
  bridge ratchets to positive_theorem, this orientation principle is
  bounded_theorem.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Honest assessment (skeptical review)

**What is genuinely new**: the rigorous use of the action-level
temporal-axis Z_2 grading `Theta_RP` to count (-1)-eigenspace
dimensions inside `P_1` and `P_3` separately. Previous no-go work
treated `Theta_RP` (or its formal twin, time parity) as a "preserved
substrate symmetry" because the Hodge map normalises it
(`{*, time parity} = 0`). The previous analysis correctly observed
that this normalisation does not affect the carrier-level statement
`*P_1*^{-1} = P_3`. The present note observes that it DOES affect
the eigenspace-dimension content: the (-1)-eigenspace of `Theta_RP`
inside `P_1` is rank 1 (just `e^t`), while inside `P_3` it is rank
3 (time-mixed 3-forms). These ranks are NOT exchanged by the Hodge
star — Hodge sends the (-1)-eigenspace of `P_1` to the (+1)-eigenspace
of `P_3`, NOT to its (-1)-eigenspace. So the asymmetric rank
content distinguishes the two carriers in a way that the carrier-
level Hodge analysis did not.

**What is bounded**: the action-level identification
`"sign rule on temporal links"  <->  Theta_RP = (-1)^{n_t} on Lambda^* W`
is a conditional bridge. The cited RP and single-clock support surfaces
load the staggered phase rule directly into their proofs, but the
exterior-1-form lift `Theta_RP` extracts only the temporal-axis
parity — not the full staggered-fermion content. A full
positive_theorem would tie the lattice action's `eta_t` rule directly
to the abstract `Lambda^* W` exterior algebra, which currently
requires the staggered-Dirac realization gate
([`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
to ratchet from `bounded_theorem` to `positive_theorem`. Until then,
the orientation principle is `bounded_theorem`.

**Honest negative**: this note does NOT claim that the time-direction
identification of `dt` with `e^t` is FORCED purely by the abstract
exterior algebra. It is forced by the cited action/time structure —
the action-level temporal-axis sign rule, the single-clock theorem's
uniqueness of the RP axis, and the forward-time generator structure —
acting through the Boolean coframe event-cell identification
`H_cell ~= Lambda^* span(t, x, y, z)`. If one rejects the Boolean
coframe event-cell identification, this orientation principle does
not apply.

**Honest negative**: the previous Hodge no-go observation
`{*, time parity} = 0` was correct. The asymmetric eigenspace
dimensions exist on the same exterior-algebra surface; what's load-
bearing is the IDENTIFICATION of the (-1)-eigenspace of `Theta_RP`
inside `P_1` with the canonical infinitesimal time direction. That
identification comes from the cited action/time structure, not from
purely algebraic substrate symmetries. This note explicitly relies
on cited RP / SC / LR / AT to make the identification.

## Cross-reference to the missing-theorem campaign

This is the **third of three** missing Planck theorems for the
"Planck-from-structure" lane (rotation 2026-05-10). The other two
are:

1. action-level identification of `Theta_RP` with the exterior 1-form
   temporal-axis sign rule (the staggered-Dirac realization gate
   substep 4 promotion); not addressed here.
2. orientation principle from cited 3+1 single-clock time-asymmetry
   (THIS note) — `bounded_theorem` proposed.
3. (campaign-specific third theorem) — not in scope of this note.

The orientation principle proposed here supplies a bounded proposed closure of the
`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30`
boundary on its specified surface, modulo the bounded action-level
bridge. It also supplies the proposed closure for the
`PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30`
boundary on the same surface, since the orientation principle now
provides the missing "extra rule that normal cochains, rather than
Hodge-dual faces, are primitive" that the no-go required.

## Verification

Run:

```bash
python3 scripts/cl3_planck_orientation_principle_2026_05_10_planckP3.py
```

Expected output line:

```text
=== TOTAL: PASS=11, FAIL=0 ===
```

The eleven checks are:

1. construct oriented Hodge star (replicates the no-go surface);
2. Hodge star exchanges `P_1` and `P_3` (replicates the no-go);
3. `Theta_RP` is Hermitian, unitary, involutive (Z_2-grading);
4. `Theta_RP` decomposes `P_1 = (1 cap E_-) + (3 cap E_+)`,
   `P_3 = (3 cap E_-) + (1 cap E_+)` (the load-bearing dimension count);
5. Hodge star anticommutes with `Theta_RP` (the degeneracy-breaker);
6. `e^t` is in `P_1` and is the unique (-1)-`Theta_RP` eigenvector
   of `P_1`;
7. `*e^t` is in `P_3` but lives in the (+1)-`Theta_RP` eigenspace,
   NOT the time-direction object;
8. (-1)-eigenspace of `P_3` is the rank-3 time-mixed 3-form sector,
   contains no `e^t`;
9. (+1)-eigenspace of `P_1` is the rank-3 spatial 1-form sector,
   contains no `e^t`;
10. orientation principle: `P_1` uniquely encodes the time direction
    as a 1-d (-1)-`Theta_RP` eigenvector;
11. forbidden-input boundary (no PDG, no fitted coefficients, no new
    axioms, no MC inputs, no observable-principle / YT Ward /
    `alpha_LM` decoration used).

## Citations

- `MINIMAL_AXIOMS_2026-05-03.md` — A_min current
- `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
  — first-order coframe carrier theorem (this note's downstream
  consumer)
- `PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`
  — the no-go this note closes (modulo the bounded bridge)
- `FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`
  — the parallel no-go on Hodge-dual exchange
- `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
  — cited RP staggered phase rule (load-bearing)
- `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`
  — cited single-clock theorem, Step 4 (load-bearing)
- `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
  — cited forward-time `alpha_t` with finite `v_LR`
- `ANOMALY_FORCES_TIME_THEOREM.md` — bounded 3+1 derivation
- `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`
  — bounded staggered-Dirac realization gate (the bridge condition)

## Forbidden-input boundary (recap)

Neither this note's proof nor its runner uses:

- PDG observed values (no `M_Pl`, `G_N`, `c`, `hbar`)
- fitted matching coefficients
- lattice MC empirical inputs
- new repo-wide axioms
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- any `alpha_LM` decoration chain

The proof is purely exterior-algebra eigenspace arithmetic on
`H_cell ~= Lambda^* span(t, x, y, z)`, with the load-bearing
identification of `Theta_RP` with the action-level temporal-axis sign
supplied by cited RP + cited single-clock + cited
microcausality.
