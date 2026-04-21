# Koide Round 1 Parallel Attack Results (evening 2026-04-20)

**Status:** Round 1 of parallel investigations complete. One strong success,
two dimensionless identities, three clean no-gos. Spirit: **we do things the
hard way to break new ground**.

---

## Summary by vector

| Vector | Topic | Result | Key finding |
|---|---|---|---|
| V1 | Gradient flow | NO-GO | No canonical flow on Herm_circ(3). "κ=2 is Frobenius-isotropic cone" — dim-counting tautology |
| V4 | Universal cover | NO-GO | Cover reproduces no-go exactly. Per-Z₃ holonomy = 2π/3 (rational × π), NOT 2/9 rad |
| V5 | Sphaleron / anomaly | PARTIAL | **Exact dimensionless**: `\|Tr[Y³]_LH\|/N_LH = 2/9`. No radian mechanism |
| V6 | Modular / CM | NO-GO | No modular form gives 2/3 or 2/9 at τ=ρ. CM values are Γ(1/3)^k·π^m, not rationals |
| **V9** | **Alternative entropy** | **STRONG SUCCESS** | **`F(G) = 2 log(tr G) + log(C_2)` has unique extremum at κ=2, no SO(2) postulate** |
| V10 | Chern-Simons TQFT | WEAK | SU(3)_1 gives Q=2/3 at (0, a, a) degenerate, not physical hierarchy |

---

## STRONG SUCCESS: Vector 9 (native forcing law for κ=2)

### The functional

**`F(G) = 2 log(tr G) + log(C_2)` on Herm_circ(3)**

where:
- `tr G = 3a` (linear Casimir, aka power sum P_1)
- `C_2 = tr G² − (tr G)²/3 = 6|b|²` (quadratic Casimir, aka traceless power sum)

Equivalently: `F_inv(G) = log[(tr G)² · C_2 / (tr G²)²]` (scale-invariant).

### Uniqueness

Under any natural constraint (scale, Frobenius norm, both), **the unique
extremum is κ := a²/|b|² = 2**.

- With `tr G² = N` constraint: Lagrange gives `α/β = 2` → κ = 2.
- Scale-invariant form: `dF_inv/dκ = (2−κ)/[κ(κ+2)] = 0` has **unique
  interior root κ = 2**.
- Second derivative at κ=2 is `−1/8` (**maximum**).

### Why this is Cl(3)/Z³-native (no SO(2) postulate)

The invariants `tr G` and `C_2 = tr G² − (tr G)²/3` are Z_3-CYCLIC TRACE
INVARIANTS built directly from powers `tr(G^n), n ≤ 2`. They require no
postulate beyond Hermitian-circulant structure:

1. **Automatically phase-independent** because `Σ_k cos(φ + 2πk/3) = 0`
   and `Σ_k cos²(φ + 2πk/3) = 3/2`. This is a **symmetric-function
   identity for three equally-spaced angles**, NOT an imposed SO(2)
   invariance.
2. **Rep-theoretic interpretation**: `F = log(E_singlet · E_doublet)`
   where E_singlet = 3a² is the trivial-rep energy-squared and E_doublet
   = 6|b|² is the doublet-rep energy-squared. F is a PARTITION FUNCTION
   over the Z_3 irreducible representations.
3. **Derivable from observable principle?** The retained
   observable-principle W[J] = log|det(D+J)| - log|det D| might give F
   naturally for specific J. TBD (Round 2 investigation).

### Contrast with log|det|

`log|det G| = log(a + 2 Re b) + log(a + 2 Re bω̄) + log(a + 2 Re bω)` has
extremum at κ = 1 (fails to give Koide).

The NEW functional `2 log(tr G) + log(C_2)` has extremum at κ = 2
(succeeds).

**Key difference**: log|det| uses EACH EIGENVALUE separately (3 logs);
F uses ISOTYPIC BLOCKS (2 logs: singlet and doublet). The isotypic
weighting (1, 1) per block — as opposed to per-eigenvalue (1, 1, 1) —
gives κ = 2.

### Is this the new native forcing law for I1?

**Candidate YES.** The functional `2 log(tr G) + log(C_2)` is:
- Manifestly Z_3-cyclic (trace invariants).
- No SO(2) postulate required.
- Unique extremum at κ = 2.
- Second-derivative negative (maximum, not saddle).

**Open question for Round 2:** can `F` be derived from the retained
observable principle `W[J] = log|det(D+J)| - log|det D|` by choosing a
specific Z_3-covariant source `J`?

If YES: I1 closes natively via the observable principle itself.
If NO: `F` is still a clean functional but needs its own structural
justification.

---

## Partial success: Vector 5 (dimensionless 2/9)

### Exact identity

**`|Tr[Y³]_LH| / N_LH = (16/9) / 8 = 2/9`**

where:
- Tr[Y³]_LH = -16/9 is the retained LH Y³ anomaly coefficient.
- N_LH = 8 is the total LH Weyl component count (2·3 quarks + 2·1 leptons).

This is the **average cubic hypercharge per LH fermion**, equaling
Brannen phase δ EXACTLY as a dimensionless rational.

### Does this close I2/P?

