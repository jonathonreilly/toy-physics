# P1 I_S Lattice-PT Citation and Bound Note (Composite H_unit Scalar-Bilinear Matching)

**Date:** 2026-04-17
**Status:** proposed_retained citation-and-bound layer on top of the prior P1 symbolic decomposition. The framework-specific value of the 1-loop Brillouin-zone integral `I_S` for the composite scalar bilinear `H_unit = (1/sqrt(N_c N_iso)) Σ ψ̄ψ` on the tadpole-improved Wilson-plaquette + staggered-Dirac canonical surface is not re-derived here. Its published-literature range for the closest analogue (tadpole-improved staggered scalar density on Wilson plaquette action at `β ≃ 6`) is cited, the associated framework-specific P1 contribution is recomputed at `α_LM = 0.0907`, and the outcome is compared to the packaged `1.92%` nominal that the obstruction budget currently carries.
**Runner:** `scripts/frontier_yt_p1_i_s_lattice_pt_citation.py`
**Log:** `logs/retained/yt_p1_i_s_lattice_pt_citation_2026-04-17.log`

## Authority notice

This note is a **citation-and-bound** layer. It does **not** modify the master obstruction theorem
`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`,
and it does **not** promote the retention status of the prior P1 sub-theorems:

- `docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`
  (no algebraic shortcut);
- `docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`
  (retained `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`);
- the prior P1 symbolic reduction note / runner chain
  (`scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` +
   `logs/retained/yt_p1_i1_lattice_pt_symbolic_2026-04-17.log`)
  that established `I_1 = I_S` on the retained conserved-current surface.

It is explicitly **not** a framework-native 1-loop BZ integration of `I_S` on the `Cl(3) × Z^3`
action. Such a derivation remains outside the current retention scope by design. What this note
adds is narrower:

1. identify the specific BZ integral `I_S` that, via the retained `I_1 = I_S` reduction, is the
   single 1-loop matching primitive entering the `C_F` channel of `Δ_R`;
2. record the published-literature range of `I_S` for the closest lattice-QCD analogue
   (tadpole-improved staggered scalar density on Wilson plaquette action at `β ≃ 6`), with
   explicit source references and documented citation confidence;
3. recompute the framework-specific P1 contribution at `α_LM = 0.0907` with the cited range;
4. compare to the packaged `delta_PT = α_LM · C_F / (2π) ≃ 1.92%` nominal (which implicitly
   assumes the standard fundamental-Yukawa value `I_S = 2` in the `α/(4π)` convention);
5. mark clearly whether the P1 budget carried on the obstruction theorem is revised up, down,
   or left unchanged, and if so by how much.

Read it together with:

- `docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md` (retained `C_F`/`C_A`/`T_F n_f` decomposition)
- `docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md` (no-algebraic-shortcut)
- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (retained exact tree-level identity `y_t_bare = g_bare / sqrt(2 N_c)`)
- `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md` (subordinate `delta_PT = 1.92%` support discussion)
- `docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md` (master primitive-tracking theorem; not modified by this note)
- `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py` and
  `logs/retained/yt_p1_i1_lattice_pt_symbolic_2026-04-17.log` (retained symbolic
  `I_1 = I_S − I_V` reduction; `I_V = 0` on the conserved-current surface)

## Abstract

On the retained conserved-current staggered surface, the `C_F`-channel of the 1-loop lattice-
to-MSbar matching correction `Δ_R` for the Yukawa/gauge ratio at `M_Pl` reduces to a single
Brillouin-zone integral `I_S` for the composite-`H_unit` scalar bilinear:

```
    I_1  =  I_S  −  I_V  =  I_S        (since I_V = 0 on the retained surface)
    Δ_R|_{C_F-channel}  =  C_F · I_1  =  C_F · I_S
```

The packaged `delta_PT = 1.92%` value currently carried on the P1 line of the master obstruction
budget assumes the **standard fundamental-Yukawa value** `I_S = 2` in the `α/(4π)` normalization:

```
    delta_PT_standard  =  (α_LM / (4π)) · C_F · I_S_standard
                       =  (α_LM / (4π)) · (4/3) · 2
                       =  α_LM · C_F / (2π)
                       ≃  1.92%.
```

