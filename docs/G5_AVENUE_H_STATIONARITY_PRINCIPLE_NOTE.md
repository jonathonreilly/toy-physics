# G5 Avenue-H Stationarity-Principle Note

**Date:** 2026-04-17
**Status:** structural no-go on six candidate variational principles.
**Verdict:** `AVENUE_H_VERDICT = AVENUE_H_NO_RETAINED_PRINCIPLE_FOUND`.
No tested candidate is BOTH retained AND Koide-selecting. Avenue H
(retained variational/stationarity route to Koide cone-forcing) is
closed on the enumerated primitive classes.
**Script:** `scripts/frontier_g5_avenue_h_stationarity_principle.py`
**Runner state:** `PASS=20, FAIL=0`.
**Authority role:** structural support note for gap `G5` (charged-lepton
mass hierarchy), Avenue H of the 14+ agent attack surface consolidated
in [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).
Extends and generalises Agent 5's character-symmetry negative
([OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md](./OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md))
from the log|det| functional class to a six-class variational survey.

## One-sentence state

On the retained `Cl(3)/Z^3` framework surface, none of six candidate
variational principles whose stationary points on the positive octant
of `v = (sqrt(m_1), sqrt(m_2), sqrt(m_3))` were enumerated simultaneously
carries a RETAINED provenance AND selects the Koide 45-degree cone
`|v_par|^2 = |v_perp|^2` — so the retained variational route to
upgrading Koide `Q = 2/3` from observational pin to flagship theorem
is genuinely closed on the primitive classes tested.

## Geometric setup

On the retained `hw=1` triplet, decompose the mass-square-root vector
`v = (sqrt(m_1), sqrt(m_2), sqrt(m_3))` under the `C_3` action as
`v = v_par + v_perp`, where `v_par` is the projection onto
`e_+ = (1,1,1)/sqrt(3)` (the `C_3` trivial character) and `v_perp` is
the two-dimensional complement carrying the nontrivial characters.
The Koide relation

```
Q = (sum m_i) / (sum sqrt(m_i))^2 = 2/3
```

is equivalent (by the orthogonal decomposition
`sum m_i = |v_par|^2 + |v_perp|^2` and `(sum sqrt(m_i))^2 = 3 |v_par|^2`,
verified in Part 0 of the runner) to the **Koide 45-degree cone**

```
|v_par|^2 = |v_perp|^2.
```

This sits exactly midway between full degeneracy (`|v_perp|^2 = 0`,
`Q = 1/3`) and full trace-zero (`|v_par|^2 = 0`, `Q = 0`).

## Question

Does there exist a retained framework functional `F(v)` — built from
retained `Cl(3)/Z^3` algebraic or observable-principle objects, with no
new sole-axiom insertion — whose stationary points on the positive
octant force `|v_par|^2 = |v_perp|^2` (so Koide `Q = 2/3` becomes a
retained THEOREM rather than an observational pin)? If yes, and if the
same functional further fixes the specific cone point matching
observation, G5 closes at sole-axiom grade as a flagship TOE result.

## Candidate survey

Six candidates were tested, each labeled explicitly as RETAINED or
AD-HOC with written justification.

### H-1 Cauchy-Schwarz midpoint functional — AD-HOC

`F_1(v) = (Q(v) - 1/3)(1 - Q(v))`. Since `Q ∈ [1/3, 1]` on the positive
octant (with `Q = 1/3` at full degeneracy and `Q = 1` at pure
single-generation), the polynomial `F_1` is maximised at `Q = 2/3` by
elementary single-variable calculus.

- **Stationary at Koide:** YES (by construction).
- **Global extremum:** YES on the `Q`-projection.
- **Retained:** NO. `F_1` has no derivation from any retained Cl(3)/Z^3
  algebraic or observable-principle object; it is polynomial-in-Q
  engineering. Retained provenance ABSENT.
- **Fixes cone point:** NO. Every `v` with `Q(v) = 2/3` is stationary,
  so the full 2-parameter Koide cone is a degenerate critical set.

### H-2 Maximum-entropy with C_3 character constraint — AD-HOC

Shannon entropy on the 3-simplex `S = -sum p_i log p_i`. Unconstrained
stationary point (under `sum p_i = 1`) is `p = (1/3, 1/3, 1/3)`, which
gives `Q = 1/3` (full degeneracy).

- **Stationary at Koide:** NO (unconstrained max is uniform).
- **The proposed "equal weight on both character subspaces" constraint
  IS `|v_par|^2 = |v_perp|^2` = Koide cone**, so imposing it is
  circular: the constraint enforces the answer.
- **Retained:** NO. The Shannon-entropy on the mass simplex is not a
  retained framework object.
