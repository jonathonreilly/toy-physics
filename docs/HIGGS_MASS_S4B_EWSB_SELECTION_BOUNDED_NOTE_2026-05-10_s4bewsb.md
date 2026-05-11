# Lane 2 S4b — EWSB-Selection Probe (s4bewsb)

**Date:** 2026-05-10
**Type:** bounded_theorem (sharpened sub-decomposition of S4b inside Lane 2)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal. Tests the hypothesis that the
retained Wilson-chain EWSB input (Wilson chain `v_EW = 246.28 GeV`,
`<H> = (0, v/√2)^T` direction, `Q = T_3 + Y/2` unbroken generator)
selects the post-EWSB physical vacuum `Ω_v` and the Higgs-mass operator
`Ô_{m_H²}` for the operational form
`m_H² = Tr(ρ̂_phys · Ô_{m_H²})` (S4a-supported per PR #915, T-S4H).
**Status:** source-note proposal. Verdict is **SHARPENED, NOT CLOSED**.
The retained EWSB content selects the EVALUATION-POINT location (φ = v_EW)
but does NOT construct the OPERATOR `Ô_{m_H²}` at that location. The
lattice taste-sector potential `V_taste(m) = -(N_taste/2)·log(m²+4u_0²)`
retained on the framework's source-stack has NO local minimum at finite
m — it is monotone decreasing for m > 0 — so evaluating its second
derivative at φ = v_EW does not produce the SM-Higgs curvature. The SM
Higgs potential form `V = -μ²H†H + λ(H†H)²` is "admitted SM convention"
per [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md),
not retained derivation. S4b therefore sub-decomposes into S4b-loc
(EVALUATION-POINT selection, bounded support via retained `v_EW`) and
S4b-op (POST-EWSB OPERATOR construction, load-bearing, structurally
fused with S7).
**Authority disclaimer:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** higgs-mass-s4b-ewsb-selection-20260510-s4bewsb
**Primary runner:** [`scripts/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.py`](../scripts/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.py)
**Cache:** [`logs/runner-cache/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.txt`](../logs/runner-cache/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the
proposal.

## 0. Question

PR #915 (T-S4H, [`HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md`](HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md))
sharpened Lane 2 S4 into:

- **S4a** (operational form `m_H² = Tr(ρ̂_phys · Ô_{m_H²})`) —
  bounded support via the G2 trace template
  ([`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)).
- **S4b** (state-and-operator selection of `(ρ̂_phys, Ô_{m_H²})`) —
  open, structurally fused with S7.

The brief proposes:

> Use the retained Wilson-chain EWSB input to SELECT the post-EWSB
> physical vacuum `Ω_v` and the Higgs-mass operator `Ô_{m_H²}`.
> The retained `v_EW = 246.28 GeV` per Wilson chain is the post-EWSB
> physical vacuum location. The framework KNOWS where the physical
> vacuum is. Combined with retained `m_H/v = 1/(2u_0)` and G2's
> Born-trace, this gives:
>
>   `m_H² = Tr(Ω_v · ∂²V_lattice/∂φ²|_{φ = v_EW})`
>
> Each component is retained: `Ω_v` (Wilson chain), `∂²V/∂φ²|_{φ=v_EW}`
> (m_H/v structural relation evaluated at v_EW), `Tr` (G2 Born-trace).
> If retained EWSB selects the physical vacuum, S4b closes — and
> combined with G2's S4a support, S4 closes — and Lane 2 unblocks.

**Question:** Does retained EWSB content (Wilson `v_EW`, `<H>` direction,
`Q = T_3 + Y/2`) select `(Ω_v, Ô_{m_H²})` for the Born-trace mass-readout?

## 1. Answer

**SHARPENED, NOT CLOSED.** Retained EWSB content selects the
EVALUATION-POINT location `φ = v_EW` but does NOT construct the
post-EWSB Higgs-mass OPERATOR `Ô_{m_H²}` at that location. The hypothesis
equation `m_H² = Tr(Ω_v · ∂²V_lattice/∂φ²|_{φ=v_EW})` evaluated using
the framework's retained lattice taste-sector potential
`V_taste(m) = -(N_taste/2)·log(m² + 4u_0²)` does not give the SM Higgs
curvature, because:

- **(F1) Lattice potential has no minimum at v.** `V_taste(m)` is
  monotone decreasing for m > 0 and has only the symmetric saddle at
  m = 0. The lattice taste-sector formula has NO local minimum at
  finite m, in particular none at m = v_EW/M_Pl. The "minimum at φ = v"
  is a feature of the SM Higgs potential `V(H†H) = -μ²H†H + λ(H†H)²`,
  whose form is *admitted SM convention* per
  [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md)
  §5 ("The Higgs potential V(H†H) = -μ²H†H + λ(H†H)² form (admitted
  SM convention)"), not a retained derivation.

- **(F2) Lattice curvature at φ = v_EW ≠ post-EWSB physical curvature.**
  Numerically, `V''_taste(v_EW/M_Pl)` evaluated on the framework's
  retained taste-sector formula equals the symmetric-point value
  `V''_taste(0) = -4/u_0²` (tachyonic) to relative precision better
  than `(v/M_Pl)² ≈ 4×10⁻³⁴`. Re-evaluating the lattice potential at
  φ = v_EW does NOT switch sign of the curvature; it remains
  tachyonic to extreme precision. Thus the brief's hypothesis
  equation, instantiated on retained content, gives a tachyonic
  curvature times v² — not the physical 125²-GeV² post-EWSB Higgs
  mass squared.

- **(F3) The structural relation `m_H/v = 1/(2u_0)` is the
  symmetric-point relation divided by N_taste — NOT independent
  post-EWSB content.** Per
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  Step 5(b), `(m_H_tree/v)² = (4/u_0²) / N_taste = 1/(4u_0²)` is the
  *tree-level mean-field Klein-Gordon readout in the symmetric phase*,
  identifying per-channel symmetric-point curvature with `(m_H/v)²`.
  This is precisely the S4 identification the parent T-S4H probe
  flagged as load-bearing. It is NOT a separately retained post-EWSB
  curvature relation; it is the asserted symmetric-point identification
  itself. Treating `m_H/v = 1/(2u_0)` as "retained post-EWSB
  structural content" is therefore circular at the S4 layer.

- **(F4) Retained `<H>` direction gives generator selection, not
  operator construction.** The retained EWSB content
  ([`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md))
  derives `Q = T_3 + Y/2` from `<H> = (0, v/√2)^T` plus standard
  SU(2)_L Lie algebra. This selects WHICH gauge generator survives EWSB
  but does NOT construct the Higgs-mass operator `Ô_{m_H²}`. The note
  explicitly admits §5 that the Higgs potential FORM, the VEV
  magnitude, and the W/Z mass formulas are *not* derived. Q-selection
  ≠ `Ô_{m_H²}` construction.

**Conclusion.** Retained EWSB content provides **partial selection**:
the evaluation-point location `φ = v_EW` is bounded-supported by the
retained Wilson chain. But the OPERATOR `Ô_{m_H²} = ∂²V_phys/∂φ²|_{φ=v}`
is NOT constructible from retained content alone. S4b sub-decomposes
into:

```text
S4b ≡ S4b-loc (evaluation-point selection)  ∧  S4b-op (operator construction)
```

S4b-loc is bounded-supported; S4b-op remains load-bearing and
structurally fused with S7. The parent matching residual
`M ≡ S4 ∧ S7 ≡ S4a ∧ S4b ∧ S7 ≡ S4a ∧ S4b-loc ∧ S4b-op ∧ S7` retains
S4b-op ∧ S7 open. **Lane 2 remains blocked.**

## 2. Setup

### Premises (this note's bounded-support lemma)

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| Hier | `v_EW = M_Pl · (7/8)^{1/4} · α_LM¹⁶ = 246.28 GeV` (hierarchy theorem, retained) | [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) §3.2 |
| EWSB-Q | `Q = T_3 + Y/2` from `<H> = (0, v/√2)^T` + Y_H = +1 (exact-support theorem) | [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) |
| EWSB-PotForm | "The Higgs potential `V(H†H) = -μ²H†H + λ(H†H)²` form (admitted SM convention)" | same source, §5 |
| Plaq-MC | `<P>_iso(β=6) = 0.5934`; `u_0 = <P>^{1/4} = 0.8776` | [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) §3.1 |
| TasteV | `V_taste(m) = -(N_taste/2)·log(m² + 4u_0²)`, `N_taste = 16` | [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) Step 2-3 |
| TreeReadout | `(m_H_tree/v)² := |V''_lat(0)|/N_taste = 1/(4u_0²)` (symmetric-point identification) | same source, Step 5(b) |
| ParentS4H | S4 ≡ S4a ∧ S4b decomposition; S4a bounded-supported, S4b open | [`HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md`](HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md) |
| ParentMatch | `M_residual = S4 ∧ S7` per-step accounting | [`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`](LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md) |
| G2-Born | Unified position-density Born map `Tr(ρ̂ · M̂(x))` (canonical for pure and mixed states) | [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| HiggsAuth | "VEV magnitude (admitted external observable)... W/Z mass formulas (require Higgs kinetic term + EW mixing angle)" | [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) §5 |

### Forbidden imports

- NO PDG observed values used as derivation input (only as falsifiability comparators).
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained.
- NO empirical fits.
- NO same-surface family arguments.
- NO new physics inputs beyond cited baseline + retained EWSB content + retained taste-sector formula + standard QM expectation-value formalism.

## 3. Theorem (bounded support, sharpened S4b decomposition)

**Theorem (S4b EWSB-selection, bounded; sharpened sub-decomposition).**

Under the premises of §2 with no new imports, the brief's hypothesis
that retained EWSB content selects `(Ω_v, Ô_{m_H²})` decomposes into a
LOCATION sub-claim and an OPERATOR sub-claim:

```text
S4b ≡ S4b-loc  ∧  S4b-op

S4b-loc := evaluation point φ* = v_EW selected from retained Wilson chain
S4b-op  := operator Ô_{m_H²} = ∂²V_phys/∂φ² constructed at φ* = v_EW
```

The decomposition satisfies:

- **(B1.1) Retained `v_EW` selects the evaluation-point location.**
  The hierarchy theorem (Hier) retains `v_EW = M_Pl · (7/8)^{1/4} ·
  α_LM¹⁶ = 246.28 GeV` as a derivation from the physical `Cl(3)`
  local algebra, `Z^3` spatial substrate, and the single computed
  plaquette `<P> = 0.5934`. This numerical value
  IS retained framework content. Setting `φ* = v_EW` for the
  Born-trace evaluation point is therefore bounded-supported; it does
  not require external SM convention.

- **(B1.2) Retained `<H>` direction selects unbroken generator, not
  operator.** EWSB-Q derives `Q = T_3 + Y/2` from `<H> = (0, v/√2)^T`
  plus Y_H = +1 plus standard SU(2)_L Lie algebra. This selects the
  unbroken U(1) generator — a CHARGE OPERATOR, not the Higgs-mass
  squared operator. The note explicitly admits (§5) that "The Higgs
  potential V(H†H) = -μ²H†H + λ(H†H)² form (admitted SM convention)"
  and "The VEV v magnitude (admitted external observable)" are NOT
  derived. So the EWSB pattern theorem does not construct the
  curvature operator at φ = v.

- **(B1.3) Lattice taste-sector potential evaluated at φ = v_EW gives
  symmetric-point curvature, not post-EWSB curvature.** The retained
  taste-sector formula (TasteV) is
  `V_taste(m) = -(N_taste/2)·log(m² + 4u_0²)`. Its second derivative is
  ```
  V''_taste(m) = -N_taste · (2|λ|² - 2m²) / (m² + |λ|²)²
  ```
  with `|λ|² = 4u_0²` in the L_t = 2 block. At m = v_EW/M_Pl, since
  `(v/M_Pl)² ≈ 4 × 10⁻³⁴` is exponentially smaller than `4u_0² ≈ 3.08`,
  ```
  V''_taste(v/M_Pl) = -2 N_taste · 4u_0² / (4u_0²)² · [1 + O((v/M_Pl)²)]
                    = -N_taste / (2u_0²) · [1 + O(10⁻³⁴)]
                    = -4/u_0² · [1 + O(10⁻³⁴)]
                    = V''_taste(0)  (to relative precision ~10⁻³⁴).
  ```
  The runner verifies this numerically. Therefore the lattice
  taste-sector curvature evaluated at the retained `v_EW` location
  remains tachyonic and equal to the symmetric-point value to extreme
  precision.

- **(B1.4) The hypothesis equation gives tachyonic m_H² on retained
  content.** Substituting B1.3 into the brief's hypothesis with
  `Ω_v ↦ ρ̂_lat(0)` (the only state available from retained content):
  ```
  Tr(ρ̂_lat(0) · ∂²V_taste/∂φ²|_{φ=v_EW}) ≈ V''_taste(0) / N_taste · v² × M_Pl² (units)
                                          = -1/(4u_0²) · v²
  ```
  in dimensionless lattice units, this is **negative**, i.e. a
  tachyonic m_H² < 0. Even if one re-interpreted as `|V''_taste|/N_taste`
  (the symmetric-point identification), one recovers the parent T-S4H
  probe's analysis: this IS the tree-level mean-field shortcut, not a
  post-EWSB derivation.

- **(B1.5) Structural relation m_H/v = 1/(2u_0) is the symmetric-point
  identification itself.** Per
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  Step 5(b), `(m_H_tree/v)² = curvature/N_taste = 1/(4u_0²)` is
  derived FROM the symmetric-point lattice curvature divided by
  N_taste. It is not an INDEPENDENT post-EWSB content piece that
  could be reused at φ = v_EW; it is precisely the asserted
  identification flagged as load-bearing in the parent matching note.
  Using it to "derive the operator at v_EW" is circular: one would be
  using the conclusion of the symmetric-point identification (the
  tree-level formula) to motivate evaluating the same symmetric-point
  curvature at the retained `v_EW` location — which gives the same
  symmetric-point value (B1.3). No new content emerges.

- **(B1.6) Sharpened S4b decomposition.**
  ```
  S4b ≡ S4b-loc ∧ S4b-op
  S4b-loc: evaluation-point location φ* = v_EW       [bounded support via Hier]
  S4b-op:  operator Ô_{m_H²} at φ* = v_EW             [LOAD-BEARING; NOT retained]
  ```
  S4b-loc is supported by retained `v_EW`. S4b-op requires either:
  (i) a derivation of the SM Higgs potential form `V = -μ²H†H + λ(H†H)²`
      from retained content (currently EWSB-PotForm is admitted SM
      convention, not derived); or
  (ii) a derivation of the post-EWSB stationary-point curvature from
       the lattice partition function (this is precisely the cluster
       obstruction synthesised in
       [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md));
       or
  (iii) a separate retained chain that constructs `Ô_{m_H²}` without
        reusing the symmetric-point identification (none currently
        exists in the source stack).

  None of (i)-(iii) is supplied by retained EWSB content.

- **(B1.7) Sister-prediction precision asymmetry confirms structural
  obstruction.** Retained sister predictions on the SAME hierarchy
  chain achieve sub-percent precision: `v_EW` (+0.03%), `α_s(M_Z)`
  (+0.14%), `m_t(pole)` (-0.07% at 2-loop), `1/α_EM(M_Z)` (-0.22%).
  The structural problem is NOT in the retained Wilson chain. It IS
  in the SYMMETRIC-POINT IDENTIFICATION (S4) and the GAP-CLOSURE
  FUNCTIONAL (S7). Retained `v_EW` has the same status here as it
  does for those sister predictions; it does not carry post-EWSB
  Higgs-curvature information that could close S4b-op.

## 4. Proof sketch

### B1.1 v_EW retained as derivation

The hierarchy theorem (Hier) retains `v_EW = M_Pl · (7/8)^{1/4} · α_LM¹⁶`
as a derivation from the physical `Cl(3)` local algebra, `Z^3`
spatial substrate, the single computed plaquette, and the staircase
taste threshold structure. The
numerical value `v_EW = 246.28 GeV` agrees with the PDG `246.22 GeV` to
+0.03%, where PDG appears as a falsifiability comparator only. The
runner (Section 1) prints `v_EW` evaluated from cited retained inputs
and verifies the agreement.

The Born-trace evaluation point `φ* = v_EW` is therefore bounded-supported
by retained content; setting `φ* = v_EW` does not require new imports. ∎

### B1.2 EWSB-Q gives generator selection, not curvature operator

Per EWSB-Q, the unbroken generator from `<H> = (0, v/√2)^T` and Y_H = +1
is `Q = T_3 + Y/2` (exact-support theorem). The runner verifies the
derivation acts at the GAUGE-GENERATOR level: it picks Q from the
SU(2)_L × U(1)_Y generators by demanding annihilation of the VEV. This
is a Lie-algebra operation on a 2D doublet space, NOT a construction of
the squared-mass operator on the physical Hilbert space.

EWSB_PATTERN_FROM_HIGGS_Y §5 explicitly admits as NOT closed:
- "The Higgs potential V(H†H) = -μ²H†H + λ(H†H)² form (admitted SM convention)"
- "The VEV v magnitude (admitted external observable)"
- "The W/Z mass formulas (require Higgs kinetic term + EW mixing angle)"

So no chain in EWSB_PATTERN_FROM_HIGGS_Y derives `Ô_{m_H²}`. The
runner cross-cites this admission. ∎

### B1.3 Lattice curvature at v_EW = symmetric-point curvature

The runner computes (in dimensionless lattice units `m̂ = m·a` with
a = 1/M_Pl):
```
m̂_v = v_EW / M_Pl ≈ 2.017 × 10⁻¹⁷
|λ̂|² = 4 u_0² = 4 · (0.8776)² ≈ 3.0808
V''_taste(m̂)/N_taste = (V''_taste(0)/N_taste) · [1 - 2(m̂/|λ̂|)² + O((m̂/|λ̂|)⁴)]
                     = -1/(4u_0²) · [1 - 1.32×10⁻³⁴ + ...]
```
The relative deviation from the symmetric-point value is
`2(m̂_v/|λ̂|)² ≈ 1.32 × 10⁻³⁴`, far below any plausible numerical
threshold. The lattice taste-sector curvature evaluated at the
retained `v_EW` location IS, to all practical precision, the
symmetric-point value `-4/u_0²` (tachyonic).

This is the central numerical finding: re-evaluating the LATTICE
curvature at `v_EW` does NOT switch sign. The runner confirms this
across multiple cross-checks (different orderings, vectorised
expressions). ∎

### B1.4 Hypothesis equation evaluated on retained content gives wrong sign

Substituting B1.3 into the hypothesis equation with the only available
retained density operator (`ρ̂_lat(0)`, the symmetric-phase lattice
vacuum):
```
Tr(ρ̂_lat(0) · V''_taste(v_EW) / N_taste) · v_EW²
   = V''_taste(v_EW) / N_taste · v_EW²
   = (-4/u_0²)/16 · v_EW²
   = -1/(4u_0²) · v_EW²
   < 0
```
This is **tachyonic** — it does not give a physical Higgs mass squared.
The framework does not retain a different `ρ̂` (the post-EWSB
`Ω_v ⟨Ω_v|` is precisely the open S4b-op residual). Therefore the
brief's hypothesis equation, evaluated strictly on retained content,
fails to give a physical m_H².

If one instead applies the parent T-S4H absolute-value identification
`m_H_tree² = |V''_taste|/N_taste · v_EW² = 1/(4u_0²) · v_EW²`,
one recovers `m_H_tree = v_EW/(2u_0) = 140.31 GeV` — but this IS the
tree-level mean-field symmetric-point shortcut already analysed in
PR #915 (M1.5). It is not a post-EWSB derivation; it is the +12% gap
parent. ∎

### B1.5 m_H/v = 1/(2u_0) is the symmetric-point identification

The structural relation `m_H/v = 1/(2u_0)` is derived in
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
Step 5(b) by *identifying* the per-channel symmetric-point curvature
`(4/u_0²)/N_taste = 1/(4u_0²)` with `(m_H/v)²`. The note itself
explicitly states (Step 5(b)): "the note's tree-level shortcut is:
identify the per-channel curvature at the symmetric point ... with
(m_H_tree/v)² directly, treating the symmetric-point curvature as a
proxy for the post-EWSB mass at the natural EWSB scale v. This is the
standard mean-field estimate that becomes exact in the limit where
... none of (i)-(iii) is exactly true — the +12% gap is precisely the
magnitude of the correction."

So `m_H/v = 1/(2u_0)` IS the asserted symmetric-point identification
flagged as the load-bearing S4 residual in the parent matching note.
Reusing it to "construct the operator at φ = v_EW" is circular at the
S4 layer: it is precisely the identification under question. The
runner cross-cites this admission. ∎

### B1.6 Sharpened S4b decomposition

Combining B1.1-B1.5:

```text
S4b: state-and-operator selection of (ρ̂_phys, Ô_{m_H²}) from retained content.

S4b decomposes as:
  S4b-loc: select evaluation-point location φ* for Ô_{m_H²}.
           SUPPORTED by retained Hier (v_EW = 246.28 GeV).
  S4b-op:  construct operator Ô_{m_H²} at φ*.
           NOT SUPPORTED by retained content because:
             - Lattice V_taste has no minimum at v_EW (B1.3).
             - SM Higgs potential form is admitted SM convention (EWSB-PotForm).
             - Tree-level relation m_H/v = 1/(2u_0) IS the symmetric-point
               identification under question (B1.5), not independent
               post-EWSB content.
             - EWSB-Q gives generator selection, not Ô_{m_H²} (B1.2).
```

S4b-loc reduces the S4b residual scope by separating the location
choice (retained) from the operator construction (open). S4b-op
remains load-bearing and structurally fused with S7 (gap-closure
functional Δ²). The parent matching residual:
```
M ≡ S4 ∧ S7
   ≡ S4a ∧ S4b ∧ S7
   ≡ S4a ∧ (S4b-loc ∧ S4b-op) ∧ S7
   ≡ S4a ∧ S4b-loc                         [bounded-supported]
   ∧ S4b-op ∧ S7                           [OPEN]
```
**Lane 2 remains blocked** (S4b-op ∧ S7 open), but the open block is
narrower than the parent S4b ∧ S7. ∎

### B1.7 Sister-prediction precision diagnosis

The runner numerically tabulates retained sister predictions on the
same hierarchy chain:
| Quantity | Predicted | PDG | Deviation |
|---|---|---|---|
| `v_EW` | 246.28 | 246.22 | +0.03% |
| `α_s(M_Z)` | 0.1181 | 0.1179 | +0.14% |
| `1/α_EM(M_Z)` | 127.67 | 127.95 | -0.22% |
| `m_t(pole, 2L)` | 172.57 | 172.69 | -0.07% |
| `m_H_tree (S4)` | 140.31 | 125.25 | +12.03% |

The Higgs-mass tree-level prediction is roughly **two orders of
magnitude worse** than the sister predictions. The structural
obstruction is therefore NOT in the retained chain; it IS in the
SYMMETRIC-POINT IDENTIFICATION (S4 ≡ S4a ∧ S4b) and the GAP-CLOSURE
FUNCTIONAL (S7). Retained `v_EW` carries the same hierarchy-chain
information for m_H as for `m_t` — it does NOT carry post-EWSB
Higgs-curvature information that could close S4b-op. ∎

## 5. Consistency with cited content

### C1 Parent T-S4H (S4 ≡ S4a ∧ S4b)

PR #915 ([T-S4H](HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md))
established `S4 ≡ S4a ∧ S4b`, with S4a (operational form) bounded-supported
via the G2 Born-trace template and S4b (state-and-operator selection)
open. This note further sub-decomposes S4b into S4b-loc (location
selection, supported via retained `v_EW`) and S4b-op (operator
construction, load-bearing). The parent's M1.5 analysis of the
tree-level mean-field shortcut as a state-and-operator approximation
is fully consistent with B1.5 here.

### C2 Parent matching theorem (M ≡ S4 ∧ S7)

PR #865 ([Match](LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md))
established the per-step accounting M ≡ S1...S7 with `M_residual = S4 ∧ S7`.
The further sub-decomposition `S4b ≡ S4b-loc ∧ S4b-op` here narrows S4b
without changing S4 ≡ S4a ∧ S4b at the parent level.

### C3 Hierarchy theorem (Hier)

The hierarchy theorem retains `v_EW = M_Pl · (7/8)^{1/4} · α_LM¹⁶ =
246.28 GeV` as a derivation from the repo baseline + computed plaquette
([COMPLETE_PREDICTION_CHAIN_2026_04_15.md](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
§3.2). This note uses Hier strictly at the level of the numerical VEV
location; it does not reuse Hier to derive the post-EWSB curvature
operator.

### C4 EWSB pattern theorem (EWSB-Q, EWSB-PotForm)

[`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md)
derives `Q = T_3 + Y/2` from `<H> = (0, v/√2)^T` plus Y_H = +1 plus
standard SU(2)_L Lie algebra. §5 explicitly admits that the Higgs
potential FORM, the VEV magnitude, and the W/Z mass formulas are NOT
derived. This note relies on EWSB-Q only for the conclusion that
EWSB-pattern content gives generator selection, not operator
construction.

### C5 Tree-level mean-field shortcut

[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
Step 5(b) is explicit that the symmetric-point identification
`(m_H_tree/v)² = curvature/N_taste = 1/(4u_0²)` is the tree-level
mean-field Klein-Gordon readout in the symmetric phase, with the
+12% gap as the magnitude of the mean-field-identification error.
This note's B1.5 analysis confirms this framing: `m_H/v = 1/(2u_0)`
is the symmetric-point identification itself, not independent
post-EWSB content.

### C6 G2 Born-trace template

[`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)
establishes `Tr(ρ̂ · M̂(x))` as canonical for both pure and mixed states.
This note instantiates the same template with the curvature observable
and verifies that no closure of S4b-op follows from template generality
alone (consistent with M1.1 of T-S4H).

## 6. What this note DOES establish

1. **Bounded support for S4b-loc.** The Born-trace evaluation-point
   location `φ* = v_EW` is supported by retained Hier (`v_EW = 246.28
   GeV`); setting `φ* = v_EW` does not require new imports.

2. **Sharpened S4b decomposition.** S4b ≡ S4b-loc (supported) ∧
   S4b-op (open). The decomposition narrows the open scope of S4b
   from "state-and-operator selection" to "post-EWSB operator
   construction at the retained `v_EW` location".

3. **Structural diagnosis: lattice curvature at v_EW = symmetric-point
   curvature.** Numerical verification that
   `V''_taste(v_EW/M_Pl) = V''_taste(0)` to relative precision better
   than `10⁻³⁴`. Re-evaluating the lattice potential at `v_EW` does
   not switch sign of the curvature.

4. **Three-fold blockage of S4b-op.** S4b-op does NOT close from
   retained content because (i) lattice taste-sector potential has no
   minimum at v, (ii) SM Higgs potential form is admitted SM
   convention, (iii) `m_H/v = 1/(2u_0)` is the symmetric-point
   identification itself (not independent post-EWSB content).

5. **Sister-prediction asymmetry.** Retained sister predictions
   (`v_EW`, `α_s`, `m_t`) achieve sub-percent precision on the same
   hierarchy chain; the Higgs-mass tree-level is +12.03%, two orders
   worse, confirming the structural obstruction is in S4 (symmetric-
   point identification) and S7 (gap-closure functional), not in the
   retained chain.

## 7. What this note does NOT establish

- It does **NOT** close S4b. The S4b-op sub-piece remains
  load-bearing and structurally fused with S7.
- It does **NOT** unblock Lane 2 (Higgs mass from axiom). The parent
  matching residual M ≡ S4 ∧ S7 has S4a ∧ S4b-loc bounded-supported,
  S4b-op ∧ S7 open.
- It does **NOT** close the lattice-curvature → physical (m_H/v)²
  matching theorem. The Nature-grade non-perturbative analytic gap
  per the 2026-05-02 cluster obstruction synthesis remains.
- It does **NOT** introduce new repo-wide axioms or new derivation
  primitives. No new imports beyond cited baseline + retained content.
- It does **NOT** consume PDG values as derivation inputs. The
  numerical sanity-check table records framework predictions vs PDG
  values for falsifiability-anchor purposes only.
- It does **NOT** discharge the staggered-Dirac realization gate, the
  g_bare = 1 gate, or any other open framework gate per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- It does **NOT** derive the SM Higgs potential form `V(H†H) = -μ²H†H +
  λ(H†H)²` from retained content. This form remains "admitted SM
  convention" per EWSB-PotForm.
- It does **NOT** construct `Ω_v` or `Ô_{m_H²}` as objects on the
  physical Hilbert space.

## 8. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| B1.1 `v_EW` retained | Demonstrate `v_EW = 246.28 GeV` is NOT derived from `M_Pl · (7/8)^{1/4} · α_LM¹⁶` on the retained chain. Trivially false; runner verifies. |
| B1.2 EWSB-Q ≠ Ô_{m_H²} | Demonstrate that the Q-selection theorem in EWSB_PATTERN_FROM_HIGGS_Y constructs the squared-mass operator. Trivially false; the theorem is a Lie-algebra annihilation argument on a 2D doublet, not a Hilbert-space curvature operator construction. |
| B1.3 V''_taste(v) = V''_taste(0) | Demonstrate `V''_taste(v/M_Pl) ≠ V''_taste(0)` to relative precision better than `10⁻³⁴`. Numerically false; runner verifies symbolically and numerically. |
| B1.4 wrong-sign m_H² | Demonstrate `Tr(ρ̂_lat(0) · V''_taste(v_EW)/N_taste) · v_EW² > 0` on the retained taste-sector potential. Numerically false; the curvature is tachyonic. |
| B1.5 m_H/v = 1/(2u_0) is symmetric-point | Demonstrate that `m_H/v = 1/(2u_0)` is derived independently of the symmetric-point identification on the retained source stack. Contradicts HIGGS_MASS_FROM_AXIOM_NOTE Step 5(b) explicit framing. |
| B1.6 S4b decomposition | Demonstrate a closure of S4b-op from retained content (no S4b-loc/S4b-op split needed). Would require deriving the SM Higgs potential form from retained content, which is currently admitted SM convention per EWSB-PotForm. |
| B1.7 sister-precision asymmetry | Demonstrate that the Higgs-mass tree-level achieves sister-grade precision (~0.1%) without S7 corrections. Numerically false; tree-level is +12.03% on retained chain. |

## 9. Verdict per brief's three honest outcomes

The originating brief listed three honest outcomes:

> 1. **CLOSURE**: S4b closes via retained EWSB + G2 Born-trace.
>    Lane 2 unblocks (modulo S7's 12% gap).
> 2. **STRUCTURAL OBSTRUCTION**: retained EWSB doesn't actually
>    select the physical vacuum without additional content.
> 3. **SHARPENED**: partial closure (Ω_v retained but operator
>    selection still has residual).

**Verdict: SHARPENED (option 3).**

The retained EWSB content (Hier, EWSB-Q) provides PARTIAL selection:
the evaluation-point location `φ* = v_EW` is bounded-supported by
retained `v_EW`. But the OPERATOR `Ô_{m_H²}` at that location is NOT
constructible from retained content because:
(F1) the lattice taste-sector potential has no minimum at v;
(F2) `V''_taste(v) = V''_taste(0)` to relative precision better than `10⁻³⁴`;
(F3) `m_H/v = 1/(2u_0)` is the symmetric-point identification itself, not
     independent post-EWSB content;
(F4) EWSB-Q gives generator selection, not operator construction.

S4b sub-decomposes into S4b-loc (supported) and S4b-op (load-bearing).
The parent matching residual reduces from `S4 ∧ S7 ≡ S4a ∧ S4b ∧ S7`
to `S4a ∧ S4b-loc ∧ S4b-op ∧ S7`, with only S4b-op ∧ S7 open. **Lane 2
remains blocked**, but the open block is narrower than the parent S4b
∧ S7.

This is **honest sharpening**: the brief's central hypothesis (retained
EWSB selects the physical vacuum) is true at the LOCATION level (B1.1)
but false at the OPERATOR level (B1.2-B1.5). The framework retains
WHERE the post-EWSB minimum sits (numerical `v_EW`), but does NOT
retain WHAT the curvature is at that minimum (operator
`Ô_{m_H²}`). The tree-level shortcut `m_H/v = 1/(2u_0)` reuses the
symmetric-point identification under question, so it does not bridge
S4b-op.

## 10. Honest scope (audit-readable)

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Sharpened sub-decomposition of S4b inside Lane 2 step S4 of the
  lattice-curvature → physical (m_H/v)² matching residual. Tests the
  hypothesis that retained EWSB content (Wilson chain v_EW, <H>
  direction, Q = T_3 + Y/2) selects (Ω_v, Ô_{m_H²}) for the Born-trace
  operational form m_H² = Tr(rho_phys * O_{m_H^2}).

  Verdict: retained EWSB content selects the EVALUATION-POINT
  LOCATION (φ* = v_EW = 246.28 GeV bounded-supported via Hier) but
  does NOT construct the OPERATOR Ô_{m_H²} at that location. The
  retained lattice taste-sector potential V_taste(m) =
  -(N_taste/2)·log(m² + 4u_0²) has no minimum at finite m; its second
  derivative at m = v_EW/M_Pl equals the symmetric-point value
  V''_taste(0) = -4/u_0² to relative precision better than 10⁻³⁴.
  The SM Higgs potential form V = -μ²H†H + λ(H†H)² is "admitted SM
  convention" per EWSB_PATTERN_FROM_HIGGS_Y §5, not retained
  derivation. The structural relation m_H/v = 1/(2u_0) is itself the
  symmetric-point identification (HIGGS_MASS_FROM_AXIOM Step 5(b)),
  not independent post-EWSB content.

  Sharpening: S4b ≡ S4b-loc (location selection, bounded-supported)
  ∧ S4b-op (operator construction, load-bearing, structurally fused
  with S7). Parent matching residual: M ≡ S4a ∧ S4b-loc ∧ S4b-op ∧
  S7, with S4a ∧ S4b-loc bounded-supported and S4b-op ∧ S7 open.
  Lane 2 remains blocked, but the open block is narrower than the
  parent S4b ∧ S7.

residual_engineering_admission: c_iso_e_witness_compute_frontier  # named, but does NOT bridge S4b-op
residual_structural_admissions:
  - lattice_curvature_to_physical_m_h_v_squared_matching_theorem  # parent residual
  - tree_level_mean_field_readout_to_post_ewsb_mass_identification  # S4 (load-bearing)
  - state_and_operator_selection_for_born_trace_mass_readout  # S4b (parent T-S4H sub-issue)
  - post_ewsb_higgs_mass_squared_operator_construction  # S4b-op (this note's load-bearing residual)
  - twelve_percent_gap_closure_functional_delta_squared  # S7 (load-bearing)
  - sm_higgs_potential_form_minus_mu2_h_h_plus_lambda_h_h_squared  # admitted SM convention per EWSB-PotForm
  - n_taste_16_uniform_channel
  - g_bare_canonical_normalization
  - staggered_dirac_realization_gate

declared_one_hop_deps:
  - higgs_mass_s4_born_extension_bounded_note_2026-05-10_higgss4
  - g_newton_born_as_source_positive_theorem_note_2026-05-10_gnewtong2
  - lattice_physical_matching_theorem_bounded_obstruction_note_2026-05-10_match
  - higgs_mass_from_axiom_note
  - higgs_mass_hierarchy_correction_note
  - ewsb_pattern_from_higgs_y_note_2026-05-02
  - complete_prediction_chain_2026_04_15
  - minimal_axioms_2026-05-03
  - physical_lattice_foundational_interpretation_note_2026-05-08
  - higgs_mass_12pct_gap_decomposition_bounded_note_2026-05-10_higgss7

admitted_context_inputs:
  - tree_level_mean_field_readout_to_post_ewsb_mass_identification
  - state_and_operator_selection_for_born_trace_mass_readout
  - post_ewsb_higgs_mass_squared_operator_construction
  - twelve_percent_gap_closure_functional_delta_squared
  - sm_higgs_potential_form_minus_mu2_h_h_plus_lambda_h_h_squared
  - n_taste_16_uniform_channel
  - g_bare_canonical_normalization
  - staggered_dirac_realization_gate

load_bearing_step_class: bounded_theorem  # location supported; operator construction open
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 11. Cross-references

### Direct parents (this note's analysis subjects)

- [`HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md`](HIGGS_MASS_S4_BORN_EXTENSION_BOUNDED_NOTE_2026-05-10_higgsS4.md) — T-S4H source: S4 ≡ S4a ∧ S4b decomposition
- [`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`](LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md) — parent S4 ∧ S7 framing
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) — symmetric-point identification (B1.5 source)
- [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md) — hierarchy correction analysis (negative result confirming S4 layer)
- [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) — EWSB-Q (B1.2) and EWSB-PotForm admission
- [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) — Hier (`v_EW = 246.28 GeV`) and sister-prediction table
- [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) — G2 Born-trace template

### Repo baseline / meta

- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)

### Sister cluster (Lane 2 S4 ∧ S7 pieces)

- [`HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md`](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md) — S7 sub-step decomposition
- [`HIGGS_MASS_WILSON_CHAIN_PARTIAL_PROGRESS_NOTE_2026-05-10_higgsH1.md`](HIGGS_MASS_WILSON_CHAIN_PARTIAL_PROGRESS_NOTE_2026-05-10_higgsH1.md) — Wilson chain partial m_H = 124.98 GeV
- [`WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md) — Wilson taste-breaking LO

## 12. Validation

```bash
python3 scripts/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.py
```

Expected: structural verification of (i) `v_EW` retained on hierarchy
chain (B1.1), (ii) EWSB-Q gives generator selection not operator
construction (B1.2), (iii) lattice curvature at v_EW equals
symmetric-point curvature to relative precision better than `10⁻³⁴`
(B1.3), (iv) hypothesis equation gives tachyonic m_H² on retained
content (B1.4), (v) `m_H/v = 1/(2u_0)` is the symmetric-point
identification itself (B1.5), (vi) sharpened S4b decomposition (B1.6),
(vii) sister-prediction precision asymmetry (B1.7). Total: PASS=N,
FAIL=0 (N tabulated by runner).

Cached: [`logs/runner-cache/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.txt`](../logs/runner-cache/cl3_higgs_mass_s4b_ewsb_selection_2026_05_10_s4bewsb.txt)

## 13. User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does NOT
  assert "consistency = derivation". Retained `v_EW` does not bridge
  S4b-op; the structural obstruction is named explicitly (F1-F4).
- `feedback_hostile_review_semantics.md`: the brief's hypothesis is
  stress-tested at the operator-construction layer. The B1.5 finding
  (m_H/v = 1/(2u_0) IS the symmetric-point identification) is the
  semantic stress-test — it shows the structural relation cannot be
  reused as "independent retained post-EWSB content".
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded-theorem proposal
  sharpening one sub-issue inside Lane 2 step S4b. Audit-lane
  authority on `effective_status` is preserved.
- `feedback_physics_loop_corollary_churn.md`: this is structurally
  new content. The S4b ≡ S4b-loc ∧ S4b-op decomposition narrows the
  parent T-S4H S4b residual without relabeling it; the structural
  diagnosis (lattice curvature at v_EW = symmetric-point curvature to
  10⁻³⁴) is new numerical content.
- `feedback_compute_speed_not_human_timelines.md`: no time estimates.
  Verdict described in terms of structural blockages (F1-F4) and
  what content suffices vs what remains open.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  the EWSB-selection attack with sharp PASS/FAIL deliverables in the
  runner: B1.1 v_EW retained, B1.2 EWSB-Q ≠ operator, B1.3 lattice
  curvature numerical match, B1.4 tachyonic-on-retained, B1.5
  symmetric-point-identification self-reference, B1.6 sharpened
  decomposition, B1.7 sister-precision asymmetry.
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  Lane 2 S4b residual is being fragmented into S4b-loc (supported)
  and S4b-op (open). No new framework premises; admissions named
  explicitly. The narrowing reduces the open scope without claiming
  closure.

## 14. Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, avoid one-step
relabelings of already-landed cycles. This note:

- Is **NOT** a relabel of T-S4H (parent), which decomposed S4 ≡ S4a
  ∧ S4b at the operational/selection layer. This note further
  decomposes S4b ≡ S4b-loc ∧ S4b-op at the location/operator layer
  and tests the brief's hypothesis (retained EWSB selects the
  physical vacuum) at a more granular level.
- Is **NOT** a relabel of the parent matching note (which decomposed
  M ≡ S1...S7). This note focuses specifically on the S4b sub-piece
  inside S4 and provides numerical evidence of the lattice-vs-physical
  curvature gap at the v_EW location (B1.3).
- Is **NOT** a relabel of the S7 12% gap decomposition (sister note),
  which decomposed Δ² ≡ δ_W · δ_CW · δ_lat · δ_R. This note operates
  at the S4b layer, not S7.
- Provides **structurally new content**: the numerical fact that
  `V''_taste(v_EW) = V''_taste(0)` to relative precision `10⁻³⁴` is
  new evidence; the B1.5 self-reference identification is a new
  semantic stress-test; the S4b-loc/S4b-op decomposition is a new
  structural sub-decomposition.

## 15. Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No — S4b-op (post-EWSB operator construction at retained `v_EW` location) remains open and structurally fused with S7 (Δ² gap-closure). S4b-loc (location selection) IS supported by retained Hier. |
| V2 | New bounded support? | Yes — (i) S4b-loc bounded-supported by retained `v_EW`; (ii) numerical structural diagnosis that `V''_taste(v_EW) = V''_taste(0)` to relative precision `10⁻³⁴` (new evidence); (iii) sharpened S4b ≡ S4b-loc ∧ S4b-op decomposition. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) `v_EW` retention (B1.1), (ii) EWSB-Q ≠ operator (B1.2, citing EWSB-PotForm admission), (iii) lattice-curvature numerical match (B1.3, with explicit computation), (iv) tachyonic-on-retained (B1.4), (v) m_H/v self-reference (B1.5, citing HIGGS_MASS_FROM_AXIOM Step 5(b) explicit framing), (vi) sharpened S4b decomposition (B1.6), (vii) sister-precision asymmetry (B1.7). |
| V4 | Marginal content non-trivial? | Yes — sharpening one sub-issue (S4b-loc/S4b-op) inside a load-bearing residual (S4b) of a Nature-grade matching theorem (Lane 2) is non-trivial. The structural insight that retained `v_EW` selects WHERE but not WHAT for the Higgs-mass operator clarifies the precise residual scope at the EWSB-selection layer. |
| V5 | One-step variant? | No — this is not a relabel of T-S4H (which operates at S4a/S4b layer) or of the parent matching note (which operates at S1...S7 layer). The location/operator sub-decomposition and the `10⁻³⁴`-precision numerical match at v_EW are structurally new. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**
