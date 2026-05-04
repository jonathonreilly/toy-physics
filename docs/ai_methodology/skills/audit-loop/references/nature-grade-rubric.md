# Nature-Grade Audit Rubric

Use this rubric when writing an audit verdict for the CL3 audit lane.

## Hostile Review Standard

The claim should be able to survive a specialist referee who assumes the result is wrong and looks for:

- hidden imported physics;
- circular dependence on the target result;
- definition-as-derivation;
- selected observable/readout/carrier not forced by retained inputs;
- unit normalization introduced as if it were a theorem;
- sector selection chosen because it gives the answer;
- stale numerical values relative to the runner;
- matching the wrong observable;
- runner PASS lines that check consistency after hard-coding the contested premise;
- algebraic decoration advertised as independent physics.

The burden is on the note. If the closure is not explicit, do not infer it.

## Common P0/P1 Failure Modes

### Physical-Observable Bridge Missing

Symptoms: the note identifies two physical quantities, phases, currents, carriers, source laws, or readouts without a retained theorem constructing the map.

Verdict usually: `audited_conditional` or `audited_renaming`.

Repair target: a theorem deriving the map from retained primitives and a runner that constructs the map rather than setting the output.

### Hard-Coded Runner

Symptoms: runner sets the target value or disputed bridge directly, then marks closure because downstream algebra agrees.

Verdict usually: same as the note's actual failure, often `audited_conditional`, `audited_renaming`, or `audited_failed`.

Repair target: runner must compute the load-bearing object from inputs and fail when the bridge is removed.

### Misidentified Observable

Symptoms: note compares a framework quantity to a different experimental observable or relabels states/indices to get a match.

Verdict usually: `audited_failed`.

Repair target: state the correct observable and redo the prediction/comparator under standard labels.

### Numerical Staleness

Symptoms: headline number disagrees with the formula or current runner output.

Verdict usually: `audited_failed` if the headline claim depends on it; otherwise `audited_conditional`.

Repair target: update note and rerun; if the corrected value weakens the claim, demote accordingly.

### Decoration / Corollary Inflation

Symptoms: exact identity is true but is only an algebraic restatement of an upstream theorem and adds no new comparator, compression, or independent falsifiability.

Verdict usually: `audited_decoration`.

Repair target: box under parent claim or add a real independent physical/comparator surface.

### Tuned Numerical Match

Symptoms: a result works only after choosing a scale, sector, endpoint, source, or parameter because it matches the target.

Verdict usually: `audited_numerical_match` or `audited_conditional`.

Repair target: derive the selection rule independently or present the result as a calibrated scenario.

## Failure Handoff Quality Bar

A non-clean audit is useful only if a physicist can act on it. Include:

- the exact failing step;
- the reason it blocks the current claim;
- the theorem/input/computation needed to fix it;
- the safe reduced claim that remains.

Do not write vague rationales such as "needs more work" or "not convincing." Name the missing theorem.