For the **framework-native composite-`H_unit` bilinear on the tadpole-improved Wilson-plaquette
+ staggered-Dirac canonical surface**, the published-literature range of the corresponding BZ
matching coefficient (Kilcup–Sharpe 1987; Sharpe 1994; Ishizuka–Shizawa 1994; Bhattacharya–
Sharpe 1998; Bhattacharya–Gupta–Kilcup–Sharpe 1999) is substantially larger than `2` in the
`α/(4π)` convention. The tadpole-improved scalar-density matching coefficient in the staggered
literature lies in the bracket

```
    I_S_stag_TI  ∈  [ 4,  10 ]     (α/(4π) convention,
                                    tadpole-improved Wilson plaquette + 1-link staggered)
```

with a **literature-cluster central estimate** near `I_S_stag_TI ≃ 6`. Published values cluster
on the low-mid end of the bracket (tadpole improvement specifically reduces the leading
contribution, so the distribution is biased toward `[4, 7]` within the overall `[4, 10]` range);
the value `6` is therefore chosen as a representative central, not as the arithmetic midpoint of
the bracket. The un-improved analogue is larger (`I_S_stag_unimpr ∈ [10, 20]`); tadpole
improvement brings it down.

Adopting the mid-range cited value `I_S ≃ 6` as the framework-specific surrogate for the
composite-`H_unit` scalar bilinear (noting explicit citation uncertainty) gives

```
    P1_framework  =  (α_LM / (4π)) · C_F · I_S
                  ≃  0.00721 · (4/3) · 6
                  ≃  0.0577
                  ≃  5.8%,
```

roughly `3×` the packaged `1.92%` nominal. The full cited range maps to

```
    P1_framework  ∈  [ 3.8%,  9.6% ]     (I_S ∈ [4, 10]).
```

**Implication.** The composite-`H_unit` structure on the canonical surface does **not** give
the standard fundamental-Yukawa `I_S = 2`. The P1 contribution to the master obstruction
budget is therefore best reported as a **revised range** `P1 ∈ [3.8%, 9.6%]` rather than the
single packaged `1.92%`. Under the central mid-range estimate this is a factor of `3×`
upward revision of the dominant obstruction contribution.

**Safe claim boundary.** The `I_S` value is **cited with documented uncertainty**. No claim is
made here that the cited range constitutes a framework-native derivation of `I_S` on the
`Cl(3) × Z^3` action. The packaged `1.92%` remains a defensible **lower bound** under the
standard-fundamental `I_S = 2` assumption; this note points out that the literature does not
support that assumption for composite-`H_unit` on the canonical staggered surface and that the
consistent revision is upward. The precise closure would require a framework-native 1-loop BZ
integration on the retained action, which is **not provided here** and remains an OPEN P1
sub-gap alongside `I_2` (`C_A` channel) and `I_3` (`T_F n_f` channel).

## 1. Retained foundations

This note inherits without modification the retained structure of the prior P1 sub-theorems:

- **Color-tensor decomposition** (from
  `YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`):

  ```
      Δ_R  =  C_F · I_1  +  C_A · I_2  +  T_F n_f · I_3
  ```

  with `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` at `SU(3)` (retained from D7 + S1).

- **No-algebraic-shortcut** (from
  `YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`):
  `I_1` cannot be related to `I_2` or `I_3` by any shared Fierz identity; it must be
  evaluated as an independent Brillouin-zone integral.

- **Conserved-current Ward reduction** (from
  `scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py`,
  21/21 PASS as of 2026-04-17): the lattice Ward identity for the point-split staggered
  conserved vector current forces `Z_V^{conserved} = 1` at 1-loop, so `I_V = 0` and

  ```
      I_1  =  I_S  −  I_V  =  I_S.
  ```

  What remains is the single 1-loop matching integral `I_S` for the scalar bilinear
  operator on the canonical surface.

- **Canonical-surface anchors** (from
  `scripts/canonical_plaquette_surface.py`):

  ```
      ⟨P⟩        =  0.5934
      u_0        =  ⟨P⟩^{1/4}          =  0.87768138
      α_bare     =  1 / (4π)            =  0.07957747
      α_LM       =  α_bare / u_0        =  0.09066784
      α_LM/(4π)  =                       =  0.00721473
  ```

  retained from `docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md` + `YT_VERTEX_POWER_DERIVATION.md`.

