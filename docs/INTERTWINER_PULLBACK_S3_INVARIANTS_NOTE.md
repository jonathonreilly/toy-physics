# Pullback of S_3 Invariants via the Site-Phase / Cube-Shift Intertwiner

**Status:** airtight (Grind Program, Batch 6)
**Runner:** `scripts/frontier_intertwiner_pullback_s3_invariants.py` (25/25 PASS)

## Classical results applied

- **Functoriality of commutants under equivariant isometries**
  (standard in representation theory; Serre, *Linear Representations
  of Finite Groups*, ch. 1-2). If Φ : V → W is a G-equivariant
  isometric embedding between G-modules, then the pullback map
  M ↦ Φ M Φ^† is a G-equivariant unital *-algebra homomorphism, and
  restricts to a bijection End(V)^G ≅ End(Φ(V))^G.
- **Isotypic decomposition + Schur's lemma** for the resulting
  commutant-dimension equalities.

## Framework-specific step

The Batch 1 Site-Phase / Cube-Shift Intertwiner Theorem supplies the
G-equivariant isometric embedding:

    Φ : C^8 → C^{L³}    (L even),
    Φ : |α⟩ ↦ |X_α⟩

where |X_α⟩(x) = exp(i π α · x) / √(L³) is the BZ-corner state for
α ∈ {0, 1}³, with Φ^† P_μ Φ = S_μ (site-phase pulls back to cube-
shift) and Φ U_{C^8}(π) = U_{L³}(π) Φ for all π ∈ S_3.

## Framework object

The pullback map M ↦ Φ M Φ^† from End(C^8) to End(Φ(C^8)) ⊂ End(C^{L³}).

## Theorem

The pullback M ↦ Φ M Φ^† is an S_3-equivariant unital *-algebra
homomorphism that restricts to a linear bijection

    End(C^8)^{S_3}  ≅  End(Φ(C^8))^{S_3}.

Consequently every S_3-invariant theorem on C^8 transports verbatim
to the BZ-corner subspace of the lattice C^{L³}:

1. Batch 3 S_3-Invariant Operator Dimension (dim 20 on C^8) ⟹
   dim End(Φ(C^8))^{S_3} = 20.

2. Batch 3 S_3 Hw-Parity Block Decomposition (20 = 10 + 10) and
   Batch 5 hw-graded decomposition (20 = 6 + 14) transport verbatim.

3. Batch 4 Cube-Shift Polynomial Algebra (dim 8) and
   S_3-Invariant Polynomial Subalgebra (dim 4) correspond to the
   site-phase polynomial algebra on the BZ-corner subspace and its
   S_3-invariant subalgebra.

4. Batch 4 S_3 Mass-Matrix No-Go on the hw=1 triplet transports:
   any S_3-invariant Hermitian operator on the hw=1 BZ-corner
   triplet has spectrum (α, α, α+β).

5. Batch 5 hw=1 ↔ hw=2 S_3-equivariant iso via e_3 transports: on
   the BZ-corner subspace the analogous iso V_1 ↔ V_2 is given by
   the site-phase product P_1 P_2 P_3 restricted to BZ corners.

## Proof sketch

(1) S_3-equivariance of Φ is the Batch 1 intertwiner statement.
(2) For any M ∈ End(C^8)^{S_3} and π ∈ S_3,

    U_{L³}(π) · Φ M Φ^†
      = Φ U_{C^8}(π) M Φ^†           (equivariance)
      = Φ M U_{C^8}(π) Φ^†           (S_3-invariance of M)
      = Φ M Φ^† · U_{L³}(π),          (equivariance)

so the pullback sends S_3-invariants to S_3-invariants. Injectivity:
the round-trip Φ^†(Φ M Φ^†)Φ = (Φ^†Φ) M (Φ^†Φ) = I_8 · M · I_8 = M.
Surjectivity: for any S_3-invariant N on Φ(C^8), set M := Φ^† N Φ;
the same equivariance argument shows M is S_3-invariant on C^8 and
Φ M Φ^† = N (using Φ Φ^† = projector onto Φ(C^8), and N = P_{Φ(C^8)}
N P_{Φ(C^8)} for any operator with support in Φ(C^8)).
*-algebra homomorphism: Φ (A B) Φ^† = Φ A (Φ^† Φ) B Φ^† =
(Φ A Φ^†)(Φ B Φ^†) using Φ^†Φ = I_8. The hw-grading, hw-parity,
and polynomial-subalgebra structures of Batches 3–5 are all defined
in terms of End(C^8)^{S_3} (and its subobjects); the bijection
carries each verbatim.

## Verification

The runner (a) builds Φ explicitly at L = 4 (64-dim lattice, 8-dim
BZ-corner image), (b) verifies Φ^†Φ = I_8, (c) verifies Φ^† P_μ Φ =
S_μ for all three μ, (d) verifies S_3-equivariance U_{L³}(π) Φ =
Φ U_{C^8}(π) against all six S_3 elements, (e) projects 64
Hermitian basis matrices to S_3-invariants on C^8 and pulls them
back, checking that every pullback is S_3-invariant on C^{L³} and
that the real dim is preserved (20 → 20), (f) verifies the
*-algebra homomorphism property Φ (M_1 M_2) Φ^† = (Φ M_1 Φ^†)(Φ M_2
Φ^†), (g) verifies the round-trip Φ^†(Φ A Φ^†)Φ = A certifying
bijectivity, (h) checks that the four hw projectors pushforward to
commuting idempotents summing to the BZ-corner subspace projector.

## Reusability

- Single citable result letting any framework lattice argument
  invoke the whole C^8-based theorem stack (Batches 3, 4, 5) on the
  BZ-corner subspace of C^{L³}, rather than re-deriving each result
  in site-phase language.
- Complements the Batch 1 intertwiner (which supplies the
  S_μ ↔ P_μ matching at the single-operator level) by extending
  the transport to full S_3-invariant algebraic structure
  (commutants, subalgebras, grading, no-gos).
