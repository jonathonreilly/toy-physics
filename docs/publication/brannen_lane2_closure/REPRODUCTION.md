# Reproduction Instructions

**Date:** 2026-04-22
**Scope:** exact commands to reproduce every numerical claim in this closure package.

## Prerequisites

- Python 3.10+
- numpy, scipy, sympy

## Full verification

From the repository root:

```bash
# Main closure theorem (Rigid-Triangle + Octahedral-Domain + G-signature)
python3 scripts/frontier_koide_brannen_wilson_dsq_quantization_theorem.py
# Expected: PASSED: 30/30

# Dirac descent theorem (explicit lattice Wilson-Dirac at L=d=3)
python3 scripts/frontier_koide_brannen_dirac_descent_theorem.py
# Expected: PASSED: 11/11

# Residual closures: closes all three reviewer residuals
python3 scripts/frontier_koide_brannen_residual_closures.py
# Expected: PASSED: 8/8
```

**Combined: 49/49 PASS.**

## What each runner verifies

### `frontier_koide_brannen_wilson_dsq_quantization_theorem.py` (30 checks)

- §1 (3 checks): Brannen conjugate-pair structural identities (n_eff = 2, d = 3, δ_per_step = 2/9, W^{d²} = exp(2i)·𝟙).
- §2 (2 checks): Projective doublet coord ζ = e^{−2iθ}; n_eff from conjugate-pair forcing.
- §3 (1 check): natural one-clock identification context.
- §4 (5 checks): ABSS η = 2/9 with symbolic verification; G-signature vs pure Dirac distinction; explicit Z_3 cyclic rotation on Pauli algebra; spin-1/2 double cover; body-diagonal σ fixed; structural derivation of 2/9 from A0 + cubic kinematics.
- §5 (2 checks): PDG mass ratio reproduction at δ = 2/9 rad; standard Berry convention δ = 2π·η FAILS PDG.
- §6 (4 checks): Framework's selected-line δ(m_*) = 2/9 numerical; |Im(b_F)|² = 2/9 topologically protected at m_0, m_*, m_pos.
- §7 (10 checks): Rigid-Triangle Rotation Theorem (radius invariance, α(m_0)=−π/2, endpoint rotation, physical rotation, framework identification); Octahedral-Domain Theorem (|O|=24, span=2π/|O|, classical trig identities, fundamental-domain interpretation).
- §3.1 of §7 structural identities.

### `frontier_koide_brannen_dirac_descent_theorem.py` (11 checks)

- 1. Euclidean Cl(4) gammas Hermitian.
- 2. Euclidean Clifford anticommutation.
- 3. Z_3 spinor rotation cycles γ_1 → γ_2 → γ_3.
- 4. γ_0, γ_5 Z_3-invariant.
- 5. Spin-1/2 double cover U_spin^3 = −I.
- 6. Three body-diagonal fixed sites.
- 7. Dirac Hermitian + Z_3-equivariant at all tested r.
- 8. 2/9 recurs at ≥20 r values in [0.1, 3.0] scan (finds 32).
- 9. Spectrum symmetry at example r.
- 10. Symbolic ABSS verification.
- 11. Physical descent identification documented.

## Key numerical values

| Quantity | Value | Precision |
|----------|-------|-----------|
| α(m_0) | −π/2 | 10⁻¹⁴ |
| α(m_pos) − α(m_0) | −π/12 | 10⁻¹⁵ |
| α(m_*) − α(m_0) | −2/9 rad | 10⁻¹³ |
| Framework δ(m_*) | 2/9 rad | 10⁻¹² |
| G-signature η (sympy) | 2/9 | exact |
| Wilson-Dirac per-fixed-site η | 2/9 | 10⁻¹⁰ at 32 r values |

## Runtime estimates

- `frontier_koide_brannen_wilson_dsq_quantization_theorem.py`: ~5 seconds.
- `frontier_koide_brannen_dirac_descent_theorem.py`: ~30 seconds (includes fine r scan).
- `frontier_koide_brannen_residual_closures.py`: ~5 seconds.

## File manifest

Package contents:

```
docs/publication/brannen_lane2_closure/
├── README.md                  (overview, package scope)
├── DERIVATION_CHAIN.md        (step-by-step derivation)
├── CLAIMS_TABLE.md            (explicit claims + authorities)
├── CRITICAL_REVIEW.md         (honest assessment + reviewer decision framework)
├── RESIDUAL_CLOSURES.md       (closes all three reviewer residuals)
└── REPRODUCTION.md            (this file)

docs/
├── KOIDE_BRANNEN_WILSON_DSQ_QUANTIZATION_THEOREM_NOTE_2026-04-22.md
├── KOIDE_BRANNEN_DIRAC_DESCENT_THEOREM_NOTE_2026-04-22.md
└── KOIDE_BRANNEN_ANOMALY_INFLOW_HYPOTHESIS_NOTE_2026-04-22.md

scripts/
├── frontier_koide_brannen_wilson_dsq_quantization_theorem.py  (30/30 PASS)
├── frontier_koide_brannen_dirac_descent_theorem.py            (11/11 PASS)
├── frontier_koide_brannen_residual_closures.py                (8/8 PASS)
└── frontier_koide_brannen_physical_bridge_investigation.py    (supporting numerical exploration)
```

## If runner fails

- Ensure numpy/scipy/sympy are installed.
- Ensure Python 3.10+.
- Run from repository root (PYTHONPATH handling).
- Check for any numerical tolerance issues (some platforms may need slightly relaxed tolerances).

Report failures with platform/Python/numpy versions to the repository maintainer.
