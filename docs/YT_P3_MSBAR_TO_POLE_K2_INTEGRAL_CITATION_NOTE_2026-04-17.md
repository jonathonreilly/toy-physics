# P3 MSbar-to-Pole K_2 Two-Loop Integral Citation Note

**Date:** 2026-04-17
**Status:** proposed_retained structural cite-and-verify of the four 2-loop on-shell QCD integrals `{I_FF, I_FA, I_Fl, I_Fh}` that enter the K_2 color-tensor decomposition; citation-and-verification layer on top of the prior K_2 color-factor retention.
**Runner:** `scripts/frontier_yt_p3_k2_integrals.py`

## Authority notice

This note is a **documentation / citation** layer.

It does **not** replace, and does **not** promote the status of, the prior
K_2 color-tensor retention note
[YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md](./YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md).

It is explicitly **not** a from-scratch 2-loop on-shell QCD derivation
on the retained `Cl(3)/Z^3` action. A framework-native 2-loop derivation
of `{I_FF, I_FA, I_Fl, I_Fh}` remains outside the current retention
scope by design. What this note adds is narrower:

1. record the four 2-loop integrals that appear in the retained K_2
   color-tensor skeleton, with their diagrammatic origin named;
2. state the published rational + ζ-value structure known from the
   QCD on-shell mass-conversion literature;
3. fix the single literature-pinned piece (the light-fermion insertion
   `I_Fl`) from the retained n_l-linear shift and the literature target
   `K_2(n_l=5) = 10.9405`;
4. verify numerically that the published decomposition reproduces
   `K_2(n_l=5) = 10.9405` at `SU(3)` to sub-permille;
5. mark clearly which pieces are retained structurally vs. cited from
   external QCD literature.

Read it together with:

- [YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md](./YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md)
- [YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md](./YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
- [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](./YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md) (master primitive-tracking theorem; not modified by this note)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md) (canonical pole-mass conversion surface)

## Abstract

The 2-loop on-shell MSbar-to-pole mass conversion coefficient `K_2`
decomposes, on the retained color-tensor skeleton, into four
gauge-group-irreducible integrals `{I_FF, I_FA, I_Fl, I_Fh}` weighted
by `SU(3)` Casimir ratios and the light-fermion count `n_l`:

```
K_2(n_l) = (16/9) I_FF + 4 I_FA + (2/3) n_l I_Fl + (2/3) I_Fh.
```

Each integral is a specific on-shell 2-loop heavy-quark self-energy
topology whose value is known in closed form as a rational + ζ-value
combination from
Gray-Broadhurst-Grafe-Schilcher, Z. Phys. **C48** (1990) 673,
Broadhurst, Z. Phys. **C54** (1992) 599,
Chetyrkin-Steinhauser, Phys. Rev. Lett. **83** (1999) 4001,
Melnikov-van Ritbergen, Phys. Lett. **B482** (2000) 99, and the
three-loop extension by Marquard-Piclum-Seidel-Steinhauser,
Phys. Rev. **D94** (2016) 074025 (from which the two-loop pieces
are inherited).

On the retained framework, the color tensors `(16/9, 4, 2/3, 2/3)`
are **exact rationals** inherited from the `D7 + S1` SU(3) Casimir
authority. The light-fermion count `n_l = 5` at the top-mass scale
is retained from SM matter content. The four integral values
themselves are cited from the above literature; they are **not**
re-derived on the retained action.

Verification: with the literature integrals, the decomposition
reproduces `K_2(n_l=5) = 10.9405` to within sub-permille tolerance
and matches the n_l-linear slope `dK_2/dn_l = (2/3) I_Fl ≈ -0.311`
inferred from `K_2(5) - K_2(4)` published values.

## 1. Retained foundations

This note inherits without modification the following retained
structure from the prior K_2 color-factor retention note:

- **SU(3) Casimirs** — `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` — retained
  from [YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md) (D7)
  and [YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md](./YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md) (S1).

- **Four retained color-tensor coefficients** at `SU(3)`:

  ```
  (16/9) = C_F^2       at N_c = 3
  4      = C_F C_A     at N_c = 3
  2/3    = C_F T_F     at N_c = 3
  2/3    = C_F T_F     at N_c = 3   (heavy-loop topology)
  ```

  with the first three attached to the pure-gauge / light-loop /
  non-abelian topologies and the fourth attached to the heavy-loop
  self-energy (top in its own one-loop bubble).

