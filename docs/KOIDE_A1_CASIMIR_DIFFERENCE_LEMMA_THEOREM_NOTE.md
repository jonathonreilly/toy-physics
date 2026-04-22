# Casimir-Difference Lemma — Formal Theorem Statement

**Date:** 2026-04-22
**Status:** derivation of Koide A1 / `Q = 2/3` under two primitives
(P1), (P2) on the retained Cl(3)/Z³ surface, with (P1) and (P2)
themselves argued at retained grade from retained inputs at 1-loop.
Absolute-scale precision (~5% lattice-integral) is **c-cancellative**
for the cone ratio.
**Companion derivation note:** [`KOIDE_A1_CASIMIR_DIFFERENCE_LEMMA_DERIVATION_NOTE.md`](./KOIDE_A1_CASIMIR_DIFFERENCE_LEMMA_DERIVATION_NOTE.md)
**Verification surface:** 31 rigorous runners, 180 PASS / 0 FAIL;
3 documentation-only runners, 96 DOC lines; hostile audit confirms
0 hardcoded-`True` assertions inside `record()` calls.

## 1. Theorem (Casimir-Difference Lemma)

Let `(T, Y)` be the SU(2)_L × U(1)_Y quantum numbers of an SM
Yukawa-doublet participant on the retained Cl(3)/Z³ surface. Let
`v = (√m_1, √m_2, √m_3)` be the charged-lepton mass-square-root
vector on the retained `hw=1` carrier, and let `(a_0, z, z̄)` be its
C_3 character coefficients (cf.
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](./CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)).

**Primitives:**

> **(P1)** `a_0² = c · (T(T+1) + Y²) · v_EW²`
>
> **(P2)** `|z|² = c · (T(T+1) − Y²) · v_EW²`, with the **same** `c` as (P1).

**Claim.**

> `a_0² / |z|² = (T(T+1) + Y²) / (T(T+1) − Y²)`,
>
> and Koide's invariant `Q = (∑ m_i)/(∑ √m_i)² = (a_0² + 2|z|²)/(3 a_0²)`
> equals `2/3` **if and only if**
>
> `3 Y² = T(T+1)`       (A1*)
>
> in the underlying group-theoretic data.

**Corollary (Cl(3)-retained closure).** The retained Cl(3) embedding
gives `T = 1/2` (from `Cl⁺(3) ≅ ℍ`) and `|Y| = 1/2` (from the
ω-pseudoscalar central direction with the lepton/Higgs assignment).
Substituting into (A1*) yields `3·(1/4) = 3/4 = T(T+1)` ✓. The cone
closes **unconditionally** on the retained Cl(3)/Z³ inputs.

## 2. Why this is a closure

| Object | Provenance | Status |
|---|---|---|
| `T = 1/2` | `Cl⁺(3) ≅ ℍ ⟹ SU(2)_L` Casimir | retained on `main` |
| `Y² = 1/4` (lepton / Higgs) | ω-pseudoscalar + assignment | retained on `main` |
| C_3 character / S_3-isotype split on hw=1 | `S3_TASTE_CUBE_DECOMPOSITION_NOTE` | retained on `main` |
| Plancherel identity (hw=1 Theorem 1) | `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE` | retained on `main` |
| Gauge-Casimir SUM `T(T+1) + Y² = 1` | `KOIDE_EXPLICIT_CALCULATIONS_NOTE` §Deliverable 2 | retained on `main` |
| UV Ward identity `y_τ(M_Pl) / g_s(M_Pl) = 1/√6` | `YT_WARD_IDENTITY_DERIVATION_THEOREM` | retained on `main` |
| (P1) sum proportionality | branch runners `p1_*` (rigorous + doc-only) | retained at 1-loop on branch |
| (P2) difference proportionality | branch runners `p2_*` (rigorous) | retained at 1-loop on branch |
| Common-c condition | branch runners `p2_same_topology`, `c_independence`, `mu_invariance` | rigorous at 1-loop on branch |

