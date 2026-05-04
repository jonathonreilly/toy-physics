# Equivalence Principle — Bounded Scaffold Lane

**Date:** 2026-04-05 (downgraded 2026-04-27 per review/audit handoff)
**Status:** bounded scaffold lane — uniform-field beam deflection gives near-unity exponents. This is **not** a derivation of `m_inertial = m_gravitational`.
**Primary runner:** [`scripts/equivalence_principle_test.py`](../scripts/equivalence_principle_test.py) (beam-level uniform-field test on lattice)

## What this note actually contains

A beam-level uniform-field test on the lattice was reported with the
following measured exponents:

- `F ~ g^{1.008}` (force vs. field strength)
- `F ~ M^{0.998}` (force vs. source strength)
- `deflection ~ layer^{1.14}` (sub-quadratic, not constant acceleration)

Earlier versions of this note packaged the two near-unity exponents as
"`m_inertial = m_gravitational` to 0.8%". The review/audit handoff (see
[docs/audit/worker_lanes/03_equivalence_principle.md](audit/worker_lanes/03_equivalence_principle.md))
found that this packaging does not close on its own terms:

- linearity of beam deflection in field strength and in source strength
  does not by itself establish equality of inertial and gravitational
  mass;
- the note reports non-constant-acceleration layer scaling
  (`layer^{1.14}`), which is inconsistent with a clean Newton-second-
  law identification of inertial mass from `F = m_i a`;
- no registered runner, force observable definition, mass extraction
  theorem, fit data, fit ranges, uncertainty model, or shared action
  coupling derivation accompanies the claim.

Per the audit verdict, the safe statement is the bounded one.

## Safe bounded reading

- A uniform-field deflection sweep on the lattice produces force
  responses that scale **near-linearly** with both the field strength
  and the source strength, with measured exponents close to 1
  (1.008 and 0.998 respectively).
- The deflection scales sub-quadratically with layer depth
  (`layer^{1.14}`), inconsistent with a constant-acceleration
  trajectory; wave-optical / propagator effects modify the trajectory.
- The action coupling `S = L · (1 − f)` is conjectured as the shared
  source of both responses but is **not derived** from the lattice
  action on the current package surface.

## What this note does NOT claim

- Equality of inertial and gravitational mass on the discrete surface.
- A retained equivalence principle.
- That the near-unity exponents constitute a 0.8% precision test of
  the equivalence principle.
- A mass-from-force operational definition on the lattice.
- A first-principles relation between the field-strength response
  coefficient and the source-strength response coefficient.

## What would close this lane (Path A future work)

A future worker pursuing the strong-claim reinstatement (Path A in the
audit-lane handoff) would need to land all of the following:

1. A registered primary runner that generates the field/mass parameter
   sweep, emits `g` and `M` fit tables with explicit uncertainties,
   and verifies independence from beam/packet parameters.
2. An operational definition of the **force observable** on the
   lattice — what `F` actually measures in the runner's units.
3. An **inertial-mass extraction theorem** — what step identifies the
   coefficient of the field-strength response with the inertial mass
   `m_i` of the test particle.
4. A **gravitational-mass source-normalization theorem** — same for
   the source-strength coefficient and `m_g`.
5. A derivation of the **action coupling** `S = L · (1 − f)` from
   the retained lattice-action stack, showing why this single coupling
   produces both responses with equal coefficients.
6. An accounting of the layer-scaling exponent `1.14` (sub-quadratic,
   wave-optical) within the same derivation, so the chain remains
   self-consistent.

Without all six, the strongest defensible reading remains the bounded
one above.

## Downstream consumers

`equivalence_principle_note` previously appeared upstream of ~119
claims in the citation graph as a `proposed_retained` authority.
Downstream notes that rely on the equivalence principle as a derived
result should either:

- re-cite this note explicitly as a **bounded scaffold** (not a
  retained derivation), or
- supply an independent derivation of `m_inertial = m_gravitational`
  on their own surface and remove the citation to this note.

The audit-lane pipeline will surface the inheritance demotion
automatically once this note re-audits.

## Cross-references

- Audit-lane handoff:
  [docs/audit/worker_lanes/03_equivalence_principle.md](audit/worker_lanes/03_equivalence_principle.md).
- The action-coupling conjecture `S = L · (1 − f)` is a candidate
  derivation target, not a current authority. If a future worker
  derives it from the retained stack, this note can be re-promoted.
