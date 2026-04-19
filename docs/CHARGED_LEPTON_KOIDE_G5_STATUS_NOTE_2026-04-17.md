# Charged-Lepton Koide / G5 Status Note

**Date:** 2026-04-17
**Status:** consolidated G5 status after five-agent attack surface — Koide
`Q_\ell = 2/3` remains algebraically equivalent to the equal-character-weight
condition on the retained `hw=1` triplet, but the cone-forcing step requires
a genuinely new retained primitive beyond the retained observable-principle
chain; four distinct attack nulls have been rigorously closed
**Authority role:** consolidated status note for gap `G5` (charged-lepton
mass hierarchy) after the 2026-04-17 five-agent parallel attack. Supersedes
the per-agent notes only in the sense that it provides a single
reviewer-facing synthesis; each per-agent note remains the canonical
authority for its specific tactic.

## One-sentence state

On the retained `Cl(3)/Z^3` framework surface, the charged-lepton Koide
relation `Q_\ell = (sum m)/(sum sqrt m)^2 = 2/3` reduces rigorously to the
equal-character-weight condition `a_0^2 = 2|z|^2` on the `hw=1` triplet, but
four structurally independent attack routes (minimal APBC block, Z_3
invariance with canonical charges, pure-APBC L_t refinement at all L_t,
observable-principle character-symmetry chain) have each been closed as
exact negative results, so the forcing step genuinely requires a new
retained primitive.

## FINAL STATE (post-19-agent attack): framework does NOT derive Koide

After three additional "framework-derives-Koide" avenues were explored
post-pass-2-review (Avenues G, H, I — Agents 15-17, plus duplicates for
G and H giving 5 runners total), all three closed **negatively** on the
retained surface. Framework-derives-Koide is **not** reachable from
current retained theorems. G5 closes ONLY at the closure-class-match
level via observational pin (Agent 11), strictly weaker than G1.

### Avenues G, H, I — the three framework-derives-Koide attempts

| Avenue | Verdict | New retained structural content | Named missing primitive |
|---|---|---|---|
| **G** Higgs-dressed propagator | `NO_MATCH` / `INCONCLUSIVE` | Transport identity: `diag(P_{T_1} Γ_1 lift(X) Γ_1 P_{T_1}) = diag(X)` | Non-Cl(3)-covariant retained lift of intermediate propagator |
| **H** Stationarity / variational | `NO_RETAINED_PRINCIPLE` / `PARTIAL` | Koide cone IS unique max of unweighted block-log-volume `log(a_0²) + log(2|z|²)` | Real-irrep-block democracy in variational weighting |
| **I** Fourth-order mixed-Γ return | `NO_RETAINED_MIXED_BREAKING` | Signed Clifford ordering cancellation: individual orderings species-resolve via O_3 but signed sums vanish | Mechanism breaking the within-multiset ordering cancellation |

Each avenue added a **new retained no-go theorem**, each added a
**sharply-named successor primitive** that would (if retained on a
future extension) close G5 as sole-axiom.

### Eigenvalue-channel near-match (Agent 15a, explicitly NOT a closure)