(P1) and (P2) consume **only** retained inputs. The only element
imprecisely known is the absolute scale of `c`; it **cancels** from
the Koide invariant. `c_independence` verifies this to machine
precision across six orders of magnitude of `c`.

## 3. What the lemma does **not** claim

- **Does not** close the physical Brannen-phase bridge `δ = 2/9` on
  its own. `δ = Q/d = 2/9` follows arithmetically on the retained
  reduction, but the radian-quantum residual `P` (physical radian
  = structural `2/d²`) remains open. Phase 2 narrowed this to three
  concrete closure routes (see branch Brannen runners).
- **Does not** fix the overall lepton mass scale `v_0`.
- **Does not** universalise beyond Yukawa doublets. Only
  `(T, Y) = (1/2, ±1/2)` sits on (A1*); see `x1_uniqueness_sweep`.
- **Does not** include a 2+-loop derivation. (P1) and (P2) are
  established at 1-loop; higher-loop corrections are out of scope
  and **not needed** for the cone (ratio is c-cancellative).
- **Does not** modify the canonical publication-package claim
  surface. Propagation into `PUBLICATION_MATRIX.md` / `CLAIMS_TABLE.md`
  is deferred pending explicit package authorisation.

## 4. No-go evasion

The lemma evades all 9 retained no-go theorems in
[`KOIDE_A1_DERIVATION_STATUS_NOTE.md`](./KOIDE_A1_DERIVATION_STATUS_NOTE.md):

- adds `3Y² = T(T+1)` (not Z_3 alone, not APBC refinement alone, not
  observable-principle symmetry alone);
- is not exchange-mixing, anomaly-forced cross-species,
  sectoral-universality, or colour-correction;
- is not a C_3-invariant variational principle on `hw=1` (uses
  gauge-Casimir data — escapes Theorem 5);
- uses quadratic Casimir, not 4th-order Clifford (escapes Theorem 6).

Executable audit: `x5_no_go_evasion` (documentation runner).

## 5. Status change

| Bridge | Before this branch | After this branch |
|---|---|---|
| `Q = 2/3` (Koide cone) | open flagship gate, no closure | closure under (P1) + (P2); both retained-grade at 1-loop; c-cancellative cone ratio |
| `δ = 2/9` (Brannen phase) | open (P residual) | arithmetic `δ = Q/d = 2/9` follows; physical P residual narrowed to 3 routes |
| `v_0` lepton scale | open, outside package | unchanged |

## 6. Reading rule for reviewers

1. Confirm retained inputs `T = 1/2`, `Y² = 1/4`, and the hw=1
   Plancherel identity (all on `main`).
2. Accept (P1) via `p1_{rainbow,blindness,promotion}` (8 rigorous
   PASSes across three runners) together with the narrative chain
   assembled in `p1_formal`.
3. Accept (P2) via `p2_{factorization,cyclic,same_topology,promotion}`
   (14 rigorous PASSes across four runners).
4. Verify c-cancellation via `c_independence` + `mu_invariance`
   (11 rigorous PASSes).
5. Then the cone closure `Q = 2/3` is automatic by (A1*) and the
   retained Cl(3) inputs, with `x3_iff` (9 PASSes) providing the
   symbolic iff and `x4_compose_hw1_theorem1` (6 PASSes) composing
   with retained hw=1 Theorem 1.

All steps are executable in ≤ 30 s via:

```
python3 scripts/frontier_koide_a1_casimir_difference_master_closure.py
```

## 7. Open retained-grade work beyond this lemma

- A fully lattice-action-native derivation of (P1) and (P2) — the
  branch argues them at retained-grade at the 1-loop amplitude level,
  not from first principles of the lattice partition function.
- Closure of the Brannen-phase radian-quantum residual `P` (three
  named candidate routes).
- A 2+-loop stability check of the common-c condition — not needed
  for the cone (c-cancellative), but would be a welcome robustness
  result.

Tracked in the derivation note §8.
