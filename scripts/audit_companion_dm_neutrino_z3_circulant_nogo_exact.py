#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15`
(claim_type=no_go, load_bearing_step_class=A).

The parent's load-bearing step is the algebraic identity that any exact
Z_3-covariant circulant kernel

      K = d I + r (chi S + chi* S^2)

(where chi is a true Z_3 character, S is the 3-cycle permutation matrix)
has a REAL spectrum, and therefore in the heavy-neutrino mass basis (where
M_R = diag(A) + real_symmetric block) the kernel K_mass remains real
symmetric, hence Im[(K_mass)_{1j}^2] = 0 for all j.

This Pattern B companion verifies the algebra at sympy `Rational` / exact
symbolic precision via:
  1. S^3 = I exact;
  2. K eigenvalues are real (closed-form chi-arithmetic);
  3. M_R real-symmetric diagonalization is real orthogonal;
  4. K_mass = O^T K_diag O remains real symmetric;
  5. Im[(K_mass)_{1j}^2] = 0 verified at concrete chi in {1, omega, omega-bar}.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's load-bearing class-(A) algebra
holds at exact precision. Does not modify the parent row's status; that
decision belongs to the independent audit lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Matrix, Rational, sqrt, exp, I, pi, simplify, eye, zeros
except ImportError:
    print("FAIL: sympy required for exact algebra")
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
section("Audit companion for dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15 (td=144)")
# Goal: exact symbolic verification of the no-go's class-(A) load-bearing
# algebra: every exact Z_3-covariant circulant K has a real spectrum;
# M_R diagonalization is real-orthogonal; K_mass stays real symmetric;
# Im[(K_mass)_{1j}^2] = 0.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: 3-cycle permutation matrix S satisfies S^3 = I exactly")
# ----------------------------------------------------------------------------
# S is the cyclic shift on Z_3:  S e_k = e_{k+1 mod 3}
S = Matrix([[0, 0, 1],
            [1, 0, 0],
            [0, 1, 0]])

S_squared = S * S
S_cubed = S * S * S
I3 = eye(3)
check("S^3 = I exact",
      S_cubed == I3,
      detail=f"S^3 - I = {S_cubed - I3}")
check("S^2 != I (S is genuine 3-cycle)",
      S_squared != I3)


# ----------------------------------------------------------------------------
section("Part 2: K = d I + r(chi S + chi* S^2) eigenvalues are real for unit-modulus chi")
# ----------------------------------------------------------------------------
# Eigenvalues of S are 1, omega, omega^2 (cube roots of unity).
# For K = d I + r(chi S + chi* S^2), the eigenvalues are
#   lambda_k = d + r(chi * omega^k + chi* * omega^{2k}),  k = 0, 1, 2.
# Note omega^{2k} = omega^{-k} mod 3, and chi* = 1/chi for unit-modulus chi,
# so lambda_k = d + r(chi * omega^k + (chi * omega^k)*) = d + 2 r Re(chi * omega^k),
# which is REAL.

omega = exp(I * 2 * pi / Rational(3))
omega_bar = exp(-I * 2 * pi / Rational(3))

# Test chi values: 1, omega, omega-bar
for chi_label, chi_val in [("chi=1", 1), ("chi=omega", omega), ("chi=omega-bar", omega_bar)]:
    chi_star = sympy.conjugate(chi_val)
    # Eigenvalues at k = 0, 1, 2
    eigenvalues = []
    for k in [0, 1, 2]:
        omega_k = omega**k
        omega_neg_k = omega**(-k)
        # eigenvalue: d + r * (chi * omega^k + chi* * omega^{-k})
        # for symbolic verification we'll use abstract d, r and check imaginary part
        lam_real_part = chi_val * omega_k + chi_star * omega_neg_k
        # Force trig reduction so sympy can confirm imaginary part is zero
        lam_real_part_reduced = simplify(lam_real_part.rewrite(sympy.cos).expand(complex=True))
        eigenvalues.append(lam_real_part_reduced)

    # Check that all three "spectral coefficients" are real (imaginary part zero)
    imaginary_parts_zero = all(
        simplify(sympy.im(lam)) == 0 for lam in eigenvalues
    )
    check(f"{chi_label}: K eigenvalue spectral coefficients (chi*om^k + chi*'*om^-k) are real",
          imaginary_parts_zero,
          detail=f"eigenvalues = {eigenvalues}")