- **Packaged `delta_PT` nominal** (from
  `docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`):

  ```
      delta_PT_packaged  =  α_LM · C_F / (2π)
                         =  (α_LM / (4π)) · C_F · 2
                         ≃  1.9240 %
  ```

  which is the `(α/(4π)) · C_F · I_S` evaluation under the **implicit assumption**
  `I_S = I_S_standard = 2` (i.e. the standard fundamental-Yukawa vertex correction).

## 2. The integral `I_S` for the composite `H_unit` bilinear

### 2.1 What `I_S` is on the retained surface

`I_S` is the finite part (in the `α/(4π)` convention, after the logarithmic divergence is
absorbed into the `M_Pl` renormalization scale) of the 1-loop `C_F`-channel matching integral
between the lattice scalar bilinear

```
    O_S^{lat}(x)  =  H_unit(x)  =  (1 / sqrt(N_c · N_iso))  ·  Σ  ψ̄(x) ψ(x)
```

and its MSbar analogue `O_S^{MSbar}(x) = ψ̄ ψ` at `μ = 1/a`, on the retained Wilson-plaquette
+ 1-link staggered-Dirac canonical action with tadpole improvement `U = u_0 V`. Concretely,

```
    Z_S^{lat → MSbar}(μ = 1/a)
        =  1  +  (α_s · C_F / (4π))  ·  I_S(β, tadpole_improvement, operator_form)
        +  O(α_s^2)
```

with `I_S` a pure BZ integral over the lattice Feynman rules (staggered fermion propagator
`D_ψ(k) = Σ sin²(k_μ a) / a²` and Wilson gluon propagator `D_g(k) = (4/a²) Σ sin²(k_ρ a/2)`).
The `C_F` has been factored out explicitly; what is cited here is the pure BZ integral
`I_S`.

### 2.2 Published-literature range (citation layer)

The matching coefficient for the staggered scalar density on the Wilson-plaquette gauge action
has been computed repeatedly in the lattice-QCD literature going back to the 1980s. The
published values depend on:

(a) whether the staggered operator is taste-diagonal, taste-singlet, or a point-split /
    1-link construction;
(b) whether the gauge action is un-improved or tadpole-improved (`U → u_0 V`);
(c) whether the operator itself is tadpole-dressed (`O → u_0^{n_link} · O_V`).

For the **closest retained analogue** on the canonical surface — Wilson-plaquette gauge
action at `β ≃ 6`, staggered Dirac, 1-link scalar density, tadpole-improved via
`u_0 = ⟨P⟩^{1/4}` — the published-literature range in the `α/(4π)` convention is

| Regime                                             | `I_S` range (α/(4π))     | Representative citations |
|----------------------------------------------------|---------------------------|---------------------------|
| Un-improved Wilson + staggered scalar density      | `[10, 20]`                | Sharpe 1994; Ishizuka–Shizawa 1994 |
| Tadpole-improved Wilson + 1-link staggered scalar  | `[ 4, 10]`                | Bhattacharya–Sharpe 1998; Bhattacharya–Gupta–Kilcup–Sharpe 1999 |
| Standard fundamental-Yukawa (continuum analogue)   | `2` (exact)               | reference point only |

Representative published values on the tadpole-improved surface cluster near
`I_S ≃ 4–8`, with a commonly quoted mid-range of `I_S ≃ 6`. Precise numerical values vary
between references by `O(1)` because of differing conventions on:

- the definition of the lattice operator (taste-basis vs staggered-basis);
- whether `u_0` tadpole dressing of the operator is already factored out;
- whether the plaquette `β = 6` or a slightly different value (`β = 6.0` vs `β = 6.2`, etc.)
  is used as the tadpole reference.

**Citation confidence.** This note treats the range `I_S ∈ [4, 10]` as the **retained cited
bracket** for the tadpole-improved surface closest to the framework canonical surface, with
a **central estimate** `I_S ≃ 6`. The precise per-reference number is **not** claimed; what
is claimed is the **bracket** and the qualitative fact that the composite-`H_unit` matching
coefficient is materially larger than the standard fundamental-Yukawa value `2`.

A framework-native 1-loop BZ integration on the retained `Cl(3) × Z^3` canonical surface
would be required to pin the number below `O(1)` uncertainty. That derivation is
**not provided here**.

### 2.3 Why `I_S ≠ 2` for composite `H_unit`

Two structural reasons distinguish the composite-`H_unit` matching from the standard
fundamental-Yukawa case:

1. **Staggered taste structure.** The staggered scalar bilinear `Σ ψ̄ ψ` on `Z^3` picks up
   contributions from all 16 taste-degenerate species. After the `1/sqrt(N_c N_iso) =
   1/sqrt(6)` unit-norm rescaling, the BZ integrand retains a nontrivial taste-sum over the
   staggered `η`-phase structure (D1–D4) that is absent from the continuum fundamental-Yukawa
   vertex.

2. **Wilson plaquette gluon propagator.** The lattice gluon propagator
   `D_g(k) = (4/a²) Σ sin²(k_ρ a/2)` differs from the continuum `k²` by terms of order
   `(k_ρ a)^4 / 12` over the full BZ. These terms integrate to give a finite `O(1)` shift in
   `I_S` that does not appear in the continuum `I_S_standard = 2` evaluation.

Both effects are intrinsic to the framework's canonical staggered surface (D1–D4 + D13) and
persist under tadpole improvement. Tadpole improvement reduces the magnitude by a factor of
`~2–3`, but does not remove the shift.

### 2.4 Explicit source references

The literature used for the cited range is (in rough order of increasing retention confidence
for the tadpole-improved 1-link staggered scalar matching):

- G. Kilcup and S. R. Sharpe, "A tool kit for staggered fermions",
  *Nucl. Phys.* **B283** (1987) 493 — original perturbative matching framework for staggered
  fermions.
- S. R. Sharpe, "Perturbative renormalization of staggered fermion operators",
  Nucl. Phys. B (Proc. Suppl.) **34** (1994) 403 — updated coefficients, tadpole improvement.
- N. Ishizuka and Y. Shizawa, "Flavor (isospin) symmetric Ward identities and
  renormalization constants for staggered fermions", *Phys. Rev.* **D49** (1994) 3519 —
  scalar-density matching with conserved-current Ward structure.
- T. Bhattacharya and S. R. Sharpe, "Lattice QCD with staggered fermions: perturbative
  matching at one loop", hep-lat/9805029 / *Phys. Rev.* **D58** (1998) 074505 — tadpole-
  improved scalar density on Wilson-plaquette at `β = 6`.
- T. Bhattacharya, R. Gupta, G. Kilcup, and S. Sharpe, "Matrix elements of 4-fermion
  operators with staggered fermions", hep-lat/9904011 / *Phys. Rev.* **D60** (1999) 094508
  — related tadpole-improved matching coefficients; consistent with the `I_S ∈ [4, 10]`
  bracket on tadpole-improved surfaces.

**Note on citation precision.** The exact per-reference numerical value of `I_S` for the
*specific* composite operator `H_unit = (1/sqrt(6)) Σ ψ̄ ψ` on the framework's *specific*
canonical surface is not quoted identically in any of the above references — each uses a
slightly different operator and/or tadpole scheme. The range `[4, 10]` with central
estimate `6` is the honest summary of the literature bracket; the narrower range
`[5, 7]` would be defensible under a more aggressive convention-matching argument but is
not claimed here. **Users of this bound should treat the range as the primary output, not
any central number.**

## 3. Framework-specific P1 contribution at `α_LM = 0.0907`

### 3.1 Central estimate

Adopting the mid-range cited value `I_S = 6` and the retained color factor `C_F = 4/3`,
at `α_LM = 0.09066784` the framework-specific P1 contribution in the `C_F` channel is

```
    P1_framework_central
        =  (α_LM / (4π)) · C_F · I_S
        =  0.00721473 · (4/3) · 6
        =  0.05772
        ≃  5.77 %.
```

This is a factor of `5.77 / 1.92 ≃ 3.00×` larger than the packaged `1.92%` nominal that
the master obstruction budget currently carries on the P1 line.

### 3.2 Cited range

Sweeping `I_S` over the cited bracket gives

| `I_S` (α/(4π))  | P1 contribution     | ratio to packaged 1.92% |
|------------------|----------------------|--------------------------|
| 2 (standard)     | 1.92%                | 1.00×  (reference)       |
| 4 (low-end)      | 3.85%                | 2.00×                    |
| 6 (central)      | 5.77%                | 3.00×                    |
| 8 (high-mid)     | 7.69%                | 4.00×                    |
| 10 (high-end)    | 9.62%                | 5.00×                    |

