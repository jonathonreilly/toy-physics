# Wilson m_H Per-Channel Closure Values — Bounded Note

**Date:** 2026-05-09
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived after audit ratification and dependency closure.
**Primary runner:** [`scripts/frontier_wilson_m_h_per_channel_closure.py`](../scripts/frontier_wilson_m_h_per_channel_closure.py)

## Claim

The all-orders Wilson-corrected `(m_H_W / v)^2` closed form derived in
[`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md)
under the parent's uniform-`N_taste = 16` channel admission is

```text
( m_H_W / v )^2  =  ( 1 / 64 ) · Σ_{k=0}^{4}  binomial(4, k) ·
   ( u_0^2 - ( k - 2 )^2 r^2 )  /  ( ( k - 2 )^2 r^2 + u_0^2 )^2,        (uniform-16)
```

with closure value `r ≈ 0.26855` against the comparison input
`(m_H_PDG / v)^2`. The uniform-`N_taste = 16` admission is one specific
channel identification: the parent
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) treats
the 16 BZ corners of `Z^3 + t` APBC at `L = 2` as one Higgs-mass
channel, summing the curvature contributions of every Hamming-weight
class `k ∈ {0, 1, 2, 3, 4}` (multiplicities `binomial(4, k) = (1, 4, 6,
4, 1)`).

This bounded note records, at exact rational precision, the closure
value of the Wilson coefficient `r` for each of the alternative
single-class and class-pair channel identifications, and reports the
boundary at which the closure mechanism breaks. Each per-channel
identification chooses an effective `N_taste^(eff) = Σ_{k ∈ S}
binomial(4, k)` and reads the per-channel curvature as

```text
( m_H_W / v )^2_{(S)}
   =  ( 1 / ( 4 · N_taste^(eff)(S) ) ) · Σ_{k ∈ S}  binomial(4, k) ·
        ( u_0^2 - ( k - 2 )^2 r^2 ) /  ( ( k - 2 )^2 r^2 + u_0^2 )^2.       (S)
```

(This is the per-channel readout: total magnitude of the curvature on
the chosen subset divided by the effective channel count, mirroring the
parent's `( 4 / u_0^2 ) / N_taste` per-channel rule at `r = 0`.)

The four identifications named in the prompt give:

```text
S = {2}        :  ( m_H_W / v )^2  =  1 / ( 4 u_0^2 )                      (k2-only)
                                  =  CONSTANT in r;  no closure to TARGET

S = {0, 4}     :  ( m_H_W / v )^2  =  ( u_0^2 - 4 r^2 )
                                       /  ( 4 · ( 4 r^2 + u_0^2 )^2 )      (k04)
                  closure r_{0,4}  ≈  0.12192   ± 10^{-5}

S = {1, 3}     :  ( m_H_W / v )^2  =  ( u_0^2 - r^2 )
                                       /  ( 4 · ( r^2 + u_0^2 )^2 )        (k13)
                  closure r_{1,3}  ≈  0.24383   ± 10^{-5}

S = {0..4}     :  uniform-16 (above);  closure r_{16}  ≈  0.26855  ± 10^{-5}
```

with canonical surface values `u_0 = 0.8776`, `v = 246.22 GeV`, and
`m_H_PDG = 125.10 GeV` (used as comparison input only, **not load-
bearing** for derivation; see Boundaries).

The `k = 2`-only result is r-independent because the Wilson factor
`(k - 2)^2` vanishes at `k = 2`, which makes both the per-summand
shift and the per-summand denominator-shift zero. The closure
mechanism therefore breaks for the `k = 2`-only identification: no
choice of `r` can move the readout away from the parent value
`1 / (4 u_0^2) = (m_H_zero / v)^2 ≈ 0.32460`, and the +12 % gap
to `(m_H_PDG / v)^2 ≈ 0.25815` is **not** closed in this channel.

The `k = 0, 4` and `k = 1, 3` paired-class identifications close
against the comparison input at the smaller values `r_{0,4} ≈ 0.12192`
and `r_{1,3} ≈ 0.24383`, respectively. Note that
`r_{1,3} ≈ 2 · r_{0,4}`: this is a consequence of the rescaling
`(k - 2)^2 r^2 → r'^2` with `r' = 2 r` for the `k = 0, 4`
class-pair (where `(k - 2)^2 = 4`) versus the `k = 1, 3` pair
(where `(k - 2)^2 = 1`); the per-class-pair rational structures are
therefore identical functions of the rescaled coupling. The runner
verifies this rescaling identity directly.

This note records the per-channel closure values. It does **not**
close the +12 % Higgs gap chain. None of the closure values
`{r_{0,4}, r_{1,3}, r_{16}}` is a derived value of the Wilson
coefficient `r`; each is a comparison-input matching value
**conditional** on:
1. its respective channel identification (single-class, paired-class,
   or uniform-16; **non-derived**);
2. the curvature-on-subset per-channel rule (eq. `(S)`; **non-
   derived**, distinct from the channel-boundary note's alternative
   substitute-into-parent-eq. `[5]` convention; see Dependencies);
3. the tree-level mean-field formalism (no CW corrections, no RGE
   running);
4. a non-zero Wilson coefficient `r`, **not** part of the canonical
   pure-Kogut-Susskind staggered setup.

Any of (1)–(4) failing voids the per-channel matching readouts.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Total Wilson curvature at `m^* = -4 r` from the all-orders note: `(1/4) Σ_k binomial(4,k) · ((k-2)^2 r^2 - u_0^2)/((k-2)^2 r^2 + u_0^2)^2` (eq. (1) of the all-orders note) | upstream [`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md) | no |
| Per-channel rule from parent eq. `[4]`: pick a subset `S ⊆ {0..4}` of Hamming-weight classes; `N_taste^(eff)(S) = Σ_{k ∈ S} binomial(4, k)`; `(m_H_W/v)^2 = |total curvature on S| / N_taste^(eff)(S)` | parent admission + admitted subset | no |
| Sign flip: total curvature is negative (tachyonic); magnitude per-summand is `binomial(4,k) · (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2` | algebraic sign | no |
| Resulting per-channel formula (S): `(m_H_W/v)^2_{(S)} = (1/(4·N_taste^(eff)(S))) · Σ_{k ∈ S} binomial(4,k) · (u_0^2 - (k-2)^2 r^2) / ((k-2)^2 r^2 + u_0^2)^2` | direct substitution | no |
| Reduction at `r = 0` for any non-empty `S`: each summand `→ binomial(4,k)/u_0^2`; sum `→ N_taste^(eff)(S)/u_0^2`; divide by `4·N_taste^(eff)(S)` `→ 1/(4 u_0^2)`; matches parent eq. `[5]` for every choice of `S`. The choice of `S` only matters at non-zero `r` | algebraic | no |
| `S = {2}` specialization: only `k = 2` summand, with `(k-2)^2 = 0`, so `x = 0` for all `r`; numerator `u_0^2 - 0 = u_0^2`; denominator `(0 + u_0^2)^2 = u_0^4`; summand `= 6 / u_0^2`; divide by `4 · 6 = 24` gives `1/(4 u_0^2)`. **r-independent** | algebraic; `(k - 2)^2` vanishes at `k = 2` | no |
| Consequence: `S = {2}` does **not** close. The Wilson-shift mechanism vanishes identically for the central Hamming-weight class; no value of `r` moves the readout away from the parent value | algebraic | no |
| `S = {0, 4}` specialization: both summands have `(k-2)^2 = 4` and `binomial(4,k) = 1`, so combined numerator `= 2 (u_0^2 - 4 r^2)`, combined denominator factor `= (4 r^2 + u_0^2)^2`; `N_taste^(eff) = 2`; readout `= (u_0^2 - 4 r^2) / (4 · (4 r^2 + u_0^2)^2)` | algebraic | no |
| `S = {0, 4}` matching equation: set readout equal to `(m_H_PDG / v)^2` (comparison input only); bisect in `Fraction` on bracket `[0.12, 0.14]` (`f(0.12) > 0`, `f(0.14) < 0` verified) until width `≤ 10^{-5}`. Result: `r_{0,4} ≈ 0.12192` | exact-rational bisection | no |
| `S = {1, 3}` specialization: both summands have `(k-2)^2 = 1` and `binomial(4,k) = 4`, so combined numerator `= 8 (u_0^2 - r^2)`, combined denominator factor `= (r^2 + u_0^2)^2`; `N_taste^(eff) = 8`; readout `= (u_0^2 - r^2) / (4 · (r^2 + u_0^2)^2)` | algebraic | no |
| `S = {1, 3}` matching equation: bisect on bracket `[0.22, 0.25]` (`f(0.22) > 0`, `f(0.25) < 0` verified) until width `≤ 10^{-5}`. Result: `r_{1,3} ≈ 0.24383` | exact-rational bisection | no |
| Rescaling identity: comparing the `S = {0, 4}` readout against the `S = {1, 3}` readout, the substitution `r → 2 r` maps `(0, 4)` onto `(1, 3)` exactly (since `4 r^2 = (2 r)^2 · 1`). Therefore `r_{1,3} = 2 · r_{0,4}` exactly at the algebraic-equation level (the runner verifies this to bisection precision: `|r_{1,3} - 2 · r_{0,4}| < 10^{-5}`) | algebraic substitution | no |
| `S = {0..4}` reference: matches the all-orders note value `r_{16} ≈ 0.26855` | upstream note + bisection cross-check | no |
| Comparison of all four readouts at `r = 0`: every identification reproduces `(m_H_zero / v)^2 = 1/(4 u_0^2)` exactly; the four identifications differ only in their response to non-zero `r` | algebraic | no |
| Validity boundaries: each per-channel readout's perturbative-Taylor radius is set by its dominant `(k - 2)^2`; for `S = {0, 4}` the boundary is `r < u_0 / 2`, for `S = {1, 3}` it is `r < u_0`; closure values `r_{0,4} ≈ 0.122` and `r_{1,3} ≈ 0.244` lie at the same dimensionless ratio `r / boundary ≈ 0.278`, well within the convergence radius of each | scalar comparison | no |