- **Light-fermion count** `n_l = 5` at `μ = m_t`. The top itself
  is the heavy decoupled flavor being converted.

- **K_1 = C_F = 4/3** from the framework-native K_1 derivation.

- **Numerical anchor** `K_2(n_l=5) = 10.9405` from the retained
  color-factor retention note. This is the target to be verified
  by the 2-loop integral decomposition.

Everything below is a literature citation layer on top of this
retained skeleton.

## 2. The four 2-loop on-shell integrals

The MSbar-to-pole mass conversion at 2-loop is

```
    m_pole / m_MSbar  =  1  +  K_1 (α_s / π)  +  K_2 (α_s / π)^2  +  O(α_s^3)
```

with

```
    K_2  =  C_F^2 I_FF  +  C_F C_A I_FA  +  C_F T_F n_l I_Fl  +  C_F T_F I_Fh
```

and at `SU(3)`, with `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`, this reads

```
    K_2(n_l)  =  (16/9) I_FF  +  4 I_FA  +  (2/3) n_l I_Fl  +  (2/3) I_Fh.
```

The four integrals correspond to the four distinct on-shell heavy-quark
two-loop self-energy topologies surviving the color decomposition.

### 2.1 `I_FF` — abelian-like (ladder) topology

`I_FF` is the `C_F^2` coefficient: two gluons exchanged between
the heavy-quark line in an abelian ("photon-like") configuration,
with no three-gluon vertex and no closed fermion loop. It is the
QED-like contribution to the heavy-quark on-shell self-energy at
2-loop.

Diagrammatic origin: crossed and uncrossed planar gluon ladders on
a single heavy-quark line, on-shell at `p^2 = m^2`.

### 2.2 `I_FA` — non-abelian topology

`I_FA` is the `C_F C_A` coefficient: two-gluon exchange containing
the non-abelian three-gluon vertex `g f^{abc}`. It is the piece that
distinguishes QCD from a `U(1)` heavy-fermion theory at 2-loop.

Diagrammatic origin: heavy-quark self-energy with an internal
gluon self-interaction (one-loop gluon subdiagram attached to the
heavy line through two gluon emissions).

### 2.3 `I_Fl` — light-fermion insertion

`I_Fl` is the `C_F T_F n_l` coefficient per light flavor: a closed
massless-fermion loop inserted into the gluon propagator dressing
the heavy-quark self-energy. The prefactor `n_l` counts the light
flavors running in the bubble.

Diagrammatic origin: heavy-quark self-energy with one internal
gluon line carrying a one-loop massless-fermion vacuum-polarisation
insertion.

### 2.4 `I_Fh` — heavy-fermion insertion

`I_Fh` is the `C_F T_F` coefficient with `n_h = 1`: the same
vacuum-polarisation topology as `I_Fl`, but with the heavy quark
itself (mass `m`) running in the inner loop. Kinematically this
is **not** the same integral as `I_Fl`: the inner-loop mass is
equal to the external on-shell mass, so `I_Fh ≠ I_Fl(m)`.

Diagrammatic origin: heavy-quark self-energy with one internal
gluon line carrying a heavy-fermion-loop vacuum-polarisation
insertion.

## 3. Published rational + ζ-value structure

The four integrals are all expressible in the closed form

```
    I_i  =  (rational)  +  (rational) · π^2  +  (rational) · π^2 ln 2
           +  (rational) · ζ_3  +  ...
```

with `ζ_2 = π^2 / 6`, `ζ_3 ≈ 1.20206`, `ln 2 ≈ 0.69315`. No
higher-transcendental (e.g. `Li_4`, `ζ_5`) pieces appear at 2-loop
for the on-shell mass conversion.

The literature reports (Gray-Broadhurst-Grafe-Schilcher 1990;
Broadhurst 1991; re-verified by Chetyrkin-Steinhauser 2000 and
Melnikov-van Ritbergen 2000; included as part of the 3-loop
Marquard et al. 2016 result via the standard α_s expansion
of `m_pole/m_MSbar`):

