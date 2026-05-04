# SU(3) L_s=3 PBC Cube Haar Monte Carlo: Honest Negative Result

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — honest negative result, unaudited.
**Primary runner:** `scripts/frontier_su3_wigner_l3_cube_haar_mc_2026_05_04.py`
**Predecessor:** `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501).

## 0. Headline

Direct attempt to compute the L_s=3 PBC cube Wigner-Racah trace
`T_lambda(L=3 cube)` via Haar Monte Carlo. **Result: naive Haar MC does
not work.**

For 5000 Haar SU(3) samples on the L_s=3 PBC cube (81 directed links,
81 unique Wilson plaquettes), the integrand averages for nontrivial
irreps are at the same order as their MC standard error:

| irrep | `<integrand>` | MC ± error |
|---|---:|---:|
| (0,0) | `1.0` | `0` (exact) |
| (1,0) | `-6.3e-5` | `±5.9e-5` (within error of 0) |
| (1,1) | `9.5e-18` | `±8.0e-18` (within error of 0) |
| (2,0) | `3.5e-9` | `±4.1e-9` (within error of 0) |
| (2,1) | `1.17e+8` | `±1.25e+8` (within error of 0) |

All nontrivial integrand averages are **statistically indistinguishable
from zero** at N_samples = 5000. The resulting source-sector Perron
solve gives `P_cube(L=3 PBC, MC) = 0.108`, dominated by random noise in
the rho values (some negative, which is unphysical for a probability
density).

The gap to the bridge-support target `0.5935` is `0.486 = 1604×
ε_witness`, **larger** than at L_s=2.

## 1. Why naive Haar MC fails here

### 1.1 Integrand magnitude

For random Haar SU(3) link variables, `chi_(1,1)(U_p) = |tr(U_p)|^2 - 1`
has mean zero (Schur orthogonality on the Cartan torus). Each plaquette
character is centered around 0 with `O(1)` variance.

The integrand is the PRODUCT of 81 such near-zero quantities:
```text
integrand = ∏_(p=1)^81 chi_(1,1)(U_p)
```

For 81 independent random Gaussian-like variables with mean 0 and
variance 1, the product has mean 0 and a wide bimodal-tailed
distribution. The MC sample mean fluctuates around 0 with standard
error ~ stddev / sqrt(N).

### 1.2 Resolving a value of order 10^(-100)

After dividing by the irrep-dimension factor `1 / d_lambda^81 = 1 / 8^81
~ 1.2e-73`, the relevant scale of `T_(1,1)(L=3 cube)` is approximately
`1e-100` or below.

To resolve `T_(1,1) ~ 1e-100` above MC noise (variance ~ 1 per sample),
we'd need `N_samples ~ (1 / 1e-100)^2 = 1e+200` samples. Infeasible by
~150 orders of magnitude.

### 1.3 What this means

The Haar MC approach is **not just slow at L_s=3 — it is structurally
the wrong tool**. The integrand is exponentially small in the lattice
volume (each plaquette factor is `O(1)` random with mean 0, and 81
multiplied together give a value at the bottom of double-precision
representable range), and direct sampling cannot resolve the result.

This is a manifestation of the **sign problem** common in lattice gauge
Monte Carlo with non-Boltzmann weighting: the integrand has
+/- contributions that cancel, and the variance grows exponentially
with system size while the signal does not.

## 2. What this rules out

This negative result, combined with Block 5's L_s=2 verdict, establishes:

| Approach | Status |
|---|---|
| L_s=2 PBC, candidate ansatz | gives `P = 0.4291`, gap `543× ε_w` (Block 5) |
| L_s=2 PBC, standard Wilson | structural degeneracies (Block 5) |
| L_s=3 PBC, Haar MC | **MC noise dominates, no signal** (this note) |
| Single-plaquette character | gives `0.4225`, gap `564× ε_w` (PR #503) |
| Strong-coupling β/(2N²) | gives `0.333`, gap `858× ε_w` (PR #503) |
| Mean-field self-consistent | gives `0.874`, gap `926× ε_w` (PR #503) |
| Weak-coupling 1-loop | gives `0.926`, gap `1097× ε_w` (PR #503) |

**Remaining viable route:** exact L_s ≥ 3 tensor-network contraction
of the Wigner-Racah cube trace. This requires:
- Memory-aware contraction-order optimization (greedy or
  graph-partitioning-based);
- Worst-case intermediate at `8^9 ~ 2 GB` per Block 4 scope analysis;
- An industrial tensor-network library (opt_einsum or ncon — neither
  in `numpy + scipy` only environment) OR a hand-rolled custom
  contractor;
- Multi-day to multi-week engineering effort.

## 3. Why importance sampling doesn't escape

The natural fix for sign-problem MC is **importance sampling**:
re-weight by Wilson Boltzmann `exp(β/N Σ_p Re tr U_p)` and sample from
the importance distribution. But this turns the computation into
**standard lattice Wilson Monte Carlo**, which:

- Imports `<P>(β=6) ≈ 0.5934` as the comparator value rather than
  deriving it;
- Violates the framework's forbidden-import policy (no MC plaquette
  values as derivation inputs);
- Reduces the framework's contribution to "we used standard lattice MC
  to compute <P>", which is not a derivation.

This is a deliberate methodological choice: the framework demands
`<P>(β=6)` from primitives, not from the importance-sampled MC that
"already knows" the answer.

## 4. Theorem statement

**Bounded theorem (L_s=3 cube Haar MC negative result).** The runner
`scripts/frontier_su3_wigner_l3_cube_haar_mc_2026_05_04.py` performs
N_samples = 5000 Haar Monte Carlo samples on the L_s=3 PBC cube (81
unique Wilson plaquettes, 81 directed links) and evaluates the
integrand `∏_p chi_lambda(U_p)` for `lambda ∈ {(0,0), (1,0), (0,1),
(1,1), (2,0), (0,2), (2,1)}`. For all nontrivial irreps, the MC mean
is statistically indistinguishable from zero (within ±1 standard
error). The induced source-sector Perron value is `P_cube(L=3 PBC, MC)
= 0.108`, dominated by MC noise; gap to bridge target is `0.486 =
1604× ε_witness`.

Naive Haar MC at L_s=3 cannot resolve `T_lambda(L=3 cube)` for
nontrivial `lambda`: the integrand's product structure across 81
plaquettes drives its expected magnitude below `~ 1e-100`, which
requires `~ 1e+200` samples to resolve above MC variance — infeasible
by ~150 orders of magnitude.

## 5. Scope

### 5.1 In scope

- Direct Haar MC of T_lambda(L=3 cube) at N_samples = 5000.
- Honest documentation of MC failure mode (sign-problem-like variance).
- Verdict: importance sampling is forbidden (would import MC value);
  exact tensor-network contraction remains the only viable route.

### 5.2 Out of scope

- Tensor-network contraction with memory-aware optimizer (multi-day
  engineering, future PR).
- Importance-sampled lattice MC (forbidden by no-imports policy).
- Closure of the gauge-scalar bridge.

### 5.3 Not making the following claims

- Does NOT promote the gauge-scalar bridge parent theorem.
- Does NOT claim P_cube(L=3) = 0.108 as a derived value (it's MC noise,
  not signal).
- Does NOT use forbidden imports: the MC value 0.5934 is comparator
  only.

## 6. Audit consequence

```yaml
claim_id: su3_wigner_l3_cube_haar_mc_negative_result_2026-05-04
note_path: docs/SU3_WIGNER_L3_CUBE_HAAR_MC_NEGATIVE_RESULT_2026-05-04.md
runner_path: scripts/frontier_su3_wigner_l3_cube_haar_mc_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03  # PR #501
  - su3_wilson_closed_form_fanout_theorem_note_2026-05-04         # PR #503
