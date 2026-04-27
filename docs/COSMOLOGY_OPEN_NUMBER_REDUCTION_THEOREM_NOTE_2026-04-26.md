# Cosmology Open-Number Reduction Theorem: The Late-Time Bounded Surface Has Two Structural Degrees Of Freedom At Fixed Radiation Readout

**Date:** 2026-04-26
**Status:** proposed_retained/admitted-surface structural-support theorem on
`main`. Packages the matter-bridge identity (2026-04-22), the structural lock
theorem (2026-04-26), and the single-ratio inverse reconstruction certificate
(2026-04-25) into one open-number-count statement at fixed admitted radiation
readout `R := Omega_r,0`.
**Primary runner:** `scripts/frontier_cosmology_open_number_reduction.py`
**Lane:** 5 — Hubble constant `H_0` derivation
**Workstream:** `hubble-h0-20260426`

---

## 0. Statement

**Theorem (Cosmology Open-Number Reduction).** Adopt:

- (P1) `Lambda = 3 / R_Lambda^2` retained spectral-gap identity;
- (P2) `H_inf = c / R_Lambda` retained scale identification;
- (P3) `w_Lambda = -1` retained dark-energy EOS;
- (P4) flat FRW with three non-interacting components
  (`Omega_m,0 + Omega_r,0 + Omega_Lambda,0 = 1`);
- (P5) `Omega_r,0` admitted from `T_CMB` plus retained `N_eff = 3.046`
  bookkeeping (not a derivation input on the retained core; admitted
  convention).

Define the late-time bounded cosmology variable set

```text
S := { H_0, H_inf, R_Lambda, Omega_Lambda,0, Omega_m,0,
       q_0, z_*, z_mLambda, H(a) for a in (a_recomb, 1] }.
```

Define the reduced pair

```text
(H_0, L)    where L := Omega_Lambda,0 = (H_inf / H_0)^2.
```

Then every variable in `S` is an exact closed-form function of `(H_0, L)`
on the retained surface, with `R := Omega_r,0` entering as an admitted
constant. Specifically:

| Variable | Closed form |
|---|---|
| `Omega_Lambda,0` | `L` |
| `Omega_m,0` | `1 - L - R` |
| `H_inf` | `H_0 sqrt(L)` |
| `R_Lambda` | `c / H_inf = c / (H_0 sqrt(L))` |
| `q_0` | `(1 + R - 3 L) / 2` |
| `1 + z_mLambda` | `(L / (1 - L - R))^{1/3}` |
| `1 + z_*` | unique positive root of `2 L a_*^4 - (1 - L - R) a_* - 2 R = 0` (then `1 + z_* = a_*^{-1}`) |
| `H(a)` | `H_0 sqrt( R a^{-4} + (1 - L - R) a^{-3} + L )` |

Hence the late-time bounded cosmology surface has **exactly two structural
degrees of freedom at fixed admitted `R`**: `H_0` and `L`. Equivalently, knowing any
non-degenerate pair from `{H_0, H_inf, R_Lambda}` together with any one of
`{L, Omega_m,0, q_0, z_mLambda, z_*}` is sufficient to fix every variable
in `S`.

The cosmology open-number-count statement is therefore

```text
|structural degrees of freedom in S at fixed R| = 2     (the pair (H_0, L)).
```

The four admitted observational layer numbers
`(T_CMB, eta, alpha_GUT, R_Lambda-anchor)` enter via `(Omega_r, Omega_b,
Omega_DM, scale)` but are not themselves in `S`.

## 1. Retained inputs

