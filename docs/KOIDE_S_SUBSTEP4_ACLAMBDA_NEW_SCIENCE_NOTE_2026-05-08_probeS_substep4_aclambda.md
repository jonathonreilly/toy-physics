# Substep-4 AC_λ Imported-Tool Closure Attempt (Bounded)

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Support class:** bounded negative support (adds imported-tool stress tests;
no positive promotion)
**Scope:** Imported-tool stress test on the AC_λ atom of the substep-4 atomic
decomposition. Applies three independent mathematical tools — topological
K-theory of the BZ-corner momentum bundle (AC_λ.struct intrinsic
test), categorical groupoid of C_3-equivariant flavor labelings
(AC_λ.label test), and modular flavor SL(2,Z) (orthogonal test) — as
bounded imports rather than new repo axioms.
Source-note proposal; audit verdict and downstream status are set only
by the independent audit lane.
**Authority role:** source-note proposal — substep-4 surface status
remains `bounded_theorem`. This note documents three imported-tool attempts
on AC_λ and records their fates under hostile-review tier classification.
**Loop:** physics-loop / probe-S-substep4-aclambda-imported-tool-20260508
**Primary runner:** [`scripts/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.py`](../scripts/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.py)
**Cache:** [`logs/runner-cache/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.txt`](../logs/runner-cache/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.txt)

## Authority disclaimer