verdict_rationale_template: |
  Bounded support theorem documenting honest negative result of naive
  Haar MC for T_lambda(L=3 PBC cube). At N=5000, all nontrivial integrand
  averages are statistically indistinguishable from zero (within MC
  standard error). Resulting source-sector Perron solve gives
  P_cube(L=3 PBC, MC) = 0.108 with gap 0.486 = 1604x epsilon_witness.

  Failure mode is sign-problem-like: integrand product across 81
  plaquettes has expected magnitude ~ 1e-100 against MC variance ~ 1
  per sample, requiring infeasibly many samples (~ 1e+200) to resolve.

  Importance sampling is forbidden (would import the MC plaquette
  value as comparator). Exact tensor-network contraction at L_s>=3
  remains the only viable route, requiring memory-aware optimizer +
  multi-day engineering.

  This negative result strengthens Block 5's verdict by ruling out
  the "just throw MC at it" path. Combined with the closed-form
  fan-out (PR #503), the campaign now has explicit ruling-out of:
  L_s=2 (intrinsic small-volume), 4 closed-form approximations, and
  Haar MC.

  Does not promote bridge parent chain. No forbidden imports.
```

## 7. Cross-references

- Block 5 (L_s=2 verdict): `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501).
- Closed-form fan-out: `docs/SU3_WILSON_CLOSED_FORM_FANOUT_THEOREM_NOTE_2026-05-04.md` (PR #503).
- Bridge no-go: `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`.
- Block 4 scope analysis (motivating tensor-network contraction route): same as PR #501.

## 8. Command

```bash
python3 scripts/frontier_su3_wigner_l3_cube_haar_mc_2026_05_04.py
```

Expected runtime: ~20 seconds. Expected summary:

```text
SUMMARY: THEOREM PASS=1 SUPPORT=1 FAIL=0
```

with headline showing P_cube(L=3 PBC, MC) ~ 0.1 (MC noise) and gap ~
0.49 = 1604x epsilon_witness.
