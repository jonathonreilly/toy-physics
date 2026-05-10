# Probe V-L1-Quartic — Quartic Casimirs and the QCD β_2/β_3 Channel-Weight Obstruction

**Date:** 2026-05-10
**Claim type:** bounded_theorem (negative on the conjecture; positive on a
narrow Casimir-value retention sub-result)
**Sub-gate:** Lane 1 (alpha_s) — does the retained Cl(3)⊗Cl(3) quartic
Casimir algebra bypass the X-L1-MSbar β_2/β_3 channel-weight integral
obstruction?
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.py`](../scripts/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.py)
**Cached output:** [`logs/runner-cache/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.txt`](../logs/runner-cache/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.txt)

## 0. Probe context

[Probe X-L1-MSbar](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)
established that QCD `beta_2` (3-loop) and `beta_3` (4-loop) are NOT
framework-derivable in any scheme — neither MSbar dim-reg nor lattice
perturbation theory. The X probe identified that the framework retains
the **Casimir-tensor SKELETON** (9 channels at 3-loop, 17+ at 4-loop)
but NOT the **scalar channel weights**, which require either dim-reg
integrals or lattice PT integrals (both foreign or outside retained
primitives).

This V probe asks: what if the failure was localized? Specifically, the
framework retains:

- **Quadratic Casimirs**: `C_F = 4/3, C_A = 3, T_F = 1/2` (giving `beta_0,
  beta_1`)
- **Cl(3) ⊗ Cl(3) tensor structure**: the SU(3) generator algebra is
  embedded in retained Cl(3) anticommutator products via the graph-first
  SU(3) bridge.

**Conjecture (stress-test).** β_2 and/or β_3 are derivable from retained
quartic Casimirs (`d_F^abcd d_F^abcd / N_F = 5/12`, `d_F^abcd d_A^abcd /
N_F = 5/2`, `d_A^abcd d_A^abcd / N_A = 135/8` for SU(3)) via the
Cl(3) ⊗ Cl(3) tensor structure, bypassing the X-L1-MSbar 3-/4-loop
integral obstruction. The "scalar channel weights" might be quartic-
Casimir COEFFICIENTS, not integrals.

**Goal.** Test whether retained quartic Casimirs from Cl(3) tensor
structure give `beta_2` and/or `beta_3` in closed form, thereby
reclassifying the X-L1-MSbar terminal status as bounded-with-quartic-
bridge.

## 1. Theorem (bounded, negative on the conjecture)

**Theorem (V-L1-Quartic; bounded; the conjecture is foreclosed).** On
retained content of Cl(3)/Z³ augmented by the retained quartic-Casimir
basis, the QCD `beta_2` and `beta_3` channel weights are STILL not
derivable. Specifically:

1. **(`beta_2` does not contain quartic Casimirs.)** The full 3-loop
   QCD beta function in MSbar (Tarasov-Vladimirov-Zharkov 1980; Larin-
   Vermaseren 1993) decomposes ONLY into products of quadratic Casimirs
   `C_F, C_A, T_F n_f` to total degree three. Six channels span the
   3-loop beta function:

   ```
   beta_2^MSbar  ⊆  span{ C_A^3,                  pure-gauge cubic
                          C_A^2 (T_F n_f),         mixed (one matter)
                          C_F C_A (T_F n_f),       mixed (one matter)
                          C_A (T_F n_f)^2,         matter quadratic
                          C_F (T_F n_f)^2,         matter quadratic
                          C_F^2 (T_F n_f) }        matter linear
   ```

   The numerical scalar coefficients of these channels are 3-loop
   master-integral combinations (rationals from massless 3-loop
   propagator masters in dim-reg). The TVZ closed-form polynomial
   `beta_2 = 2857/2 − (5033/18) n_f + (325/54) n_f²` is the
   reduction of this 6-channel sum at SU(3); it is degree 2 in
   `n_f`, which directly excludes any quartic-Casimir contribution
   (those would generate higher-degree `n_f` mixing).

   No `d_F^abcd`, no `d_A^abcd`, no quartic invariants enter `beta_2`.
   Quartic Casimirs first appear at **4-loop** (`beta_3`), not at 3-loop.
   The conjecture's framing ("β_2 might be derivable from quartic
   Casimirs") is therefore structurally unavailable: the quartic
   Casimir basis CONTRIBUTES ZERO to `beta_2` in any scheme.

2. **(`beta_3` does contain quartic Casimirs, but their scalar weights
   are 4-loop integrals.)** At 4-loop, the channel basis extends with
   `d_F^abcd d_F^abcd / N_R` and `d_F^abcd d_A^abcd / N_R` plus
   higher-order quadratic-Casimir products. For SU(3):
   - `d_F^abcd d_F^abcd / N_F = 5/12` (retained, group-theoretic)
   - `d_F^abcd d_A^abcd / N_F = 5/2` (retained, group-theoretic)
   - `d_A^abcd d_A^abcd / N_A = 135/8` (retained, group-theoretic)

   These VALUES are pure group theory, derivable on retained Cl(3) ⊗
   Cl(3) tensor algebra (already noted in X-L1-MSbar Section 4). However,
   the SCALAR COEFFICIENTS multiplying these channels in `beta_3`
   (per van Ritbergen-Vermaseren-Larin 1997 in MSbar):
   - `c_dFdF · d_F^abcd d_F^abcd / N_F` channel weight in `beta_3` is
     a rational + `zeta_3` combination from 4-loop ladder/sunrise
     integrals. The pure number is, e.g., `c_dFdF ~ -64 + 480 zeta_3`
     in one convention.
   - `c_dFdA · d_F^abcd d_A^abcd / N_F` channel weight similarly is
     a 4-loop integral combination.

   These scalars are NOT framework-retained: they require explicit
   evaluation of 4-loop master integrals (massless propagator masters,
   crossed sunsets, etc.) that depend on the regulator (dim-reg in MSbar
   versus lattice cutoff in `<P>`-scheme). Retained Cl(3) ⊗ Cl(3)
   tensor algebra does NOT compute these.

3. **(Casimir VALUES are retained; channel WEIGHTS are not.)** A clean
   structural distinction:
   - **Casimir values** (e.g., `5/12, 5/2, 135/8`): pure group-theoretic
     invariants, derivable on retained Cl(3) ⊗ Cl(3) algebra. These
     are RETAINED.
   - **Channel weights** (e.g., the rational + `zeta_n` numbers
     multiplying each Casimir-tensor channel in `beta_2, beta_3`):
     loop-integral-derived numbers requiring dim-reg or lattice PT
     machinery. These are NOT retained.

   The conjecture conflates these two. Quartic Casimir VALUES being
   retained does NOT bridge to channel WEIGHTS being retained. The
   X-L1-MSbar bounded admission stands.

4. **(Hostile-review sharpening: cubic Casimirs at 3-loop also retained
   as values, but channel weights still not derivable.)** Even at 3-loop
   the situation is parallel: the 9-channel skeleton uses cubic products
   of `(C_F, C_A, T_F n_f)`, all retained as values. The MSbar 3-loop
   coefficients (e.g., `2857/54, -1415/54, -205/18, 79/54, 11/9, 1/2`)
   come from 3-loop integrals (sunsets, ladders, mixed topologies)
   evaluated in dim-reg with MS-bar subtraction. These rationals are
   NOT pure group theory; they encode the 3-loop master integral
   reduction. The same parallel obstruction applies at every order
   beyond 2-loop.

5. **(Why 1-loop, 2-loop ARE retained but 3-loop, 4-loop are not.)**
   The 1-loop (`beta_0`) and 2-loop (`beta_1`) coefficients are universal
   (scheme-independent) and given by *combinatorial* counting of
   (vertex × leg × Casimir) at low order — they are computable from
   the Lie algebra alone using just the Lagrangian Wick contractions
   plus quadratic Casimir trace identities. From 3-loop onwards, the
   coefficients depend genuinely on integrating loop momenta in the
   regulator: they pick up `1/epsilon^k` poles whose finite parts
   depend on which subtraction scheme is used. Group theory alone
   cannot reach them.

## 2. What this closes vs. does not close

### Closed (positive narrow result)

- **Quartic Casimir VALUES at SU(3) are framework-retained.** The
  invariants `d_F^abcd d_F^abcd / N_F = 5/12`, `d_F^abcd d_A^abcd /
  N_F = 5/2`, `d_A^abcd d_A^abcd / N_A = 135/8` are pure group-theoretic
  numbers derivable on retained Cl(3) ⊗ Cl(3) algebra. (Already noted
  by X-L1-MSbar; this V probe sharpens the audit-grade record.)

### Closed (positive negative result on the conjecture)

- **β_2 contains NO quartic Casimirs.** This is a hostile-review
  sharpening: the conjecture as framed (β_2 might be derivable from
  quartic Casimirs) is structurally unavailable because β_2 simply
  has no quartic-Casimir channels to begin with. Quartic Casimirs first
  appear at 4-loop (β_3), not at 3-loop (β_2).
- **β_3 contains quartic Casimirs but their channel weights are
  4-loop integrals.** Even where quartic Casimirs DO appear, the
  retained quartic-Casimir basis is consistent with arbitrary scalar
  channel weights. Cl(3) ⊗ Cl(3) tensor algebra alone CANNOT fix
  the scalar weights without invoking 4-loop momentum-space integral
  machinery.

### Not closed (frontier remaining; bounded admission identical to X-L1-MSbar)

- **β_2 in any scheme.** Same obstruction as X-L1-MSbar: 3-loop integral
  primitives required.
- **β_3 in any scheme.** Same obstruction as X-L1-MSbar: 4-loop integral
  primitives required (in the quartic-Casimir channels too).

### Final bounded statement

```
[POSITIVE — narrow]
SU(3) quartic Casimir invariants are retained:
  d_F^abcd d_F^abcd / N_F = 5/12     (fundamental⊗fundamental)
  d_F^abcd d_A^abcd / N_F = 5/2      (fundamental⊗adjoint)
  d_A^abcd d_A^abcd / N_A = 135/8    (adjoint⊗adjoint)

