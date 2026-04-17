# Review Note: `claude/angry-chatelet-2dc78c`

## Status

Current verdict: **do not merge as-is**.

The branch is mechanically clean:

- rebase is clean on current `origin/main`;
- the new authority runner replays cleanly at `EXACT PASS=19`,
  `BOUNDED PASS=3`, `FAIL=0`;
- the sibling CKM runners cited in the branch summary also replay cleanly.

The remaining problem is claim discipline, not runtime. The branch currently
promotes a still-open identification surface as if it were a retained theorem
output.

## Why It Does Not Clear

### 1. The new bridge theorem is still exact only by choosing the identification surface

The authority note defines

- `m_d/m_s := alpha_s(v) / 2`
- `m_s/m_b := [alpha_s(v)/sqrt(6)]^(6/5)`

and then proves GST and the `5/6` bridge exactly on that chosen surface.

That algebra is correct. But the note also explicitly says the framework still
lacks:

- a framework-internal RG/transport derivation that **forces** this
  identification surface from retained inputs;
- a theorem-grade scale-selection rule.

So the retained structural content is narrower than the current theorem
headline:

- `sqrt(6)` is the same retained Ward / `Q_L` block constant;
- `1/2 = 1/n_pair`;
- `5/6 = 1 - 1/6` is the atlas orthogonal-complement projector weight on the
  six-state block.

What is **not** yet retained is the claim that the down-type mass ratios
themselves sit on this exact identification surface as a framework output. At
the current tip, GST and the `5/6` bridge are exact on the chosen
identification surface, not exact retained outputs of the framework.

### 2. The new runner certifies the conditional algebra, not the open forcing step

The runner is honest enough when read closely: it hardcodes

- `r_ds = alpha_s(v) / 2`
- `r_sb = [alpha_s(v)/sqrt(6)]^(6/5)`

and then verifies that the bridge formulas hold on that surface.

That means the runner certifies:

- the structural count equalities;
- the projector-weight equalities;
- the exact algebra once the identification surface is chosen.

It does **not** certify the still-open step that would make this a retained
framework theorem rather than an atlas-consistent identification.

### 3. The publication surfaces propagate the same overpromotion

The package surfaces currently advertise the lane as a retained structural
theorem rather than as conditional exact algebra on an open identification
surface.

That is too strong until the forcing step is actually closed.

## Mergeable Alternatives

### Option A: Conservative landing

Keep the structural content only:

- same `sqrt(6)` constant in Ward and CKM lanes;
- GST exponent `1/2 = 1/n_pair`;
- `5/6` bridge exponent numerically matching the retained `1 + 5` projector
  split rather than being carried only by the Casimir coincidence.

Then frame GST and the `5/6` bridge as exact algebra on a chosen
identification surface that remains open as a framework derivation.

### Option B: Full retained promotion

Only promote this as a retained bridge theorem if you add the missing theorem
that forces the identification surface

- `m_d/m_s := alpha_s(v) / 2`
- `m_s/m_b := [alpha_s(v)/sqrt(6)]^(6/5)`

from retained framework structure, plus the theorem-grade scale-selection rule
for the observation surface.

## Bottom Line

This is useful work and the branch materially improves the hygiene of the
down-type CKM-dual lane. But right now it is still packaging a chosen
identification surface as if the framework had already derived it. That is the
remaining blocker.