This is a source-note proposal. The independent audit lane has full
authority to retag, narrow, or reject. The author does NOT propose a
positive_theorem promotion at this time; the result is bounded because
each imported tool either (a) merely relocates the bounded dependency
to a postulated bridge, or (b) supplies content equivalent to the
audit-pending meta dependency already recorded in the prior AC_λ partial
closure (PR #890). No new axioms are added. No PDG values are imported.

## Question

The substep-4 atomic decomposition note
[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
decomposed the substep-4 admitted context as

```
AC_narrow = AC_φ ∧ AC_λ ∧ AC_φλ
```

The recent AC_λ partial closure note
[`SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md`](SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md)
further sub-decomposed AC_λ as

```
AC_λ = AC_λ.struct ∧ AC_λ.label
```

with two distinct bounded-tier inheritances:

- **AC_λ.struct** (block-diagonality of free-fermion propagator on
  hw=1 corner basis): runner-certified bounded candidate via interval-
  certified Kawamoto-Smit + Reed-Simon §VIII.5 simultaneous-
  diagonalization. **Bounded tier inherited from the Kawamoto-Smit
  upstream**, which is itself `bounded_theorem` (not positive) on main.
- **AC_λ.label** (species-kind label characterization): characterized
  as labeling-convention bridge under audit-pending meta companion notes
  (PR #728 C_3-preserved interpretation; PR #729 conventions
  unification; PR #790 BAE rename).

The 30-probe BAE campaign (PR #836) attacked AC_φλ under the original
derivation surface and left it bounded. The AC_λ atom was not attacked
under these imported mathematical lenses — that is the gap this note
addresses.

For this bounded stress test, imported mathematical tools may act on
existing retained content as structural lenses only. They are NOT new
content axioms.

**Question:** Can imported mathematical tools — applied to retained Cl(3)/Z³
content + the substep-4 BZ-corner triplet on hw=1 — close AC_λ atom
completely, ratcheting AC_λ from sharpened-bounded to positive?

Three imported tools natural to AC_λ:

1. **Topological K-theory** of the BZ-corner momentum bundle on the
   3-torus T³ (AC_λ.struct intrinsic closure candidate — bypass the
   Kawamoto-Smit-inheritance).
2. **Categorical groupoid** of C_3-equivariant flavor labelings on the
   M_3(C)-irreducible 3-orbit (AC_λ.label intrinsic closure candidate —
   bypass the audit-pending-meta dependency).
3. **Modular flavor SL(2,Z)** action on the hw=1 triplet (independent
   closure test — different mathematical lens, same physics surface).

## Answer

**No.** Each of the three imported tools faces structural obstructions
that prevent positive closure of AC_λ. Under hostile-review tier
classification:

- **K1 (Topological K-theory):** the K^0(T³) classification of the
  hw=1 momentum-space sub-bundle is mathematically rigorous and gives
  the **same** corner-triplet 3-fold structure as Kawamoto-Smit, but the
  identification of "K-theoretic class = block-diagonal propagator
  species" requires the **same translation-invariance + non-degenerate
  joint eigenspace structure** that Kawamoto-Smit already supplies.
  K-theory does NOT bypass the KS inheritance — it derives the same
  fact via a more abstract route. AC_λ.struct **remains** bounded.

- **K2 (Categorical groupoid):** the C_3-equivariant labelings on the
  M_3(C) 3-orbit have **exactly three** equivariant bijection choices
  (the three cyclic shifts),
  identical to the parameter-counting result of PR #790 + PR #728. The
  groupoid gives a clean categorical *characterization* of the residual
  "which cyclic shift labels electron/muon/tau" question, but does NOT
  *derive* the specific shift — that remains a labeling convention.
  AC_λ.label **remains** dependent on audit-pending meta.

- **K3 (Modular flavor SL(2,Z)):** modular flavor models (Feruglio,
  Kobayashi, et al.) attach a modular form to the flavor triplet under
  a congruence subgroup `Γ(N)`. For N=3 (matching the C_3 cyclicity),
  `Γ(3)` has 3-dimensional irreducible representations, consistent with
  the hw=1 triplet, but the **specific modular form** (which modular
  weight, which `Γ(N)`) is a separate postulated bridge requiring an
  *external import of modular-flavor framework machinery* — three
  postulated bridges (level N, weight k, congruence subgroup choice).
  This is materially the same trap that closed the spectral-action
  probe (PR #730): **NCG/modular import = multi-bridge import**,
  not a one-bridge closure.

The combined picture: **AC_λ resists imported-tool closure at the
positive tier** for the same structural family of reasons that closed
NCG/spectral-action and the broader convention-dependence trap. New
science tools provide **fresh structural characterizations** of AC_λ.struct
and AC_λ.label, but do not bypass the bounded inheritances. AC_λ
narrowing is **extended** (more characterization angles) but not
**promoted** (no surface tier change).

Result tier: **bounded**. Adds imported-tool stress tests around PR #890;
does not ratchet substep-4 to positive.

## Setup

### Premises (P_min for AC_λ imported-tool stress test)

| ID | Statement | Class |
|---|---|---|
| Baseline local algebra | physical Cl(3) local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Baseline substrate | Z³ spatial substrate | repo baseline; same source |
| KS | Kawamoto-Smit phase form on Z³ APBC | upstream `bounded_theorem`: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md) |
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra; distinct joint translation characters | upstream: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md), [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| NQ | M_3(C) on hw=1 has no proper exact quotient | upstream: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md) |
| ACλpartial | AC_λ partial closure (Kawamoto-Smit-inherited + audit-pending meta) | upstream-bounded: [`SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md`](SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md) |
| C3pres | C_3[111] is the preserved load-bearing symmetry | audit-pending meta: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md) |
| BAErename | AC_φλ = BAE = amplitude-equipartition `|b|²/a² = 1/2` | audit-pending meta: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md) |
| ImportedToolScope | Imported mathematical tools act as bounded structural lenses on retained content | review-loop bounded-import scope |

### Forbidden imports

- NO PDG observed values (no `m_e`, `m_μ`, `m_τ` numerical inputs)
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new content axioms added beyond the physical Cl(3) local algebra and
  Z³ spatial substrate baseline
- NO HK + DHR appeal (Block 01 audit retired this)
- NO BAE-condition closure claim (AC_φλ remains bounded)
- NO physical-observable distinguishability claim on H_{hw=1} (AC_φ
  remains bounded structural no-go candidate)

### Imported Tools Used As Structural Lenses

The following mathematical tools are used as structural lenses on retained
content, NOT as new physics axioms:

- **K-theory** of the BZ-corner momentum bundle on T³.
- **Categorical structures**: groupoid `[*//C_3]`, finite-group
  representation category Rep(C_3), 2-vector spaces.
- **Modular forms** under congruence subgroups `Γ(N) ⊂ SL(2,Z)`.

Each tool's identification with framework content is bounded by
explicitly under hostile-review tiering (RETAINED/IMPORTED/POSTULATED)
in the per-tool analysis below.

## Imported Tool K1: Topological K-theory of BZ-corner bundle

### K1 setup

The Brillouin zone for Z³ is the 3-torus `T³ = (R/2πZ)³`. The hw=1 sub-
locus consists of three discrete points (the three corners
`{(π,0,0), (0,π,0), (0,0,π)}`). Over each corner, the staggered-Dirac
spinor space is a finite-dimensional complex vector space (the local
Dirac fiber).

Topological K-theory `K^0(T³)` classifies complex vector bundles on T³
up to stable isomorphism. For T³:

```
K^0(T³) ≅ Z^4
K^1(T³) ≅ Z^4
```

The hw=1 momentum sub-bundle picks out 3 isolated fibers; its K-theory
class is determined by the **rank** at each corner plus the
**equivariant character** under lattice translations.

### K1 hostile-review tiering

| Ingredient | Class | Justification |
|---|---|---|
| `T³` as BZ for Z³ | RETAINED | Standard Pontryagin dual of Z³; not external |
| K-theory functor `K^0(·)` | IMPORTED | Atiyah-Hirzebruch construction; standard math |
| Equivariant character `T_μ ↦ ±1` | RETAINED | Direct from Z³ translation action on staggered modes |
| Identification "K-class = species-label" | **POSTULATED** | Requires bridge: K-theoretic equivariant rank ↔ free-propagator species index |

### K1 closure attempt

**Claim:** K^0_{T³,equiv}(hw=1 sub-locus) decomposes as `Z^3` with the
three generators corresponding to the three corners, each generator
distinguished by its equivariant character `(±1, ±1, ±1)` with exactly
one `−1`. This decomposition is **automatic** (no Kawamoto-Smit
inheritance) — it follows from the equivariant K-theory of three points
under Z³.

**Hostile-review check:** does the K-class decomposition close AC_λ.struct
INTRINSICALLY (bypassing the KS-inheritance)?

**Answer:** No. The reason: K-theory classifies vector bundles up to
stable isomorphism — it tells us **what topological data the corners
carry** but does NOT, on its own, tell us **how the free-propagator
behaves on these bundle classes**. The propagator's block-diagonality
is a statement about the OFF-DIAGONAL kernel of a *specific operator*
(the Kawamoto-Smit kinetic operator K), not a topological invariant of
the bundle.

Concretely: any operator on the hw=1 fiber that is *not* translation-
invariant could couple the three K-classes. The vanishing of K-class
mixing requires the *additional* input "K is translation-invariant",
which is the Kawamoto-Smit forcing content. Therefore:

```
K-theoretic closure of AC_λ.struct = K-theoretic decomposition  AND
                                      translation-invariance of K
                                    = K-theoretic decomposition  AND
                                      Kawamoto-Smit inheritance  (same as before)
```

K-theory does NOT bypass the KS-inheritance — it derives the same fact
via a more abstract route, but with the **same load-bearing input**.

**Conclusion K1:** AC_λ.struct via K-theory has the **same bounded
tier** as AC_λ.struct via direct Kawamoto-Smit + Reed-Simon. The K-
theoretic route adds **one postulated bridge** (the K-class
↔ species-label bridge identification), making the K-theoretic route
materially *worse* by primitive count, not better.

## Imported Tool K2: Categorical groupoid of C_3-equivariant labelings

### K2 setup

The hw=1 corner triplet under the preserved C_3[111] symmetry is a free
C_3 torsor. The "species-labeling" of the hw=1 triplet is a
C_3-equivariant bijection

```
F: hw=1 triplet  →  Set_3        (both treated as Z/3Z-torsors)
```

picking out which abstract label the labeling assigns to each corner.
There are three equivariant choices:

```
{e/μ/τ, μ/τ/e, τ/e/μ}    (the three cyclic shifts; one C_3-orbit)
```

### K2 hostile-review tiering

| Ingredient | Class | Justification |
|---|---|---|
| C_3 action on hw=1 triplet | RETAINED | Preserved C_3[111] per C3pres; M_3(C) on hw=1 per BlockT3 |
| C_3 action groupoid / torsor language | IMPORTED | Standard category-theory construction; no new physics axiom |
| Equivariant labeling choices = 3 | RETAINED | Follows from free C_3-torsor maps |
| Identification "labeling choice = generation label" | **POSTULATED** | Requires bridge: groupoid orbit ↔ SM e/μ/τ assignment |

### K2 closure attempt

**Claim:** There are exactly three C_3-equivariant labeling choices for
the hw=1 triplet, corresponding to the
three cyclic shifts. The "label-class" structure is **fully
characterized** by this groupoid — there are no other C_3-equivariant
labelings.

**Hostile-review check:** does the groupoid characterization close
AC_λ.label INTRINSICALLY (bypassing the audit-pending meta)?

**Answer:** No. The groupoid gives a clean **characterization** of the
residual labeling ambiguity (3 choices, all C_3-shifted of each
other), but it does NOT *select* one choice over the others — that
selection remains a labeling convention. This is exactly the content
of PR #790 (BAE rename): the AC_λ.label is a labeling-convention
question, isomorphic in nature to the PDG convention `{u, c, t}`,
`{ν_1, ν_2, ν_3}`, etc.

Concretely: any of the three choices yields the same physics on the
M_3(C) algebra. Selecting one is a bookkeeping operation. The groupoid
provides the **language** to state this cleanly, but does not derive
the specific selection.

**Conclusion K2:** AC_λ.label via C_3-torsor labelings characterizes
the residual labeling convention more cleanly, but **does not derive**
the convention away. The groupoid analysis recovers the same content
as PR #790's parameter-counting + PR #728's C_3-preserved interpretation,
just in categorical language. AC_λ.label still depends on the audit-
pending meta.

## Imported Tool K3: Modular flavor SL(2,Z) action

### K3 setup

Modular flavor models (Feruglio 2019; Kobayashi-Tanimoto 2018) attach
to each fermion field a modular form of definite weight `k` under a
congruence subgroup `Γ(N) ⊂ SL(2,Z)`. For `N = 3` (matching the C_3
cyclicity in the framework), `Γ(3)` has a 3-dimensional irreducible
representation in the projective finite modular quotient commonly
identified with `A_4`.

The candidate modular flavor identification for AC_λ:

```
hw=1 triplet under C_3 = 3-dim irrep of the level-3 finite modular quotient
                       = weight-2 modular forms under Γ(3)
```

### K3 hostile-review tiering

| Ingredient | Class | Justification |
|---|---|---|
| C_3 cyclicity on hw=1 | RETAINED | Per BlockT3 + C3pres |
| SL(2,Z) modular group | IMPORTED | Standard arithmetic group; not new physics |
| Choice of congruence subgroup level N=3 | **POSTULATED** | Requires postulating N=3 (vs N=2, 4, 6 alternatives) |
| Choice of modular weight k=2 | **POSTULATED** | Requires postulating k=2 (vs k=4, 6 alternatives) |
| Level-3 finite-modular quotient structure | IMPORTED | Standard arithmetic structure; not a repo axiom |
| Identification "modular form value = Yukawa coefficient" | **POSTULATED** | The Feruglio dictionary, a separate bridge |

### K3 closure attempt

**Claim:** A weight-2 modular form of `Γ(3)` evaluated at the modular
parameter `τ` produces a 3-component triplet whose components transform
under the level-3 finite modular quotient as the 3-dim irrep, matching
the hw=1 C_3-triplet.

**Hostile-review check:** does modular flavor close AC_λ INTRINSICALLY?

**Answer:** No. The modular flavor route faces **three postulated
bridges** structurally analogous to the NCG/spectral-action probe's
four-import bridge (PR #730):

- Congruence subgroup level `N = 3` is a choice (N=2 gives `S_3`,
  N=4 gives `S_4`, N=6 gives `S_4 × Z/2`).
- Modular weight `k = 2` is a choice (k=4 gives 5-dim modular forms,
  k=6 gives 7-dim).
- The modular parameter `τ` value is a free parameter — different `τ`
  give different numerical Yukawa values.

Crucially, **the modular-form-to-Yukawa dictionary is a separate
postulated bridge**: nothing in retained Cl(3)/Z³ + BlockT3 selects
weight-2 forms over weight-4, nor `Γ(3)` over `Γ(2)`. The modular
flavor route is a fresh instance of the **convention-dependence trap**
identified in `KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`
(Routes A/D/E/F/Probe-4 family): "framework primitives do not fix
canonical normalizations".

**Conclusion K3:** Modular flavor SL(2,Z)/Γ(3) is a separate imported
route (three postulated bridges: level, weight, dictionary), not a one-bridge
closure. It does not bypass the convention-dependence trap; it merely
relocates it (from "cutoff function shape" / "hypercharge convention" /
"root-length normalization" to "congruence subgroup level + modular
weight + modular parameter").

## Synthesis: AC_λ resists imported-tool closure

The three imported tools above are **independent angles** on AC_λ:

| Tool | Closes AC_λ.struct? | Closes AC_λ.label? | Postulated bridge count |
|---|---|---|---|
| K1 K-theory | Same bounded tier as KS (no bypass) | Not addressed | 1 extra bridge (K-bridge) |
| K2 Groupoid | Not addressed | Same labeling-convention as PR #790 | 1 extra bridge (label bridge) |
| K3 Modular | Not addressed | Same labeling-convention | 3 extra bridges (level, weight, dict) |

The unified pattern: **each imported tool provides a fresh structural
lens on AC_λ but does not bypass the bounded inheritances**. The tools
reproduce or relocate the convention-dependence trap, mirroring the
PR #730 spectral-action probe and the broader Koide Frobenius-equipartition campaign
synthesis (`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`).

This is the same meta-pattern that closed Routes A/D/E/F + Probe 4:
*new mathematical tools relocate, but do not eliminate, the
identification residual*. AC_λ joins this family of bounded-with-
sharpened-characterization results.

## Theorem (AC_λ imported-tool bounded stress test)

**Theorem (bounded; imported-tool stress test).** On the physical Cl(3)
local algebra + Z³ spatial substrate baseline + retained upstream
authorities + audit-pending meta (C3pres, ConvU, BAErename) + imported
tools (K-theory, categorical structures, modular forms, all used as
structural lenses with explicit bridge accounting):

```
The AC_λ atom of the substep-4 atomic decomposition does NOT close
positively under any of the three imported tools (K1, K2, K3).

K1 (K-theory of BZ-corner bundle):
  AC_λ.struct has the same bounded tier via K-theory as via
  direct Kawamoto-Smit + Reed-Simon. K-theory adds one postulated bridge
  (the K-class ↔ species-label bridge) without bypassing the
  translation-invariance load-bearing input.

K2 (C_3-torsor labelings):
  AC_λ.label is characterized cleanly by the C_3-torsor language
  (3 equivariant labeling choices) but the residual labeling convention
  is NOT derived — only re-described in categorical language.

K3 (Modular flavor SL(2,Z)/Γ(3)):
  Materially worse: requires three postulated bridges (level N=3,
  weight k=2, modular-form-to-Yukawa dictionary), structurally
  analogous to the Probe 4 spectral-action four-import trap.

Net effect on substep-4 admission count:
  AC_φ ∧ AC_λ ∧ AC_φλ  →  AC_φ ∧ AC_λ ∧ AC_φλ        (UNCHANGED at 3 atoms)

Net effect on AC_λ partial closure characterization:
  AC_λ.struct bounded inheritance: KS upstream + (3 imported redundant routes)
  AC_λ.label  bounded inheritance: audit-pending meta + (1 imported
                                     categorical characterization)

Substep-4 surface status: bounded_theorem (UNCHANGED)
```

**Proof.** The three imported tools K1, K2, K3 are independent
mathematical lenses on the physical Cl(3) local algebra + Z³ spatial
substrate + BlockT3 content. Each is
analyzed under hostile-review tiering (RETAINED/IMPORTED/POSTULATED)
in §§K1-K3 above. The runner verifies:

- K1: the K-theoretic decomposition of K^0_{T³, equiv}(hw=1 sublocus)
  produces a Z^3 with the three corners as generators, but the
  block-diagonality of the propagator requires the *additional*
  translation-invariance input — the same KS load-bearing content.
- K2: the C_3-torsor language has exactly 3 equivariant labeling choices.
  This is **isomorphic in content** to PR #790's parameter-counting result
  (3 cyclic-shift bijections). No selection of a specific choice is forced.
- K3: modular flavor under Γ(3) requires three postulated bridges
  (level, weight, dictionary). Each is an external import equivalent
  in bridge count to the spectral-action probe's four-import trap.

The unified conclusion is that imported tools applied to AC_λ
**relocate** the bounded dependencies (sometimes adding extra
postulated bridges) but do not **eliminate** them. ∎

## Comparison to prior work

| Prior attack on AC_λ | Status | Mechanism |
|---|---|---|
| Block 04 (single-clause AC) | bounded with single-clause AC | Pre-narrowing |
| Substep-4 atomic decomposition (PR #635) | bounded with 3-atom AC | Atomic split |
| Rigorization 2026-05-09 | interval-certified bounded candidate | Per-atom interval certification |
| AC_λ partial closure (PR #890) | bounded with 2-sub-atom AC_λ | Sub-decomposition + KS-inheritance + meta dependency |
| **This note (imported-tool stress test)** | **bounded with sharpened characterization** | **Three imported tools (K1/K2/K3) each fail to bypass the bounded inheritances; convention-dependence trap reproduced** |

The meta-pattern is now established: **AC_λ closure attempts via imported
tools all face the same convention-dependence trap as the Koide
Frobenius-equipartition campaign + Probe 4 spectral-action**. AC_λ remains
bounded under both prior surface and imported-tool scope, modulo audit-pending
meta acceptance and Kawamoto-Smit upstream promotion.

## What this narrowing proposes

- **AC_λ subjected to imported-tool stress test** under three independent
  tools: K-theory (K1), categorical groupoid (K2), modular flavor (K3).
- **Each tool fails to bypass the bounded inheritances** of the prior
  AC_λ partial closure (PR #890).
- **K1 provides an alternative derivation of AC_λ.struct** but with the
  same load-bearing input (translation-invariance of K).
- **K2 provides a clean categorical characterization of AC_λ.label**
  but does not derive the labeling convention.
- **K3 is materially worse** (three postulated bridges, same trap as
  spectral-action).
- **Substep-4 admission count unchanged** at 3 atoms (AC_φ ∧ AC_λ ∧
  AC_φλ); AC_λ characterization SHARPENED by adding three imported
  structural lenses.

## What this narrowing does NOT close

- The substep-4 surface status remains `bounded_theorem`.
- AC_λ itself remains a bounded atom (no positive promotion).
- AC_φ remains a bounded structural no-go candidate within the current
  framework surface.
- AC_φλ (= BAE) remains bounded per the 30-probe campaign
  (PR #836).
- Kawamoto-Smit upstream remains `bounded_theorem` (its own audit
  status unchanged).
- The audit-pending meta companion notes (PR #728, PR #729, PR #790)
  remain audit-pending.
- No claim about specific SM mass values, CKM/PMNS angles, or any PDG
  observable.
- The parent staggered-Dirac realization gate remains open at
  positive_theorem tier.
- L3a trace-surface bounded obstruction status unchanged.
- P3 Planck Orientation Principle bounded status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| K-theory does not bypass KS-inheritance (K1) | Exhibit a translation-NON-invariant kinetic operator on the BZ-corner bundle whose K-theoretic block-diagonality holds anyway — refutes K1. |
| Groupoid does not derive labeling convention (K2) | Exhibit a categorical/torsor construction whose codomain selection is forced by retained content — refutes K2. |
| Modular flavor is multi-bridge import (K3) | Derive `(N=3, k=2, dictionary)` from retained `Cl(3) + Z³ + BlockT3` content alone — refutes K3. |
| AC_λ resists imported-tool closure | Exhibit an imported mathematical tool that derives both AC_λ.struct (without KS-inheritance) AND AC_λ.label (without audit-pending meta) — refutes the bounded stress test. |

## Status

```yaml
source_proposed_surface_status: bounded_theorem (sharpened; imported-tool stress test around AC_λ partial closure)
proposed_claim_type: bounded_theorem
audit_review_points: |
  Conditional on:
   (a) independent audit confirmation that K1 K-theoretic decomposition
       of K^0_{T³,equiv}(hw=1 sub-locus) requires translation-invariance
       of the propagator operator (so KS inheritance is not bypassed);
   (b) independent audit confirmation that K2 C_3-torsor labelings have
       exactly 3 equivariant choices, matching PR #790 parameter-counting,
       and that no choice is forced;
   (c) independent audit confirmation that K3 modular flavor under
       Γ(3) requires three postulated bridges (level, weight, dictionary)
       structurally analogous to the Probe 4 spectral-action trap;
   (d) independent audit confirmation that the substep-4 admission
       count is UNCHANGED (still AC_φ ∧ AC_λ ∧ AC_φλ; no atom removal);
   (e) independent audit confirmation that the partial AC_λ closure of
       PR #890 is NOT promoted (still inherits bounded tier from KS +
       audit-pending meta).
hypothetical_axiom_status: null
admitted_observation_status: |
  AC_λ.struct: still inherits bounded tier from Kawamoto-Smit upstream
  (K1 K-theoretic alternative requires the same translation-invariance
  load-bearing input).
  AC_λ.label: still depends on audit-pending meta companion notes (K2
  groupoid provides clean characterization but no selection; K3 modular
  flavor is materially worse with three postulated bridges).
  Substep-4 admission residual after this note: AC_φ + AC_λ (still 2
  sub-atoms) + AC_φλ + inherited Kawamoto-Smit upstream + audit-pending
  meta + (three imported redundant structural characterizations of AC_λ).
claim_type_reason: |
  Bounded sharpened-characterization result: the AC_λ atom of the
  substep-4 atomic decomposition does NOT close positively under any
  of three independent imported tools (K-theory, categorical
  groupoid, modular flavor). Each tool either reproduces the existing
  bounded inheritance (K1, K2) or is materially worse with multi-
  bridge import (K3). The substep-4 surface status remains
  bounded_theorem with admission count unchanged at 3 atoms. The new
  content is the structural sharpening: AC_λ now has FOUR equivalent
  characterizations (Kawamoto-Smit, K-theory, groupoid, modular) all
  hitting the same bounded inheritance.
independent_audit_required_before_any_effective_status_change: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The AC_λ atom is subjected to three imported-tool attacks (K1, K2, K3), each closed negatively with explicit bridge accounting. No new obstruction introduced; existing AC_λ bounded inheritances confirmed under multiple lenses. |
| V2 | New derivation? | The three-tool comparative analysis (K-theory vs groupoid vs modular flavor) with hostile-review tiering (RETAINED/IMPORTED/POSTULATED) is new structural content. The unified meta-pattern observation (imported tools relocate but do not eliminate the convention-dependence trap, mirroring Probe 4) is new audit-defensibility content. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) K-theoretic equivariant decomposition validity; (ii) C_3-torsor labeling-count correctness; (iii) modular-flavor bridge count; (iv) RETAINED/IMPORTED/POSTULATED tiering of each ingredient; (v) the unchanged substep-4 admission count. |
| V4 | Marginal content non-trivial? | Yes — bounded imported tools test whether AC_λ escapes the PR #890 partial-closure boundary. The bounded-negative result closes a candidate escape route from PR #890's bounded characterization without adding a repo-wide axiom. |
| V5 | One-step variant? | No — the three tools (K-theory, groupoid, modular flavor) attack different sub-aspects of AC_λ via different mathematical structures. Each tool has its own hostile-review tiering. The unified synthesis is not a relabel of PR #890 or the Probe 4 spectral-action note. |

**Source-note V1-V5 screen: pass for sharpened-bounded audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of PR #890 (AC_λ partial closure). PR #890
  decomposed AC_λ into struct ∧ label and assigned bounded
  inheritances; this note attacks those inheritances under three
  independent imported tools and verifies they survive the attack.
- Is NOT a relabel of Probe 4 (spectral-action). Probe 4 attacked the
  Koide Frobenius-equipartition condition
  (= BAE = AC_φλ); this note attacks AC_λ specifically. Different
  atom, different tools (K-theory, groupoid, modular vs spectral
  action), same meta-pattern (convention-dependence trap).
- Identifies a unified meta-pattern: **AC_λ under imported-tool scope
  remains bounded with sharpened characterization**, mirroring the
  Koide Frobenius-equipartition condition under the same imported-tool
  scope (Probe 4).
- Per `feedback_special_forces_seven_agent_pattern.md`: AC_λ
  specifically was the un-attacked atom under imported-tool scope (AC_φλ
  exhausted by 30-probe; AC_φ rigorized to bounded structural no-go);
  this single 3-tool probe is the sharp narrow attack on the un-
  attacked atom.

## Cross-references

- Parent atomic decomposition: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- AC_λ partial closure (prior round): [`SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md`](SUBSTEP4_AC_LAMBDA_SEPARATE_CLOSURE_SHARPENED_NOTE_2026-05-10_aclambda.md)
- Kawamoto-Smit upstream: [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- BZ corner forcing upstream: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- C_3-preserved interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Conventions unification: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- BAE rename: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- Context-only spectral-action probe: `KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`
- Context-only Koide Frobenius-equipartition 11-probe campaign synthesis:
  `KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`
- Context-only BAE 30-probe terminal synthesis:
  `KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Command

```bash
python3 scripts/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.py
```

Expected output: structural verification of (1) K1 K-theory equivariant
decomposition + translation-invariance load-bearing identification;
(2) K2 C_3-torsor equivariant-choice enumeration; (3) K3 modular
flavor bridge-count audit; (4) hostile-review tiering of each
ingredient; (5) substep-4 admission count unchanged verification;
(6) forbidden-imports check; (7) source-note hygiene check.

Cached: [`logs/runner-cache/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.txt`](../logs/runner-cache/cl3_koide_s_substep4_aclambda_2026_05_08_probeS_substep4_aclambda.txt)

## User-memory feedback rules respected

- `feedback_derivation_surface_extends_via_new_science.md`: this probe
  uses K-theory, categorical groupoid, and modular flavor as
  imported tools (structural lenses) acting on retained content.
  No new content axioms are added; each tool's identification is
  tiered RETAINED/IMPORTED/POSTULATED per hostile-review pattern.
- `feedback_consistency_vs_derivation_below_w2.md`: this note is
  honest about the convention-dependence trap reappearing across each
  imported tool. Identification of "K-class with species-label" or
  "groupoid choice with generation label" is POSTULATED, not
  derived.
- `feedback_hostile_review_semantics.md`: this narrowing stress-tests
  the action-level semantics of each imported tool — what is
  RETAINED, what is IMPORTED, what is POSTULATED — not just algebra.
  Each tool's identification with framework content is justified
  explicitly.
- `feedback_retained_tier_purity_and_package_wiring.md`: AC_λ.struct
  remains inherited-bounded from Kawamoto-Smit upstream; K-theory does
  not promote it. AC_λ.label remains audit-pending-meta-bounded;
  groupoid does not promote it. No automatic cross-tier promotion.
- `feedback_physics_loop_corollary_churn.md`: the three-tool analysis
  with explicit hostile-review tiering + unified meta-pattern
  observation is substantive new structural content. NOT a relabel of
  PR #890 (which decomposed AC_λ into struct ∧ label) or Probe 4
  (which attacked the Koide Frobenius-equipartition condition).
- `feedback_compute_speed_not_human_timelines.md`: each imported
  tool's failure mode is characterized in terms of WHAT additional
  bridge content would be needed, not how-long-it-takes.
- `feedback_review_loop_source_only_policy.md`: this delivery is the
  source-only triplet (source theorem note + paired runner + cached
  output); no output-packets, lane promotions, or working "Block"
  notes.
- `feedback_primitives_means_derivations.md`: each postulated bridge
  introduced by an imported tool (K1 K-bridge, K2 label bridge, K3
  level+weight+dict) is EXPLICITLY accounted as a POSTULATED
  bridge, not as a new axiom or import dressed as derivation.
- `feedback_special_forces_seven_agent_pattern.md`: the three
  imported tools (K-theory, groupoid, modular flavor) form a
  3-angle parallel attack on the un-attacked AC_λ atom with sharp
  yes/no deliverables per tool.
