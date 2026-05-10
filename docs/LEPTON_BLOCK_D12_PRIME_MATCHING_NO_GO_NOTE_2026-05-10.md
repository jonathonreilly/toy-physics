# Lepton Block D12-Prime Matching — No Composite-Higgs Identity (No-Go)

**Date:** 2026-05-10

**Status:** proposed_no_go sharp negative result on the lepton (2,1)
block. Attempts the YT-style matching argument that would close the
y_τ Ward identity via D17-prime + D16-prime + S2 + the matching of
Rep A (single-B-exchange) with Rep B (H_unit^lep matrix element).
**Result: the matching argument does NOT yield a Ward identity for y_τ.**

The structural reason is sharp and identifiable: the framework's
**composite Higgs** (D9) is a **QCD-generated quark bilinear**
`H = (1/N_c) ψ̄_a ψ_a`, not a lepton bilinear. The H_unit^lep
established in D17-prime is a mathematical tensor uniqueness
statement on the (2,1) block, but it does NOT correspond to a
dynamically-generated field in the bare framework action.

The matching identity requires Rep A and Rep B to refer to the
**same physical operator**. For the Q_L block, both refer to the
QCD-generated composite Higgs (D9). For the L_L block, Rep A's
B-exchange amplitude refers to a real tree-level diagram, but
Rep B's H_unit^lep does NOT correspond to the framework's
single composite Higgs (which is the quark bilinear, not a lepton
bilinear). Therefore the matching is structurally invalid on the
lepton block.

The naive numerical matching (assuming the matching DID hold)
would give `y_τ ≈ g_1/√2 ≈ 0.354` at M_Pl, which is **~35× larger
than the empirical y_τ ≈ 0.01**. This empirical falsification
provides independent confirmation of the structural obstruction.

**Primary runner:** `scripts/frontier_lepton_block_d12_prime_matching.py`

**Lane:** 6 — Charged-lepton mass retention (M5-a fully obstructed)

---

## 1. Theorem statement

**Theorem (D12-prime matching no-go on the lepton (2,1) block).**

The YT-style matching argument

```text
   Rep A (Feynman rules) = Rep B (composite-operator matrix element)
```

does NOT yield a Ward identity for `y_τ` on the lepton (2,1) block.
This is because:

1. **(Structural)** The framework's composite Higgs (D9) is the
   QCD-generated quark bilinear `H = (1/N_c) ψ̄_a ψ_a`. There is
   no analog "lepton composite Higgs" in the bare framework
   action; D17-prime's `H_unit^lep = (1/√2) Σ L̄_L^α H_α e_R` is
   a mathematical tensor uniqueness statement (verified at PR
   #1018) but does NOT correspond to a dynamically-generated
   field analogous to the QCD-bound H.

2. **(Empirical)** Even if the matching were applied formally
   (treating H_unit^lep as a tensor object regardless of dynamics),
   the resulting prediction `y_τ ≈ g_1/√2 ≈ 0.354` is empirically
   falsified by `y_τ ≈ 0.01` by a factor of ~35. There is no
   natural small factor (RGE, kinematic, anomaly) that closes
   this gap.

The combination of (1) and (2) is a definitive negative result:
the YT-style chain extension to the lepton block does NOT close
into a y_τ Ward identity. The combined no-go #912 is now sharpened
from "no sqrt-rational form" to "no matching argument applicable
at all."

## 2. The matching argument structure

### 2.1 YT chain matching on Q_L (works)

The YT chain identifies `y_t` via TWO computations of the same
4-fermion 1PI Green's function `Γ⁽⁴⁾(q²)`:

**Rep A (Feynman rules path)**: at tree level on the bare action,
the unique diagram contributing to `Γ⁽⁴⁾` on the color-singlet ×
iso-singlet × Dirac-scalar channel is single-gluon-exchange. Per
D12 + S2:

```text
   q² Γ⁽⁴⁾_OGE = g_s² × [1/(2 N_c)] × |c_S|²
              = g_s²/6   (with N_c = 3, |c_S| = 1)            (2.1.1)
```

**Rep B (composite-operator path)**: via the composite Higgs
`H_unit^Q_L = (1/√6) Σ Q̄_L H q_R` (D17 + D9):

```text
   q² Γ⁽⁴⁾_H_unit = y_t² × |<ψ̄ψ | H_unit | 0>|²
                = y_t² × 1   (H_unit unit-normalized)       (2.1.2)
```

Both Reps refer to the SAME physical Green's function (the same
external states, same momentum transfer, same channel). Therefore
they MUST agree. Equating (2.1.1) and (2.1.2):

