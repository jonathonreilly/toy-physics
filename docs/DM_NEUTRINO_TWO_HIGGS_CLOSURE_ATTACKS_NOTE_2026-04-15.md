# DM Neutrino Two-Higgs Closure Attacks

---

**This is an attack-paths inventory / planning record. It does not
establish any retained claim.**
For retained claims on the DM neutrino two-Higgs closure surface, see
the per-claim notes referenced from the `## Audit scope` block below.

---

**Date:** 2026-04-15
**Status:** support / attack-paths inventory record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / attack-paths inventory record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no

## Audit scope (relabel 2026-05-10)

This file is an **attack-paths inventory / planning record** for the
DM neutrino two-Higgs closure derivation surface. It is **not** a
single retained theorem and **must not** be audited as one. The audit
ledger row for `dm_neutrino_two_higgs_closure_attacks_note_2026-04-15`
classified this source as conditional/bounded_theorem with auditor's
repair target:

> register a runner/proof note for the load-bearing step or cite an
> audited retained dependency.

The minimal-scope response in this PR is to **relabel** this document
as an attack-paths inventory rather than to register a runner or
cite an audited retained dependency for the inventoried attack paths
here. Those steps belong in dedicated review-loop or per-attack-path
audit passes. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The Gap A / Gap B sub-targets, Approach A1/A2/A3 + B1/B2/B3
  attack inventories, "strongest execution choice" recommendations,
  and "uniquely minimal" framing language below are **historical
  attack-paths memory only**.
- The retained-status surface for any DM two-Higgs neutrino
  extension, right-Gram bridge, residual-sheet, or CP-admissible
  closure is the audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus
  the per-claim notes, **not** this attack inventory.
- Retained-grade does **NOT** propagate from this attack inventory
  to any approach-path, recommendation, or successor closure.

For any retained claim about DM neutrino two-Higgs closure, audit
the corresponding dedicated note and its runner as a separate scoped
claim — not this attack-paths inventory.

---

## Exact live gaps

After the two-Higgs right-Gram bridge theorem, the DM denominator is no longer
blocked on a vague missing flavor mechanism. The live derivations are:

1. derive or justify the **local two-Higgs neutrino extension** on the
   retained axiom surface
2. derive the **right-sensitive local data / residual sheet** strongly enough
   that the realized `Y^dag Y` lands in the CP-admissible odd-circulant
   subcone

This note records three concrete attack paths for each gap and the strongest
execution choice.

## Gap A: derive / justify the local two-Higgs neutrino extension

### Approach A1: minimal CP-support uniqueness

Combine the single-Higgs monomial no-mixing theorem, the universal-Yukawa
leptogenesis no-go, the odd-circulant CP tool, and the two-Higgs escape theorem
into one DM-side statement:

- one Higgs is exactly too small
- repeated Higgs charges are still effectively one Higgs
- two distinct Higgs charges are the unique minimal exact local escape
- that escape is support-equivalent to the canonical two-Higgs lane

This does not yet derive the extension from the bare axiom alone, but it
upgrades it from "possible" to "uniquely minimal once nonzero DM CP support is
required."

**Strength:** strongest honest theorem available on the current stack.

### Approach A2: weak-CP transfer from the strong-CP lane

Try to port the exact weak-only `Z_3` CP source on the strong-CP branch into a
neutrino-specific local flavor-breaking operator that forces the second Higgs
charge sector.

**Strength:** potentially stronger if it works, but currently speculative.
The strong-CP lane cleanly factorizes weak and color CP, but it does not yet
produce a neutrino two-Higgs selector.

### Approach A3: PMNS selector microscopic transplant

Port the PMNS "sector-odd mixed bridge" logic and its selector-amplitude
boundary into the DM denominator lane, then ask whether the same mixed bridge
forces the neutrino-side two-Higgs branch.

**Strength:** structurally relevant, but currently still an admitted-extension
boundary, not a retained positive selector.

### Chosen execution

**A1.** It is the strongest exact theorem that can actually be landed now.

## Gap B: derive the right-sensitive local data / residual sheet

### Approach B1: continuity to the retained universal Dirac bridge

On the DM circulant subcone, the two-Higgs bridge theorem already forces the
realization onto the symmetric local slice. The remaining ambiguity is then the
swap `x <-> y`.

Use continuity to the retained exact universal bridge `Y = y_0 I` at vanishing
deformation to select the physical sheet:

- one sheet tends to `sqrt(d) I`
- the other tends to a pure cycle-supported monomial class

So the universal bridge anchors the sheet.

**Strength:** strongest DM-specific exact route because it uses a retained DM
datum rather than an admitted PMNS-side scalar.

### Approach B2: one right-Gram modulus

Port the PMNS right-Gram sheet-fixing theorem directly and use one admitted
off-diagonal modulus of `Y^dag Y` to fix the residual sheet generically.

**Strength:** exact and clean, but it still adds an admitted right-sensitive
datum rather than deriving the sheet from the DM chain itself.

### Approach B3: residual-`Z_2` / EWSB alignment reduction

Try to collapse the seven quantities using the aligned Hermitian core and then
infer the right sheet from the reduced `2+1` structure.

**Strength:** useful sharpening when alignment is granted, but the current bank
does not force that alignment.

### Chosen execution

**B1.** It is the strongest exact DM-side route because it converts the sheet
from an admitted PMNS datum into a continuity law anchored by the retained
universal bridge.

## Execution summary

The strongest current work plan is therefore:

1. prove the **DM two-Higgs minimality theorem** on the local neutrino lane
2. prove the **DM two-Higgs continuity sheet theorem** on the circulant
   CP-admissible subcone
3. then reassess the remaining blocker after those two exact reductions land

