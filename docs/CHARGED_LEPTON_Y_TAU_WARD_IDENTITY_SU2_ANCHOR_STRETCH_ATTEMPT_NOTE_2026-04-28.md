# `y_τ` Ward Identity from `SU(2)` Anchor — Stretch Attempt (SA-A)

**Type:** open_gate

**Date:** 2026-04-28
**Status:** open_gate — branch-local **stretch-attempt** note on
`frontier/charged-lepton-pickup-20260428`. Cycle 2 of the charged-
lepton loop: attempts SA-A `y_τ` Ward identity construction anchored
on `SU(2)` weak coupling `g_2`, as direct analog of the retained YT-
lane identity `y_t / g_s = 1/sqrt(6)`. **Result: direct SU(2)
analog FAILS** — the YT-lane derivation chain rests on the **color**
Fierz identity D12 (sqrt(2 N_c) factor), which does not extend to
the colorless lepton sector. Identifies the structural mismatch and
names two alternative anchor candidates (SA-B hypercharge,
SA-C Koide-structural).
**Lane:** 6 — Charged-lepton mass retention (Phase-1 6B target)
**Loop:** `charged-lepton-pickup-20260428`

**Audit-conditional perimeter (2026-05-09):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
open_gate`. The audit chain-closure explanation is exact: "The note
depends on the YT-lane D12/D17 structure and on a non-extension claim
for the (2,1) lepton block, but no cited authority or runner is
provided in the restricted packet to establish either step. The
missing step is a retained theorem or computation showing that the
SU(2)-only lepton block lacks the required Fierz/composite-scalar
uniqueness analog." The audit-stated repair target
(`notes_for_re_audit_if_any`) is exact: "missing_dependency_edge: add
the YT Ward theorem as a one-hop dependency and provide or cite a
retained bounded no-go for the SU(2)-only (2,1) lepton-block analog."
This note is a stretch-attempt artifact: it does **not close** the
SA-A `g_2`-anchor route; it records a worked failed substitution and
names the load-bearing structural mismatch (color Fierz factor
`sqrt(2 N_c) = sqrt(6)` does not extend to colorless lepton sector).
The audit-conditional perimeter is therefore the absence of a
standalone retained no-go theorem for the SU(2)-only (2,1) lepton-
block analog: the structural argument here is internal to the note
and cited authorities, not an audited dependency. Nothing in this
edit promotes audit status; the note remains an honest stretch-
attempt record per Deep Work Rules' no-churn exception. See "Citation
chain and audit-stated repair path (2026-05-10)" below.

---

## 0. First-principles reset (per Deep Work Rules)

### 0.1 `A_min` + Phase-1 retained content

`MINIMAL_AXIOMS_2026-04-11.md` axioms 1-4, plus retained:
- `v = 246.282818290129 GeV` (electroweak hierarchy)
- YT-lane identity `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6)` per
  `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- Recent retained gauge-anomaly cluster (SM_*_PROOF_2026-04-26)
- `Cl(3)` bivector → `SU(2)` native gauge structure
- Three-generation matter structure (anomaly-forced + hw=1)

### 0.2 Forbidden imports

- no PDG charged-lepton masses as derivation input
- no Koide observed Q value as derivation input (Q comparator only)
- no fitted Yukawa / coupling constants

### 0.3 Goal

Construct an exact algebraic Ward identity for the τ-Yukawa on the
charged-lepton carrier:

```text
y_τ_bare = g_? × const                                        (T-tau)
```

