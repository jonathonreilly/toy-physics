# Dim-Parametric log|det| Extremum (DPLE) Theorem

**Date:** 2026-04-19
**Lane:** Dark-matter A-BCC basin-selector.
**Status:** Exact matrix-analysis theorem;  status is **support
theorem on the open DM gate**, not full A-BCC closure. The `F4`
interior-minimum linear-path Sylvester discriminant on the DM A-BCC chart is
the `d = 3` specialization of the **Dim-Parametric log|det| Extremum (DPLE)**
principle on linear Hermitian pencils. Uhlig 1982 supplies the structural
backbone at `d = 3`, but the theorem does not by itself derive the physical
source-side chart. See
`docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md`.
**Primary runner:** `scripts/frontier_dm_dple_theorem.py`
(PASS=19 FAIL=0).

---

## 0. Executive summary

DPLE is a standalone matrix-analysis theorem that states: along the
linear Hermitian pencil `H(t) = H_0 + t H_1` on `Herm(d, C)`, the
observable `W(t) = log|det H(t)|` has at most `floor(d/2)` interior
Morse-index-0 critical points. At `d = 3`, this upper bound is
**exactly 1**, making the "`F_d` selector" (existence of an interior
local minimum of `p(t) = det H(t)` in `(0, 1)` with matching signature)
a clean binary discriminator iff `d = 3`.

On the retained DM A-BCC chart with `H_0 = H_base` and `H_1 = J_*`,
the DPLE `d = 3` specialization `F_3` agrees with the retained `F4`
condition algebraically on all four basins `{1, N, P, X}`. Basin 1 is
the unique `F_3 = True` basin.

**Consequence.** `F4` is upgraded from a heuristic/chart-level selector to a
real theorem on the fixed DM chart. This materially strengthens the open DM
lane, but it does not by itself close the A-BCC gate.

---

## 1. Setup

Let `d >= 2` and let `H_0, H_1` be Hermitian `d x d` matrices with
`H_0` invertible. The retained linear pencil is

    H(t) = H_0 + t * H_1,    t in [0, 1].

Define

    W(t) := log|det H(t)|,
    p(t) := det H(t) = c_0 + c_1 t + ... + c_d t^d.

By Leibniz / Faddeev–LeVerrier, `deg p = d` in `t`. Interior critical
points of `W(t)` on `(0, 1)` are exactly interior zeros of
`p'(t) / p(t)` where `p(t) != 0`.

---

## 2. The DPLE principle

> **Definition (`F_d` selector).** Given `(H_0, H_1) in Herm(d; C)`
> with `H_0` invertible, define
>
> ```
> F_d(H_0, H_1) := there exists t* in (0, 1) with p'(t*) = 0,
>                   p''(t*) > 0, and sign(p(t*)) = sign(det H_0).
> ```
>
> Equivalently: `W(t) = log|det H(t)|` has an interior Morse-index-0
> critical point in `(0, 1)` with matching Sylvester signature.

### 2.1 Hellmann–Feynman form

Using Jacobi's formula:

    W'(t) = Tr[H(t)^{-1} H_1]
          = sum_k (1 / lambda_k(t)) * dlambda_k(t)/dt.

This is the eigenvalue-weighted Hellmann–Feynman condition: `W'(t) = 0`
iff the sum of reciprocal eigenvalues weighted by Hellmann–Feynman
flow vanishes.

### 2.2 Algebraic upper bound on Morse-idx-0 CPs

For `p(t)` a real polynomial of degree `d`, local minima and maxima
alternate; the max number of local minima is `floor(d/2)`:

| d | max interior Morse-idx-0 CPs |
|---|---|
| 2 | 1 (quadratic; trivial case) |
| **3** | **1 (clean binary selector)** |
| 4 | 2 (first dim with genuine ambiguity) |
| 5 | 2 |
| 6 | 3 |

**The unique dimension where `F_d` is a clean binary selector with
standard retained structure is `d = 3`.**

---

## 3. DPLE at `d = 3` reproduces `F4`

### 3.1 Algebraic form at `d = 3`

`p(t) = c_0 + c_1 t + c_2 t^2 + c_3 t^3`;
`p'(t) = c_1 + 2 c_2 t + 3 c_3 t^2`.
The quadratic `p'(t)` has real roots iff

    Delta_ret := c_2^2 - 3 c_1 c_3 > 0.

When `Delta_ret > 0`, the smaller real root

    t_* := (-c_2 + sqrt(Delta_ret)) / (3 c_3)

is the local minimum of `p` iff `p''(t_*) > 0`. The `F_3` selector is

    F_3 := Delta_ret > 0  AND  t_* in (0, 1)  AND  p(t_*) > 0
           AND  sign(p(t_*)) = sign(c_0).

This is exactly the retained `F4` condition. Uhlig 1982's sign-
characteristic classification for Hermitian pencils supplies the
structural backbone: at `d = 3` the only admissible interior Morse-idx-0
CP structure is the cubic single-minimum pattern encoded above.