Every load-bearing step is exact-rational arithmetic, scalar calculus
on a known closed form, or `Fraction` bisection. The Wilson plaquette
form, staggered phases, link unitaries, and lattice scale `a` do not
appear as load-bearing inputs to the per-channel closure values.

## Exact Arithmetic Check

The runner verifies, at exact rational precision via
`fractions.Fraction`:

(A) **Per-channel formulas at `r = 0` reduce to parent.** For each
`S ∈ { {2}, {0, 4}, {1, 3}, {0..4} }`, the per-channel readout
evaluates to `1 / (4 u_0^2)` exactly at `r = 0`, matching parent eq.
`[5]`.

(B) **`S = {2}` is r-independent.** Direct evaluation of the
`k = 2`-only readout at several `r` values (`0, 0.1, 0.2, 0.3, 0.4`)
gives the same value `1 / (4 u_0^2)` exactly. The Wilson shift
mechanism vanishes for this single-class identification.

(C) **`S = {2}` does not close to the comparison target.** The
constant readout `1 / (4 u_0^2) ≈ 0.32460` does not equal
`(m_H_PDG / v)^2 ≈ 0.25815` at any `r`; the gap `+0.06645` is the
canonical `+12 %` Higgs-mass gap unmoved by Wilson in this
identification.

