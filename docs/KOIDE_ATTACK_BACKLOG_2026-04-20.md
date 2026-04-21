# Koide Attack Backlog (self-paced loop, 2026-04-20+)

**Purpose:** Candidate attacks for the loop that will close I1, I2/P, and
I5 to retained-derived theorem-grade with no reviewer cracks.

**User's "done" criteria (2026-04-20 late night):**
> "fully closed retained derived with no open doors for a reviewer to
>  push on no cracks in the wall top to bottom I1 I2, then I5"

## Current status (start of loop)

- **I1**: CONDITIONAL on (C1) Peter-Weyl prescription retention.
- **I2/P**: DISCHARGED from (C2) via topological robustness (iteration 1).
  Now UNCONDITIONAL given retained C_3[111] spatial rotation.
- **I5**: PMNS observational pins (NuFit 3σ ranges, T2K `sin δ_CP < 0`)
  still retained-observational. Needs framework-native derivation.

## Iteration 1 (completed)

**Attack**: C2 discharge via topological robustness of equivariant APS η.
**Runner**: `scripts/frontier_koide_aps_topological_robustness.py` (41/41 PASS).
**Outcome**: C2 discharged. Atiyah-Bott-Segal-Singer fixed-point formula
depends only on tangent rep, not metric. Thus δ = 2/9 rad is metric-
independent given the retained kinematics.

## Iteration 2 (completed)

**Attack**: C1 discharge via AM-GM on isotype Frobenius energies.
**Runner**: `scripts/frontier_koide_peter_weyl_am_gm.py` (24/24 PASS).
**Outcome**: C1 discharged. F = log(E_+·E_⊥) under fixed E_+ + E_⊥ = N
forces max at E_+ = E_⊥ ⟺ κ = 2 ⟺ Q = 2/3 by AM-GM inequality. The
"Peter-Weyl weighting" is a renaming of the Frobenius isotype metric,
not a separate prescription.

## Iteration 3 (completed)

**Attack**: I5 leading-order — PMNS V_TBM from S_3 axis-permutation symmetry.
**Runner**: `scripts/frontier_koide_pmns_tbm_from_s3.py` (35/35 PASS).
**Outcome**: I5 INTERMEDIATE. The retained Z³ cubic S_3 symmetry forces
V_TBM as the leading-order PMNS matrix — the simultaneous real eigenbasis
of {C_3[111]-symmetrizer, P_{23}-reflection}. Diagonalizes every
S_3-invariant Majorana M_ν. Predictions:
- θ₁₂ = 35.264° (NuFit 33.44°, gap −1.82°)
- θ₁₃ = 0° (NuFit 8.57°, gap +8.57° DOMINANT "reactor angle")
- θ₂₃ = 45° (NuFit 49.2°, gap +4.20°)
Does NOT close I5; next iter targets θ₁₃ activation via Z_2 breaking.

## Iteration 4 (completed)

**Attack**: I5 conjecture-level closure via δ-Q deformation of TBM.
**Runner**: `scripts/frontier_koide_pmns_delta_q_deformation.py` (25/25 PASS).
**Outcome**: I5 RETAINED-PREDICTIVE-CONJECTURE. All three NuFit-2024
mixing angles fit **within 1σ** from just retained (Q, δ) = (2/3, 2/9):
- θ₁₃ = δ·Q = 4/27 rad = 8.488° (NuFit 8.57°, inside 1σ)
- θ₂₃ − π/4 = δ·Q/2 = 2/27 rad = 4.244° (NuFit 49.2°, inside 1σ)
- sin²θ₁₂ = 1/3 − δ²·Q = 73/243 = 0.3004 (NuFit 0.307, inside 1σ)
Bonus: J_max at δ_CP=π/2 = 0.0327, matches T2K best-fit magnitude.
Rational denominators are powers of 3 (Z_3 orbifold signature).
Distinct from TM1 and TM2. NOT yet derived from first principles —
iter 5 target is the mechanism.

## Iteration 5 target (next loop)

**Attack**: Derive at least one of the δ-Q coefficient formulas
(NT1: θ₁₃=δQ, NT2: factor 1/2 in θ₂₃, NT3: coefficient −1 in sin²θ₁₂)
from retained Cl(3)/Z³ mechanism.

