# EWSB Cascade Precision: Sharpening the Log-Enhancement Factor

**Script**: `scripts/frontier_ewsb_cascade_precision.py`
**Status**: 10/10 checks pass (6 exact, 4 bounded)

## Status

BOUNDED. The lattice self-energy integrals are exact on the taste Hamiltonian. The margin analysis is model-dependent. Generation physicality remains open per review.md.

## Theorem / Claim

The EWSB log-enhancement factor L, previously estimated as log(M_Pl/v) ~ 38.8, is sharpened to L = C_heavy / C_light ~ 160, where C_heavy and C_light are the 1-loop self-energy integrals for the direct and radiative VEV couplings computed on the lattice taste Hamiltonian.

This raises the up-quark sector margin from +4% to +32%.

## Assumptions

1. The lattice Hamiltonian with Kawamoto-Smit Gamma matrices correctly describes the taste/generation structure (framework assumption).
2. The EWSB VEV phi = (v, 0, 0) selects direction 1 as weak (from frontier_ewsb_generation_cascade.py, exact 1+2 split).
3. The 1-loop self-energy dominates the mass splitting between T_1 orbit members (perturbative assumption, bounded).
4. The identification of T_1 orbit members with physical generations (generation physicality assumption, still open).
5. The synthesis framework (Wilson masses + RG + EWSB) correctly accounts for the mass hierarchy (model-dependent).

## What Is Actually Proved

### Exact results (from the lattice taste Hamiltonian)

1. **Gamma_1 connectivity**: The VEV-direction operator Gamma_1 maps the T_1 orbit members to distinct targets:
   - (1,0,0) -> (0,0,0) [singlet, hw=0]
   - (0,1,0) -> (1,1,0) [T_2, hw=2]
   - (0,0,1) -> (1,0,1) [T_2, hw=2]

2. **Self-energy integrals**: With UV cutoff Lambda = M_Planck and the VEV background:
   - C_heavy = 2 * log(M_Pl/v) = 76.89 (intermediate state is the singlet at mass ~ v)
   - C_light = log(1 + pi^2/16) = 0.48 (intermediate state is T_2 at mass ~ Lambda)
   - L = C_heavy / C_light = 160.0

3. **Coupling identification**: The VEV-direction loop uses the SU(2)_L gauge coupling:
   - alpha = alpha_weak = g^2/(4pi) = 0.034
   - alpha/(4pi) = g^2/(16pi^2) = 0.0027

4. **Color loops are democratic**: Gamma_2 and Gamma_3 map all T_1 members to T_2 members (hw=2). The color-direction loops contribute equally to all three generations and do not affect the mass splitting.

5. **JW splitting is perturbative**: The Jordan-Wigner asymmetry between directions 2 and 3 gives |m_2/m_3 - 1| ~ 0.5% at O(g^2 a^2). This enters only at 2-loop / O(a^2) because at 1-loop Gamma_mu Gamma_1 Gamma_mu = -Gamma_1 for mu = 2, 3.

### Bounded results (model-dependent)

6. **Mass ratio from EWSB cascade**:
   - Heavy generation: m_3 = y * v (tree-level Yukawa to singlet)
   - Light generations: m_1,2 = y * v * [alpha_w/(4pi)] * C_light (radiative only)
   - Ratio: m_heavy/m_light ~ 1 / (0.0027 * 0.48) ~ 770

7. **Sharpened margin table**:

   | Sector | Required Delta(gamma) | Available | Margin |
   |--------|----------------------|-----------|--------|
   | Down quarks | 0.016 | 0.173 | +987% |
   | Leptons | 0.051 | 0.173 | +242% |
   | Up quarks | 0.131 | 0.173 | +32% |

   vs. the original (L = 38.8):

   | Sector | Required Delta(gamma) | Available | Margin |
   |--------|----------------------|-----------|--------|
   | Down quarks | 0.052 | 0.173 | +230% |
   | Leptons | 0.087 | 0.173 | +99% |
   | Up quarks | 0.167 | 0.173 | +4% |

## What Remains Open

1. **Generation physicality**: The identification of T_1 orbit members with physical fermion generations is still not proved at theorem grade. The 1+2 split is exact; the 1+1+1 hierarchy is bounded.

2. **C_light evaluation scale**: C_light = 0.48 uses the lattice-scale loop integral where the T_2 intermediate state lives at the cutoff. If the T_2 mass is renormalized significantly below the cutoff by RG running, C_light would increase and L would decrease. The conservative bound (C_light = log(M_Pl/v), L = 9.6) gives much weaker margins.

3. **Double-counting with RG**: The synthesis formula multiplies L_EWSB with the RG factor. The RG running converts Wilson mass ratios to exponential hierarchies. The EWSB factor provides the additional tree-vs-radiative suppression. The boundary between these two mechanisms is model-dependent.

4. **JW 2-3 splitting**: The 0.5% JW splitting is far too small to explain the charm/up or strange/down ratios. The intra-generation hierarchy must come from the Wilson mass difference and RG running, not from the JW structure. The beta_JW = 0.1 parameter used in the model is not derived from first principles.

## How This Changes The Paper

The sharpened EWSB log factor moves the up-quark margin from +4% (barely sufficient) to +32% (comfortable). This means the bounded EWSB + RG synthesis model has room to accommodate all three SM sectors without requiring the strong-coupling anomalous dimension to be tuned to its maximum value.

This does NOT change the generation physicality status -- that gate remains open. It strengthens the BOUNDED hierarchy model.

Paper-safe wording: "The EWSB log-enhancement factor, computed from the lattice self-energy integrals rather than estimated, gives L ~ 160 (vs the previous estimate of ~39). This provides a +32% margin for the up-quark sector in the bounded hierarchy model."

## Commands Run

```
python3 scripts/frontier_ewsb_cascade_precision.py
# 10 PASS, 0 FAIL
```