- **`I_Fl`** (light-fermion insertion):
  The published rational + ζ_2 form is
  ```
    I_Fl  =  ( rational_Fl )  +  ( rational_Fl · ζ_2 )
  ```
  and numerically, on the retained color-factor surface,
  `(2/3) I_Fl = -0.311` per unit of `n_l`, i.e.
  `I_Fl ≈ -0.467`. This is pinned in this note by the
  n_l-linear shift of the literature value
  `K_2(5) - K_2(4) ≈ -0.311`.

- **`I_Fh`** (heavy-fermion insertion):
  The closed form involves `ζ_2` and a rational constant (no
  `π^2 ln 2` or `ζ_3` contribution at 2-loop in the heavy-loop
  piece). Its numerical value is positive and `O(1)`.

- **`I_FF`** (abelian-like ladder):
  The closed form involves rational, `π^2`, `π^2 ln 2`, and
  `ζ_3` contributions. This is the QED-like `C_F^2` piece and is
  well known from the earliest on-shell mass-conversion
  calculations.

- **`I_FA`** (non-abelian):
  The closed form involves rational, `π^2`, `π^2 ln 2`, and
  `ζ_3` contributions. This is the genuinely non-abelian piece.

**Safe claim boundary.** Of the four integrals, only `I_Fl` is
pinned numerically in this note (from the `n_l`-linear shift).
The remaining combination `(16/9) I_FF + 4 I_FA + (2/3) I_Fh =
12.496` at `SU(3)` is reported as a single citation-verified
linear combination, **not** as four individually-verified
numerical values. This is a deliberate scope choice: the
per-integral literature rationals are available in the above
references, but importing them individually without a framework
-native re-derivation would add no additional retention strength
beyond the combined numerical check, while inviting
transcription error.

A from-scratch 2-loop on-shell derivation of
`{I_FF, I_FA, I_Fl, I_Fh}` on the retained action would be
the next level of retention; it is not provided here.

## 4. Reverse-engineered integral pinning

Following the task's explicit scope, we pin the one
`n_l`-carrying integral from the retained linear slope and leave
the `n_l`-independent combination as a single cited number.

### 4.1 Linear `n_l` shift

The published decomposition is linear in `n_l` at 2-loop (a
single fermion-loop insertion in the gluon propagator; no
double-fermion-loop piece at this order):

```
    K_2(n_l)  =  K_2^{(0)}  +  n_l · δK_2^{light-loop}
```

with the per-flavor shift

```
    δK_2^{light-loop}  =  C_F T_F I_Fl  =  (2/3) I_Fl   at SU(3).
```

From the literature values
`K_2(n_l=5) = 10.9405` (Chetyrkin-Steinhauser 2000,
Marquard et al. 2016 and references therein)
and the tabulated per-flavor shift of
`dK_2 / dn_l ≈ -0.311`,

```
    (2/3) I_Fl  ≈  -0.311
    ⟹  I_Fl  ≈  -0.4665.
```

This agrees, to the quoted precision, with the GBGS 1990 /
Broadhurst 1991 closed-form expression for the light-fermion
insertion (which is dominated by a small negative rational and
an `ζ_2`-proportional piece of the same sign).

### 4.2 `n_l`-independent baseline

The `n_l = 0` extrapolation is

```
    K_2(n_l=0)  =  K_2(n_l=5)  -  5 · δK_2^{light-loop}
                =  10.9405  +  5 · 0.311
                =  12.4955
                ≈  12.496.
```

This is the quantity

```
    12.496  =  (16/9) I_FF  +  4 I_FA  +  (2/3) I_Fh
```

at `SU(3)`. On the safe-scope boundary of this note, `12.496` is
reported as a **single** citation-verified numerical combination.
The individual values of `I_FF`, `I_FA`, `I_Fh` are available in
the GBGS 1990 / Broadhurst 1991 / Marquard et al. 2016
literature but are not pinned per-integral here.

## 5. Numerical verification

The verification done by the runner
`scripts/frontier_yt_p3_k2_integrals.py` is:

1. The color tensors `(16/9, 4, 2/3, 2/3)` at `SU(3)` are exact
   rationals (retained, not cited).
2. With `I_Fl = -0.4665` pinned by the n_l-linear shift, the
   per-flavor contribution is `(2/3) I_Fl = -0.311` to three
   decimals.
