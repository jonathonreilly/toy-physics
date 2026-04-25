# SU(3) Gauge-Loop Derivation of the 8/3 Enhancement -- Obstruction Note

**Date:** 2026-04-25 (third iteration)
**Status:** **HONEST OBSTRUCTION** on the simplest closure path for the
unified A0+G1 candidate identity. The standard one-loop Coleman-Weinberg
gauge-boson contribution to a color-singlet scalar's mass is exactly
zero. The 8/3 enhancement of the dark-sector hierarchy compression
cannot emerge from this route; an alternative mechanism is required.
**Primary runner:** `scripts/frontier_dm_su3_gauge_loop_derivation_attempt.py`
**Runner result:** `PASS = 8, FAIL = 0`.

## Why this is in the science chain

The freeze-out-bypass quantitative theorem
([`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md))
identifies `m_DM = N_sites * v = 16 v` as the audit-discovered structural
candidate. The unified A0+G1 candidate
([`DM_DARK_SECTOR_HIERARCHY_COMPRESSION_CANDIDATE_NOTE_2026-04-25.md`](DM_DARK_SECTOR_HIERARCHY_COMPRESSION_CANDIDATE_NOTE_2026-04-25.md))
expresses this as

```
m_DM = 6 * M_Pl * (8/3) * (7/8)^(1/4) * alpha_LM^16
```

where `8/3 = dim(adj_3)/N_c` is the SU(3) Casimir ratio bridging the
chiral Wilson bare mass `6 M_Pl` to the audit candidate `16 v`. The
candidate's promotion to retained-grade requires deriving this `8/3`
from a specific dynamical mechanism on the SU(3)-gauged staggered
minimal block.

## What the runner verifies

The runner attempts the standard route -- one-loop Coleman-Weinberg
gauge-boson contribution to a scalar's mass-squared:

```
delta m^2 = (3 g^2 / (16 pi^2)) * C_2(R) * m^2 * log(Lambda^2/m^2)
```

For a color-SINGLET scalar (representation R = trivial), `C_2(R) = 0`,
so `delta m^2 = 0` at one loop. **The 8/3 cannot emerge from this
route.**

The runner additionally tests:
- Two-loop adjoint propagator: gives `dim(adj) * C_F = 32/3` or `32/9`
  with normalization, neither matches 8/3.
- Color-singlet bilinear sum rule: gives `4/9`, no match.
- Alternative SU(3) Casimir ratios (`2 * C_F`, `dim(adj)/N_c`, etc):
  numerically match 8/3 but lack derivation that places them in a
  dark-singlet mass calculation.

## Conclusion

The standard perturbative one-loop gauge route is OBSTRUCTED. The 8/3
enhancement must come from a non-standard mechanism. The runner names
three alternative routes for follow-up:

### R1 -- Wilson-r doubling

The lattice Wilson action with `r = 1` doubles the fermion content. If
the dark singlet sits in the doubled sector and picks up an extra
factor of 2 from the doubling, combined with `C_2(F) = 4/3`, this
gives `2 * 4/3 = 8/3`. Status: NOT YET DERIVED. Needs a careful
accounting of staggered-Dirac doubler structure restricted to the
gauge-singlet block.

### R2 -- Non-perturbative gluon condensate

The QCD vacuum has a non-zero `<Tr(F^2)>` condensate. The dark singlet
may acquire mass via this condensate proportional to `dim(adj)/N_c`.
Status: speculative; non-perturbative gluon condensate is bounded but
not derived in the framework.

### R3 -- Cl(3) / SU(3) embedding structural identity

The Cl(3) chiral algebra `C^8 = (C^2)^otimes 3` has dimension `8 = dim(adj_3)`.
The retained
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
embeds SU(3)_c on the 3D symmetric base subspace of `C^4_base ⊗ C^2_fiber`,
with the antisymmetric 1D base being a lepton singlet. The dark
singlet's `8/3` ratio could emerge from a specific algebraic identity
between the Cl(3) chiral cube structure and the SU(3) adjoint
representation. Status: this is the most structurally promising route
and requires explicit calculation on the Cl(3) -> SU(3) bridge.

## Why this is meaningful

This obstruction note RULES OUT the most obvious closure path
(perturbative one-loop CW). Future work attempting the unified A0+G1
closure should NOT pursue the standard one-loop route -- it has been
checked here and gives exactly zero for the color-singlet sector.

The closure must instead pursue R1 (Wilson doubling), R2
(non-perturbative condensate), or R3 (Cl(3)/SU(3) embedding). Of
these, R3 is structurally most aligned with the framework's existing
retained CL3_COLOR_AUTOMORPHISM_THEOREM.

The obstruction is therefore CONSTRUCTIVE: it sharpens the open lane
from "derive 8/3" to "derive 8/3 via the Cl(3)/SU(3) embedding
identity". This is a more specific and tractable theorem to attempt
in follow-up.

## What this note does NOT claim

- That the 8/3 enhancement is impossible. It rules out only the
  one-loop CW route; alternatives R1-R3 remain open.
- That the unified A0+G1 candidate is falsified. The candidate stands
  with its open lane sharpened.
- That R3 (Cl(3)/SU(3) embedding) is the correct mechanism. It is
  flagged as most promising; the actual derivation is still open.

## Cross-references

- [`DM_DARK_SECTOR_HIERARCHY_COMPRESSION_CANDIDATE_NOTE_2026-04-25.md`](DM_DARK_SECTOR_HIERARCHY_COMPRESSION_CANDIDATE_NOTE_2026-04-25.md)
  -- the unified A0+G1 candidate this obstruction note constrains.
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  -- retained Cl(3) -> SU(3) embedding referenced in R3.
- [`DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md)
  -- adversarial review that named A0 and G1 originally.
