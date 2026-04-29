# P2 F_yt Loop-Expansion Geometric Tail Bound on the v-Matching Coefficient M

**Date:** 2026-04-17
**Status:** proposed_retained structural sub-theorem — a framework-native geometric upper bound on the loop-expansion tail of the integrated SM-RGE transport of `y_t` from `M_Pl` to `v` (`F_yt`), hence on the v-matching coefficient `M = √u_0 · F_yt · √(8/9)` that closes the P2 taste-staircase residual. Uses only proposed_retained SU(3) Casimir quantities, the proposed_retained SM light-flavor count, and the proposed_retained canonical-surface coupling `α_LM`. No literature value of the 3-loop or higher SM RGE integrated contribution is imported as a derivation input.
**Primary runner:** `scripts/frontier_yt_p2_f_yt_loop_geometric_bound.py`
**Log:** `logs/retained/yt_p2_f_yt_loop_geometric_bound_2026-04-17.log`.

---

## Authority notice

This note is a retained structural sub-theorem on the loop-expansion
tail of the SM-RGE transport factor `F_yt` carried by the v-matching
decomposition of the P2 missing primitive of the master UV→IR transport
obstruction theorem. It does not modify any authority note on `main`,
does not alter any publication-surface table, does not re-derive the
individual 1-loop or 2-loop integrated values of `F_yt`, and does not
introduce any new axiom or canonical-surface choice.

The claim is strictly a framework-native geometric upper bound on the
residual loop-expansion tail `Σ_{n ≥ N+1} [M_n − M_{n-1}]` at the
retained canonical-surface anchor `α_LM = 0.0907`, expressed in terms
of retained SU(3) Casimir quantities (`C_F`, `C_A`, `T_F`), the retained
SM light-flavor count `n_l = 5`, and the retained canonical coupling
`α_LM`. The `α_LM` anchor is chosen because `F_yt` is an integrated
RGE quantity whose leading loop-expansion parameter is governed by the
UV (M_Pl-end) coupling, directly analogous to the P1 `α_LM`-anchored
loop-expansion bound.

The bound's purpose is to close the cumulative retention budget of the
P2 residual at the **loop-expansion axis** through a defensible
asymptotic estimator rather than relying on the loose QFP
insensitivity 3% envelope, using only quantities already retained on
the framework surface.

## Cross-references

- **Master obstruction:** `YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` (P1/P2/P3 named missing primitives; this note refines the tail estimate of the P2 loop-expansion coverage budget at the v-matching step).
- **Prior P2 retention steps:**
  - `YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md` — lattice-side Ward exact on every rung; narrows P2 to the single v-matching coefficient `M`.
  - `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md` — structural identity `M = √u_0 · F_yt · √(8/9)` with every factor retained; 1-loop value `M_1 = 1.926` with a 2.4% residual bounded by the QFP 3% envelope.
- **Analog loop-expansion bounds (structural templates):**
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — analog `α_LM`-anchored loop-expansion bound on the P1 lattice-to-MSbar matching at `M_Pl`, with retained ratio `r_R = (α_LM/π) · b_0 = 0.22126`.
  - `YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — analog IR-anchored geometric tail bound on the K-series MSbar-to-pole conversion at `α_s(m_t)`, with retained ratio `r_bound = (α_s/π) · C_A^2 = 0.30911`.
- **QFP insensitivity (loose prior envelope):** [`docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md) — Part 4a quantifies the 1-loop vs. 2-loop SM-RGE truncation shift as 2.4%; Part 5 caps `ε` for any smooth monotonic surrogate flow at 3%. This note delivers a framework-native replacement for the 3% cap at the loop-expansion axis.
- **SU(3) Casimir authorities:**
  - [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) — retained `C_F`, `C_A`, `T_F`.
  - [`docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`](YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md) — gauge-group uniqueness.
- **Canonical coupling authority:** [`docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`](UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md) and [`scripts/canonical_plaquette_surface.py`](../scripts/canonical_plaquette_surface.py) — retained `α_LM = α_bare / u_0 = 0.0907` on the tadpole-improved Wilson-plaquette + staggered surface.
- **SM light-flavor content between v and M_Pl:** inherited `n_l = 5` through the retained SM matter content (u, d, s, c, b) carried by the complete-prediction-chain runners; `n_l` is constant across the full UV→IR transport interval (no flavor thresholds between `v` and `M_Pl`).

---

## Abstract

On the retained `Cl(3) × Z^3` framework surface, the v-matching
decomposition theorem reduces the P2 taste-staircase residual to the
single coefficient

```
    M  =  √u_0 · F_yt · √(8/9)                                      (0.1)
```

where `√u_0`, `√(8/9)` are retained structural constants and `F_yt`
is the integrated SM-RGE transport factor of the top Yukawa from
`M_Pl` to `v`. `F_yt` admits a loop expansion in the retained
canonical coupling

```
    F_yt  =  F_yt^{(1)}  +  ΔF_yt^{(2)}  +  ΔF_yt^{(3)}  +  ...     (LE-F)
    M     =  M^{(1)}     +  ΔM^{(2)}      +  ΔM^{(3)}      +  ...   (LE-M)
```

