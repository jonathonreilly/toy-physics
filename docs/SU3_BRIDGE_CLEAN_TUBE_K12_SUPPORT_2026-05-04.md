# SU(3) Bridge Clean-Tube k=12 Support Calculation: ρ = (c/c_00)^12 → P = 0.5888

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support calculation, unaudited.
**Primary runner:** `scripts/frontier_su3_bridge_rho_modification_scoping_2026_05_04.py`

## 0. Headline

This note evaluates a clean tube-power support calculation for `<P>(β=6)`:

```text
ρ_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^12
```

This is the **K-plaquette tube formula at k=12** (already in the framework's staging gate K-tube probe at k=0..6, just never extended to k=12). It uses NO dimensional factors and NO Haar-pairing topological corrections — purely the per-plaquette character coefficient ratio raised to the 12-plaquette power.

**Result:**

```text
P_cube(L_s=2 APBC, β=6, ρ = (c/c_00)^12) = 0.5887944343
                                    target = 0.5934
                                       gap = 0.0046 = 15× ε_witness
                                  fractional gap = 0.78%
```

The support value is within **0.78%** of the canonical MC comparator
`0.5934`, but it still misses by `15× ε_witness`. This is useful
near-miss structure, not a closure theorem.

The remaining 0.78% gap is numerically of the same order as some
perturbative correction scales, but this note does not derive or
identify such a correction. Any correction term would be new science.

## 1. The clean formula

For the L_s=2 APBC cube with 12 plaquettes:

```text
ρ_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^12
```

where `c_(p,q)(β)` is the Wilson character coefficient via Bessel determinant (existing framework primitive, no imports):

```text
c_(p,q)(β) = sum_(n ∈ Z) det[I_(n + λ_j + i - j)(β/3)]_(i,j=1..3)
```

with `λ = (p+q, q, 0)`. Computed for β=6 with mode_max=200.

**Top ρ values:**

| (p,q) | ρ_(p,q)(6) |
|---|---:|
| (0,0) | 1.000000 |
| (1,1) | 22.888 |
| (1,0) | 17.209 |
| (0,1) | 17.209 |
| (2,0) | 0.0869 |
| (0,2) | 0.0869 |
| (1,2) | 0.0209 |
| (2,1) | 0.0209 |

Notice these ρ values are LARGE (>>1) — the framework's previous candidate (`d^(-16)` factor) was suppressing them by ~10⁴×, which explains why P came out at 0.4291 instead of 0.5888.

## 2. Comparison to prior candidates

| Ansatz | Formula | P(6) | Gap to MC | Gap × ε_witness |
|---|---|---:|---:|---:|
| Trivial (Reference B) | ρ = δ_(0,0) | 0.4225 | 0.171 | 564× |
| Local (Reference A) | ρ = 1 | 0.4524 | 0.141 | 466× |
| Index-graph candidate | (d c/c_00)^12 × d^(-16) | 0.4291 | 0.164 | **543×** |
| K-tube k=6 (max in staging) | (c/c_00)^6 | 0.5158 | 0.078 | 256× |
| **K-tube k=12 (this PR)** | **(c/c_00)^12** | **0.5888** | **0.0046** | **15×** |
| MC reference | (canonical) | 0.5934 | 0 | 0× |

**This PR's clean formula is 36× closer than the prior candidate ansatz.**

## 3. Physical interpretation

The candidate ansatz (`d^(-16)`) assumed Haar pairing on shared cyclic indices: each link integration `∫dU D[a,b] D[c,d] = (1/d) δ δ` contributes a `1/d` factor, with 24 such factors compensated by 8 surviving cyclic-index components: total `d^(-24+8) = d^(-16)`.

The clean formula `(c/c_00)^12` assumes the unmarked plaquettes contribute INDEPENDENTLY to ρ — no shared-index pairing, just the 12-fold product of the leading per-plaquette character ratio.

These represent two different physical pictures:
- **Haar pairing** (d^(-16)): unmarked plaquettes are GAUGE-CONNECTED via shared link variables; integration produces δ identifications.
- **Independent product** ((c/c_00)^12): unmarked plaquettes contribute as independent character samples to the boundary measure.

The fact that the **independent product** lands closer to the MC
comparator than the Haar-pairing candidate is useful scoping evidence.
It does not by itself establish that the framework's source-sector
factorization is the independent-product picture.

## 4. The remaining 0.78% gap

```text
P_clean = 0.5888
P_MC    = 0.5934
gap     = 0.0046 = 0.78% of MC
        = 15× ε_witness (= 3.03e-4)
```

For SU(3) at β=6, the typical 1-loop perturbative correction scale is:

```text
g²/(N²β) ~ 1/(N²β) = 1/(9 × 6) ≈ 1.85%
α_s/π ~ 0.5/π = 0.16  (too large by factor ~ 20)
1/(2N²β) ≈ 0.93%
```

The 0.78% gap is in the range of some perturbative scales, but this
calculation does not identify the missing term. Treat any proposed
1-loop, tadpole, marked/unmarked, or larger-cube correction as an open
science item until it has its own derivation and runner.

### 4.1 Review disposition of closed target-fit branches

The closed `12 + 2/pi` branches are preserved as review context, not as
source authority:

- the numerical beta=6 match from the `12 + 2/pi` exponent is real as a
  target-fit calculation, but the correction is not derived here;
- the beta-dependence check showed the same `2/pi` correction is not a
  universal beta-family law;
- the proposed `(N^2 - 1)/(4 pi)` interpretation imports an unproved
  correction term and does not supply the source-sector derivation;
- the Schur-vs-K-tube comparison remains a real tension: the landed full-rho
  Schur calculation gives `0.4291`, while the independent-product K-tube
  support calculation gives `0.5888`.

The durable theorem boundary is therefore exactly the one stated in this
note: k=12 is a strong bounded near-miss, and the residual correction remains
open science until derived from repo primitives with a load-bearing runner.

## 5. NMAX convergence

Stable to 12 decimal places across NMAX_rho ∈ {2..8}:

```text
NMAX_rho = 2: P = 0.5887944343
NMAX_rho = 3: P = 0.5887944343
NMAX_rho = 4: P = 0.5887944343
NMAX_rho = 5: P = 0.5887944343
NMAX_rho = 6: P = 0.5887944343
NMAX_rho = 7: P = 0.5887944343
NMAX_rho = 8: P = 0.5887944343
```

The Perron value is fully converged at NMAX_rho ≥ 2. The 0.78% gap is **not a truncation artifact**.

## 6. Theorem statement

**Bounded theorem (clean tube formula at k=12).** The candidate
boundary character measure

```text
ρ_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^12
```

evaluated via Wilson character coefficients (existing framework
primitive) and plugged into the source-sector factorization Perron
solve gives

```text
P_cube(L_s=2 APBC, β=6) = 0.5887944343
```

stable to 12 decimal places across NMAX_rho ∈ {2..8}. The gap to the
canonical MC comparator value `0.5934` is `0.0046 = 0.78%` of the MC
value, equivalent to `15× ε_witness`.

This formula uses NO dimensional factors and NO Haar-pairing
topological corrections — purely the K-plaquette tube formula at the
natural cube size k=12 (vs k=0..6 in the framework's existing staging
gate K-tube probe). It is computed from existing framework primitives
(Bessel-determinant character coefficients).

The remaining 0.78% gap is unresolved. This note does not identify a
derived correction that closes to ε_witness.

## 7. Open residual routes

To close the remaining 0.78% gap from `0.5888` to `0.5934`:

1. **Identify 1-loop correction**: derive the per-plaquette 1-loop correction from existing framework primitives (Wilson β-function jet, tadpole coefficient, link-coupling).
2. **Refine the K-tube extrapolation**: investigate whether the K-tube formula has additional corrections at k=12 (vs k=0..6 where the framework already uses it).
3. **Marked-vs-unmarked structure**: properly account for the framework's "1 marked + 5 unmarked" specification — the existing K-tube uses uniform k, but the actual cube may have differential marked/unmarked treatment.
4. **NMAX_perron beyond 7**: although NMAX_rho is converged, NMAX_perron (= 7 in the existing source-sector solve) may have a small residual.

These are open follow-up routes, not conclusions of this note.

## 8. Scope

### 8.1 In scope

- The clean formula `ρ_(p,q)(6) = (c/c_00)^12`.
- Verification that this gives P = 0.5888 (within 0.78% of MC).
- Comparison to prior ansätze (candidate, K-tube, references).
- Identification of the residual correction as open science.

### 8.2 Out of scope

- Deriving the 1-loop correction itself (deferred to follow-up PR).
- Closing the bridge to ε_witness.
- Marked-vs-unmarked structural analysis (deferred).

### 8.3 Not making the following claims

- Does NOT promote bridge parent chain.
- Does NOT close the bridge to ε_witness.
- Does NOT claim 0.5888 IS the MC value.
- Uses MC value 0.5934 ONLY as comparator (not derivation input).

## 9. Audit consequence

```yaml
claim_id: su3_bridge_clean_tube_k12_support_2026-05-04
note_path: docs/SU3_BRIDGE_CLEAN_TUBE_K12_SUPPORT_2026-05-04.md
runner_path: scripts/frontier_su3_bridge_rho_modification_scoping_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_cube_full_rho_perron_2026-05-04
verdict_rationale_template: |
  Bounded support calculation for <P>(beta=6) from existing framework
  primitives. Clean formula rho_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^12
  (= K-plaquette tube at k=12, already in framework's staging gate
  K-tube probe at k=0..6) gives P = 0.5888 via source-sector Perron
  solve. Gap to MC comparator 0.5934 is 0.0046 = 0.78% = 15× ε_witness.

  This is dramatically closer than the prior candidate ansatz
  (P = 0.4291, gap 543× ε_witness). The d^(-16) Haar-pairing factor
  in the candidate was over-suppressing rho.

  Physical interpretation: unmarked plaquettes contribute as
  INDEPENDENT character samples to the boundary measure (consistent
  with the source-sector formula's diagonal C_env structure), not as
  Haar-paired joint integration.

  Remaining 0.78% gap is unresolved; this note does not derive a
  correction that closes to epsilon_witness.

  Stable to 12 decimal places across NMAX_rho 2..8.

  Does not promote bridge parent chain. Does not close to ε_witness.
  No forbidden imports.
```

## 10. Cross-references

- Campaign context, not a load-bearing dependency:
  `SU3_BRIDGE_CAMPAIGN_SALVAGE_2026-05-04.md`.
- Counterfactual context, not a load-bearing dependency:
  `SU3_BRIDGE_COUNTERFACTUAL_PASS_2026-05-04.md`.
- Full-ρ Perron:
  [`SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md`](SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md).
- Block 5 (verified candidate):
  [`SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md).
- Native staging gate (K-tube source): `docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`

## 11. Commands

```bash
python3 scripts/frontier_su3_bridge_rho_modification_scoping_2026_05_04.py
```

Expected outputs:
- ρ-modification scoping: `SUMMARY: THEOREM PASS=2 SUPPORT=2 FAIL=0` with M2 finding (N=12 → P = 0.5888).
