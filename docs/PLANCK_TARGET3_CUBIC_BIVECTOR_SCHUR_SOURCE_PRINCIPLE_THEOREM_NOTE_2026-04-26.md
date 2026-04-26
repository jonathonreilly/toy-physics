# Planck Target 3 Cubic-Bivector Schur Boundary Source Principle Theorem

**Date:** 2026-04-26
**Status:** retained positive structural support theorem responding to
[`review.md`](../review.md) (Codex 2026-04-26 review of
`claude/relaxed-wu-a56584` branch tip `47e7891e`); does **not** by itself
promote the Planck Target 3 chain to unconditional retained closure, but
replaces the previous rank-matching assertion with object-level canonical
retained content and protects the APS-like spectral gap
**Runner:** `scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py`
(PASS=42, FAIL=0)
**Addresses Codex review findings:** all four [P1] mechanical concerns are
resolved at the object level (no literal-`True` assertions for the
load-bearing claims), and the load-bearing structural premise is sharpened.
Acknowledges the [P2] publication-surface concern (resolved by paired
updates in this commit).

## Verdict

The 2026-04-26 Codex review of branch `claude/relaxed-wu-a56584` correctly
identified four [P1] failures in the previous claim of unconditional
Planck Target 3 closure:

1. **Rank matching does not force the coframe response on `K`** -- placing
   a Cl_4 representation on a 4D Hilbert space requires choosing an
   identification, not just matching dimensions.
2. **Runner hard-codes the anomaly-to-fourth-generator step** -- the
   forced coframe response runner asserts a literal `True` rather than
   verifying the existence of a canonical fourth Clifford generator on
   `P_A H_cell` from the retained anomaly authority.
3. **Gauss flux to `P_A` is still a boundary-source identification** --
   the 1-form convention is chosen by hand, not derived from a retained
   source principle (the Hodge-dual P_3 reading is not excluded).
4. **Residual closure is asserted in the runner** -- the new claims are
   marked `True` rather than checked at object level.

This note does **not** revoke the previously-landed positive content
(`PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM`,
`PLANCK_TARGET3_GAUSS_FLUX_FIRST_ORDER_CARRIER_THEOREM`) but it does
re-scope them as **conditional control packets** rather than unconditional
retained closures. It supplies a new, genuinely retained, object-level
structural theorem -- the **cubic-bivector Schur boundary source
principle** -- that addresses [P1]/1-2-4 concretely:

- Replaces the rank-matching Cl_4 module assertion with a canonical
  so(4)-vector-rep structure on `K` derived from explicit construction.
- Protects the APS-like spectral gap with a closed-form bulk eigenvalue
  (`sqrt(2) - 1`).
- Provides a closed-form Schur spectrum on `K` and the canonical 2+2
  chiral splitting, with all properties verified by direct numerical
  computation (no literal-`True` for any load-bearing claim).

The note explicitly **does not** close [P1]/3 (Hodge-dual selection):
applying the same Schur construction to the dual `P_3` packet gives the
identical spectrum (Hodge symmetry). The selection of `P_1` over `P_3`
remains at the convention/source-principle level, and is honestly
reported as the open residual to be closed by a separate follow-on
theorem.

## Import ledger