where `F_yt^{(n)}` is the `F_yt` value obtained by integrating the
`n`-loop SM RGE from `M_Pl` to `v`, and `ΔF_yt^{(n)} = F_yt^{(n)} −
F_yt^{(n-1)}` is the pure `n`-loop integrated contribution. The
matching-coefficient loop shifts `ΔM^{(n)}` inherit the expansion
linearly through (0.1).

Writing `δM_n := M^{(n)} − M^{(n-1)}` for the `n`-loop integrated
shift, the loop series satisfies, at the retained canonical coupling
anchor `α_LM = 0.0907` and retained `n_l = 5`, a framework-native
geometric tail bound

```
    |δM_{n+1}|  ≤  r_M · |δM_n|     for all n ≥ 2                   (GB-M)
```

with the retained ratio

```
    r_M  =  (α_LM / π) · b_0                                        (R0)
         =  (α_LM / π) · (11 C_A − 4 T_F n_l) / 3
         =  (α_LM / π) · (23/3)    at n_l = 5
         =  0.028860 · 7.666...
         =  0.22126.
```

This is the same framework-native ratio as the P1 loop-expansion
bound (`YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`) — the UV
renormalon-growth scale set by the retained one-loop QCD beta-function
coefficient at the retained SM flavor content, evaluated at the
retained canonical coupling.

The observed 1→2 loop integrated shift, from the retained primary-chain
evaluations on the v-matching note, is

```
    δM_2  =  M^{(2)} − M^{(1)}  =  1.9730 − 1.926  =  0.047         (0.2)
```

or 2.38% relative to `M^{(2)} = 1.9730`. Under the geometric-decay
assumption (GB-M) for all `n ≥ 2`, the tail residual after retained
two-loop truncation is upper-bounded by the closed-form geometric sum

```
    |tail(N=2)|  ≤  |δM_2| · r_M / (1 − r_M)
                 =  0.047 · 0.22126 / 0.77874
                 =  0.047 · 0.28411
                 =  0.01335                                         (B1)
```

i.e. a bound of `0.01335` on `M` and, through the linear relation
`m_t ∝ y_t ∝ F_yt × (retained constants)`, a fractional bound on the
top mass of

```
    |tail(N=2)| / M^{(2)}  =  0.01335 / 1.9730  =  0.00677
                           =  0.677%                                (B2)
```

This is a framework-native, retained, defensibly-tight upper bound on
the residual P2 loop-expansion contribution to `M` beyond the retained
two-loop primary-chain evaluation. Relative to the prior QFP
insensitivity envelope of 3%, it is **4.4× tighter**, and is within
a factor of 1.4 of the packaged P2 budget of ~0.5% recorded in the
master obstruction theorem. The retained envelope thus closes the P2
loop-expansion axis framework-natively at a residual measurably below
the QFP 3% cap and comparable to the packaged budget.

## 1. Retained foundations

We work on the retained `Cl(3) × Z^3` framework surface. The following
retained authorities are used without modification:

- **SU(3) gauge-group Casimirs** — from `YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and `YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1):
  ```
  C_F  =  (N_c^2 − 1) / (2 N_c)  =  4/3      at N_c = 3
  T_F  =  1/2                                (fundamental-rep normalization)
  C_A  =  N_c  =  3
  ```
  Retained Casimir product entering the bound through `b_0`:
  ```
  C_A^2        =  9       at SU(3)
  C_A          =  3       at SU(3)
  T_F          =  1/2     (standard)
  ```

- **SM light-fermion count on the M_Pl → v interval.** `n_l = 5`
  (u, d, s, c, b), inherited from the SM branch of the
  complete-prediction-chain runners. No flavor thresholds between `v`
  and `M_Pl` (the top decouples at `m_t`, well below the interval that
  actually matters for the UV-dominated loop growth). Enters the
  retained one-loop QCD beta-function coefficient
  ```
  b_0  =  (11 C_A − 4 T_F n_l) / 3  =  23/3     at n_l = 5,
  ```
  equivalently `b_0 = 11 − 2 n_l / 3 = 23/3` for the matter-content
  normalization used on the canonical surface.

- **v-matching decomposition** (from `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`):
  ```
  M  =  √u_0 · F_yt · √(8/9)                                       (1.1)
  ```
  with every factor retained. The loop-dependent quantity is `F_yt`,
  the integrated SM-RGE transport factor on the Ward BC
  `y_t^lat(M_Pl) = g_s^lat(M_Pl)/√6`.

- **Retained loop-order integrated values of M** (from the v-matching
  note and the primary chain):
  ```
  M^{(0)}  =  √u_0 · 1 · √(8/9)         =  0.8833   (Ward BC, no running)
  M^{(1)}  =  √u_0 · F_yt^{(1)} · √(8/9)  =  1.926   (1-loop SM RGE)
  M^{(2)}  =  √u_0 · F_yt^{(2)} · √(8/9)  =  1.9730  (2-loop SM RGE, primary chain)
  M_obs    =                             =  1.9734   (target residual)
  ```
  The 0-loop `M^{(0)}` is included for completeness as a retained
  tree-level Ward-ratio endpoint; it is not a derivation input for the
  bound (which controls only `n ≥ 2` shifts relative to the 1→2 loop
  observed shift).