- **Fixes cone point:** NO.

### H-3 Partition-function extremum with retained log|det| generator — RETAINED

`W[J] = log|det(D + J)|` with retained scalar baseline `D = m I_3`
(Schur baseline from G1 closure) and Yukawa source
`J = diag(y_1, y_2, y_3)`. Per
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md),
this IS the retained unique additive CPT-even scalar generator.

`W(y) = log(m + y_1) + log(m + y_2) + log(m + y_3)`.

Under fixed-sum constraint `sum y_i = S`, the Lagrange system
`1/(m + y_i) = lam` forces `y_1 = y_2 = y_3 = S/3` — the fully
symmetric configuration. The Hessian at the symmetric point has
triply-degenerate eigenvalue `-9/(S + 3m)^2 < 0`, so this is a
genuine maximum, not a saddle whose stable manifold passes through the
Koide cone.

- **Stationary at Koide:** NO (full degeneracy -> Q = 1/3).
- **Retained:** YES (observable-principle generator).
- **Fixes cone point:** N/A (no cone selected).
- **Directly extends Agent 5:** the retained log|det| generator carries
  NO cross-character coupling on `hw=1` with retained scalar baseline
  `D = m I_3`; stationary points respect `C_3` symmetry.

### H-4 Information-geometric Fisher-midpoint — AD-HOC

In the sqrt-embedding `x_i = 2 sqrt(p_i)` (Fisher metric flattens to
the 2-sphere of radius 2), compute the great-circle midpoint between
`p_A = (1/3, 1/3, 1/3)` (uniform) and `p_B = (1, 0, 0)` (pure). The
geodesic midpoint sits at
```
x_mid = 2 (x_A + x_B) / |x_A + x_B|
```
Pulled back, `p_mid` gives

```
Q(p_mid) = 36 / [2 sqrt(3) sqrt(3 - sqrt(3)) + sqrt(6) sqrt(sqrt(3) + 3)]^2
        ~ 0.422650
```

which is NOT 2/3. The Fisher geodesic midpoint is NOT on the Koide cone
(|diff| ~ 0.244).

- **Stationary at Koide:** NO.
- **Retained:** NO. Fisher metric on the mass simplex is a canonical
  information-geometric object but not derived from the retained
  Cl(3)/Z^3 algebra or observable-principle generator.
- **Fixes cone point:** NO.

### H-5 C_3 symmetric/antisymmetric decomposition norm extremum — AD-HOC

`N(v) = alpha |v_par|^2 + beta |v_perp|^2`. Under single-constraint
`sum v_i = S`, `|v_par|^2 = S^2/3` is fixed, so stationarity in `N`
amounts to extremising `beta |v_perp|^2`. For `beta > 0` the minimum is
at `v_perp = 0` (symmetric, Q = 1/3); for `beta < 0` the maximum is at
the boundary. The Koide cone `|v_perp|^2 = |v_par|^2` is not selected
as an interior stationary point of any fixed-`alpha, beta` norm
under natural single-constraint stationarity.

For Koide to be selected one would need `alpha = beta`, but that is
PRECISELY Agent 5's character-symmetry question
([OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md](./OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md)),
which is closed negatively: the retained log|det| chain does not force
`alpha = beta` on blocks where the cross-species propagator `b` is
nonzero.

- **Stationary at Koide:** NO.
- **Retained:** NO for generic quadratic (or reduces to Agent 5 no-go
  if built from retained kernel).
- **Fixes cone point:** NO.

### H-6 Retained Matsubara `K_ii` balance — RETAINED

From CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md ("What remains
rigorous", item 2), the retained second-order Dirac-bridge return
evaluates to `K_{ii}^(spec) = 16 / (m_i^2 + (7/2) u_0^2)` (a retained
Matsubara form). Build

```
F(m_1, m_2, m_3) = sum_i K_ii = 16 sum_i 1 / (m_i^2 + C)
```

with `C = (7/2) u_0^2` universal.

- **Under `sum m_i = S`:** The Lagrange system
  `-32 m_i / (m_i^2 + C)^2 = lam` admits fully-symmetric
  `m_1 = m_2 = m_3 = S/3` (verified), plus potentially a 2+1 split
  (since each `m_i` solves a univariate cubic, giving up to two
  distinct values). The Koide cone admits 2+1-degenerate solutions at
  `sqrt(m+)/sqrt(m-) = 4 + 3 sqrt(2) ~ 8.243`, but observed
  charged-lepton `sqrt`-mass ratios are
  `sqrt(m_mu)/sqrt(m_e) ~ 14.3` and
  `sqrt(m_tau)/sqrt(m_mu) ~ 4.1` — clearly not 2+1 degenerate.
- **Under `sum m_i^2 = T`:** Stationarity forces `m_1^2 = m_2^2 = m_3^2`
  (full degeneracy, Q = 1/3).
- **Stationary at Koide:** NO generic (the Koide 2+1 ray is admitted
  as one of several cubic roots under fixed-sum, but neither is the
  cone selected in full nor does it match observation).
- **Retained:** YES (K_ii is on the retained shape-theorem PASS set).
- **Fixes cone point:** NO.

## Four-outcome verdict

```
AVENUE_H_VERDICT = AVENUE_H_NO_RETAINED_PRINCIPLE_FOUND
```

Explicit outcome table:

| Candidate | Retained? | Forces cone? | Fixes point? |
|---|---|---|---|
| H-1 Cauchy-Schwarz midpoint | AD-HOC | YES (by construction) | NO |
| H-2 Max-entropy w/ char constraint | AD-HOC | NO (Q=1/3) | NO |
| H-3 log|det| partition extremum | **RETAINED** | NO (Q=1/3) | NO |
| H-4 Fisher geodesic midpoint | AD-HOC | NO (Q~0.423) | NO |
| H-5 C_3 norm extremum | AD-HOC | NO | NO |
| H-6 Matsubara K_ii balance | **RETAINED** | NO (degenerate/2+1) | NO |

The unique cone-forcer (H-1) is AD-HOC. The two retained candidates
(H-3, H-6) do not force the cone; their stationary points sit at
fully-symmetric (H-3, H-6) or 2+1-degenerate (H-6 under fixed-sum)
configurations. The observed charged-lepton cone point is generically
asymmetric, so neither retained candidate reproduces observation even
if one accepted a degenerate cone-admitting solution.

## Quantitative outputs

- Residual-ratio reference (observational): `sqrt(m_e/m_tau) = 0.016958`,
  `sqrt(m_mu/m_tau) = 0.243851`, `Q_obs = 0.66666051`,
  `|Q_obs - 2/3| = 6.15e-6`.
- Fisher geodesic midpoint: `Q ~ 0.422650`.
- 2+1-degenerate Koide cone roots: `sqrt(m+)/sqrt(m-) = 4 + 3 sqrt(2)`.
- log|det| Hessian at symmetric critical point: eigenvalues
  `-9/(S + 3m)^2` (triply degenerate, strictly negative).
- Runner state: `PASS=20, FAIL=0`.

## Relationship to Agent 5's character-symmetry no-go

Agent 5
([OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md](./OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md))
closed ONE functional class: the retained log|det| generator on the
two-parameter `(a, b)` circulant curvature kernel does NOT force
`alpha = a + 2b` and `beta = a - b` to coincide, so the Koide
character-symmetry condition is not a theorem output of the
observable-principle chain.

This note extends that result along two axes:

1. **Direction:** Agent 5 examined the curvature-kernel eigenvalue
   forcing question directly; this note examines the corresponding
   variational / stationarity question on the sqrt-mass vector. The
   direct Legendre transform of the log|det| kernel (H-3) reproduces
   Agent 5's negative structurally — stationary points of `W[J]` under
   natural constraints sit at the symmetric configuration, not the
   Koide cone. This confirms the Agent 5 result in the dual
   (stationary-point) formulation.
2. **Breadth:** this note enumerates five further candidate classes
   (entropic, Fisher-geometric, C_3 norm, retained Matsubara, and
   an ad-hoc polynomial) to test whether any alternative retained
   functional class avoids the Agent 5 obstruction. The survey finds:
   none does. Every retained class is symmetric under `C_3` at the
   kernel level, so stationary points respect `C_3` and land on
   symmetric (Q = 1/3) or semi-symmetric (2+1 split) configurations
   — not the generically-asymmetric observed cone point.

The Avenue-H no-go is therefore a genuine generalisation of Agent 5:
the character-symmetry obstruction is intrinsic to retained
`Cl(3)/Z^3` kernels and variational forms on them, not specific to the
log|det| functional.

## What this does not claim

- **Does NOT claim** Avenue H is closed in a fully general sense.
  Only the six enumerated candidate classes are tested. A seventh
  candidate principle not built from: (i) Cauchy-Schwarz polynomials
  in Q, (ii) Shannon entropy on the simplex, (iii) log|det| with
  scalar Schur baseline, (iv) Fisher-metric geodesic midpoints,
  (v) C_3-decomposition norms, or (vi) retained Matsubara diagonal
  `K_ii` balance, could in principle evade the no-go.
- **Does NOT claim** Koide `Q = 2/3` is impossible as a retained
  theorem. It remains algebraically equivalent to `|v_par|^2 =
  |v_perp|^2` (exact), and a sufficient retained cross-character
  primitive (not yet found) would promote it to theorem.
- **Does NOT weaken** the G5 observational-pin closure
  (Agent 11, [G5_OBSERVATIONAL_PIN_CLOSURE_NOTE.md](./G5_OBSERVATIONAL_PIN_CLOSURE_NOTE.md)).
  That closure remains retained-map-plus-observational-promotion at
  the same class as G1.
- **Does NOT claim** to have identified the missing retained primitive.
  It only certifies that three classes of natural candidates (log|det|
  partition, Matsubara K_ii, C_3 invariant norm) fail the stationarity
  test; any successor attempt must supply a genuinely new retained
  cross-character mechanism not reducible to any of H-1..H-6.
- **Does NOT import** fitted charged-lepton masses into the
  structural verdict; PDG values appear only in the residual-ratio
  check as observational reference. The negative structural result on
  H-1..H-6 is independent of any observed charged-lepton mass input.

## Dependency contract

This runner is self-contained and purely symbolic/numeric. It depends
on the following retained authorities as conceptual inputs (their
runners must pass on `main` before this note is trusted; the runner
does not re-execute them, matching lightweight-attempt scope):

- `frontier_three_generation_observable_theorem.py` — retained `hw=1`
  algebra and `C_3` character structure.
- `frontier_hierarchy_observable_principle_from_axiom.py` — unique
  additive CPT-even generator `W[J] = log|det(D + J)|`.
- `frontier_observable_principle_character_symmetry.py` — Agent 5's
  character-symmetry no-go whose extension this note provides.
- `frontier_g5_gamma_1_second_order_return.py` — Agent 10 v2 shape
  theorem supplying the retained Matsubara form `K_ii = 16 / (m_i^2 +
  (7/2) u_0^2)` used in H-6.
- `frontier_dm_neutrino_dirac_bridge_theorem.py` — second-order
  Dirac-bridge identity `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} =
  I_3`, retained Matsubara frame context.

No observed charged-lepton masses, quark masses, Yukawas, CKM / PMNS
data, or fitted values are imported for the structural verdict. The
residual-ratio reference (Part RESIDUAL-RATIO) reads PDG charged-lepton
masses but only to print a reference cone point; the structural verdict
is unaffected by that printing.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, none of six candidate
> variational principles whose stationary points on the positive
> octant of the mass-square-root vector `v = (sqrt(m_1), sqrt(m_2),
> sqrt(m_3))` were enumerated — Cauchy-Schwarz midpoint, Shannon
> maximum-entropy with C_3 character constraint, retained partition-
> function extremum `log|det(D + J)|`, Fisher-metric geodesic midpoint,
> C_3 symmetric/antisymmetric decomposition norm, and retained
> second-order-return Matsubara balance `16/(m_i^2 + (7/2) u_0^2)` —
> simultaneously carries retained provenance and selects the Koide
> 45-degree cone `|v_par|^2 = |v_perp|^2`. The unique cone-selecting
> candidate (Cauchy-Schwarz midpoint) is polynomial engineering with no
> retained Cl(3)/Z^3 derivation. The two retained candidates (log|det|
> partition extremum and Matsubara K_ii balance) have stationary points
> at fully-symmetric (Q = 1/3) or 2+1-degenerate configurations, not at
> the generic Koide cone. This generalises the Agent-5 character-
> symmetry no-go from the log|det|-curvature-eigenvalue forcing question
> to the corresponding variational-stationarity question, and extends
> the no-go to five additional primitive classes. Avenue H (retained
> stationarity principle) is therefore closed on the enumerated
> primitive classes; a retained route to promoting Koide `Q_ell = 2/3`
> from observational pin to flagship theorem must supply a genuinely
> new cross-character primitive not reducible to any of H-1..H-6, or
> accept the G5-observational-pin closure class shared with G1.

## Validation

- `scripts/frontier_g5_avenue_h_stationarity_principle.py`

Current state:

- `frontier_g5_avenue_h_stationarity_principle.py`: `PASS=20`, `FAIL=0`
- `AVENUE_H_VERDICT = AVENUE_H_NO_RETAINED_PRINCIPLE_FOUND`

## Status

**PROPOSED** — structural variational no-go recorded. This note does
not claim a new theorem; it records that six enumerated candidate
variational/stationarity principles each fail at least one of the two
required properties (retained provenance, Koide-cone selection),
extends Agent 5's character-symmetry no-go into the dual variational
formulation and five additional primitive classes, and scopes the
successor theorem objects required to re-open Avenue H. The G5
observational-pin closure class (shared with G1) remains the cleanest
consistent closure path; the retained sole-axiom Koide-theorem route
remains genuinely open pending a new retained cross-character
primitive.
