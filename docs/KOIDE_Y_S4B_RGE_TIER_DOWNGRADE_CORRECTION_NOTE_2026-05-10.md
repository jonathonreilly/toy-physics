# Probe Y-S4b-RGE — Positive→Bounded Tier Downgrade Correction Note

**Date:** 2026-05-10
**Status:** source-only correction stanza for Probe Y-S4b-RGE's tier
declaration.
**Target note:** [`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md)
(file lives on open PR #948 branch
`probe/y-s4b-rge-lambda-running-2026-05-08`).
**Catching PRs:**
- [#956](https://github.com/jonathonreilly/Physics/pull/956) — hostile
  audit Z-S4b-Audit downgrades Y-S4b-RGE from positive to bounded with
  named imports {I2 β_λ^(2), I3 β_λ^(3), I4 λ(M_Pl)=0 postulate}.
- [#1023](https://github.com/jonathonreilly/Physics/pull/1023) —
  W-S4b-Classicality partially reclassifies I4 to *structurally
  forced at lattice-bare layer + named matching admission for
  runner-MSbar layer*.
**Authority role:** correction stanza (source-only). Does NOT modify
the targeted source note. Records the tier downgrade and the named
imports so downstream audits cite the corrected classification.

---

## 0. Context

Probe Y-S4b-RGE (PR #948) claims a **POSITIVE THEOREM** at the
operator-construction layer S4b-op: 3-loop SM `β_λ`-running from
`M_Pl` to `v_EW` with the framework classicality BC `λ(M_Pl) = 0`
gives `m_H = 125.14 GeV`, a **−0.09%** deviation from PDG
`m_H = 125.25 GeV`, well inside the ~5% positive-tier threshold.

Two hostile-review PRs subsequently revised this verdict:

1. **PR #956 (Z-S4b-Audit, hostile downgrade).** Audits the
   ingredient list of Y-S4b-RGE's closure and identifies **three
   imports**:

   | Import | Y-S4b-RGE ingredient | Status |
   |--------|----------------------|--------|
   | I2 | 2-loop β_λ coefficients (FJJ92, LWX03) | **IMPORTED** — dim-reg MSbar integrals; framework retains only the Casimir skeleton at 2-loop+ per Probe X-L1-MSbar. |
   | I3 | 3-loop β_λ coefficients (CZ12, BPV13) | **IMPORTED** — contains ~200 ζ(3) factors from D = 4 − 2ε integrals; framework's lattice `<P>`-scheme is foreign to dim-reg. |
   | I4 | `λ(M_Pl) = 0` BC | **POSTULATED, not derived** — Y-S4b-RGE §10 itself admits "framework-axiom in nature, not derived from A1 + A2". |

   Per the tier-brief mapping (≥3 imports forces BOUNDED), Y-S4b-RGE
   downgrades from positive_theorem to **BOUNDED THEOREM**.

2. **PR #1023 (W-S4b-Classicality, I4 refinement).** Performs
   four-route foreclosure on `λ(M_Pl) = 0`. Concludes I4 is partially
   reclassified:

   - **At the lattice-bare layer:** `λ_bare(a⁻¹) = 0` is
     **STRUCTURALLY FORCED** by the retained operator content (no
     marginal scalar quartic in the retained Cl(3)/Z³ skeleton at
     the cutoff scale).
   - **At the runner-MSbar layer:** the identification
     `λ_bare(a⁻¹) = λ^{MSbar}(M_Pl)` requires a
     **NAMED MATCHING ADMISSION** (the lattice-to-MSbar matching
     scheme is not internally derivable in the retained content).

   Net: I4 is no longer a "free postulate" but a "forced + matching
   admission". This does not lift the BOUNDED downgrade (the matching
   admission is still a named admission, and I2/I3 remain unchanged),
   but it pinpoints the residual structural content of I4.

This correction stanza records the corrected tier classification for
Y-S4b-RGE so downstream audits cite **BOUNDED** rather than POSITIVE.

## 1. Corrected status declaration

| Field | Original (PR #948) | Corrected (this note) |
|-------|--------------------|------------------------|
| Type | positive_theorem | **bounded_theorem** |
| Claim type | positive_theorem | **bounded_theorem (with named imports)** |
| Verdict header | POSITIVE THEOREM | **BOUNDED THEOREM (with named imports {I2, I3, I4})** |
| Tier promotion claim | Inside ~5% positive-tier threshold | Numerical closure inside ~5% retained, **but ingredient list is import-contaminated** at 3 named places. |

The numerical closure (`m_H = 125.14 GeV`, −0.09% from PDG) is
**unchanged**. The tier classification is corrected from POSITIVE to
BOUNDED on the basis that **three of the closure's ingredients are
named imports**, not framework-derivable content.

## 2. Named imports (corrected ingredient list)

The following imports are CARRIED by Y-S4b-RGE's closure and must be
cited whenever the closure result is referenced:

```
Imports needed by Y-S4b-RGE closure:
  I1 : 1-loop β_λ Casimir skeleton          — RETAINED (Probe X-L1-MSbar)
  I2 : 2-loop β_λ scalar coefficients       — IMPORTED (FJJ92, LWX03)
  I3 : 3-loop β_λ scalar coefficients       — IMPORTED (CZ12, BPV13)
  I4 : λ(M_Pl) = 0 BC, structured as:
        I4a : λ_bare(a⁻¹) = 0                — STRUCTURALLY FORCED
             at the lattice-bare layer
             (PR #1023, four-route closure).
        I4b : λ_bare(a⁻¹) = λ^{MSbar}(M_Pl)   — NAMED MATCHING ADMISSION
             at the runner-MSbar layer
             (PR #1023).
  I5 : 2-loop running-y_t feed-in            — IMPORT-CONTAMINATED
        (same dim-reg machinery as I2 at the y_t side).
```

Total: **3 named imports (I2, I3, I4b) + 1 structurally forced
(I4a) + 1 import-contaminated (I5)**. The tier-brief mapping
(≥3 imports → BOUNDED) is satisfied at the conservative count of
{I2, I3, I4b}.

## 3. Classification

| Item | Tier |
|------|------|
| Y-S4b-RGE numerical closure (`m_H = 125.14 GeV`) | **NUMERICALLY CORRECT** (unchanged) |
| Y-S4b-RGE tier as POSITIVE THEOREM | **REVOKED** |
| Y-S4b-RGE tier as BOUNDED THEOREM with named imports {I2, I3, I4b} | **CORRECT** (this note) |
| I4 lattice-bare layer `λ_bare(a⁻¹) = 0` | **STRUCTURALLY FORCED** (PR #1023) |
| I4 runner-MSbar matching `λ_bare(a⁻¹) = λ^{MSbar}(M_Pl)` | **NAMED MATCHING ADMISSION** (PR #1023) |

## 4. Where the correction must propagate

Downstream notes and audits that cite Probe Y-S4b-RGE must reference
the **BOUNDED THEOREM** tier with the named imports {I2, I3, I4b},
not POSITIVE, when they need:

- the closure of the +12.03% Higgs-mass residual at S4b-op,
- the running-`λ` route as a retained ingredient,
- comparison of S4b-op operator-construction layer with retained
  S4b-positive theorems.

Notes that cite only the **numerical closure value** (`m_H ≈
125.14 GeV` to within ~0.1%) require no further change — the
numerical content is unaffected by the tier downgrade.

## 5. Source-only review-loop compliance

- Only a SOURCE NOTE is added; no synthesis / no output packet.
- The targeted source note (PR #948) is NOT edited from this PR.
- The catching PRs (#956 hostile downgrade, #1023 I4 refinement) are
  cited; this stanza records the corrected tier so it propagates
  independent of those PRs' merge state.
- A paired runner [`scripts/cl3_t1_corrections_v2_2026_05_10.py`](../scripts/cl3_t1_corrections_v2_2026_05_10.py)
  verifies the import-count threshold against the tier-brief mapping.
- Cached output: [`logs/runner-cache/cl3_t1_corrections_v2_2026_05_10.txt`](../logs/runner-cache/cl3_t1_corrections_v2_2026_05_10.txt).

## 6. Authority disclaimer

This is a source-only correction stanza. Audit verdict and downstream
status (retention, tier promotion) are set only by the independent
audit lane.
