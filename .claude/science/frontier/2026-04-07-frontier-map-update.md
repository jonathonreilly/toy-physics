# Frontier Map Update — 2026-04-07

## Direction (after Lane 8b promotions + Lane 9 hardening review)

Modest, not dramatic, adjustments to two scorecard rows:

| Row | Old | New | Why |
| --- | --- | --- | --- |
| Strength against harshest critique | static + 3 families | static + 26 swept + 8 held-out + LOO | empirical only, not derived; modest bump |
| Compact underlying principle | 3 families pass | 2-property AND rule predicts 8/8 held-out | small bump; rule is fitted, not proved |
| Theory compression | open | open | Lane 9 does **not** close this; the rule is empirical |

## Lanes shipped this session (artifact-chain clean)

| Lane | Subject | Status |
| --- | --- | --- |
| 4 | Poisson 3D static gravity | retained |
| 5 | (2+1)D wave-eq lightcone (delta pulse) | retained |
| 6 | (2+1)D retarded ≠ instantaneous | retained (proper c=∞ comparator) |
| 7 | (2+1)D radiation slope −0.47 | retained (narrow scope) |
| 8 | (3+1)D radiation falloff slope −1.14 | retained (narrow scope) |
| 8b | (3+1)D lightcone + (3+1)D retarded ≠ inst | retained |
| 9 | Universality classifier (empirical) | retained (LOO 84.6%, held-out 8/8) |

## Lane 9 explicit boundary (do NOT count it as the derivation closure)

- Battery is **static only**: gravity sign, F~M, Born, null
- Classifier is **empirical**: thresholds fitted on 26 families, not proved
- Held-out set is built by the same author on the same lattice, in the same generator family
- LOO 84.6% < in-sample 100% — thresholds are fragile under single-family removal
- The rule's structural meaning (connectivity + Z2 in measurement axis) is intuitive but not derived

## Three hardening steps (in priority order)

1. **Add one dynamic condition to the classifier battery** (cheap, decisive)
   - Add Lane 6 retarded-vs-instantaneous gap as a 5th PASS condition
   - Re-fit the classifier on the dynamic-augmented battery
   - Re-run LOO and held-out
   - Expected: a few families that pass the static battery may fail the dynamic one — that's the test

2. **Test a genuinely different generator family as held-out** (medium cost)
   - Build a generator that is **not** a parameter variation of the current family
   - Candidates: random k-regular DAG, hyperbolic lattice, expander graph, sparse-random with no underlying grid
   - Evaluate the classifier on those without refitting
   - This kills the "same author, same lattice family" caveat

3. **Derive or no-go the classifier analytically** (hardest)
   - From path-sum + S=L(1−f), prove that gravity TOWARD requires Z2 symmetry in the measurement axis
   - Or: prove that F~M ≈ 1 requires sufficient connectivity (avg_deg ≥ some f(propagator))
   - If a derivation exists, the classifier becomes a theorem; if it can be shown impossible, that's a no-go
   - This is the "compact underlying principle" promotion

## What this map update is NOT

- Not a claim that the harshest critique is solved
- Not a claim that Lane 9 is a universality theorem
- Not a claim that the held-out validation is independent of the author
- Not a substitute for the dynamic-condition extension or analytic derivation

## Next step in this session

Step 1 above: add the Lane 6 dynamic condition to the classifier battery, re-run LOO + held-out, and report whether the dynamic-augmented PASS rate moves.