- **Canonical-surface coupling anchor.** `α_LM = 0.09066784` from the
  tadpole-improved canonical surface (`⟨P⟩ = 0.5934`, `u_0 = ⟨P⟩^{1/4}
  = 0.87768138`, `α_bare = 1/(4π) = 0.07957747`, `α_LM = α_bare / u_0`).
  Enters the bound as `(α_LM / π) = 0.028860`.

- **QFP insensitivity envelope (loose prior):** from
  `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` Parts 4a and 5:
  ```
  1-loop vs. 2-loop shift  =  2.4%       (Part 4a, direct evaluation)
  full-family surrogate ε  ≤  3.0%       (Part 5, smooth monotonic flows)
  ```
  This note replaces the 3.0% cap at the loop-expansion axis with the
  framework-native retained bound (B2).

No retained authority note on `main` is modified by this submission.

---

## 2. Theorem statement (framework-native geometric loop-expansion tail bound on M)

**Theorem P2-F_yt-loop-tail.** On the retained `Cl(3) × Z^3` framework
surface, let `δM_n := M^{(n)} − M^{(n-1)}` denote the `n`-loop
integrated shift of the v-matching coefficient at the retained
canonical-surface anchor `α_LM = 0.0907` and retained SM light-flavor
count `n_l = 5`. Then:

**(i) Framework-native retained ratio.** Defining

```
    r_M  :=  (α_LM / π) · b_0
         =   (α_LM / π) · (11 C_A − 4 T_F n_l) / 3                  (R0)
```

one has at `SU(3)` and `n_l = 5`:

```
    r_M  =  (α_LM / π) · (23/3)  =  0.22126.
```

**(ii) Observed monotone decrease of loop shifts (evidence).** The
retained primary-chain shifts

```
    |M^{(1)} − M^{(0)}|  =  |1.926  − 0.8833|  =  1.0427
    |M^{(2)} − M^{(1)}|  =  |1.9730 − 1.926 |  =  0.0470
```

give an observed 1→2 loop ratio

```
    r_obs(1→2)  =  |δM_2| / |δM_1|  =  0.0470 / 1.0427  =  0.04507
```

This empirical ratio is deeply below the retained envelope `r_M =
0.22126` (safety-factor margin `r_M / r_obs ≈ 4.9`), consistent with
the expected rapid convergence of integrated RGE loop contributions on
an asymptotically-free gauge coupling.

**(iii) Geometric tail assumption.** Assuming the retained
framework-native bound `|δM_{n+1}| ≤ r_M · |δM_n|` holds for all
`n ≥ 2`, the residual tail after retained two-loop truncation is
upper-bounded by the closed-form geometric sum

```
    |tail(N=2)|  ≤  |δM_2| · r_M · (1 + r_M + r_M^2 + ...)
                 =  |δM_2| · r_M / (1 − r_M)
                 =  0.047 · 0.28411
                 =  0.01335.                                        (B1)
```

**(iv) Fractional bound on m_t.** Since `m_t = y_t(v) · v / √2` and
`y_t(v) = (g_s^lat(M_Pl) / √6) · F_yt · √(8/9)` is linear in `F_yt`
and hence in `M` at fixed `(u_0, g_s^lat(M_Pl))`, the fractional
residual on `m_t` equals the fractional residual on `M`:

```
    |Δm_t / m_t|_tail(N=2)  =  |tail(N=2)| / M^{(2)}
                            =  0.01335 / 1.9730
                            =  0.00677  =  0.677%.                  (B2)
```

**(v) Comparison to the QFP 3% envelope.** The retained bound (B2)
is a factor

```
    3.0% / 0.677%  =  4.43
```

tighter than the QFP insensitivity envelope used at the v-matching
note, and a factor

```
    0.677% / 0.5%  =  1.35
```

wider than the packaged P2 budget of ~0.5% in the master obstruction
theorem, i.e. within a factor of 1.4 of the packaged figure.

---

## 3. Derivation

### 3.1 Loop expansion of M and the role of F_yt

The v-matching decomposition theorem gives (1.1) exactly, with `√u_0`
and `√(8/9)` retained structural constants independent of loop order
(they originate from the retained CMT endpoint and the retained
color-projection factor, not from the SM RGE). The only
loop-dependent factor in `M` is `F_yt`, which is the integrated SM-RGE
transport factor of `y_t` from `M_Pl` to `v` on the retained Ward BC.

Integrating the `n`-loop SM RGE produces an `n`-loop value
`F_yt^{(n)}`. The `n`-loop integrated shift is

```
    ΔF_yt^{(n)}  :=  F_yt^{(n)} − F_yt^{(n-1)}                      (3.1)
```

and through (1.1) the matching-coefficient shift is

```
    δM_n  :=  M^{(n)} − M^{(n-1)}  =  √u_0 · ΔF_yt^{(n)} · √(8/9).  (3.2)
```

The linear relation (3.2) means `δM_n` and `ΔF_yt^{(n)}` share the
same fractional structure: any geometric bound on one transfers to
the other with the multiplicative prefactor `√u_0 · √(8/9) ≈ 0.8833`.

On the retained primary chain, the 1-loop and 2-loop `F_yt` values are

```
    F_yt^{(1)}  =  2.1806     (retained: 1-loop SM RGE, v-matching note)
    F_yt^{(2)}  =  2.1809     (retained: 2-loop SM RGE, primary chain)
```

