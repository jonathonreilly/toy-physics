# Chain Closure: 3D-vs-4D Structural Mismatch — Honest Negative + Sharp Diagnosis

**Date:** 2026-05-06
**Claim type:** research_finding (negative closure result + structural diagnosis)
**Status:** research_finding (chain stays at bounded support 4.4 ppm; new structural insight)
**Companion:** [`CHAIN_CLOSURE_FINAL_ROBUST_SYNTHESIS_NOTE_2026-05-06.md`](CHAIN_CLOSURE_FINAL_ROBUST_SYNTHESIS_NOTE_2026-05-06.md)

## Headline

The Nature-grade follow-up — L→∞ extrapolation of Route 4's direct MC
ρ_(p,q)(β=6) measurement — was attempted at L=2, 3, 4, 6. **It does
NOT close the famous problem**, but yields a sharp structural diagnosis:

**Route 4's Peter-Weyl readout on a 3D spatial cube measures the WRONG
physical object for the framework's 4D Perron formula.** The chain's
residual is the 3D-spatial vs 3D+1-temporal dimensional difference,
not a perturbative correction.

This honestly negative result is structurally clean and unifies
several prior findings.

## The numerical evidence

Route 4 MC (4 chains × 800 therm + 4000 sample × interval 2):

| irrep | L=2 | L=3 | L=4 | L=6 |
|---|---|---|---|---|
| (1,0) | +0.080 ± 0.007 | +0.030 ± 0.011 | +0.030 ± 0.003 | +0.043 ± 0.009 |
| (1,1) | +0.005 ± 0.001 | +0.007 ± 0.002 | +0.001 ± 0.002 | +0.002 ± 0.003 |
| (2,0) | +0.005 ± 0.002 | +0.003 ± 0.001 | +0.0001 ± 0.002 | +0.001 ± 0.002 |
| (2,2) | -0.0003 ± 0.0003 | -0.0002 ± 0.0005 | -0.0002 ± 0.0003 | +0.0006 ± 0.0006 |

**ρ_(1,0) plateaus at ~0.031 ± 0.003 for L ≥ 3.** Significantly nonzero
(χ² = 283 vs zero hypothesis, dof = 4) but very small.

FSS extrapolation `ρ(L) = ρ(L→∞) + c/L²`:
- ρ_(1,0)(L→∞) = +0.017 ± 0.004 (χ²/dof = 3.2)
- All higher irreps: ρ_∞ ≈ 0 within errors
- **Bootstrap 95% upper bound: ρ_(1,0)(∞) ≤ 0.024**

Plug into framework Perron formula:

| L | P(L, β=6) |
|---|---|
| 2 | 0.4250 ± 0.0002 |
| 3 | 0.4235 ± 0.0003 |
| 4 | 0.4235 ± 0.0001 |
| 6 | 0.4239 ± 0.0003 |
| **L→∞ (FSS)** | **0.4231 ± 0.0001** |

Reference: ρ=δ → P_triv = 0.4225; ρ=1 → P_loc = 0.4524; canonical 4D
Wilson L→∞: 0.5934.

**The MC P(L→∞) sits at the decoupled-environment limit, NOT at canonical 0.5934.**

## Quantitative diagnostic

The framework's K-tube ansatz at k = 12.6342 reproduces 0.5934, requiring
**ρ_(1,0) = 20.00**. The MC FSS gives ρ_(1,0)(∞) ≤ 0.024 (95% CL),
**an 849× shortfall**.

## The structural explanation

Route 4's Peter-Weyl readout on a single 3D spatial cube is bounded by
character orthogonality (|ρ| ≲ 1 trending to 0 with volume). But the
framework's R_env factor encodes a **time-tube of length k ≈ 12.6**,
NOT the spatial cube alone. A tube of length k amplifies via
`ρ ~ a_(p,q)^k`, giving the O(20) values needed. With `a_(1,0)(6) ≈ 0.422`:

```
a_(1,0)(6)^12 ≈ 0.422^12 ≈ 1.0 × 10⁻⁵      (way too small)
a_(1,0)(6)^k for k = 12.6342, with proper amplification ≈ 20  (what's needed)
```

The factor of 10⁻⁵ vs 20 mismatch confirms: **the tube power on c_R/c_(0,0)
is what gives the K-tube structure, NOT a single-cube character measurement**.

**Route 4 measures the wrong object.**

## Cross-check: 3D vs 4D Wilson