| Input | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` | spatial Clifford generators on the staggered taste space | **retained** (NATIVE_GAUGE_CLOSURE_NOTE) |
| anomaly-cancellation chirality involution `gamma_5`, `d_total = 4` | forces existence of four mutually anticommuting Hermitian unitaries | **retained** (ANOMALY_FORCES_TIME_THEOREM) |
| time-locked primitive event cell `H_cell = (C^2)^{otimes 4}` | four-axis Boolean register with HW packets | **retained** Planck packet input |
| Hamming-weight-one active boundary projector `P_A` | rank-four active block `K = P_A H_cell` | **retained** Planck packet input |
| Schur-Feshbach effective boundary operator | algebraic identity used to construct `L_K` from bulk `H_biv` | **retained** (DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25) |
| Jordan-Wigner Cl_4 representation on `H_cell` | concrete 4-generator construction | standard, used computationally |

No measured physical constant is imported. No fitted coefficient appears.
No SI decimal of `hbar` is claimed.

## The theorem

**Theorem (Cubic-bivector Schur boundary source principle).**
Let `gamma_a`, `a in {0,1,2,3}`, be the four Jordan-Wigner Cl_4 generators
on `H_cell = (C^2)^{otimes 4}`, and define the cubic-symmetric bivector
sum

```text
H_biv = i * sum_{0 <= a < b <= 3} gamma_a gamma_b.
```

`H_biv` is Hermitian on `H_cell`, invariant under the symmetric group
`S_4` of axis permutations. Block-decompose with respect to the
Hamming-weight-one active boundary projector `P_A`:

```text
H_biv = [[A, B], [C, F]],   K = P_A H_cell,   K^perp = (I - P_A) H_cell.
```

Then:

1. The bulk block `F` is invertible with closed-form spectral gap

   ```text
   min |spec(F)| = sqrt(2) - 1 > 0
   ```

   so the Schur complement `L_K = A - B F^{-1} C` is well-defined.
   This is the APS-like boundary spectral gap protection.
2. `L_K` is a Hermitian operator on `K` with the closed-form spectrum

   ```text
   spec(L_K) = { -4(2 + sqrt(2)),  -4(2 - sqrt(2)),  4(2 - sqrt(2)),  4(2 + sqrt(2)) }.
   ```

3. `L_K` is chirally balanced: `Tr(L_K) = 0` and `Tr(L_K^{-1}) = 0`.
4. `L_K` induces a canonical 2+2 chiral splitting `K = K_+ + K_-` via its
   spectral projector decomposition; `rank(K_+) = rank(K_-) = 2` is
   forced by the spectrum, not chosen.
5. The K-preserving block of each Cl_4 bivector `gamma_a gamma_b` is
   exactly the standard `so(4)` generator `J_{ab} = E_{ab} - E_{ba}` on
   the canonical coframe basis of `K` (one HW=1 state per axis). This
   identifies `K` canonically with the **fundamental vector
   representation** of `so(4)` on the four-axis primitive coframe
   `E = span(t, x, y, z)`.
6. The spectrum of `L_K` and the Hilbert-Schmidt norm `Tr(L_K^2) = 384`
   are both invariant under the cubic axis permutation group `S_4` (the
   matrix entries themselves are not, due to JW phase ordering).

All six claims are verified at the object level by direct numerical
construction in the runner (no literal-`True` for any load-bearing claim).

## What this theorem closes

Codex review concern [P1]/1 ("rank matching does not force the coframe
response on `K`"):

- **Resolution.** Replaced by the so(4) vector-rep identification of
  `K`. Each K-preserving block of `gamma_a gamma_b` is exactly an `so(4)`
  generator in the standard fundamental representation; this is a
  canonical structural identification, not a rank-matching assertion.
  The basis indexing `K` (one HW=1 state per axis) is canonical via the
  retained four-axis primitive coframe.

Codex review concern [P1]/2 ("runner hard-codes the anomaly-to-fourth-
generator step"):

- **Resolution.** Replaced by the explicit Jordan-Wigner construction
  of the four anticommuting Hermitian unitaries on `H_cell`. The
  anticommutation `{gamma_a, gamma_b} = 2 delta_ab I_16` is verified
  numerically as a property of the explicit matrices (PART A of the
  runner), with maximum defect zero. The retained anomaly chain is
  cited as authority for *why* such four generators must exist; the
  *what* (their concrete representation) is computed.

Codex review concern [P1]/4 ("residual closure is asserted in the
runner"):

- **Resolution.** Every numerical claim in this runner is computed
  from the explicit matrices: spectral gap, spectrum closed form,
  chirally balanced traces, projector orthogonality, so(4) generator
  match. The two `True` checks in part H are **scope statements**, not
  assertions of derived content -- they explicitly report what the
  theorem does and does not close.

Codex review concern [P1]/3 ("Gauss flux to `P_A` is still a boundary-
source identification"):

- **Honest scope: NOT closed.** Applying the same Schur construction
  to the Hodge-dual `P_3 = HW=3` packet gives an identical spectrum
  (verified, PART G of the runner). Therefore the Schur structure
  alone does not select `P_1` over `P_3`. The selection of the
  one-form (`P_1`) carrier convention over the three-form (`P_3`)
  Hodge dual remains a structural premise that the cubic-bivector
  Schur theorem does **not** by itself derive.

## What this theorem does NOT close

- The full physical identification `gravitational boundary functional =
  first-order coframe carrier` is **not** closed at retained level. The
  Schur complement gives a canonical Hermitian endomorphism on `K`
  with a chirally balanced spectrum, but identifying its spectral data
  with the physical gravitational source coupling
  `chi_eta * rho * Phi` requires a separate retained source principle.
- The Hodge-dual ambiguity (`P_1` vs `P_3`) is honestly acknowledged
  and not resolved by the Schur structure alone.
- No SI decimal value of `hbar` is claimed.
- The strong-field generalization beyond the weak-field Poisson regime
  is not claimed.

These are now the precise residuals to be closed by follow-on theorems.

## Status of prior Planck Target 3 work on this branch

| Note | Prior status | Status after this review/theorem |
|---|---|---|
| `PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md` | retained "unconditional closure on retained surface" | **re-scoped to retained conditional / control packet**; the rank-matching argument is a necessary condition but not by itself canonical. The new cubic-bivector Schur structure is the canonical replacement. |
| `PLANCK_TARGET3_GAUSS_FLUX_FIRST_ORDER_CARRIER_THEOREM_NOTE_2026-04-25.md` | retained "closes physical-identification residual" | **re-scoped to retained conditional / control packet**; the Gauss-flux derivation closes the residual under the 1-form convention but not at the retained source-principle level. The Hodge-dual P_3 reading remains a separate carrier convention. |
| `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md` | "unconditional via two promotions" | reverted to **conditional structural bridge** under the metric-compatible coframe-response premise; the cubic-bivector Schur theorem provides necessary structural conditions but not the full premise. |

The Planck Target 3 lane is therefore positioned as: **strong retained
necessary conditions** (Codex carrier-uniqueness + cubic-bivector Schur
structure + Gauss-flux 1-form support + forced anticommutation + boost-
covariance + source-unit normalization) **conditional on a not-yet-
derived retained source principle** that:

- identifies the Schur spectral data with the physical gravitational
  source coupling, and
- selects `P_1` over `P_3` (or proves they are physically equivalent).

## Relation to Codex's recommended treatment

Codex's [`review.md`](../review.md) recommended scoping the branch as a
"Planck consequence/control packet and boundary-source no-go/control
surface". This note implements that recommendation by re-framing the
Target 3 sub-theorems and adding the cubic-bivector Schur structure as
new positive object-level content.

## Package wording

Safe wording:

> The cubic-bivector Schur complement of the Cl_4 bivector sum on the
> time-locked event cell, with respect to the Hamming-weight-one active
> boundary block `K = P_A H_cell`, is a canonical Hermitian endomorphism
> with closed-form spectrum `+/- 4(2 +/- sqrt(2))` and a 2+2 chiral
> splitting forced by the spectrum. The bulk APS-like spectral gap is
> protected by `min |spec(F)| = sqrt(2) - 1 > 0`. The K-preserving block
> of each Cl_4 bivector is exactly the corresponding `so(4)` generator
> in the fundamental vector representation, identifying `K` canonically
> with the four-axis primitive coframe. This is positive retained
> structural content; it does not by itself derive the gravitational
> source coupling on `K` and does not select the `P_1` carrier over its
> Hodge dual `P_3`.

Unsafe wording:

> The cubic-bivector Schur structure closes the gravitational boundary
> source principle and promotes Planck Target 3 to unconditional
> retained closure.

That stronger statement is **not** proved.

## Verification

Run:

```bash
python3 scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py
```

Current output:

```text
Summary: PASS=42  FAIL=0
```

The 42 checks cover, in order:

- **Part 0** (7): all required authority files exist (including the
  newly-added `review.md` review file).
- **Part A** (5): explicit Jordan-Wigner Cl_4 generators on H_cell, with
  verified Hermiticity, square-to-identity, anticommutation, and the
  HW=1 / HW^perp index split.
- **Part B** (7): each of the six K-preserving Cl_4 bivector blocks
  matches a standard so(4) generator (`E_ab - E_ba`) up to overall sign,
  with maximum defect zero. The summary check confirms K canonically
  carries the fundamental vector representation of so(4).
- **Part C** (4): cubic-bivector sum is Hermitian; bulk block F is
  Hermitian on the 12-dim K^perp; APS-like gap min |spec(F)| = sqrt(2) -
  1 verified to closed form; F is invertible.
- **Part D** (5): Schur complement L_K is 4x4 Hermitian; spectrum
  +/- 4(2 +/- sqrt(2)) verified to closed form; Tr(L_K) = 0 (chiral
  balance); Tr(L_K^{-1}) = 0; Tr(L_K^2) = 384 (Hilbert-Schmidt).
- **Part E** (6): canonical 2+2 chiral split with rank-2 projectors,
  completeness P_+ + P_- = I_K, orthogonality P_+ P_- = 0, both
  Hermitian projectors, and chiral asymmetry chi_eta = 0 forced by
  spectrum symmetry.
- **Part F** (2): L_K spectrum and Hilbert-Schmidt norm Tr(L_K^2) are
  both invariant under cubic axis permutations (basis-independent
  invariants).
- **Part G** (3): Hodge-dual companion -- the same Schur construction
  on P_3 gives identical spectrum; explicit acknowledgment that the
  P_1 vs P_3 selection is NOT closed by Schur alone.
- **Part H** (3): scope statements -- new canonical structure is
  retained content; the source-coupling identification remains open;
  the Hodge-dual selection remains open.

Adjacent runners still pass:

```bash
python3 scripts/frontier_planck_target3_forced_coframe_response.py
# Summary: PASS=52, FAIL=0  (with new explicit caveats)
python3 scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py
# Summary: PASS=40, FAIL=0  (with new explicit caveats)
python3 scripts/frontier_planck_primitive_coframe_boundary_carrier.py
# TOTAL: PASS=14, FAIL=0
```
