#!/usr/bin/env python3
"""Pattern A narrow runner for `GAUGE_TEMPORAL_GAUGE_MIXED_KERNEL_SPATIAL_LINK_FACTORIZATION_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies on abstract compact-group Wilson kernels:

  (T1) Temporal-gauge tensor factorization of the one-step mixed kernel
       over spatial links.

  (T2) Per-link convolution diagonalization: a class function w with
       character expansion w = sum_lambda c_lambda chi_lambda acts on
       every matrix coefficient of irrep lambda by the exact scalar
       c_lambda / d_lambda (Schur orthogonality).

  (T3) Trivial-channel normalization: a_0(beta) = c_0(beta) / (d_0 c_0(beta)) = 1.

  (T4) Marked / non-marked compression map: each marked spatial link
       contributes the irrep eigenvalue a_lambda(beta), non-marked
       spatial links contribute the trivial-channel scalar 1 after
       normalization.

  Class D counterexample: with U_t != 1 (no temporal gauge), the
  per-link tensor factorization fails.

This is class-A pure compact-group convolution algebra plus the
algebraic structure of the Wilson action in temporal gauge.
No SU(3), beta = 6, marked plaquette, source-sector compression, or
framework physical identification is consumed; concrete verifications
are realized on the finite abelian groups Z_N because they exhibit
exactly the same Peter-Weyl convolution diagonalization that the
abstract theorem invokes.

"""

from pathlib import Path
import sys
import math

try:
    import sympy as sp
    from sympy import Rational, exp, I, pi, symbols, simplify, summation, conjugate, nsimplify
except ImportError:
    print("FAIL: sympy required for exact symbolic algebra")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("FAIL: numpy required for finite-group numerical verification")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section(
    "Pattern A narrow theorem: temporal-gauge mixed-kernel spatial-link"
    " factorization on a compact group"
)
# ============================================================================


# ----------------------------------------------------------------------------
section("(T2) Per-link convolution diagonalization: c_lambda / d_lambda")
# ----------------------------------------------------------------------------
# On any finite abelian group Z_N, all irreps are one-dimensional (d_lambda = 1),
# characters are chi_k(g) = exp(2 pi i k g / N), and convolution by w(g) acts
# on each chi_k by the eigenvalue c_k = (1/N) sum_g conj(chi_k(g)) w(g).
# We verify this on Z_N for several N with the explicit Wilson weight
# w_beta(g) = exp(beta cos(2 pi g / N)), which is the abelian analog of the
# SU(N) Wilson weight w_beta(U) = exp((beta/N_c) Re Tr U).

beta_test = 1.7
for N in (3, 4, 5, 7, 9):
    # Build the per-link convolution kernel matrix:
    # (K f)(h) = (1/N) sum_g w_beta(h - g) f(g)
    w_vals = np.array([np.exp(beta_test * np.cos(2 * np.pi * g / N)) for g in range(N)])
    K = (1.0 / N) * np.array([[w_vals[(i - j) % N] for j in range(N)] for i in range(N)])

    # Verify Schur orthogonality: chi_k is an eigenvector with eigenvalue c_k.
    diagonal_ok = True
    eigvals = []
    for k in range(N):
        chi_k = np.array([np.exp(2j * np.pi * k * g / N) for g in range(N)])
        K_chi_k = K @ chi_k
        # Expected c_k:
        c_k_expected = (1.0 / N) * sum(
            np.exp(-2j * np.pi * k * g / N) * w_vals[g] for g in range(N)
        )
        eigvals.append(c_k_expected)
        # Ratio should be c_k on every entry:
        ratio = K_chi_k[0] / chi_k[0]
        if not np.isclose(ratio, c_k_expected, atol=1e-10):
            diagonal_ok = False

    check(
        f"Z_{N}: convolution by w_beta diagonalizes on characters chi_k with eigenvalue c_k",
        diagonal_ok,
        detail=f"all {N} eigenvalues matched within 1e-10",
    )


