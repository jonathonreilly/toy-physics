#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`FERMION_PARITY_PAULI_TENSOR_INVOLUTION_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is the Pauli-tensor-algebra
identity that on an N-site `⊗ ℂ²` Fock space the operator
F := ⊗_x σ_3^{(x)} is a Hermitian unitary involution with spectrum {+1, -1},
balanced 2^{N-1}-dim grading, and Z_2-odd / Z_2-even action on the per-site
ladder operators and bilinears.

This is the (P1)-(P7) clause of the parent
`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02`, isolated from (F8)
dynamical conservation `[F, H] = 0`, which requires a Hamiltonian and the
lattice Noether authority.

This Pattern A audit companion provides sympy-symbolic exact-precision
verification on the concrete N = 3 case:

  (a) verifies per-site Pauli identities (σ_3² = I, {σ_3, σ_+} = 0, etc.);
  (b) constructs F_3 = σ_3 ⊗ σ_3 ⊗ σ_3 on the 8-dim Fock space and verifies
      Hermiticity, unitarity, F_3² = I, spectrum {+1, -1} with balanced
      multiplicity 4 = 2^{3-1};
  (c) verifies F_3 |ν> = (-1)^{Q(ν)} |ν> on each of the 8 occupation states;
  (d) verifies {F_3, σ_+^{(x)}} = 0 and {F_3, σ_-^{(x)}} = 0 exact for
      x = 1, 2, 3 (Z_2-odd action on ladder ops);
  (e) verifies [F_3, n̂_x] = 0 and [F_3, σ_+^{(x)} σ_-^{(y)}] = 0 exact for
      all (x, y) (Z_2-even action on bilinears);
  (f) verifies [F_3, Q̂_total] = 0 exact;
  (g) verifies the combinatorial identity dim(H_even) = dim(H_odd) = 2^{N-1}
      for N ∈ {1, 2, 3, 4, 5};
  (h) verifies F_3 = exp(i π Q̂_total) on the spectral expansion;
  (i) counterfactual: F_3 σ_+^{(x)} F_3 = -σ_+^{(x)} (Z_2-odd conjugation).

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow theorem's
load-bearing class-(A) Pauli-tensor identity holds at exact symbolic
precision.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import (
        Matrix, eye, zeros, symbols, simplify, sympify, Rational, exp, I,
        pi, log, sqrt, binomial, factorial, Sum, Symbol
    )
    from sympy.physics.quantum import TensorProduct
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def embed_3site(op_1: Matrix, op_2: Matrix, op_3: Matrix) -> Matrix:
    """Build 8x8 tensor product op_1 ⊗ op_2 ⊗ op_3 on (ℂ²)^⊗3."""
    return TensorProduct(op_1, TensorProduct(op_2, op_3))


def occupation_basis_vector(nu1: int, nu2: int, nu3: int) -> Matrix:
    """Build the 8-component column vector for occupation state |nu1, nu2, nu3>.
    Convention: |0> = (1, 0), |1> = (0, 1) per site."""
    bra_0 = Matrix([[1], [0]])
    bra_1 = Matrix([[0], [1]])
    def per_site(nu):
        return bra_1 if nu == 1 else bra_0
    return TensorProduct(per_site(nu1), TensorProduct(per_site(nu2), per_site(nu3)))


