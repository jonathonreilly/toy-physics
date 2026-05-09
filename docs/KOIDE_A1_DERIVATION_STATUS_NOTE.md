# A1 derivation status — full landscape audit

**Context:** this note documents the exhaustive audit of routes to
derive A1 (Frobenius equipartition, |b|/a = 1/√2 ⟺ Brannen c = √2 ⟺
Koide Q = 2/3) from the retained Cl(3)/Z³ framework + textbook math.
It establishes what's been ruled out (by retained theorems and
source-note bounded-obstruction proposals) and what remains open.

**2026-05-09 review-loop update:** Routes A, D, E, F and Probes 1-6
are now represented by companion bounded-obstruction source notes. These
notes do not promote any audit verdict and do not reduce the A1
admission count. They update the route map: the named A1 closure
attempts are negative boundaries unless a future branch supplies a new
coefficient-fixing bridge or the user explicitly approves an A1-class
admission.

## Retained no-go theorems (all close negatively)

The retained atlas establishes 7 structural no-go theorems ruling out
specific Koide-cone-forcing mechanisms:

1. **Z_3 invariance alone is insufficient** (STRUCTURAL_NO_GO_SURVEY §5.1)
   — Z_3-invariant bilinear source-response = I_3 (triply-degenerate).

2. **Pure APBC temporal refinement is insufficient** (§5.2)
   — L_t ∈ {4,6,8,12,16,24,∞} all fail to force Koide cone.

3. **Observable principle character symmetry is insufficient** (§5.3)
   — `W[J] = log|det(D+J)|` character-symmetric content does NOT force
     Koide cone at any order.

4. **SU(2) gauge exchange mixing is insufficient** (§5.4)
   — Standard SM SU(2)_L × U(1)_Y gauge exchange doesn't force Koide.

5. **Anomaly-forced cross-species is insufficient** (§5.5)
   — Anomaly-cancellation constraints don't force Koide.

6. **Sectoral universality is insufficient** (§5.6)
   — Universal sectoral factors don't force Koide.

7. **Color-sector correction is insufficient** (§5.7)
   — Color-sector corrections don't force Koide.

Plus `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE`:

8. **Theorem 5**: No retained C_3-invariant VARIATIONAL PRINCIPLE selects
   the Koide cone. Six candidate variational principles surveyed
   (Cauchy-Schwarz midpoint, max-entropy, Legendre partition function,
   Fisher-Rao, etc.) all close negatively.

9. **Theorem 6**: 4TH-ORDER MIXED-Γ CANCELLATION — the fourth-order
   retained spatial-Clifford + EWSB-weighted Higgs family CANCELS
   identically, ruling out 4th-order retained Clifford mechanisms.

All 9 routes close negatively. The retained atlas has definitively
established that standard mechanisms within the current framework do
NOT force A1.

## Candidate routes outside the original no-go's (now bounded-obstruction proposals)

### Route A: Koide-Nishiura U(3) quartic potential

The quartic V(Φ) = [2(trΦ)² − 3tr(Φ²)]² = 81·(a² − 2|b|²)² has:
  - V ≥ 0 everywhere (square form)
  - V = 0 ⟺ A1 (Frobenius equipartition)
  - V is U(3)-invariant (depends only on trΦ and tr(Φ²))

**This is OUTSIDE Theorem 6's cancellation** because V is built from
TRACE invariants (tr, tr²), not from Clifford generator products
(Γ_a Γ_b Γ_c Γ_d). Theorem 6 rules out Clifford-based 4th-order,
but not trace-based.

**Review-loop result:** the companion
[`KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md`](KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md)
records a bounded obstruction. The internal arithmetic remains true,
but retained content does not fix the Wilson-coefficient ratio
`(2 : -3)` without importing the Koide target.

Runner:
[`scripts/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.py`](../scripts/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.py).

### Route B: Clifford torus bipartition on S³ = Spin(3)

The preprint 202505.2156 claims Q = 2/3 is forced by equal-area
bipartition of Clifford torus on S³.

