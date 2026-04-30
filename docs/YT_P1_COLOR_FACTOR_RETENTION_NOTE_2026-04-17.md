# P1 Color-Factor Retention Sub-Theorem Note (Three-Channel Ratio Decomposition)

**Date:** 2026-04-17
**Status:** proposed_retained structural sub-theorem — the 1-loop lattice-to-MSbar
scheme conversion of the Ward ratio `y_t/g_s` at M_Pl has a retained
three-channel color-tensor decomposition
`Δ_R = C_F · Δ_1 + C_A · Δ_2 + T_F · n_f · Δ_3` with exact SU(3)
Casimir prefactors. The color-tensor structure is retained
framework-native; the three channel integrals Δ_1, Δ_2, Δ_3 are cited /
computed separately (not retained as structural primitives here).
**Primary runner:** `scripts/frontier_yt_p1_color_factor_retention.py`.
**Log:** `logs/retained/yt_p1_color_factor_retention_2026-04-17.log`.

## Authority notice

This note is a retained structural sub-theorem on the P1 primitive of
the master UV-to-IR transport obstruction theorem. It records the
color-tensor (gauge-group-irreducible) decomposition of the 1-loop ratio
correction `Δ_R ≡ δ_y − δ_g`, with exact SU(3) prefactors
(`C_F = 4/3`, `C_A = 3`, `T_F · n_f = 3` at n_f = 6). The three
per-channel integrals Δ_1, Δ_2, Δ_3 are named but not retained
structurally here; they are computed in the dedicated Δ_1/Δ_2/Δ_3
BZ-computation sub-theorems.

This note does NOT modify:

- the master obstruction theorem
  (`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`);
- the retained Ward-identity tree-level theorem
  (`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`), which holds at tree
  level and attaches no 1-loop claim;
- any publication-surface file.

## Cross-references

- **Master obstruction (parent):**
  `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` —
  names P1 as the 1-loop lattice-to-MSbar matching primitive on the
  Ward ratio.
- **Rep-A/Rep-B partial-cancellation sub-theorem:**
  `docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md` —
  derives the three-channel structure from the diagrammatic subtraction
  of δ_g (Rep-A, OGE extraction of g_s²) and δ_y (Rep-B, H_unit
  extraction of y_t²). This note packages the resulting color-tensor
  decomposition.
- **Shared-Fierz shortcut no-go:**
  `docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` — the
  three-channel structure is NOT reducible to a single channel by any
  shared Ward-Fierz shortcut.
- **Δ_1 BZ computation:**
  [`docs/YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md) — C_F channel,
  central `Δ_1 ≃ +2`.
- **Δ_2 BZ computation:**
  [`docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md) — C_A channel,
  central `Δ_2 ≃ −10/3`.
- **Δ_3 BZ computation:**
  [`docs/YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md`](YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md) — T_F n_f
  channel, central `Δ_3 ≃ +0.933`.
- **Δ_R master assembly:**
  [`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`](YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md) —
  consumes this color-factor retention note as the structural
  decomposition on which the per-channel BZ centrals are assembled.