[NEGATIVE — on the conjecture]
β_2 contains NO quartic-Casimir channels — the conjecture's framing
  ("β_2 derivable from quartic Casimirs") is structurally unavailable.
β_3 contains quartic-Casimir channels but their scalar weights require
  4-loop integrals; retained quartic-Casimir VALUES alone do not fix
  the WEIGHTS.

[BOUNDED ADMISSION — unchanged from X-L1-MSbar]
β_2 channel weights: NOT derivable in any scheme (as X-L1-MSbar)
β_3 channel weights: NOT derivable in any scheme (as X-L1-MSbar)

[FALSIFIABLE PREDICTION]
The X-L1-MSbar terminal status on Lane 1 β_2/β_3 imports STANDS. The
quartic-Casimir bridge does NOT reclassify β_2 or β_3 from terminal
to bounded-with-quartic-bridge.
```

## 3. Conditional admissions

This bounded theorem inherits the conditional admissions of the
underlying framework, plus the X-L1-MSbar bounded note:

- `g_bare = 1` per [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- S1 Identification Source Theorem per [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
- SU(3) Casimir authority per [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
- SU(3) quadratic Casimir on fundamental per [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
- SU(3) adjoint Casimir per [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
- N_f = 6 above all SM thresholds (asymptotic regime)
- X-L1-MSbar bounded admission per [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)

**Imported authorities (numerical comparators only, NOT load-bearing):**

- MSbar `beta_2` Casimir-tensor decomposition per Tarasov-Vladimirov-
  Zharkov 1980: 6 channels, all built from quadratic Casimirs only,
  no quartic.
- MSbar `beta_3` Casimir-tensor decomposition per van Ritbergen-
  Vermaseren-Larin 1997: 14+ channels including 2 quartic-Casimir
  channels (`d_F^abcd d_F^abcd / N_F`, `d_F^abcd d_A^abcd / N_F`).
- SU(3) quartic invariants per van Ritbergen-Vermaseren-Larin 1997
  Appendix B; cross-check with standard group-theoretic references
  (Slansky 1981; Patera-Sankoff 1973).

These are imported authorities for a bounded theorem comparator; the
runner verifies them at the level of group-theoretic identity-check
and structural-decomposition cross-check, NOT framework-native
derivation of channel weights.

## 4. Implementation overview

The runner [`scripts/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.py`](../scripts/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.py)
implements:

1. **POSITIVE retention check 1**: SU(3) quartic Casimir invariants
   `d_F^abcd d_F^abcd / N_F = 5/12`, `d_F^abcd d_A^abcd / N_F = 5/2`,
   `d_A^abcd d_A^abcd / N_A = 135/8` reproduced from explicit Gell-Mann
   anticommutator computation.

2. **NEGATIVE structural check 2**: Verify by explicit Casimir-channel
   enumeration that `beta_2` contains NO quartic-Casimir channels —
   the 6 standard channels (`C_A^3, C_A^2 T_F n_f, C_F C_A T_F n_f,
   C_A (T_F n_f)^2, C_F (T_F n_f)^2, C_F^2 T_F n_f`) span the 3-loop
   beta function, leaving zero room for `d_F d_F` or `d_F d_A` at 3-loop.

3. **NUMERICAL retention check 3**: Reproduce the standard `beta_2`
   value at `N_f = 6` from the TVZ 1980 closed-form `n_f`-polynomial
   `beta_2 = 2857/2 − (5033/18) n_f + (325/54) n_f²`, confirming
   `beta_2 = -65/2`. Verify that the polynomial is degree 2 in `n_f`,
   which directly forbids any quartic-Casimir channel contribution
   (those would require higher-degree `n_f` mixing). The per-channel
   rational coefficients in the Casimir-tensor decomposition are NOT
   re-derived in this note (they are TVZ literature imports); only
   the `n_f`-polynomial structural shape is used.

4. **NEGATIVE structural check 4**: For `beta_3`, identify that
   quartic-Casimir channels DO appear but the scalar weights require
   4-loop integral primitives. Document the retained-vs-not boundary.

5. **NEGATIVE conjecture check 5**: Test the underspecification
   directly: assume the framework KNOWS only the quartic-Casimir VALUES
   (and quadratic Casimir products); show that this is consistent with
   arbitrary channel-weight scalars in `beta_2, beta_3`. Hence the
   framework cannot pin down `beta_2` or `beta_3` from quartic
   Casimirs alone.

6. **HOSTILE-REVIEW check 6**: Apply the same analysis to 3-loop
   cubic-Casimir products; show that the same negative result holds
   (cubic products are retained as values; channel weights are 3-loop
   integrals). This generalizes the negative result: at every loop
   order ≥ 3, retained Casimir products give the SKELETON, not the
   WEIGHTS.

7. **HONEST verdict**: bounded; NEGATIVE on the conjecture; positive
   on the narrow Casimir-value retention sub-result.

## 5. Dependencies

- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) — A1, A2.
- [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)
  for the X probe's bounded result that this V probe stress-tests.
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
  for `C_F = 4/3` retention.
- [`SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md`](SU3_ADJOINT_CASIMIR_THEOREM_NOTE_2026-05-02.md)
  for `C_A = 3` retention.
- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  for retained `(C_F, C_A, T_F)` Casimir authority.
- [`YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md`](YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md)
  for the precedent pattern: color-tensor skeleton retained, scalar
  integral primitives cited from QCD literature.

These are imported authorities for a bounded theorem.

## 6. Boundaries

This note does NOT claim:

- **A framework-native closed form for `beta_2` or `beta_3` in any scheme.**
  The honest verdict is BOUNDED ADMISSION (unchanged from X-L1-MSbar):
  the framework retains the channel SKELETON and the Casimir VALUES
  but not the channel WEIGHTS.
- **Promotion of any current MSbar import to retained.** The MSbar values
  for `beta_2, beta_3` remain external numerical inputs.
- **Direct contribution to closing Lane 1 alpha_s(M_Z).** The X-L1-MSbar
  bounded admission STANDS; the quartic-Casimir conjecture is foreclosed.
- **A new axiom or new primitive.** This probe operates entirely within
  retained Cl(3) ⊗ Cl(3) tensor algebra and confirms its boundary.

## 7. Standard QCD beta-function literature (channel decomposition)

- **Tarasov O.V., Vladimirov A.A., Zharkov A.Yu.** (1980), *The Gell-Mann-Low
  function of QCD in the three-loop approximation*, Phys. Lett. B 93, 429.
  Original 3-loop MSbar `beta_2`. The 6-channel decomposition with
  rational MSbar weights from massless 3-loop master integrals.
- **Larin S.A., Vermaseren J.A.M.** (1993), *The three-loop QCD beta-function
  and anomalous dimensions*, Phys. Lett. B 303, 334. Refined 3-loop MSbar.
- **van Ritbergen T., Vermaseren J.A.M., Larin S.A.** (1997), *The four-loop
  beta function in quantum chromodynamics*, Phys. Lett. B 400, 379.
  4-loop MSbar `beta_3`; introduces the quartic Casimir channels
  `d_F^abcd d_F^abcd / N_F` and `d_F^abcd d_A^abcd / N_F` for the first
  time in the QCD beta function.
- **Czakon M.** (2005), *The four-loop QCD beta-function and anomalous
  dimensions*, Nucl. Phys. B 710, 485. 4-loop MSbar verification with
  same channel decomposition.
- **Slansky R.** (1981), *Group theory for unified model building*,
  Phys. Rep. 79, 1. Reference for SU(N) quartic invariant values.
- **Patera J., Sankoff D.** (1973), *Tables of branching rules for
  representations of simple Lie algebras*. Reference for SU(3) tensor
  invariants.

## 8. Status summary

| Quantity | Retention status | Source |
|---|---|---|
| `d_F^abcd d_F^abcd / N_F = 5/12` | RETAINED (group theory) | Standard SU(3); this probe |
| `d_F^abcd d_A^abcd / N_F = 5/2` | RETAINED (group theory) | Standard SU(3); this probe |
| `d_A^abcd d_A^abcd / N_A = 135/8` | RETAINED (group theory) | Standard SU(3); this probe |
| 6-channel `beta_2` skeleton (no quartic) | RETAINED (already in X probe) | TVZ 1980 + this probe |
| 14+-channel `beta_3` skeleton (with quartic) | RETAINED (already in X probe) | VVL 1997 + this probe |
| `beta_2` channel weights (rationals) | NOT DERIVABLE; 3-loop integrals | TVZ 1980 |
| `beta_3` channel weights (rationals + ζ_3) | NOT DERIVABLE; 4-loop integrals | VVL 1997 |
| Conjecture: quartic Casimirs derive `beta_2` | NEGATIVE (`beta_2` has no quartic channels) | This probe |
| Conjecture: quartic Casimirs derive `beta_3` | NEGATIVE (channel weights still 4-loop integrals) | This probe |

## 9. Falsifiable structural claims

1. The standard MSbar 3-loop QCD beta function `beta_2` decomposes
   into EXACTLY 6 channels of products of quadratic Casimirs `(C_F,
   C_A, T_F n_f)`, with NO quartic-Casimir contributions. Verified
   by (a) the TVZ 1980 closed-form `n_f`-polynomial reproducing
   `beta_2(N_f=6) = -65/2`, and (b) the polynomial having degree
   exactly 2 in `n_f`, which structurally forbids any quartic-Casimir
   channel contribution.
2. The standard MSbar 4-loop QCD beta function `beta_3` first
   introduces 2 quartic-Casimir channels (`d_F d_F / N_F` and
   `d_F d_A / N_F`); these channels' VALUES are retained but their
   scalar WEIGHTS require 4-loop master integrals.
3. Group-theoretic tensor algebra (Cl(3) ⊗ Cl(3) included) gives
   Casimir-tensor VALUES at all orders; it does NOT give channel
   WEIGHTS at orders ≥ 3.
4. The X-L1-MSbar bounded admission on `beta_2, beta_3` is robust
   under the quartic-Casimir-bridge attack: no quartic-Casimir bridge
   exists at 3-loop (no quartic channels in `beta_2`), and at 4-loop
   the quartic channels' weights are 4-loop integrals.

## 10. Reproduction

```bash
python3 scripts/cl3_koide_v_L1_quartic_2026_05_08_probeV_L1_quartic.py
```

Expected: a sequence of PASS lines for the positive Casimir-value
retentions and the negative conjecture stress-tests, with explicit
ADMITTED lines for the channel-weight obstructions, and a final
summary classifying the probe verdict as `bounded_theorem`
(positive on narrow Casimir-value retention, negative on the
conjecture, mostly negative on full closed-form derivation,
inheriting the X-L1-MSbar bounded admission).
