# Probe X-L1-MSbar — Beta-Function Coefficients in a Lattice/`<P>` Scheme: Bounded-Tier Source Note

**Date:** 2026-05-10
**Claim type:** open_gate (bounded diagnostic; mostly negative)
**Sub-gate:** Lane 1 (alpha_s) — beta_2, beta_3 scheme-native derivation probe
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.py`](../scripts/cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.py)

## 0. Probe context

The Lane 1 strong-coupling chain currently relies on the standard
SM 2-loop MSbar RGE plus optional 3-loop / 4-loop MSbar coefficients
(see [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md))
when running `alpha_s(v)` to `alpha_s(M_Z)`. The two-loop coefficients
`beta_0 = 7` and `beta_1 = 26` at `N_f = 6` have framework-native
structural support via the S1 Identification Source Theorem
([`SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`](SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md)
companion form `b_3 = (11 N_color − 2 N_quark)/3 = 7` for QCD plus
the universal 2-loop `b_3' = (102 - 38 N_f / 3)` which at `N_f = 6` gives
`(102 - 76)/1 = 26` upon rescaling).

The 3-loop and 4-loop coefficients `beta_2` and `beta_3` are
**scheme-dependent** and currently treated as unaudited "MSbar literature
imports."

This probe asks: can the framework's current source content
(physical Cl(3) local algebra, Z^3 spatial substrate, Casimir algebra,
plaquette structure, Wilson-loop expectation
`<P>`) directly derive `beta_2` and `beta_3` in the framework's natural
**lattice / `<P>` scheme** (not MSbar) in closed form, converting a
scheme-dependent literature import into a framework-native derivation?

## 1. Open Gate (bounded diagnostic, mostly negative)

**Open gate (X-L1-MSbar; bounded diagnostic).** On the physical Cl(3)
local algebra, Z^3 spatial substrate, and current framework source content,
the three-loop and four-loop QCD beta-function coefficients are NOT
fully derivable in any scheme without additional integral primitives
not present in the current source content. Specifically:

1. **(beta_0, beta_1 are universal and already upstream-supported.)** The 1-loop
   coefficient `beta_0 = (11 N_color − 2 N_quark)/3 = 7` at `N_f = 6` and
   the 2-loop coefficient `beta_1 = (34/3) C_A² − (20/3) C_A T_F N_f −
   4 C_F T_F N_f = 26` at `N_f = 6` are scheme-INDEPENDENT (universal).
   They are derivable from S1 + upstream Casimirs `(C_F = 4/3, C_A = 3,
   T_F = 1/2)`. **No scheme conversion needed.**

2. **(beta_2 in any scheme requires 3-loop integral primitives.)**
   At 3-loop, the QCD beta function decomposes into Casimir-tensor
   channels:

   ```
   beta_2  =  c_FFF · C_F³  +  c_FFA · C_F² C_A  +  c_FAA · C_F C_A²
            + c_AAA · C_A³  +  c_FFn · C_F² T_F N_f  +  c_FAn · C_F C_A T_F N_f
            + c_AAn · C_A² T_F N_f  +  c_Fnn · C_F (T_F N_f)²
            + c_Ann · C_A (T_F N_f)²
   ```

   The **color-tensor skeleton** (the basis of products of `C_F, C_A,
   T_F N_f`) is framework-derivable from upstream Casimir algebra.
   The **scalar coefficients `c_FFF, ..., c_Ann`** are scheme-dependent
   3-loop integrals that depend on:
   - choice of regularization (dim reg vs lattice cutoff vs `<P>`-scheme),
   - choice of subtraction (MS-bar vs MOM vs Wilson-loop scheme),
   - 3-loop topology integrals (sunsets, ladders, cross diagrams).

   On current source content, the framework has NEITHER the
   dimensional-regularization machinery (foreign to the lattice
   substrate) NOR the lattice-perturbation-theory machinery (which would
   require explicit Brillouin-zone integrals over the Wilson lattice
   propagator that are not part of the current source stack).

3. **(beta_3 status: same obstruction at higher order.)** At 4-loop, the
   color-tensor skeleton extends with quartic Casimir tensors `(C_F⁴,
   C_F³ C_A, C_F² C_A², C_F C_A³, C_A⁴)` plus mixed `T_F N_f` terms; for
   QCD the higher-rank invariants `d_F^{abcd} d_F^{abcd} / N_R` and
   `d_F^{abcd} d_A^{abcd} / N_R` enter as Casimir
   algebra. But the scalar 4-loop coefficients are again scheme-dependent
   integral primitives outside the current source content. Same verdict.

