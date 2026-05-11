# Lane 2 Probe X-S4b-Combined — Combined Higgs Structural + EWSB + G2 Born-as-Source (probeX_S4b_combined)

**Date:** 2026-05-08 (compute date 2026-05-10)
**Type:** bounded_theorem (combined-content stress test of S4b-op closure hypothesis)
**Claim type:** bounded_theorem
**Scope:** bounded source note. Tests whether the combination of three
cited ingredients —
  (i)  Higgs structural ratio `m_H/v = 1/(2 u_0)`
       ([HIGGS_MASS_FROM_AXIOM_NOTE.md](HIGGS_MASS_FROM_AXIOM_NOTE.md) Step 4)
  (ii) EWSB Wilson chain `v_EW = M_Pl · (7/8)^{1/4} · α_LM¹⁶ = 246.28 GeV`
       ([COMPLETE_PREDICTION_CHAIN_2026_04_15.md](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) §3.2)
  (iii) G2 Born-as-source position-density trace
        `Tr(ρ̂ · M̂(x))` with `M̂(x) = |x⟩⟨x|`
        ([G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md))
— jointly select the post-EWSB Higgs-mass operator `Ô_{m_H²}` and
thereby close S4b-op (operator-construction sub-piece of Lane 2 step
S4b). Earlier probe W-S4b-EWSB found that
EWSB content alone selects only the LOCATION (φ* = v_EW), not the
CURVATURE. This probe attacks the joint hypothesis that combining the
structural ratio + EWSB location + G2 source-coupling rule fixes
all three quantities (location, structural ratio, source coupling)
simultaneously.
**Status:** bounded - combined stress test, not closure.
The combination yields the SAME numerical prediction as any single
piece evaluated alone (`m_H = v_EW/(2 u_0) = 140.31 GeV`, +12.0% gap
vs PDG `125.25 GeV`), with no shift attributable to combining all
three. The +12% gap is the load-bearing residual S4b-op ∧ S7 that
none of the three cited ingredients can close, and combining them
does not add new content beyond the symmetric-point identification
(component (i)) re-evaluated at the cited `v_EW` location
(component (ii)) under the canonical position-density Born trace
(component (iii)).
**Loop:** probe-x-s4b-combined-higgs-ewsb-g2-20260508-probeX_S4b_combined
**Primary runner:** [`scripts/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.py`](../scripts/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.py)
**Cache:** [`logs/runner-cache/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.txt`](../logs/runner-cache/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.txt)

## 0. Question

Earlier probes on Lane 2 step S4b have ruled out closure from any
single cited ingredient:
- **W-S4b-EWSB** (worktree probe): EWSB content (Wilson `v_EW`,
  `<H>` direction, `Q = T_3 + Y/2`) selects the EVALUATION-POINT
  LOCATION (φ* = v_EW) but not the CURVATURE; the lattice
  taste-sector potential `V_taste(m) = -(N_taste/2)·log(m² + 4u_0²)`
  has no minimum at finite m, and `V''_taste(v/M_Pl) = V''_taste(0)`
  to relative precision `10⁻³⁴`. Verdict: SHARPENED, not closed.
- **G2 Born-as-source**
  ([gnewtonG2](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)):
  the unified position-density map `Tr(ρ̂ · M̂(x))` is canonical for
  pure and mixed states, but the source-coupling derivation (why
  gravity must use this readout) remains open. Verdict: bounded,
  not closure of the source-coupling admission.
- **Tree-level structural shortcut**
  ([HIGGS_MASS_FROM_AXIOM Step 5(b)](HIGGS_MASS_FROM_AXIOM_NOTE.md)):
  the relation `m_H/v = 1/(2 u_0)` is the symmetric-point
  identification itself (per-channel curvature `(4/u_0²)/N_taste`
  identified with `(m_H/v)²`), giving `m_H_tree = 140.3 GeV` (+12%
  gap to PDG 125.25). Verdict: tree-level shortcut, +12% gap as the
  load-bearing residual.

The originating brief proposes:

> Each piece individually was bounded. Combining ALL THREE — Higgs
> structural ratio (`m_H/v = 1/(2 u_0)`) WITH EWSB location (`v_EW`)
> WITH G2 Born-as-source (curvature from source-coupling) — might
> select the operator differently than any single piece alone.
> Curvature at vacuum requires both location AND a structural ratio
> AND a source-coupling rule; combining these three cited
> ingredients might fix all three quantities simultaneously.
>
> Tier: positive theorem if combination closes S4b-op with
> prediction matching PDG `m_H` within ~5%; bounded if partial
> closure; negative if combination still cannot fix the operator.

**Question:** Does the combination of (i) `m_H/v = 1/(2 u_0)`,
(ii) `v_EW`, (iii) G2 Born-trace simultaneously fix `(location,
ratio, source coupling)` to close S4b-op as a positive theorem?

## 1. Answer

**BOUNDED, NOT CLOSED.** The combination does not improve on any
single ingredient. The joint hypothesis instantiated on cited
content gives:

```
   m_H(combined) = v_EW · (1/(2 u_0)) = 246.28 / (2 · 0.8776) = 140.31 GeV
   PDG comparator: m_H = 125.25 GeV
   Relative gap:    +12.03%
```

This is **identical** to the tree-level mean-field prediction
([HIGGS_MASS_FROM_AXIOM_NOTE.md](HIGGS_MASS_FROM_AXIOM_NOTE.md)
Step 4) and to the W-S4b-EWSB partial-closure prediction. The
combination does NOT match PDG within the 5% tier-1 threshold; it
does not match within ~10% either. The +12.03% gap is the
load-bearing S7 12% gap-closure functional Δ², which is open per
[HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md).

The structural reasons the combination fails to close S4b-op:

- **(K1) Curvature ingredient (i) IS the symmetric-point
  identification.** Per HIGGS_MASS_FROM_AXIOM Step 5(b),
  `(m_H_tree/v)² = curvature/N_taste = 1/(4 u_0²)` is derived BY
  identifying the symmetric-point lattice curvature
  `|V''_taste(0)|/N_taste` with `(m_H/v)²`. The structural relation
  `m_H/v = 1/(2 u_0)` therefore IS the per-channel symmetric-point
  curvature divided by `N_taste`, square-rooted. It is not
  independent post-EWSB content; reusing it at the `v_EW` location
  gives the SAME number as evaluating it at `m = 0`.

- **(K2) Location ingredient (ii) gives v_EW but not curvature.**
  The hierarchy theorem retains `v_EW = 246.28 GeV` as a derivation
  from the framework axioms + computed plaquette + APBC correction.
  This bounds where the post-EWSB minimum sits, but does not derive
  what the curvature is at that minimum: the SM Higgs potential FORM
  `V = -μ²H†H + λ(H†H)²` is admitted SM convention per
  [EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02 §5](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md),
  not derived. So setting `φ = v_EW` does not specify a curvature.

- **(K3) Source-coupling ingredient (iii) is bounded support, not
  derivation.** The G2 Born-as-source theorem
  ([gnewtonG2](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md))
  establishes that the unified map `Tr(ρ̂ · M̂(x))` is canonical for
  both pure and mixed states. It explicitly does NOT close the
  source-coupling admission: "the gravitational source-coupling
  derivation remains open." Applying this map to the curvature
  observable evaluates `Tr(ρ̂_vac · ∂²V/∂φ²|_{v_EW})`, but the
  curvature operator construction at `v_EW` is precisely S4b-op,
  the open piece.

- **(K4) Combined evaluation collapses to the symmetric-point
  identification.** Substituting (i) into the combination at
  location (ii) under trace (iii):
  ```
   Tr(ρ̂_vac · Ô_{m_H²}|_{v_EW}) = Tr(ρ̂_vac) · m_H²|_{(i)} · ⟨v_EW²/v²⟩
                                = 1 · (v_EW/(2 u_0))² · 1
                                = m_H_tree²
                                = (140.31 GeV)²
  ```
  The trace acts identically (Tr ρ̂ = 1 for a normalized state); the
  location appears via `v_EW`; the ratio (i) provides
  `m_H = v_EW/(2 u_0)`. These three multiply to give
  `m_H_tree = 140.31 GeV` — exactly the prior tree-level shortcut.
  No combination interaction shifts the value.