```text
   y_t² = g_s²/(2 N_c) = g_s²/6                              (2.1.3)
   y_t = g_s/√6                                              (2.1.4)
```

This is YT-T1, the retained framework identity.

### 2.2 The L_L block: same setup, different physical content

For the lepton (2,1) block, by direct analogy:

**Rep A** (single-B-exchange, from D16-prime at PR #1026):

```text
   q² Γ⁽⁴⁾_lep_BE = g_1² × Y(L_L) × Y(e_R) × |c_S|²
                  = g_1² × (-1/2)(-1) × 1
                  = g_1²/2                                   (2.2.1)
```

**Rep B** (H_unit^lep matrix element, from D17-prime at PR #1018):

```text
   q² Γ⁽⁴⁾_lep_H_unit^lep = y_τ² × |<L̄_L H e_R | H_unit^lep | 0>|²
                          = y_τ² × 1                        (2.2.2)
```

If the matching argument applied as in YT, equating would give:

```text
   y_τ² = g_1² × |Y(L_L) Y(e_R)|
        = g_1²/2                                             (2.2.3)
   y_τ = g_1/√2                                              (2.2.4)
```

The numerical prediction at M_Pl (with `g_1(M_Pl) ≈ 0.5`):

```text
   y_τ_naive(M_Pl) = 0.5/√2 ≈ 0.354                         (2.2.5)
```

## 3. Why the matching FAILS on the lepton block

### 3.1 Structural reason: H_unit^lep is not a dynamically-generated field

Per D9 (`docs/YUKAWA_COLOR_PROJECTION_THEOREM.md`):

> phi(x) = (1/N_c) ψ̄_a(x) ψ_a(x)
> where a = 1,...,N_c is the color index and the 1/N_c is the
> singlet projection normalization.

The framework's composite Higgs is **explicitly** a quark bilinear,
with the COLOR sum `Σ_a` running over color indices. This composite
emerges from QCD-strong-binding dynamics on the lattice — the
attractive gluon-exchange forces between quarks generate the
condensate.

D17-prime's `H_unit^lep = (1/√2) Σ_α L̄_L^α H_α e_R` is a
**mathematical tensor uniqueness statement** on the lepton (2,1)
block. It IS the unique unit-normalized iso-singlet × Dirac-scalar
composite structurally. But it is NOT a dynamically-generated
field in the bare framework action — there is no analog
"lepton condensate" because:

- Lepton self-interactions in the SM are weak (Yukawa-strength,
  not strong-coupling)
- The framework's bare action contains gauge interactions
  (Wilson plaquette + staggered Dirac) but no contact 4-fermion
  vertices to generate lepton bilinears
- Lepton Yukawas couple leptons to the SAME (QCD-generated)
  composite Higgs, not to a separate lepton composite

### 3.2 Therefore the matching argument is invalid

The matching identity Rep A = Rep B requires both Reps to refer
to the SAME physical operator. For Q_L, they both refer to the
QCD-generated H_unit. For L_L:

- Rep A (B-exchange, real tree-level diagram) — physical
- Rep B (H_unit^lep matrix element) — mathematical tensor, not
  matched to a physical field in the bare action

The two Reps are NOT computing the same Green's function. The
"matching" is mathematically incoherent on the lepton block.

### 3.3 Empirical confirmation

Even if one applied the matching FORMALLY (ignoring the structural
mismatch), the prediction `y_τ ≈ g_1/√2 ≈ 0.354` is empirically
falsified:

```text
   y_τ_predicted (M_Pl) ≈ 0.354
   y_τ_empirical (M_Pl) ≈ 0.01   (using m_τ ≈ 1.777 GeV, v ≈ 246 GeV)
   ratio: ~35×
```

`y_τ` runs slowly (small Yukawa, no QCD running), so the prediction
at M_Pl is essentially the same as at M_Z. There is no natural
small factor (RGE running, kinematic suppression, anomaly correction)
that closes a 35× gap.

This empirical mismatch independently confirms the structural
obstruction: a Ward identity that would predict `y_τ ≈ 0.354`
is wrong by 1.5 orders of magnitude.

## 4. Significance: sharpens the combined no-go #912

The `CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
(#912) gave the combined obstruction in the form:

> No Ward identity of the form `y_τ_bare = G × C` is constructible,
> where G is a retained gauge or transport coefficient and C is a
> structural sqrt-rational constant.

D12-prime matching no-go SHARPENS this from "no sqrt-rational form"
to **"no matching argument applicable at all on the lepton block"**:

| | Combined no-go #912 | D12-prime matching no-go (this PR) |
|---|---|---|
| Scope | "no sqrt-rational C" | "no matching argument" |
| Specificity | excludes sqrt-rational | excludes the YT-style matching paradigm |
| Structural reason | abelian Y vs non-abelian Fierz | no lepton composite Higgs (D9 is quark-only) |
| Empirical anchor | none | y_τ ≈ 0.354 vs 0.01 (~35× off) |

The no-go #912's M5-a route ("D17-prime on (2,1) block — open
structural problem with no current candidate") is now **fully
obstructed**:

- **D17-prime** delivered (#1018): mathematical tensor uniqueness ✓
- **D16-prime** delivered (#1026): tree-level exchange identification ✓
- **D12-prime matching** (this PR): does NOT close — H_unit^lep
  doesn't correspond to a physical field; matching is invalid ✗

M5-a is now closed as a research route on the current framework
surface. The remaining surviving routes from #912 are M1
(Koide-anchored) and M5-c (Koide-anchored cross-sector), both
depending on Koide flagship Q + δ closure.

## 5. What this theorem CLOSES

- The M5-a research-level route from #912 is now FULLY obstructed.
- The lepton-block analog of YT-T1 does NOT exist, with a sharp
  structural reason (no lepton composite Higgs in the bare framework).
- The combined no-go #912 is sharpened from "no sqrt-rational form"
  to "no matching argument."

## 6. What this theorem does NOT close

- Lane 6 (charged-lepton mass retention) remains open via M1 and
  M5-c routes (both depend on Koide flagship closure).
- Does NOT predict any lepton mass.
- Does NOT bar future closures via fundamentally different
  structural mechanisms not based on YT-style matching.
- Does NOT touch the YT identity itself (y_t = g_s/√6 stays
  retained for Q_L).

## 7. Falsifiers

The no-go is falsified by any one of:

1. A demonstrated framework-internal "lepton composite Higgs"
   field that emerges from the bare action (analogous to D9's
   quark composite). This would require new strong lepton
   self-interaction in the bare framework.
2. A revised D9 statement showing the composite Higgs is built
   from BOTH quarks and leptons (with iso/color combinations
   that include the lepton sector).
3. A different matching argument (not Rep A = Rep B with
   composite-Higgs identification) that yields a Ward identity
   for y_τ.
4. A demonstration that y_τ_predicted = `g_1/√2` is actually
   correct empirically when computed with the right RGE running
   or kinematic factors that close the 35× gap.

## 8. Implications for the Lane 6 closure pathway

After this PR (combined with #912, #1018, #1026):

- **Direct YT-style chain extension to lepton block**: CLOSED
  (combined no-go + this PR's structural sharpening)
- **M5-a (D17-prime)**: structurally delivered; matching fails
  → CLOSED
- **M1 (Koide-anchored)**: still depends on Koide flagship
  Q + δ closure (in flight on parallel BAE probe lane)
- **M5-c (Koide-anchored cross-sector)**: still depends on
  Koide closure + new derivation chain
- **Fundamentally different mechanisms**: open research

Lane 6 closure on the current framework surface continues to
require either Koide flagship breakthrough or fundamentally
different structural content. The YT-chain-extension route is
now definitively excluded.

## 9. Cross-references

- D17-prime (companion): PR #1018 / `docs/LEPTON_BLOCK_SCALAR_SINGLET_COMPOSITE_UNIQUENESS_D17_PRIME_THEOREM_NOTE_2026-05-10.md`
- D16-prime (companion): PR #1026 / `docs/LEPTON_BLOCK_TREE_LEVEL_EXCHANGE_D16_PRIME_THEOREM_NOTE_2026-05-10.md`
- Combined no-go (parent context): #912 / `docs/CHARGED_LEPTON_Y_TAU_WARD_COMBINED_NO_GO_NOTE_2026-05-10.md`
- YT chain (the analog this fails to extend):
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- D9 (composite Higgs as quark bilinear):
  `docs/YUKAWA_COLOR_PROJECTION_THEOREM.md` §1.1
- Koide flagship (parallel work on M1/M5-c prerequisite):
  `docs/KOIDE_BAE_PROBE_*.md` (multiple probes in flight)

## 10. Boundary

This is a sharp negative structural result on the lepton (2,1)
block. It closes the YT-style chain extension as a route to
y_τ Ward identity by identifying the precise structural step
where the matching argument fails (the H_unit^lep ↔ H_unit
identification, since D9 makes H specifically a quark
bilinear).

It does NOT close Lane 6 itself; it closes one specific
attack route on Lane 6.

A class-A runner accompanies this note
(`scripts/frontier_lepton_block_d12_prime_matching.py`).