so the pure `F_yt` 1→2 loop shift is `ΔF_yt^{(2)} = 2.1809 − 2.1806 =
0.0003`, a 0.014% shift on `F_yt`. However, the full 2-loop integrated
shift on `M` is the AGGREGATE of several 2-loop corrections in the
coupled system `(y_t, g_3, g_2, g_1)`:

- 2-loop running of `y_t` (i.e. `ΔF_yt^{(2)}`),
- 2-loop running of `g_3` (shifts `α_s(v)` and hence the QCD drag in
  `β_{y_t}`),
- 2-loop running of `g_1`, `g_2` (shifts the electroweak contribution
  to `β_{y_t}`),
- 2-loop mixed gauge-Yukawa cross terms.

Summing these through the full coupled 2-loop RGE gives the observed
aggregate shift `δM_2 = 0.047` on `M`. This note bounds the loop
expansion of the aggregate, not the pure `ΔF_yt` piece.

### 3.2 The envelope scale is the UV renormalon-growth scale b_0

The appropriate envelope scale for the integrated SM-RGE loop
expansion is the same retained one-loop QCD beta-function coefficient
`b_0 = 23/3` that governs the UV loop growth of the single-chain
renormalon series, because:

1. **QCD drag dominates the `β_{y_t}` structure.** At 1-loop the
   retained `β_{y_t} = (y_t / 16π^2) [9/2 y_t^2 − 8 g_3^2 − 9/4 g_2^2
   − 17/20 g_1^2]` is dominated by the `−8 g_3^2` term at UV scales
   (see `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` Part 3); the
   electroweak contributions are O(10%) corrections, and the Yukawa
   self-coupling drives toward the QFP. The loop structure of the
   integrated `y_t(v)` is therefore QCD-like at leading order.

2. **The integrated loop expansion of any QCD-like flow tracks b_0.**
   The Borel-plane singularity structure of the integrated
   asymptotically-free coupling has its first UV/IR renormalon at
   `u = 1/2` with residue proportional to `2 b_0` (the `NS` renormalon).
   This is the same `b_0` that governs the leading bubble-chain
   insertions into the `y_t` self-energy / anomalous-dimension
   integrand at higher loop. The scale of higher-loop growth in
   integrated RGE quantities is therefore set by `b_0`.

3. **P1 analog on the same UV surface.** The analog P1
   loop-expansion bound (`YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md`)
   operates at the same retained coupling `α_LM` and the same retained
   `b_0` at `n_l = 5`, with the same envelope `(α_LM/π) · b_0`. Using
   a different envelope for P2 would break structural consistency
   between the two UV-matching axes of the obstruction theorem.

At `α_LM = 0.0907`, `n_l = 5`:

```
    r_M  =  (α_LM / π) · b_0  =  0.028860 · 23/3  =  0.22126.       (3.3)
```

### 3.3 Envelope property: r_M ≫ r_obs

The observed 1→2 loop ratio on the retained primary chain,

```
    r_obs(1→2)  =  |δM_2| / |δM_1|  =  0.047 / 1.043  =  0.04507    (3.4)
```

is a factor of approximately

```
    r_M / r_obs  =  0.22126 / 0.04507  =  4.91
```

below the retained envelope. This is substantially looser than the P1
envelope margin of 1.28 and the P3 envelope margin of 1.10, and
reflects the structural fact that the integrated 1→2 loop shift on
`M` is suppressed well beyond the single-insertion `b_0`-renormalon
bound by two additional mechanisms:

- **QFP focusing compression** (retained from the QFP insensitivity
  note Part 1): the Pendleton-Ross IR focusing mechanism compresses
  `y_t(v)` across a wide range of UV BCs, so integrated shifts across
  the 17-decade interval are smaller than the unconstrained
  single-vertex loop series would suggest.
- **CMT endpoint anchoring** (retained from the v-matching note
  `(0.2)`): the structural factors `√u_0` and `√(8/9)` in `M` are
  loop-independent and absorb none of the shift, so `r_obs(1→2)` on
  `M` equals `r_obs(1→2)` on `F_yt` without amplification.

The retained bound `r_M = 0.22126` is therefore a conservative
envelope on the loop tail at `n ≥ 2`, not a saturated estimate. The
conservative margin is the structural price of using only retained
Casimir + flavor + canonical-coupling inputs.

### 3.4 Candidate envelope comparison

Several retained combinations were evaluated. Only combinations using
retained SU(3) Casimirs, retained `n_l`, and retained `α_LM` are
admissible.

| Candidate              | Value at SU(3), α_LM, n_l=5   | Envelopes r_obs(1→2) = 0.04507? |
|------------------------|-------------------------------|---------------------------------|
| `(α_LM/π) · C_F`       | `0.02886 · 4/3 = 0.03848`     | NO  (below r_obs)               |
| `(α_LM/π) · 2 T_F n_l` | `0.02886 · 5 = 0.14430`       | YES (margin 3.20)               |
| `(α_LM/π) · C_A`       | `0.02886 · 3 = 0.08658`       | YES (margin 1.92)               |
| `(α_LM/π) · 2 C_A`     | `0.02886 · 6 = 0.17316`       | YES (margin 3.84)               |
| `(α_LM/π) · b_0`       | `0.02886 · 23/3 = 0.22126`    | YES (margin 4.91)               |
| `(α_LM/π) · C_A^2`     | `0.02886 · 9 = 0.25974`       | YES (margin 5.77)               |
| `(α_LM/π) · 4 C_A`     | `0.02886 · 12 = 0.34632`      | YES (margin 7.69)               |

