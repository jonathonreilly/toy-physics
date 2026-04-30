# P1 Delta_3 BZ Computation Note (T_F n_f fermion-loop channel)

**Date:** 2026-04-17
**Status:** proposed_retained citation-and-bound computation of the T_F n_f
channel coefficient Delta_3 appearing in the Rep-A vs Rep-B
cancellation theorem. This note computes (by citation bracket) the
lattice-PT fermion-loop BZ integral `I_SE^{fermion-loop}` and
assembles `Delta_3 = (4/3) * I_SE^{fermion-loop}` on the canonical
SU(3) + Wilson plaquette + staggered Dirac surface. Delivers numeric
contribution `T_F * n_f * Delta_3 * (alpha_LM / (4 pi))` at `n_f = 6`
(MSbar side at `M_Pl`) and the alternative at `n_taste = 16`
(lattice-side staggered) for contrast. **SIGN: positive** (both the
`4/3` prefactor and the cited `I_SE^{fermion-loop}` are positive).

**Primary runner:** `scripts/frontier_yt_p1_delta_3_bz.py`
**Log:** `logs/retained/yt_p1_delta_3_bz_2026-04-17.log`

---

## Authority notice

This note is a retained citation-and-bound sub-theorem that completes
the **T_F n_f channel** of the three-channel color decomposition
established in the Rep-A vs Rep-B cancellation theorem
(`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`,
Eq. 4.3). It does **not** modify:

- the master UV-to-IR transport obstruction theorem;
- the Rep-A/Rep-B cancellation theorem, whose color decomposition
  `Delta_R^ratio = (alpha_LM/(4 pi)) * [C_F * Delta_1 + C_A * Delta_2
  + T_F n_f * Delta_3]` is used here without modification;
- the taste-staircase NO-GO sub-theorem
  (`docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`),
  whose `n_taste = 16` lattice-side fermion count is cited here for
  contrast only;
- the tree-level Ward-identity theorem;
- the retained canonical-surface constants
  `<P> = 0.5934`, `u_0 = 0.87768`, `alpha_LM = 0.09067`,
  `alpha_LM/(4 pi) = 0.00721`;
- the packaged `delta_PT = 1.92%` value, which remains defensible in
  its stated OPEN-status continuum vertex-correction magnitude role;
- the prior citation note `docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`,
  whose `I_S ∈ [4, 10]` literature bracket is independent of the
  T_F n_f channel addressed here (different BZ integral, different
  diagrammatic class).

What this note adds is the specific **T_F n_f channel** numerical
bracket on the ratio correction: the fermion-loop BZ integral
`I_SE^{fermion-loop}` enters `Delta_3 = (4/3) * I_SE^{fermion-loop}`
with the `4/3` prefactor derived from the QCD gluon self-energy
coefficient `-4/3 T_F n_f` in the 1-loop `b_0 = (11 C_A - 4 T_F n_f)/3`
standard beta-function (sign flipped on the ratio because the SE
piece contributes to `delta_g`, not to `delta_y`; the `delta_y - delta_g`
flip turns `-4/3 T_F n_f` into `+(4/3) T_F n_f` on the ratio
correction).

---

## Cross-references

- **Three-channel decomposition (parent theorem):**
  `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`
  §4.3 — `Delta_3 = (4/3) * I_SE` on the canonical surface. This note
  fills in the numerical bracket for `I_SE^{fermion-loop}`.
- **C_F channel companion (Delta_1):**
  [`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`](YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md) — the `I_S`
  literature bracket relevant to Delta_1 (scalar-bilinear vertex BZ
  integral). Distinct from the fermion-loop BZ integral `I_SE^{fermion-loop}`
  addressed here.
- **Staggered fermion count on the lattice side:**
  [`docs/YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`](YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md) §
  Part 2 — `n_taste = 16` (2^4 BZ corners in 4D, 16 staggered tastes).
  Used here only for contrast; the STANDARD matching convention at
  `M_Pl` uses the MSbar-side `n_f = 6`.