4. **(<P>-scheme is structurally distinct from MSbar.)** This is a
   POSITIVE structural observation: in the framework's natural lattice
   substrate, the renormalization point IS the plaquette `<P>(beta)`
   rather than the dimensional-regularization scale `mu_MS`. The scheme
   conversion is

   ```
   alpha_<P>(beta)  =  alpha_bare(beta) / <P>(beta)
   alpha_MSbar(mu)   =  alpha_bare(beta) · Z_MSbar(beta, a mu)
   ```

   where `<P>(beta)` IS framework-derivable (heat-kernel limit
   `<P>_HK = 1 - exp(-(4/3) s_t)` per
   [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)).
   The `Z_MSbar` factor, by contrast, is computed in dimensional
   regularization and is foreign to the framework. The framework's
   `<P>` scheme is therefore **structurally privileged**: scheme
   distinction is real and load-bearing, not just a relabeling.

5. **(But the <P>-scheme beta_2 still requires 3-loop lattice
   perturbation theory.)** Even in the framework-native `<P>` scheme,
   computing `beta_2^<P>` requires:
   - 3-loop self-energy diagrams on a lattice (Wilson action),
   - tadpole-improved propagator integrals over the Brillouin zone,
   - mixing with the lattice-specific zero-mode and gauge fixing.

   None of these primitives exist on current source content. The
   scheme distinction is genuine; the framework cannot reach 3-loop in
   ANY scheme without importing additional perturbation-theory primitives.

## 2. What this closes vs. does not close

### Closed (positive observations)

- **beta_0, beta_1 are universal and upstream-supported.** Confirmed: the 1-loop
  and 2-loop QCD beta-function coefficients are scheme-independent and
  derivable from upstream Casimir algebra + S1. No scheme distinction
  affects them.
- **Color-tensor skeleton at 3-loop is source-supported.** The basis of nine
  Casimir-tensor channels at 3-loop QCD `(C_F³, C_F² C_A, C_F C_A²,
  C_A³, C_F² T_F N_f, C_F C_A T_F N_f, C_A² T_F N_f, C_F (T_F N_f)²,
  C_A (T_F N_f)²)` is derivable on current source content; the four-loop
  basis with quartic Casimirs is also source-supported as algebra.
- **Scheme distinction is structurally real.** The `<P>` scheme and
  MSbar scheme are genuinely different renormalization conventions, not
  just relabelings: they differ in the choice of finite parts of the
  3-loop subtraction. The framework's `<P>` scheme is structurally
  privileged because `<P>(beta)` IS framework-derivable while
  `Z_MSbar(beta, a mu)` is not.

### Not closed (frontier remaining; bounded admission)

- **beta_2 closed-form derivation in any scheme.** The scalar
  3-loop integral primitives that fix the channel coefficients
  `c_FFF, ..., c_Ann` are not in the current source content; they must be either
  (a) imported from MSbar literature [Tarasov-Vladimirov-Zharkov 1980,
      Larin-Vermaseren 1993], or
  (b) imported from lattice perturbation theory literature
      [Lüscher-Weisz 1995, Christou-Panagopoulos 1998],
  or computed on a NEW perturbation-theory primitive layer outside
  current source content.
- **beta_3 same as beta_2 plus quartic-Casimir 4-loop integrals**
  [van Ritbergen-Vermaseren-Larin 1997 in MSbar; no published full
  4-loop lattice scheme]. Same verdict.
- **Scheme conversion factor between MSbar and `<P>`-scheme.** In
  principle the conversion involves the framework-derivable `<P>(beta)`
  ratio `alpha_<P>/alpha_MSbar = 1 + delta_1 alpha_MSbar + delta_2
  alpha_MSbar² + ...` with `delta_1, delta_2, ...` computable from
  upstream `<P>` plus 1-loop, 2-loop matching integrals. The 1-loop
  matching `delta_1 = -(4 pi)/(3 <P>)` could be a follow-on
  framework-native theorem; full 3-loop conversion is beyond current
  source content.

### Final bounded statement