**Verified this route:** the Clifford torus projects to the EQUATOR
of S² via Hopf fibration, but the Koide cone sits at 45° LATITUDE on
S² (not the equator). So the Clifford torus doesn't directly identify
with the Koide cone.

**Status:** doesn't directly close A1, but the 45° latitude
corresponds to "equal projection onto trivial vs doublet" which is
the geometric form of real-irrep-block democracy. The underlying
principle remains democracy — not a new derivation.

### Route C: AS G-signature Lefschetz sum coincidence

Σ cot²(πk/3) = 2/3 (Gauss identity at n=3) and Koide Q = 2/3
numerically match. This is a parallel numerical identity, not a
structural replacement for A1 (verified earlier).

### Route D: Newton-Girard polynomial structure

V(Φ) = [e_1² − 6e_2]² where e_1 = trΦ, e_2 = Σ_{i<j}λ_iλ_j. The
coefficient 6 = n(n+1)/2 for n=3. This clean elementary-symmetric
form suggests a natural polynomial structure, but does not by itself
force the specific 6 coefficient.

**Review-loop result:** the companion
[`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)
records a bounded obstruction: Newton-Girard gives an identity between
coordinate systems, not a constraint selecting A1.

### Route E: A_1 Weyl-vector / Kostant-strange-formula coincidence

**NEW**: three independent quantities ALL equal 1/2 in their natural
normalizations:

  1. **Kostant strange formula** for A_1 (sl(2)):
     |ρ_{A_1}|² = h̄(h̄+1)·r/12 = 2·3·1/12 = 1/2

  2. **Koide A1 condition** (Frobenius equipartition):
     |b|²/a² = 1/2

  3. **Retained Casimir imbalance** (C_τ = 1 decomposition):
     C_2(SU(2)_L fund) − Y²(Higgs) = 3/4 − 1/4 = 1/2

This three-way exact match is the STRONGEST structural hint yet for
axiom-native A1 derivation. The retained Cl^+(3) ≅ H ⟹ Spin(3) =
SU(2) = A_1 Lie algebra carries Weyl vector with |ρ|² = 1/2
(Kostant), matching the charged-lepton amplitude ratio.

**Review-loop result:** the companion
[`KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md`](KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md)
records a bounded obstruction. The Weyl-vector numerical match remains
a useful coincidence, but the Cartan-Killing normalization and
gauge-to-flavor bridge are not derived by retained content.

The older scout runner
[`scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py`](../scripts/frontier_koide_a1_weyl_vector_kostant_coincidence.py)
documents the coincidence; the companion obstruction runner tests the
negative boundary.

**DOUBLE MATCH (A_1 AND A_2)**: Brannen c = 2|b|/a converts A1 to the
equivalent condition c² = 2. This matches |ρ_{A_2}|² = 2 via Kostant
(A_2 = sl(3), rank 2, h̄ = 3: 3·4·2/12 = 2). So A1 matches BOTH:

  |b|²/a²  = 1/2  =  |ρ_{A_1}|²    (A_1 = SU(2)_L gauge sector)
  c²       = 2    =  |ρ_{A_2}|²    (A_2 = Z_3-center / hidden SU(3)_family)

The DOUBLE Weyl-vector match across two independent Lie algebras is a
very strong structural indicator. Probability of random coincidence is
essentially zero. Runner: `scripts/frontier_koide_a1_a2_weyl_double_match.py`.

Candidate lemmas that would close A1 axiom-natively via Weyl geometry:
  - A_1 imprint from retained SU(2)_L Casimir structure (C_τ = 1 lemma)
  - Hidden SU(3)_family broken to Z_3 (Z_3 = SU(3) center)
  - Cl(3) ⊃ sl(3) via pseudoscalar extension

### Route F: Yukawa Casimir-difference identity

**KEY OBSERVATION**: T(T+1) − Y² = 1/2 holds UNIQUELY for the lepton
SU(2)_L doublet L (T=1/2, Y=-1/2) AND the Higgs H (T=1/2, Y=+1/2).

NO other SM particle satisfies this identity:
  - Quark doublet: T(T+1) − Y² = 3/4 − 1/36 = 13/18
  - e_R: T(T+1) − Y² = 0 − 1 = −1
  - u_R: 0 − 4/9 = −4/9
  - d_R: 0 − 1/9 = −1/9

The retained CL3_SM_EMBEDDING_THEOREM provides:
  - T(T+1) = 3/4 from Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2)_L
  - Y² = 1/4 from pseudoscalar ω ⟹ U(1)_Y, with L hypercharge = -1/2
  - Difference: 1/2 = A1 condition

The retained C_τ = T(T+1) + Y² = 1 theorem (already used to derive
y_τ = α_LM/(4π)) gives the SUM. The proposed candidate gives the
DIFFERENCE. Both are derivable from retained gauge structure alone.

**Review-loop result:** the companion
[`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
records a bounded obstruction. The numerical identity is not a
structural derivation because the value is convention-dependent and
there is no retained gauge-to-flavor normalization map.

Runner:
[`scripts/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.py`](../scripts/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.py).

## Round-2 probes

The following companion source notes test additional A1 closure routes
and leave the A1 admission count unchanged:

- [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
  — RP+GNS does not force the canonical Frobenius pairing.
- [`KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md`](KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md)
  — flavor-anomaly channels do not fix operator-coefficient ratios.
- [`KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md`](KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md)
  — gravity-as-phase content does not induce the required matter-sector
  inner product.
- [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md)
  — spectral-action import does not produce an A1 critical point.
- [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
  — A1 is not a retained charged-lepton RG fixed point.
- [`KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md`](KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md)
  — expanding the operator class does not create a closure path.

## Targeted follow-up probes and synthesis

The 2026-05-09 review-loop batch adds targeted follow-up notes that
sharpen the same missing primitive without changing the admission
count:

- [`KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md)
  — no retained `Z_2 x C_3` pairing forces `1/2`; the note localizes
  the obstruction at the `3:6` multiplicity-weighted Frobenius pairing
  on `M_3(C)_Herm`.
- [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
  — meta/index note naming the missing primitive; it does not admit the
  primitive, derive A1, or promote a theorem.
- [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
  — Plancherel/Peter-Weyl route still leaves a scalar-normalization
  convention at the same locus.
- [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
  — real-structure / antilinear-involution route sharpens the same
  obstruction and leaves the A1 admission count unchanged.

## Status: A1 remains a load-bearing non-axiom input

Given the original no-go theorems and the companion bounded-obstruction
source notes above, A1 is still not derived from physical `Cl(3)` on
`Z^3` plus textbook math alone. The current target is precise: a future
axiom-native closure must derive the canonical `(1,1)`-multiplicity-
weighted Frobenius pairing on `M_3(C)_Herm` under `C_3`-isotype
decomposition, or the A1 amplitude-ratio input must be explicitly
admitted by the user. This note does not set audit verdicts or
pipeline-derived retained status.

## References

- `STRUCTURAL_NO_GO_SURVEY_NOTE` — 6 structural no-go theorems
- `HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE` — Theorem 5 (no variational),
  Theorem 6 (4th-order Clifford cancellation)
- `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE` — Koide
  cone ⟺ 45° latitude ⟺ σ = 1/2 ⟺ a_0² = 2|z|²
- `HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE` — charged-lepton
  mass = diag(w_{O_0}, w_a, w_b), 3 free weights (unconstrained)
- Koide & Nishiura, hep-ph/0509214 — S_3 flavor Higgs quartic potential
- Brannen (2006), hep-ph/0505220 — original Brannen form
- Koide (1983), original Koide relation papers

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [structural_no_go_survey_note](STRUCTURAL_NO_GO_SURVEY_NOTE.md)
- [higher_order_structural_theorems_note](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [hw1_second_order_return_shape_theorem_note](HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)