def main() -> int:
    global PASS, FAIL

    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("fermion_parity_pauli_tensor_involution_narrow_theorem_note_2026-05-10")
    print("Goal: sympy-symbolic verification of (P1)-(P7) Pauli-tensor identity")
    print("on N = 3 site Fock space `(ℂ²)^⊗3`")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: per-site Pauli generators and identity")
    # ---------------------------------------------------------------------
    I2 = eye(2)
    sigma_3 = Matrix([[1, 0], [0, -1]])
    sigma_plus = Matrix([[0, 1], [0, 0]])
    sigma_minus = Matrix([[0, 0], [1, 0]])
    n_hat = sigma_minus * sigma_plus  # = diag(0, 1)

    check("σ_3² = I per site", sigma_3 * sigma_3 == I2)
    check("{σ_3, σ_+} = 0 per site",
          sigma_3 * sigma_plus + sigma_plus * sigma_3 == zeros(2, 2))
    check("{σ_3, σ_-} = 0 per site",
          sigma_3 * sigma_minus + sigma_minus * sigma_3 == zeros(2, 2))
    check("σ_+ σ_- + σ_- σ_+ = I per site",
          sigma_plus * sigma_minus + sigma_minus * sigma_plus == I2)
    check("n̂ = σ_- σ_+ = (I - σ_3)/2 per site",
          n_hat == (I2 - sigma_3) / 2,
          detail=f"n̂ = {n_hat}")
    check("Spec(n̂) = {0, 1} per site",
          n_hat == Matrix([[0, 0], [0, 1]]))

    # ---------------------------------------------------------------------
    section("Part 1: (P1)-(P3) F_3 := σ_3 ⊗ σ_3 ⊗ σ_3 on (ℂ²)^⊗3")
    # ---------------------------------------------------------------------
    F3 = embed_3site(sigma_3, sigma_3, sigma_3)
    I8 = eye(8)

    check("F_3 = σ_3 ⊗ σ_3 ⊗ σ_3 is Hermitian (F_3 = F_3^†)",
          F3 == F3.conjugate().transpose())
    check("F_3 is unitary (F_3^† F_3 = I_8)",
          F3.conjugate().transpose() * F3 == I8)
    check("F_3² = I_8 exact (involution P3)",
          F3 * F3 == I8)

    # ---------------------------------------------------------------------
    section("Part 2: (P4) spectrum {+1, -1} and (P5) Z_2 grading")
    # ---------------------------------------------------------------------
    # Spectrum check: F_3 is diagonal (tensor product of diagonals), so
    # spectrum is the set of diagonal entries.
    F3_diagonal = [F3[i, i] for i in range(8)]
    check("Spec(F_3) ⊆ {+1, -1} (diagonal entries)",
          set(F3_diagonal) == {1, -1},
          detail=f"diagonal entries = {F3_diagonal}")

    plus_count = sum(1 for v in F3_diagonal if v == 1)
    minus_count = sum(1 for v in F3_diagonal if v == -1)
    check("dim(H_even) = dim(H_odd) = 2^{3-1} = 4 (balanced grading P5)",
          plus_count == 4 and minus_count == 4,
          detail=f"+1 eigenvalues: {plus_count}, -1 eigenvalues: {minus_count}")

    # ---------------------------------------------------------------------
    section("Part 3: (P1) explicit F_3 |ν> = (-1)^{Q(ν)} |ν> on all 8 states")
    # ---------------------------------------------------------------------
    for nu1 in (0, 1):
        for nu2 in (0, 1):
            for nu3 in (0, 1):
                ket = occupation_basis_vector(nu1, nu2, nu3)
                F3_ket = F3 * ket
                Q = nu1 + nu2 + nu3
                expected = ((-1) ** Q) * ket
                check(
                    f"F_3 |{nu1},{nu2},{nu3}> = (-1)^{Q} |{nu1},{nu2},{nu3}> exact",
                    F3_ket == expected,
                    detail=f"sign = {(-1) ** Q}",
                )

    # ---------------------------------------------------------------------
    section("Part 4: (P6) {F_3, σ_±^{(x)}} = 0 for x = 1, 2, 3")
    # ---------------------------------------------------------------------
    sigma_plus_at_1 = embed_3site(sigma_plus, I2, I2)
    sigma_plus_at_2 = embed_3site(I2, sigma_plus, I2)
    sigma_plus_at_3 = embed_3site(I2, I2, sigma_plus)
    sigma_minus_at_1 = embed_3site(sigma_minus, I2, I2)
    sigma_minus_at_2 = embed_3site(I2, sigma_minus, I2)
    sigma_minus_at_3 = embed_3site(I2, I2, sigma_minus)

    Z8 = zeros(8, 8)
    check("{F_3, σ_+^{(1)}} = 0 exact",
          F3 * sigma_plus_at_1 + sigma_plus_at_1 * F3 == Z8)
    check("{F_3, σ_+^{(2)}} = 0 exact",
          F3 * sigma_plus_at_2 + sigma_plus_at_2 * F3 == Z8)
    check("{F_3, σ_+^{(3)}} = 0 exact",
          F3 * sigma_plus_at_3 + sigma_plus_at_3 * F3 == Z8)
    check("{F_3, σ_-^{(1)}} = 0 exact",
          F3 * sigma_minus_at_1 + sigma_minus_at_1 * F3 == Z8)
    check("{F_3, σ_-^{(2)}} = 0 exact",
          F3 * sigma_minus_at_2 + sigma_minus_at_2 * F3 == Z8)
    check("{F_3, σ_-^{(3)}} = 0 exact",
          F3 * sigma_minus_at_3 + sigma_minus_at_3 * F3 == Z8)

    # ---------------------------------------------------------------------
    section("Part 5: (P7) [F_3, n̂_x] = 0 and [F_3, σ_+^{(x)} σ_-^{(y)}] = 0")
    # ---------------------------------------------------------------------
    n_hat_at_1 = embed_3site(n_hat, I2, I2)
    n_hat_at_2 = embed_3site(I2, n_hat, I2)
    n_hat_at_3 = embed_3site(I2, I2, n_hat)

    check("[F_3, n̂_1] = 0 exact (n̂_1 is Z_2-even bilinear)",
          F3 * n_hat_at_1 - n_hat_at_1 * F3 == Z8)
    check("[F_3, n̂_2] = 0 exact",
          F3 * n_hat_at_2 - n_hat_at_2 * F3 == Z8)
    check("[F_3, n̂_3] = 0 exact",
          F3 * n_hat_at_3 - n_hat_at_3 * F3 == Z8)

    # All bilinears σ_+^{(x)} σ_-^{(y)} for (x, y) ∈ {1,2,3}²
    ladder_plus = [sigma_plus_at_1, sigma_plus_at_2, sigma_plus_at_3]
    ladder_minus = [sigma_minus_at_1, sigma_minus_at_2, sigma_minus_at_3]
    for x_idx in range(3):
        for y_idx in range(3):
            biln = ladder_plus[x_idx] * ladder_minus[y_idx]
            check(
                f"[F_3, σ_+^{x_idx+1} σ_-^{y_idx+1}] = 0 exact (Z_2-even bilinear)",
                F3 * biln - biln * F3 == Z8,
            )

    # ---------------------------------------------------------------------
    section("Part 6: [F_3, Q̂_total] = 0 exact")
    # ---------------------------------------------------------------------
    Q_total = n_hat_at_1 + n_hat_at_2 + n_hat_at_3
    check("[F_3, Q̂_total = n̂_1 + n̂_2 + n̂_3] = 0 exact",
          F3 * Q_total - Q_total * F3 == Z8)

    # ---------------------------------------------------------------------
    section("Part 7: combinatorial dim balance for N ∈ {1, 2, 3, 4, 5}")
    # ---------------------------------------------------------------------
    for N_val in (1, 2, 3, 4, 5):
        even_sum = sum(int(binomial(N_val, k)) for k in range(0, N_val + 1, 2))
        odd_sum = sum(int(binomial(N_val, k)) for k in range(1, N_val + 1, 2))
        target = 2 ** (N_val - 1)
        check(
            f"∑_{{k even}} C({N_val}, k) = ∑_{{k odd}} C({N_val}, k) = 2^{N_val - 1}",
            even_sum == odd_sum == target,
            detail=f"even = {even_sum}, odd = {odd_sum}, 2^{{N-1}} = {target}",
        )

    # ---------------------------------------------------------------------
    section("Part 8: F_3 = exp(i π Q̂_total) on diagonal")
    # ---------------------------------------------------------------------
    # Spec(Q̂_total) on the 8 occupation states = {0, 1, 1, 1, 2, 2, 2, 3}
    # (each Q-value appears C(3, Q) times).
    # exp(i π k) = (-1)^k for integer k.
    # Build the diagonal expansion of exp(i π Q̂_total):
    exp_i_pi_Q = Matrix.diag(*[(-1) ** (Q_total[i, i]) for i in range(8)])
    check(
        "F_3 = exp(i π Q̂_total) exact on the 8-dim occupation basis",
        F3 == exp_i_pi_Q,
        detail=f"diagonal Q-values give {[(-1) ** (Q_total[i, i]) for i in range(8)]}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: counterfactual probes — Z_2-odd conjugation")
    # ---------------------------------------------------------------------
    # F_3 · σ_+^{(1)} · F_3 = -σ_+^{(1)} (Z_2-odd ⇒ sign-flip under conjugation)
    conj_plus_1 = F3 * sigma_plus_at_1 * F3
    check(
        "F_3 σ_+^{(1)} F_3 = -σ_+^{(1)} exact (Z_2-odd conjugation, P6 directional)",
        conj_plus_1 == -sigma_plus_at_1,
        detail="confirms Z_2-odd direction of {F, σ_+} = 0",
    )

    # Z_2-even conjugation: F_3 · (σ_+^{(1)} σ_-^{(2)}) · F_3 = +σ_+^{(1)} σ_-^{(2)}
    biln_12 = sigma_plus_at_1 * sigma_minus_at_2
    conj_biln_12 = F3 * biln_12 * F3
    check(
        "F_3 σ_+^{(1)} σ_-^{(2)} F_3 = +σ_+^{(1)} σ_-^{(2)} exact (Z_2-even bilinear)",
        conj_biln_12 == biln_12,
        detail="confirms Z_2-even direction of [F, bilinear] = 0",
    )

    # Counterfactual: same-site bilinear σ_+^{(1)} σ_-^{(1)} = n̂_1 is also Z_2-even
    conj_n1 = F3 * n_hat_at_1 * F3
    check(
        "F_3 n̂_1 F_3 = n̂_1 exact (Z_2-even bilinear, same site)",
        conj_n1 == n_hat_at_1,
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision on N = 3 site Fock space:")
    print("    (P1) F_3 = σ_3 ⊗ σ_3 ⊗ σ_3 = exp(i π Q̂_total) on all 8 states")
    print("    (P2) F_3 Hermitian (F_3 = F_3^†)")
    print("    (P3) F_3² = I_8 exact (involution)")
    print("    (P4) Spec(F_3) = {+1, -1} exact (diagonal entries)")
    print("    (P5) dim(H_+) = dim(H_-) = 4 = 2^{3-1} (balanced grading)")
    print("    (P6) {F_3, σ_±^{(x)}} = 0 exact for x = 1, 2, 3")
    print("    (P7) [F_3, n̂_x] = 0 and [F_3, bilinear] = 0 exact for all (x,y)")
    print("    [F_3, Q̂_total] = 0 exact")
    print("    Combinatorial ∑ C(N,2k) = ∑ C(N, 2k+1) = 2^{N-1} for N=1..5")
    print("    Counterfactual Z_2-odd conjugation F σ_+ F = -σ_+ confirmed")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