# ----------------------------------------------------------------------------
section("Part 3: M_R block-form gives real orthogonal diagonalization in doublet block")
# ----------------------------------------------------------------------------
# On the current denominator stack, M_R in the Z_3 basis is
#     M_R = [[A, 0, 0],
#            [0, eps, B],
#            [0, B, eps]]
# with real A, eps, B. So the only nontrivial diagonalization sits in the
# 2x2 doublet block, which is real symmetric. Real-symmetric matrices
# diagonalize via real orthogonal transformations.

A_sym, eps_sym, B_sym = sympy.symbols('A eps B', real=True)
M_R = Matrix([
    [A_sym, 0, 0],
    [0, eps_sym, B_sym],
    [0, B_sym, eps_sym],
])

# Verify M_R is real symmetric
check("M_R is symmetric exact (M_R = M_R^T)",
      M_R == M_R.T)
check("M_R has all real entries (A, eps, B real symbols)",
      all(entry.is_real or entry == 0 for entry in M_R))

# The 2x2 doublet block diagonalizes by the orthogonal matrix
#     O_2 = (1/sqrt(2)) * [[1, 1], [1, -1]]
# with eigenvalues eps + B, eps - B.
O_2 = Matrix([[1, 1], [1, -1]]) / sqrt(2)
diag_block = O_2 * Matrix([[eps_sym, B_sym], [B_sym, eps_sym]]) * O_2.T
diag_block_simplified = simplify(diag_block)
expected_diag = Matrix([[eps_sym + B_sym, 0], [0, eps_sym - B_sym]])
check("doublet block diagonalizes via real orthogonal O_2: O_2 [[eps,B],[B,eps]] O_2^T = diag(eps+B, eps-B)",
      simplify(diag_block_simplified - expected_diag) == zeros(2, 2),
      detail=f"diagonalized = {diag_block_simplified}")

# Verify O_2 is orthogonal: O_2 O_2^T = I
O_2_orthogonal = simplify(O_2 * O_2.T - eye(2))
check("O_2 is real orthogonal: O_2 O_2^T = I",
      O_2_orthogonal == zeros(2, 2),
      detail=f"O_2 O_2^T - I = {O_2_orthogonal}")


# ----------------------------------------------------------------------------
section("Part 4: K_mass = O^T K_Z3-diag O is real symmetric -> Im[(K_mass)_{1j}^2] = 0")
# ----------------------------------------------------------------------------
# In the Z_3 basis, K is diagonal with real entries (Part 2). The mass-basis
# diagonalization U is block-diag(1, O_2), which is real orthogonal. So
# K_mass = U^T K_diag U is real symmetric (real entries), and therefore
# (K_mass)_{1j} are real for all j, so Im[(K_mass)_{1j}^2] = 0.

# Concrete instance: pick rational d, r and chi = omega (full-source branch),
# then compute K explicitly, diagonalize via U_Z3, transform with U = block_diag(1, O_2).
d_val, r_val = Rational(1), Rational(1, 2)

# Eigenvalues of K at chi = omega:
#   k=0: d + r(omega * 1 + omega-bar * 1) = d + r(omega + omega-bar) = d - r
#   k=1: d + r(omega * omega + omega-bar * omega-bar) = d + r(omega^2 + omega^-2) = d - r
#   k=2: d + r(omega * omega^2 + omega-bar * omega^-2) = d + r(omega^3 + omega^-3) = d + 2r
#
# All three are real. Let us verify numerically.
chi_val = omega
chi_star_val = omega_bar
eigs_at_omega = []
for k in [0, 1, 2]:
    lam = d_val + r_val * (chi_val * omega**k + chi_star_val * omega**(-k))
    lam_reduced = simplify(lam.rewrite(sympy.cos).expand(complex=True))
    eigs_at_omega.append(lam_reduced)
