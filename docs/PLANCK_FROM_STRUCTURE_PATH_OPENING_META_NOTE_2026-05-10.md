# Planck-from-Structure Path-Opening Meta Note

**Date:** 2026-05-10
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status is set only after independent audit
review.
**Authority role:** records the synthesis-level state of the
substrate-to-carrier round of 2026-05-10 against the prior 30-probe
campaign synthesis ([`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md))
and the conventions-unification companion ([`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)).
Documents the four source-note proposals from that round (P1, P2, P3, P4)
that target the Planck-from-structure missing-theorem trio plus the
G_Newton self-consistency lane, identifies what each supports or narrows, and
records the conditional path to **zero conventional anchors** under
the framework's existing physical `Cl(3)` on `Z^3` baseline.
**Companion to:** [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md),
[`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md),
[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md).
**Primary runner:** [`scripts/frontier_planck_from_structure_path_opening.py`](../scripts/frontier_planck_from_structure_path_opening.py)
**Cache:** [`logs/runner-cache/frontier_planck_from_structure_path_opening.txt`](../logs/runner-cache/frontier_planck_from_structure_path_opening.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `effective_status` is
generated only after the independent audit lane reviews the claim,
dependency chain, and runner. This note does not promote any source
theorem note, does not retag any existing audit row, does not modify
any theorem, and does not select among the strategic options
that the path-opening exposes. The audit lane has full authority
on the four PR-level source-note proposals listed below and on the
synthesis-level claim of "path-opening" itself.

## Naming

Throughout this note:

- **"physical Cl(3) local algebra"** = the repo baseline local algebra per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"`Z^3` spatial substrate"** = the repo baseline spatial substrate per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).
- **"the missing-theorem trio"** = the three substrate-to-carrier
  derivation gaps named in the prior Planck-lane lane-status work
  (parent-source hidden-character delta, substrate-to-carrier forcing,
  orientation principle).
- **"P1, P2, P3, P4"** = the four substrate-to-carrier round source-note
  proposals (original PR numbers below).
- **"M_Pl as conventional anchor"** = the framework's earlier surface
  in which absolute lattice-spacing identification with Planck length
  was an empirical anchor, not a structural derivation; this is the
  surface that the missing-theorem trio targets.
- **"path-opening"** = the synthesis-level observation that the round's
  four source-note proposals, **conditional on their audit ratification
  and on the substep-4 / G_Newton residuals listed below**, would
  collectively narrow the framework's import surface from "two
  physical `Cl(3)`/`Z^3` baseline + one conventional scale anchor +
  named admissions" toward "the same baseline + named admissions only."

The phrase **"path-opening, not closure"** is load-bearing on this
note: under audit ratification of the four PR-level source notes, the
remaining residuals are explicitly enumerated in the
"What remains conditional" section below.

## Round scope (2026-05-10)

The 2026-05-10 substrate-to-carrier round produced four source-note
proposals, originally staged in separate PRs for independent audit:

| PR | Probe | Subject | Proposed claim type | Review-loop boundary |
|----|-------|---------|---------------------|--------------------|
| [#877](https://github.com/jonathonreilly/cl3-lattice-framework/pull/877) | P1 | Substrate-to-carrier forcing — RP route | `bounded_theorem` | bounded support via cited reflection-positivity OS Cauchy-Schwarz; selects `P_A` uniquely from 17 rank-four projector classes under the "vacuum-reachable degree-1 sector dim = rank" criterion; audit decides final status |
| [#876](https://github.com/jonathonreilly/cl3-lattice-framework/pull/876) | P2 | Hidden-character `δ = 0` via source-free state | `positive_theorem` | source-free state `ρ_cell = I_16/16` collapses every Schur trace to `Tr(O)/16`; audit decides final status |
| [#874](https://github.com/jonathonreilly/cl3-lattice-framework/pull/874) | P3 | Orientation principle — 3+1 single-clock time-asymmetry | `bounded_theorem` | bounded support from action-level `Z_2` grading `Θ_RP = (-1)^{n_t}` and asymmetric eigenspace dimensions; audit decides final status |
| [#875](https://github.com/jonathonreilly/cl3-lattice-framework/pull/875) | P4 | G_Newton self-consistency bounded sharpening | bounded sharpening, **not full closure** | dimensional-rigidity sub-theorem plus three explicitly named admissions: (B(a)) skeleton-selection, (B(b)) Born-as-source, (B(c)) valley-linear weak-field action |

All four source notes adhere to the existing audit-honest rules:

- No new repo-wide axioms; the physical `Cl(3)` local algebra and
  `Z^3` spatial substrate baseline are unchanged.
- No PDG observed values used as derivation input
  (substep-4 AC narrowing rule preserved).
- No promotion of unaudited content to retained grade.
- Each PR ships with a paired runner reaching `=== TOTAL: PASS=N, FAIL=0 ===`.

## What this synthesis records

The round's four source-note proposals, taken together with the prior
round's wins (C-iso `ε_witness` engineering, foundational
clarifications, BAE rename, BAE 30-probe terminal synthesis),
constitute a **path-opening** for the Planck-from-structure target:

1. **The missing-theorem trio is no longer a wholesale gap.** Each of
   the three substrate-to-carrier derivation gaps named in the prior
   Planck-lane lane-status work has at least one source-note proposal
   in flight (P1, P2, P3) with explicit cited-content load-bearing
   inputs and explicit forbidden-input boundaries. Under audit
   ratification, the trio narrows from "missing" to "named bounded /
   positive sub-theorems with identified residuals."

2. **The G_Newton self-consistency lane has explicit residual
   structure.** The P4 source-note proposal does **not** close
   `G_Newton` from retained-grade content; it sharpens what was previously a
   bundled gap into a positive dimensional-rigidity sub-theorem plus
   three named admissions, each with its own structural target.

3. **The path to zero conventional anchors is conditional.** Under
   independent audit ratification of P1+P2+P3 plus closure of the substep-4
   staggered-Dirac realization gate (currently `bounded_theorem` per
   [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)),
   the lattice-spacing-as-Planck-length identification becomes a
   **structural** consequence of the framework's primitive layer rather
   than an empirical anchor. This is conditional, not closed.

4. **Engineering-side wins from the prior round amplify the
   path-opening.** The C-iso `ε_witness` closure (PR #845, 2.6×10⁻⁴ at
   `ξ=4`) and the SU(3) NNLO/NNNLO/N4LO/N5LO closed-form rationals
   (PR #857) eliminate the C-iso truncation as the dominant systematic
   on the gauge-side bridge — the dominant remaining bottleneck is the
   stat+vol floor, not a structural gap.

## The conditional path to zero conventional anchors

Under the framework's existing physical `Cl(3)` on `Z^3` baseline
([`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)), import categories on the
prior surface were:

| Category | Pre-round count | Description |
|---|---|---|
| Framework baseline | 2 named pieces | physical `Cl(3)` local algebra + `Z^3` spatial substrate |
| Open derivation gates | 2 | staggered-Dirac realization gate; `g_bare = 1` derivation gate |
| Conventional scale anchors | 1 | absolute lattice spacing ↔ Planck length identification |
| Named admissions outside the path | 2 | BAE multiplicity-counting; P (radian bridge) — per [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md) |
| Convention bookkeeping | (unbounded) | mass-ordering names, units, particle naming, etc. — per [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |

This round addresses the **conventional scale anchor** row:

- P1+P2+P3 supply the substrate-to-carrier identification chain that
  the absolute scale-anchor identification required (carrier forcing,
  hidden-character closure, orientation principle).
- P4 sharpens the `G_Newton` lane so that the dimensional bridge
  `G ~ ℏc / M_Pl²` carries explicit named admissions rather than a
  bundled "gap."

**Under independent audit ratification of P1+P2+P3** and **conditional on closure
of the substep-4 staggered-Dirac realization gate**, the conventional
scale anchor row reduces toward zero. The framework's import surface
under that conditional path becomes:

| Category | Conditional post-round count | Description |
|---|---|---|
| Framework baseline | 2 named pieces | unchanged physical `Cl(3)` local algebra + `Z^3` spatial substrate |
| Open derivation gates | 2 | unchanged (substep-4 staggered-Dirac, `g_bare = 1`) |
| Conventional scale anchors | 0 (conditional) | conditional on P1+P2+P3 audit ratification + substep-4 closure |
| Named admissions outside the path | 2 (BAE, P) + 3 (G_Newton: skeleton, Born, valley-linear) | three new admissions named explicitly by P4; not promoted; closure paths identified for each |
| Convention bookkeeping | (unbounded) | unchanged — labeling conventions and unit conventions are not physical imports |

The "(conditional)" label is load-bearing. This synthesis does **not**
claim the conventional scale anchor row is at zero; it records that
the round's four source-note proposals sketch a structural path on
which it would reach zero.

## What remains conditional (the residuals, named)

This synthesis enumerates the residuals explicitly. Each residual is
audit-lane authority; this note records them, does not adjudicate.

### Conditional on audit ratification of P1, P2, P3

Each of the four source-note proposals (#874, #875, #876, #877) awaits
independent audit. Until the relevant rows are audit-ratified, the
synthesis-level "path-opening" remains
conditional on the proposals as authored.

### Conditional on substep-4 staggered-Dirac closure (currently `bounded_theorem`)

The substrate-to-carrier closures all rely upstream on the
substep-4 AC narrowing surface
([`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
The narrowing decomposes the substep-4 AC into three atoms
(`AC_λ`, `AC_φ`, `AC_φλ`); the residual `AC_φλ` is the explicit
identification between the framework's three-fold structure and SM
flavor-generation structure. Substep 4 currently has BAE residual per
the 30-probe terminal synthesis (PR #836). Until substep 4 ratchets
from `bounded_theorem` to `positive_theorem`, the substrate-to-carrier
chain inherits its bounded label.

### Conditional on G_Newton's three named admissions closing

PR #875 names three admissions for the `G_Newton` lane:

- **B(a) Skeleton-selection.** Multiple cited propagator skeletons
  exist (Hamiltonian, d'Alembertian, complex-action); no retained-grade
  skeleton-selection theorem is in the audit ledger.
- **B(b) Born-as-source.** Born map is target-side; pure-state and
  density-matrix-trace readings diverge on mixed states; no retained-grade
  Born-as-gravity-source theorem.
- **B(c) Valley-linear weak-field action.** Valley-linear vs
  spent-delay action comparison currently selects valley-linear by
  empirical `F~M=1` match, not by retained-grade derivation.

Each admission has a separate companion-probe path identified in the
G_Newton task framing; those probes' results may not be on main yet at
synthesis time.

### Already-named admissions (unchanged by this round)

Per [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
(PR #836):

- **BAE** — bounded; closure requires multiplicity-counting principle
  outside `C_3` rep theory on `Herm_circ(3)`.
- **P** (radian bridge) — bounded; radian unit not in framework's
  dimensional Buckingham-Pi inventory.

These admissions are outside the substrate-to-carrier path and are
**unaffected** by this round. The synthesis records them only to
preserve the running named-admission inventory.

## Audit-honest framing

This synthesis is explicit about what the round did and did not do.

### What the round did

1. Produced four source-note proposals (PRs #874, #875, #876, #877)
   with paired runners and cached outputs, each claiming a specific
   bounded or positive sub-theorem on cited-content surfaces.
2. Decomposed the previously-bundled "missing-theorem trio" into named
   bounded/positive sub-theorems with explicit cited-content
   load-bearing inputs.
3. Sharpened the `G_Newton` self-consistency lane into a positive
   dimensional-rigidity sub-theorem plus three explicitly named
   admissions.
4. Identified a conditional path on which the conventional scale
   anchor row reaches zero, with the conditionalities enumerated above.

### What the round did NOT do

1. **Close the Planck-from-structure target.** The conditional path
   above has explicit named residuals (substep-4 ratchet, G_Newton's
   three admissions, audit ratification of P1+P2+P3). Closure
   requires those residuals to land.
2. **Promote any source note to retained.** Each PR is awaiting
   independent audit verdict.
3. **Add a new repo-wide axiom.** The physical `Cl(3)` local algebra and
   `Z^3` spatial substrate baseline are unchanged.
4. **Modify any retained theorem or audit row.** Retained-grade content,
   bounded labels, and `effective_status` rows are unchanged.
5. **Reclassify named admission counts.** BAE and P are still bounded
   admissions per PR #836; this synthesis adds three explicit
   `G_Newton` admissions named by PR #875 (B(a), B(b), B(c)) but
   does not aggregate them into a single composite count.
6. **Select among strategic options.** The path-opening exposes
   strategic decisions (how to attack substep-4 ratchet, which of
   B(a)/B(b)/B(c) to attack first); the audit lane has authority on
   path selection.
7. **Replace the substep-4 AC narrowing rule.** PDG values remain
   not load-bearing as derivation input.
8. **Drop the "BAE outside C_3 rep theory" structural claim** of
   PR #836. That claim is unchanged by this round; the path-opening
   is on the Planck-from-structure track, not the BAE track.

## Strategic implications (synthesis-level observation, not selection)

The path-opening exposes three strategic options. The synthesis does
**not** select among them; the audit lane has authority.

1. **Attack the substep-4 ratchet next.** Substep 4 is the load-bearing
   ratchet: ratcheting it from `bounded_theorem` to `positive_theorem`
   simultaneously promotes all bounded substrate-to-carrier
   conclusions and frees the conventional scale anchor row.
2. **Attack G_Newton's three admissions in parallel.** The B(a) /
   B(b) / B(c) admissions are independent. Parallel companion probes
   can be dispatched without serial dependence.
3. **Continue engineering-side hardening.** The C-iso `ε_witness`
   ladder (PRs #845, #857) is currently bottlenecked by stat+vol; the
   non-bridging engineering frontier remains tightening that floor
   (more seeds, larger lattices) while the structural path-opening
   matures.

The audit lane has authority on which strategic option(s) to pursue
and on whether the path-opening is admissible as a synthesis-level
record at all.

## Cross-references (foundational + this round)

### Foundational

- Minimal axiom surface: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Physical-lattice narrowed no-go: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- Physical-lattice foundational interpretation: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- 30-probe BAE terminal synthesis (PR #836): [`KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md`](KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md)
- Conventions unification companion (PR #729): [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)

### This round's source-note proposals (open PRs)

- **P1** Substrate-to-carrier forcing — RP route: [PR #877](https://github.com/jonathonreilly/cl3-lattice-framework/pull/877)
- **P2** Hidden-character `δ = 0`: [PR #876](https://github.com/jonathonreilly/cl3-lattice-framework/pull/876)
- **P3** Orientation principle: [PR #874](https://github.com/jonathonreilly/cl3-lattice-framework/pull/874)
- **P4** G_Newton self-consistency bounded sharpening: [PR #875](https://github.com/jonathonreilly/cl3-lattice-framework/pull/875)

### Prior-round wins combined into the path-opening

- **C-iso `ε_witness`** closure (PR #845, 2.6×10⁻⁴ at `ξ=4`)
- **SU(3) NNLO/N5LO closed-form rationals** (PR #857)
- **BAE rename** to Brannen Amplitude Equipartition (PR #790,
  [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md))

## Validation

```bash
python3 scripts/frontier_planck_from_structure_path_opening.py
```

The runner is a review-hygiene check, not a physics proof. It verifies:

1. The note is classified as `meta` and does not declare pipeline status.
2. Each of the four open-PR cross-references (#874, #875, #876, #877)
   is present.
3. Each prior-round win cross-reference (#845, #857, #790, #836, #729,
   #725) is present.
4. The "path-opening, not closure" framing is stated explicitly.
5. The conditionalities are enumerated explicitly (audit ratification
   of P1+P2+P3; substep-4 ratchet; G_Newton's three admissions).
6. The framework's physical `Cl(3)`/`Z^3` baseline is unchanged.
7. No PDG values are loaded as derivation input.
8. No new repo-wide axiom is added.
9. No theorem promotion or admission reclassification.
10. The G_Newton three named admissions (B(a), B(b), B(c)) are recorded.
11. The strategic options are listed without selection.

## Review-loop rule

Going forward:

1. The synthesis-level "path-opening" framing remains in force only
   while the four source-note proposals (#874, #875, #876, #877) remain
   candidate surfaces; if any of P1+P2+P3 is rejected by audit, the
   synthesis-level path-opening claim must be re-stated as the surviving
   subset.
2. Substep-4 ratchet attempts on the staggered-Dirac realization gate
   should explicitly cite this synthesis as the downstream consumer of
   their ratchet.
3. New `G_Newton`-lane work should map onto the three named admissions
   (B(a), B(b), B(c)) rather than re-bundle the gap.
4. The conditional path to zero conventional anchors is **never** to
   be claimed as closed in any downstream branch absent independent
   audit ratification of P1+P2+P3 and substep-4 closure.

## What this note is NOT

- Not a route-history document.
- Not a replacement for the publication matrix.
- Not a claim that Planck-from-structure is closed.
- Not a unilateral retagging of the four open PRs.
- Not an aggregation of named admission counts into a single number.
