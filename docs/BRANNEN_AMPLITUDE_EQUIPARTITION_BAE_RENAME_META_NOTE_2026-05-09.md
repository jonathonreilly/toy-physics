# Brannen Amplitude Equipartition (BAE) Rename Meta Note

**Date:** 2026-05-09
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status set only after independent audit
review.
**Authority role:** records the rename of "A1-condition" / "Brannen-Rivero
A1" / "A1 admission" to **"Brannen Amplitude Equipartition (BAE)"**
across the framework's documentation surface. Resolves the longstanding
naming collision with framework axiom A1 (the retained `Cl(3)`
local-algebra axiom).
**Primary runner:** [`scripts/frontier_bae_rename_meta.py`](../scripts/frontier_bae_rename_meta.py)
**Cache:** [`logs/runner-cache/frontier_bae_rename_meta.txt`](../logs/runner-cache/frontier_bae_rename_meta.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim. This note does
not write audit verdicts and does not promote any downstream theorem.
It records a vocabulary clarification.

## What this rename addresses

Throughout the framework's audit ledger, two distinct objects share the
label "A1":

1. **Framework axiom A1** = the retained `Cl(3)` local-algebra axiom
   per `MINIMAL_AXIOMS_2026-05-03.md`.
   This is one of two retained mathematical axioms (A1 + A2 = Cl(3) +
   Z³).

2. **The Brannen-Rivero "A1" assumption** = the amplitude-ratio
   constraint `|b|²/a² = 1/2` (equivalently `3a² = 6|b|²`, `Brannen
   c = √2`, `Koide Q = 2/3`) on the C_3-equivariant Hermitian circulant
   `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`. Introduced in
   [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
   as "Assumption 1" within the Koide derivation chain (alongside R1 =
   circulant form, R2 = eigenvalue spectrum).

The "A" was for *Amplitude*. The "1" was the first assumption in that
chain. The collision with framework axiom A1 was inherited from the
Brannen-Rivero literature.

## The new name

Going forward:

> The Brannen-Rivero amplitude-ratio constraint `|b|²/a² = 1/2` is
> renamed **"Brannen Amplitude Equipartition" (BAE)** — equivalently
> the **BAE-condition**.

Equivalent legacy names (all alias to BAE):

- "A1-condition"
- "A1 admission"
- "Brannen-Rivero A1"
- "BR-A1"
- "Frobenius equipartition `3a² = 6|b|²`"
- "Brannen amplitude equipartition"

In future branches, **"BAE"** is the canonical name. Existing landed and
open PRs grandfather the "A1" label with the BAE alias.

## Why this rename is the right one

The 17-probe campaign that ran 2026-05-07 to 2026-05-09 attacked closure
of the BAE-condition from 17 independent angles. Across the campaign,
the structural content of BAE became precisely characterized:

| Layer | Characterization |
|---|---|
| Brannen-Rivero original | "A1 = amplitude equipartition" |
| Frobenius level (Probe 7) | "`3a²` = `6|b|²` ⇔ multiplicity-weighted Frobenius equality on `M_3(ℂ)_Herm` under C_3-isotype decomposition" |
| ℝ-isotype level (Probe 12) | "`(1,1)` real-isotype counting principle" |
| Continuous-symmetry level (Probe 13) | "U(1)_b angular quotient on the b-doublet" |
| Algebra-impossibility level (Probe 14) | "non-algebraic linear extension of discrete C_3" |
| Spectrum-impossibility level (Probe 17) | "spectrum-non-preserving transformation; cannot be any unitary similarity" |
| Functional level (Probe 16) | "F1 vs F2 vs F3 canonical-functional choice on the (a, |b|)-plane" |

Across all these layers, the underlying object is the **equipartition
condition `3a² = 6|b|²`** in the Brannen circulant ansatz. The name
"Brannen Amplitude Equipartition" captures both the historical
Brannen-Rivero origin and the structural content (equipartition between
trivial and non-trivial isotype Frobenius norms).

## Cross-reference: campaign PRs (all use legacy "A1" name; future renamed)

The 17-probe campaign produced these source-notes / PRs (all using the
legacy "A1-condition" name):

| Probe | PR | Note (legacy filename) |
|---|---|---|
| Route F | #727 | `KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md` |
| Route E | #730 | `KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md` |
| Route A | #731 | `KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md` |
| Route D | #732 | `KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md` |
| Probe 1 | #735 | `KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md` |
| Probe 2 | #733 | `KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md` |
| Probe 3 | #736 | `KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md` |
| Probe 4 | #734 | `KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md` |
| Probe 5 | #738 | `KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md` |
| Probe 6 | #737 | `KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md` |
| Probe 7 | #740 | `KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md` |
| Synthesis | #751 | `KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md` |
| Probe 12 | #755 | `KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md` |
| Probe 13 | #763 | `KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md` |
| Probe 14 | #784 | `KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md` |
| Probe 15 | #788 | `KOIDE_A1_PROBE_CONTINUUM_LIMIT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe15.md` |
| Probe 16 | #789 | `KOIDE_A1_PROBE_Q_READOUT_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe16.md` |
| Probe 17 | #787 | `KOIDE_A1_PROBE_LATTICE_NON_CONJUGATION_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe17.md` |

All 18 PRs use the legacy "KOIDE_A1_*" filename pattern. Per the
review-loop file-immutability principle (already-landed source-notes
are not retroactively renamed at the filesystem level), these
filenames are grandfathered. Future BAE-related source-notes use
"KOIDE_BAE_*" prefix.

## Review-loop rule for future branches

When reviewing future branches that touch the Brannen amplitude
equipartition condition:

1. **Use "BAE" as the primary name**. Acceptable: "BAE-condition",
   "Brannen Amplitude Equipartition", "BAE admission". Mention the
   legacy "A1" alias parenthetically only when cross-referencing
   landed PRs.

2. **Filename convention for new source-notes**:
   `docs/KOIDE_BAE_<descriptor>_<status>_NOTE_<date>_<slug>.md`. Replace
   "A1" with "BAE" in new filenames.

3. **Naming-collision warning sections**: future source-notes touching
   BAE should still include a brief naming-collision warning citing
   this rename note, until the legacy "A1" alias is fully retired
   from active use.

4. **Audit-ledger row keys**: existing audit rows keyed by
   "koide_a1_*" remain at their current key (file immutability); new
   rows use "koide_bae_*". The rename does not migrate ledger keys.

## What this rename does NOT do

This note explicitly does **not**:

1. Modify any retained theorem on main. The 17-probe campaign's
   structural findings remain unchanged.
2. Reclassify the BAE admission's `claim_type` or `effective_status`.
   The admission status is independent of the name.
3. Promote any specific Probe's verdict. The campaign's terminal state
   (bounded admission with 3 structural-impossibility theorems on
   algebra-level closure + functional-choice residue at Q-level)
   stands.
4. Change the framework's axiom set. A1 (Cl(3)) and A2 (Z³) remain the
   only mathematical axioms.
5. Rename anything in already-landed PR source-notes. File immutability
   is preserved; the rename applies prospectively.

## Validation

```bash
python3 scripts/frontier_bae_rename_meta.py
```

The runner is a review-hygiene check, not a physics proof. It verifies:

1. The rename note is classified as `meta`.
2. The rename does not promote any audit row.
3. The campaign's structural findings (referenced) are not altered.
4. The framework axiom set (A1, A2) is unchanged.
5. The BAE name is consistently used in this note's body.
6. The legacy "A1-condition" alias is acknowledged.
7. Cross-references to all 18 campaign PRs are present.