print(f"\n  K eigenvalues at chi=omega, d=1, r=1/2:")
for k, lam in enumerate(eigs_at_omega):
    print(f"    lambda_{k} = {lam}")

# Verify all are real
all_real = all(simplify(sympy.im(lam)) == 0 for lam in eigs_at_omega)
check("all K eigenvalues at chi=omega real (no_go's load-bearing fact)",
      all_real,
      detail=f"eigs = {eigs_at_omega}")

# Now: K_diag = diag(eigs); transform via U = block_diag(1, O_2).
# K_mass[1, j] for j=0, 1, 2: take row 1 of U^T K_diag U.
# Since U is block_diag(1, O_2), and K_diag is diag(lam_0, lam_1, lam_2),
# K_mass[1, j] = (U^T K_diag U)[1, j].
# All entries are real because lam_k are real and U is real orthogonal.

# Construct full U
U = Matrix([
    [1, 0, 0],
    [0, 1 / sqrt(2), 1 / sqrt(2)],
    [0, 1 / sqrt(2), -1 / sqrt(2)],
])

K_diag = sympy.diag(*eigs_at_omega)
K_mass = simplify(U.T * K_diag * U)
print(f"\n  K_mass at chi=omega, d=1, r=1/2:")
for i in range(3):
    for j in range(3):
        print(f"    K_mass[{i},{j}] = {K_mass[i, j]}")

# Verify all entries of K_mass are real
all_K_mass_real = all(simplify(sympy.im(K_mass[i, j])) == 0 for i in range(3) for j in range(3))
check("K_mass has all real entries (no_go closure: real symmetric in mass basis)",
      all_K_mass_real,
      detail="all imaginary parts identically zero")

# Verify Im[(K_mass)_{1j}^2] = 0 for all j (the parent no-go conclusion)
all_im_squared_zero = all(
    simplify(sympy.im(K_mass[0, j]**2)) == 0 for j in range(3)
)
check("Im[(K_mass)_{1j}^2] = 0 for all j (no_go conclusion at chi=omega)",
      all_im_squared_zero,
      detail="full-source branch chi=omega still real-symmetric in mass basis")


# ----------------------------------------------------------------------------
section("Part 5: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
parent_id = "dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15"
parent = rows.get(parent_id, {})
print(f"\n  {parent_id} current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check(f"{parent_id} is no_go claim_type",
      parent.get('claim_type') == 'no_go',
      detail=f"claim_type = {parent.get('claim_type')}")
check(f"{parent_id} has class-(A) load-bearing step (linear-algebraic identity)",
      parent.get('load_bearing_step_class') == 'A',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent no-go theorem's load-bearing class-(A) algebra:

    Z_3-covariant circulant K = d I + r(chi S + chi* S^2) has a REAL
    spectrum for any unit-modulus character chi; M_R real-symmetric
    block-form diagonalizes via real orthogonal U; therefore K_mass
    remains real symmetric and Im[(K_mass)_{1j}^2] = 0 for all j.

  The companion verifies S^3 = I, the real-eigenvalue spectral structure
  for chi in {1, omega, omega-bar}, the real orthogonal diagonalization of
  the 2x2 doublet block, and the full-source-branch (chi=omega) closure
  Im[(K_mass)_{1j}^2] = 0 at exact symbolic precision.

  Audit-lane class for the parent's load-bearing step:
    (A) — algebraic identity / linear algebra on Z_3-covariant circulants
    and real-symmetric blocks. No external observed/fitted/literature input.

  This companion does NOT introduce a new claim row, a new source note,
  or any modification of the parent row's status. Independent audit
  remains responsible for any later parent-row disposition.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