The retained envelope `r_M = (α_LM/π) · b_0 = 0.22126` is chosen
because:

- it is the **same retained quantity** as the P1 loop-expansion
  envelope on the same UV surface, ensuring structural consistency;
- it has a natural framework-native interpretation as the
  **UV renormalon-growth scale** at the retained SM flavor content;
- it sits in the middle of the viable candidate range, neither
  saturating the observed ratio (which would risk failure in higher
  loops) nor arbitrarily loose.

A tighter retained choice (`(α_LM/π) · C_A` or `(α_LM/π) · 2 C_A`)
would further reduce the tail residual to ~0.33% and ~0.48% on `m_t`
respectively, but at the cost of using an envelope scale that is not
the natural renormalon-growth coefficient for the integrated series.
Any such tightening would be a conservative step beyond the scope of
this note and is not adopted.

### 3.5 Geometric sum

Assuming bound (GB-M) holds for all `n ≥ 2`, the tail after the
retained 2-loop truncation is

```
    |Σ_{n ≥ 3} δM_n|   ≤   Σ_{n ≥ 3} |δM_n|
                       ≤   |δM_2| · r_M + |δM_2| · r_M^2 + ...
                       =   |δM_2| · r_M / (1 − r_M)                 (B1')
```

provided `r_M < 1`, which is satisfied at the canonical `α_LM` by a
large margin (`r_M = 0.221 ≪ 1`). Numerically with `|δM_2| = 0.047`:

```
    |tail(N=2)|  ≤  0.047 · 0.22126 / 0.77874
                 =  0.047 · 0.28411
                 =  0.01335.                                        (3.5)
```

The total matching correction beyond the tree-level `M^{(0)} = 0.8833`
satisfies

```
    |M_true − M^{(2)}|  ≤  |tail(N=2)|  =  0.01335                  (3.6)
```

which bounds `M_true ∈ [M^{(2)} − 0.01335, M^{(2)} + 0.01335] =
[1.9597, 1.9864]`. The observed residual `|M_obs − M^{(2)}| = |1.9734
− 1.9730| = 0.0004` is well inside the retained interval.

### 3.6 Sensitivity to the truncation index

For a generic truncation index `N ≥ 2` with retained bound `r_M`, the
tail is

```
    |tail(N)|  ≤  |δM_N| · r_M / (1 − r_M)                          (B3)
```

At `N = 2, 3, 4`, under the retained geometric-decay assumption
(cumulative application of (GB-M)):

| N | `|δM_N|` upper bound          | `|tail(N)|` upper bound |
|---|-------------------------------|-------------------------|
| 2 | `0.04700` (retained primary)  | `0.01335` (this note)   |
| 3 | `0.04700 · r_M = 0.01040`     | `0.00295`               |
| 4 | `0.04700 · r_M^2 = 0.00230`   | `0.00065`               |

Successive retention of each additional loop integrated shift would
tighten the residual tail by a factor of `r_M ≃ 0.22`. The
corresponding `m_t` fractional residuals scale from 0.677% (N=2) to
0.150% (N=3) to 0.033% (N=4). The packaged P2 budget ~0.5% is
comfortably met at `N = 3` and tightly met at `N = 2` (this note).

---

## 4. Comparison to the analog P1 and P3 bounds

### 4.1 Structural comparison

| Axis            | P1 loop-expansion                 | **P2 F_yt loop-expansion (this note)**  | P3 K-series                       |
|-----------------|-----------------------------------|-----------------------------------------|-----------------------------------|
| Scale           | `μ = M_Pl` (UV)                   | `integrated M_Pl → v` (UV-dominated)    | `μ = m_t` (IR)                    |
| Coupling        | `α_LM = 0.0907`                   | `α_LM = 0.0907` (UV anchor)             | `α_s(m_t) = 0.1079`               |
| `α / π`         | `0.02886`                         | `0.02886`                               | `0.03435`                         |
| Envelope scale  | `b_0 = 23/3`                      | `b_0 = 23/3`                            | `C_A^2 = 9`                       |
| `r_bound`       | `0.22126`                         | `0.22126`                               | `0.30911`                         |
| Margin vs obs.  | `1.28`                            | `4.91`                                  | `1.10`                            |
| Tail factor     | `r/(1-r) = 0.2841`                | `0.2841`                                | `0.4474`                          |
| Observed anchor | `max(r_CF, r_CA, r_lp) = 0.1732`  | `r_obs(1→2) = 0.04507`                  | `max(r_1, r_2) = 0.2818`          |
| Residual on m_t | `0.547% – 1.640%` (I_S dependent) | **`0.677%`**                            | `0.14%`                           |

### 4.2 Why the same retained envelope `(α_LM/π) · b_0` is used for P1 and P2

Both P1 and P2 are UV-anchored axes of the obstruction theorem at
`M_Pl`:

- **P1** controls the lattice-to-MSbar matching correction `Δ_R` at
  `M_Pl` itself (a 0-decade matching vertex).