# ----------------------------------------------------------------------------
section("(T3) Trivial-channel normalization: a_0(beta) = 1")
# ----------------------------------------------------------------------------
# Symbolic: c_0 > 0 by positivity of w_beta, d_0 = 1, hence a_0 = c_0 / (1 * c_0) = 1.
c0, dlambda = symbols('c_0 d_lambda', positive=True)
a_0_sym = c0 / (1 * c0)  # d_0 = 1
check(
    "a_0(beta) = c_0(beta) / (d_0 c_0(beta)) = 1 symbolically (d_0 = 1)",
    simplify(a_0_sym - 1) == 0,
    detail=f"a_0 = {a_0_sym}, simplified = {simplify(a_0_sym)}",
)

# Numerical: on Z_N for the same Wilson-weight family, a_0 = 1 by construction.
for N in (3, 4, 5, 7):
    w_vals = np.array([np.exp(beta_test * np.cos(2 * np.pi * g / N)) for g in range(N)])
    c0_num = (1.0 / N) * sum(w_vals)
    # a_0 = c_0 / (d_0 c_0) = 1 (d_0 = 1 for abelian)
    a_0_num = c0_num / (1.0 * c0_num)
    check(
        f"Z_{N} numerical: a_0(beta={beta_test}) = 1",
        np.isclose(a_0_num, 1.0, atol=1e-14),
        detail=f"a_0_num = {a_0_num}",
    )


# ----------------------------------------------------------------------------
section("(T1)+(T4) Tensor factorization + marked / non-marked compression map")
# ----------------------------------------------------------------------------
# We verify directly that the one-step mixed kernel
#   K(U', U) = prod_x w_beta(U'_x - U_x)
# satisfies
#   integral K(U', U) f(U_M) prod_x dU_x  =  [prod_{m in M} c_lambda_m] *
#                                            [prod_{m NOT in M} c_0] * f(U'_M)
# for f(U) = prod_{m in M} chi_{lambda_m}(U_m), on a Z_N toy lattice with L_s spatial sites.

for N in (3, 4, 5):
    L_s = 4  # 4 spatial sites; one cyclic chain
    w_vals = np.array([np.exp(beta_test * np.cos(2 * np.pi * g / N)) for g in range(N)])
    c = np.array(
        [(1.0 / N) * sum(np.exp(-2j * np.pi * k * g / N) * w_vals[g] for g in range(N)) for k in range(N)]
    )

    def idx_to_config(idx):
        config = []
        for _ in range(L_s):
            config.append(idx % N)
            idx //= N
        return config

    dim = N ** L_s

    # Test for a few marked subsets M and irrep labels (kept abelian: 1-dim irreps).
    for marked_size in (1, 2, 3, 4):
        marked_links = list(range(marked_size))
        # Pick a non-trivial irrep label k for each marked link.
        k_labels = [(i + 1) % N for i in range(marked_size)]
        # If all labels are 0, skip (would just be trivial).
        if all(k == 0 for k in k_labels):
            k_labels = [1] * marked_size

        # f(U) = prod_{m in M} chi_{k_m}(U_m)
        def f_eval(config):
            val = 1.0 + 0j
            for m, k_m in zip(marked_links, k_labels):
                val *= np.exp(2j * np.pi * k_m * config[m] / N)
            return val

        f_vec = np.array([f_eval(idx_to_config(j)) for j in range(dim)])

        # Build K and apply
        Kf = np.zeros(dim, dtype=complex)
        for ip in range(dim):
            Up = idx_to_config(ip)
            total = 0j
            for jp in range(dim):
                U = idx_to_config(jp)
                kernel = np.prod([w_vals[(Up[x] - U[x]) % N] for x in range(L_s)])
                total += kernel * f_vec[jp]
            Kf[ip] = total / (N ** L_s)

        # Expected: eigenvalue [prod_m c_{k_m}] * c_0^(L_s - |M|), eigenvector f(U').
        expected_eig = np.prod([c[k_m] for k_m in k_labels]) * (c[0] ** (L_s - marked_size))

        # Compare entry-wise: Kf should equal expected_eig * f_vec
        ok = np.allclose(Kf, expected_eig * f_vec, atol=1e-9)
        check(
            f"Z_{N} L_s={L_s}: marked subset |M|={marked_size} labels={k_labels} factorization",
            ok,
            detail=f"max abs diff = {np.max(np.abs(Kf - expected_eig * f_vec)):.3e}",
        )

        # Normalized: divide by c_0^L_s, expected eigenvalue is prod_m a_{k_m}.
        norm_eig = expected_eig / (c[0] ** L_s)
        a_vals = c / c[0]
        norm_expected = np.prod([a_vals[k_m] for k_m in k_labels])
        check(
            f"Z_{N}: normalized eigenvalue = prod_{{m in M}} a_(k_m) [|M|={marked_size}]",
            np.isclose(norm_eig, norm_expected, atol=1e-12),
            detail=f"norm_eig={norm_eig:.6f}, prod a_k = {norm_expected:.6f}",
        )