- **(K5) The +12% gap survives the combination.** The combined
  prediction `m_H(combined) = 140.31 GeV` deviates from PDG
  `125.25 GeV` by `+12.03%`. The 12.03% gap is by construction the
  S7 gap-closure functional residual
  ([higgsS7](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md));
  it is structurally NOT addressable by combining components (i),
  (ii), (iii), each of which inherits the symmetric-point
  identification.

**Conclusion.** S4b-op cannot be closed by combining the three named
cited ingredients. The combination is at best a multiplicative
recombination of the same symmetric-point identification, and yields
the same `m_H_tree = 140.31 GeV` as any single ingredient. This is
**bounded** (not negative): it ratifies S4b-loc's bounded support
(component (ii) does fix the location), but exposes that S4b-op's
curvature operator construction is structurally orthogonal to all
three cited pieces — the SM Higgs potential FORM remains the
admitted SM convention, and no combination of admitted/cited
content turns it into a derivation.

## 2. Setup

### Premises (this note's bounded-support lemma)

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| Plaq-MC | `<P>_iso(β=6) = 0.5934`; `u_0 = <P>^{1/4} = 0.8776` | [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) §3.1 |
| Hier | `v_EW = M_Pl · (7/8)^{1/4} · α_LM¹⁶ = 246.28 GeV` (hierarchy theorem in cited chain) | [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) §3.2 |
| AlphaLM | `α_LM = α_bare / u_0` with `α_bare = 1/(4π)` (g_bare = 1 admitted) | same source, §3 |
| TasteV | `V_taste(m) = -(N_taste/2) · log(m² + 4 u_0²)`, `N_taste = 16` | [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) Step 2-3 |
| HiggsRatio | `m_H/v = 1/(2 u_0)` derived in HIGGS_MASS_FROM_AXIOM Step 4 (but per Step 5(b) IS the symmetric-point identification) | [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) |
| EWSB-Q | `Q = T_3 + Y/2` from `<H> = (0, v/√2)^T` + Y_H = +1 (exact-support theorem) | [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) |
| EWSB-PotForm | "The Higgs potential `V(H†H) = -μ²H†H + λ(H†H)²` form (admitted SM convention)" | same source, §5 |
| G2-Born | Unified position-density Born map `Tr(ρ̂ · M̂(x))`; bounded support; source-coupling admission still open | [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| HiggsAuth | "VEV magnitude (admitted external observable)... W/Z mass formulas (require Higgs kinetic term + EW mixing angle)" | [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) §5 |
| PDG-Higgs | `m_H = 125.25 GeV` (falsifiability comparator only, never derivation input) | PDG 2024 |

### Forbidden imports

- NO PDG observed values used as derivation input (only as falsifiability comparators).
- NO new repo-wide axioms.
- NO source text promotes unaudited content.
- NO empirical fits.
- NO same-surface family arguments.
- NO new physics inputs beyond cited baseline + cited content + standard QM expectation-value formalism.

## 3. Theorem (combined-ingredient bounded support; S4b-op remains open)

**Theorem (X-S4b-Combined, bounded; combined hypothesis stress test).**

Under the premises of §2 with no new imports, the joint instantiation
of (i) `m_H/v = 1/(2 u_0)`, (ii) `v_EW = 246.28 GeV`, and (iii) G2
position-density Born trace `Tr(ρ̂ · M̂(x))` produces the same
prediction as any single ingredient evaluated alone. Specifically:

- **(K1.1) Combined-ingredient evaluation.** Substituting components
  (i)-(iii) into the brief's joint hypothesis equation gives:
  ```
   m_H(combined)² ≡ Tr(ρ̂_vac · Ô_{m_H²}|_{v_EW})
                  = 1 · (v_EW · (1/(2 u_0)))² · 1
                  = (v_EW/(2 u_0))²
                  = (140.31 GeV)²
  ```
  Numerically, `m_H(combined) = 140.31 GeV`. PDG comparator
  `m_H = 125.25 GeV`. Relative gap: `+12.03%`.

- **(K1.2) The combination collapses to the symmetric-point
  identification.** Component (i) `m_H/v = 1/(2 u_0)` IS the
  per-channel symmetric-point curvature `(4/u_0²)/N_taste = 1/(4u_0²)`
  identified with `(m_H/v)²`, square-rooted (HIGGS_MASS_FROM_AXIOM
  Step 5(b)). Multiplying by `v_EW` recovers `m_H_tree =
  v_EW/(2u_0) = 140.31 GeV`. The G2 trace contributes a unit factor
  (Tr ρ̂_vac = 1 for normalized states). No interaction term
  emerges from combining the three pieces.

- **(K1.3) Lattice taste-sector curvature at v_EW remains
  symmetric-point curvature.** Per the prior W-S4b-EWSB probe
  finding (replicated here), the lattice taste-sector curvature
  evaluated at `m̂ = v_EW/M_Pl ≈ 2 × 10⁻¹⁷` agrees with the
  symmetric-point value `V''_taste(0) = -4/u_0²` to relative
  precision better than `10⁻³⁴`. Combining (i) with (ii) and (iii)
  does NOT shift this curvature; it inherits it.

- **(K1.4) G2 Born trace adds a unit factor under canonical
  normalization.** For a normalized vacuum state `ρ̂_vac` (`Tr ρ̂ = 1`)
  and an operator `Ô = m_H² · 𝟙_v² × M̂(v_EW)` localized at the
  vacuum location, the G2 trace evaluates to
  `Tr(ρ̂_vac · Ô) = m_H² · 𝟙_v² · ρ̂_vac(v_EW)`, with
  `ρ̂_vac(v_EW)` the position-density at the vacuum. Under
  normalization `∫ ρ̂_vac(x) dx = 1` and a delta-localized vacuum
  state, `ρ̂_vac(v_EW) = δ(v_EW - v_EW) = 1` (in dimensionless
  evaluation). The trace contributes a unit multiplicative factor
  with no curvature-shifting structure.

- **(K1.5) +12% gap survives the combination.** The combined
  prediction `140.31 GeV` deviates from PDG `125.25 GeV` by
  `+12.03%`. This is the SAME gap as the tree-level mean-field
  shortcut and the W-S4b-EWSB probe. No tier-1 closure (≤5%) and no
  bounded improvement (≤10%) is achieved by combining the three
  pieces. The gap is the load-bearing S7 residual Δ², open per
  [higgsS7](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md).

- **(K1.6) S4b-op remains structurally orthogonal to (i)-(iii).**
  S4b-op is the construction of `Ô_{m_H²} = ∂²V_phys/∂φ²|_{φ = v_EW}`
  on the post-EWSB physical Hilbert space. None of the cited
  ingredients constructs this operator:
  - (i) re-uses the symmetric-point curvature divided by `N_taste`.
  - (ii) bounds the evaluation-point location only.
  - (iii) defines a Born trace canonical for pure and mixed
    states but does not derive the source-coupling rule.
  The SM Higgs potential FORM `V = -μ²H†H + λ(H†H)²` remains
  admitted SM convention per EWSB-PotForm. Combining admitted/
  cited content does not turn admitted content into derivation.

- **(K1.7) Sister-prediction asymmetry preserved.** The cited
  sister predictions on the same hierarchy chain (`v_EW` +0.03%,
  `α_s(M_Z)` +0.14%, `1/α_EM(M_Z)` -0.22%, `m_t(pole, 2L)` -0.07%)
  achieve sub-percent precision. The Higgs combined prediction is
  `+12.03%` — two orders of magnitude worse. The structural
  obstruction is in S4 (symmetric-point identification) and S7
  (gap-closure functional), not in the cited chain.

## 4. Proof sketch

### K1.1 Combined-ingredient evaluation

The brief proposes the joint hypothesis equation:
```
m_H² ≡ Tr(ρ̂_vac · Ô_{m_H²}|_{v_EW})
```
with each component instantiated from cited content:
- Location: `φ* = v_EW` (component (ii))
- Structural: `m_H/v = 1/(2 u_0)` (component (i))
- Source coupling: `Tr(ρ̂ · M̂(x))` (component (iii))

Numerical substitution:
```
v_EW = M_Pl · (7/8)^{1/4} · α_LM^{16}
     = 1.221 × 10^{19} · 0.9680 · (0.09066)^{16}
     ≈ 246.28 GeV    (cross-check: PDG 246.22, +0.03%)

u_0 = (0.5934)^{1/4} = 0.8776

m_H(combined) = v_EW / (2 u_0) = 246.28 / 1.7552 = 140.31 GeV
```

The runner computes this from cited cited inputs (no PDG used as
derivation input). Cross-check vs PDG `m_H = 125.25 GeV` shows
`+12.03%` relative gap.

### K1.2 Combination collapse to symmetric-point identification

Per HIGGS_MASS_FROM_AXIOM Step 5(b): the relation `m_H/v = 1/(2u_0)`
is derived by *identifying* the per-channel symmetric-point lattice
curvature
```
|V''_taste(0)|/N_taste = (4/u_0²)/16 = 1/(4u_0²)
```
with `(m_H/v)²`. So component (i) IS the symmetric-point
identification, square-rooted. Multiplying by component (ii) `v_EW`
recovers `m_H_tree = v_EW/(2u_0)`. Component (iii) G2 trace
evaluates `Tr(ρ̂_vac · 𝟙) = 1` for normalized vacuum states, hence
contributes no curvature shift.

The combined prediction is therefore:
```
m_H(combined) = 1 · v_EW · (1/(2u_0)) = v_EW/(2u_0) = m_H_tree
```
identical to the tree-level prediction. No interaction term from
combining the three pieces.

### K1.3 Lattice curvature at v_EW unchanged

The cited taste-sector formula:
```
V_taste(m) = -(N_taste/2) · log(m² + 4u_0²)
V''_taste(m) = -N_taste · (|λ|² - m²) / (m² + |λ|²)²
            with |λ|² = 4u_0²
```
At `m̂ = v_EW/M_Pl ≈ 2 × 10⁻¹⁷`,
```
V''_taste(m̂)/V''_taste(0) = (1 - (m̂/|λ|)²) / (1 + (m̂/|λ|)²)²
                          ≈ 1 - 3(m̂/|λ|)² + O((m̂/|λ|)⁴)
                          ≈ 1 - 3 · (v_EW/M_Pl)²/(4u_0²)
                          ≈ 1 - 1.32 × 10⁻³⁴
```
Re-evaluating the lattice curvature at `v_EW` does not switch sign;
it agrees with the symmetric-point value to relative precision
better than `10⁻³⁴`. The runner verifies this numerically.

### K1.4 G2 Born trace contributes unit factor

For a normalized vacuum state `ρ̂_vac` (Tr ρ̂ = 1) and an operator
of the form `Ô = c · 𝟙` (a c-number times identity), the G2 Born
trace evaluates to:
```
Tr(ρ̂_vac · Ô) = c · Tr(ρ̂_vac) = c · 1 = c
```
The G2 map preserves c-number observables. For the curvature
observable (a c-number coefficient `λv²` in the SM-form interpretation),
G2 contributes the unit normalization factor only. No
curvature-shifting structure is supplied by component (iii).

### K1.5 +12% gap survives combination

Numerical comparison:
```
m_H(combined) = 140.31 GeV    [framework prediction]
m_H(PDG)      = 125.25 GeV    [falsifiability comparator]
Relative gap  = (140.31 - 125.25)/125.25 = +12.03%
```
This is the SAME gap as:
- HIGGS_MASS_FROM_AXIOM tree-level (Step 4): `m_H_tree = 140.3 GeV`, +12%.
- W-S4b-EWSB partial-closure result.
- HIGGS_MASS_HIERARCHY_CORRECTION analysis.

The 12.03% gap is the load-bearing S7 functional Δ² residual
([higgsS7](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md)),
structurally NOT addressable by recombining components inheriting
the symmetric-point identification. ∎

### K1.6 S4b-op orthogonal to (i)-(iii)

S4b-op := construct `Ô_{m_H²} = ∂²V_phys/∂φ²|_{φ = v_EW}` on the
post-EWSB physical Hilbert space.

- Component (i): `m_H/v = 1/(2u_0)` is the symmetric-point
  identification (HIGGS_MASS_FROM_AXIOM Step 5(b)). Provides a
  RATIO, not an operator at `v_EW`.
- Component (ii): `v_EW` is a NUMERICAL LOCATION. Does not specify
  the curvature at that location. The SM Higgs potential FORM `V =
  -μ²H†H + λ(H†H)²` is admitted SM convention per EWSB-PotForm.
- Component (iii): G2 Born trace is a MAP, canonical for pure and
  mixed states. Does not derive the source-coupling rule (gnewtonG2
  explicitly preserves this open admission).

Combining a ratio + a location + a map yields a number (`m_H_tree =
140.31 GeV`), not an operator. The construction `Ô_{m_H²}` requires
either (i') a derivation of the SM Higgs potential FORM from
cited content, or (ii') a derivation of post-EWSB stationary-point
curvature from the lattice partition function (per the cluster
obstruction synthesis), or (iii') a separate cited chain. None
of (i')-(iii') is supplied by combining (i)-(iii). ∎

### K1.7 Sister-prediction asymmetry preserved

Retained predictions on the same hierarchy chain (from
[COMPLETE_PREDICTION_CHAIN_2026_04_15](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)):

| Quantity | Predicted | PDG | Deviation |
|---|---|---|---|
| `v_EW` | 246.28 | 246.22 | +0.03% |
| `α_s(M_Z)` | 0.1181 | 0.1179 | +0.14% |
| `1/α_EM(M_Z)` | 127.67 | 127.95 | -0.22% |
| `m_t(pole, 2L)` | 172.57 | 172.69 | -0.07% |
| **`m_H(combined)`** | **140.31** | **125.25** | **+12.03%** |

The Higgs prediction is roughly 100× worse than sister predictions.
The combination does NOT close this asymmetry. The structural
obstruction is in S4 ∧ S7, not in the cited chain itself
(which delivers `v_EW` to +0.03%).

## 5. Consistency with cited content

### C1 Parent T-S4H decomposition (S4 ≡ S4a ∧ S4b)

The parent T-S4H probe established `S4 ≡ S4a ∧ S4b`, with S4a
(operational form `m_H² = Tr(ρ̂_phys · Ô_{m_H²})`) bounded-supported
via the G2 Born-trace template, and S4b (state-and-operator
selection) open. This note tests the combined-ingredient hypothesis
at the S4b layer; the verdict (combination still bounded) is fully
consistent with the parent T-S4H S4b-open finding.

### C2 W-S4b-EWSB sub-decomposition (S4b ≡ S4b-loc ∧ S4b-op)

The earlier W-S4b-EWSB probe sub-decomposed
`S4b ≡ S4b-loc ∧ S4b-op`, with S4b-loc bounded-supported via
cited `v_EW` and S4b-op open. This note ratifies the
sub-decomposition (component (ii) supplies S4b-loc) and confirms
S4b-op remains open under the combination of all three cited
ingredients (K1.6).

### C3 G2 Born-as-source bounded support (gnewtonG2)

The G2 Born-as-source probe established the unified position-density
map `Tr(ρ̂ · M̂(x))` is canonical for pure and mixed states, but
explicitly preserves the source-coupling admission as open. This
note's K1.4 confirms the G2 trace contributes a unit factor under
canonical normalization, NOT a source-coupling derivation.

### C4 Hierarchy theorem (Hier)

The hierarchy theorem retains `v_EW = 246.28 GeV` as a derivation
from framework axioms + computed plaquette + APBC correction. This
note uses Hier strictly for the numerical VEV location (component
(ii)); does not reuse it to derive curvature.

### C5 Tree-level mean-field shortcut (HIGGS_MASS_FROM_AXIOM Step 5(b))

[HIGGS_MASS_FROM_AXIOM_NOTE.md](HIGGS_MASS_FROM_AXIOM_NOTE.md)
Step 5(b) is explicit that `(m_H_tree/v)² = curvature/N_taste = 1/(4u_0²)`
is the tree-level mean-field Klein-Gordon readout in the symmetric
phase, with the +12% gap as the magnitude of the mean-field-
identification error. This note's K1.2 confirms component (i) IS
the symmetric-point identification, not independent post-EWSB
content. The +12% gap reproduced here is the same gap as in Step 5(b).

### C6 EWSB pattern theorem admissions

[EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md)
§5 explicitly admits as NOT derived: the Higgs potential FORM, the
VEV magnitude, the W/Z mass formulas. This note's K1.6 cross-cites
this admission as the structural reason combination cannot close
S4b-op.

### C7 S7 12% gap decomposition

[HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md)
decomposed the 12% gap into the S7 gap-closure functional Δ². This
note's +12.03% combined-prediction gap matches the sister note's S7
residual.

## 6. What this note DOES establish

1. **Combined-ingredient bounded support.** Combining (i)
   `m_H/v = 1/(2 u_0)`, (ii) `v_EW`, (iii) G2 Born trace yields
   `m_H(combined) = 140.31 GeV`, the same as any single ingredient.
   Numerical verification anchored in cited content only (no PDG
   inputs).

2. **Structural reason for failure.** The combination collapses to
   the symmetric-point identification (K1.2). G2 trace contributes
   only a unit factor under canonical normalization (K1.4). No
   interaction term shifts the curvature.

3. **+12% gap survives the combination.** The combined prediction
   matches the tree-level shortcut and the S7 12% gap residual.

4. **S4b-op orthogonal to (i)-(iii).** None of the three cited
   ingredients supplies a derivation of the post-EWSB Higgs-mass
   curvature operator at `v_EW`. The SM Higgs potential FORM
   remains admitted SM convention.

5. **Sister-prediction asymmetry preserved.** Higgs-mass gap is two
   orders of magnitude larger than sister-prediction gaps; the
   combination does not close this asymmetry.

## 7. What this note does NOT establish

- It does **NOT** close S4b-op. The post-EWSB Higgs-mass operator
  construction at `v_EW` remains load-bearing and structurally
  fused with S7.
- It does **NOT** unblock Lane 2 (Higgs mass from axiom). The
  parent matching residual `M ≡ S4 ∧ S7 ≡ S4a ∧ S4b ∧ S7 ≡
  S4a ∧ S4b-loc ∧ S4b-op ∧ S7` retains S4b-op ∧ S7 open.
- It does **NOT** close the lattice-curvature → physical
  `(m_H/v)²` matching theorem.
- It does **NOT** introduce new repo-wide axioms or new derivation
  primitives.
- It does **NOT** consume PDG values as derivation inputs. PDG
  `m_H = 125.25 GeV` appears only as a falsifiability comparator
  for the +12.03% gap.
- It does **NOT** discharge the staggered-Dirac realization gate,
  the g_bare = 1 gate, or any other open framework gate.
- It does **NOT** derive the SM Higgs potential FORM from cited
  content. This form remains "admitted SM convention".
- It does **NOT** close G2's source-coupling admission. The G2
  trace map remains bounded support for the canonical
  position-density extension.

## 8. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| K1.1 combined evaluation = `140.31 GeV` | Demonstrate that combining (i)-(iii) on cited content gives `m_H ≠ 140.31 GeV` (e.g., < 130 or > 150 GeV). Numerically false; runner verifies. |
| K1.2 combination = symmetric-point id | Demonstrate that combining (i)-(iii) is NOT a multiplicative recombination of the symmetric-point identification. Contradicts K1.4 unit-factor structure of G2 trace. |
| K1.3 lattice curvature at v_EW = symmetric value | Demonstrate `V''_taste(v_EW/M_Pl) ≠ V''_taste(0)` to relative precision better than `10⁻³⁴`. Numerically false; runner verifies. |
| K1.4 G2 trace = unit factor | Demonstrate that `Tr(ρ̂_vac · 𝟙) ≠ 1` for a normalized state. Trivially false (Tr ρ̂ = 1). |
| K1.5 +12.03% gap | Demonstrate `(m_H(combined) - m_H(PDG))/m_H(PDG) ≠ +12.03%` to relevant precision. Numerically false. |
| K1.6 S4b-op orthogonal | Demonstrate that combination (i)-(iii) constructs `Ô_{m_H²} = ∂²V_phys/∂φ²|_{v_EW}` on the post-EWSB physical Hilbert space. Requires deriving SM Higgs potential FORM from cited content (currently admitted SM convention). |
| K1.7 sister asymmetry | Demonstrate that the Higgs combined prediction achieves sister-grade precision (~0.1%) without S7 corrections. Numerically false; tree-level/combined is +12.03%. |

## 9. Verdict per brief's three honest tiers

The originating brief listed three tiers:

> 1. **Positive theorem**: combination closes S4b-op with prediction
>    matching PDG `m_H` within ~5%.
> 2. **Bounded**: partial closure.
> 3. **Negative**: combination still cannot fix the operator.

**Verdict: BOUNDED (tier 2).**

The combination of (i) `m_H/v = 1/(2u_0)`, (ii) `v_EW`, (iii) G2
Born trace gives `m_H(combined) = 140.31 GeV`, which deviates from
PDG `125.25 GeV` by `+12.03%`. This is FAR outside the tier-1 5%
threshold (would need `m_H` between 119.0 and 131.5 GeV) and outside
the typical ~10% threshold. So the combination does NOT close S4b-op
as a positive theorem.

It is also NOT cleanly tier-3 negative, because:
- Component (ii) `v_EW` does retain bounded support for S4b-loc
  (location selection).
- The combination ratifies the prior W-S4b-EWSB sub-decomposition
  `S4b ≡ S4b-loc ∧ S4b-op` and the prior tree-level mean-field
  prediction.
- The +12.03% gap is precisely the S7 residual, structurally
  identified.

**Honest reading:** the combination IS strictly equivalent to the
tree-level mean-field shortcut, multiplied by a G2 unit factor.
S4b-loc's bounded support carries through; S4b-op remains
load-bearing and structurally fused with S7. The combination does
not improve on prior results; it confirms the structural reason
(K1.2: symmetric-point identification self-reference) why it cannot.

This is **bounded** (tier 2): partial closure on S4b-loc, no
closure on S4b-op, with a structural diagnosis of why the
combination collapses to the prior tree-level prediction.

## 10. Honest scope

This note is a bounded_theorem source row for independent audit. Its claim scope is the combined-content stress test of the S4b-op closure hypothesis: the combination of the Higgs structural ratio, the EWSB Wilson-chain location, and the G2 Born-as-source trace yields m_H(combined) = v_EW/(2 u_0) = 140.31 GeV, identical to the tree-level mean-field shortcut and still +12.03% versus the PDG comparator. S4b-loc remains bounded-supported by the cited v_EW location, while S4b-op and the S7 gap-closure functional remain open.

## 11. Cross-references

### Direct parents (this note's analysis subjects)

- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) — component (i), Step 4 + Step 5(b)
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) — component (ii), Hier and sister-prediction table
- [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) — component (iii), G2 Born trace
- [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md) — hierarchy correction analysis (negative result confirming S4 layer)
- [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) — EWSB-Q + EWSB-PotForm admission

### Repo baseline / meta

- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)

### Sister cluster (Lane 2 S4 ∧ S7 pieces)

- [`HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md`](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md) — S7 sub-step decomposition (+12% functional Δ²)
- [`HIGGS_MASS_WILSON_CHAIN_PARTIAL_PROGRESS_NOTE_2026-05-10_higgsH1.md`](HIGGS_MASS_WILSON_CHAIN_PARTIAL_PROGRESS_NOTE_2026-05-10_higgsH1.md) — Wilson chain partial m_H = 124.98 GeV

## 12. Validation

```bash
python3 scripts/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.py
```

Expected: structural verification of (i) the joint hypothesis
equation evaluates to `m_H(combined) = 140.31 GeV` (K1.1), (ii) the
combination collapses to the symmetric-point identification (K1.2),
(iii) lattice curvature at `v_EW` agrees with symmetric-point
curvature to relative precision better than `10⁻³⁴` (K1.3), (iv) G2
Born trace contributes a unit factor under canonical normalization
(K1.4), (v) the +12.03% gap survives the combination (K1.5), (vi)
S4b-op is structurally orthogonal to (i)-(iii) (K1.6), (vii)
sister-prediction asymmetry preserved (K1.7). Total: PASS=N, FAIL=0
(N tabulated by runner).

Cached: [`logs/runner-cache/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.txt`](../logs/runner-cache/cl3_higgs_x_s4b_combined_2026_05_08_probeX_S4b_combined.txt)