| Identity | Authority |
|---|---|
| `Lambda = 3 / R_Lambda^2` | [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |
| `w_Lambda = -1` | [DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md) |
| `H_inf = c / R_Lambda` | [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) |
| `Omega_Lambda = (H_inf/H_0)^2` | [OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md) |
| FRW kinematic forward reduction | [COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md](COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md) |
| Single-ratio inverse reconstruction | [COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md](COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md) |
| Structural lock theorem | [HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md](HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md) |
| `R_base = 31/9` | [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md) |
| `1 + z_mr = Omega_m / Omega_r` | [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `N_eff = 3 + 0.046 = 3.046` | [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md) |

## 2. Proof

### 2.1 Closed forms

The closed forms in the table follow directly from the listed retained
identities.

- `Omega_Lambda,0 = L` is the definition.
- `Omega_m,0 = 1 - L - R` follows from flatness (P4).
- `H_inf = H_0 sqrt(L)` follows from squaring the matter-bridge identity
  `L = (H_inf/H_0)^2`.
- `R_Lambda = c / H_inf` follows from (P2).
- `q_0 = (1 + R - 3 L) / 2` is Theorem 2 of the inverse reconstruction
  note (rearranged forward).
- `1 + z_mLambda = (L / (1 - L - R))^{1/3}` follows from
  `M s_mL^3 = L` (Theorem 3 of the inverse reconstruction note) with
  `M = 1 - L - R`. Note `s_mL = 1 + z_mLambda = (L/M)^{1/3}`, equivalently
  `a_mLambda = (M/L)^{1/3}`.
- `1 + z_*` from `2 L a_*^4 - M a_* - 2 R = 0` (Theorem 4 of the inverse
  reconstruction note).
- `H(a) = H_0 sqrt( R a^{-4} + M a^{-3} + L )` is the structural lock
  theorem (★) with `M = 1 - L - R`.

### 2.2 No structurally independent variables remain in `S`

Suppose for contradiction that some variable `X in S` is not a function of
`(H_0, L)` on the retained surface. Then `X` introduces an independent
parameter beyond `(H_0, L, R)`. By the closed forms above, every variable
in `S` is expressible as a function of `(H_0, L, R)`, so the supposed
independent parameter must be `R` itself. But (P5) admits `R` as a
non-derivation observational layer number; `R notin S`. Contradiction.
Hence every variable in `S` is a function of `(H_0, L)` only (with `R`
held fixed by admission).

`QED`

### 2.3 The count is sharp

The pair `(H_0, L)` is also necessary: knowing only `H_0` and not `L`
leaves `Omega_Lambda,0` and `Omega_m,0` open, hence `q_0`, `z_*`,
`z_mLambda`, and `H(a)` for `a < 1` open. Knowing only `L` and not `H_0`
leaves the absolute time and length scales open. The count is therefore
exactly 2, not 1 or 3.

## 3. Operational consequences

### 3.1 Late-time observable cross-consistency

The single-ratio inverse reconstruction theorem (2026-04-25) already
proved that any two of `{H(a) at known a, q_0, z_mLambda, z_*}` must
reconstruct the same `L`. Combined with the present open-number reduction:

- any pair of `(H(a) at known a, q_0, z_mLambda, z_*, H_0)` over-
  determines the cosmology surface;
- giving any *third* such measurement is a consistency check;
- if any third measurement disagrees with the first two reconstructions
  beyond observational error, the retained surface is falsified.

This sharpens the "Hubble tension" landscape: the open question is
whether two observables that should reconstruct the same `L` actually
do.

### 3.2 What it costs to retain the cosmology rows

Retiring the cosmology bounded rows (`Omega_Lambda`, `Omega_m`,
`H_0`, ...) on the retained surface requires at minimum:

- a derivation of `H_0` directly, OR
- a derivation of `L` directly, OR
- a derivation of `R_Lambda` (which gives `H_inf = c/R_Lambda`) plus a
  separate derivation pinning either `H_0` or `L`.

There is no fourth class of derivation that retires the cosmology surface
without crossing one of these three premise sets. This is the program-
bounding statement of the open-number reduction theorem.

### 3.3 Why `q_0`, `z_*`, `z_mLambda` are not additional knobs

Late-time observable papers often quote `q_0` or `z_*` as if they were
independent measurements alongside `H_0` and `Omega_Lambda`. On the
retained surface, they are not: each is an exact function of `(H_0, L)`.
A "tension" between, say, `q_0` from supernovae and `Omega_Lambda` from
Planck is *the same tension as* a disagreement on `L`. The reduction
theorem makes this explicit.

## 4. What this closes and does not close

**Closes.**

- The exact open-number-count statement for the late-time bounded
  cosmology surface (`= 2`).
- The closed-form table relating every variable in `S` to `(H_0, L, R)`.
- The "no fourth class of derivation" program-bounding statement of §3.2.

**Does not close.**

- The numerical value of `H_0`. (Lane 5 main target — still open.)
- The numerical value of `L`. (Reduces to deriving `H_inf` or
  `Omega_Lambda` directly.)
- The Planck-scale anchor that gives `R_Lambda` numerically. (Planck lane;
  blocked by carrier identification; multiple finite-response /
  parent-source / area-law shortcuts closed negatively.)
- `Omega_b`, `Omega_DM` cascade closure. (DM/leptogenesis lane; depends
  on `eta` and `alpha_GUT` retirement.)

## 5. How this advances Lane 5

Before this theorem, the lane file listed multiple cosmology-related
target identities `(Omega_m, Omega_Lambda, q_0, z_*)` as if they were
independent goals. After this theorem, the cosmology bounded surface is
known to have exactly two structural degrees of freedom at fixed admitted
`R`: `H_0` and `L`. The
correct framing of Lane 5 closure is now:

- **Lane 5A:** retain `L` (or, equivalently, retain `Omega_m,0`,
  `Omega_Lambda,0`, `q_0`, `z_*`, or `z_mLambda`).
- **Lane 5B:** retain `H_0` (or, equivalently, retain `H_inf` and `L`,
  or retain `R_Lambda` and `L`).

The two sub-lanes can be closed independently. Either alone retires one
of the two structural degrees of freedom; both close the surface.

The bounded `Omega_b -> R -> Omega_DM -> Omega_m -> Omega_Lambda` cascade
in `OMEGA_LAMBDA_DERIVATION_NOTE.md` is consistent with this picture:
that cascade closes 5A *if* `eta` and `alpha_GUT` are retained. The
present theorem says nothing new about that cascade; it does provide the
clean structural framing that makes the cascade's role precise.

## 6. Runner

**Path:** `scripts/frontier_cosmology_open_number_reduction.py`
**Paired log:** `logs/2026-04-26-cosmology-open-number-reduction.txt`

The runner verifies:

1. **Symbolic closed-form table (sympy).** Each row of the table in §0
   is verified as a sympy identity given the retained premises.
2. **Forward map injectivity (sympy).** The map
   `(H_0, L, R) -> (Omega_Lambda, Omega_m, H_inf, R_Lambda, q_0,
   z_mLambda)` has nonzero Jacobian determinant in `(H_0, L)` for fixed
   `R`, confirming that no row degenerates.
3. **Cross-consistency reconstruction (sympy).** Solving the q_0 equation
   for `L` gives the inverse from Theorem 2 of the inverse reconstruction
   note. Likewise for the matter-Lambda equality equation.
4. **Numerical Planck 2018 closure (numpy).** Plugging Planck 2018
   `(H_0, L, R) = (67.4 km/s/Mpc, 0.685, 9.2e-5)` and computing every
   row of the closed-form table reproduces the observational values
   within Planck error bars.
5. **Acceleration-onset numerical check (numpy).** Solving
   `2 L a_*^4 - (1 - L - R) a_* - 2 R = 0` gives a unique positive root
   `a_* in (0, 1)`, recovering `1 + z_* ≈ 1.59` (matter-Lambda
   acceleration onset, the standard ΛCDM result).

Expected: all five PASS.

## 7. Cross-references

- `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`
- `COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`
- `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` — companion
  Cycle-1 theorem on the same workstream branch.
- `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md`
- `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`
- `OMEGA_LAMBDA_DERIVATION_NOTE.md` — the bounded cascade closure path
  for 5A (now explicitly framed as one of two sub-lanes).
- `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  — Lane 5 status; this note adds an explicit open-number-count framing
  to §3.

## 8. Boundary

This theorem is structural, not numerical. It does not retire `H_0`,
`L`, or `R_Lambda`. It packages prior retained identities into a sharp
parameter-count claim and a "no fourth derivation class" bound. External
references are limited to standard FRW cosmology (textbook; admitted
convention). All derivation premises are framework-internal retained
items already on `main`.
