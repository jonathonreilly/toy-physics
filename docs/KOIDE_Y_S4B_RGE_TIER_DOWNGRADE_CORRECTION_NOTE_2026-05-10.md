# Probe Y-S4b-RGE — Positive→Bounded Tier Downgrade Correction Note

**Date:** 2026-05-10
**Type:** meta
**Claim scope:** source-level import inventory and tier-boundary guidance
for the unlanded Probe Y-S4b-RGE candidate. This note does not ratify
the target, set audit status, or promote a Higgs-mass closure; it records
that the candidate cannot be treated as a positive theorem while the
named MSbar and matching imports remain load-bearing.
**Status:** source-only correction stanza for Probe Y-S4b-RGE's tier
declaration.
**Runner:** [`scripts/cl3_t1_corrections_v2_2026_05_10.py`](../scripts/cl3_t1_corrections_v2_2026_05_10.py)
**Target note:** `KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`
(file lives on open PR #948 branch
`probe/y-s4b-rge-lambda-running-2026-05-08`).
**Review context:**
- [#956](https://github.com/jonathonreilly/cl3-lattice-framework/pull/956) — hostile
  audit Z-S4b-Audit downgrades Y-S4b-RGE from positive to bounded with
  named imports {I2 β_λ^(2), I3 β_λ^(3), I4 λ(M_Pl)=0 postulate}.
- [#1023](https://github.com/jonathonreilly/cl3-lattice-framework/pull/1023) —
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

Two hostile-review PRs subsequently raised the correction context:

1. **PR #956 (Z-S4b-Audit, hostile downgrade).** Audits the
   ingredient list of Y-S4b-RGE's closure and identifies **three
   imports**:

   | Import | Y-S4b-RGE ingredient | Status |
   |--------|----------------------|--------|
   | I2 | 2-loop β_λ coefficients (FJJ92, LWX03) | **IMPORTED** — dim-reg MSbar integrals; framework retains only the Casimir skeleton at 2-loop+ per Probe X-L1-MSbar. |
   | I3 | 3-loop β_λ coefficients (CZ12, BPV13) | **IMPORTED** — contains ~200 ζ(3) factors from D = 4 − 2ε integrals; framework's lattice `<P>`-scheme is foreign to dim-reg. |
   | I4 | `λ(M_Pl) = 0` BC | **POSTULATED, not derived** — Y-S4b-RGE §10 treats the boundary condition as an added framework-level premise rather than deriving it from the physical `Cl(3)` local algebra plus `Z^3` spatial substrate. |

   Per the tier-brief mapping (≥3 imports forces BOUNDED), Y-S4b-RGE
   downgrades from positive_theorem to **BOUNDED THEOREM**.

2. **PR #1023 (W-S4b-Classicality, I4 refinement).** Performs
   four-route foreclosure on `λ(M_Pl) = 0`. Concludes I4 is partially
   reclassified:

   - **At the lattice-bare layer:** `λ_bare(a⁻¹) = 0` is
     **STRUCTURALLY FORCED** by the proposed operator content (no
     marginal scalar quartic in the physical `Cl(3)` local algebra /
     `Z^3` spatial substrate skeleton at the cutoff scale).
   - **At the runner-MSbar layer:** the identification
     `λ_bare(a⁻¹) = λ^{MSbar}(M_Pl)` requires a
     **NAMED MATCHING ADMISSION** (the lattice-to-MSbar matching
     scheme is not internally derivable in the current source content).

   Net: I4 is no longer a "free postulate" but a "forced + matching
   admission". This does not lift the BOUNDED downgrade (the matching
   admission is still a named admission, and I2/I3 remain unchanged),
   but it pinpoints the residual structural content of I4.

This correction stanza records the import inventory that forces the
candidate tier boundary: if the Y-S4b-RGE target later lands with these
inputs still load-bearing, downstream audits should treat it as
bounded/import-contaminated rather than positive.

## 1. Corrected status declaration

| Field | Original (PR #948) | Corrected (this note) |
|-------|--------------------|------------------------|
| Type | positive_theorem | **bounded_theorem** |
| Claim type | positive_theorem | **bounded_theorem (with named imports)** |
| Verdict header | POSITIVE THEOREM | **BOUNDED candidate (with named imports {I2, I3, I4})** |
| Tier promotion claim | Inside ~5% positive-tier threshold | Numerical closure is close to the comparator, **but ingredient list is import-contaminated** at 3 named places. |

The numerical closure (`m_H = 125.14 GeV`, −0.09% from PDG) is not
recomputed here. The tier boundary is corrected from POSITIVE to
BOUNDED on the basis that **three of the closure's ingredients are
named imports**, not internally derived content.

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
| Y-S4b-RGE numerical closure (`m_H = 125.14 GeV`) | not recomputed here |
| Y-S4b-RGE tier as POSITIVE THEOREM | not supported with these imports |
| Y-S4b-RGE tier as bounded candidate with named imports {I2, I3, I4b} | review-level boundary recorded here |
| I4 lattice-bare layer `λ_bare(a⁻¹) = 0` | proposed structural part; not ratified here |
| I4 runner-MSbar matching `λ_bare(a⁻¹) = λ^{MSbar}(M_Pl)` | named matching admission |

## 4. Where the correction must propagate

Downstream notes and audits that cite Probe Y-S4b-RGE must preserve the
named imports {I2, I3, I4b} and should not cite it as POSITIVE when they
need:

- the closure of the +12.03% Higgs-mass residual at S4b-op,
- the running-`λ` route as an ingredient,
- comparison of S4b-op operator-construction layer with other S4b
  positive-theorem candidates.

Notes that cite only the **numerical closure value** (`m_H ≈
125.14 GeV` to within ~0.1%) require no further change — the
numerical content is unaffected by the tier downgrade.

## 5. Source-only review-loop compliance

- Only a SOURCE NOTE is added; no synthesis / no output packet.
- The targeted source note (PR #948) is NOT edited from this PR.
- The review-context PRs (#956 hostile downgrade, #1023 I4 refinement)
  are cited only as context; this stanza records the import inventory
  so it propagates independent of those PRs' merge state.
- A paired runner [`scripts/cl3_t1_corrections_v2_2026_05_10.py`](../scripts/cl3_t1_corrections_v2_2026_05_10.py)
  verifies the import-count threshold against the tier-boundary mapping.

## 6. Authority disclaimer

This is a source-only correction stanza. Audit verdict and downstream
effective status are set only by the independent audit lane.