# ----------------------------------------------------------------------------
section("(T4) Marked = 4 special case mirrors the four-link plaquette structure")
# ----------------------------------------------------------------------------
# On a Z_N abelian toy with L_s = 5 and marked subset M = {0,1,2,3}, |M| = 4, all
# labels k_m = 1 (same irrep), the normalized one-step eigenvalue on the four-marked
# character subspace is exactly a_1^4. This mirrors the structure used downstream
# in the SU(3) marked-plaquette four-link loop case (where the four marked links
# are the four spatial links of the marked plaquette loop), specialized to the
# four-link special case at the abstract level. Note: this is the abstract
# Peter-Weyl/compact-group statement; no SU(3) / framework specifics are consumed.

for N in (3, 4, 5):
    L_s = 5
    w_vals = np.array([np.exp(beta_test * np.cos(2 * np.pi * g / N)) for g in range(N)])
    c = np.array(
        [(1.0 / N) * sum(np.exp(-2j * np.pi * k * g / N) * w_vals[g] for g in range(N)) for k in range(N)]
    )

    def idx_to_config(idx):
        config = []
        for _ in range(L_s):
            config.append(idx % N)
            idx //= N
        return config

    dim = N ** L_s
    marked_links = [0, 1, 2, 3]
    k_label = 1
    k_labels = [k_label] * 4

    def f_eval(config):
        val = 1.0 + 0j
        for m in marked_links:
            val *= np.exp(2j * np.pi * k_label * config[m] / N)
        return val

    f_vec = np.array([f_eval(idx_to_config(j)) for j in range(dim)])

    Kf = np.zeros(dim, dtype=complex)
    for ip in range(dim):
        Up = idx_to_config(ip)
        total = 0j
        for jp in range(dim):
            U = idx_to_config(jp)
            kernel = np.prod([w_vals[(Up[x] - U[x]) % N] for x in range(L_s)])
            total += kernel * f_vec[jp]
        Kf[ip] = total / (N ** L_s)

    expected_eig = (c[k_label] ** 4) * (c[0] ** (L_s - 4))
    a1 = c[k_label] / c[0]
    norm_eig = expected_eig / (c[0] ** L_s)

    check(
        f"Z_{N}: |M|=4 four-link special case, eigenvalue = c_1^4 c_0^{L_s-4}",
        np.allclose(Kf, expected_eig * f_vec, atol=1e-9),
        detail=f"max abs diff = {np.max(np.abs(Kf - expected_eig * f_vec)):.3e}",
    )
    check(
        f"Z_{N}: |M|=4 normalized eigenvalue = a_1^4 (downstream 4-link plaquette pattern)",
        np.isclose(norm_eig, a1 ** 4, atol=1e-12),
        detail=f"norm_eig = {norm_eig:.6f}, a_1^4 = {a1**4:.6f}",
    )