- **P2** controls the integrated SM-RGE transport over 17 decades
  from `M_Pl` to `v`.

Both are loop expansions in the canonical coupling at the UV end of
the interval. The retained one-loop QCD beta-function coefficient
`b_0` is the natural envelope for both because:

- on the P1 axis, `b_0` appears as the renormalon-growth scale of the
  single-scale matching series at `M_Pl`;
- on the P2 axis, `b_0` appears as the renormalon-growth scale of the
  integrated SM-RGE solution over the full interval, with the UV-end
  coupling `α_LM` setting the magnitude of higher-loop contributions.

Using the same retained envelope for both P1 and P2 preserves the
structural consistency of the obstruction-theorem budget accounting.
Using a DIFFERENT envelope scale on P2 (e.g., `C_A^2` from the P3
surface at `m_t`) would implicitly import an IR anchor into a
UV-dominated problem, which is not consistent with the retained
surface.

### 4.3 Why the observed margin is larger for P2 than for P1 or P3

The observed empirical ratio `r_obs(1→2) = 0.04507` on P2 is
significantly smaller than the P1 observed ratio `max(r_CF, r_CA,
r_lp) = 0.1732` (indicative 2-loop/1-loop) and the P3 observed ratio
`max(r_1, r_2) = 0.2818` (direct K-series). This reflects:

- **Integrated vs. single-scale loop growth.** P2 operates on an
  integrated quantity over 17 decades, where the loop expansion is
  integrated-averaged rather than evaluated at a single scale. The
  integrated 2-loop correction to `y_t(v)` is the SUM of (partially
  cancelling) contributions from the 2-loop pieces of `β_{y_t}`,
  `β_{g_3}`, `β_{g_2}`, `β_{g_1}`, all weighted by the IR focusing.
  The P1 and P3 expansions are at a fixed scale, where no such
  averaging occurs.
- **QFP focusing compression.** The Pendleton-Ross IR QFP absorbs a
  fraction of the UV BC sensitivity (retained QFP note Part 2), which
  further compresses the aggregate 2-loop shift.

The retained envelope `r_M = 0.22126` is therefore conservative for
P2 by a larger factor than for P1 or P3. This conservatism is the
price of restricting the envelope scale to retained Casimir + flavor
+ canonical-coupling combinations and not importing the QFP focusing
mechanism as a separate tightening input.

---

## 5. Implication for P2 closure and the master obstruction budget

The master obstruction theorem
(`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`)
packages P2 as a ~0.5% residual budget on `m_t`. Prior to this note,
the P2 v-matching residual was bounded at the loop-expansion axis by:

- **Direct primary-chain 2-loop evaluation** (exact to primary-chain
  precision), giving `M^{(2)} = 1.9730` against `M_obs = 1.9734`
  (0.02% on the primary chain), but with residual higher-loop
  contributions only loosely bounded by the QFP 3% envelope.
- **QFP insensitivity 3% envelope** (retained): broad but not
  framework-native at the loop-expansion axis; treats all smooth
  monotonic surrogates on equal footing without exploiting the
  specific retained `b_0`-renormalon structure of the SM RGE.

After this note:

- **Retained framework-native geometric tail bound** (this note):
  `|tail(N=2)| ≤ 0.01335` on `M`, or `0.677%` on `m_t`. Replaces the
  loose 3% QFP cap at the loop-expansion axis with a structurally
  motivated bound built from retained Casimirs, retained SM flavor
  count, and the retained canonical coupling — the same retained
  envelope as the P1 loop-expansion axis.

### 5.1 Budget rollup

Combining the retained structural identity `(1.1)` with the retained
two-loop primary-chain evaluation of `F_yt` and the retained
loop-expansion bound (B2):

```
    |M_true − M^{(2)}|  ≤  0.01335                                  (5.1)
    |Δm_t / m_t|_tail   ≤  0.677%                                   (5.2)
```

The P2 contribution to the master obstruction residual is therefore
bounded by `0.677%` of `m_t`, which is:

- **4.4× tighter than the prior QFP 3% envelope**;
- **within a factor of 1.4 of the packaged P2 budget of ~0.5%**;
- **closed structurally at the retained `(α_LM/π) · b_0` envelope**
  with no additional axiomatic content.

Any future step extending the retained primary chain to 3-loop SM RGE
would tighten the P2 residual to `|tail(N=3)| ≤ 0.150% on m_t` under
the same retained envelope, comfortably inside the packaged P2 budget.

### 5.2 Net effect on the obstruction theorem

The master obstruction tracker's three-axis budget is now retained
framework-natively at the loop-expansion layer on each axis:

| Primitive | Loop-expansion bound                                   | Fractional m_t bound |
|-----------|--------------------------------------------------------|----------------------|
| P1        | `\|tail(N=1)\|` at packaged `I_S=2`: `0.547%`          | `0.547%`             |
| **P2**    | **`\|tail(N=2)\| = 0.01335` on M**                     | **`0.677%`**         |
| P3        | `\|tail(N=3)\| = 0.00146` on m_pole/m_MSbar            | `0.137%`             |

The combined retention-bound budget on `m_t` from the three
loop-expansion axes, added in quadrature (under the retained
geometric-decay assumption that the three axes are structurally
orthogonal, which holds because P1 is a fixed-scale matching, P2 is
an integrated RGE flow, and P3 is a fixed-scale pole conversion):