where `g_?` is some retained gauge coupling and `const` is a
structural constant (analog of YT-lane's `1/sqrt(2 N_c)`).

Primary anchor candidate: `g_2` (SU(2) weak coupling).

## 1. The YT-lane derivation chain in detail

Per `YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (T1):

```text
y_t_bare = g_bare / sqrt(2 N_c) = g_bare / sqrt(6)              (YT-T1)
```

The derivation rests on:

- **D12** SU(N_c) color Fierz identity (Block 4)
- **D17** composite-Higgs scalar uniqueness on the `Q_L = (2, 3)`
  block (Block 5)
- **S2** Lorentz Clifford Fierz identity (Block 8)
- **D16** tree-level Feynman diagram completeness
- **D15** `n_link = 1` per single vertex (tadpole `u_0` cancels in
  the ratio)

The factor `sqrt(2 N_c) = sqrt(6)` enters specifically via **D12**
(SU(N_c) color Fierz). The trace structure of color-matrix Fierz
contraction in SU(3) representation theory yields this exact
factor.

## 2. Attempt at SU(2) analog

**Naive analog:** for the lepton doublet `L_L = (2, 1)` (SU(2)
doublet, SU(3) singlet), substitute SU(2) for SU(3) in the YT
chain. The color-Fierz block (D12, factor sqrt(2 N_c)) becomes the
SU(2)-Fierz block with `N_w = 2`. Naive substitution:

```text
y_τ_bare ?= g_2_bare / sqrt(2 N_w) = g_2_bare / 2              (Naive)
```

If this naive substitution worked, `y_τ / g_2 = 1/2` would be the
analog identity, and combined with retained `g_2` and Koide ratios,
`m_τ` retains.

## 3. Why the naive substitution FAILS

The YT-lane derivation chain D1-D17 is **specifically about the
top-quark sector**. The Ward identity arises from a 1PI Green's
function `Γ⁽⁴⁾(q²)` on the scalar-singlet channel of the
**`Q_L = (2, 3)` block**. The (2, 3) is critical: SU(2) × SU(3)
representation pair. The composite-Higgs scalar uniqueness (D17) is
**verified for the (2, 3) block specifically** (Block 5), not for
arbitrary blocks.

For the lepton sector `L_L = (2, 1)`:

- The SU(2) doublet structure is shared with `Q_L`.
- **The SU(3) triplet structure is NOT shared.** `L_L` is color-
  singlet.
- The composite-Higgs scalar uniqueness D17 was verified for the
  (2, 3) block via specific color-trace structure. The **(2, 1)
  block has no such color-trace structure** to verify against.
- The Fierz identity D12 used in the YT chain is specifically the
  **color** Fierz with sqrt(2 N_c) factor. There is no SU(2) Fierz
  identity that would give sqrt(2 N_w) in the same role on the
  (2, 1) block.

So the YT chain does not extend to the lepton sector by simple
SU(2) substitution. **The naive analog fails.**

### 3.1 What specifically fails

The structural mismatch is:

- YT chain Block 4 (D12 SU(N_c) color Fierz): exists for (2, 3)
  block; **does not have a SU(2)-only analog on the (2, 1) block**.
- YT chain Block 5 (D17 composite-Higgs scalar uniqueness): verified
  for (2, 3) block; the (2, 1) block has different scalar-channel
  structure.
- YT chain Block 8 (S2 Lorentz Clifford Fierz): same for both
  sectors (Lorentz structure); does not anchor the gauge factor.

The factor `1/sqrt(6)` in YT-T1 comes specifically from the SU(3)
Fierz trace, not from SU(2) structure. **There is no g_2-anchor
analog of YT-T1 on the (2, 1) block.**

## 4. Two alternative anchor candidates

Since the direct g_2 anchor fails, two alternatives:

### SA-B — Hypercharge `g_1` anchor

The lepton doublet `L_L` has hypercharge `Y = -1/2`; `τ_R` has
`Y = -1`. A Yukawa-Ward identity anchored on `g_1` would use the
hypercharge representation structure.

**Why it might work:** unlike the SU(2) analog above, hypercharge
representation theory is U(1) — no Fierz identity in the SU(N) sense,
but the multiplicative hypercharge couples directly to the Yukawa
vertex through the Higgs scalar's hypercharge `Y_H = +1/2`.

**Why it might not:** U(1) representation theory doesn't deliver
a sqrt(2 N) factor analog. It would deliver simple linear
relations like `y_τ / g_1 = Y_τR / sqrt(?)`. Whether such an
identity is structural (analogous to retained YT) or fitted is the
open question.

**Status:** unattempted on current framework surface; would be the SA-B
stretch attempt for a future cycle.

### SA-C — Koide-structural anchor

The Koide flagship lane is in flight on Q=2/3 and δ=2/9 closures.
If those land, the lepton mass-square-root vector
`v = (sqrt(m_e), sqrt(m_μ), sqrt(m_τ))` has a structurally fixed
direction in R³ via Q. A `y_τ` Ward identity could in principle be
anchored on the Koide combinatorial structure rather than on a
gauge coupling.

**Why it might work:** the Koide structure is internal to the
lepton sector; doesn't need to import an external gauge-coupling
anchor. It uses the three-generation structure directly.

**Why it might not:** Q=2/3 fixes ratios (direction of `v`),
not absolute scale. Anchoring `y_τ` on Q alone gives ratios; an
absolute-scale identity needs to break the rotational symmetry
that Q preserves.

**Status:** depends on Koide flagship lane closing first; then
SA-C becomes attemptable.

### Combined SU(2)×U(1) doublet anchor (SA-D from route portfolio)

A combined gauge-doublet structural anchor uses both `g_2` and
`g_1` simultaneously. Would replicate the YT-lane's combination
of SU(N_c) color + SU(2) electroweak structure but with SU(2) +
U(1) for the colorless lepton.

**Status:** open / plausible single-cycle stretch target after SA-B
failure analysis.

## 5. Synthesis

Cycle 2's SA-A `g_2`-anchor attempt **fails**: the YT-lane
derivation chain rests on color Fierz structure (sqrt(2 N_c)) that
does not exist for the colorless lepton sector.

The Ward identity for `y_τ` cannot be a direct YT analog. It must
either:

- **(SA-B)** anchor on hypercharge `g_1` with U(1) representation
  structure (no Fierz; simpler multiplicative relation).
- **(SA-C)** anchor on Koide combinatorial structure (depends on
  Koide flagship closure first).
- **(SA-D)** combined SU(2)×U(1) anchor.
- Or a **completely different derivation chain** specific to the
  charged-lepton sector, not based on the YT-lane chain template.

The cleanest single-cycle next attempt is **SA-B** (hypercharge
anchor) — it doesn't require Koide flagship closure first, and
gives a focused testable structural identity hypothesis.

## 6. Implications for the Lane 6 closure pathway

After Cycle 2:

- The "direct YT-lane analog" route to `y_τ` is **excluded**.
  Charged-leptons are color-singlet; the color-Fierz factor
  `sqrt(2 N_c) = sqrt(6)` has no analog. SA-A is dead as a route.
- The remaining `y_τ` routes (SA-B, SA-C, SA-D) all require either
  different gauge-anchor structure or Koide flagship closure first.
- Lane 6 Phase-1 `y_τ` Ward identity remains open. The cleanest
  candidate route is now **SA-B hypercharge anchor**.

This is honest progress: the cycle excluded one route definitively
and clarified the remaining attack frames. Per Deep Work Rules
no-churn exception, this is valid stretch output.

## 7. Falsifiers

The cycle's findings are falsified by:

- a worked SU(2)-Fierz-analog identity on the (2, 1) block that
  reproduces the YT-T1 structure with `sqrt(2 N_w) = 2`. The
  D17 composite-Higgs-scalar-uniqueness verification on the (2, 1)
  block would be the load-bearing missing piece.
- a YT-chain-style derivation showing `(2, 1)` and `(2, 3)` blocks
  share the relevant structural primitives.
- empirical 0νββ (irrelevant for charged-lepton identity but
  relevant globally).

## 8. What this cycle closes and does not close

**Closes:**

- SA-A as a direct YT-analog route via `g_2` anchor on the
  colorless lepton sector.
- Identification of the **color Fierz factor sqrt(2 N_c)** as the
  load-bearing element of YT that doesn't extend to leptons.
- Recommendation that SA-B (hypercharge anchor) is the cleanest
  remaining single-cycle attack frame.

**Does not close:**

- 6B `y_τ` Ward identity itself.
- SA-B, SA-C, SA-D — all remain hypothetical routes.
- Lane 6 closure.

## 9. Cross-references

- Cycle 1 theorem plan:
  `docs/CHARGED_LEPTON_LANE6_THEOREM_PLAN_NOTE_2026-04-28.md`.
- YT-lane analog template:
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`.
- Closed direct-Ward-free Yukawa route:
  `docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
  (this Cycle 2 finding is consistent with that no-go: the direct
  free-Ward route is closed; the gauge-anchored SA-A route is also
  excluded because the gauge structure doesn't extend).
- Koide flagship lane (SA-C dependency):
  `docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`.
- Loop pack:
  `.claude/science/physics-loops/charged-lepton-pickup-20260428/`.

## 10. Boundary

This is a stretch-attempt artifact under Deep Work Rules. It
**produces** an honest finding that SA-A is excluded, with sharp
identification of the load-bearing structural mismatch (color Fierz
factor sqrt(2 N_c)). Recommends SA-B (hypercharge anchor) for the
next single-cycle stretch attempt. **It does not close 6B `y_τ`.**

A runner is not authored.

## 11. Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-05-09, see top of note) names two missing
dependency edges. The cited authority chain on this row currently
stands as follows.

| Cited authority | Note | Effective status (2026-05-10) | Conditional on |
|---|---|---|---|
| YT-lane Ward identity (D12 color Fierz, D17 composite-Higgs scalar uniqueness) | [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) | `unaudited` (claim_type `bounded_theorem`) | one-hop dependency edge requested by audit |
| Charged-lepton direct Ward-free Yukawa no-go | [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) | `audited_conditional` (no_go) | parallel no-go on direct-Ward-free Yukawa route |
| `Cl(3)` + `Z^3` + staggered-Dirac axiom set | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | live retained axiom-set anchor |
| SU(2)-only (2,1) lepton-block non-extension claim | inline §3, this note | not yet packaged as standalone retained no-go | audit-flagged second one-hop dependency |

The audit-stated repair path (verbatim from
`audit_ledger.json/notes_for_re_audit_if_any`) is to **add the YT
Ward theorem as a one-hop dependency** and **provide or cite a
retained bounded no-go for the SU(2)-only (2,1) lepton-block
analog**. The first edit can be done in this note's citation block
above; the second requires either packaging §3.1's structural-
mismatch argument as a standalone retained no-go note (separate work,
audit-track), or extending the existing direct Ward-free Yukawa no-go
(`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`)
to cover the SU(2)-anchor variant. Until either path lands, this row
remains `audited_conditional` and this note remains a stretch-attempt
record, not a closure of the SA-A route at audit-grade. The
acknowledged residual is the absence of an audited (2,1)-block
non-extension theorem; §3-§4 of this note exhibit the structural
argument informally but do not close that gap.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit status
and does not modify any `docs/audit/data/*.json` file.