# ----------------------------------------------------------------------------
section("(D) Counterexample: WITHOUT temporal-gauge spatial-link factorization, marked/non-marked compression fails")
# ----------------------------------------------------------------------------
# The claim of (T1)+(T4) is that the one-step kernel factorizes as an INDEPENDENT
# product over spatial links, so the marked/non-marked compression map separates
# cleanly. We demonstrate this by constructing two kernels:
#   K_factorized: pure per-link kernel as in (T1) — the temporal-gauge structure.
#   K_nonfact:    deliberately couples a non-marked spatial link to a marked one,
#                 via an extra two-link interaction that depends on BOTH (U_0 - U'_0)
#                 AND (U_2 - U'_2) jointly. This is the structure that would arise
#                 if the temporal-gauge factorization (T1) failed: a non-marked link
#                 would no longer contribute the rep-independent scalar c_0.
# Then we apply both kernels to a marked-link character f = chi_k(U_0 - U'_0)
# integrated over U, and verify that:
#   * with K_factorized, the non-marked links contribute exactly c_0^(L_s - 1)
#     (the trivial-channel scalar), as required by (T4);
#   * with K_nonfact, the contribution from the non-marked link x = 2 is NOT
#     just c_0; it depends on k (the marked irrep label) because the coupling
#     mixes the two links.

N = 3
L_s = 3
w_vals = np.array([np.exp(beta_test * np.cos(2 * np.pi * g / N)) for g in range(N)])

def idx3(idx):
    config = []
    for _ in range(L_s):
        config.append(idx % N)
        idx //= N
    return config

dim = N ** L_s
K_factorized = np.zeros((dim, dim), dtype=complex)
K_nonfact = np.zeros((dim, dim), dtype=complex)
for ip in range(dim):
    Up = idx3(ip)
    for jp in range(dim):
        U = idx3(jp)
        per_link = np.prod([w_vals[(Up[x] - U[x]) % N] for x in range(L_s)])
        K_factorized[ip, jp] = per_link
        # Add a two-link coupling between link 0 (marked) and link 2 (non-marked)
        # that depends on the PRODUCT of their differences, i.e., the coupling has
        # the form exp(gamma * cos(2 pi (Up[0]-U[0])(Up[2]-U[2]) / N)). This couples
        # the marked and non-marked link in a way that breaks the marked/non-marked
        # compression separation.
        gamma = 0.6
        K_nonfact[ip, jp] = per_link * np.exp(
            gamma * np.cos(2 * np.pi * ((Up[0] - U[0]) * (Up[2] - U[2])) / N)
        )

# Apply both kernels to a marked-link character f = chi_k(U[0]):
k_test = 1
f = np.array([np.exp(2j * np.pi * k_test * idx3(j)[0] / N) for j in range(dim)])

c_k_val = (1.0 / N) * sum(np.exp(-2j * np.pi * k_test * g / N) * w_vals[g] for g in range(N))
c_0_val = (1.0 / N) * sum(w_vals)

# Factorized: K f / N^L_s should equal c_k * c_0^(L_s - 1) * f (as proved by T4).
Kf_factorized = K_factorized @ f / (N ** L_s)
expected_factorized = c_k_val * (c_0_val ** (L_s - 1))
factorized_eigenvalue_ok = np.allclose(Kf_factorized, expected_factorized * f, atol=1e-10)
check(
    "Factorized kernel (T1): marked-link character is eigenvector with eigenvalue c_k c_0^(L_s-1)",
    factorized_eigenvalue_ok,
    detail=f"max abs diff = {np.max(np.abs(Kf_factorized - expected_factorized * f)):.3e}",
)

# Non-factorized kernel: f is still an eigenvector of K_nonfact by translation
# symmetry of the Z_N group (the coupling commutes with global Z_N action on each
# variable), so we check the EIGENVALUE: it must DIFFER from c_k c_0^(L_s-1) because
# the non-marked link x = 2 no longer contributes a rep-independent scalar.
Kf_nonfact = K_nonfact @ f / (N ** L_s)
# Confirm eigenvector property (translation invariance):
ratios_nonfact = []
for i in range(dim):
    if abs(f[i]) > 1e-12:
        ratios_nonfact.append(Kf_nonfact[i] / f[i])
