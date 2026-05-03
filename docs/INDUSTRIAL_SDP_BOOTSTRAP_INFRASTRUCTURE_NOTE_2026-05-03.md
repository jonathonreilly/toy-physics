# Industrial SDP Bootstrap — Infrastructure + SU(2)/SU(3) Single-Plaquette Validation

**Date:** 2026-05-03
**Type:** infrastructure + validation support theorem
**Claim scope:** establish a working CVXPY-based moment-problem SDP
infrastructure for lattice gauge bootstrap on this framework, validated
on SU(2) and SU(3) single-plaquette reference data via Bessel functions
and numerical Haar integration on the Cartan torus. The infrastructure is
unblocked by infra PR
[#430](https://github.com/jonathonreilly/cl3-lattice-framework/pull/430)
which added cvxpy 1.8.2 + open-source SDP solvers via venv. The
infrastructure provides the foundation for actual lattice bracketing of
`⟨P⟩(β=6)` (block 02 of this campaign).
**Status authority:** independent audit lane only.
**Primary runner:** `scripts/frontier_industrial_sdp_bootstrap_block01.py`
**Run with:** `.venv/bin/python3 scripts/frontier_industrial_sdp_bootstrap_block01.py`

## 0. Question

Can CVXPY (now installed via venv per PR #430) actually produce useful
SDP-based brackets on plaquette moments for SU(N) lattice gauge theory?
Validation requires comparing CVXPY brackets to known reference values
(single-plaquette via Bessel for SU(2), Haar integration for SU(3)).

## 1. Setup

CVXPY 1.8.2 + open-source solvers (CLARABEL, SCS, HIGHS, OSQP, SCIPY).
No commercial Mosek (industrial Kazakov-Zheng-class precision out of
reach without it).

Three primitives implemented:

| # | Primitive | Description |
|---|---|---|
| BS1 | SU(2) single-plaquette moments via Bessel + numerical Haar | `⟨((1/2) tr U)^k⟩_single` for k ∈ {0,1,2,3,4} from numerical integration of `∫dθ sin²(θ/2) cos^k(θ/2) exp(β cos(θ/2)) dθ` over θ ∈ [0, π] |
| BS2 | SU(3) single-plaquette moments via Cartan-torus Haar integration | `⟨((1/3) Re tr U)^k⟩_single` from 2D grid integration over Weyl chamber with Vandermonde measure |
| BS3 | CVXPY moment-problem bootstrap | Hankel-PSD + Hausdorff-shifted-PSD on `[a, b]`-supported moment sequences; max/min `m_1 = ⟨P⟩` subject to PSD constraints; supports fixing higher moments to known reference values |

## 2. Validation results

At `β = 6`:

### SU(2) single-plaquette (Bessel/Haar reference)

```text
⟨P^0⟩_SU(2)_single = 1.00000000  (normalization)
⟨P^1⟩_SU(2)_single = 0.76736480  (Bessel-style: I_2(β)/I_1(β) variant)
⟨P^2⟩_SU(2)_single = 0.62153293
⟨P^3⟩_SU(2)_single = 0.51967618
⟨P^4⟩_SU(2)_single = 0.44425771
```

CVXPY bracket with `m_2, m_3, m_4` fixed to reference, `m_1` free:
`m_1 ∈ [0.684871, 0.769227]` — width 0.084, contains reference 0.767.

### SU(3) single-plaquette (Haar reference, 80×80 grid)

```text
⟨P^0⟩_SU(3)_single = 1.00000000
⟨P^1⟩_SU(3)_single = 0.42253174
⟨P^2⟩_SU(3)_single = 0.24341355
⟨P^3⟩_SU(3)_single = 0.14974607
⟨P^4⟩_SU(3)_single = 0.09939457
```

CVXPY bracket: `m_1 ∈ [0.281915, 0.451550]` — width 0.170, contains
reference 0.4225.

### Pure PSD bracket (no fixed moments)

For SU(N) with `P ∈ [a, b]` support but no other constraints:
- SU(2) (`P ∈ [-1, 1]`): `m_1 ∈ [-1.00, 1.00]` — trivial (full support)
- SU(3) (`P ∈ [-1/3, 1]`): `m_1 ∈ [-0.333, 1.000]` — trivial (full support)

PSD + Hausdorff alone gives only the support endpoints. **Loop equations
or higher-moment constraints are required for non-trivial brackets.**

## 3. Connection to lattice ⟨P⟩(β=6)

The single-plaquette reference values are:
- SU(2)_single ≈ 0.767 (vs lattice MC ≈ 0.770 at the SU(2) Wilson convention)
- SU(3)_single ≈ 0.422 (vs lattice MC = **0.5934** at the framework's β=6)

The SU(3) single-plaquette gap to lattice MC (~30% relative) reflects the
**mean-field deficiency**: in lattice gauge theory, plaquettes share
links and the correlations among plaquettes raise `⟨P⟩` substantially
above the single-plaquette mean-field value.

**Block 02 of this campaign** will attempt to bracket the FULL LATTICE
`⟨P⟩(β=6)` using:
- CVXPY moment bootstrap on a multi-Wilson-loop set
- Loop equations (Schwinger-Dyson on framework's V-invariant minimal block) or
- Framework's mixed-cumulant audit (`P_full(β) = P_1plaq(β) + β^5/472392 + O(β^6)`) as
  a soft constraint

## 4. What this note closes

- **CVXPY-based SDP infrastructure** for moment-problem bootstrap is
  validated and working on this framework.
- SU(2) and SU(3) single-plaquette references computed analytically/numerically.
- CVXPY brackets recover known reference values when higher moments are fixed.
- Pure PSD brackets without loop equations are demonstrated to be trivial
  (just support endpoints).

## 5. What this note does NOT close

- Lattice ⟨P⟩(β=6) bracket (deferred to block 02).
- Industrial-precision (Kazakov-Zheng 2022 ~10⁻²) brackets (require Mosek
  + ~3-month engineering; out of scope of this 12h campaign).
- Loop-equation derivation on framework's V-invariant minimal block (deferred).

## 6. Honest status

```yaml
actual_current_surface_status: infrastructure validation support theorem
target_claim_type: positive_theorem (infrastructure works)
conditional_surface_status: bounded by the open lattice ⟨P⟩(β=6) target
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  This is an infrastructure/methodology cycle: it establishes that
  CVXPY-based SDP moment-bootstrap is functional and correctly recovers
  reference values when higher moments are constrained. It does NOT
  bracket the lattice ⟨P⟩(β=6) target on its own; that requires loop
  equations (block 02).
audit_required_before_effective_retained: true
bare_retained_allowed: false
proposal_allowed: false
proposal_allowed_reason: |
  Infrastructure validation cycle. The retained-positive value comes
  in block 02 where the infrastructure is applied to the actual lattice
  target.
```

## 7. Comparators (admitted-context only)

- Canonical lattice MC SU(3) `⟨P⟩(β=6)` = **0.5934**
  (`PLAQUETTE_SELF_CONSISTENCY_NOTE`)
- Bridge-support analytic upper-bound candidate = **0.59353**
- SU(2) lattice MC at β=6 ≈ 0.7706 (Creutz 1980)
- Kazakov-Zheng 2022 SU(∞) bracket near λ≈1.35: `[0.59, 0.61]` at L_max=16
  ([arXiv:2203.11360](https://arxiv.org/abs/2203.11360))
- Kazakov-Zheng 2024 SU(2) finite-N: 0.1% precision in physical range
  ([arXiv:2404.16925](https://arxiv.org/abs/2404.16925))

## 8. Cross-references

- Infra unblocker: PR [#430](https://github.com/jonathonreilly/cl3-lattice-framework/pull/430) (cvxpy + venv setup)
- Verdict-named obstruction: [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- Prior bootstrap framework integration (analytical small-truncation): PR [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420), PR [#423](https://github.com/jonathonreilly/cl3-lattice-framework/pull/423)
- Block 02 (planned, this campaign): apply CVXPY to lattice ⟨P⟩(β=6)
- Loop pack: `.claude/science/physics-loops/industrial-sdp-bootstrap-20260503/`