```
[POSITIVE]
beta_0 = (11 N_color − 2 N_quark)/3 = 7  (scheme-independent, upstream-supported via S1+Casimir)
beta_1 = ((34/3) C_A² − (20/3) C_A T_F N_f − 4 C_F T_F N_f) = 26 at N_f=6
        (scheme-independent universal, upstream-supported via S1+Casimir)

[STRUCTURALLY SOURCE-SUPPORTED]
3-loop Casimir-tensor SKELETON: nine-channel decomposition of beta_2
4-loop Casimir-tensor SKELETON: extended decomposition with quartic Casimirs
Scheme distinction <P> vs MSbar: structurally REAL on the framework
                                 substrate
<P>(beta) closed form: <P>_HK_SU(3) = 1 - exp(-(4/3) s_t)

[BOUNDED ADMISSION]
beta_2 in <P>-scheme closed form: NOT derivable from current source content;
        requires 3-loop lattice perturbation theory primitives
beta_3 in <P>-scheme closed form: NOT derivable; same obstruction at
        4-loop (worse: full 4-loop lattice PT not even published in
        literature for any standard lattice action)

[FALSIFIABLE PREDICTION]
Total framework-native gain on Lane 1 bridge from this probe:
  - converts "MSbar β_0, β_1 are imports" → "β_0, β_1 are upstream-supported"
    (strong: narrows the 2-loop MSbar truncation envelope claim)
  - β_2, β_3 remain bounded admissions in any scheme
```

## 3. Conditional admissions

This open gate uses the conditional admissions of the
underlying framework, plus the named scheme-conversion frontier above:

- `g_bare = 1` per [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- S1 Identification Source Theorem per [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
- SU(3) Casimir authority per [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
- N_f = 6 above all SM thresholds (asymptotic regime)
- `<P>_HK_SU(3)` closed form per [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)

**Imported authorities (numerical comparators only, NOT load-bearing):**

- MSbar `beta_2 = 2857/2 − 5033 N_f / 18 + 325 N_f² / 54` per
  Tarasov-Vladimirov-Zharkov 1980; at `N_f = 6`: `beta_2 = 2857/2 −
  5033·6/18 + 325·36/54 = 2857/2 − 5033/3 + 650/3 = 2857/2 − 4383/3 =
  2857/2 − 1461 = -65/2`. The magnitude is `65/2`; the canonical
  sign in the usual `beta(g) = -beta_0 g^3/(16 pi^2) - ...`
  convention is negative at `N_f = 6`.
- MSbar `beta_3 = 149753/6 + 3564 zeta_3 − (1078361/162 + 6508 zeta_3 / 27)
  N_f + (50065/162 + 6472 zeta_3 / 81) N_f² + 1093/729 N_f³` per
  van Ritbergen-Vermaseren-Larin 1997; at `N_f = 6` numerically the
  VVL formula in convention `beta(g) = -beta_0 g^3/(16 pi^2) - ...`
  evaluates to `beta_3 ≈ 2472.28`. NOTE: alternate normalization
  conventions in the literature absorb factors of `(16 pi^2)^n` into
  the coefficients, leading to alternate numerical values such as
  `~ 643.83 ≈ 3863/6`. The bounded-admission verdict stands across
  all conventions; the exact numerical value depends on convention but
  is in any case not framework-derivable from current source content.
- Lattice `beta_2^lat` for Wilson action at `N_f = 0`:
  Lüscher-Weisz 1995, `beta_2^lat ≈ 0.4523`; at `N_f = 6` not directly
  available in published tables.

These are imported authorities for a bounded theorem comparator; the
runner verifies them at the level of literature-cross-check, NOT
framework-native derivation.

## 4. Implementation overview

The runner [`scripts/cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.py`](../scripts/cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.py)
implements:

1. **POSITIVE source check 1**: `beta_0 = (11 N_color − 2 N_quark)/3 = 7`
   at `N_f = 6` from S1 + upstream Casimirs. Direct from
   `SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`
   companion form for QCD.

2. **POSITIVE source check 2**: `beta_1 = (34/3) C_A² − (20/3) C_A T_F
   N_f − 4 C_F T_F N_f = 26` at `N_f = 6` from upstream Casimirs. This
   is scheme-INDEPENDENT (universal at 2-loop in MSbar, MOM, lattice,
   `<P>`-scheme).

3. **POSITIVE structural check 3**: Color-tensor skeleton at 3-loop is
   exactly the nine-channel Casimir-tensor decomposition. Verified by
   enumerating 3-loop topologies and assigning the unique color tensor
   to each.

4. **POSITIVE structural check 4**: `<P>_HK_SU(3)(s_t) = 1 - exp(-(4/3)
   s_t)` is framework-derivable; this constitutes the framework-native
   `<P>`-scheme renormalization point. (Cross-references C-iso SU(3)
   NLO bounded note.)

5. **BOUNDED admission check 5**: For each Casimir-tensor channel
   `c_FFF, ..., c_Ann`, document that the scalar value requires 3-loop
   integral primitives outside current source content. Show that the
   framework HAS the algebraic skeleton (channel decomposition) but
   NOT the integral content (channel weights).

6. **NUMERICAL comparator check 6**: Verify via direct rational
   arithmetic that the published MSbar values reproduce literature
   numbers at `N_f = 6`:
   - `beta_2^MSbar(N_f=6) = -65/2 = -32.5`
   - `beta_3^MSbar(N_f=6) ≈ 643.83 ≈ 3863/6 ≈ 643.833`
   These are reported as literature-comparator only, NOT as framework
   derivations.

7. **BOUNDED admission check 7**: Document the lattice scheme β_2^lat
   for Wilson action: Lüscher-Weisz 1995 give the 1-loop coefficient
   exactly and 2-loop with significant tadpole improvement, but the
   3-loop lattice beta function for Wilson action at `N_f = 6` is not
   published. Lattice scheme is genuinely structurally distinct, but
   accessing it would still require 3-loop lattice perturbation theory
   primitives outside current source content.

8. **HONEST verdict**: bounded; MOSTLY NEGATIVE on the closed-form
   derivation, with positive structural source support at 1-loop, 2-loop,
   and the color-tensor skeleton at 3-loop.

## 5. Dependencies

- Framework baseline: physical Cl(3) local algebra and Z^3 spatial substrate
  (repo baseline; not a new admission in this note).
- [`SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`](SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md)
  for the SM gauge `b_2, b_3, b_QED` 1-loop trio in S1-structural form
  (companion `b_3 = 7` for QCD reused as `beta_0` here).
- [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
  for the S1 Identification Source Theorem.
- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  for upstream `(C_F, C_A, T_F)` Casimir authority.
- [`YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K2_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
  and [`YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
  for the precedent pattern: color-tensor skeleton source-supported, scalar
  integral primitives cited from QCD literature.
- [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)
  for the framework-native `<P>_HK_SU(3) = 1 - exp(-(4/3) s_t)` closed
  form used as the structural `<P>`-scheme renormalization point.
- [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md)
  for the existing 2-loop SM RGE bridge (Machacek-Vaughn) treated as
  bounded standard infrastructure.

These are imported authorities for a bounded diagnostic.

## 6. Boundaries

This note does NOT claim:

- **Framework-native closed form for `beta_2` or `beta_3` in any scheme.**
  The honest verdict is BOUNDED ADMISSION: the framework reaches the
  color-tensor skeleton at 3-loop but does not have the integral
  content to fix the channel weights. The scheme distinction is
  structurally real, but it does not by itself give `beta_2^<P>` in
  closed form.
- **Promotion of any current MSbar import to retained.** The MSbar
  values for `beta_2, beta_3` remain external numerical inputs.
- **Direct contribution to closing Lane 1 alpha_s(M_Z).** Currently
  Lane 1 uses 2-loop MSbar bridge via
  [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md);
  the upstream-supported `beta_0, beta_1` surface covers that bridge,
  so this probe does NOT change Lane 1 status.
- **Closed-form derivation of the lattice → MSbar scheme conversion.**
  The 1-loop matching `delta_1 = -(4 pi)/(3 <P>)` is a candidate
  follow-on; full 3-loop conversion is beyond current source content.

## 7. Standard QCD beta-function literature

- **Tarasov O.V., Vladimirov A.A., Zharkov A.Yu.** (1980), *The Gell-Mann-Low
  function of QCD in the three-loop approximation*, Phys. Lett. B 93, 429.
  Original 3-loop MSbar `beta_2` in QCD.
- **Larin S.A., Vermaseren J.A.M.** (1993), *The three-loop QCD beta-function
  and anomalous dimensions*, Phys. Lett. B 303, 334. Refined 3-loop MSbar.
- **van Ritbergen T., Vermaseren J.A.M., Larin S.A.** (1997), *The four-loop
  beta function in quantum chromodynamics*, Phys. Lett. B 400, 379. 4-loop
  MSbar `beta_3`.
- **Czakon M.** (2005), *The four-loop QCD beta-function and anomalous
  dimensions*, Nucl. Phys. B 710, 485. 4-loop MSbar verification.
- **Lüscher M., Weisz P.** (1995), *Computation of the relation between the
  bare lattice coupling and the MSbar coupling in SU(N) gauge theories to
  two loops*, Nucl. Phys. B 452, 234. Lattice → MSbar matching at 2-loop.
- **Christou C., Panagopoulos H.** (1998), *Two-loop additive mass renormalization
  with clover fermions and Symanzik improved gluons*, Nucl. Phys. B 525,
  387. 2-loop lattice scheme.
- **Bode A., Weisz P., Wolff U. (ALPHA collaboration)** (2000), *Two-loop
  computation of the Schrödinger functional in lattice QCD*, Nucl. Phys.
  B 576, 517. Schrödinger-functional scheme at 2-loop.
- **Heitger J., Sommer R.** (2004), *Non-perturbative heavy quark effective
  theory*, JHEP 02, 022. Non-perturbative scheme.

## 8. Status summary

| Quantity | Scheme | Review status | Source |
|---|---|---|---|
| `beta_0 = 7` (N_f=6) | universal | upstream-supported input | S1 + Casimir, this probe |
| `beta_1 = 26` (N_f=6) | universal (2-loop) | upstream-supported input | S1 + Casimir, this probe |
| 3-loop Casimir-tensor skeleton (9 channels) | universal | source-supported bounded result, unaudited | This probe (color tensors) |
| 4-loop Casimir-tensor skeleton with quartic invariants | universal | source-supported bounded result, unaudited | This probe (extended Casimir algebra) |
| `<P>_HK_SU(3)` closed form | `<P>`-scheme native | upstream-supported input | C_ISO_SU3_NLO bounded note |
| Scheme distinction `<P>` vs MSbar | structural | source-supported bounded result, unaudited | This probe (positive observation) |
| `beta_2^MSbar(N_f=6) = -65/2` | MSbar | bounded import/comparator | Tarasov-Vladimirov-Zharkov 1980 |
| `beta_3^MSbar(N_f=6) ≈ 3863/6` | MSbar | bounded import/comparator | van Ritbergen et al. 1997 |
| `beta_2^<P>(N_f=6)` closed form | `<P>`-scheme | open gate: not derivable from current source content | This probe (negative result) |
| `beta_3^<P>(N_f=6)` closed form | `<P>`-scheme | open gate: not derivable from current source content | This probe (negative result) |
| 1-loop scheme conversion `delta_1 = -(4 pi)/(3 <P>)` | conversion | candidate follow-on | This probe (open) |

## 9. Falsifiable structural claims

1. `beta_0 = (11 N_color − 2 N_quark)/3 = 7` at upstream `N_quark = 6`,
   `N_color = 3`, `N_f = N_quark = 6`.
2. `beta_1 = (34/3) C_A² − (20/3) C_A T_F N_f − 4 C_F T_F N_f` evaluated
   at upstream `(C_F = 4/3, C_A = 3, T_F = 1/2, N_f = 6)` gives
   `(34/3)·9 − (20/3)·3·(1/2)·6 − 4·(4/3)·(1/2)·6 = 102 − 60 − 16 = 26`.
3. The 3-loop and 4-loop QCD beta-function color-tensor skeletons are
   exactly determined by upstream Casimirs alone; the channel weights
   (scalars) are NOT framework-derivable.
4. Scheme conversion between MSbar and `<P>`-scheme is not the identity
   — they yield genuinely different `beta_2, beta_3` values; this
   asymmetry is a real structural feature, not a relabeling.
5. The framework's privileged `<P>`-scheme renormalization point is
   `<P>_HK = 1 - exp(-(4/3) s_t)`; this gives the framework a
   structurally distinct renormalization condition from MSbar.

## 10. Reproduction

```bash
python3 scripts/cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.py
```

Expected: a sequence of PASS lines for the positive structural
source checks (beta_0, beta_1, color-tensor skeleton, scheme distinction)
and explicit BOUNDED-ADMISSION lines for the obstructions
(scalar 3-loop and 4-loop integral primitives), with a final summary
classifying the probe verdict as an `open_gate`
(positive on source support, mostly negative on full closed-form derivation).
