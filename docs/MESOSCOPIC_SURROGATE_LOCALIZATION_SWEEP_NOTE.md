# Mesoscopic Surrogate Localization Sweep

**Status:** bounded - bounded or caveated result note

**Primary runner:** [`scripts/mesoscopic_surrogate_localization_family_sweep.py`](../scripts/mesoscopic_surrogate_localization_family_sweep.py)

**Runner cache:** [`logs/runner-cache/mesoscopic_surrogate_localization_family_sweep.txt`](../logs/runner-cache/mesoscopic_surrogate_localization_family_sweep.txt)
(SHA-pinned; runner exits 0; ~6s on the audit-lane host.)

This note records an alternative localization-family sweep on the retained 3D ordered-lattice mesoscopic source control. The question was whether an explicitly local source shape can preserve the same two-stage sourced-response stability as the broad top-N control, and possibly improve on it.

## Setup

The sweep reuses the retained 3D valley-linear family and compares three localization families:

- `topN` compression
- symmetric square windows around the peak bin
- compact Gaussian masks centered at the peak bin

All families are evaluated against the same stage-1 sourced profile, then relaunched through the same field and compared by:

- stage-1 and stage-2 capture
- stage-1 and stage-2 centroid shifts
- best-shift score between the two stages
- width ratio between stages

The full sweep log is here:

- [logs/2026-04-04-mesoscopic-surrogate-localization-family-sweep.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-localization-family-sweep.txt)

## Retained result

The sweep found that:

- degenerate point-like localizations can reach the best score numerically
  - square radius `0`
  - Gaussian `sigma=0.5`
- but those cases have very low capture and effectively behave like point-source surrogates
- once the family is meaningfully localized but still carries nontrivial support, the broad top-N control remains the least-bad mesoscopic source

The best scored rows were:

- `square radius 0`: score `1.0000`, width ratio `1.0000`, capture2 `0.107`
- `gaussian sigma 0.5`: score `1.0000`, width ratio `1.0033`, capture2 `0.171`

The strongest non-degenerate localized rows were weaker than the broad top-N control in the score/capture tradeoff:

- `square radius 1`: score `1.0000`, capture2 `0.427`
- `gaussian sigma 1.0`: score `0.9998`, capture2 `0.409`
- `topN 25`: score `0.9993`, capture2 `0.993`
- `topN 49+`: score `0.9994`, capture2 `1.000`

## Safe read

The honest interpretation is:

- more localized families do not obviously beat the broad top-N control on the retained 3D family
- the near-point-source cases can match the shift score, but only by collapsing into very small capture/support
- for a mesoscopic source object, top-N remains the least-bad control unless a future sweep finds a non-degenerate localized family with comparable capture and width stability

This is a bounded negative result, not a failure of the broader surrogate lane.
