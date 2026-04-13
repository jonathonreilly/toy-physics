# Wild Idea: Bypass Baryogenesis via Freeze-Out Ratio?

**Date:** 2026-04-13
**Status:** Sharp negative. The idea fails on physics grounds.

## The Proposal

Compute R = Omega_DM / Omega_b directly from the RATIO of thermal
freeze-out yields, without ever computing the baryon asymmetry eta.

Both visible and dark sectors share a single thermal plasma. They
freeze out at different temperatures because they have different
annihilation cross-sections (both derived from H via T-matrix). The
ratio of their relic abundances is:

    Y_DM / Y_vis = (sigma_v_vis / sigma_v_DM) * f(x_F_DM, x_F_vis)

where Y = n/s (yield), sigma_v are thermally averaged cross-sections,
and f encodes the freeze-out kinematics.

Since R = (m_DM / m_b) * (Y_DM / Y_b), and we already have the mass
ratio from Hamming weights, if Y_b were also a freeze-out yield then
R would be fully determined without baryogenesis.

## Why It Fails

The idea conflates two fundamentally different mechanisms for setting
relic abundances:

**Dark matter abundance (freeze-out):**
DM particles are their own antiparticles (or have equal particle and
antiparticle populations). At freeze-out, annihilation stops and the
SYMMETRIC population is frozen in. The relic density is set by the
annihilation cross-section: larger sigma_v means later freeze-out and
smaller Y_DM. This is the standard WIMP miracle calculation.

**Baryon abundance (asymmetry):**
Baryons are NOT set by freeze-out of a symmetric population. Quarks
and antiquarks annihilate almost completely -- the tiny residual
baryon density is the ASYMMETRY n_B - n_Bbar, not a freeze-out relic.
This asymmetry is parameterized by eta = n_B / n_gamma ~ 6e-10. The
baryon yield Y_b = eta / 7.04 is determined by whatever mechanism
created the matter-antimatter asymmetry (baryogenesis), not by the
QCD annihilation cross-section.

If baryons DID freeze out symmetrically like WIMPs, the baryon relic
density would be many orders of magnitude smaller than observed (the
"baryon catastrophe" of symmetric cosmology).

## Can We Rescue It?

Three escape routes were considered:

**1. Express eta as a ratio of framework quantities.**
This would require computing the baryon asymmetry from H. But
baryogenesis needs: (a) baryon number violation, (b) C and CP
violation, (c) departure from thermal equilibrium (Sakharov
conditions). While the framework can produce CP violation from complex
phases in the T-matrix, computing the actual magnitude of the
asymmetry requires a full out-of-equilibrium field theory calculation
-- essentially solving baryogenesis, which is the hardest unsolved
problem in particle cosmology. This does not simplify anything.

**2. Treat both sectors as asymmetric.**
If the dark sector ALSO has an asymmetry (asymmetric dark matter),
then R = (m_DM / m_b) * (eta_DM / eta_b). But now we need TWO
asymmetries instead of one, making the problem harder.

**3. Find a relation eta = g(framework quantities) that avoids
dynamical baryogenesis.**
For instance, if eta were fixed by the number of degrees of freedom
at the EW phase transition. The sphaleron rate converts lepton
asymmetry to baryon asymmetry, and the conversion factor B = 28/79 in
the SM IS computable from the framework (it depends only on the
number of generations and Higgs doublets). But the INPUT lepton
asymmetry still needs a dynamical calculation (leptogenesis).

## Verdict

**The ratio R = Omega_DM / Omega_b fundamentally requires two
different physics inputs:**

1. sigma_v for DM (freeze-out) -- we have this from H
2. eta for baryons (asymmetry) -- we do not have this from H

These are not the same kind of calculation, and no algebraic trick
makes one reduce to the other. The baryon abundance is not a thermal
relic; it is an asymmetry relic. The s in Y = n/s does cancel in the
ratio, but the numerators n_DM and n_b are determined by completely
different physics (cross-section vs. CP-violating out-of-equilibrium
dynamics).

The existing approach (compute sigma_v from H, take eta from
observation, derive R) remains the cleanest path. Bypassing
baryogenesis for R requires solving baryogenesis -- there is no
shortcut.

## What This Clarifies

This exercise sharpens the status of R in the framework:

- **What the framework CAN do:** predict m_DM/m_b and sigma_v, which
  together with the observed eta give R. This is already nontrivial.
- **What the framework CANNOT do (yet):** predict eta from first
  principles. This would require a full baryogenesis calculation,
  which is a separate (and major) research program.
- **The honest claim:** R is a ONE-parameter prediction (using
  observed eta), not a zero-parameter prediction. This is still
  valuable -- the SM itself does not predict eta.
