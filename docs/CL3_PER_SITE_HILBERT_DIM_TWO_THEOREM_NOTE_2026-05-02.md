# Per-Site Hilbert Space Dimension = 2 from Retained Cl(3) Per-Site Uniqueness

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the per-site Hilbert space at every lattice site of the framework's retained Cl(3) ⊗ Z^3 substrate has complex dimension exactly 2; equivalently, every faithful irreducible complex representation of the Cl(3) algebra has dim_C = 2.
**Status:** awaiting independent audit.
**Loop:** `positive-only-r4-20260502`
**Cycle:** 1 (Block 1)
**Branch:** `physics-loop/positive-only-r4-block01-per-site-dim-20260502`
**Runner:** `scripts/cl3_per_site_hilbert_dim_two_check.py`
**Log:** `outputs/cl3_per_site_hilbert_dim_two_check_2026-05-02.txt`

## Cited authorities (one hop)

- [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) — `effective_status: retained` on the live ledger. Provides: any faithful irreducible representation of Cl(3) on a finite-dimensional complex vector space has dimension exactly 2 and is unitarily equivalent to the canonical Pauli representation `γ_i = σ_i`.

This is the only load-bearing one-hop dependency.

## Admitted-context inputs

- **A2 — Z^3 substrate.** The framework's retained spatial substrate; each site carries a copy of Cl(3).
- **Site-Hilbert-space identification.** The Hilbert space at each lattice site is the faithful irreducible Cl(3) representation. Standard structural definition.

No physics conventions admitted beyond the retained Cl(3) per-site uniqueness theorem.

## Statement

For every lattice site `x ∈ Z^3` on the framework's retained Cl(3) ⊗ Z^3 substrate:

**(D1) Site Hilbert space dim.** `dim_C H_x = 2` exactly.

**(D2) Pauli realization.** The Cl(3) generators at site x are realized (up to unitary equivalence) as the standard Pauli matrices `σ_1, σ_2, σ_3`.

**(D3) Total Hilbert dim on finite block.** For a finite block `Λ ⊂ Z^3` with `|Λ|` lattice sites, the total Hilbert space is `⊗_{x ∈ Λ} H_x` with `dim_C = 2^{|Λ|}`.

**(D4) Spinor module is unique up to unitary equivalence.** No alternative inequivalent faithful Cl(3) representation exists on a finite-dimensional complex space.

## Proof

### Step 1 — Cite the retained per-site uniqueness theorem

By [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md), the minimal complex spinor irrep of Cl(3) has dimension 2.

### Step 2 — Apply to the framework substrate

The framework's per-site algebra at every `x ∈ Z^3` is Cl(3) (axiom A1 of A_min). The site Hilbert space is the faithful irreducible representation. By Step 1, `dim_C H_x = 2`. ∎

### Step 3 — Pauli realization (D2)

The retained per-site uniqueness theorem also says the representation is unitarily equivalent to `γ_i = σ_i`. Hence each site carries a Pauli-matrix realization. ∎

### Step 4 — Total Hilbert dim (D3)

Tensor product: `⊗_{x ∈ Λ} H_x` has dim `∏_x dim H_x = 2^{|Λ|}`. ∎

### Step 5 — No alternatives (D4)

Direct restatement: by uniqueness, no inequivalent representation exists. ∎

## Hypothesis set used

- `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained).
- A2 (Z^3 substrate, structural).
- Site Hilbert space = faithful irreducible Cl(3) rep (structural).

## Corollaries

C1. **Single qubit per Cl(3) site.** Each site is a "qubit" in QC terminology. Quantum-information operations on the framework's retained substrate map to multi-qubit operations on `2^|Λ|`-dim Hilbert space.

C2. **No bosonic CCR per site.** The bosonic canonical commutation relation `[a, a^†] = I` requires infinite-dimensional rep (Stone-von Neumann). Per-site dim 2 forbids bosonic CCR per site. Bosonic modes can exist as collective modes across many sites.

C3. **Pauli algebra per site.** The site operator algebra is `M_2(C) ≅ Cl(3) ⊗ C` (with the complex structure), exhausting all 2×2 complex matrices.

C4. **Total state-space size formula.** A finite cubic block of side L has `|Λ| = L^3` sites and `2^{L^3}` -dim total Hilbert space. Quickly intractable for direct numerical methods at large L.

## Honest status

Positive theorem on the retained surface. Single one-hop chain. Direct application of the retained per-site uniqueness theorem to the framework substrate.

```yaml
claim_type_author_hint: positive_theorem
claim_scope: "dim_C H_x = 2 for every lattice site; total dim_C = 2^|Λ| for finite block."
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29 (retained)
```
