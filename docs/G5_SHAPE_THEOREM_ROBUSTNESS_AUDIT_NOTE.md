# G5 Shape-Theorem Robustness Audit

**Date:** 2026-04-17
**Status:** SHAPE_THEOREM_ROBUST = TRUE. Seven independent stress tests, 57 PASS / 0 FAIL.
**Script:** [`scripts/frontier_g5_shape_theorem_robustness_audit.py`](../scripts/frontier_g5_shape_theorem_robustness_audit.py)
**Authority role:** robustness audit of Agent 10 v2's second-order `Γ_1` return shape theorem ([`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md)). Not a closure. Not a new retained axiom. A structural robustness certificate.

## Agent 10 v2's central claim under audit

> On the retained `Cl(3) ⊗ chirality` carrier `C^16`, the retained branch-convention second-order return
> `Σ(P_mid) = P_{T_1} Γ_1 P_mid Γ_1 P_{T_1}`
> restricted to the `T_1` species basis is the affine map
> `Σ(w) = diag(w_O0, w_a, w_b)` with the `(0,1,1) ∈ T_2` weight `w_c` decoupled, via `Γ_1` hopping `species 1 → O_0`, `species 2 → (1,1,0) ∈ T_2`, `species 3 → (1,0,1) ∈ T_2`. The residual `S_2` on axes `{2, 3}` forces `w_a = w_b` in every retained propagator scheme that respects this residual symmetry.

## Overall verdict

**`SHAPE_THEOREM_ROBUST = TRUE`**. Publication-grade robustness. Under all seven independent stress tests, the shape theorem survives exactly.

## Seven stress tests — outcomes

### Stress 1 — Alternative `Γ_i` axis choices (12 PASS / 0 FAIL)

For each `i ∈ {1, 2, 3}`, using the retained axis generator `Γ_i` and the axis-`i` species ordering for `T_1`, the shape theorem holds:

- First-order vanishing `P_{T_1} Γ_i P_{T_1} = 0`.
- Second-order return `P_{T_1} Γ_i (P_{O_0} + P_{T_2}) Γ_i P_{T_1} = I_3` (species).
- **The unreachable `T_2` state changes covariantly with the axis:**

  | axis | unreachable `T_2` state |
  |---|---|
  | 1 | `(0, 1, 1)` |
  | 2 | `(1, 0, 1)` |
  | 3 | `(1, 1, 0)` |

  The pattern is: *the `T_2` state with a zero in slot `i` is unreachable from any `T_1` state in one `Γ_i` hop*. The three unreachable states are exactly the three elements of `T_2`, and the map `axis → unreachable` is an `S_3`-equivariant bijection. **Shape theorem survives.**

### Stress 2 — `O_3` at fourth order (10 PASS / 0 FAIL)

Direct one-hop `T_1 → O_3` via `Γ_1` vanishes identically (`|P_{O_3} Γ_1 P_{T_1}|_F = 0`), even though `T_2 → O_3` is non-zero (`|P_{O_3} Γ_1 P_{T_2}|_F = √2`). For the iterated return family
`[Γ_1 P_{not T_1} Γ_1]^n` with `n = 1, 2, 3, 4` on species, the intermediate `P_{not T_1} = P_{O_0} + P_{T_2}` versus `P_{not T_1} = P_{O_0} + P_{T_2} + P_{O_3}` give IDENTICAL species blocks to machine precision at every `n`. The explicit 4th-order path `T_1 → T_2 → O_3 → T_2 → T_1` is computed and returns `diag(0, 0, 0)` on species — `O_3` cannot reseed species-resolved structure even when it is kinematically accessible via two `T_2` bridges. **Shape theorem survives.** `O_3` does not enter at any tested order.

### Stress 3 — Taste doublet L-taste vs R-taste (6 PASS / 0 FAIL)

Both `L`-taste and `R`-taste species blocks of `Σ(P_{O_0} + P_{T_2})` equal `I_3`. The weighted shape theorem `diag(w_O0, w_a, w_b)` holds **identically** on both tastes at arbitrary weight `(0.37, 1.19, 2.31, 0.73)`; the `(0,1,1)` weight `w_c = 0.73` is absent from both diagonals. The R-taste does not break the residual `S_2`. **Shape theorem survives.** The taste doubling is a pure spectator at second order.

### Stress 4 — Alternative intermediate-state splittings (10 PASS / 0 FAIL)

Single-projector decomposition of the retained intermediate:

| `P_mid` | species diag |
|---|---|
| `P_{O_0}` | `(1, 0, 0)` |
| `P_{T_2,(1,1,0)}` | `(0, 1, 0)` |
| `P_{T_2,(1,0,1)}` | `(0, 0, 1)` |
| `P_{T_2,(0,1,1)}` | `(0, 0, 0)` |
| `P_{T_2}` | `(0, 1, 1)` |

Linear reconstruction `Σ(P_{T_2}) = Σ(110) + Σ(101) + Σ(011)` is exact. The axis-aligned vs axis-complementary split `P_{T_2} = P_{T_2,contains-ax1} + P_{T_2,lacks-ax1}` gives `(0, 1, 1)` and `(0, 0, 0)` respectively — the "lacks axis 1" state is precisely the unreachable `(0, 1, 1)`. Every finer subsplitting respects the shape theorem exactly. **Shape theorem survives.**

### Stress 5 — `S_3` permutation gauge check (10 PASS / 0 FAIL)

Representation subtlety clarified: the retained `C^16` embedding `G_1 = σ_x ⊗ I ⊗ I ⊗ I`, `G_2 = σ_z ⊗ σ_x ⊗ I ⊗ I`, `G_3 = σ_z ⊗ σ_z ⊗ σ_x ⊗ I` is a Jordan-Wigner ordering; a naive bit-permutation unitary `U_{perm}` is NOT a Clifford ring automorphism (it maps `G_1` to `D Γ_{perm[0]}` with a diagonal ±1 dressing `D` for even permutations; for odd permutations the resulting `U_{perm} G_1 U_{perm}^†` can fail `{·, γ_5} = 0`). **However, the HW-projector structure is manifestly `S_3`-equivariant:** `U_{perm}` commutes exactly with `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` for all six permutations (max commutator = 0 to machine precision). The physically correct gauge-invariance statement uses the native `Γ_i` operators directly: for each axis `i ∈ {1, 2, 3}`, the shape theorem holds with the unreachable state covariantly mapped. **Shape theorem survives** as an `S_3`-covariant physical identity. The naive-`U_{perm}` failure at odd permutations is a *Clifford-representation* artifact, not a shape-theorem failure.

### Stress 6 — Pre-EWSB `M(φ) = Σ_i φ_i Γ_i` and axis compatibility (10 PASS / 0 FAIL)

For pure axis selections `φ = e_i`, `M(e_i) = Γ_i` and the axis-`i` shape theorem holds. For general `φ` not on an axis (tested at `(1,1,0), (1,1,1), (0.5,1.3,2.7), (1,-1,2)`), the identity
`Σ_{species}(M(φ)) = |φ|² I_3`
holds exactly — a direct consequence of `M(φ)² = |φ|² I` from the Dirac-bridge theorem. Each of the three axis choices `e_1, e_2, e_3` gives its OWN shape theorem (with its own unreachable state). The three are mutually compatible, each defining a valid post-EWSB branch consistent with the selector-potential minima. **Shape theorem survives** as a family-index-resolved structure before EWSB.

### Stress 7 — Retained-surface reading of the Dirac-bridge theorem (4 PASS / 0 FAIL)

The Dirac-bridge runner `frontier_dm_neutrino_dirac_bridge_theorem.py` (28 PASS / 0 FAIL on live `main`) asserts three relevant PASS items:

- (a) `P_{T_1} Γ_1 P_{T_1} = 0`
- (b) `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_6` on full taste-doubled `T_1`
- (c) `O_3` adds nothing

Agent 10 v2's shape theorem is a *strictly stronger* statement:

- (d) for any weighted intermediate `P_{mid}(w) = w_{O_0} P_{O_0} + Σ_j w_{T_2,j} P_{T_2,j}`,
  `P_{T_1} Γ_1 P_{mid}(w) Γ_1 P_{T_1}` restricted to species equals `diag(w_{O_0}, w_{T_2,(1,1,0)}, w_{T_2,(1,0,1)})` with `w_{T_2,(0,1,1)}` absent.

**Verified logical chain:** (d) follows from linearity in `P_{mid}` plus the single-projector identities from Stress 4 (which are corollaries of (a)+(b)+(c) via `I_6 = Σ_{single projectors}`). The runner's PASS set plus the single-projector identities (also computed here) logically entails Agent 10 v2's shape theorem. **Shape theorem is implied by the retained surface**, not an assertion beyond it.

## Summary table