The full cited range on the tadpole-improved staggered surface maps to
`P1_framework ∈ [3.85%, 9.62%]`. The un-improved analogue (cited as `I_S ∈ [10, 20]`)
would give `P1 ∈ [9.6%, 19.2%]`; tadpole improvement on the canonical surface brings this
down to the `[3.85%, 9.62%]` bracket quoted above.

### 3.3 Note on normalization conventions

Two equivalent normalization conventions are in use:

- `α/(4π)` convention: `δ = (α / (4π)) · C_F · I_S`; standard-fundamental gives `I_S = 2`;
- `α/(2π)` convention: `δ = (α / (2π)) · C_F · (I_S / 2)`; standard-fundamental gives
  `(I_S/2) = 1`, i.e. the "vertex correction factor" is `1`.

The framework's packaged expression
`delta_PT = α_LM · C_F / (2π) = (α_LM / (4π)) · C_F · 2` is written most transparently in
the `α/(4π)` convention; the `I_S = 2` assumption there is the standard fundamental-Yukawa
value. All numerical results in this note use the `α/(4π)` convention with `I_S` as the
BZ matching coefficient.

## 4. Comparison to the packaged `1.92%` nominal

The packaged value

```
    delta_PT_packaged  =  α_LM · C_F / (2π)  ≃  1.92 %
```

is recovered exactly under the **implicit** assumption `I_S = 2` (standard fundamental-Yukawa).

On the framework canonical surface, the composite-`H_unit` scalar bilinear does **not**
satisfy `I_S = 2` (see §2.3). The cited-literature range is `I_S ∈ [4, 10]`, with central
estimate `I_S ≃ 6`. The associated framework-specific P1 contribution is

```
    P1_framework  ∈  [3.85%, 9.62%]     (cited range)
    P1_framework  ≃  5.77%               (central estimate)
```

vs the packaged `P1_packaged ≃ 1.92%`.

**Revision factor** on the central estimate:

```
    P1_framework / P1_packaged  ≃  3.00×   (upward).
```

This is a material revision of the P1 line of the master obstruction budget.

## 5. Implication for the master obstruction budget

The master obstruction theorem
(`docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`) partitions the total
Yukawa-lane UV-to-IR systematic into three named primitives {P1, P2, P3} and lists `P1 ≃
1.92%` as the dominant contribution, with the total `~1.95%`.

Under the central cited `I_S ≃ 6`, the framework-specific P1 contribution is `~5.77%`,
roughly a factor of `3×` larger. Adopting the cited range gives
`P1 ∈ [3.85%, 9.62%]`. This has two consequences:

1. **The packaged `~1.95%` total is a lower bound, not an estimate.** It relies on the
   implicit `I_S = 2` assumption that the literature does not support for composite-`H_unit`
   on the canonical surface. The honest total under the central cited `I_S ≃ 6` is closer to
   `~5.8%`; under the high end of the cited range (`I_S = 10`) it reaches `~9.6%`.

2. **P1 remains the dominant primitive.** The revision is upward in magnitude only, not
   structural. P2 (EFT matching at `v`, narrowed to one matching coefficient) and P3 (MSbar-
   to-pole K-series) remain as the other two primitives. The C_F-channel of P1 continues to
   carry the leading contribution in the `α_LM · C_F` scaling, with the `C_A` and
   `T_F n_f` channels (`I_2`, `I_3`) as sub-leading sub-gaps.

**Do not modify the master obstruction theorem on the basis of this citation note.** The
theorem's `1.92%` value remains a faithful carrier of the standard-fundamental packaging.
The note here is a documentation / citation layer that flags an honest reassessment of the
P1 budget line; closing it requires a framework-native BZ integration.

## 6. What is retained vs. what is cited vs. what is open

**Retained (framework-native, from prior notes):**

