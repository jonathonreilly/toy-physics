# Gauge-Scalar Bridge 3+1 Native Lower-Bound Staging Note

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** retained_bounded — staging note for the L_s=2 APBC spatial
cube tensor-transfer Perron solve (the explicit "out of scope" gap from
[`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)).
This note ASSEMBLES, on the V-invariant minimal block, the K-plaquette
TUBE physical-environment Perron data at `beta_env = 6` from the existing
framework primitives, reports super-polynomial NMAX convergence, and
identifies the precise closure target: explicit ρ_(p,q)(6) for the
unmarked spatial cube (5 plaquettes in a fixed L_s=2 APBC geometry).
**Primary runner:** `scripts/frontier_gauge_scalar_bridge_3plus1_native_lower_bound.py`
**Companion lift:** [`GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md)
(PR #484; K-Z external lift, conservative `W_lift = 0.05`).
**Bypass target context:** [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md).

## 0. Headline

This is a STAGING note, not a closure note. It does not derive a new
strict lower bound on `<P>(beta=6)` beyond the framework's existing
trivial floor `P_triv(6) = 0.4225` (rho = delta reference). It does:

1. Compile, on the V-invariant minimal block at NMAX = 7, the
   K-plaquette TUBE family Perron values at `beta_env = 6` for
   `k = 0..6`, exhibiting monotonic increase from `0.4524` (k = 0,
   Reference A) to `0.5158` (k = 6).
2. Verify super-polynomial NMAX truncation convergence
   (drift `|P(NMAX=7) - P(NMAX=6)| = 1.3e-9` at k = 1).
3. Frame the explicit closure target: the L_s = 2 APBC spatial cube has
   5 unmarked plaquettes in a SPECIFIC GEOMETRIC arrangement, NOT a
   tube; the cube's physical ρ_(p,q)(6) sequence and its Perron
   eigenvalue is the `out of scope` item from the spatial-environment
   tensor-transfer theorem.
4. Honestly compare to PR #484's K-Z external lift: the native
   framework bracket is currently WIDER (0.141 vs 0.05).

The runner does NOT solve the L_s = 2 cube Perron problem. It assembles
the framework infrastructure and stages the next computational step.

## 1. Cited framework primitives carried forward

This note depends on, and respects the scope boundaries of, the
following retained framework primitives:

- [`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md):
  retained_bounded; the kernel-level temporal completion law
  `K_O(omega) = 3w(3 + sin^2 omega)` with `A_inf / A_2 = 2/sqrt(3)`
  exact on the V-invariant minimal `3 spatial + 1 derived-time` block
  with APBC `L_s = 2`.
- [`GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md):
  exact source-sector factorization
  `T_src(6) = exp(3J) D_6^loc C_(Z_6^env) exp(3J)`, with `D_6^loc`
  fully explicit from `c_lambda(6)` Bessel-determinant data and
  `C_(Z_6^env)` the open spatial-environment boundary character measure.
- [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md):
  support; explicit Perron solves at structural reference choices
  `rho = 1` (P_loc = 0.4524) and `rho = delta` (P_triv = 0.4225); plus
  the no-go theorem (Theorem 3) that `c_lambda(6)` and SU(3)
  intertwiners alone do NOT determine the physical
  `rho_(p,q)(6)`. Combined admissible span: `[0.4225, 0.6163]`.
- [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md):
  positive_theorem; identifies the spatial-environment boundary data as
  the Perron state of an explicit positive tensor-transfer operator
  built from `c_lambda(6)` and SU(3) intertwiner data. The full
  evaluation at `beta = 6` is explicitly OUT OF SCOPE in that note.
- [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md):
  retained_bounded; first nonlocal coefficient `+ beta^5 / 472392`,
  giving `beta_eff(beta) = beta + beta^5/26244 + O(beta^6)` onset.
- [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md):
  positive_theorem; rules out the constant-lift ansatz as the EXACT
  reduction law (slope mismatch `Gamma = 1` forced) but the candidate
  `0.59353` survives as an analytic upper-bound CANDIDATE.

## 2. Forbidden imports preserved

Per the [`GAUGE_SCALAR_TEMPORAL_OBSTRUCTION_BRIDGE_STRETCH_NOTE_2026-05-02.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md)
section 2 list:

- no PDG `<P>`
- no MC `<P>(beta=6)` as derivation input (only as audit comparator)
- no fitted `beta_eff`
- no perturbative beta-function expansion as derivation
- no same-surface family arguments

The runner explicitly avoids all five. The single-plaquette Cartan-torus
Haar reference and the Bessel-determinant Wilson character coefficients
are framework-internal computations of the local Wilson source response,
not measurements.

## 3. Computational result on the V-invariant minimal block

### 3.1 K-plaquette TUBE physical environment Perron values

For `k = 0..6` and the parameterization
`rho_k = (c_(p,q)(6) / c_(0,0)(6))^k` (one-plaquette physical environment
at `beta_env = 6` iterated `k` times):

| k | P(6) | Perron eigenvalue |
|---|---|---|
| 0 | 0.4524071590 | 3.812630 |
| 1 | 0.4594237929 | 3.915306 |
| 2 | 0.4678430800 | 4.047790 |
| 3 | 0.4777615094 | 4.219099 |
| 4 | 0.4891802187 | 4.441077 |
| 5 | 0.5019552672 | 4.729211 |
| 6 | 0.5157590249 | 5.103608 |

Tube family span over `k = 0..6`: `0.0634`.

These values are inside the framework's existing combined admissible
span `[0.4225, 0.6163]` (per the no-go's Theorem 3) and saturate only a
subset of it: the tube parameterization with `beta_env = 6` does not
reach the lower endpoint `0.4225` (which requires `rho = delta`,
the decoupled environment) nor the upper endpoint `0.6163` (which
requires high-power tube `k = 20`).

### 3.2 NMAX truncation convergence

At `k = 1` (single-plaquette physical environment at `beta_env = 6`):

| NMAX | P(6) |
|---|---|
| 3 | 0.459032827025 |
| 4 | 0.459414804723 |
| 5 | 0.459423660967 |
| 6 | 0.459423791566 |
| 7 | 0.459423792895 |

Truncation drift `|P(NMAX=7) - P(NMAX=6)| = 1.329e-9`, super-polynomial
in NMAX as expected from the Bessel-determinant decay of `c_(p,q)(beta)`.

### 3.3 Native framework-internal bracket

| Bound | Value | Source |
|---|---|---|
| Lower (trivial floor) | 0.4225 | Reference Perron solve B (`rho = delta`); not physical (decoupled env) but admissible |
| Lower (Reference A) | 0.4524 | Reference Perron solve A (`rho = 1`); structural input, not physical |
| Lower (k=1 tube) | 0.4594 | One-plaquette physical env at `beta_env = 6`; admissible parameterization |
| Lower (k=6 tube) | 0.5158 | Iterated tube; admissible parameterization |
| Upper | 0.59353 | Constant-lift candidate (ruled out as exact, retained as upper bound) |

The framework cannot currently derive a STRICT lower bound tighter than
`0.4225` (the trivial admissible-rho minimum) without computing the
physical L_s=2 cube ρ_(p,q)(6) directly. The K-plaquette tube values
are admissible parameterizations but are not proven to lower-bound the
physical cube's P(6).

Conservative native framework bracket:
```text
<P>(6) in [0.4225, 0.59353],   W_native = 0.1411.
```

## 4. Comparison to PR #484 K-Z external lift

| Source | Width | Status |
|---|---|---|
| PR #484 K-Z external lift (CONSERVATIVE) | 0.0500 | retained_bounded; load-bearing external authority |
| Native framework structural bracket (this note) | 0.1411 | retained_bounded; framework-internal admissible-rho span |
| Difference (PR #484 narrower than this) | factor 2.82x | K-Z external lift is currently the load-bearing tighter input |

The PR #484 conservative K-Z external lift `W_lift = 0.05` remains the
load-bearing TIGHTER input for the parent
[`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
observable-level scope. This staging note does not displace it.

## 5. Witness comparison (no-go Lemma 2)

```text
epsilon_witness = Var(P) * delta_beta_eff
                = 0.0649 * 0.0046656
                = 3.03e-4
```

Comparison:

```text
W_native (this note)        = 0.1411   (factor 470x above epsilon_witness)
W_lift   (PR #484 K-Z)      = 0.0500   (factor 165x above epsilon_witness)
W_target (witness closure)  = 3.03e-4
```

Both the native framework bracket and the K-Z external lift are above
`epsilon_witness`. Honest Path A applies; the no-go's structural
impossibility is bypassed via PR #484, but the witness construction is
not quantitatively closed by either the K-Z lift or the native framework
bracket at the current state.

## 6. Closure target: L_s = 2 APBC spatial cube tensor-transfer Perron solve

The remaining computational gap is precise:

> Compute the explicit `rho_(p,q)(6)` sequence for the unmarked
> 3 spatial Wilson environment on the L_s = 2 APBC spatial cube with
> marked-plaquette boundary, using:
>
> - exact Wilson character coefficients `c_(p,q)(6)` from Bessel
>   determinants (already implemented),
> - exact SU(3) fusion intertwiner multiplicities (already
>   implemented),
> - the explicit cube geometry (8 sites, 6 unique unoriented spatial
>   plaquettes after L=2 PBC degeneracy, 1 marked + 5 unmarked).

The result would be a single derived `rho_(p,q)(6)` sequence from
framework primitives alone, giving the EXACT P(6) on the V-invariant
minimal block. Combined with the temporal completion law, this would
fully close the observable-level bridge and quantitatively bypass the
no-go (provided the resulting bracket has width below
`epsilon_witness ≈ 3e-4`).

### 6.1 Computational scope estimate

The computation is finite-dimensional:
- 6 unique unoriented spatial plaquettes (1 marked + 5 unmarked)
- 12 unique unoriented spatial links (4 on marked-plaquette boundary; 8 free)
- For each unmarked plaquette, character-expand into ≤ NMAX = 7 dominant
  weights → at most `8^5 = 32768` non-trivially-irreducible
  configurations (most vanish by Haar selection rules)
- Effective number of nonzero terms after selection rules: estimated
  `~10^3` configurations, each requiring an SU(3) Wigner intertwiner
  trace lookup

Memory: well within commodity hardware. Runtime: minutes-hours (in
Python; seconds-minutes in optimized C).

### 6.2 Expected outcome

If the L_s = 2 cube Perron solve gives `P_cube(6)` within `~3e-4` of
either bound `[0.4225, 0.59353]`, the no-go closes quantitatively
(Honest Path B). Given the framework's strong-coupling local floor of
`0.4225` and the bridge-support upper bound of `0.59353`, with the K-Z
external lift suggesting the true value is near `0.59` (consistent with
MC `0.5934`), the L_s = 2 cube result is expected to be near `0.5-0.6`,
well inside the admissible span.

## 7. What this note establishes

```yaml
new_perron_data:
  - K-plaquette TUBE family at beta_env = 6 for k = 0..6 on V-invariant
    minimal block (NMAX = 7); super-polynomial convergence verified.
  - Single-plaquette physical environment at beta_env = 6:
    P(6) = 0.4594237929 (k = 1, NMAX = 7).

framework_internal_bracket: [0.4225, 0.59353]   # admissible-rho span
framework_internal_width:    0.1411              # NOT a tightening of existing bracket

closure_path_explicit:
  target: L_s = 2 APBC spatial cube tensor-transfer Perron solve
  scope: finite-dimensional, ~10^3 nonzero SU(3) tensor terms
  status: open; explicitly out of scope for this note
  reference: GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE
             section "Out of scope"
```

## 8. What this note does NOT establish

- No new strict lower bound on `<P>(6)` tighter than the existing
  framework floor `0.4225` (rho = delta).
- No quantitative bypass of the no-go's witness construction
  (`W_native = 0.1411 >> epsilon_witness = 3.03e-4`).
- No promotion of the parent gauge-scalar-temporal-completion theorem
  beyond the PR #484 retained_bounded status.
- No replacement of the K-Z external lift as the load-bearing tighter
  bracket.

## 9. Audit consequence

```yaml
claim_id: gauge_scalar_bridge_3plus1_native_lower_bound_staging_note_2026-05-03
note_path: docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_LOWER_BOUND_STAGING_NOTE_2026-05-03.md
runner_path: scripts/frontier_gauge_scalar_bridge_3plus1_native_lower_bound.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - gauge_scalar_temporal_completion_theorem_note
  - gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03
  - gauge_scalar_bridge_kz_external_lift_theorem_note_2026-05-03
  - gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note
  - gauge_vacuum_plaquette_tensor_transfer_perron_solve_note
  - gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note
  - gauge_vacuum_plaquette_mixed_cumulant_audit_note
  - gauge_vacuum_plaquette_constant_lift_obstruction_note
verdict_rationale_template: |
  Staging note compiling K-plaquette TUBE physical environment Perron data
  at beta_env = 6 on the V-invariant L_s=2 minimal block (NMAX = 7,
  MODE_MAX = 200) using existing framework primitives only. Verifies
  super-polynomial NMAX convergence (drift 1.3e-9 at k=1). Reports
  framework-internal bracket [0.4225, 0.59353] with width 0.1411 — wider
  than PR #484's K-Z external lift (W_lift = 0.05). Does NOT establish a
  new strict lower bound; the trivial admissible-rho floor 0.4225 remains
  the framework's strict lower bound until the L_s=2 APBC spatial cube
  tensor-transfer Perron solve is completed. Honest Path A (W_native >>
  epsilon_witness = 3.03e-4 by factor ~470). Identifies the explicit
  closure target as the L_s=2 spatial cube Perron solve, computationally
  in scope (~10^3 nonzero SU(3) tensor terms) but explicitly out of
  scope for this note.
```

This note's claim_type is `bounded_theorem` because it asserts:
1. A finite native framework bracket exists (`[0.4225, 0.59353]`).
2. Specific K-plaquette tube Perron values at `beta_env = 6` are
   explicit and converged at NMAX = 7.
3. The closure path is structured and computationally finite.

It does NOT claim a new strict lower-bound theorem; the bound 0.4225
is the existing framework floor inherited from
`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`.

## 10. Cross-references

- Companion external lift: [`GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md) (PR #484)
- Bypass target: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md) (PR #477)
- Parent of bracket consumer: [`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- Existing reference Perron solves: [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md)
- Closure target documentation: [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md) (section "Out of scope")
- Source-sector factorization: [`GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
- Cumulant onset: [`GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- Constant-lift obstruction: [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)

## 11. Command

```bash
python3 scripts/frontier_gauge_scalar_bridge_3plus1_native_lower_bound.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=4 SUPPORT=2 FAIL=0
```
