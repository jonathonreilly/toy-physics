# Direct Top Mass from Lattice Propagator Pole

**Script:** `scripts/frontier_yt_direct_pole.py`
**Status:** BOUNDED (exact algebraic sub-results + CW 1-loop)
**Date:** 2026-04-13

## Idea

Skip the RGE entirely. Compute m_t directly as the pole of the staggered
propagator at the hw=1 Brillouin zone corner k = (pi, 0, 0).

On a lattice with spacing a = l_Planck:

    m_phys = E_pole x M_Planck

where E_pole is the dimensionless pole position in G(k, E) = <k|(E - H)^{-1}|k>.

## Results

### What works (exact)

1. **Bare pole verified.** The free staggered Hamiltonian at k = (pi, 0, 0)
   has all 8 eigenvalues degenerate at E = 2r. With r = 1, the bare mass
   is 2 M_Planck ~ 2.4e19 GeV.

2. **Hierarchy is manifest.** m_t / m_bare = 173 / (2 x 1.22e19) ~ 7e-18.
   The lattice makes the hierarchy problem sharp: the bare mass IS the
   cutoff. No hand-waving about "quadratic divergences."

3. **Cl(3) ratio verified.** y_t / g_s = 1/sqrt(6) from the G_5 trace
   identity. Centrality of G_5 in d=3 protects this at all orders.

### What fails

4. **Pure CW has no minimum.** With Lambda = M_Planck and SM couplings, the
   1-loop Coleman-Weinberg potential has effective quartic lambda_eff < 0
   (top loop dominates). The potential is unbounded below -- no stable
   vacuum at v = 246 GeV without tuned bare parameters.

5. **Naive ratio at M_Z misses by ~60%.** Using y_t = g_s(M_Z)/sqrt(6)
   directly gives m_t ~ 73 GeV, off by a factor of ~2.4. The ratio
   y_t/g_s = 1/sqrt(6) holds at M_Planck, not at M_Z. Running is essential.

6. **CW dimensional transmutation scale is wrong.** The CW estimate
   v ~ M_Pl x exp(-8 pi^2 / (3 y_t^2)) ~ 10^7 GeV, five orders of
   magnitude above the EW scale.

## Verdict

**You cannot skip the RGE.** The lattice propagator pole lives at the Planck
scale. Bridging from M_Planck to m_t = 173 GeV requires either:

- (a) the RGE (the existing derivation chain), or
- (b) a nonperturbative mechanism that generates the full hierarchy.

The CW mechanism alone does not produce v = 246 GeV with a Planck-scale
cutoff. It needs tuned bare parameters (the standard fine-tuning problem).

## Value of this negative result

This confirms that the framework's derivation chain --

    lattice -> Cl(3) ratio -> alpha_V(M_Pl) -> 1-loop RGE -> y_t(M_Z) -> m_t

-- is the correct and minimal path. There is no shortcut through the
hierarchy. The RGE is doing real physical work: it encodes the logarithmic
running that converts O(1) UV couplings into the observed IR masses.

## Derivation chain summary

| Step | Content | Status |
|------|---------|--------|
| 1 | Free propagator pole at hw=1 corner | EXACT |
| 2 | Hierarchy: m_t/m_bare ~ 10^{-17} | EXACT |
| 3 | y_t/g_s = 1/sqrt(6) from Cl(3) | EXACT |
| 4 | CW potential from derived couplings | BOUNDED |
| 5 | Self-consistent VEV extraction | BOUNDED (fails: no minimum) |
| 6 | m_t = y_t v/sqrt(2) predictions | BOUNDED |
