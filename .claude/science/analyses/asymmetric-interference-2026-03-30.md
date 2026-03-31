# Analysis: Asymmetric Interference

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-asymmetric-sweep.txt`
- Script: `scripts/interference_asymmetric_sweep.py`

## Data Summary
- 5 configurations tested, each with coherent + record mode
- Full V(y) profiles and P(y) distributions

## Key Findings

### Finding 1: Symmetry breaking destroys V(y=0) = 1.0
| Config | V(y=0) |
|--------|--------|
| Symmetric baseline | 1.000 |
| Asymmetric slits (+2, +6) | 0.010 |
| Strongly asymmetric (+1, +8) | 0.000 |
| Off-center source, symmetric slits | 0.229 |
| Off-center source + asymmetric slits | 0.163 |

**The symmetry protection is decisively broken.** V(y=0) drops from 1.0 to as low as 0.000 with strong asymmetry. This confirms the sanity check's earlier concern: the V=1 at center was indeed a symmetry artifact in the original experiment.

### Finding 2: Visibility peak shifts to between the slits
- Asymmetric slits (+2, +6): highest visibility near y=+6 (V=0.50), the wider slit.
- Strongly asymmetric (+1, +8): visibility concentrates near y=+8 (V=0.99), the more isolated slit.
- The visibility profile is no longer symmetric — it's pulled toward the slit that subtends more of the detector's view.

### Finding 3: Interference survives symmetry breaking
Even with broken symmetry, interference still occurs — V is nonzero at multiple screen positions. The model's path-sum produces genuine multi-path interference, not just a symmetric-geometry artifact. This is the key result.

### Finding 4: Off-center source creates new interference patterns
- Source at (1, +3) with symmetric slits: V peaks near the lower slit (y=-4, V=0.50), NOT near the source. The source position biases which slit gets more amplitude, changing the interference pattern.
- Combined off-center + asymmetric: rich multi-peak V profile with peaks near both slits AND near the source.

### Finding 5: Record suppression remains complete under asymmetry
All record-mode configurations show V=0 at all positions. The record mechanism is robust to symmetry breaking.

## Hypothesis Verdict
**SUPPORTED** — Breaking symmetry produces asymmetric V(y) profiles, eliminates the trivial V(y=0)=1 artifact, and confirms that interference is a genuine dynamical property of the model, not a setup artifact.

## Significance
This is the strongest evidence so far that the model produces genuine interference from its path-sum dynamics. The symmetric setup was a special case; the asymmetric setup tests the general mechanism.