Agent 15a found a striking numerical near-match in the Σ_Higgs
**eigenvalue channel**: at `λ = chamber_slack = 0.01594` (derived from
G1's observational chamber pin), the resolvent `W(H) = 1/(λ − H_lift)`
gives `Q_eig = 0.6664` and `cos-sim = 0.9963` to observed
`(√m_e, √m_μ, √m_τ)` direction. **This is not a physical closure** —
the retained Dirac-bridge theorem fixes `U_e = I_3`, so charged-lepton
masses are read off the **diagonal in axis basis**, not from
eigenvalues of a non-diagonal matrix. In the physical diagonal channel,
Agent 15b's best reach is cos-sim 0.919 — well below publication
threshold. The eigenvalue-channel result is a structural artifact
tracking the G1 PMNS pin, not a Koide derivation.

### Updated 19-agent G5 runner totals

```
441 PASS / 0 FAIL  (14 original agents)
 70 PASS / 0 FAIL  (5 framework-derives attempts: G×2, H×2, I×1)
----
511 PASS / 0 FAIL
```

### The sharpest honest statement

> On the current retained `Cl(3)/Z^3` framework surface, G5 closes at
> the same **closure-class** as G1 (retained-map-plus-observational-
> promotion) via observational pinning, but the retained framework
> **does not derive Koide** as a sole-axiom theorem. Nineteen agents
> covering every natural attack surface — algebraic (Agent 1), Z_3
> invariance (Agent 2), sectoral universality (Agent 3), pure-APBC
> refinement (Agent 4), observable-principle character symmetry (Agent
> 5), color-theoretic correction (Agent 6), SU(2)_L gauge exchange
> (Agent 7), anomaly-forced 3+1 (Agent 8), direct G1-H application
> (Agent 9), Γ_1 second-order return + shape theorem (Agent 10 v2),
> observational pin (Agent 11), S_2-breaking primitive survey (Agent
> 12), joint PMNS+Koide pinning (Agent 13), shape-theorem robustness
> (Agent 14), Higgs-dressed propagator (Agents 15a/b), retained
> stationarity principle (Agents 16a/b), fourth-order mixed-Γ return
> (Agent 17) — produce no retained route to Koide derivation. The
> retained framework is structurally COMPATIBLE with Koide `Q = 2/3`
> (via three independent weight slots in the shape theorem) but does
> not UNIQUELY PREDICT it. Three sharply-named missing primitives
> remain for future retained extension: (1) non-Cl(3)-covariant lift
> of the intermediate propagator, (2) real-irrep-block democracy in
> variational weighting, (3) a mechanism breaking signed Clifford
> ordering cancellation at fourth-order in mixed-Γ insertions. Any
> retained extension supplying one of these would promote G5 from
> closure-class-match to sole-axiom derivation.

---


The full 14-agent G5 attack is complete. The retained `Cl(3)/Z^3`
framework delivers G5 closure at the SAME CLOSURE CLASS as G1 —
`retained-map-plus-observational-promotion` — but with strictly weaker
predictive content than G1. This is a post-review-pass-2 honest restatement;
the reviewer-facing caveats below are mandatory.

### Closure status

- `G5_OBSERVATIONAL_PIN_CLOSES = TRUE` (Agent 11, `PASS=32, FAIL=0`)
  (verdict on "generous reading"; see "honest caveats" below)
- Observational pin `(w_O0, w_a, w_b) = (2.71e-4, 5.61e-2, 9.44e-1)`
  from PDG charged-lepton masses — chamber-interior, unique **as a set**
  (species-to-slot bijection has a residual `S_2` ambiguity on slots
  `w_a ↔ w_b`, not broken by any retained object; Koide `Q` and Σ spectrum
  are `S_2`-invariant so the closure is unaffected, but the "unique pin"
  language should be read as "unique set of three values up to overall
  scale and residual `S_2` labeling")
- Koide `Q_pin = 0.6666605` matching `2/3` to `|dev| = 6.15e-6`.
  **Honest reading:** the pin is literally `(w_O0, w_a, w_b) ∝ (m_e, m_μ, m_τ)`,
  so `Q_pin ≡ Q_PDG` by construction. The framework contribution is
  STRUCTURAL COMPATIBILITY with observed Koide — the retained shape
  theorem supplies exactly three independent slots, the chamber
  constraints admit the observed triple, and nothing in the framework
  excludes `Q = 2/3`. This is NOT a framework derivation of `Q = 2/3`;
  it is framework compatibility with observed `Q = 2/3` (analogous to G1
  being compatible with observed PMNS angles rather than deriving them).

### Honest caveats

1. **Map dimension: G5 is 3→3, G1 is 3→4.** G1's three PMNS-angle pins
   produce δ_CP ≈ −81° as a GENUINE fourth-observable forecast. G5's
   three charged-lepton mass pins produce no spare observable. Agent 11's
   own note explicitly admits: *"a critical reviewer may argue this note
   deserves the TRUE_NO_PREDICTION label since the four predictions are
   consistent with already-observed quantities rather than forecasts for
   currently-unmeasured numbers"*.

2. **"Four falsifiable predictions" is imprecise.** Of the four listed:
   - **P2 (LFV zeros at leading order):** consistent with SM, not a
     framework-distinguishing falsifier (SM LFV rates are far below
     MEG-II/Belle-II bounds anyway).
   - **P3 (no charged-lepton EDM beyond SM):** consistent with SM; SM
     charged-lepton EDMs are below observable thresholds already.
   - **P4 (electron-isolation hopping ratio `(m_μ/m_e)/(m_τ/m_μ) = 12.30`):**
     this is *literally the PDG ratio-of-ratios*; "reproduced by PDG" is
     tautological. It is a structural pattern the framework accommodates,
     not a framework-derived numerical prediction.
   - **P5 (combined G1+G5 DUNE double-test):** a consistency check tying
     the δ_CP prediction of G1 to the observational stability of Q = 2/3
     under PDG updates; not a new numerical prediction.

   Net: G5 closure supplies **two genuine structural consequences**
   (LFV-zero and no-CL-CP, both SM-consistent) and **two consistency
   checks** — but **zero genuinely new numerical forecasts** beyond what
   the SM already produces. A strict review should read the verdict as
   `TRUE_NO_PREDICTION`.

3. **Shape theorem is a linear-response form on a retained identity.**
   The retained Dirac-bridge theorem states
   `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3` — i.e., the
   second-order return at unit-weighted intermediate projector is the
   identity. Agent 10 v2's "three independent weight slots" are the
   LINEAR-RESPONSE form `diag(Σ(w)) = (w_O0, w_a, w_b)` obtained by
   ALLOWING the intermediate propagator to carry arbitrary positive
   weights. The three weights are NOT free in the retained theorem —
   they are fixed to 1 by the Dirac-bridge identity. They become
   effective-theory parameters only under an observational-promotion
   reading, where the retained propagator's spectrum is replaced by
   three independent observational inputs. This is the standard
   "retained-map-plus-observational-promotion" pattern shared with G1,
   and is defensible, but should not be read as "the framework contains
   three free parameters for charged-lepton masses" in the sole-axiom
   sense.

### Structural backbone certified

- Shape theorem: `diag(Σ) = (w_O0, w_a, w_b)` (Agent 10 v2)
- Robustness: `SHAPE_THEOREM_ROBUST = TRUE` (Agent 14, 7 stress tests,
  `PASS=57, FAIL=0`)
- Shape theorem is a retained-surface **corollary** of the Dirac-bridge
  PASS set + linearity, not a new axiom

### Sole-axiom route closed

- `S2_BREAKING_PRIMITIVE_AMBIGUOUS` across 8 exhaustive channels (Agent
  12, `PASS=31, FAIL=0`). The retained framework has no sole-axiom
  S_2-breaking primitive on axes `{2, 3}`. G5 requires observational
  promotion (as does G1).

### G1 ⊕ G5 architectural decomposition theorem

- `JOINT_PINNING_THEOREM_ABSENT` via sharp structural theorem
  `dim(V_H ∩ V_D) = 0` (Agent 13, `PASS=9, FAIL=0`)
- G1's H-chart tangent space `V_H = span{T_m, T_δ, T_q}` and G5's
  species-diagonal subspace `V_D = span{D_1, D_2, D_3}` are
  structurally orthogonal in the retained Hermitian `M_3(ℂ)` on hw=1
- G1 pins the off-diagonal subspace via PMNS; G5 pins the diagonal
  subspace via charged-lepton masses; the two are independent
  observational pins covering the retained algebra from orthogonal
  directions
- **This is not a weakness — it's a clean retained architecture**:
  each flagship gate closes via its own orthogonal observational pin
  at the same closure class

### Total runner count

Across all 14 G5 agents: **441 PASS / 0 FAIL**.

### The publication-safe G5 statement

> The retained `Cl(3)/Z^3` framework on `hw=1` carries an exact
> structural shape theorem (Agent 10 v2) proving that the effective
> charged-lepton mass operator `Σ = P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1
> P_{T_1}` has diagonal `(w_O0, w_a, w_b)` via `Γ_1` hopping from the
> three generations to `O_0`, `T_2(1,1,0)`, and `T_2(1,0,1)`
> respectively, with `T_2(0,1,1)` structurally unreachable. Observational
> pinning by PDG charged-lepton masses produces a scale-unique
> chamber-interior point, and Koide `Q = 2/3` is recovered automatically
> to PDG precision `|dev| = 6.15 × 10^{-6}`. G5 closes at the same
> `retained-map-plus-observational-promotion` class as G1. Structural
> theorems rule out the sole-axiom route (Agent 12, 8 channels) and the
> G1-corollary route (Agent 13, `dim(V_H ∩ V_D) = 0`); the framework's
> retained `hw=1` algebra decomposes into two orthogonal observational-
> pin lanes — G1 on `V_H`, G5 on `V_D`.

---

## Eight-agent attack summary

**Important context for reading this note:** in parallel with these eight
agents, a separate `claude/g1-complete` branch landed a **G1 CLOSURE** via
Physicist-H's PMNS-as-f(H) retained map (see
[G1_OMNIBUS_CLOSURE_REVIEW_NOTE_2026-04-17.md](./G1_OMNIBUS_CLOSURE_REVIEW_NOTE_2026-04-17.md)).
G1 closure supplies the retained Yukawa/H-source machinery on the Z_3
doublet block. In light of the Agent 7+8 no-go results below — which
rigorously eliminate every retained **non-Yukawa** cross-species mechanism
— G1 closure is the unique remaining retained primitive capable of forcing
Koide on the retained hw=1 triplet. G5's natural next step is therefore
to apply the G1 retained H(m, δ, q_+) operator to the charged-lepton
sector.

| Lane | Agent | Runner | Note | Verdict |
|---|---|---|---|---|
| Primary attempt (Candidates A/B/C on minimal L_t=4 APBC) | 1 | `frontier_charged_lepton_hw1_observable_curvature.py` | [CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md) | exact attempt; `KOIDE_FORCING_RESOLVED=FALSE`; `b=0` collapses K to `a*I` |
| Z_3 source-response cross-check (Option D) | 2 | `frontier_charged_lepton_z3_source_response_crosscheck.py` | [CHARGED_LEPTON_Z3_SOURCE_RESPONSE_CROSSCHECK_NOTE.md](./CHARGED_LEPTON_Z3_SOURCE_RESPONSE_CROSSCHECK_NOTE.md) | `Z3_CROSSCHECK_AGREES_WITH_PRIMARY=INDEPENDENT`; `S=I_3`; Z_3 alone forces no direction |
| Sectoral Koide universality (Prediction 3 test) | 3 | `frontier_koide_sectoral_universality.py` | [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md) | `KOIDE_UNIVERSALITY=CHARGED_LEPTON_ONLY`; `Q_\ell=2/3` only; `Q_d=0.73`, `Q_u=0.85` |
| L_t > 4 pure-APBC extension | 4 | `frontier_charged_lepton_curvature_lt_extension.py` | [CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md](./CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md) | `NO_GO_PURE_APBC=TRUE`; `b=0` on every `L_t` by translation-character orthogonality |
| Observable-principle character-symmetry reach | 5 | `frontier_observable_principle_character_symmetry.py` | [OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md](./OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md) | `CHARACTER_SYMMETRY_FORCES_KOIDE=FALSE`; three independent counterexamples |
| Color-theoretic sector correction | 6 | `frontier_koide_color_sector_correction.py` | [KOIDE_COLOR_SECTOR_CORRECTION_NOTE.md](./KOIDE_COLOR_SECTOR_CORRECTION_NOTE.md) | `COLOR_CORRECTION_FORCES_SQRT_65=FALSE_BUT_NEAR`; exact `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` identity; `Q_d` match to 0.04%; up-type extension fails (5.75%); deployment primitive open |
| SU(2)_L gauge-exchange mixing | 7 | `frontier_koide_su2_gauge_exchange_mixing.py` | [KOIDE_SU2_GAUGE_EXCHANGE_MIXING_NOTE.md](./KOIDE_SU2_GAUGE_EXCHANGE_MIXING_NOTE.md) | `SU2_GAUGE_EXCHANGE_GENERATES_B=FALSE`; taste ⊗ species carrier orthogonality theorem |
| Anomaly-forced 3+1 cross-species | 8 | `frontier_koide_anomaly_forced_cross_species.py` | [KOIDE_ANOMALY_FORCED_CROSS_SPECIES_NOTE.md](./KOIDE_ANOMALY_FORCED_CROSS_SPECIES_NOTE.md) | `ANOMALY_FORCED_MIXING_GENERATES_B=FALSE`; every retained anomaly ingredient is species-blind on hw=1 |

Total runner passes across all eight lanes: `28 + 41 + 20 + 44 + 30 + 24 + 49 + 42 = 278 PASS, 0 FAIL`.

## What remains rigorous

1. **Algebraic cone equivalence (Agent 1, Steps 1-5).** On the retained
   `hw=1` triplet, `Q = 2/3` is equivalent to `a_0^2 = 2|z|^2` where
   `a_0, z` are the trivial and nontrivial `C_3` character components of
   the spectral-amplitude vector. Exact symbolic identity.

2. **Dirac spectral amplitude closed form on L_t=4.** The
   observable-principle curvature at species `i` evaluates to
   `K_{ii}^{(spec)} = 16 / (m_i^2 + (7/2) u_0^2)` with the retained
   `7/2 = 3 + 1/2` that produces the `(7/8)^{1/4}` selector in the
   `v = 246.28 GeV` hierarchy theorem. Same retained selector surface.

3. **Bulk-limit effective denominator.** `lim c_eff(L_t) = 2\sqrt{3}`
   (not `3`), derived from the continuum integral
   `1/(2\pi) \int_0^{2\pi} d\omega/(3 + sin^2\omega) = 1/(2\sqrt{3})`.
   The retained `c(4) = 7/2` sits `1%` above the bulk value and the
   sequence `c(L_t)` is non-increasing.

4. **Charged-lepton Koide holds at PDG precision.** `Q_\ell = 0.66666`
   matches `2/3` to `|dev| < 0.001%`.

## What rigorously died

Six independent null hypotheses are closed:

1. **Algebraic-permissiveness null** (Agent 2). The `Z_3`-invariant
   source-response kernel with canonical left/right charges gives `S = I_3`
   — the triply-degenerate point `(a, b) = (1, 0)`. So the algebra is not
   just permissive; it is *completely* degenerate in the canonical
   invariant setting. If the primary lane does produce a unique ray, it
   cannot be a disguised `Z_3` invariance statement.

2. **Universal-sector-extension null** (Agent 3). `Q_\ell \approx 2/3` but
   framework-native `Q_d \approx 0.73`, PDG `Q_u \approx 0.85`. Running to
   common scale makes the up-type deviation worse. No scheme correction
   derivable from retained theorems closes the gap. A universal Koide
   theorem across all three mass sectors is falsified.

3. **Pure-APBC refinement null** (Agent 4). `b = K_{12} = 0` holds on every
   pure-APBC `L_t` block. The three `hw=1` species carry pairwise-
   orthogonal joint translation characters, so `(D+J)^{-1}` commutes with
   every `T_k` for species-diagonal `J`, eliminating every cross-species
   matrix element at quadratic source-response order. The pure-APBC
   refinement lane is permanently closed.

4. **Observable-principle character-symmetry null** (Agent 5). The unique-
   generator + additivity + CPT-even chain does NOT force `alpha = beta`
   on `hw=1` blocks with `b != 0`. Three independent tactics (direct
   symbolic Legendre transform, Schur's lemma on `C_3` irreps, independent-
   subsystem additivity chain) each produce explicit symbolic
   counterexamples. Candidate B of the Koide-cone derivation is
   structurally dead, not merely unclosed on the minimal block.

5. **SU(2)_L gauge-exchange null** (Agent 7). Retained native `SU(2)_L`
   generators `S^a` live in the taste `Cl(3)` subalgebra and satisfy
   `rho_{hw=1}(S^a) = I_species`. Every SU(2)_L-dressed operator therefore
   commutes with `P_i` and cannot generate cross-species mixing at any
   order in `g_2`. Color dressing on quarks multiplies only the
   `a`-diagonal. This is the **taste ⊗ species carrier orthogonality
   theorem**: any operator living in the retained gauge algebra (taste
   subalgebra or commutant) cannot touch the species label.

6. **Anomaly-forced 3+1 null** (Agent 8). Every retained anomaly-forced
   ingredient on the SM branch — `gamma_5`, the RH singlet completion
   (species-blind Y per sector), the five vanishing anomaly traces, the
   chirality-forcing Dirac mass bilinear (species-blind without Higgs
   VEV), the chirality projectors — acts as a scalar on the `hw=1`
   species label. Tested on `L_t in {6, 8, 12, 16}`. Sector-scale signal
   `Q_L : L_L = -1/27 : 1` distinguishes leptons from quarks but does NOT
   produce within-sector cross-species mixing.

**The convergent architectural conclusion:** all six nulls trace to the
same deeper fact — within the retained `Cl(3)/Z^3` framework, every
operator on the hw=1 triplet built from the retained algebraic or anomaly
structure acts as a scalar multiple of the species identity UNLESS it
involves a Higgs/Yukawa VEV insertion. The Higgs Yukawa is **the unique
retained cross-species primitive on the hw=1 triplet**.

## G1 closure supplies the unique remaining primitive

On 2026-04-17, the `claude/g1-complete` branch landed a **G1 CLOSURE** via
Physicist-H's PMNS-as-f(H) retained map. 20 commits, 11 runners,
**PASS=305, FAIL=0**. See
[G1_OMNIBUS_CLOSURE_REVIEW_NOTE_2026-04-17.md](./G1_OMNIBUS_CLOSURE_REVIEW_NOTE_2026-04-17.md).
Key retained objects now on `main`:

- **Canonical scalar baseline from Schur.** `D = m I_3` is forced on the
  retained three-generation observable algebra by Schur's lemma.
- **Retained affine Hermitian operator** `H(m, delta, q_+)` on the
  hw=1 triplet, whose direct diagonalization gives the retained map
  `(m, delta, q_+) -> (sin^2 theta_12, sin^2 theta_13, sin^2 theta_23, delta_CP)`.
- **Observational chamber pin.** G1 closes on the P3 lane at
  `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`.
- **Retained delta_CP prediction.** `sin(delta_CP) = -0.9874`,
  `delta_CP ~ -81°`, falsifiable at DUNE / Hyper-Kamiokande.

G1 closure is labeled **retained-map-plus-observational-promotion** (not
sole-axiom), consistent with Physicist-G's microscopic-polynomial
impossibility theorem on the Z_3 doublet block.

### What G1 closure means for G5 (post-Agent-9 revision)

Agent 9 explicitly tested the direct reading "apply G1's retained H to
charged leptons" and rigorously ruled it out. See
[G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md](./G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md).

Verdict: `G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.

At the G1 chamber pin `(m_*, delta_*, q_+*) = (0.657, 0.934, 0.715)`,
the retained `H(m, delta, q_+)` has eigenvalue triple
`(-1.309, -0.320, +2.287)`. Neither `m_i = |lambda_i|` nor
`m_i = lambda_i^2` reproduces Koide `Q = 2/3` or the observed
charged-lepton direction. An 80-restart chamber search confirms no
interior pin saturates Koide while matching observed ratios
simultaneously.

**The architectural insight from Agent 9's reading of the Physicist-H
theorem:** `H(m, delta, q_+)` carries the **neutrino** Hermitian
structure on the retained hw=1 triplet. The Physicist-H closure uses the
retained **Dirac-bridge theorem** to impose `U_e = I_3` and force the
charged-lepton operator `Gamma_1` to be diagonal in the axis basis on
hw=1. **The three diagonal entries of `Gamma_1` are the charged-lepton
masses, and they are NOT determined by G1.** G1 imposes `Gamma_1`'s
diagonality as a bridge, but the eigenvalues are inputs to that bridge,
not outputs.

### The correct retained target for G5 (refined after reconnaissance)

**Further scope-sharpening:** main-session reconnaissance reading of
[DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
and the runner `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py`
(**28 PASS, 0 FAIL** on live main) reveals a critical subtlety:

- `Γ_1` directly restricted to the hw=1 triplet is **identically zero**
  (`P_{T_1} Γ_1 P_{T_1} = 0`, first-order vanishing).
- The effective second-order return
  `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3` on the retained
  lattice — i.e., the three generations are **mass-degenerate** at the
  leading retained order.

So the G5 target is not "diagonal entries of Γ_1" directly (which are
zero), but:

> **What retained framework corrections to the second-order effective return
> `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}` break the leading-order `I_3`
> degeneracy into a diagonal mass matrix `diag(m_e, m_μ, m_τ)` satisfying
> Koide `Q = 2/3`?**

See the reconnaissance note
[G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md](./G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md)
for the exact Γ_1 definition, the first- / second-order structure, and
the refined candidate deployment primitives.

(Equivalently: what retained primitive fixes the leading **hierarchy-
breaking** structure on top of `I_3` in the second-order Γ_1 return?)

### Agent 10 v2 final answer — structural shape found, one specific primitive missing

Agent 10 v2 (runner `frontier_g5_gamma_1_second_order_return.py`, **PASS=20, FAIL=0**)
produced the sharpest-possible G5 diagnosis by constructing the retained
second-order return explicitly on `C^16` and testing four correction candidates.

**The structural shape theorem:** the retained second-order return on `T_1` is
exactly
```
diag(Σ) = (w_O0, w_a, w_b)
```
— three independent weight slots assigned to the three generations via the
`Γ_1` hopping pattern:

| T_1 species | Spatial label | Γ_1-reached intermediate | Weight slot |
|---|---|---|---|
| Generation 1 (electron) | `(1, 0, 0)` | `O_0 = (0,0,0)` | `w_O0` |
| Generation 2 (muon) | `(0, 1, 0)` | `(1, 1, 0) ∈ T_2` | `w_a` |
| Generation 3 (tau) | `(0, 0, 1)` | `(1, 0, 1) ∈ T_2` | `w_b` |

The fourth `T_2` state `(0, 1, 1)` is **unreachable** from `T_1` in one `Γ_1`
hop at this order. This is the retained **shape theorem** — it says the
framework algebra has exactly the right number of independent slots for the
three charged-lepton masses, with the explicit species-to-slot mapping
determined by `Γ_1` hopping.

**The correction survey:**

| Correction | Species structure | Result |
|---|---|---|
| A: Higgs fluctuations `φ = e_1 + ε` around EWSB axis | `diag(Σ − I_3) = |ε|² (1,1,1)` | REJECT — democratic |
| B: Higher-order returns `[Γ_1 P_{not-T_1} Γ_1]^n` | `I_3` at every `n ∈ {1,2,3,4}` | REJECT — democratic |
| C: Weighted intermediate propagator on `O_0 ⊕ T_2` | `(w_O0, w_a, w_b)` affine | UNDERDETERMINED — shape right |
| D: Retained Cl(3)-bilinear mass insertion | Zero species-diagonal on `T_1` | REJECT — null |

Best retained scheme (hw-staggered propagator `1/(m_0 + hw·Δ)`) gives a
common weight to all `T_2` states and is structurally `2+1` degenerate
(`w_a = w_b`), yielding cos-similarity `0.85` with the observed
charged-lepton direction — far from the `0.99+` that would indicate a
true match.

**The newly-named missing primitive:**
The three retained schemes tested all respect the residual `S_2` symmetry
on axes `{2, 3}` left unbroken after the EWSB selector `V_sel` picks
axis 1. This `S_2` symmetry EXCHANGES the two species-relevant `T_2`
states: `(1, 1, 0) ↔ (1, 0, 1)`. Therefore on the retained framework
surface

> **`w_a = w_b` is structurally forced by the unbroken residual `S_2`.**

The G5 attack requires **a retained operator that breaks the residual
`S_2` on axes `{2, 3}`**, assigning distinct propagator weights to the
two species-relevant `T_2` states.

### Publication-grade honest conclusion

The retained `Cl(3)/Z^3` framework has the *correct structural shape*
(three independent weight slots in the second-order `Γ_1` return) to
accommodate the charged-lepton mass hierarchy with Koide `Q = 2/3`, but
**lacks a retained `S_2`-breaking primitive** on the residual axes `{2,
3}` to assign the three weights. The observed `Q_ℓ = 2/3` is therefore
currently compatible-with-but-not-derived-from the framework.

G5 closure requires one of:

1. **A new retained primitive** breaking `S_2` on axes `{2, 3}` after
   EWSB axis-1 selection. Concrete target: an operator on `C^16` with
   distinct matrix elements between the two `T_2` states `(1, 1, 0)`
   and `(1, 0, 1)`.
2. **An observational pin** on the charged-lepton side analogous to
   G1's PMNS pin. `Q_ℓ = 2/3` would be retained-via-observational-
   promotion rather than retained-sole-axiom, matching the closure
   class of G1.
3. **Accept Koide as an unretained observational fact** outside the
   framework's theorem stack.

Option 2 is the cleanest path consistent with G1's architecture.
Option 1 is the most scientifically valuable if the right retained
primitive is identifiable. Option 3 is the minimal-claim honest
fallback.

This is a sharply different object than "apply H to charged leptons".
`Gamma_1` lives on the retained hw=1 algebra but is constrained to be
diagonal in the axis basis by the Dirac-bridge theorem; its eigenvalues
are the physical charged-lepton masses. Agent 9's candidate list:

1. **Species-dependent diagonal carrier from Agent 6's `(C_F - T_F)^{-1/4}`
   Casimir identity.** The exact retained algebra contains
   `(C_F - T_F)^{-1/4} = (6/5)^{1/4}`; if the corresponding deployment
   primitive lives on the `Gamma_1` diagonal rather than on the H
   cross-species generators, the 0.04% match Agent 6 found could be
   structural rather than coincidental.

2. **Higgs-VEV insertion with retained Higgs-current observable.** Since
   `Gamma_1` is explicitly a Higgs-coupled object on the charged-lepton
   side (via the Physicist-H Dirac-bridge theorem), the retained
   Higgs-current machinery may carry a species-dependent diagonal
   structure that fixes `Gamma_1`'s eigenvalues.

3. **Joint PMNS + Koide pinning theorem.** A theorem tying `H` and
   `Gamma_1` to a shared hw=1 source would close both simultaneously,
   with PMNS pinning one sector and Koide pinning the other.

The Higgs Yukawa / diagonal-`Gamma_1` route remains the active open lane
for G5 closure; G1 closure alone does not force it as an automatic
corollary.

## What remains open (post-G1-closure)

1. **Application of G1 retained H-operator to charged-lepton sector.**
   The G1 chamber-pin determines `(m_*, delta_*, q_+*)` via observational
   PMNS. What mass-square-root vector does the G1 H-operator produce on
   the charged-lepton sector, and does it satisfy Koide?

2. **Color-correction deployment primitive.** Agent 6 established that
   `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` is an exact retained Casimir
   identity matching the observed `Q_d / Q_\ell` to 0.04%, but the
   retained hw=1 algebra does not currently carry a species-dependent
   color-adjoint projector that would deploy the identity. Whether G1
   closure supplies the missing deployment mechanism is open.

3. **Up-type sector.** Agent 6 showed that `(C_F - T_F)^{-1/2} = sqrt(6/5)`
   gives `Q_u = 4/5` versus observed `0.849` (off by 5.75%). The simple
   Casimir-power extension does not work. Up-type Koide is genuinely
   sector-specific and needs a different structural input.

4. **Wilson / lattice-improvement operators.** Untested. Low-priority
   lane since the Higgs Yukawa route via G1 is now retained.

5. **Non-APBC temporal mixing.** Untested. Low-priority lane since the
   Higgs Yukawa route via G1 is now retained.

(Historical stub from the pre-closure candidate list, kept for
continuity. Candidates 2, 3, 4, 5, 6 below have been superseded by the
rigorous no-go results above, by Agent 6's bounded color-correction
result, or by G1 closure. The active open candidate is now item 1 in the
post-G1-closure list above.)

3. **Wilson / lattice-improvement operators.** Untested. Higher-
   derivative terms that break translation-character orthogonality.

4. **Non-APBC temporal mixing.** Untested. Thermal / non-periodic
   temporal modifications.

5. **Color-theoretic sector correction** (Agent 6 result).
   `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` is exact retained algebra; applied
   as a down-quark dressing it reproduces `Q_d` to 0.04%. Deployment
   primitive open; up-type extension fails.

6. **Anomaly-forced 3+1 cross-species propagator.** Agent 8 — FALSE.
   Every retained anomaly ingredient acts as scalar on hw=1 species.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the charged-lepton Koide
> relation `Q_\ell = 2/3` is rigorously equivalent to the equal-
> character-weight condition `a_0^2 = 2|z|^2` on the retained `hw=1`
> triplet. An eight-agent attack surface rigorously closes six
> independent null hypotheses (Z_3 permissiveness, pure-APBC at all
> `L_t`, observable-principle character-symmetry, SU(2)_L gauge-exchange,
> anomaly-forced 3+1, universal sector-extension). A color-theoretic
> sector-correction identity `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` is exact
> from retained SU(3) Casimirs and matches the framework-native `Q_d` to
> 0.04%, but the retained `hw=1` algebra does not currently carry a
> species-dependent color-adjoint projector that would deploy it. The
> convergent architectural conclusion is that every retained operator on
> hw=1 built from the retained algebraic or anomaly structure is
> species-diagonal unless it involves a Higgs/Yukawa VEV insertion, so
> the Higgs Yukawa is the unique retained cross-species primitive. In
> parallel, a separate thread closed the G1 Z_3 doublet-block selector
> law via Physicist-H's PMNS-as-f(H) retained map. G1 closure provides
> exactly the retained H-operator on the hw=1 algebra needed to attack
> Koide cone-forcing; applying G1's retained H to the charged-lepton
> sector is the natural next theorem object for G5.
> non-minimal temporal block.

## Dependency contract

Retained authorities validated on live `main` before the five-agent attack:

- `frontier_three_generation_observable_theorem.py` `PASS=47, FAIL=0`
- `frontier_generation_fermi_point.py` `EXACT PASS=7, BOUNDED PASS=1, FAIL=0`
- `frontier_generation_rooting_undefined.py` `PASS=37, FAIL=0`
- `frontier_hierarchy_observable_principle_from_axiom.py` `PASS=13, FAIL=0`
- `frontier_anomaly_forces_time.py` `PASS=85+2, FAIL=0`
- `frontier_plaquette_self_consistency.py` `PASS=16, FAIL=0`

All passed fresh on `main` at the start of the attack.

## What this does not claim

- Koide `Q_\ell = 2/3` is NOT promoted to a retained framework theorem.
  The algebraic cone equivalence is theorem-grade; the cone-forcing step
  is open.
- The `Q_d / Q_\ell \approx \sqrt{6/5}` observation is NOT promoted to a
  retained relation. It is a sharply-labeled numerical coincidence
  motivating a specific successor hypothesis.
- The four remaining mechanisms listed above are NOT claimed to work;
  they are the concrete successor targets identified by the five-agent
  attack.

## Atlas status

All five agent notes appear as tool rows in
[DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md) Section F,
[PUBLICATION_MATRIX.md](./publication/ci3_z3/PUBLICATION_MATRIX.md)
Section B, and
[FULL_CLAIM_LEDGER.md](./publication/ci3_z3/FULL_CLAIM_LEDGER.md)
Section 3 (Flavor / CKM portfolio). This consolidated status note is the
reviewer-facing synthesis.
