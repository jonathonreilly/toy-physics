# Parity-Mixing Selector Law — Narrower-Gap + Closure-Candidate-Pending-Physics-Cross-Check

**Date:** 2026-04-17
**Status:** narrower-gap + closure-candidate-pending-physics-cross-check
**Script:** `scripts/frontier_dm_neutrino_source_surface_parity_mixing_selection_obstruction.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

The info-geometric, Z_3-cubic, and Z_3-parity-split obstructions each
produced an obstruction theorem for the right-sensitive 2-real selector
law on `(delta, q_+)`. The Z_3 parity-split theorem in particular showed
that `T_q` is purely Z_3-circulant and `T_delta` is purely Z_3-anti-
circulant, and consequently that **any Z_3-parity-DEFINITE scalar
functional constrains at most one of the active coordinates at fixed m**.

The remaining untested class is Z_3-parity-MIXING functionals. This note:

1. surveys the retained atlas for genuine parity-mixing ingredients,
2. identifies the strongest retained-atlas-native parity-mixing candidate,
3. attempts a sole-axiom derivation of the `(delta, q_+)` selector point,
4. records the obstruction that remains, and
5. produces a new closure-candidate point for Physics-Validation
 cross-check.

**The DM flagship gate remains OPEN.** Nothing in this note is promoted to
theorem-grade beyond the retained atlas. The parity-mixing route produces
a **new candidate selector point** that is strictly inequivalent to
every previously-tested candidate. Physics-Validation via
`eta / eta_obs = 1` can cross-confirm at most one of the candidates.

## Survey of retained-atlas parity-mixing candidates

The Z_3-parity-decomposition theorem establishes that the active
generators split:
```
sym(T_q) = T_q, anti(T_q) = 0
sym(T_delta) = 0, anti(T_delta) = T_delta
```
Hence any Z_3-parity-definite scalar sees at most one of `(delta, q_+)`
at fixed `m`. Parity-mixing invariants are the only remaining class.

| # | Candidate | Atlas status | Parity structure | Fix (δ, q_+)? |
|---|-----------|--------------|------------------|---------------|
| 1 | Singlet-doublet slots `K01 = a_*`, `K02 = b_*` | retained theorem ([intrinsic-slot](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)) | frozen constants | No — no active dependence |
| 2 | Doublet diagonals `K11, K22` | retained theorem ([Z_3 doublet-block](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)) | parity-definite (q_+ only) | No |
| 3 | Doublet off-diag `K12` | retained theorem | parity-definite (δ only) | No |
| 4 | `det K_doublet = K11 K22 − \|K12\|²` | retained-atlas-native (difference of parity-definite) | parity-mixing via SUM structure | Yes, but saddle; crit point outside chamber |
| 5 | `‖K_doublet‖_F² = K11² + K22² + 2\|K12\|²` | retained-atlas-native (positive-definite sum) | parity-mixing via SUM structure | **Yes; m-independent closed-form boundary min** |
| 6 | Traceless-Frob `½(K11−K22)² + 2\|K12\|²` | retained-atlas-native | parity-mixing but degenerate (K11−K22 = −1/√3 constant) | No — q_+-blind |
| 7 | CP bilinear `c_even · c_odd` ([odd-circulant Z2 slot](./DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md)) | retained theorem on DM circulant family | parity-mixing (bilinear of even/odd) | No — on the active sheet the singlet-slot is frozen (K01 = a_*), so the bilinear is a constant |
| 8 | Positive polar H CP tensor ([positive-polar](./DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md)) | retained theorem | parity-mixing in right-Gram slots | Not directly on (δ, q_+); lives in `(d_i, r_ij, φ)` |
| 9 | Z_3 phase-lift mixed bridge ([phase-lift](./DM_NEUTRINO_Z3_PHASE_LIFT_MIXED_BRIDGE_NOTE_2026-04-15.md)) | **invented post-axiom family** | genuinely parity-mixing | **Not usable** — post-axiom |
| 10 | Odd-mixed-bridge extension ([extension note](./DM_NEUTRINO_ODD_MIXED_BRIDGE_EXTENSION_NOTE_2026-04-15.md)) | extension-class only (no construction) | classifies activator class | **Not usable** — no derivation |
| 11 | CP-kernel deformation necessity ([necessity note](./DM_NEUTRINO_CP_KERNEL_DEFORMATION_NECESSITY_NOTE_2026-04-15.md)) | retained necessary-condition theorem | classifies deformation class | **Not usable** — no construction |
| 12 | Cubic `Tr(J_act³) = 12 Re(w³)` | retained structural lemma | genuine parity-mixing | already obstructed by the cubic variational route — m-dependent boundary extremum, joint CPs singular |
| 13 | PMNS selector class `S_cls` ([unique amplitude slot](./PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md)) | retained reduced-form theorem | structural framing | **Not usable** — one-amplitude slot, no delta/q_+ coupling |

**Classification summary:**
- **Sufficient (parity-mixing + evades the parity-split theorem + couples both δ and q_+):** candidates 4, 5 (and 12 in cubic-variational-obstructed sense).
- **Insufficient (parity-definite or already-obstructed):** 1, 2, 3, 6, 7 on active sheet, 12 (already cubic-variational-obstructed).
- **Not usable (post-axiom, necessary-only, or in different carrier space):** 8, 9, 10, 11, 13.

Candidate 5 (`||K_doublet||_F^2`) emerges as the strongest retained-atlas-native
parity-mixing invariant because:
- it is positive-definite, so "minimum" is well-defined,
- it is m-independent in its chamber-boundary minimizer,
- its minimizer is a closed-form retained-atlas expression, and
- its definition is entirely theorem-grade (doublet-block + intrinsic-slot
 + Schur-baseline + active-affine chart — all retained).

## Theorem (Parity-Mixing Decomposition)

**Theorem (retained-atlas-native).** On the active source-oriented sheet
`H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`, every
quadratic trace invariant of the Z_3 doublet block `K_doublet = K[1:3, 1:3]`
splits as a sum of two Z_3-parity-definite scalars:

```
||K_doublet||_F^2 = [K11^2 + K22^2] + [2 |K12|^2]
   \\_______________/ \\___________/
   Z_3-EVEN sector Z_3-ODD sector
   depends on q_+ depends on delta, m
   only   (not q_+)