| Stress test | PASS | FAIL | Status |
|---|---|---|---|
| 1. Alternative axis choices | 12 | 0 | survives |
| 2. `O_3` at fourth order | 10 | 0 | survives |
| 3. Taste doublet (L vs R) | 6 | 0 | survives |
| 4. Alternative intermediate splittings | 10 | 0 | survives |
| 5. `S_3` gauge check | 10 | 0 | survives (HW-projector equivariance) |
| 6. Pre-EWSB family | 10 | 0 | survives |
| 7. Retained-surface reading | 4 | 0 | logically implied by retained PASS set |
| **Total** | **57** | **0** | **`SHAPE_THEOREM_ROBUST = TRUE`** |

## Additional structure revealed by the stress tests

1. **S_3 equivariance is structural, not accidental.** The unreachable-state rule is the `S_3`-covariant "the `T_2` state with a zero in axis-`i` slot is unreachable under `Γ_i`". This is a manifestly axis-symmetric statement of the mechanism.
2. **Taste is a pure spectator at second order.** Both chirality tastes give identical species-block structure; the residual `S_2` on axes `{2, 3}` is independent of taste. Any taste-distinguishing primitive on the retained surface would have to enter above second order.
3. **`O_3` is doubly suppressed.** `Γ_1` has no matrix element `T_1 → O_3` at all, so `O_3` can only enter via a two-bridge path through `T_2`. Even then, species-block content of that 4th-order path is identically zero.
4. **Single-projector identities form a basis.** The four species-diagonals `(1,0,0), (0,1,0), (0,0,1), (0,0,0)` from `P_{O_0}, P_{T_2,(1,1,0)}, P_{T_2,(1,0,1)}, P_{T_2,(0,1,1)}` span the affine space of shape-theorem-compatible weighted propagators — this is why Correction-C in Agent 10 v2's note can in principle achieve any target diagonal but the HW-staggered retained primitive cannot.
5. **Representation subtlety without physical consequence.** The Jordan-Wigner ordering of `Γ_i` breaks strict bit-permutation covariance of the Clifford ring, but HW-projector covariance is absolute. The shape theorem is a statement about HW-projector-resolved hopping, so the Jordan-Wigner artifact does not touch it.

## What this does NOT claim

- No closure of G5. The shape theorem being robust does not supply the missing per-`T_2`-state weighting primitive.
- No new retained theorem. The shape theorem is a *corollary* of the retained Dirac-bridge theorem PASS set, now certified as airtight under seven independent audits.
- No refutation of Agent 10 v2's note; the audit *supports* it.

## Honest interpretation

Agent 10 v2's shape theorem is publication-grade robust. It is not sensitive to the choice of axis-branch (Γ_1 vs Γ_2 vs Γ_3), does not leak through `O_3` at fourth order, is taste-independent, respects all finer intermediate-state splittings, is a pure HW-projector-covariant `S_3`-equivariant identity (the naive-Jordan-Wigner `S_3` failure is a Clifford-representation artifact with zero impact on HW-projector physics), works across the whole pre-EWSB `M(φ)` family consistent with axis selection, and is logically implied by the retained Dirac-bridge theorem PASS set plus a single-projector linearity argument. This transfers no new physics to G5 — the hierarchy problem remains `UNDERDETERMINED` exactly as stated — but it confirms that any future retained primitive attempting to lift the `I_3` degeneracy must act as a per-`T_2`-state weighting on the very structure that this audit certifies is airtight. The missing lever is a single well-posed object, not a family of possible fixes against an uncertain background.

## Dependency contract

Retained authorities that must PASS on live `main`:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` — 28 PASS / 0 FAIL (supplies (a), (b), (c) of Stress 7).
- `frontier_g5_gamma_1_second_order_return.py` — 20 PASS / 0 FAIL (Agent 10 v2's note; this audit stress-tests its central claim).

Framework objects used (none as fit parameters):
`Γ_1, Γ_2, Γ_3, γ_5, Ξ_5`, `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}`, single-state `T_2` projectors, `L/R` chirality-taste bases, `S_3` permutation unitaries. No PDG input. No phenomenology.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md) Section F:

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_shape_theorem_robustness_audit.py` | This note | `SHAPE_THEOREM_ROBUST = TRUE`; 57 PASS / 0 FAIL; seven-angle stress test certifies Agent 10 v2's shape theorem as publication-grade robust and logically implied by the retained Dirac-bridge PASS set plus a linearity argument. |

## Status

Robustness audit. Not a closure. The retained `Γ_1` second-order shape on `T_1` is now audited from seven independent directions and survives all of them. G5 remains open along Correction-C — requiring a new retained primitive that distinguishes the three `T_2` states — but the shape-theoretic backbone against which any such primitive must be measured is now certified robust.
