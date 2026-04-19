# Quark Up-Amplitude Exact-Candidate Scan

**Date:** 2026-04-19
**Status:** bounded exact-candidate shortlist on the reduced quark closure
surface
**Primary runner:** `scripts/frontier_quark_up_amplitude_candidate_scan.py`

## Safe statement

The reduced quark closure branch still does **not** derive the remaining
up-sector amplitude `a_u`.

But after fixing the exact pieces already isolated by the earlier audit,

- projector ray `sqrt(1/6) + i sqrt(5/6)`,
- down amplitude `a_d = 1/sqrt(42)`,
- support-angle probe `phi = -1/42 rad`,

the remaining gap is now much smaller than “one free scalar with no structure”.

This scan shows that the current branch already supports a short exact-candidate
shortlist for `a_u`.

That is a bounded sharpening, not a retained derivation.

## Anchor surface

Use the exact-support anchor from
[QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md):

```text
a_d = 1/sqrt(42)
phi = -1/42 rad
```

with the solved support-anchored reference value

```text
a_u = 0.778161628656
```

This scan evaluates exact candidates in two ways:

1. **Anchored observable package.**
   Keep the anchored mass ratios fixed and score only
   `|V_us|, |V_cb|, |V_ub|, J`.
2. **Two-ratio refit.**
   Fix the exact candidate `a_u`, keep `a_d` and `phi` exact, and re-solve
   only `(m_u/m_c, m_c/m_t)`.

## Main results

### Best small-rational candidate

The strongest small-rational candidate on the two-ratio refit is

```text
a_u = 7/9 = 0.777777777778
```

It lands at

- `m_u/m_c = 1.681365 x 10^-3`
- `m_c/m_t = 7.365674 x 10^-3`
- `|V_us| = 0.227270206`
- `|V_cb| = 0.042171507`
- `|V_ub| = 0.003910288`
- `J = 3.306110 x 10^-5`

with every listed deviation below `1%` and
`arg det(M_u M_d) = 0 mod 2pi`.

So the remaining scalar already has a very tight simple rational candidate.

### Best small-radical candidate

The strongest small-radical candidate on the anchored observable package is

```text
a_u = sqrt(3/5) = 0.774596669241
```

On the exact-support anchor it gives aggregate CKM+`J` absolute deviation
`0.720%`, with component deviations

- `|V_us|`: `-0.029%`
- `|V_cb|`: `-0.003%`
- `|V_ub|`: `+0.010%`
- `J`: `-0.677%`

After the two-ratio refit it still keeps the full package close:

- `m_u/m_c`: `-1.047%`
- `m_c/m_t`: `-0.146%`
- `|V_us|`: `-0.000%`
- `|V_cb|`: `-0.005%`
- `|V_ub|`: `-0.011%`
- `J`: `-0.632%`

So the best small-radical candidate is already in the same quality band as the
solved support anchor.

### Strong projector/support-native dressings

The widened scan also finds exact candidates built directly from the current
projector/support primitives. The strongest current examples are

- `sqrt(5/6) * (1 - 1/sqrt(42))`
- `sqrt(6/7) - 1/sqrt(42)`
- `atan(sqrt(5)) - sqrt(5)/6`

Numerically, these all stay near the anchored closure surface.

The best anchored observable package among the explicitly projector/support
expressions above is

```text
a_u = sqrt(5/6) * (1 - 1/sqrt(42)) = 0.772011886721
```

with anchored aggregate CKM+`J` absolute deviation `0.742%`.

So the branch now has a real exact-candidate dressing family, not just a
single isolated fit.

## Interpretation

This changes the honest quark endpoint in a narrow but useful way.

Before this scan, the reduced quark closure could be summarized as:

- one exact projector ray,
- one exact down amplitude,
- one exact support-angle probe,
- and one remaining non-derived scalar `a_u`.

After this scan, the honest summary is:

- the remaining non-derived scalar is **not** an unconstrained free parameter;
- it already sits on a short exact-candidate shortlist;
- that shortlist includes both a very strong simple rational candidate and a
  very strong small-radical candidate;
- projector/support-native dressings also remain competitive.

What still does **not** change:

- no retained derivation of `a_u`,
- no promotion of full quark closure to retained theorem status,
- no claim that `7/9`, `sqrt(3/5)`, or any dressing law is framework-forced.

## Relation to the earlier notes

- [QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md](./QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
  remains the strongest bounded reduced full-closure existence statement.
- [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
  remains the exact-support audit that isolates the remaining scalar.
- [QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md)
  is the follow-on restricted native-family scan.
- [QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md)
  is the later widened affine-support no-go.
- This note is the bounded candidate-law compression step that sits between
  those two endpoints.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_candidate_scan.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_candidate_scan.py`: `PASS=7 FAIL=0`
