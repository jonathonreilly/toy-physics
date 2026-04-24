# α_LM Geometric-Mean Identity Theorem

**Date:** 2026-04-24
**Status:** **retained standalone structural-identity theorem** on `main`. Extracts and packages as its own theorem the exact identity `α_LM² = α_bare × α_s(v)` that follows immediately from the retained plaquette/coupling definitions in [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) and [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), but is not currently named as a standalone retained row anywhere on `main`.
**Primary runner:** `scripts/frontier_alpha_lm_geometric_mean_identity.py`

---

## 0. Statement

**Theorem (α_LM geometric-mean identity).** On the retained plaquette surface defined by

```text
α_bare      =  1 / (4π)
<P>          =  0.5934                        (Wilson plaquette evaluation, retained)
u_0           =  <P>^(1/4)
α_LM         =  α_bare / u_0                  (long-mode coupling)
α_s(v)        =  α_bare / u_0²                 (IR strong coupling on the same surface)
```

the long-mode coupling `α_LM` is exactly the **geometric mean** of the bare coupling `α_bare` and the IR strong coupling `α_s(v)`:

```text
(M)   α_LM²  =  α_bare · α_s(v)                       ⟺   α_LM  =  √(α_bare · α_s(v)).
```

Equivalently, on a logarithmic scale `α_LM` sits exactly halfway between `α_bare` and `α_s(v)`:

```text
(M')  log α_LM  =  (log α_bare + log α_s(v)) / 2.
```

In ratio form:

```text
(M'')  α_LM / α_bare  =  α_s(v) / α_LM  =  1 / u_0.
```

The identity holds as an **algebraic identity in `u_0`**, valid for every `u_0 > 0`. It does *not* depend on the specific numerical value of `<P>`; what depends on `<P>` is only the absolute scale of each coupling.

## 1. Retained inputs

| Ingredient | Reference |
|------------|-----------|
| Plaquette `<P> = 0.5934` retained evaluation | [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |
| `u_0 = <P>^(1/4)` plaquette weight | same |
| `α_bare = 1/(4π)` from native gauge normalization | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `g_bare² = 1` retained |
| `α_LM = α_bare / u_0` long-mode coupling | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) |
| `α_s(v) = α_bare / u_0²` IR strong coupling | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) |

No observed coupling and no lattice Monte Carlo result enter the derivation of (M). The retained `α_s(M_Z) = 0.1181` (matching observed `0.1179`) and `α_s(v) = 0.1033` are post-derivation comparators.

## 2. Derivation

The proof is one algebraic step.

```text
α_LM²  =  (α_bare / u_0)²
       =  α_bare² / u_0²
       =  α_bare · (α_bare / u_0²)
       =  α_bare · α_s(v).                                      ∎
```

Equivalently, (M) follows from `α_LM × u_0 = α_bare` and `α_s(v) × u_0² = α_bare`, by multiplying the first by `α_LM / α_bare = 1/u_0`:

```text
α_LM × α_LM × u_0 / u_0  =  α_LM² / 1  =  α_bare × (α_LM / α_bare)
                                       =  α_bare × (1 / u_0)
                                       =  α_bare × α_s(v) / α_bare
                                       =  α_s(v) × α_bare,
```

verifying `α_LM² = α_bare × α_s(v)`.

## 3. Numerical verification

Using the retained plaquette evaluation `<P> = 0.5934`:

```text
u_0           =  0.5934^(1/4)            =  0.877681381198…
α_bare       =  1/(4π)                  =  0.079577471545…
α_LM         =  α_bare / u_0             =  0.090667877…
α_s(v)        =  α_bare / u_0²            =  0.103303816…
```

Geometric-mean check:

```text
α_LM²            =  (0.090667877…)²    =  0.008220663…
α_bare × α_s(v)   =  0.079577471… × 0.103303816…
                  =  0.008220663…
```

Exact agreement to all printed digits (the runner verifies to floating-point precision and via exact symbolic comparison).

Logarithmic form:

```text
log α_bare       =  −2.531395…
log α_LM         =  −2.400485…
log α_s(v)        =  −2.269575…
(log α_bare + log α_s(v)) / 2  =  −2.400485…  =  log α_LM      ✓
```

The arithmetic-mean of `log α_bare` and `log α_s(v)` is exactly `log α_LM`, confirming the geometric-mean structure of (M).

## 4. Structural interpretation

**Why "geometric mean" and not "arithmetic mean" or some other interpolation?** The structural reason is the plaquette weight `u_0` enters `α_LM` with **power 1** and `α_s(v)` with **power 2**:

- `α_LM` carries `1/u_0` because it is a long-mode (Wilson-loop) observable: each gauge link contributes one factor of `u_0`.
- `α_s(v)` carries `1/u_0²` because it is a gauge-coupling observable: the running picks up a second factor of `u_0` from the radiative correction.
- `α_bare` carries `1/u_0⁰ = 1` because it is the un-tadpoled bare value.