det K_doublet = [K11 · K22] - [|K12|^2]
   \\__________/ \\__________/
   EVEN sector  ODD sector
```

**Corollary.** The gradient of any such SUM decouples parity-by-parity:
`∂/∂(delta)` sees only the odd-sector piece, `∂/∂(q_+)` sees only the
even-sector piece. Hence the joint stationarity condition reduces to two
independent 1D conditions — **one on δ alone and one on q_+ alone**.

**Significance.** This construction **evades** the parity-split single-parity
obstruction theorem (parity-split Theorem 2 obstructs any scalar depending on
`sym(H)` OR `anti(H)` alone; a SUM of two parity-definite scalars depends
on both but its gradient still decouples). This is the single missing
structural observation that distinguishes the parity-mixing class from
the parity-definite class ruled out in the Z_3 parity-split theorem.

**Proof.** Use the retained theorem-grade closed forms from
[DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md):
```
K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3))
K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3))
K12 = (m - 4 sqrt(2)/9) + i (sqrt(3) delta - 4 sqrt(2)/3)
```
`K11, K22` depend only on `(m, q_+)` (on the active sheet `m`-shift is
trivial since neither contains `m`), hence on `q_+` only. `K12` depends
only on `(m, delta)`. The stated split and gradient decoupling are
immediate.

**Claim label.** *Retained-atlas-native theorem.* Direct algebraic
consequence of the retained Z_3 doublet-block point-selection theorem.
No new axiom.

## Theorem (Closed-Form Parity-Mixing F1-Minimizer)

**Theorem (retained-atlas-native).** Under the Schur-forced baseline
`D = m I_3`, on the chamber boundary `q_+ = sqrt(8/3) − delta`, the
parity-mixing functional `F1(m, delta, q_+) := ||K_doublet||_F^2` has a
unique m-independent chamber-boundary minimizer

```
delta_* = sqrt(6)/2 - sqrt(2)/18 ≈ 1.1461774513
q_+* = sqrt(6)/6 + sqrt(2)/18 ≈ 0.4868157106
m_* = 4 sqrt(2)/9  ≈ 0.6285393611
```

and the unconstrained minimum (outside the chamber) is at
`(delta, q_+) = (4 sqrt(6)/9, 2 sqrt(2)/9) ≈ (1.0887, 0.3143)`.

**Proof.** Expand `F1` on the boundary, setting `q = sqrt(8/3) − delta`:
```
K11 + K22 = 2(-q + 2 sqrt(2)/9) = 2 delta - 2 sqrt(8/3) + 4 sqrt(2)/9
K11^2 + K22^2 = (K11+K22)^2/2 + (K11-K22)^2/2
  = (1/2) [2 delta - 2 sqrt(8/3) + 4 sqrt(2)/9]^2 + 1/6