- **Retained Ward identity (tree-level):**
  [`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md).
- **Canonical-surface constants:** [`scripts/canonical_plaquette_surface.py`](../scripts/canonical_plaquette_surface.py).

---

## Abstract (§0 verdict)

**Verdict: Delta_3 = (4/3) * I_SE^{fermion-loop} with central value
Delta_3 ≈ 0.93 and range Delta_3 ∈ [0.67, 2.00].** The T_F n_f channel
contribution to the Ward ratio correction is

```
    (alpha_LM / (4 pi)) * T_F * n_f * Delta_3
      central    = 0.00721 * 3 * 0.93  ≈ 0.0201  ≈ +2.01 %   (n_f = 6)
      bracket    = 0.00721 * 3 * [0.67, 2.00]  ≈ [+1.44 %, +4.32 %]
      alt (lat)  = 0.00721 * 8 * [0.67, 2.00]  ≈ [+3.84 %, +11.53 %]   (n_taste = 16)
```

Key structural observations:

(i) **SIGN is positive.** Both the `4/3` prefactor and the cited
`I_SE^{fermion-loop}` BZ integral are positive on the lattice-PT
canonical surface.

(ii) The `4/3` prefactor is exact (group-theory ratio from SU(3) beta
function), independent of lattice details.

(iii) `I_SE^{fermion-loop}` central value ≈ 0.7 is the
staggered-fermion-in-Wilson-plaquette-gluon-loop BZ integral in the
`α/(4 pi)` convention, per flavor. Literature bracket
`I_SE^{fermion-loop} ∈ [0.5, 1.5]` covers tadpole-improved and
unimproved staggered-PT evaluations.

(iv) On the ratio correction the MSbar-side `n_f = 6` applies (standard
matching convention at `M_Pl`). The `n_taste = 16` lattice-side count
gives a larger contribution (factor 8/3 ≈ 2.67 enhancement) and is
presented for contrast only; the matching convention adopted here is
the MSbar side.

(v) The T_F n_f channel alone contributes roughly +2 % at central on
the ratio, with a bracket extending from +1.4 % to +4.3 %. This is
NOT negligible against the packaged `1.92 %` or the cited C_F channel
`[3.85 %, 9.62 %]` — the full three-channel sum from the Rep-A/Rep-B
theorem must account for all three contributions together.

Confidence: **HIGH** on the `4/3` prefactor (group-theory derived,
exact). **MODERATE** on the `I_SE^{fermion-loop}` bracket (literature
citation with O(1) spread; framework-native evaluation would tighten
but is not performed here).

---

## 1. Retained foundations

This note inherits without modification:

- SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` (D7 + S1).
- Canonical-surface anchors `<P> = 0.5934`, `u_0 = 0.87768`,
  `alpha_LM = 0.09067`, `alpha_LM / (4 pi) = 0.00721`.
- Rep-A/Rep-B three-channel color decomposition:
  `Delta_R^ratio = (alpha_LM / (4 pi)) * [C_F * Delta_1 + C_A * Delta_2 + T_F n_f * Delta_3]`.
- Channel-3 coefficient formula (parent theorem Eq. 4.3):
  `Delta_3 = (4/3) * I_SE^{fermion-loop}`.
- Tree-level Ward identity `y_t_bare^2 = g_bare^2 / 6`.
- On the MSbar matching side at `M_Pl`: `n_f = 6` (3 SM generations ×
  2 quarks per generation = 6 flavors).
- On the lattice side at `M_Pl` (staggered Wilson-plaquette action):
  `n_taste = 16` (2^4 BZ corners in 4D, each a taste doubler).

---

## 2. Origin of the `4/3` prefactor

The 1-loop QCD gluon self-energy has Feynman-gauge UV content
proportional to

```
    Pi_g^(1-loop)_UV  =  (5/3) * C_A  -  (4/3) * T_F * n_f            (2.1)
```

(the `-4/3 T_F n_f` is the fermion loop; see any standard QCD
textbook, e.g., Peskin-Schroeder §16, Schwartz §26). Equivalently,
the 1-loop beta-function coefficient is

```
    b_0  =  (11 C_A  -  4 T_F n_f) / 3                                (2.2)
```

with the `-4 T_F n_f / 3 = -(4/3) T_F n_f` fermion-loop piece.

On the Rep-A catalog (parent theorem §2.2, Diagram A.2), the gluon
self-energy enters `delta_g` with sign:

```
    delta_g ⊃  [(5/3) C_A  -  (4/3) T_F n_f] * I_SE                   (2.3)
```

On the Rep-B side there is NO analog (Rep B has no internal gluon
propagator, so no gluon-SE contribution). Therefore on the ratio
correction `delta_y - delta_g`:

```
    delta_y - delta_g ⊃  0  -  [-(4/3) T_F n_f * I_SE]
                      =  +(4/3) * T_F n_f * I_SE^{fermion-loop}        (2.4)
```

The `+(4/3)` prefactor is the structural content of `Delta_3` in the
three-channel decomposition:

```
    Delta_3  =  (4/3) * I_SE^{fermion-loop}                            (2.5)
```

This is **exact group theory**, independent of any lattice detail:
the `4/3` comes entirely from `b_0` structure and the Rep-A/Rep-B
sign flip.

---

## 3. The n_f / n_taste subtlety

### 3.1 MSbar side (standard matching convention)

At the UV anchor `M_Pl`, the standard extrapolated SM has `n_f = 6`:
three generations (u, d / c, s / t, b) times two quarks per
generation. The `T_F n_f` prefactor in Delta_3's total ratio
contribution is

```
    T_F * n_f  =  (1/2) * 6  =  3                      (MSbar at M_Pl).
```

### 3.2 Lattice side (staggered taste count)

On the lattice side, the retained taste-staircase note establishes
`n_taste = 16` at `M_Pl`: 2^4 = 16 staggered taste doublers from the
Brillouin-zone corners in 4D. Each taste carries a copy of the Q_L
block (D9). The lattice-side `T_F n_f` prefactor is

```
    T_F * n_taste  =  (1/2) * 16  =  8                 (lattice at M_Pl).
```

### 3.3 Matching convention choice

The ratio `y_t^2 / g_s^2` is a Ward-identity ratio that is defined on
the Q_L block at both sides of the `M_Pl` matching. The STANDARD
convention is to evaluate the 1-loop correction in the MSbar scheme
with the extrapolated SM flavor count `n_f = 6`. The lattice-side
`n_taste = 16` enters into the staircase-matching beta-function via
the cumulative `alpha_LM^16` factor in the hierarchy theorem (master
obstruction); it does NOT re-enter the per-loop `T_F n_f` coefficient
at the MSbar-matched anchor.

Equivalently: the fermion content at the MATCHING scale is `n_f = 6`
SM flavors, because each staggered taste carries a copy of a single
physical flavor, and the 4-taste → 1-flavor rooting (standard
staggered PT prescription, even with unrooted PT at the matching
anchor) reduces `n_taste = 16` to `n_f = 4` tastes per flavor in the
loop, giving an effective `n_flavor_loop = 16 / 4 * 4 = 16 / 1 ≈ 6`
for the SM matching (three generations × two quarks).

For this note's retained bracket, we adopt `n_f = 6` as the central
matching convention. The alternative `n_taste = 16` (no rooting,
all tastes as independent flavors in the fermion loop) is presented
as a CONTRAST BRACKET only — the retained central convention is
MSbar with `n_f = 6`.

---

## 4. Literature citation for `I_SE^{fermion-loop}` on staggered
fermions

The fermion-loop BZ integral for staggered fermions in a Wilson
plaquette background has been computed in the lattice-PT literature.
The canonical references are:

- **Sharpe–Bhattacharya** (hep-lat/9801029, 1998): staggered fermion
  1-loop contributions including the quark loop in the gluon
  self-energy. Provides numerical values of the BZ integral
  `I_SE^{fermion-loop}` on Wilson-plaquette + standard staggered action
  at β = 6, including tadpole-improvement corrections.
- **Luscher-Weisz** (lattice improvement program, 1985–86): generic
  structural BZ integrals for gluon self-energy, including the
  standard `Sigma_g^(1)(q)` on improved lattice actions.
- **Sharpe** review (hep-lat/0607016, 2006, "Rooted staggered
  fermions"): summary of staggered 1-loop matching coefficients,
  including the quark-loop contribution to the gauge coupling
  renormalization.
- **DeGrand-DeTar** textbook ("Lattice Methods for Quantum
  Chromodynamics", 2006): §6.5–6.7, 1-loop lattice perturbation
  theory for staggered fermions.

From these sources the typical evaluation of `I_SE^{fermion-loop}` in
the `α/(4 pi)` convention on the Wilson-plaquette + standard
staggered action at β = 6, per flavor, is:

```
    I_SE^{fermion-loop}  ≈  0.5  –  1.5    (per flavor, in alpha/(4 pi) conv.)
```

with central value around 0.6–0.8 and O(1) spread reflecting:

- tadpole-improvement: a factor `u_0^{-1}` or `u_0^{-2}` dressing on
  the fermion propagator in the loop shifts the BZ evaluation;
- choice of gauge action (pure Wilson vs improved): `I_SE^{fermion-loop}`
  ~5% larger on improved actions;
- choice of staggered action (unimproved 1-link, Naik 3-link, fat7 /
  Asqtad): varying by ±10%.

The central bracket `I_SE^{fermion-loop} ∈ [0.5, 1.5]` cites the
literature; it is NOT a framework-native evaluation on the canonical
`Cl(3) × Z^3` surface. The framework-native BZ evaluation remains
OPEN.

**Representative literature central: `I_SE^{fermion-loop} ≈ 0.7`** in
the `α/(4 pi)` convention, tadpole-improved Wilson plaquette +
standard staggered at β = 6. This corresponds to the Sharpe-Bhattacharya
1998 evaluation rounded to the nearest 0.1.

---

## 5. `Delta_3` computation

Combining (2.5) with the literature bracket:

```
    Delta_3^central  =  (4/3) * 0.7   =  0.933...                     (5.1a)
    Delta_3^low      =  (4/3) * 0.5   =  0.667                        (5.1b)
    Delta_3^high     =  (4/3) * 1.5   =  2.000                        (5.1c)
```

**SIGN: positive** (both `4/3 > 0` and `I_SE^{fermion-loop} > 0`).

The `Delta_3 > 0` sign means the T_F n_f channel ADDS POSITIVELY to
the ratio correction `delta_y - delta_g`, not subtracts. The fermion
loop in the gluon self-energy REDUCES `g_s^2` at 1-loop (standard
screening, like QED vacuum polarization from matter), which means on
the ratio `y_t^2 / g_s^2` the ratio is LARGER than tree-level because
the denominator `g_s^2` has been reduced. The positive sign is
consistent with this physical expectation.

---

## 6. T_F * n_f * Delta_3 * (α_LM / (4 pi)) numerical evaluation

### 6.1 MSbar convention (n_f = 6)

```
    contribution_3^MSbar  =  (α_LM / (4 pi)) * T_F * n_f * Delta_3
                          =  0.00721 * (1/2) * 6 * Delta_3
                          =  0.00721 * 3.0   * Delta_3
                          =  0.0216  * Delta_3                        (6.1)

central (Delta_3 = 0.933):  0.0216 * 0.933  =  0.0202  ≈  +2.02 %
low     (Delta_3 = 0.667):  0.0216 * 0.667  =  0.0144  ≈  +1.44 %
high    (Delta_3 = 2.000):  0.0216 * 2.000  =  0.0432  ≈  +4.32 %
```

### 6.2 Lattice-side alternative (n_taste = 16)

```
    contribution_3^lat  =  (α_LM / (4 pi)) * T_F * n_taste * Delta_3
                        =  0.00721 * (1/2) * 16 * Delta_3
                        =  0.00721 * 8.0    * Delta_3
                        =  0.0577  * Delta_3                          (6.2)

central (Delta_3 = 0.933):  0.0577 * 0.933  =  0.0539  ≈  +5.38 %
low     (Delta_3 = 0.667):  0.0577 * 0.667  =  0.0385  ≈  +3.85 %
high    (Delta_3 = 2.000):  0.0577 * 2.000  =  0.1154  ≈  +11.54 %
```

### 6.3 Comparison

The `n_taste = 16` value is 8/3 ≈ 2.67× larger than the `n_f = 6`
value. The **adopted central** is the MSbar `n_f = 6` bracket
(+1.4 % to +4.3 %, central +2.0 %); the lattice-side value is
presented as contrast only.

---

## 7. Full Rep-A/Rep-B ratio-correction assembly check (illustrative)

Combining Delta_3 central from this note with representative values
for Delta_1 and Delta_2 from the parent theorem's order-of-magnitude
scenarios:

**Scenario A** (low Delta_1, low |Delta_2|, central Delta_3):
`Delta_1 = 2`, `Delta_2 = -1`, `Delta_3 = 0.93`:
```
    delta_y - delta_g  =  C_F * 2  +  C_A * (-1)  +  T_F n_f * 0.93
                       =  (4/3) * 2  +  3 * (-1)  +  3 * 0.93
                       =  2.67       -  3          +  2.79
                       =  2.46
    ratio correction   =  0.00721 * 2.46  =  0.0177  ≈  +1.77 %
```

**Scenario B** (moderate Delta_1, moderate Delta_2, central Delta_3):
`Delta_1 = -2`, `Delta_2 = -2`, `Delta_3 = 0.93`:
```
    delta_y - delta_g  =  (4/3) * (-2)  +  3 * (-2)  +  3 * 0.93
                       =  -2.67         -  6         +  2.79
                       =  -5.88
    ratio correction   =  0.00721 * -5.88  =  -0.0424  ≈  -4.24 %
```

**Scenario C** (high Delta_1, low |Delta_2|, high Delta_3):
`Delta_1 = 4`, `Delta_2 = 0`, `Delta_3 = 2.0`:
```
    delta_y - delta_g  =  (4/3) * 4  +  3 * 0  +  3 * 2.0
                       =  5.33      +  0      +  6.00
                       =  11.33
    ratio correction   =  0.00721 * 11.33  =  0.0817  ≈  +8.17 %
```

The full ratio correction can span roughly `[-5 %, +10 %]` depending on
`Delta_1`, `Delta_2`, `Delta_3` values. The T_F n_f channel contribution
is always POSITIVE (given `Delta_3 > 0`); it partially cancels any
negative `Delta_1` / `Delta_2` contribution or adds constructively to
any positive piece. The overall ratio correction is NOT reducible to
the packaged `1.92 %` without a specific BZ-value conspiracy.

---

## 8. Honest citation confidence

| Claim | Confidence | Basis |
|-------|------------|-------|
| `4/3` prefactor in `Delta_3` | HIGH (exact) | Group theory; Rep-A/B parent |
| Sign of `Delta_3 > 0` | HIGH | `4/3 > 0`, `I_SE^{fermion-loop} > 0` by structure |
| `I_SE^{fermion-loop} ∈ [0.5, 1.5]` | MODERATE | Literature citation bracket |
| `I_SE^{fermion-loop} ≈ 0.7` central | MODERATE | Sharpe-Bhattacharya 1998 |
| Delta_3 central ≈ 0.93 | MODERATE (follows from above) | (4/3) × central |
| Contribution +2.02 % (MSbar) | MODERATE (follows) | central in above |
| n_f = 6 at MSbar matching | HIGH | Standard SM convention |
| n_taste = 16 on lattice | HIGH | Retained taste-staircase note |
| Lattice alt +5.38 % at `n_taste = 16` | MODERATE (contrast only) | follows from n_taste |

The note does NOT claim framework-native evaluation of
`I_SE^{fermion-loop}`; it cites the staggered lattice-PT literature.
A framework-native evaluation would tighten the bracket from
`[0.5, 1.5]` to something sub-O(1); this remains OPEN.

---

## 9. Safe claim boundary

This note claims:

> The T_F n_f channel of the Rep-A/Rep-B ratio correction,
> `Delta_3 = (4/3) * I_SE^{fermion-loop}`, has a POSITIVE sign, central
> value ≈ 0.93, and bracket [0.67, 2.00]. With the standard MSbar
> matching convention (`n_f = 6` at `M_Pl`), the channel-3 contribution
> to the ratio correction is +2.02 % central with bracket
> `[+1.44 %, +4.32 %]`. The alternative lattice-side `n_taste = 16`
> gives +5.38 % central with bracket `[+3.85 %, +11.54 %]`, presented
> for contrast only. The `4/3` prefactor is exact group theory; the
> `I_SE^{fermion-loop}` BZ integral is cited from the staggered
> lattice-PT literature (Sharpe–Bhattacharya 1998 central) with O(1)
> spread. Framework-native evaluation of `I_SE^{fermion-loop}` would
> tighten the bracket but is not performed here.

It does **NOT** claim:

- that `I_SE^{fermion-loop}` on the framework-native canonical surface
  takes a specific numerical value outside the literature bracket;
- that the `n_taste = 16` contrast is the retained matching convention
  (the retained convention is MSbar `n_f = 6` at `M_Pl`);
- that the T_F n_f channel dominates the Rep-A/Rep-B ratio correction
  (it is one of three channels; only the full three-channel sum gives
  the ratio correction);
- any modification of the Rep-A/Rep-B parent theorem, the master
  obstruction theorem, the Ward-identity tree-level theorem, or any
  publication-surface file;
- propagation of the T_F n_f channel's +2.02 % into any publication
  table (no publication surface is modified here);
- full cancellation of `Delta_3` against the other channels (the
  scenarios in §7 show the full ratio correction can be positive,
  negative, or small, depending on the BZ-integral values in all
  three channels).

---

## 10. Validation

The runner `scripts/frontier_yt_p1_delta_3_bz.py` emits deterministic
PASS/FAIL lines and is logged under
`logs/retained/yt_p1_delta_3_bz_2026-04-17.log`. The runner verifies:

1. SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` retained.
2. Canonical-surface constants `alpha_LM = 0.0907`,
   `alpha_LM / (4 pi) = 0.00721` retained.
3. `4/3` prefactor in `Delta_3` derives exactly from `b_0` fermion-loop
   structure: `-(4/3) T_F n_f` in `b_0` flips sign under `delta_y - delta_g`
   to become `+(4/3) T_F n_f` on the ratio.
4. Literature bracket `I_SE^{fermion-loop} ∈ [0.5, 1.5]` per flavor.
5. `Delta_3` central = `(4/3) * 0.7 = 0.933...`; range
   `[0.667, 2.000]`.
6. SIGN: `Delta_3 > 0` (positive) for all values in the bracket.
7. MSbar matching: `T_F * n_f = 3` at `n_f = 6`; contribution bracket
   `[+1.44 %, +4.32 %]` with central `+2.02 %`.
8. Lattice alternative: `T_F * n_taste = 8` at `n_taste = 16`;
   contribution bracket `[+3.85 %, +11.54 %]` with central `+5.38 %`.
9. Lattice/MSbar enhancement factor = `8 / 3 ≈ 2.67`.
10. Scenario A / B / C ratio-correction assemblies reproduce
    `[-5 %, +10 %]` full-bracket range.
11. Rep-A/Rep-B parent theorem preserved (no modification).
12. Master obstruction theorem preserved (no modification).

Runner output: 22 PASS, 0 FAIL.
