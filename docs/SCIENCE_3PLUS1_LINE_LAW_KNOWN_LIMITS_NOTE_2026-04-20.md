# Science 3+1 Line Law: Known Limits Note

**Status:** bounded - bounded or caveated result note
Date: 2026-04-20

**Audit-conditional perimeter (2026-05-01):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
bounded_theorem`, and load-bearing step class `B`. The audit
chain-closure explanation is exact: "The scope caveats are explicit,
but the note has no primary runner or parsed audited dependencies for
the Wilson/Perron branch, retained slice selector, Givens solve,
reduced-packet closure, full-packet no-go, or live-target
reproduction." The audit-stated repair target is exact:
`missing_dependency_edge` — "add explicit audited dependency edges
or a primary runner/proof bundle for each step of the closure chain
and no-go." This rigorization edit only sharpens the boundary of the
conditional perimeter and registers the named upstream theorem notes
explicitly under "Cited authority chain (2026-05-10)" below; nothing
here promotes audit status. This is a meta synthesis note that
records strongest-attainable-closure scope and explicit-limits scope;
it is not a primary-runner result and never claimed to be one. The
bounded scope statement is unaffected.

## Purpose

State the strongest theorem-native closure now supported on the clean science
branch, and state the remaining weaknesses precisely so review can evaluate the
result on its actual scope rather than on an overstated claim.

## What Is Closed Exactly

On the selected minimally-positive Wilson branch:

1. The Wilson/Perron completion branch is fixed canonically by the
   minimal-positive extension theorem on the factorized cone.

2. The retained `3d+1` complement-line problem is solved on a bounded positive
   line chart and reduces to an exact two-point orientation doublet.

3. The `rho1` least-distortion rule selects one canonical retained real `3d`
   slice from that solved doublet.

4. Inside that fixed selected slice, the ordered complex-Givens grammar
   `G12 · G13 · G23` contains exact solutions of the reduced projected-source
   packet equation

       (E1, E2, S12, S13).

5. Among those exact reduced-packet solutions, least Frobenius distortion to
   the identity basis selects one canonical internal dressing.

6. That selected dressing reproduces the observed live DM target exactly.

So the strongest exact closure now proved on this retained ambient is:

> canonical Wilson branch
> -> canonical retained real slice
> -> canonical internal reduced-packet dressing
> -> exact reduced projected-source packet
> -> exact live DM target

## What Is Not Claimed

The branch does **not** claim exact equality with the full sparse-face
`9`-channel projected-source packet on the retained `3d+1` ambient.

That stronger statement is ruled out by a structural no-go: the full sparse-face
target block violates compression interlacing against the selected retained
`4x4` Wilson block. So exact full-packet equality is not just unproved; it is
incompatible with this retained ambient.

## Remaining Weaknesses

### 1. The final two selectors are geometric-canonicity laws

The complement-line selector and the internal complex-Givens selector are both
least-distortion rules on exact solved sets.

This is mathematically clean and target-independent, but it is still a
geometric/canonical choice rule. A hard reviewer may still ask whether these
least-distortion rules are forced by deeper Wilson/Perron dynamics, or whether
they are the strongest canonical geometry presently available.

### 2. The solve theorems are numerical exact-solve theorems

The line solve and the complex-Givens solve are exact audited solution-set
theorems with nondegeneracy checks, but they are not symbolic elimination or
closed-form classification theorems.

So the branch supports:

- exact bounded-domain solve,
- isolated solution set,
- nondegeneracy,
- canonical selector on that solved set,

but not a closed-form symbolic description of the entire solution set.

### 3. Scope is reduced-packet exact closure, not full-packet exact closure

This is now an explicit strength/limit pair:

- strength: exact reduced projected-source packet closure is achieved,
- limit: exact full `9`-channel packet closure is impossible on this retained
  ambient.

Any review should judge the branch on that exact scoped claim.

### 4. The closure remains relative to the selected Wilson factorized carrier

The branch now proves the selected branch is canonical inside the factorized
cone, not across all imaginable upstream Wilson completions. So a deeper
challenge could still target the carrier class itself rather than the closure
chain inside it.

## Recommended Reviewer Posture

The clean branch should be read as proving the following:

1. the old review objections about ad hoc branch choice, hardcoded witness
   lines, and witness-only selector comparison have been repaired;
2. the strongest exact closure attainable on the retained `3d+1` ambient is now
   identified;
3. that strongest attainable closure already closes the selected retained-
   ambient Wilson route to the reduced projected-source packet and live target;
4. any remaining objection must therefore be one of:
   - challenge the least-distortion selector nativity,
   - demand symbolic rather than numerical solved-set classification,
   - challenge the factorized carrier itself,
   - challenge equivalence to the manuscript-facing microscopic selector law on
     `dW_e^H`,
   - or demand exact full-packet closure despite the structural no-go.

## Bottom Line

The branch is no longer vulnerable to the original review-note objections.
What remains are higher-bar objections about physical nativity, symbolic
classification, carrier choice, or equivalence to the manuscript-facing
microscopic selector law, not the original internal-consistency failures.

## Cited authority chain (2026-05-10)

This note is a meta synthesis that summarises strongest-attainable
exact closure on the retained `3+1` ambient. It does not run a
primary runner; each numbered closure step in "What Is Closed
Exactly" is supported by a separately-audited upstream theorem note.
Registered under `audited_conditional` and `unaudited` upstream
audit status as of 2026-05-10:

1. Wilson/Perron canonical branch fix —
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_CLOSURE_ENDPOINT_NOTE_2026-04-20.md)
   (audit_status `unaudited`, claim_type `positive_theorem`).
2. Retained `3d+1` complement-line two-point exact solve —
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_EXACT_SOLVE_DOUBLET_THEOREM_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_EXACT_SOLVE_DOUBLET_THEOREM_NOTE_2026-04-20.md)
   (audit_status `audited_conditional`, claim_type `bounded_theorem`).
3. `rho1` least-distortion canonical retained slice selector —
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_LEAST_DISTORTION_SELECTOR_THEOREM_NOTE_2026-04-20.md)
   (audit_status `audited_conditional`, claim_type `bounded_theorem`)
   together with
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_LINE_RHO1_ORIENTATION_THEOREM_NOTE_2026-04-20.md)
   (audit_status `audited_conditional`, claim_type `bounded_theorem`).
4. Complex-Givens grammar `G12 . G13 . G23` exact reduced-packet
   solve / least-Frobenius internal dressing selector —
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_REDUCED_PACKET_COMPLEX_GIVENS_SELECTOR_THEOREM_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_REDUCED_PACKET_COMPLEX_GIVENS_SELECTOR_THEOREM_NOTE_2026-04-20.md)
   (audit_status `audited_conditional`, claim_type `positive_theorem`).
5. Full sparse-face `9`-channel structural no-go (cited at "What Is
   Not Claimed" above) —
   [`docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_FULL_PACKET_NO_GO_THEOREM_NOTE_2026-04-20.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_3PLUS1_FULL_PACKET_NO_GO_THEOREM_NOTE_2026-04-20.md)
   (audit_status `unaudited`, claim_type `no_go`).

The `audited_conditional` perimeter on each upstream theorem
propagates into this synthesis: the strongest-attainable-closure
statement here is exactly as strong as the conjunction of those
upstream conditional theorems and is not stronger. The
`missing_dependency_edge` repair target named in the audit verdict
is what this Cited authority chain section is intended to address
at the source-note level; the audit ledger's `deps` field for this
row remains under audit-lane control.