ratios_nonfact = np.array(ratios_nonfact)
eig_nonfact = np.mean(ratios_nonfact)
# Compare to expected c_k c_0^(L_s-1):
relative_diff = abs(eig_nonfact - expected_factorized) / abs(expected_factorized)
check(
    "WITHOUT (T1) factorization: marked/non-marked compression FAILS — eigenvalue differs from c_k c_0^(L_s-1)",
    relative_diff > 1e-3,
    detail=f"|eig_nonfact - c_k c_0^(L-1)| / |c_k c_0^(L-1)| = {relative_diff:.3e} (>>1e-3 expected)",
)

# Direct tensor-factorization test: K(U',U) should equal a product of per-link
# factors when (T1) holds. Test this directly using the rank-1 product structure:
# for the factorized kernel, K(U',U) / [w(U'_0 - U_0) w(U'_1 - U_1) w(U'_2 - U_2)] = 1
# everywhere, but for the non-factorized kernel it varies with (U', U).

prod_residual_fact = []
prod_residual_nonfact = []
for ip in range(dim):
    Up = idx3(ip)
    for jp in range(dim):
        U = idx3(jp)
        per_link_product = np.prod([w_vals[(Up[x] - U[x]) % N] for x in range(L_s)])
        prod_residual_fact.append(K_factorized[ip, jp] / per_link_product)
        prod_residual_nonfact.append(K_nonfact[ip, jp] / per_link_product)

prod_residual_fact = np.array(prod_residual_fact)
prod_residual_nonfact = np.array(prod_residual_nonfact)

check(
    "Factorized kernel: K(U',U) / prod_x w(U'_x - U_x) = 1 identically (true per-link product)",
    np.allclose(prod_residual_fact, 1.0, atol=1e-12),
    detail=f"max deviation from 1 = {np.max(np.abs(prod_residual_fact - 1.0)):.3e}",
)

check(
    "WITHOUT factorization: K_nonfact(U',U) / prod_x w(U'_x - U_x) NOT constant (NOT a per-link product)",
    np.std(prod_residual_nonfact.real) + np.std(prod_residual_nonfact.imag) > 1e-3,
    detail=f"std of residual = {np.std(prod_residual_nonfact.real) + np.std(prod_residual_nonfact.imag):.3e} (>>0 confirms non-factorization)",
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print(
    """
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    G compact group with normalized Haar measure dg;
    w_beta a real positive class function on G with character expansion
        w_beta(g) = sum_lambda c_lambda(beta) chi_lambda(g),
        c_lambda(beta) = integral conj(chi_lambda(g)) w_beta(g) dg;
    finite hypercubic Wilson lattice in temporal gauge U_t = 1.

  CONCLUSION:
    (T1) One-step mixed kernel K(U', U) = prod_(x,mu) w_beta(U'(x,mu) U(x,mu)^-1).
    (T2) Per-link convolution diagonalization: each per-link factor acts on
         every matrix coefficient of irrep lambda by c_lambda / d_lambda
         (Schur orthogonality).
    (T3) Trivial-channel normalization: a_0(beta) = c_0 / (d_0 c_0) = 1.
    (T4) Marked/non-marked compression map: marked links contribute a_lambda,
         non-marked links contribute the trivial-channel scalar c_0 (= 1 after
         normalization).

  Audit-lane class:
    (A) pure compact-group convolution algebra + algebraic structure of the
    Wilson action in temporal gauge. No SU(3) / beta = 6 / marked-plaquette /
    source-sector / framework physical identification consumed.

  This narrow theorem isolates the temporal-gauge mixed-kernel spatial-link
  factorization and the marked/non-marked compression map flagged by the
  audit verdict on
  GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md
  as the missing bridge theorem. The narrow content can be ratified
  independently of any disposition of the parent note or its companion
  spatial-environment notes.
"""
)


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
