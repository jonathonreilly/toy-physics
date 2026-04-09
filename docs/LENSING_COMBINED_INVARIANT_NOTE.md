# Lensing Combined Invariant — Phenomenological Fingerprint (Look Deeper)

**Date:** 2026-04-08
**Status:** retained POSITIVE (phenomenological) — combining all detected signals across the lensing lanes gives one coherent, continuum-stable, reproducible empirical power law at the reference configuration. It is NOT canonical 1/b lensing and NOT derivable from any ray-optics formula tried, but it IS the cleanest single characterization of the program's first-order gravitational response. Flagged **"look deeper at this"** — the mechanism is unknown and every attempt to derive it has been falsified, but the observable itself is sharp and stable.

## The combined invariant

At the reference configuration (Fam1 DAG, H=0.25, β=0.8, k·H=2.5, PW=6, T_phys=15, S=0.004, 2D 1/r field with mass at x_src=NL/3·H, z_src=b):

> **kubo_true(b) ≈ 28.4 · b^(−1.43)**,  b ∈ {3, 4, 5, 6}

Equivalently: kubo_true(3) = 5.986, with slope −1.4335 (R² = 0.998) on log-log.

## What each lane contributes

| Lane | Contribution | Status |
| --- | --- | --- |
| Lane α (Fam1 static Kubo) | **Magnitude anchor**: kubo_true(b=3) = +5.986 with 0.2% drift across H ∈ {0.5, 0.35, 0.25}; Fam3 agrees to 0.5% | continuum-stable ✓ |
| Lane L+ (fine-H lensing sweep) | **Slope**: −1.4335 with R² = 0.998 on b ∈ {3..6} at H=0.25 | sharp ✓ |
| Lane L++ (long-/short-path test) | **L-independence** at fine H: T=7.5 gives −1.44, T=15 gives −1.43, whole curve at T=15 is 2.4× uniform rescale of T=7.5 | invariant ✓ |
| Lane L# (β sweep) | Slope is **not** the narrow-beam ray limit; −1.43 is specific to β=0.8 | narrows the claim |
| Fermat ray-integral | **Falsified** (Lane L++) | ✗ |
| Finite-path deflection formula | **Falsified** (Lane L++) | ✗ |
| Narrow-beam asymptote | **Falsified** (Lane L# + H=0.35 sign flip) | ✗ |

## What the invariant is

- A reproducible, continuum-stable, configuration-specific empirical power law
- Anchored in magnitude (Lane α) and sharp in shape (Lane L+)
- Survives refinement to H=0.25 on the slope and H=0.25 on the magnitude
- Survives a path-length falsification test (slope the same at T=7.5 and T=15)
- Sign is correct: deflection toward the mass for all b in the tested range

## What the invariant is NOT

- NOT canonical 1/b weak-field gravitational lensing (slope ≠ −1)
- NOT any known finite-path ray-optics formula (all predict L-dependence, not observed)
- NOT the narrow-beam asymptote (β sweep shows no monotone approach to −1)
- NOT derivable from any of the three first-principles attempts made in this session
- NOT a universal law — slope varies strongly with (β, H, T, k); −1.43 is specific to the reference point
- −1.43 is not an obvious fraction: not −4/3, not −√2, not −3/2; no known physics constant

## Why "look deeper at this"

The observable is the sharpest, most stable gravity-side number the program has produced. Every attempt to derive it from ray optics has been falsified, which means the mechanism is genuinely wave-mechanical and not reducible to geometric deflection. The honest read is:

> The program has a clean but non-canonical gravitational fingerprint whose
> origin is unknown. It is reproducible, refinement-stable, and L-invariant,
> but does not match any textbook weak-field lensing law. It is a
> phenomenological invariant, not a derived law.

Three concrete deeper-look directions (queued, not attempted in this session):

1. **Analytical Kubo-over-propagator derivation.** Evaluate the Kubo formula `<z · ∂H/∂s>` directly over the propagator's wave-mechanical amplitude distribution (not a ray path). This is the correct first-principles calculation; it's harder than the Fermat integral but it's the one that might actually match.
2. **k (propagator coupling) sweep.** The phase per edge is `k·L·(1−f)`. If the slope is independent of k, the −1.43 is purely geometric in some deep sense. If it depends on k, it's a coupled wave-mechanical effect whose k-dependence would itself constrain the mechanism.
3. **Family sweep at the reference slope.** Lane α showed Fam1/Fam3 agree on the b=3 magnitude to 0.5%. Does the SLOPE also agree across families? If yes, −1.43 is a property of the propagator structure, not a family-specific coincidence.

None of these is in this note. They're flagged for the next dedicated pass.

## Retraction trail (for the record)

Four moonshot claims in the lensing lane were made and retracted in the preceding session day:

1. "Lane L matches 1/b lensing" — downgraded when H=0.25 steepened the slope to −1.43
2. "Finite-path Fermat formula matches at 1.5%" — falsified by L-independence at fine H
3. "L-independent −1.43 IS the physics" — true as observation, but not a derivation
4. "Canonical 1/b recovered at β=5" — falsified by denser β sampling + H=0.35 sign flip

The retained finding — this combined invariant — is what survives after all four retractions. It is less than a match to known physics but more than nothing: a specific, stable, falsifier-tested numerical prediction the program makes.

## Frontier map adjustment (Update 18)

| Row | Before | Combined invariant |
| --- | --- | --- |
| Gravity-side strongest observable | "clean power law slope ≈ −1.43 of unknown origin" | **kubo_true(b) ≈ 28.4·b^(−1.43), anchored, L-invariant, refinement-stable** |
| Derivation | "none survive" | **still none** — flagged for deeper analytical attempt |
| Next-action flag | "exhaust parameter-tweak lane" | **"look deeper" — three specific follow-ups queued** |

## Bottom line

> "Combining Lane α (magnitude anchor +5.986 at b=3, 0.2% drift),
> Lane L+ (slope −1.4335 at H=0.25, R² = 0.998), and Lane L++
> (L-independence: same slope at T=7.5 and T=15), the program's
> first-order Kubo response to a 2D 1/r field at the reference
> configuration is kubo_true(b) ≈ 28.4 · b^(−1.43) on b ∈ {3..6}.
> This is the cleanest, most stable gravity-side observable the
> program has produced: reproducible, continuum-stable, and
> L-invariant at fine refinement. It is NOT canonical 1/b lensing,
> NOT any finite-path ray formula, and NOT the narrow-beam
> asymptote — all three derivation attempts in this session were
> falsified. It is a phenomenological invariant whose mechanism
> remains unknown. Flagged 'look deeper' with three queued
> follow-ups: (a) analytical Kubo over the propagator amplitude
> distribution, (b) k (coupling) sweep, (c) family sweep of the
> slope across Fam1/Fam2/Fam3."