(D) **`S = {0, 4}` bisection.** Solve `(m_H_W / v)^2_{(0, 4)}
= (m_H_PDG / v)^2` by bisection in `Fraction` arithmetic on bracket
`[0.12, 0.14]`. Bracket endpoints verified opposite-sign: `f(0.12) >
0`, `f(0.14) < 0`. Bisect until bracket width `≤ 10^{-5}`. Result:
`r_{0,4} ∈ [0.12191, 0.12193]`, i.e. `0.12192 ± 10^{-5}`.

(E) **`S = {1, 3}` bisection.** Solve `(m_H_W / v)^2_{(1, 3)}
= (m_H_PDG / v)^2` by bisection in `Fraction` arithmetic on bracket
`[0.22, 0.25]`. Bracket endpoints verified opposite-sign: `f(0.22) >
0`, `f(0.25) < 0`. Bisect until bracket width `≤ 10^{-5}`. Result:
`r_{1,3} ∈ [0.24382, 0.24384]`, i.e. `0.24383 ± 10^{-5}`.

(F) **Rescaling identity.** The `(0, 4)` and `(1, 3)` readouts are
related by `r → 2 r`: the runner checks
`|r_{1,3} - 2 · r_{0,4}| < 10^{-5}` directly, confirming the
algebraic-substitution identity at bisection precision.

(G) **Uniform-16 cross-check.** Re-bisecting the `S = {0..4}` form on
bracket `[0.26, 0.28]` reproduces `r_{16} ≈ 0.26855`, matching the
all-orders note value to bisection precision.

(H) **Per-channel ordering.** The four closure values satisfy
`r_{0,4} < r_{1,3} < r_{16}` (no closure for `S = {2}`), reflecting
that identifications with smaller dominant `(k - 2)^2` need a larger
matching `r`.

(I) **Validity-boundary check.** For each closure value, the runner
verifies the dimensionless ratio `r / boundary < 1`: for
`S = {0, 4}`, `r_{0,4} / (u_0 / 2) ≈ 0.278`; for
`S = {1, 3}`, `r_{1,3} / u_0 ≈ 0.278`; for
`S = {0..4}`, `r_{16} / (u_0 / 2) ≈ 0.612`. All four lie within the
perturbative-Taylor convergence radius of their respective forms.

## Dependencies

- [`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md)
  for the all-orders Wilson curvature at `m^* = -4 r` and the
  uniform-16 reference value `r_{16} ≈ 0.26855`.
- [`WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
  for the exact curvature at `m^* = -4 r`.
- [`WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`](WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md)
  for the `V_taste^W` formula.
- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the staircase multiplicities `binomial(4, k) = (1, 4, 6, 4, 1)`
  on the 16 BZ corners.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) for
  the parent tree-level setup, eqs. `[3]–[6]`, the `(m_H/v)^2 =
  curvature / N_taste` per-channel readout rule, and the uniform-
  `N_taste = 16` admission.