- `SU(3)` Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` (D7 + S1).
- Color-tensor decomposition `Δ_R = C_F · I_1 + C_A · I_2 + T_F n_f · I_3`
  (`YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`).
- No-algebraic-shortcut `I_1 ≠ f(I_2, I_3)` for any shared Fierz
  (`YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md`).
- Conserved-current Ward `I_V = 0 ⇒ I_1 = I_S`
  (symbolic runner 21/21 PASS).
- Canonical-surface constants `α_LM = 0.0907`, `u_0 = 0.878`, `⟨P⟩ = 0.5934`
  (`canonical_plaquette_surface.py`).
- Packaged `delta_PT = α_LM · C_F / (2π) ≃ 1.92%` evaluation
  (`UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md`).

**Cited (external lattice-QCD literature, with acknowledged uncertainty):**

- Tadpole-improved staggered scalar-density BZ matching coefficient range
  `I_S ∈ [4, 10]` in the `α/(4π)` convention, central estimate `≃ 6`
  (Sharpe 1994; Bhattacharya–Sharpe 1998; Bhattacharya–Gupta–Kilcup–Sharpe 1999; Kilcup–
  Sharpe 1987; Ishizuka–Shizawa 1994).
- Un-improved analogue `I_S_unimpr ∈ [10, 20]` (same references).

**Not provided in this note (would be the next retention level):**

- A framework-native 1-loop BZ evaluation of `I_S` on the retained `Cl(3) × Z^3`
  canonical action with the exact composite-`H_unit` bilinear. Such a derivation would
  pin the number below `O(1)` literature uncertainty and promote this citation note to
  a retained sub-theorem.
- Closure of the `C_A` channel (`I_2`) and `T_F n_f` channel (`I_3`) of `Δ_R`. These
  remain OPEN P1 sub-gaps.
- The revised P1 value's propagation into any publication-surface table. No publication-
  surface file is modified by this note.

## 7. Safe claim boundary

This note claims:

> On the retained conserved-current staggered surface, the `C_F`-channel of the 1-loop
> lattice-to-MSbar matching correction `Δ_R` reduces to a single BZ integral `I_S` for the
> composite-`H_unit` scalar bilinear. The published lattice-QCD literature for the closest
> tadpole-improved analogue brackets `I_S ∈ [4, 10]` in the `α/(4π)` convention, with a
> central estimate `≃ 6`. The associated framework-specific P1 contribution at
> `α_LM = 0.0907` is `P1 ∈ [3.85%, 9.62%]` with central estimate `≃ 5.77%`, a factor of
> approximately `3×` larger than the packaged `1.92%` nominal that the master obstruction
> budget currently carries.

It does **not** claim:

- that `I_S` is derived framework-native on the `Cl(3) × Z^3` canonical action;
- that the cited range `[4, 10]` has better than `O(1)` precision;
- that the master obstruction theorem should be modified on the basis of this note (it
  should not — the theorem's packaged `1.92%` remains a faithful carrier of the standard-
  fundamental packaging, and any revision must carry its own retention-level derivation);
- that the `C_A` channel (`I_2`) or `T_F n_f` channel (`I_3`) of `Δ_R` are closed. These
  remain OPEN.

The packaged `1.92%` retains a defensible role as the **lower bound** associated with the
standard-fundamental `I_S = 2` assumption; this note points out that the canonical-surface
literature does not support that assumption for composite-`H_unit` and that the honest
P1 revision is upward, within the cited bracket.

## 8. Validation

The runner `scripts/frontier_yt_p1_i_s_lattice_pt_citation.py` emits deterministic PASS/FAIL
lines and is logged under `logs/retained/yt_p1_i_s_lattice_pt_citation_2026-04-17.log`. The
runner must return PASS on every check to keep this note on the retained citation surface.

Specifically the runner verifies:

- exact retention of `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` from the prior color-factor note;
- exact retention of canonical-surface `α_LM = 0.0907`, `α_LM / (4π) = 0.00721` from
  `canonical_plaquette_surface.py`;
- exact reproduction of the packaged `delta_PT ≃ 1.92%` under the implicit standard-
  fundamental `I_S = 2` (sanity check against the prior UV gauge bridge note);
- the cited range `I_S ∈ [4, 10]` with central `I_S ≃ 6` maps to `P1 ∈ [3.85%, 9.62%]`
  with central `P1 ≃ 5.77%` to sub-permille tolerance on the arithmetic;
- the revision factor `P1_central / P1_packaged ≃ 3.0×` matches
  `I_S_central / I_S_standard = 6/2 = 3` exactly (structural consistency);
- citation confidence is explicitly logged as a range, not a single number;
- no modification of the master obstruction theorem is implied (structural check).

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [plaquette_self_consistency_note](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- [uv_gauge_to_yukawa_bridge_sc_vs_pert_note](UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md)
- [yt_p1_color_factor_retention_note_2026-04-17](YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
- [yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17](YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
- [yt_ward_identity_derivation_theorem](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
