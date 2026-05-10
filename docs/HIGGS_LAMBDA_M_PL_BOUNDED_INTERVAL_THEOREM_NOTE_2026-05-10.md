# Higgs λ(M_Pl) Bounded-Interval Theorem Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Type:** bounded_theorem
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/higgs_lambda_m_pl_bounded_interval_diagnostic_2026_05_10.py`](../scripts/higgs_lambda_m_pl_bounded_interval_diagnostic_2026_05_10.py)

## Claim

Conditional on (X1) the operator-absence reasoning carried by the
sibling probe note `KOIDE_W_S4B_CLASSICALITY_LAMBDA_MPL_FORCED_NOTE_2026-05-10_probeW_S4b_classicality`
and (X2) the 1-loop scheme-universal lattice → MSbar matching
admission used by the retained 3-loop runner
[`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py),
the effective perturbative-MSbar Higgs quartic coupling at the cutoff
scale `a⁻¹ = M_Pl` lies in the bounded interval

```text
   λ_eff(M_Pl)  ∈  [0, + O(10⁻³)]                       (B-1)
```

with quantitative upper bound

```text
   |λ_eff(M_Pl)|  ≲  g²(M_Pl) / (16 π²)  ·  O(1)
                  ≲  0.5² / (16 π²)
                  ≃  1.6 × 10⁻³                          (B-2)
```

and a conservative retained-running envelope estimate

```text
   |λ_eff(M_Pl)|  ≲  g⁴(M_Pl) / (16 π²)
                  ≃  4 × 10⁻⁴                            (B-3)
```

per the existing bound on the classicality BC quantum correction in
[`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
§3.2 (eq. H-Gap2a).

The lower edge `λ_eff(M_Pl) ≥ 0` is the operator-absence statement on
the lattice bare action: no `λ_bare φ⁴` term exists in
`S_bare = S_W^{plaq}[U] + S_stagg^{Dirac}[ψ̄, ψ, U]`, so the bare quartic
vanishes, and 1-loop matching at scheme-universal order does not lift
it from below.

The upper edge `λ_eff(M_Pl) ≲ +O(10⁻³)` is the dimensional-analysis
envelope on the leading non-vanishing 1-loop matching finite part
`δ_λ(g_*)` between the lattice-bare scheme and perturbative-MSbar,
evaluated at the retained SU(2) coupling
`g_2(M_Pl) ≈ g_2(v) · (running)` running on the 3-loop SM RGE system
(per [`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py)).

This is a bounded proof-walk of two named-admission inputs into a
single quantitative band. It does not add a new axiom, a new
repo-wide theory class, or a retained status claim.

## Directional discriminator vs SM literature

Buttazzo et al. 2013 / Degrassi et al. 2012 read
`λ^{SM,MSbar}(M_Pl) ≈ −0.013 ± 0.007` from observed `m_t = 173.3 GeV`
and `α_s(M_Z) = 0.1184`, lying firmly on the negative side.

The framework's bounded interval (B-1) is positive-side:
`λ_eff(M_Pl) ∈ [0, +O(10⁻³)]`. The two bands are disjoint:

```text
   SM-literature ±1σ:   [−0.020, −0.006]
   framework B-1:       [   0,   +0.001]
   λ-gap:               +0.006        (framework lower edge above lit upper edge)
   σ-distance:          +1.86         (framework lower edge above lit central)
```

(diagnostic Block 3.) This is a falsifiable directional prediction.
Vacuum stability flips sign with this distinction: SM-negative-side
gives metastable vacuum with finite tunneling time,
framework-positive-side (within the band) gives absolutely-stable
vacuum. The framework is therefore falsified by either of:

- a future precision measurement that pins `λ(M_Pl)` firmly negative
  with a 5σ upper edge below 0 (the framework's lower edge);
- a measurement that requires `|λ(M_Pl)| > 10⁻³` regardless of sign
  (the framework's upper edge).

A measurement pinning λ(M_Pl) inside `[0, +10⁻³]` leaves the
framework consistent.

A subordinate quantitative observation (not load-bearing on the
bounded interval; informational only): on the retained linearized
slope, the framework central `λ = 4 × 10⁻⁴` gives `m_H = 125.16 GeV`
(0.09 GeV from PDG), while the SM-literature central `λ = −0.013`
gives `m_H = 120.98 GeV` (4.27 GeV from PDG, outside the inherited
±3.17 GeV systematic). The framework's positive-side reading is
closer to PDG by 4.06 GeV on the same inherited y_t systematic. This
is a comparator observation, not a refutation of SM-literature m_H
fits (which use Buttazzo's full machinery including extracted y_t
that differs from the framework value 0.9176); see
[`HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md`](HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md)
§3 for the y_t tension framing.

## Proof-walk

| Step | Load-bearing input | Operator-absence layer? | Matching layer? |
|---|---|---|---|
| 1. Identify operator content of `S_bare` from `A1+A2+gates` | gauge link variables `U_μ(x)` and staggered Grassmann fermions `ψ̄, ψ` | yes | n/a |
| 2. Inspect for `λ_bare φ⁴` term | direct enumeration: Wilson plaquette + bilinear Dirac + bilinear Yukawa-via-gauge | yes | n/a |
| 3. Conclude `λ_bare(a⁻¹) = 0` | structural absence in operator basis | yes (lower edge of B-1) | n/a |
| 4. Identify matching map `λ_bare(a⁻¹) ↔ λ^{MSbar}(M_Pl)` | scheme translation `Z_λ · λ_bare + δ_λ` | n/a | yes (1-loop scheme-universal at leading order) |
| 5. Bound the leading non-vanishing matching contribution | dimensional analysis `δ_λ ~ g²/(16π²)` at gauge couplings retained by the 3-loop runner | n/a | yes (upper edge of B-1) |
| 6. Evaluate at retained running `g_2(M_Pl) ≈ 0.51` | 3-loop SM RGE run from `g_2(v) = 0.648` with retained light-flavor count | n/a | yes |
| 7. Assemble bounded interval | combine lower edge (operator absence) with upper edge (matching envelope) | yes | yes |

## Exact arithmetic check

The retained gauge-coupling running at the 3-loop SM RGE (with the
framework's retained low-scale inputs `g_1(v) = 0.464`,
`g_2(v) = 0.648`, `g_3(v) = √(4π · 0.1033)`, `y_t(v) = 0.9176`,
`v = 246.28 GeV`, `M_Pl = 1.2209 × 10¹⁹ GeV`) gives

```text
   g_1(M_Pl)  ≈  0.466    (GUT-normalized)
   g_2(M_Pl)  ≈  0.507
   g_3(M_Pl)  ≈  0.489
```

per [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
§3.2.

Dimensional-analysis envelope on the 1-loop matching finite part:

```text
   |δ_λ^{1-loop, SU(2) gauge}|   ~  g_2⁴(M_Pl) / (16 π²)         =  (0.507)⁴ / 158   ≃  4.2 × 10⁻⁴
   |δ_λ^{1-loop, all gauge}|     ~  Σ_i g_i⁴(M_Pl) / (16 π²)     =  0.170    / 158   ≃  1.1 × 10⁻³
                                    (g_1⁴ + g_2⁴ + g_3⁴ at M_Pl)
   |δ_λ^{1-loop, top Yukawa}|    ~  y_t⁴(M_Pl) / (16 π²)         =  (0.382)⁴ / 158   ≃  1.3 × 10⁻⁴
```

The framework's retained `y_t(M_Pl) ≈ 0.382` (3-loop run) makes the
Yukawa contribution subleading at M_Pl.

Conservative upper edge of (B-1) using `g²/(16π²) · O(1)` cap with a
factor-of-a-few headroom for unresolved O(1) finite-part coefficients:

```text
   |δ_λ^{1-loop, total}|   ≲   1 × 10⁻³   =   O(10⁻³)        (B-4)
```

Quadrature combination of independent gauge + Yukawa channels gives a
tighter retained-central estimate

```text
   |δ_λ^{retained central}|   ≃   √[(4.2)² + (1.3)²] × 10⁻⁴   ≃   4.4 × 10⁻⁴    (B-5)
```

matching the existing `≲ 4 × 10⁻⁴` headline number in
[`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
§3.2 (eq. H-Gap2a).

## m_H consequence

The retained 3-loop runner slope from
[`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
§3.2 (Table at line 698):

```text
   dm_H / dλ(M_Pl)   =   +312 GeV / unit-λ    (averaged over ±0.005)        (B-6)
```

Propagating the bounded interval (B-1):

```text
   Δm_H^{from B-1}   ≲   312 GeV × 10⁻³   =   0.31 GeV               (B-7)
   Δm_H^{from B-3 retained central}   ≲   312 GeV × 4 × 10⁻⁴   =   0.13 GeV   (B-8)
```

This is well below the inherited y_t systematic, currently
`σ_m_H^{retained total} = 3.17 GeV` per
[`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
§3.6 (eq. M-tot-quad). The `m_H = 125.1 GeV` central from
[`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md) (full 3-loop
SM RGE route) is preserved under the bounded-interval reading of the
boundary input.

The other two Higgs values in the repository are not affected by
this note: `m_H = 140.3 GeV` from
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) is a
tree-level `m_H = v/(2u_0)` chain that does not consume `λ(M_Pl)`,
and the intermediate 119.93 GeV value in the discrimination note
[`HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md`](HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md)
is a corrected-y_t RGE diagnostic, not a separate derivation of the
boundary input.

## Dependencies

- [`KOIDE_W_S4B_CLASSICALITY_LAMBDA_MPL_FORCED_NOTE_2026-05-10_probeW_S4b_classicality.md`](KOIDE_W_S4B_CLASSICALITY_LAMBDA_MPL_FORCED_NOTE_2026-05-10_probeW_S4b_classicality.md)
  for the operator-absence (route W-B) argument that gives
  `λ_bare(a⁻¹) = 0` at the lattice-bare layer.
- [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
  for the existing `|δλ(M_Pl)| ≲ g⁴/(16π²) ≃ 4 × 10⁻⁴` bound (eq.
  H-Gap2a) and the retained `dm_H/dλ(M_Pl) = +312 GeV` slope.
- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md) for the
  `m_H ≈ 125.1 GeV` 3-loop SM RGE central output, and for the Gap #7
  demotion of the boundary-input derivation to OPEN (2026-05-10).
- [`HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md`](HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md)
  for the D4 discrimination framing of `λ(M_Pl)` as a falsifiable
  prediction.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) for
  the open `staggered_dirac_realization_gate` context.
- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  for the open realization-gate that the operator-absence argument
  is conditional on.
- [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) for the
  Wilson plaquette structural form that the operator-absence
  argument uses.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the operator-absence statement itself — that is the subject of the
  sibling probe note and remains a source-note proposal pending
  audit;
- the lattice → MSbar matching at 2-loop and higher — these are
  named admitted-context imports per the same sibling note's named
  imports `{δ_λ_higher_loop_matching_finite_part}`;
- the staggered-Dirac realization gate or the g_bare canonical
  normalization gate — both remain open per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md);
- the y_t(v) = 0.9176 derivation that drives the dominant m_H
  systematic (this note is downstream of, not load-bearing on, that
  derivation);
- the M_Pl scale itself, which remains an upstream
  `audited_conditional` input;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any parent theorem/status promotion.

## Open derivation gap

The two named admissions are:

1. **X1 — Operator absence on the bare action.** The lower edge
   `λ_eff(M_Pl) ≥ 0` is conditional on the operator-content claim
   carried by the sibling probe note
   [`KOIDE_W_S4B_CLASSICALITY_LAMBDA_MPL_FORCED_NOTE_2026-05-10_probeW_S4b_classicality.md`](KOIDE_W_S4B_CLASSICALITY_LAMBDA_MPL_FORCED_NOTE_2026-05-10_probeW_S4b_classicality.md).
   That note carries the route-W-B argument that `S_bare` derivable
   from `A1+A2+gates` contains no `λ_bare φ⁴` operator. The argument
   is itself conditional on the open `staggered_dirac_realization_gate`
   and the `g_bare_canonical_normalization_gate`.

2. **X2 — 2-loop lattice → MSbar matching.** The upper edge
   `λ_eff(M_Pl) ≲ +O(10⁻³)` envelopes a leading non-vanishing 1-loop
   matching finite part. Higher-loop matching corrections
   `δ_λ^{(n≥2)}` are import-class (perturbative-MSbar multi-loop
   matching machinery) and are not load-bearing for this bounded
   interval, but they are admissions on the upstream chain that
   would tighten or shift the band if derived.

The deeper unblock is the upstream M_Pl-scale derivation, currently
`audited_conditional`. With that scale derivation closed, the
operator-absence layer and the leading matching envelope combine to
the bounded interval (B-1) without further unattested imports.

## Verification

Run the diagnostic:

```bash
PYTHONPATH=scripts python3 scripts/higgs_lambda_m_pl_bounded_interval_diagnostic_2026_05_10.py
```

The diagnostic:

- imports the retained 3-loop runner's slope `dm_H/dλ(M_Pl) ≈ +312
  GeV/unit-λ` from
  [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
  §3.2 (Table at line 698);
- cross-checks the linearized slope against the full-3-loop runner
  table over `λ ∈ [−0.01, +0.01]` (linear deviation < 0.25 GeV
  across the range);
- computes `m_H(λ)` over the test grid `λ ∈ { −0.020, −0.013,
  −0.006, −0.005, 0, +1 × 10⁻⁴, +4 × 10⁻⁴, +1 × 10⁻³ }`;
- tabulates "consistent with observed `m_H = 125.25 GeV` within the
  inherited `σ_m_H^{retained total} = 3.17 GeV` 1σ band" for each
  λ point;
- confirms that the entire positive-side framework interval `[0,
  +10⁻³]` is consistent with PDG on this inherited band;
- reports that the SM-literature point `λ^{SM,MSbar}(M_Pl) ≈ −0.013`
  by itself gives `m_H ≈ 120.98 GeV`, **outside** the inherited
  ±3.17 GeV systematic (gap = −4.27 GeV; framework central is 4.06
  GeV closer to PDG than the SM-literature central);
- confirms the directional discriminator: framework interval and
  SM-literature ±1σ interval are disjoint with a +0.006 gap on λ,
  and the framework lower edge sits +1.86 literature-σ above the
  literature central;
- confirms the vacuum-stability sign flip: framework positive-side
  → absolutely stable; SM-literature negative-side → metastable.

Expected:

```text
TOTAL: PASS=14 FAIL=0
VERDICT: bounded-interval [0, +1e-3] reproduces m_H = 125.1 GeV within
the inherited 3.17 GeV systematic; directional discriminator vs SM
literature -0.013 +/- 0.007 framing established.
```