Specific sub-attacks to try:
- **Effective TBM-perturbation Lagrangian**: Write most general
  S_3-breaking, (Q, δ)-coupled operator and derive coefficients.
- **Cl(3) bivector rotation by δ in C_3-doublet plane**: Compute
  induced mixing angle; does it give exactly δ·Q?
- **Jarlskog natural-value argument**: Require J_max = 0.0327
  (T2K best-fit) as retained consistency; does it pin angles?
- **δ_CP sign from CP structure of Cl(3)**: T2K sign < 0 target.
- **PMNS = V_TBM · U_correction**: derive U_correction from retained
  SELECTOR bivector rotation.

## Long-tail brainstorm (priority-unranked)

### For I1 (C1 Peter-Weyl discharge)

- **Haar measure uniqueness**: show Peter-Weyl is the unique prescription
  compatible with translation invariance on Z_3 + trace normalization.
- **Coherent state expectation values**: show F-functional arises as
  the entropy of Z_3 coherent states on Herm_circ(3).
- **Free cumulants on the group algebra**: use non-commutative
  probability theory to derive the cumulant-isotype weighting.
- **Schur-Weyl duality**: GL(d) × S_d duality on V^⊗d might force the
  specific weighting.
- **Plancherel measure on Ẑ_3**: normalize by (dim irrep)² = 1² = 1
  for each Z_3 character; combined with Z_3 counting gives (2, 1) weights
  for F.

### For I2/P (further strengthening beyond C2 discharge)

- **PL-equivariant index theorem** (Cheeger-Goresky-MacPherson style):
  show APS η for PL structures extends cleanly, matching smooth case.
- **Cohomological uniqueness**: η is well-defined on any topological
  Z_3 orbifold with (1, 2) weights, by a K-theory classification
  argument.
- **Explicit witness computation**: lift Brannen δ to explicit Dirac
  spectral asymmetry on a retained lattice Dirac operator with Z_3
  action.

### For I5 (PMNS)

- **Tribimaximal (TBM) ansatz** from retained C_3: TBM gives
  sin²(2θ_12) = 8/9, sin²(2θ_23) = 1, θ_13 = 0. Not quite right but
  a starting point.
- **Z_3 × Z_2 deformations of TBM**: small corrections from retained
  Cl(3) breaking patterns.
- **Majorana vs Dirac CP phase distinction**: retained Cl(3) structure
  might pick one over the other.
- **Sign of sin δ_CP**: from CP violation structure of retained anomaly-
  cancelled SM content.
- **Mass-matrix texture from Cl(3) plus C_3[111]**: fix PMNS angles
  via specific structural zeros.
- **Retained Clifford-native neutrino Yukawa**: derive from anomaly
  cancellation + neutrino masses.
- **Brannen-like Koide for neutrinos**: δ_ν = 2/9 + π/12 conjecture
  (literature). If retained, determines NuFit angles.

### Long-shot ideas

- **Octonion / E8 unification structure**: retained Cl(3)/Z³ might
  embed in octonion-based E8 unification, which fixes Koide + PMNS
  + quark masses simultaneously.
- **Modular form special values**: continue modular-form hunt
  (Round 2's CM attempt was partial — try different level/weight).
- **Knot invariants of retained 3+1 spacetime**: specific invariants
  of PL S³ × R might give PMNS-Koide closure.
- **Holographic / AdS correspondence**: if retained Cl(3)/Z³ has a
  gravity dual, PMNS comes from boundary CFT data.

## Loop discipline

1. **Each iteration**: pick ONE attack from the backlog. Execute to
   completion (runner + docs). Commit. Push.
2. **If no good idea**: use that turn as a BRAINSTORM turn. Add new
   candidates to this backlog.
3. **Never push noise**: only push theorem-grade artifacts.
4. **Always reconcile**: each new attack must honestly address existing
   no-gos and retained notes. No overclaiming.
5. **Stop when**: I1, I2/P, and I5 are ALL retained-derived with no
   reviewer cracks, or backlog is genuinely exhausted.