2 |K12|^2 = 2 (m - 4 sqrt(2)/9)^2 + 2 (sqrt(3) delta - 4 sqrt(2)/3)^2
```
Then `d F1 / d delta = 0` gives
```
2 [2 delta - 2 sqrt(8/3) + 4 sqrt(2)/9] · 2 + 4 sqrt(3) (sqrt(3) delta - 4 sqrt(2)/3) = 0
```
Simplifying:
```
16 delta = 4 sqrt(8/3) - 8 sqrt(2)/9 + 48 sqrt(6)/9
  = 8 sqrt(6) - 8 sqrt(2)/9
delta_* = sqrt(6)/2 - sqrt(2)/18
```
The boundary gives `q_+* = sqrt(8/3) − delta_* = 2 sqrt(6)/3 − (sqrt(6)/2 − sqrt(2)/18) = sqrt(6)/6 + sqrt(2)/18`.
The m-dependent piece `2 (m − 4 sqrt(2)/9)^2` is `(delta, q_+)`-independent
and factors out, giving m-independence of `(delta_*, q_+*)` and
`m_* = 4 sqrt(2)/9`. ∎

**Numerical verification.** The runner verifies m-independence across
`m ∈ {0.1, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0}` to tolerance 1e-6.

**Asymmetry from Schur-Q.**
```
delta_* - sqrt(6)/3 = +(3 sqrt(6) - sqrt(2))/18 ≈ +0.329681
q_+* - sqrt(6)/3 = -(3 sqrt(6) - sqrt(2))/18 ≈ -0.329681
```
The parity-mixing F1-minimizer is displaced from the Schur-Q symmetric
minimum `(sqrt(6)/3, sqrt(6)/3)` by `±(3 sqrt(6) − sqrt(2))/18` along
the chamber-boundary diagonal `delta + q_+ = sqrt(8/3)`.

## Obstruction (Parity-Mixing Functional-Selection Ambiguity)

**Theorem.** The three natural retained-atlas parity-mixing invariants
`{F1, F2, F3}` select **DIFFERENT** chamber-boundary extrema:

```
F1 = ||K_doublet||_F^2  -> boundary min at delta ≈ 1.1462
F2 = det K_doublet (boundary max) -> boundary max at delta ≈ 0.9736
F3 = ||K_doublet - (TrK/2)I||_F^2 -> degenerate in q_+ (K11 - K22 const)
```

This is the **parity-mixing analog of the info-geometric Cubic Splitting
Obstruction (Theorem B)**. The info-geometric Quadratic Unanimity Theorem
from the info-geometric selection obstruction note states that all natural info-geometric functionals agree at
`(sqrt(6)/3, sqrt(6)/3)` at leading quadratic order; the parity-mixing
analog **FAILS**: there is no parity-mixing unanimity.

**Consequence.** Selecting F1 as the canonical parity-mixing functional
requires an additional axiom-native selection rule (analog of `(G-Var)`).
The retained atlas does not supply one.

**Claim label.** *Obstruction / narrower-gap.* Parity-mixing class also
requires a canonical-functional selection axiom to close the selector gate.

## Verdict

**Classification of all parity-mixing candidates:**

- **SUFFICIENT (passes all three info-geometric / cubic-variational / parity-split obstructions, produces a
 unique m-independent closed-form minimizer):** F1 `= ||K_doublet||_F^2`
 alone, provided a min-selection axiom is available.
- **INSUFFICIENT:** det K_doublet (saddle, unconstrained crit outside
 chamber); traceless-Frob (degenerate in q_+); cubic Tr(J^3) (already
 cubic-variational-obstructed); CP bilinear c_even c_odd (constant on active
 sheet because K01 is the frozen intrinsic slot a_*); positive-polar
 H CP tensor (lives in right-Gram space, not (δ, q_+)).
- **NOT USABLE (post-axiom, necessary-only, or orthogonal carrier):**
 phase-lift mixed bridge, odd-mixed-bridge extension, CP-kernel
 deformation necessity, PMNS selector amplitude slot.

**Overall verdict:** **narrower-gap + closure-candidate-pending-physics-cross-check.**
Not a theorem-grade closure.

The parity-mixing class:
- produces a **new candidate selector point**
 `(delta_F1, q_+F1) = (sqrt(6)/2 − sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18)`,
- evades the parity-split theorem (single-parity obstruction) by construction,
- is **inequivalent** to Schur-Q `(sqrt(6)/3, sqrt(6)/3)` and to every
 the parity-split mixed invariant,
- **but** exhibits parity-mixing functional-selection ambiguity,
 requiring a canonical-functional axiom.

## Physics-Validation discipline

The cumulative candidate ledger now contains **five** inequivalent
retained-atlas-native points for `(delta_*, q_+*)`:

| Candidate | (δ, q_+) | Source |
|-----------|----------|--------|
| Schur-Q variational | `(sqrt(6)/3, sqrt(6)/3) ≈ (0.8165, 0.8165)` | info-geometric / cubic-variational, Schur-baseline minimum-coupling |
| det(H) stationary | `(0.9644, 1.5524)` | (a) chamber-interior |
| Tr(H²) chamber-bdy min | `(1.2679, 0.3651)` | (b) |
| K_12 char-match | `(0.8000, q_+ free)` | (c) |
| **Parity-mixing F1-min** | `(sqrt(6)/2 − sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18) ≈ (1.1462, 0.4868)` | **THIS NOTE** |

**Physics-Validation discipline (follow-up requirement):** Evaluate the
DM transport chain at each of the five candidate points. If one lands at
`eta / eta_obs = 1`, it is a compelling candidate closure for selector that
deserves theorem-grade pursuit in its own right, with a sharpened
obligation to explain why the other four candidates miss the physical
point. If none lands at `1`, the selector gate is obstructed across all
currently-tested microscopic classes (info-geom, cubic, parity-definite,
parity-mixing).

At least one candidate (Schur-Q) is known to give
`eta / eta_obs ≈ 0.189` at the current theorem-native radiation branch;
the PMNS-assisted route is required to reach 1. Cross-check of the
parity-mixing F1-min candidate is recorded here as a **follow-up
discipline requirement** for Physics-Validation.

## Narrowed-gap statement

**Before this note (after the info-geometric / Z_3-cubic / parity-split obstructions):**
```
(G-Var) variational selection axiom unclosed; info-geom
  functionals agree at sqrt(6)/3 at LEADING QUADRATIC only