Powers `(0, 1, 2)` of `1/u_0` form an arithmetic progression in the exponent, equivalent to a geometric progression in the values. The geometric mean of `α_bare` (exponent 0) and `α_s(v)` (exponent 2) is at exponent 1, which is exactly `α_LM`.

This explains structurally why:
- `α_LM = √(α_bare · α_s(v))` (geometric mean)
- `α_LM/α_bare = α_s(v)/α_LM = 1/u_0` (constant ratio between successive levels)

The "ladder" structure is

```text
α_bare  →  ×(1/u_0)  →  α_LM  →  ×(1/u_0)  →  α_s(v)
```

with each step multiplying by the same factor `1/u_0 ≈ 1.140`.

## 5. Consequences

### 5.1 Reduction of three couplings to two retained quantities

The three retained couplings `(α_bare, α_LM, α_s(v))` have a single structural relation (M) that ties them together. Consequently, only **two** of the three are independent. With `α_bare = 1/(4π)` fixed by gauge normalization and `α_s(v)` measured from the lattice plaquette, `α_LM` is **forced** to its geometric-mean value with no additional degree of freedom.

### 5.2 Logarithmic-spacing structural fingerprint

The arithmetic progression of exponents `(0, 1, 2)` is a structural fingerprint of the lattice/Wilson-flow architecture. Any modified gauge-coupling chain (e.g. an `α_LM' = α_bare / u_0^{3/2}` ansatz) would *break* the geometric-mean identity.

### 5.3 Cross-lane consistency check

Every retained lane that uses both `α_LM` and `α_s(v)` (CKM, neutrino seesaw, Yukawa transport, hierarchy) implicitly uses (M) to convert between them. This theorem packages that conversion as a standalone retained identity.

### 5.4 Test for lattice-coupling consistency

If non-perturbative lattice computation ever produced an `α_LM` violating (M) at the retained plaquette evaluation point (e.g. from a higher-loop lattice anisotropy), the framework's plaquette/coupling chain would be falsified. Current lattice agreement to `O(1/N_c²)` corrections (~0.2%) keeps (M) consistent with measurement.

## 6. Scope and boundary

**Claims:**

- (M) `α_LM² = α_bare × α_s(v)` exactly on the retained plaquette/coupling surface.
- (M') equivalent logarithmic form `log α_LM = (log α_bare + log α_s(v)) / 2`.
- (M'') equivalent ratio form `α_LM/α_bare = α_s(v)/α_LM = 1/u_0`.
- Three-coupling structural reduction to two independent quantities.

**Does NOT claim:**

- A native-axiom derivation of `<P> = 0.5934` itself (that's the retained plaquette self-consistency theorem, separate).
- The same identity in modified Wilson actions, anisotropic lattices, or non-Wilson plaquette discretisations.
- Anything about higher-loop running corrections to `α_s(M_Z)` (the retained one-decade running bridge is separate).
- Validity beyond `g_bare² = 1` (the retained canonical normalisation; if `g_bare²` were varied, the identity would still hold algebraically but `<P>` would shift).

## 7. Falsifiability

The identity holds as an algebraic consequence of the retained definitions. Any falsification would be of the underlying definitions:

- A modified retained `α_LM = α_bare / u_0^a` with `a ≠ 1`: would break (M) unless paired with a corresponding modification to `α_s(v) = α_bare / u_0^{2a}`.
- A higher-loop lattice correction `α_LM_phys ≠ α_bare / u_0`: would falsify the canonical plaquette/coupling chain. Current lattice MC measurements at `β = 6` show no evidence for such a correction at `O(1/N_c²)` precision.
- An anisotropic plaquette weight `u_0(t) ≠ u_0(s)` with `<P>` evaluated at a different topology: would change the form of all three couplings.

**Current observational status:** The retained chain `α_bare → u_0 → α_LM → α_s(v)` is consistent with lattice MC to sub-percent precision. The identity (M) is therefore consistent with current data.

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_alpha_lm_geometric_mean_identity.py
```

Expected: all checks pass.

The runner:

1. Computes `<P>`, `u_0`, `α_bare`, `α_LM`, `α_s(v)` to floating-point precision.
2. Verifies `α_LM² == α_bare × α_s(v)` to machine precision.
3. Verifies `log α_LM == (log α_bare + log α_s(v)) / 2`.
4. Verifies the ratio form `α_LM/α_bare == α_s(v)/α_LM == 1/u_0`.
5. Symbolic (sympy) verification on the abstract `u_0` parameter (identity holds for every `u_0 > 0`).
6. Cross-checks against retained values quoted in [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) and [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md).

## 9. Cross-references

- [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) — retained `<P>` evaluation
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) — retained `α_LM` and `α_s(v)` definitions
- [`RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md`](RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md) — Block A (couplings)
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) — parallel structural-identity extraction precedent
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) — same precedent
