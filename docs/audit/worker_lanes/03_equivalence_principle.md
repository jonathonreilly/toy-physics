# Lane 3: Equivalence principle chain repair

**Status:** OPEN — accepting workers.
**Source claim:** [`equivalence_principle_note`](../../../docs/EQUIVALENCE_PRINCIPLE_NOTE.md)
**Audit verdict:** `audited_failed`
**Criticality:** `high` · **Transitive descendants:** 119 · **Load-bearing class:** G (numerical match at tuned input)

The most foundational claim flagged by the audit. Currently the chain
**does not close on its own terms** — this is a hard failure, not a
conditional.

## Audit finding (verbatim from the ledger)

**Load-bearing step under audit:**

> Uniform field f = g·z gives F ~ g^1.008 and F ~ M^0.998, so the note
> concludes m_inertial = m_gravitational to 0.8%.

**Why the chain does not close:**

The source note provides only headline numerical exponents and no
registered runner, command, log, data table, fit ranges, uncertainty
model, or one-hop derivation of the mass / readout identifications.
The asserted equality of inertial and gravitational mass therefore
cannot be audited from the allowed packet.

**Specific failure:** linearity of a beam deflection with respect to
field strength and source strength does not by itself establish
`m_inertial = m_gravitational`, especially when the note also reports
non-constant-acceleration layer scaling. The 0.8% equality is **not
reproducible** without the supporting infrastructure.

**Unregistered dependencies / missing components:**

- Primary equivalence-principle runner
- Uniform-field force observable definition
- Inertial mass extraction theorem
- Gravitational mass source normalization theorem
- Fit data ranges, uncertainties, logs
- Valley-linear action coupling `S = L · (1−f)` (the shared source of
  both responses, currently unregistered)

## Repair target

A registered primary runner that:

1. Generates the field/mass parameter sweep.
2. Emits the `g` and `M` fit tables with explicit uncertainties.
3. Defines the force/mass observables operationally.
4. Checks independence from packet/beam parameters.
5. Either proves or registers `S = L · (1−f)` as the shared source of
   both responses (this is the load-bearing physical link between the
   two coefficients that the current note skips).

A retained derivation note that either:

- Derives `m_inertial = m_gravitational` from the action coupling and
  the registered observable definitions, OR
- Honestly downgrades the claim to a bounded numerical observation of
  near-unity exponents, scoped to the specific lattice surface.

## Why this is high-leverage

The equivalence principle sits upstream of the gravity / GR program,
weak-field gravity matching, the "exact discrete 3+1 GR" claim, and
several cosmology rows. 119 transitive descendants. This is also one
of the few `audited_failed` claims at high criticality — most failures
are leaf-level. A foundational physics claim failing the audit is the
most consequential signal in the lane.

## Claim boundary while this lane is open

Per the audit verdict:

- It **is** safe to say the note reports a beam-level uniform-field
  proportionality test with exponents near one.
- It is **not** safe to claim a retained equivalence principle or
  equality of inertial and gravitational mass.

This boundary should be reflected in any publication-facing surface
that currently cites the note as authority for the equivalence principle.

## Suggested approach (worker-side)

This is genuine science work, not hygiene. Two viable paths:

### Path A: closure via action coupling

If `S = L · (1−f)` is the right shared source, derive it from the
lattice action surface, register the derivation, then show that both
inertial response (force-vs-mass slope) and gravitational response
(force-vs-source slope) follow from the same coupling. The 0.8%
agreement then becomes a real test of a derived identity.

### Path B: honest downgrade

If the action coupling cannot be derived in this form, downgrade the
note's `Status:` from `proposed_retained` to `support` or `bounded`,
with the claim boundary narrowed to "near-unity exponents on the
lattice." This is a perfectly respectable scientific outcome — the
audit lane is supposed to surface exactly this kind of distinction.

Either path closes the audit. Path A leaves a strong claim; Path B
removes a weak one. Both are wins.

## Success criteria

- Path A: `equivalence_principle_note` audits as `audited_clean`
  after the action coupling is registered and the runner emits the
  fit data with uncertainties. Cross-confirmation required (high
  criticality, but below the critical threshold).
- Path B: `equivalence_principle_note` is rewritten with
  `current_status: support` or `bounded` and a narrowed claim
  boundary; re-audit returns `audited_clean` against the narrower
  claim or accepts the support tier without ratification.

## Branch / worker conventions

- Path A proposal: `claude/equivalence-principle-action-coupling-2026-04-27`.
- Path B proposal: `claude/equivalence-principle-downgrade-2026-04-27`.
- The worker should pick one, not both.

## What this lane is NOT

- Not a request to fight the auditor. The verdict is well-formed; the
  load-bearing step really is a numerical-match-at-tuned-input.
- Not a request to derive general relativity. The lane targets the
  one identity `m_inertial = m_gravitational` on the discrete surface
  the framework actually uses.
- Not a request to expand the equivalence-principle claim surface.
  Either path narrows the surface; neither expands it.