- [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  for the boundary statement that the uniform-`N_taste = 16` choice
  is itself a non-derived admission. The channel-boundary note uses a
  different
  per-channel rule at `r = 0` (it substitutes `N_taste^(eff)` directly
  into parent eq. `[5]` keeping the full-lattice total `4 / u_0^2`,
  giving `r = 0` values 561.1, 280.6, 229.1, 280.6, 561.1 GeV for
  single-class `k = 0, 1, 2, 3, 4`). This note instead uses the
  curvature-on-subset rule (eq. `(S)` above), which collapses to the
  parent's `1 / (4 u_0^2)` at `r = 0` for every non-empty `S`. Both
  rules inherit the same parent-admission status; the choice between
  them is not derived by either note. This note follows the
  curvature-on-subset convention because that is the convention under
  which the all-orders note `WILSON_M_H_TREE_AT_EXTREMUM_ALL_
  ORDERS_BOUNDED_NOTE_2026-05-08` derives the uniform-16 closure
  `r_{16} ≈ 0.26855`, and this note's S-dependent values are the
  natural per-`S` extension of that closure equation.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  for the staggered-Dirac realization-gate context.
- `MINIMAL_AXIOMS_2026-05-03.md` for
  the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the +12 % Higgs gap chain in
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md). The
  per-channel matching values `r_{0,4}, r_{1,3}, r_{16}` are
  **conditional** on:
  1. the chosen channel identification (which subset `S` of the
     Hamming-weight classes is identified with the Higgs; **non-
     derived**);
  2. the curvature-on-subset per-channel rule used for the readout
     (eq. `(S)` above; **non-derived**, see the channel-boundary note's
     alternative substitute-into-parent-eq.[5] convention in
     Dependencies);
  3. the tree-level mean-field formalism (no CW corrections, no RGE
     running);
  4. a non-zero Wilson coefficient `r`, **not** part of the canonical
     pure-Kogut-Susskind staggered setup.
  Any of (1)–(4) failing voids the matching readouts;
- the Higgs-channel assignment itself: this note enumerates four
  candidate identifications (`{2}`, `{0, 4}`, `{1, 3}`, `{0..4}`) but
  does not select one. Whether a single-class, paired-class, or
  uniform-16 identification is the physically correct one is **not**
  resolved here; the parent admits uniform-16, and the boundary note
  [`HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`](HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md)
  records that the staircase identity does not by itself pick a
  channel;
- the physical Higgs mass `m_H` numerical value (`m_H_PDG = 125.10` is
  treated as a comparison input only, **not** a derivation input);
- the value of the Wilson coefficient `r` itself (none of `r_{0,4}`,
  `r_{1,3}`, or `r_{16}` is a derivation of `r`; each is a per-
  identification matching value);
- the plaquette mean-field link `u_0` numerical value;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any parent theorem/status promotion;
- any claim that `S = {2}` (the central single-class Higgs
  identification) is wrong; the boundary statement is only that the
  Wilson-shift closure mechanism vanishes for this identification, so
  the +12 % gap cannot be closed by `r` in this channel;
- any claim that the rescaling identity `r_{1,3} = 2 r_{0,4}` extends
  beyond the matching-equation level (it is an algebraic-substitution
  consequence of the closed forms, not a structural derivation of
  either `r` value);
- the exact algebraic matching roots for `r`. The bisection results
  `r_{0,4} ≈ 0.12192 ± 10^{-5}` and `r_{1,3} ≈ 0.24383 ± 10^{-5}`
  are approximate; they are not derivations of canonical Wilson
  coefficient values.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_m_h_per_channel_closure.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: per-channel closure values verified at exact rational
precision. The k=2-only identification is r-independent (the closure
mechanism breaks because the Wilson factor (k-2)^2 vanishes at k=2);
no value of r closes the +12% gap in this channel. The k={0,4} and
k={1,3} paired-class identifications close at r_{0,4} ≈ 0.12192 and
r_{1,3} ≈ 0.24383 respectively (bisection precision ± 10^{-5}); the
two are related by the algebraic-substitution identity r_{1,3} = 2 ·
r_{0,4} at the matching-equation level. The uniform-16 identification
reproduces the all-orders note value r_{16} ≈ 0.26855. All
matching readouts are conditional on (i) channel identification, (ii)
the curvature-on-subset per-channel rule, (iii) tree-level mean-field,
(iv) non-zero r — none of which is a derived value of the Wilson
coefficient.
```