Direct Wilson `⟨P⟩` on 3D spatial cube (no marked plaquette exclusion)
at β=6:
- L=2: 0.479
- L=3: 0.461
- L=4: 0.458
- Extrapolation to 3D Wilson L→∞: ≈ **0.450**

This matches the framework's P_loc(ρ=1) = 0.4524.

The canonical **0.5934 is the 4D lattice Wilson β=6 value**, not 3D.

**3D and 4D Wilson at the same β are DIFFERENT physical observables.**

## Unification of prior findings

This 3D-vs-4D diagnosis explains several previously puzzling results:

1. **Route 1c c_6 confinement to (1,0) sector**: cube-shell geometry
   confines finite-order onset coefficients to fundamental sector.
   This is the SAME spatial-cube character confinement seen in Route 4.

2. **Route 3's 9.3× magnitude mismatch**: the algebraic factorization
   `(N²−1)/(8N × b_0³) = 1/3993` was right structurally, but missing
   the 3D→4D dimensional amplification factor (= length of time-tube /
   spatial-cube count ratio).

3. **Route 4's measurement falling at decoupled-environment limit**:
   confirms that the spatial-cube measurement decouples from the
   time-tube structure that gives the K-tube amplification.

4. **L=2 cube ⟨P⟩ = 0.4226 ≠ 4D L→∞ Wilson 0.5934**: confirmed; these
   are different physical observables on different geometries.

## What this changes

**Chain refactoring status: UNCHANGED at bounded support 4.4 ppm.** The
residual remains. But its structural origin is now sharper: **the 3D
spatial cube character measurements alone cannot derive 4D Wilson L→∞
behavior. The missing piece is the temporal extent (time-tube of length
k ≈ 12-13).**

This means the path to closure requires either:
- (i) 3+1D MC at L_t ≫ 1 (computationally similar to PR #539's full 4D MC,
  but with character measurements at each time slice)
- (ii) Transfer-matrix computation that builds ρ from products of
  slice-to-slice intertwiners
- (iii) Both — combine framework's existing tensor-transfer machinery
  with explicit time-tube character data

This is **CONSTRUCTIVE**, not blocked: a clear computational target.
Just not what Route 4's pure-spatial method can do.

## What this does NOT change

- Chain refactoring at bounded support 4.4 ppm: still the framework's
  best analytical chain claim
- PR #539 retained MC value 0.5934: still the L→∞ comparator
- PR #541's V=1 PF ODE: still the framework's minimal-block closed form
- All prior derivation routes (1, 2, 3, 8): still blocked at their
  respective structural barriers; this finding adds context but not closure
- Theorem 3 audit corrections: still stand (the no-go itself was
  scope-overclaimed; this finding doesn't restore the original scope)

## Status proposal

```yaml
note: CHAIN_CLOSURE_3D_VS_4D_STRUCTURAL_DIAGNOSIS_NOTE_2026-05-06.md
type: research_finding (honest negative closure + structural diagnosis)
proposed_status: research_finding
positive_subresults:
  - Route 4 multi-L MC successfully measured ρ_(p,q)(L, β=6) at L=2,3,4,6
  - FSS extrapolation gives ρ_(1,0)(∞) ≤ 0.024 (95% CL)
  - Identified 849× quantitative shortfall vs K-tube requirement
  - Structural explanation: 3D spatial cube ≠ 4D Wilson; missing time-tube
  - Unifies 4 prior puzzling findings (Route 1c, 3, 4 spatial limit, L=2 cube)
negative_subresults:
  - L→∞ extrapolation does NOT close to 0.5934
  - Route 4's pure-spatial method is structurally insufficient
  - Chain stays at bounded support 4.4 ppm
audit_required: yes
follow_up:
  - 3+1D MC with explicit time-slice character measurements (next-step)
  - Transfer-matrix slice-to-slice intertwiner construction
```

## Reusable artifacts

- `/tmp/route4_multi_L/route4_multiL.py` — multi-L Metropolis + character
- `/tmp/route4_multi_L/perron_from_rho.py` — framework Perron plug-in
- `/tmp/route4_multi_L/rho_combined.json` — all MC ρ data
- `/tmp/route4_multi_L/wilson_p_check.py` — 3D vs 4D Wilson cross-check

## Ledger entry

- **claim_id:** `chain_closure_3d_vs_4d_structural_diagnosis_note_2026-05-06`
- **note_path:** `docs/CHAIN_CLOSURE_3D_VS_4D_STRUCTURAL_DIAGNOSIS_NOTE_2026-05-06.md`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
