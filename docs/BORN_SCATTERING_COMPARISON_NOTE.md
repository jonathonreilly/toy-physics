# Born/Eikonal Scattering Comparison with Lattice Lensing

**Date:** 2026-04-08 (originally); 2026-04-08 (updated same day with 3D corrections); 2026-05-10 (rigorize PATH B — bounded numerical observation demotion)
**Status:** bounded — bounded finite-run numerical comparison between a runner-computed plane-wave finite-path eikonal slope and an imported lattice slope, on a fixed parameter envelope (not a first-principles closure of the lattice lensing observable, not a derivation of the lattice slope, not a chain-closing theorem)
**Claim type:** bounded_theorem (bounded numerical observation only for the fixed-envelope runner-computed eikonal and Gaussian-beam slopes versus the imported lattice slope; not a positive theorem, not a closure of the grown-DAG lensing readout)
**Claim scope:** the runner-computed plane-wave eikonal slope is `−1.28` and the runner-computed 2D and 3D Gaussian-beam-corrected eikonal slopes are `−0.35` and `−0.77` respectively, all on the fixed envelope `L=15, x_src=5, β=0.8, b ∈ {3..6}`; the **lattice slope `−1.43` is an imported observational input** with retained authority cited below; the comparison is **diagnostic only**, not a first-principles closure of the lattice lensing observable, and not a derivation of either the lattice slope or the eikonal slope from the cited framework baseline.

## Rigorize-pass disposition (2026-05-10) — PATH B: bounded numerical observation

The 2026-05-05 audit verdict (`audited_numerical_match`, see
`docs/audit/data/audit_ledger.json`) explicitly recorded
`chain_closes: false` with the rationale that "the runner verifies the
plane-wave and 2D Gaussian computations, but the lattice measurement,
the 3D beam correction, and the physical identification of this
eikonal comparison with the grown-DAG observable are imported rather
than closed in the packet." The notes-for-re-audit field requested a
retained-grade lattice measurement, retained-grade 3D beam-correction
artifacts, and a bridge theorem identifying the finite-path eikonal
observable with the grown-DAG lensing readout — none of which are
available on the current retained surface.

The 2026-05-10 rigorize pass selects **PATH B**: this note is hereby
reframed as a **bounded numerical observation**, not a positive
theorem. The two PATH options at audit time were:

- **PATH A** (derive from first principles): close all three audit
  gaps (retained-grade lattice slope at the audited geometry,
  retained-grade 3D beam correction, and bridge theorem identifying
  the finite-path eikonal observable with the grown-DAG lensing
  readout). This is genuine theorem-level work; the audit explicitly
  rated this row "hard" with the reason that "closing it requires
  first-principles lattice/dispersion and 3D beam/L-independence
  derivations, not a small writeup or runner fix." This is **deferred
  to future work** as a separate retained promotion.
- **PATH B** (demote to bounded numerical observation): explicitly
  scope the runner output as a fixed-envelope numerical comparison
  with the imported lattice slope held as an observational input.
  This is the disposition selected by this rigorize pass.

The prior independent audit verdict on the old source hash was
`audited_numerical_match`. This source edit does not request or write a
new verdict; the generated audit pipeline owns the row status after this
claim-scope correction. PATH B simply makes the **claim scope** in this
note honest about what the runner verifies versus what is imported.

## Imported observational inputs (NOT derived in this packet)

The following inputs are **observational imports** held with retained
authority cited; they are NOT derived from the cited framework baseline in this
note:

- **Lattice slope `−1.43`** on `b ∈ {3..6}` — imported from the
  `gauss_lensing_*` lattice runners under
  [`scripts/`](../scripts/) and the dispersion-relation
  characterization. The retained-grade authority for this measurement
  remains
  [`DISPERSION_RELATION_NOTE.md`](DISPERSION_RELATION_NOTE.md), which
  is itself `audited_conditional` (Schrödinger ≈ Klein-Gordon on the
  grown DAG, R² Δ=0.002 — too close to distinguish). Until that note
  closes, the lattice slope `−1.43` retains its imported-observational
  character even where the comparison runner reports it.
- **Lattice configuration `L=15, x_src=5, β=0.8`** — imported as the
  fixed audit envelope from the directional-measure architecture
  (see
  [`ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md`](ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md),
  `audited_conditional`, where `β = 0.8` is itself recorded as
  **tuned support, not derived** per its 2026-05-10 PATH B
  disposition). The eikonal-slope comparison here is at this fixed
  point and is not claimed outside it.