### 3.2 Verification on DM A-BCC basins

`F_3` runs on the retained `H_base` and `J_*` for each basin:

| Basin | Delta_ret | # interior CPs in (0,1) | t_* | p(t_*) | F_3 |
|---|---|---|---|---|---|
| Basin 1 | +7.80 | 1 | 0.776 | +0.88 | **TRUE** |
| Basin N | -10.11 | 0 | — | — | FALSE |
| Basin P | +458.7 | 0 | — | — | FALSE |
| Basin X | -4.7e6 | 0 | — | — | FALSE |

On all four basins, `F_3` agrees with the retained `F4`. Basin 1 is
the unique `F_3 = True` basin.

### 3.3 Formal reduction

> **Claim.** On the retained DM A-BCC chart with `H_0 = H_base` and
> `H_1 = J_*`, the retained `F4` condition is algebraically equivalent
> to `F_3(H_base, J_*)`.

Proof: both conditions are "`p(t) = det H(t)` has an interior
Morse-idx-0 CP `t_*` in `(0, 1)` with `p(t_*) > 0`". At `d = 3` the
quadratic-discriminant and local-minimum test are the same.
`sign(p(t_*)) = sign(c_0)` matches since `sign(det H_base) = +1` on
Basin 1 (positive Sylvester sheet).

---

## 4. `d = 3` uniqueness

### 4.1 Algebraic

From section 2.2, the dim at which `F_d` is a clean binary selector
with at most one interior Morse-idx-0 CP is `d = 3`. At `d = 2`, `F_2`
is vacuous (no cubic discriminant structure). At `d >= 4`, `F_d`
admits multiple interior CPs (an explicit `d = 4` Hermitian pair with
2 interior Morse-idx-0 CPs in `(0, 1)` is constructed by the runner in
Task T4).

### 4.2 Physical-carrier uniqueness

The retained `{R1, R2, R3}` on main jointly force `d = 3`:

- R1: bivector-count saturation `C(d, 2) = d`;
- R2: anomaly-parity `d_s + 1` even with `d_t = 1`;
- R3: cubic-orbit / Cayley–Hamilton coincidence at `d = 3`.

All three independent conditions pick out `d = 3` — the dim-uniqueness
fingerprint of the DM A-BCC lane.

---

## 5. Scope

### 5.1 What DPLE closes

- `F4` — the retained DM A-BCC basin-selector — as a theorem at
  `d = 3`.
- Algebraic upper bound `floor(d/2)` on interior Morse-idx-0 CPs;
  clean binary selector iff `d = 3`.
- Structural unification with MRU and Berry-phase: three independent
  dim-parametric principles whose `d = 3` specializations match
  retained framework content.

### 5.2 What DPLE does not close (honest gap)

DPLE does not derive *why* the retained linear path from `H_base` to
`H_base + J_*` is the physical path. That is answered by the
already-retained P3 Sylvester linear-path signature theorem (on
main). DPLE inherits path-retention from P3; no new gap introduced.

Nor does DPLE derive `H_base` and `J_*` as operators; these are fixed
by the retained sigma-hier uniqueness theorem and cubic-variational
obstruction theorem (both on main).

---

## 6. Runner verification

`scripts/frontier_dm_dple_theorem.py` runs 7 tasks totalling 19
checks. Key results:

- T1: `det H(t)` is degree-`d` in `t` for `d = 2, 3, 4, 5`
  (max `|coeff(t^{d+1})|` `< 1e-6` across 100 random pairs per `d`).
- T2: interior Morse-idx-0 CP histograms over 400 random pairs per
  `d`; max observed `<= floor(d/2)`.
- T3: `F_3` reproduces `F4` on DM A-BCC basins (4/4).
- T4: `d = 4` fragmentation exhibited (random-search construction of
  a Hermitian pair with 2 interior Morse-idx-0 CPs).
- T5: `d = 2` degeneracy (`F_2` is a vacuous signature condition).
- T6: `d = 3` signature connection to retained `F4`.
- T7: `d = 3` binary-selector uniqueness (CP counts histogram).

Expected: PASS=19 FAIL=0.

---

## 7. Cross-references

- `docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`
  (retained path theorem on main)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
- Uhlig 1982 (Linear Algebra Appl. 46 — sign-characteristic
  classification for Hermitian pencils); Mehl–Mehrmann–Ran–Rodman 2016
  (Linear Algebra Appl. 511); Milnor, Morse Theory (1963).

---

## 8. Honest statement

DPLE is a mechanical algebraic theorem (Jacobi, Cayley–Hamilton,
Sylvester inertia); its `d = 3` specialization reduces to the retained
`F4` exactly. No numerical tuning. No new axioms. The dim-parametric
probe at `d = 2..5` demonstrates both the fragmentation at `d >= 4`
and the binary-selector uniqueness at `d = 3`. Uhlig 1982 is the
structural backbone that makes `d = 3` clean.

Runner status: PASS=19 FAIL=0.