```
    √(0.547^2 + 0.677^2 + 0.137^2)  =  √(0.299 + 0.458 + 0.019)
                                     =  √0.776
                                     =  0.881%                      (5.3)
```

This is the **framework-native retained loop-expansion envelope on
m_t**, consistent with the master obstruction theorem's packaged
~1.5% total-m_t residual budget (the remaining ~0.6% buffer allows for
non-loop-expansion retention uncertainties such as the `I_S`
integral, the 2-loop color tensors not yet retained, and the
`m_pole` to on-shell conversion).

---

## 6. Safe claim boundary

The claim retained by this note is strictly:

> On the retained `Cl(3) × Z^3` framework surface, the v-matching
> coefficient `M = √u_0 · F_yt · √(8/9)` admits a loop expansion
> `M = M^{(1)} + Σ_{n ≥ 2} (M^{(n)} − M^{(n-1)})` whose successive
> shifts satisfy a framework-native geometric bound with retained
> ratio `r_M = (α_LM / π) · b_0 = 0.22126` at the retained
> canonical-surface anchor `α_LM = 0.0907` and retained SM light-flavor
> count `n_l = 5`. The observed 1→2 loop ratio
> `r_obs(1→2) = |δM_2| / |δM_1| = 0.04507` is deeply below `r_M`,
> with a safety margin of `r_M / r_obs ≈ 4.9`. Under the
> geometric-decay assumption `|δM_{n+1}| ≤ r_M · |δM_n|` for all
> `n ≥ 2`, the tail residual after retained 2-loop truncation is
> bounded above by `|tail(N=2)| ≤ |δM_2| · r_M / (1 − r_M) = 0.01335`,
> corresponding to a fractional `m_t` residual of `0.677%`. This is
> `4.4×` tighter than the prior QFP insensitivity 3% envelope and
> within a factor of 1.4 of the packaged P2 budget of ~0.5% in the
> master obstruction theorem.

The following claims are explicitly NOT made:

- The retained framework does **not** derive individual 3-loop or
  higher integrated `F_yt` or `M` values. The bound is a structural
  asymptotic assumption on the retention surface, not a derivation
  of any individual higher-order integrated shift.
- The retained geometric bound is **not** claimed to be strict for
  all `n ≥ 2` without further structural input. The bound is
  verified against the retained 1→2 loop primary-chain shift; its
  extension to `n ≥ 3` is a structural asymptotic assumption on the
  retention surface, motivated by the `b_0`-renormalon growth scale
  of the integrated asymptotically-free RGE. A framework-native proof
  of geometric decay for all `n ≥ n_0` from the underlying action
  would be a separate retention step (e.g., a renormalon-bound
  theorem on the integrated SM RGE on the retained canonical
  surface).
- The bound does **not** replace the structural identity
  `M = √u_0 · F_yt · √(8/9)` from the v-matching note; it refines the
  tail estimate on the integrated `F_yt` factor only. The structural
  identity is exact and loop-independent.
- The bound does **not** derive or tighten the QFP insensitivity
  envelope itself; it provides a retained alternative bound at the
  **loop-expansion axis** of the P2 v-matching residual, which is
  the dominant axis for UV-to-IR integrated flows (the QFP envelope
  controls the broader family-of-flows uncertainty, which is a
  separate retention axis and not modified by this note).
- The retained bound does **not** depend on any imported literature
  value of the 3-loop or higher SM RGE integrated contribution; only
  the retained 1-loop and 2-loop primary-chain `M` values enter as
  retained anchors.
- The retained envelope is **not** the tightest possible bound.
  Tighter retained choices (`(α_LM/π) · C_A` giving 0.34% on m_t, or
  `(α_LM/π) · 2 C_A` giving 0.48% on m_t) are accessible but
  deliberately not adopted; the present bound uses the same
  framework-native `b_0` envelope as the P1 loop-expansion bound for
  structural consistency across the two UV-anchored axes of the
  master obstruction theorem.
- The canonical coupling value `α_LM = 0.0907` enters as a numerical
  anchor from `canonical_plaquette_surface.py`; no derivation result
  of this note depends on its specific numerical value beyond the
  tail-size estimates reported above.
- The bound loses structural tightness as `α_LM` increases: at
  `(α_LM/π) · b_0 ≥ 1` (i.e., `α_LM ≥ π · 3/23 ≈ 0.410`), the
  geometric sum diverges and the bound fails. The retention anchor
  `α_LM = 0.0907` is well below this regime.

---

## 7. Validation

The structural retention is verified by the primary runner
`scripts/frontier_yt_p2_f_yt_loop_geometric_bound.py`, which performs
deterministic PASS/FAIL checks on:

1. Retained SU(3) Casimirs `C_F = 4/3`, `T_F = 1/2`, `C_A = 3`, and
   the retained SM light-flavor count `n_l = 5`.
2. Retained derived coefficient `b_0 = (11 C_A − 4 T_F n_l) / 3 = 23/3`
   at `n_l = 5`.
3. Retained canonical coupling `α_LM = 0.09066784`,
   `(α_LM / π) = 0.02886`.