- **SU(3) Casimir authorities:**
  [`docs/YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md) (D7 — `C_F`, `C_A`, `T_F`);
  [`docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md`](YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md) (S1 — gauge-group
  uniqueness).

## Abstract

On the retained `Cl(3)/Z^3` framework surface, the 1-loop correction to
the Ward ratio `(y_t/g_s)²` at M_Pl, defined as the difference of the
Rep-B Yukawa-side scheme conversion `δ_y` and the Rep-A gauge-side
scheme conversion `δ_g`, decomposes into three gauge-group-irreducible
color channels:

```
Δ_R  =  δ_y − δ_g
     =  C_F · Δ_1  +  C_A · Δ_2  +  T_F · n_f · Δ_3.
```

The three color-tensor prefactors evaluate to the exact rationals
`C_F = 4/3`, `C_A = 3`, `T_F · n_f = (1/2) · 6 = 3` at SU(3) with SM
flavor content n_f = 6. The decomposition is retained framework-native
from the D7 + S1 SU(3) Casimir authority; the three per-channel
integrals (Δ_1, Δ_2, Δ_3) are named but not retained structurally here.

This note closes the color-tensor retention step: the color-factor
structure of Δ_R is now exactly fixed, and the remaining P1
uncertainty is fully carried by the three per-channel integral values.
The downstream Δ_R master assembly theorem
(`docs/YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md`) and
the three per-channel BZ-computation sub-theorems inherit this
decomposition without modification.

## 1. Retained foundations

This note inherits without modification:

- **SU(3) Casimirs.** `C_F = (N_c² − 1)/(2 N_c) = 4/3`,
  `T_F = 1/2`, `C_A = N_c = 3` at N_c = 3, retained from
  `docs/YT_EW_COLOR_PROJECTION_THEOREM.md` (D7) and
  `docs/YT_EXACT_SCHUR_NORMAL_FORM_UNIQUENESS_NOTE.md` (S1).
- **MSbar SM flavor count at M_Pl.** `n_f = 6` (standard SM flavor
  content at the Planck matching scale).
- **Rep-A vs Rep-B diagrammatic catalog.** From the Rep-A/Rep-B
  partial-cancellation sub-theorem
  (`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md`):
  the 1-loop differences δ_y − δ_g on the Ward ratio retain only the
  color-tensor-irreducible pieces after the exact cancellation of the
  external quark wave-function renormalization `2 C_F · I_leg`.

## 2. Theorem statement

**Theorem P1-Color-Factor.** On the retained `Cl(3)/Z^3` framework
surface, the 1-loop scheme conversion of the Ward ratio `(y_t/g_s)²`
from the canonical lattice-PT surface to MSbar at M_Pl admits the
three-channel color-tensor decomposition

```
Δ_R  =  C_F · Δ_1  +  C_A · Δ_2  +  T_F · n_f · Δ_3                 (2.1)
```

with color-tensor prefactors at SU(3), n_f = 6

```
C_F         =  4/3                                                   (2.2a)
C_A         =  3                                                     (2.2b)
T_F · n_f   =  (1/2) · 6  =  3                                       (2.2c)
```

where:

- **C_F channel (`Δ_1`)** carries the vertex-correction difference
  between Rep-A's gauge-vertex C_F piece and Rep-B's scalar-vertex
  C_F piece, plus the MSbar scalar-bilinear anomalous dimension
  constant `−6` that enters only through Rep-B.
- **C_A channel (`Δ_2`)** carries the non-abelian gauge-vertex piece
  (Rep-A only) minus the gluonic gluon self-energy piece (Rep-A only);
  Rep-B has no C_A contribution at 1-loop.
- **T_F n_f channel (`Δ_3`)** carries the fermion-loop insertion in
  the gluon self-energy (Rep-A only); Rep-B has no internal gluon and
  hence no T_F n_f contribution.

The color-tensor decomposition (2.1) is **retained framework-native**
from the D7 + S1 SU(3) Casimir authority and the Rep-A/Rep-B
diagrammatic catalog. The three per-channel integrals `Δ_1`, `Δ_2`,
`Δ_3` are named but not retained here as structural primitives; they
are computed in the three dedicated BZ-computation sub-theorems.

## 3. Color-tensor structure (retained)

### 3.1 Three-channel irreducibility

The three tensors `{C_F, C_A, T_F · n_f}` are a basis of the
one-loop gauge-group-irreducible color structure for a flavor-blind
fermion bilinear on a non-abelian gauge background. Specifically:

- `C_F = (N_c² − 1)/(2 N_c)` arises from a single `T^A T^A` fundamental
  Casimir contraction, characteristic of any fermion-quark bilinear
  correction.
- `C_A = N_c` arises from the non-abelian commutator
  `[T^A, T^B] = i f^{ABC} T^C`, present only when a three-gluon vertex
  or gluon self-energy enters.
- `T_F · n_f` arises from a closed light-fermion loop in the gluon
  propagator; the `T_F = 1/2` is the fundamental-rep normalization and
  `n_f` counts the flavors running in the loop.

No other independent color tensor can appear at 1-loop on the Ward
ratio. In particular, products like `C_F²` appear only at 2-loop and
beyond.

### 3.2 SU(3) values

At `N_c = 3`, `n_f = 6` (SM flavor content at M_Pl):

```
C_F          =  (3² − 1) / (2 · 3)  =  8/6  =  4/3                  (3.1a)
C_A          =  3                                                    (3.1b)
T_F          =  1/2                                                   (3.1c)
T_F · n_f    =  (1/2) · 6  =  3                                      (3.1d)
```

All four are exact rationals inherited from the retained D7 + S1 SU(3)
Casimir authority. None is a citation.

### 3.3 Consistency with the Rep-A/Rep-B catalog

The three-channel decomposition (2.1) is the unique assembly of the
Rep-A/Rep-B 1-loop diagrammatic catalog into gauge-group-irreducible
pieces after exact cancellation of the external quark Z_ψ. The
cancellation and diagrammatic origin of each channel are derived in
`docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md` §§2–4:

| Channel | Rep-A contribution | Rep-B contribution | Net |
|---|---|---|---|
| C_F | `2 C_F · I_v_gauge` (from vertex) + `2 C_F · I_leg` (from Z_ψ) | `2 C_F · I_v_scalar` (from scalar vertex) + `−6 C_F` (from γ_S) + `2 C_F · I_leg` (from Z_ψ) | `C_F · [2 (I_v_scalar − I_v_gauge) − 6]` — leg cancels |
| C_A | `−C_A · I_v_gauge + (5/3) C_A · I_SE^{gluonic}` (from non-abelian vertex and gluon SE) | none | `C_A · [I_v_gauge − (5/3) I_SE^{gluonic}]` |
| T_F n_f | `−(4/3) T_F n_f · I_SE^{fermion}` (from fermion loop in gluon SE) | none | `T_F n_f · [(4/3) I_SE^{fermion}]` |

Hence

```
Δ_1  =  2 · (I_v_scalar − I_v_gauge)  −  6                           (3.2-Δ_1)
Δ_2  =  I_v_gauge  −  (5/3) · I_SE^{gluonic}                         (3.2-Δ_2)
Δ_3  =  (4/3) · I_SE^{fermion}                                       (3.2-Δ_3)
```

with the three per-channel integrals treated in the dedicated
BZ-computation notes. The color-tensor prefactor structure (2.1)
is retained here independent of the per-channel integral values.

## 4. Safe claim boundary

This note claims:

> On the retained `Cl(3)/Z^3` framework surface, the 1-loop correction
> to the Ward ratio `(y_t/g_s)²` decomposes into exactly three
> gauge-group-irreducible color channels `C_F · Δ_1`, `C_A · Δ_2`,
> `T_F · n_f · Δ_3`, with exact SU(3) prefactors `C_F = 4/3`,
> `C_A = 3`, `T_F · n_f = 3` at n_f = 6. The three-channel structure
> is retained framework-native from the D7 + S1 SU(3) Casimir authority
> and the Rep-A/Rep-B diagrammatic catalog.

It does **not** claim:

- framework-native values for the per-channel integrals `Δ_1`, `Δ_2`,
  `Δ_3` on the retained action (these remain separate sub-theorems,
  currently cited rather than retained);
- that any single channel dominates (the master-assembly theorem
  shows partial cancellation among all three channels);
- any modification of the master obstruction theorem, the Ward-identity
  tree-level theorem, the Rep-A/Rep-B cancellation sub-theorem, or
  any publication-surface file.

## 5. What is retained vs. cited vs. open

**Retained (framework-native, established upstream and preserved):**

- `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` at SU(3) (D7 + S1).
- `n_f = 6` (SM flavor content at M_Pl).
- Three-channel color-tensor decomposition
  `Δ_R = C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3`.
- Exact SU(3) prefactor values `C_F = 4/3`, `C_A = 3`, `T_F n_f = 3`.
- Rep-A vs Rep-B diagrammatic catalog and the `2 C_F · I_leg`
  external-Z_ψ cancellation (from the cancellation sub-theorem).

**Cited / computed separately (not retained structurally in this note):**

- The per-channel integrals `Δ_1`, `Δ_2`, `Δ_3`; each is treated in a
  dedicated BZ-computation sub-theorem with its own cited-literature
  bracket and operational central.

**Open (not closed by this note):**

- Framework-native 4D BZ quadrature of `I_v_scalar`, `I_v_gauge`,
  `I_SE^{gluonic}`, `I_SE^{fermion}` on the retained action (closed at
  the full-staggered-PT note downstream; structurally distinct from the
  color-factor retention question addressed here).

## 6. Validation

The runner `scripts/frontier_yt_p1_color_factor_retention.py` emits
deterministic PASS/FAIL lines and is logged under
`logs/retained/yt_p1_color_factor_retention_2026-04-17.log`. The
runner must return PASS on every check to keep this note on the
retained surface.

The runner verifies 5 checks:

1. `C_F = 4/3` exactly at SU(3) (from D7 + S1).
2. `C_A = 3` exactly at SU(3) (from D7).
3. `T_F · n_f = 3` exactly at SU(3), n_f = 6 (from D7 + S1 + SM
   flavor count at M_Pl).
4. Three-channel decomposition identity
   `Δ_R = C_F Δ_1 + C_A Δ_2 + T_F n_f Δ_3` is structurally exact
   (symbolic reassembly matches the Rep-A − Rep-B subtraction
   channel-by-channel).
5. Consistency with the Rep-A/Rep-B decomposition: the net C_F, C_A,
   T_F n_f channel coefficients after the `2 C_F · I_leg`
   external-Z_ψ cancellation reproduce (3.2).

## Status

**RETAINED** — three-channel color-tensor decomposition of `Δ_R`
retained framework-native. Per-channel integrals `Δ_1`, `Δ_2`, `Δ_3`
remain cited / computed separately and live outside this note's scope.