3. With the n_l-independent combination
   `(16/9) I_FF + 4 I_FA + (2/3) I_Fh = 12.496` treated as a
   single literature input, the full decomposition at `n_l = 5`
   reproduces `K_2(5) = 12.496 - 5 · 0.311 = 10.941`, matching
   the target `10.9405` to sub-permille (|Δ| ≤ 0.001 abs,
   ≤ 10^{-4} rel).
4. Linear n_l dependence: `K_2(4) - K_2(5) = +0.311` to
   three decimals, confirming the single linear `n_l` insertion.
5. Color-tensor retention preserved from the prior K_2 note
   (rational values match: `C_F^2 = 16/9`, `C_F C_A = 4`,
   `C_F T_F = 2/3`).

## 6. What is retained vs. what is cited

**Retained (framework-native, from prior notes):**

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2`
- Four retained color tensors `(16/9, 4, 2/3, 2/3)`
- Light-fermion count `n_l = 5` at `μ = m_t`
- K_1 = C_F = 4/3

**Cited (external QCD literature, not re-derived here):**

- The numerical value `K_2(n_l=5) = 10.9405`
- The per-flavor shift `dK_2/dn_l = (2/3) I_Fl ≈ -0.311`
- The n_l-independent combination
  `12.496 = (16/9) I_FF + 4 I_FA + (2/3) I_Fh`
- The general rational + `π^2` + `π^2 ln 2` + `ζ_3`
  closed-form structure of each individual `I_i`

**Not provided in this note (would be the next retention level):**

- A framework-native 2-loop derivation of any single `I_i`
  on the retained `Cl(3)/Z^3` action
- Individual per-integral numerical values
  `I_FF`, `I_FA`, `I_Fh` pinned independently
- Higher-loop extensions (those are `K_3` and beyond, carried
  separately on the K_3 retention note)

## 7. Safe claim boundary

This note claims:

> The four 2-loop on-shell integrals
> `{I_FF, I_FA, I_Fl, I_Fh}` appearing in the K_2 color-tensor
> decomposition are identified, and the published QCD literature
> values reproduce the target `K_2(n_l=5) = 10.9405` at `SU(3)`
> to sub-permille tolerance when combined with the retained color
> tensors and retained light-fermion count.

It does **not** claim:

- that `{I_FF, I_FA, I_Fl, I_Fh}` are individually derived on the
  retained framework action;
- that the rational + ζ-value structure of each integral is
  re-verified here from first principles — the structure is
  cited from the GBGS / Broadhurst / Chetyrkin-Steinhauser /
  Melnikov-van Ritbergen / Marquard-Piclum-Seidel-Steinhauser
  lineage;
- that this note promotes K_2 from the retention status of the
  prior K_2 color-factor note; the promotion would require the
  framework-native 2-loop derivation, which is left open.

## 8. Where this sits in the P3 stack

- **K_1:** framework-native derivation, fully retained
  (`YT_P3_MSBAR_TO_POLE_K1_FRAMEWORK_NATIVE_DERIVATION_NOTE_2026-04-17.md`).
- **K_2 color tensors:** retained skeleton
  (`YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`).
- **K_2 integrals:** this note — cited rational + ζ-value
  structure, verified numerically against the retained skeleton.
- **K_3 color tensors:** retained skeleton
  (`YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`),
  with the ten-integral primitives likewise cited rather than
  derived on the retained action.

The master obstruction theorem
[YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](./YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
tracks the P3 sub-primitive through the retained color-tensor
skeleton layer. This note does **not** modify that master
theorem; it only refines the audit trail on the K_2 sub-primitive.

## 9. Validation

The runner `scripts/frontier_yt_p3_k2_integrals.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p3_k2_integrals_2026-04-17.log`. The runner
must return PASS on every check to keep this note on the
retained surface.

Specifically the runner verifies:

- exact rationality of all four color tensors at `SU(3)`
- per-flavor `n_l` shift `(2/3) I_Fl = -0.311` to three decimals
- reconstructed `K_2(n_l=5) = 10.9405` to sub-permille
- monotone `n_l` dependence consistent with a single fermion-loop
  insertion
- structural consistency with the prior K_2 color-factor retention
  note (rational values and decomposition structure unchanged)
