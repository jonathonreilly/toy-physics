# Koide Q probe-source zero-background Nature review

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_q_probe_source_zero_background_nature_review.py`
**Status:** adversarial review pass for retained source-response Q closure

## Review Target

The theorem under review derives the Q zero section from source-response
semantics:

```text
physical scalar observable = probe-source Taylor coefficient at J=0.
```

It rejects treating an arbitrary nonzero `J0` as another value of the same
coefficient.  A nonzero `J0` is a different undeformed background:

```text
D -> D + J0.
```

## Verdict

Accepted as a retained source-response closure of the Q residual.

The retained generator is:

```text
W[J] = log |det(D+J)| - log |det D|.
```

On the normalized two-channel carrier:

```text
W(k_plus,k_perp) = log(1+k_plus) + log(1+k_perp).
```

The probe-source coefficients at the undeformed theory are:

```text
dW/dk_plus |0 = 1
dW/dk_perp |0 = 1.
```

Therefore:

```text
Y = (1,1)
K_TL = 0
Q = 2/3.
```

## Hostile Review Answers

- **Target import:** no.  The value follows after the source-domain theorem.
- **Hidden midpoint choice:** no.  The midpoint is the Taylor coefficient at
  the undeformed source, not a selected probability.
- **Old no-gos:** compatible.  They remain valid if a nonzero undeformed
  charged-lepton background source is retained.
- **Falsifier:** retain a native nonzero charged-lepton scalar background
  `J0 != 0`.

## Verification

```bash
python3 scripts/frontier_koide_q_probe_source_zero_background_nature_review.py
python3 -m py_compile scripts/frontier_koide_q_probe_source_zero_background_nature_review.py
```

Expected closeout:

```text
KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_NATURE_REVIEW=PASS
KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE
KOIDE_Q_K_TL_ZERO_DERIVED=TRUE
Q_PHYSICAL=2/3
NO_TARGET_IMPORT=TRUE
FALSIFIER=retained_nonzero_undeformed_charged_lepton_scalar_background_source
```