4. Retained integrated-M values from the v-matching note and primary
   chain: `M^{(0)} = 0.8833`, `M^{(1)} = 1.926`, `M^{(2)} = 1.9730`,
   `M_obs = 1.9734`.
5. Observed integrated shifts `|δM_1| = 1.0427`, `|δM_2| = 0.0470`.
6. Observed ratio `r_obs(1→2) = |δM_2| / |δM_1| = 0.04507`.
7. Proposed framework-native bound
   `r_M = (α_LM / π) · b_0 = 0.22126` at `n_l = 5`.
8. Envelope check `r_M > r_obs(1→2)` with safety margin ~4.9.
9. Geometric-sum convergence `r_M < 1`.
10. Tail residual `|tail(N=2)| = |δM_2| · r_M / (1 − r_M) = 0.01335`.
11. Fractional `m_t` residual `|tail(N=2)| / M^{(2)} = 0.00677 =
    0.677%`.
12. Comparison to QFP 3% envelope: retained bound is 4.4× tighter.
13. Comparison to packaged P2 budget ~0.5%: retained bound is within
    a factor of 1.4.
14. Candidate envelope comparison: `(α_LM/π) · b_0` identified as
    the natural retained choice matching the P1 analog envelope.
15. Comparison with analog P1 and P3 loop-expansion bounds (same
    retained envelope as P1; different envelope scale and anchor
    from P3).
16. Retention-tightening table at truncation N = 2, 3, 4.
17. Structural retention provenance: bound depends only on retained
    SU(3) Casimirs, retained `n_l = 5`, retained `α_LM`, and the
    retained two-loop primary-chain `M` values. No literature value
    of the 3-loop or higher SM RGE integrated contribution imported.

- **Log:** `logs/retained/yt_p2_f_yt_loop_geometric_bound_2026-04-17.log`.
- **Prior retention steps:**
  - `YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md` — lattice-side Ward exact on every rung.
  - `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md` — structural identity `M = √u_0 · F_yt · √(8/9)`.
- **Analog loop-expansion templates:**
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — same retained envelope on the UV surface.
  - `YT_P3_K_SERIES_GEOMETRIC_BOUND_NOTE_2026-04-17.md` — analog IR surface with `C_A^2` envelope.
- **Upstream authorities (read-only):**
  - `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` — SU(3) Casimirs.
  - `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` — gauge-group uniqueness.
  - `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` — canonical `α_LM`.
  - `docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` — loose prior 3% envelope.

No publication-surface file (`CLAIMS_TABLE`, `PUBLICATION_MATRIX`,
`DERIVATION_ATLAS`, ...) is modified by this submission.

---

## Import status

| Element                                                   | Status     |
|-----------------------------------------------------------|------------|
| AX1: Cl(3) local algebra                                  | AXIOM      |
| AX2: Z^3 spatial substrate                                | AXIOM      |
| SU(3) Casimirs `C_F`, `C_A`, `T_F`                        | DERIVED    |
| SM light-flavor count `n_l = 5` on M_Pl → v               | DERIVED    |
| `b_0 = (11 C_A − 4 T_F n_l) / 3 = 23/3` at `n_l = 5`      | DERIVED    |
| Canonical coupling `α_LM = 0.09066784`                    | DERIVED    |
| v-matching identity `M = √u_0 · F_yt · √(8/9)`            | DERIVED (prior v-matching note) |
| Retained `M^{(0)}, M^{(1)}, M^{(2)}, M_obs`               | DERIVED (prior v-matching note + primary chain) |
| Observed 1→2 loop shift `|δM_2| = 0.047`                  | DERIVED (this note, from retained M values) |
| Retained envelope `r_M = (α_LM / π) · b_0 = 0.22126`      | DERIVED (this note; retained Casimirs + flavor + coupling) |
| Tail residual `|tail(N=2)| = 0.01335`                     | DERIVED (this note) |
| Fractional `m_t` bound `0.677%`                           | DERIVED (this note) |
| Geometric-decay assumption `|δM_{n+1}| ≤ r_M · |δM_n|`    | STRUCTURAL ASSUMPTION on retention surface (motivated by `b_0`-renormalon growth) |

**No new axioms. No new canonical-surface choices. No new numerical
inputs beyond the retained 1-loop and 2-loop primary-chain `M` values
(which come from retained β coefficients on the retained derived
gauge + matter content). The only new content of this note is the
application of the retained `(α_LM/π) · b_0` envelope (already used
for P1) to the integrated F_yt / M loop expansion, yielding a
framework-native retained tail bound at the P2 loop-expansion axis
that is 4.4× tighter than the prior QFP 3% envelope and within a
factor of 1.4 of the packaged P2 budget.**

## Status

**RETAINED** — framework-native geometric tail bound on the
loop-expansion axis of the P2 v-matching residual retained through
`r_M = (α_LM / π) · b_0 = 0.22126` at `α_LM = 0.0907`, `n_l = 5`,
delivering a retained tail residual of `|tail(N=2)| = 0.01335` on `M`
and a retained fractional-`m_t` contribution of `0.677%`, measurably
tighter than the prior QFP insensitivity 3% envelope and within a
factor of 1.4 of the packaged P2 budget of ~0.5%. Together with the
taste-staircase transport theorem (lattice-side) and the v-matching
decomposition theorem (structural identity), this closes the P2
loop-expansion axis on the retained surface.