**NO.** δ = 2/9 is in RADIANS, this is DIMENSIONLESS. The identity shows
2/9 appears natively in Cl(3)/Z³ anomaly arithmetic but doesn't bridge
to radians.

### But: it's a third cross-check

Combined with:
- Tr[Y³]_quark_LH = 2/9 (per-quark-sector contribution)
- n_eff/d² = 2/9 (from Brannen reduction theorem)

We now have THREE exact dimensionless 2/9 identities from retained
Cl(3)/Z³ structure. All agree on the pure rational. The remaining open
is ONLY the radian-unit bridge.

---

## Clean no-gos: Vectors 1, 4, 6

### V1 (gradient flow)

Four principled gradient flows (Ricci, Yamabe, Fisher, observable-principle)
all fail to select κ=2 dynamically. Key insight: **"κ=2 is the
Frobenius-isotropic cone" is a dim-counting tautology** (dim trivial : dim
doublet = 1 : 2, so equal weights means a² : |b|² = 2 : 1). No non-trivial
dynamics needed.

This actually STRENGTHENS the qubit-lattice-dim closure — it shows the
structural identity is "baked into" the Z_3 isotypic decomposition
without needing flow dynamics.

### V4 (universal cover)

The universal cover of three Koide arcs under Z_3 deck action is `S¹`,
but the tautological bundle winding on the cover gives per-Z_3 holonomy =
`2π/3` radians (rational × π), NOT 2/9 rad. The no-go's obstruction
"every retained radian is rational × π" is CONFIRMED even on the cover.

The pure rational 2/9 appears as `fractional winding / d²` (dimensionless),
not as radians.

### V6 (modular / CM)

Despite the Z_3 CM structure at τ = e^{2πi/3} on the elliptic curve
`y² = x³ + 1`, NO natural modular form evaluates to 2/3 or 2/9 at ρ.

CM values live in `ℚ(Γ(1/3)^k · π^m)` — transcendental algebraic
extensions, not simple rationals.

The 2/3 appearing as stabilizer-order ratio `|Aut(i)|/|Aut(ρ)| = 2/3`
is TOPOLOGICAL, not a modular form value, so it cannot encode specific
Koide mass relations.

---

## Weak result: Vector 10 (TQFT)

`SU(3)_1` Chern-Simons at level k=1 has 3 primaries with conformal
weights (0, 1/3, 1/3). Identifying weights with masses gives Koide
Q = 2/3 EXACTLY — but only at the degenerate (0, m, m) point, NOT the
physical hierarchy (m_e ≪ m_μ ≪ m_τ).

**Verdict:** structural symmetry match, but the physical Koide lives at
a DIFFERENT point on the Koide cone. The TQFT gives one specific
boundary condition, not the full solution.

Other TQFTs scanned (SU(2)_2, Ising, Z_3 DW, Fibonacci, minimal models)
did NOT give Q = 2/3 at any relevant point.

---

## Status reassessment

### I1 (Q = 2/3):

**New strong candidate closure via Vector 9.** The functional
`F = 2 log(tr G) + log(C_2)` has unique extremum κ = 2 on Herm_circ(3),
without SO(2) postulate. This is a NATIVE forcing law if derivable from
the retained observable principle.

**Round 2 target:** derive F from W[J] for a specific Z_3-covariant J.
If successful, I1 closes definitively.

### I2/P (δ = 2/9 radians):

**All five radian-targeted vectors failed.** The "every retained radian
is rational × π" obstruction appears structurally unshakeable for
closed-loop / static mechanisms.

**Surviving dimensionless identity:** δ = 2/9 = |Tr[Y³]_LH|/N_LH
= Tr[Y³]_quark_LH = n_eff/d² — three different retained Cl(3)/Z³
rational derivations. All dimensionless.

**Radian bridge remains open.** The gap is pure-rational-to-radian
conversion, which retained Cl(3)/Z³ character data cannot provide.

**Round 2 targets:**
- Dynamical (non-static) radian quantization mechanisms.
- Lattice propagator radian quantum (candidate input (a) from no-go).
- Non-abelian Wilson holonomies with fractional phases.
- Re-examine the Brannen cosine parametrization for hidden radian
  structure.

---

## Round 2 priorities

Based on Round 1 results, launch Round 2 attacks:

1. **Derive F (Vector 9 winner) from observable principle.** Highest
   value: if successful, I1 closes.
2. **Lattice propagator analysis.** Compute retained Cl(3)/Z³ lattice
   Green's function phase structure. Can it produce 2/9 rad natively?
3. **4×4 hw=1+baryon Wilson holonomy.** Extend hw=1 to 4×4 sector;
   compute C_3 Wilson line phases. Any naturally give 2/9 rad?
4. **Brannen cosine re-derivation.** Derive √m_k = A(1+√2 cos(δ+2πk/3))
   from retained structure directly; see if δ = 2/9 rad emerges.
5. **Non-commutative geometry / Connes framework.** Does the retained
   spectral triple have a specific scaling parameter equaling 2/9?
6. **Seiberg-Witten-like monopole calculation.** On 4d manifolds with
   Z_3 action, SW invariants give specific phases.

**Multi-week horizon.** Each is a serious physics project. Start
parallel investigations immediately.