- **Identification of the eikonal integral with the grown-DAG
  lensing readout** — the audit explicitly named this as
  not-closed-in-packet ("the physical identification of this
  eikonal comparison with the grown-DAG observable [is] imported
  rather than closed"). No bridge theorem is on the retained surface.

## What this note's runner DOES verify (under PATH B scope)

The runner [`scripts/gaussian_beam_eikonal.py`](../scripts/gaussian_beam_eikonal.py)
genuinely computes the following from chosen parameter values
`L=15, x_src=5, β=0.8, b ∈ {3..6}`:

- The plane-wave finite-path eikonal slope is **`−1.28`** (R² = 0.999).
- The 2D Gaussian-beam-corrected eikonal slope at `β = 0.8` is
  **`−0.35`**.
- The 3D Gaussian-beam-corrected eikonal slope at `β = 0.8` (with the
  `1/L²` kernel factor) is **`−0.77`**, per
  [`scripts/eikonal_3d_corrected.py`](../scripts/eikonal_3d_corrected.py).
- Among these three runner-computed eikonal predictions, **`−1.28`
  (plane-wave)** is numerically closest to the imported lattice slope
  `−1.43`, with `Δ = 0.15`.

The runner is not merely printing constants; it computes the finite-path
eikonal integral and the Gaussian-beam-averaged integral from the
formulas given below. The bounded numerical observation is precisely
this: AT the fixed envelope `(L=15, x_src=5, β=0.8, b ∈ {3..6})`, the
plane-wave eikonal slope `−1.28` is the closest of the three tested
runner-computed predictions to the imported lattice slope `−1.43`.

## What this note does NOT establish

- Not a derivation of the lattice slope `−1.43` from the cited framework baseline.
- Not a closure of the lattice lensing observable.
- Not a bridge theorem identifying the finite-path eikonal integral
  with the grown-DAG lensing readout (this remains an audit-named
  open gap).
- Not a parameter-independent claim outside the fixed audit envelope
  `(L=15, x_src=5, β=0.8, b ∈ {3..6})`.
- Not an explanation of the L-independence of the lattice
  measurement (the eikonal IS L-dependent; the lattice is NOT, at
  fine H — this remains unexplained).
- Not a determination of whether the 3D grown-DAG dispersion is
  Schrödinger or Klein-Gordon (the dispersion authority itself is
  `audited_conditional` with R² Δ=0.002 between forms).

## Future-work first-principles derivation target (deferred)

A retained promotion of this comparison to a chain-closing positive
theorem would require, per the audit's
`notes_for_re_audit_if_any` field, ALL of:

1. A retained-grade lattice measurement of the lensing slope on the
   grown DAG at the audited geometry (closing the dispersion
   authority dependency).
2. A retained-grade 3D beam-correction derivation that explains the
   Δ=0.15 residual without observable-tuning of `β`.
3. A bridge theorem identifying the finite-path eikonal integral
   with the grown-DAG lensing readout, including an explanation of
   the L-independence.

None of these are in scope for this PATH B rigorize pass. The audit
rated this work "hard" — closing all three is theorem-level effort
deferred to future work and would file as a separate retained note,
not a status change to this row.

## Context

The [dispersion relation measurement](DISPERSION_RELATION_NOTE.md) originally established Schrödinger on 2D lattice, but 3D follow-up showed **Schrödinger ≈ Klein-Gordon on the actual grown DAG** (R² Δ=0.002). The eikonal comparison is valid regardless of the dispersion type — it's a geometric-optics prediction for the deflection integral along a straight path through a 1/r potential.

## The prediction

For a non-relativistic particle on a straight path from x=0 to x=L, passing a 2D 1/r potential at (x_src, b), the eikonal deflection integral gives:

```
I_geom(b) = (1/b) · [(L-x_src)/√((L-x_src)²+b²) + x_src/√(x_src²+b²)]
```

At the lattice configuration (L=15, x_src=5):

| b | I_geom | local slope |
| ---: | ---: | ---: |
| 3 | 0.605 | — |
| 4 | 0.427 | −1.21 |
| 5 | 0.320 | −1.29 |
| 6 | 0.250 | −1.37 |

Power-law fit on b ∈ {3..6}: **I_geom ≈ 2.48 · b^(−1.28)**, R² = 0.999.

## Comparison

| Quantity | Eikonal prediction | Lattice measurement |
| --- | ---: | ---: |
| Slope on b ∈ {3..6} | −1.28 | −1.43 |
| Local slope at b=5→6 | −1.37 | ≈−1.43 |
| R² of power-law fit | 0.999 | 0.998 |
| Steepening with b? | Yes | Yes |
| L-dependent? | Yes (strongly) | **No** (Lane L++) |

## The discrepancy (open-gap diagnosis, NOT explained in this packet)

The slope difference `Δ = 0.15` between the runner-computed plane-wave
eikonal slope and the imported lattice slope is **not explained** by
any correction tested in this note. Three candidate explanations were
considered, none of which the runner closes:

1. **Gaussian beam profile (TESTED AND FALSIFIED below)**: A Gaussian
   angular weight `exp(−β·θ²)` on the eikonal integral was tested in
   both 2D and 3D forms at `β = 0.8`; both **worsen** the match
   (`Δ = 1.08` and `Δ = 0.66` respectively, see the Beam-averaging
   table). The β sweep does show the slope crosses `−1.43` at large
   `β ≈ 10–20`, but at the audited `β = 0.8` the beam correction is
   not in the right direction. The 2026-04-08 note text previously
   asserted "β = 0.8 provides the specific correction that shifts
   −1.28 → −1.43"; that earlier claim is **withdrawn** by this
   PATH B pass — the runner output above refutes it.

2. **Wave-mechanical corrections (NOT TESTED HERE)**: The eikonal is
   a classical-path approximation; diffraction corrections of order
   `λ/b` would modify the slope. No retained-grade derivation of the
   relevant `λ` (which presumes a closed dispersion relation) is on
   the surface in this packet, and no runner test is provided.

3. **L-independence (UNEXPLAINED)**: The finite-path eikonal formula
   used here IS strongly `L`-dependent, while the lattice measurement
   is `L`-independent at fine `H`. This packet does not derive an
   `L`-independent observable; it is one of the three explicit
   audit-named open gaps deferred to future-work retained promotion.

## Interpretation (under PATH B scope — diagnostic only, no structural claim)

Under PATH B, this note offers **no structural interpretation** of
why the runner-computed plane-wave slope happens to land closer to
the imported lattice slope than the beam-corrected variants tested.
The earlier "right functional form" / "wave-mechanical effect"
language is **withdrawn**; it overclaimed a structural mechanism
that the runner does not establish. The remaining bounded statement
is just the numerical observation in 'What this bounded numerical
observation establishes' below.

## Beam-averaging corrections (BOTH TESTED AND FALSIFIED)

The queued follow-up was to compute beam-corrected eikonals. Both 2D and 3D beam corrections were tested and both **WORSEN** the match:

| Model | Slope | Δ from −1.43 | Status |
| --- | ---: | ---: | --- |
| Plane-wave (single ray) | −1.28 | 0.15 | **BEST** |
| 2D beam average (β=0.8) | −0.35 | 1.08 | Falsified |
| 3D beam average (β=0.8, 1/L²) | −0.77 | 0.66 | Falsified |
| Canonical 1/b | −1.00 | 0.43 | Wrong |
| Lattice measurement | −1.43 | 0.00 | Target |

Scripts: [`gaussian_beam_eikonal.py`](../scripts/gaussian_beam_eikonal.py), [`eikonal_3d_corrected.py`](../scripts/eikonal_3d_corrected.py)

**Why beam averaging fails:** At β=0.8, the beam width at the source position is σ_z ≈ 3.5–4.0, comparable to the impact parameters b ∈ {3..6}. Averaging over this wide beam smears out the 1/b structure, flattening the slope. The 3D correction (1/L² kernel factor) tightens the beam slightly (σ_z: 3.95 → 3.54) but not enough.

## What this bounded numerical observation establishes (under PATH B scope)

- AT the fixed envelope `(L=15, x_src=5, β=0.8, b ∈ {3..6})`, the
  runner-computed plane-wave finite-path eikonal slope is `−1.28`,
  numerically closer to the imported lattice slope `−1.43`
  (`Δ = 0.15`) than the runner-computed 2D and 3D Gaussian-beam
  corrections at `β = 0.8` (`Δ = 1.08` and `Δ = 0.66` respectively).
- The picture remains **INCOMPLETE** as a first-principles closure:
  the `Δ = 0.15` gap and the lattice L-independence are unexplained
  by any correction tested in this packet, and the bridge to the
  grown-DAG lensing readout is not derived here.
- The original "non-relativistic" framing does not transfer
  cleanly: the grown-DAG dispersion is too close to distinguish
  Schrödinger from Klein-Gordon (R² Δ=0.002).

## Bottom line (bounded numerical observation)

> "Under PATH B (bounded numerical observation, 2026-05-10 rigorize
> pass): AT the fixed envelope `(L=15, x_src=5, β=0.8, b ∈ {3..6})`,
> the runner-computed plane-wave finite-path eikonal slope is `−1.28`,
> numerically closer to the imported lattice slope `−1.43` (`Δ = 0.15`)
> than the runner-computed 2D and 3D Gaussian-beam-corrected eikonal
> slopes at `β = 0.8` (`−0.35` and `−0.77`, with `Δ = 1.08` and
> `Δ = 0.66` respectively). The lattice slope is an **imported
> observational input** (retained-grade authority pending dispersion
> closure); the comparison is **diagnostic only**, not a
> first-principles closure of the lattice lensing observable. The
> `Δ = 0.15` residual, the L-independence, and the identification of
> the finite-path eikonal integral with the grown-DAG lensing
> readout are explicit audit-named open gaps and are deferred to a
> future-work retained promotion (see 'Future-work first-principles
> derivation target' above)."
