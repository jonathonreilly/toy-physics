# B-Independence Mechanism Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-01  
**Scope:** review-safe mechanism note for why the corrected linear path-sum
force stays flat/topological on the current retained DAG families.

## Short version

The current mainline evidence supports a simple mechanism story:

- the path ensemble does **not** look like it is scrambling transverse
  position into a generic center;
- the retained graph-wide field does look like a smooth phase-valley
  landscape that reaches broadly across the connected DAG;
- localized field variants can weaken the signal, but they do not restore a
  clean `1/b` law;
- therefore the flat distance law is best read as a structural property of
  the linear path-sum on these discrete causal graphs, not as a bug in one
  particular field kernel.

This note is intentionally narrower than the full distance-law closure:
the propagator-power sweep, locality-shell sweep, fixed-mass shell sweep,
minimal nonlinearity probe, and effective-metric probe already closed the
easy rescue lanes. This document just explains the mechanism picture that
goes with that closure.

## What the diagnostics say

Two companion scripts summarize the current mechanism view:

- [scripts/path_sampling_analysis.py](/Users/jonreilly/Projects/Physics/scripts/path_sampling_analysis.py)
- [scripts/field_localization_test.py](/Users/jonreilly/Projects/Physics/scripts/field_localization_test.py)
- [2026-04-01-b-independence-mechanism.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-01-b-independence-mechanism.txt)

### 1. Path preservation

The path-sampling diagnostic is meant to answer a very specific question:
does the graph ensemble preserve local transverse routing, or does it
scramble paths so thoroughly that all impact parameters become equivalent?

The retained modular DAGs support the first reading, not the second:

- channel openings remain channel-like at the detector side;
- post-barrier amplitude stays mostly on the same side that was opened;
- the amplitude distribution is broad enough to support a graph-wide path
  ensemble, but not so scrambled that source-side transverse information is
  erased.

That means the flat force law is not well explained by "the paths all mix to
the center anyway." The graph keeps local routing structure.

### 2. Graph-wide field / phase valley

The field-localization diagnostic asks whether the force law is driven by a
field that is too smooth and graph-wide, rather than by a sharply local
interaction.

The current answer is:

- the Laplacian-relaxed field gives the strongest retained gravity signal;
- sharp or strongly localized fields usually weaken the signal or make the
  sweep noisier;
- none of the tested local field variants restores a clean `1/b` falloff on
  the retained modular family.

So the best mechanism picture is:

- the graph preserves local paths;
- the field spreads enough to act as a smooth phase valley on that path
  ensemble;
- the integrated phase perturbation is then dominated by a graph-averaged
  field, which is why the force behaves topologically rather than like a
  simple geometric `1/b` law.

## What this does and does not claim

This note does **not** claim:

- a derivation of the phase-valley mechanism from deeper first principles;
- a universal theorem over all possible graph families;
- a rescue of Newtonian distance falloff inside the current linear
  path-sum architecture.

It does claim:

- the path-sum model is not flat in `b` because paths scramble;
- the retained field law is not flat in `b` because it is too local;
- the broad, graph-averaged field is the more plausible source of the
  topological force law on the retained families.

## Review-safe summary

The current mainline distance-law story is now best summarized as:

- local path preservation survives;
- graph-wide smooth fields survive;
- neither propagator-power tuning nor localized field variants recover a
  clean `1/b` law;
- so the b-independence is a structural feature of the current linear
  path-sum architecture.

That is a mechanism diagnostic, not a new rescue lane.
