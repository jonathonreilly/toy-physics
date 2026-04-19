# Quark Projector-Parameter Audit

**Date:** 2026-04-19
**Status:** bounded parameter audit on the reduced projector-ray closure
**Primary runner:** `scripts/frontier_quark_projector_parameter_audit.py`

## Safe statement

The quark branch already has a strong bounded closure on a fixed projector ray:

- one exact projector direction,
- two real sector amplitudes,
- one shared phase,
- and the full quark package closes numerically.

This note asks a narrower question:

> which of those reduced parameters are already supported by exact quantities
> on the current projector/tensor surface?

The answer is sharper than before.

This note audits the exact-support anchor itself. It does **not** try to
exhaust the remaining exact-candidate laws for `a_u`; that wider shortlist is
now tracked separately in
[QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md).

## What is exact-support compatible now

Three pieces of the reduced closure already line up with exact quantities that
exist on the current atlas surface:

1. **Projector ray.**
   The carrier direction
   `sqrt(1/6) + i sqrt(5/6)` is the exact `1⊕5` CKM projector branch.
2. **Down-sector reduced amplitude.**
   The reduced down amplitude is compatible with the exact scalar comparison
   constant
   `rho_scalar = 1/sqrt(42)`.
3. **Small support-angle probe.**
   Interpreting the exact support datum `delta_A1(q_dem) = 1/42` as a small
   angle, `phi = -1/42 rad`, still keeps the reduced closure near-full.

With those two exact-support inputs fixed,

```text
a_d = 1/sqrt(42)
phi = -1/42 rad
```

and solving only for `(m_u/m_c, m_c/m_t, a_u)`, the branch lands at

- `m_u/m_c = 1.681720 x 10^-3`
- `m_c/m_t = 7.365631 x 10^-3`
- `a_u = 0.778262`
- `|V_us| = 0.227270181`
- `|V_cb| = 0.042171993`
- `|V_ub| = 0.003909719`
- `J = 3.305502 x 10^-5`

with `arg det(M_u M_d) = 0 mod 2pi`.

So the exact-support anchoring is already strong enough to keep the whole
package within about `1%` to `2%`.

## What still does not derive

The remaining non-derived object is now sharply isolated:

- one scalar up-sector reduced amplitude law.

The current support/projector surface does **not** yet provide an exact law
for that amplitude. In this limited baseline audit, obvious exact candidates such as

- `pi/4`,
- `sqrt(2/3)`,
- `5/6`,
- `sqrt(5)/6`,
- `sqrt(6/7)`,

does not reproduce the solved `a_u` at the same quality. The best audited
exact candidate is `pi/4`, but it still misses the stronger reduced closure at
the aggregate sub-percent level. So the current branch does **not** yet have a
full exact reduced-parameter derivation.

A later widened scan now shows that there is already a short exact-candidate
shortlist beyond this baseline set. That shortens the bounded search space,
but it does not change the derivation status: `a_u` is still not retained.

## Interpretation

This is a real improvement over the earlier quark-CP closure language.

The remaining gap is no longer:

- “some missing CP primitive,” or
- “some free complex 1-3 carrier family.”

It is now:

- **one missing scalar amplitude law for the up sector** on the exact
  projector/support surface.

That is the cleanest current no-go statement.

## Relation to the earlier notes

- [QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md](./QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
  remains the strongest reduced bounded closure statement.
- [QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md](./QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
  remains the broader bounded existence proof with freer complex carriers.
- This audit note is the sharper structural statement about what is already
  exact-support compatible and what remains non-derived.

## Validation

Run:

```bash
python3 scripts/frontier_quark_projector_parameter_audit.py
```

Current expected result on this branch:

- `frontier_quark_projector_parameter_audit.py`: `PASS=6 FAIL=0`