(G-Non-Var) non-variational obstructed along Z_3-parity-definite;
  mixed-invariant candidates disagree with sqrt(6)/3
parity-mixing sub-class: untested
```

**After this note:**
```
(G-Var) unchanged -- still requires selection axiom
(G-Non-Var) parity-mixing sub-route TESTED:
  - evades parity-split Theorem 2 by sum-of-parity-definite construction
  - produces NEW candidate point
   (sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18)
  - parity-mixing unanimity FAILS (F1, F2, F3 disagree)
  - parity-mixing sub-route ALSO needs canonical-functional axiom
```

All three classes (info-geom, cubic, parity-mixing) produce inequivalent
candidate points; each requires an additional selection axiom. The selector gate
gap is strictly narrower than before: the parity-mixing class is no
longer open. It is now classified as "narrower-gap via functional-
selection ambiguity", matching the sibling status of the information-geometric selection obstruction `(G-Var)`.

## Atlas inputs used

All retained / theorem-grade on the integration branch:

- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
 — exact closed forms for K_11, K_22, K_12
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
 — frozen singlet-doublet slots (a_*, b_*)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
 — exact affine chart and active generators
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
 — chamber `q_+ >= sqrt(8/3) - delta`
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)
 — Schur baseline D = m I_3 and theorem-native curvature Q
- [DM_NEUTRINO_SOURCE_SURFACE_INFO_GEOMETRIC_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_INFO_GEOMETRIC_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md)
 — Quadratic Unanimity, Cubic Splitting Obstruction, Structural
 Obstruction, narrowed-gap (G-Var)/(G-Non-Var) split
- [DM_NEUTRINO_SOURCE_SURFACE_CUBIC_VARIATIONAL_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_CUBIC_VARIATIONAL_OBSTRUCTION_NOTE_2026-04-17.md)
 — cubic obstruction theorem
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md)
 — Z_3-parity split theorem, single-parity obstruction, mixed-invariant
 cross-check candidates

Post-axiom / not used as theorem input (reviewed and rejected as
parity-mixing selector candidates for sole-axiom derivation):

- [DM_NEUTRINO_Z3_PHASE_LIFT_MIXED_BRIDGE_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_PHASE_LIFT_MIXED_BRIDGE_NOTE_2026-04-15.md)
 (flagged invented axiom-native family)
- [DM_NEUTRINO_ODD_MIXED_BRIDGE_EXTENSION_NOTE_2026-04-15.md](./DM_NEUTRINO_ODD_MIXED_BRIDGE_EXTENSION_NOTE_2026-04-15.md)
 (extension-class only)
- [DM_NEUTRINO_CP_KERNEL_DEFORMATION_NECESSITY_NOTE_2026-04-15.md](./DM_NEUTRINO_CP_KERNEL_DEFORMATION_NECESSITY_NOTE_2026-04-15.md)
 (necessary-condition only)
- [DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ODD_CIRCULANT_Z2_SLOT_THEOREM_NOTE_2026-04-15.md)
 (CP-bilinear c_even c_odd; the singlet slot K01 on the active sheet is
 frozen, so this bilinear is a constant on the active sheet)
- [DM_NEUTRINO_ODD_CIRCULANT_CURRENT_STACK_ZERO_LAW_NOTE_2026-04-15.md](./DM_NEUTRINO_ODD_CIRCULANT_CURRENT_STACK_ZERO_LAW_NOTE_2026-04-15.md)
 (current stack does not turn on c_odd; zero-law)

No new axioms are introduced.

## Position on publication surface

This note is **not** publication-grade on its own. It is a claim-surface
advance on the selector gap structure: the parity-mixing class is no longer
classified as "untested" — it is now classified as "narrower-gap via
functional-selection ambiguity", matching the sibling status of the information-geometric selection obstruction
`(G-Var)`.

Appropriate placement:

- atlas obstruction row in
 [DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md)
 under the DM neutrino source-surface family, sibling to the info-geometric / Z_3-cubic / parity-split obstructions
- **do NOT** use for any publication-grade positive quantitative claim
- **do NOT** use to "justify" the Schur-Q variational candidate — this
 note actively produces a competing candidate
- **do NOT** promote the parity-mixing F1-min candidate to theorem-grade
 without a sole-axiom derivation of the functional-selection axiom and
 a Physics-Validation cross-check via eta/eta_obs = 1

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_parity_mixing_selection_obstruction.py
```

Current expected: `PASS = 27, FAIL = 0`.

## What this file must never say

- that selector is closed
- that the DM flagship gate is closed
- that the parity-mixing F1-min candidate is the physical `(delta_*, q_+*)`
 (it is a closure-candidate-pending-physics-cross-check, not a selector
 theorem)
- that the parity-mixing class is closed (it is obstructed by functional-
 selection ambiguity; a canonical-functional axiom is still missing)
- that the Schur-Q candidate has been ruled out (it remains one of five
 inequivalent candidates)
- that the Z_3 phase-lift mixed-bridge family has been promoted from
 post-axiom (it has not)

If any future revision of this note tightens those boundaries, it must
cite a new source on the live retained/promoted surface. Until then, the
safe read is: **parity-mixing class narrower-gap + closure-candidate-
pending-physics-cross-check; the selector gate remains OPEN with five inequivalent
candidate points now on record**.
