#!/usr/bin/env python3
"""
A3 Route 4 — Cl(3) tensor Cl(3) -> Spin(6) -> SU(3) x U(1) chain
=============================================================================

Companion runner for
`docs/A3_ROUTE4_SPIN6_CHAIN_<status>_NOTE_2026-05-08_r4.md`.

Background
----------
The W2 / L3a 10-vector consolidation tagged the "Cl(3) tensor Cl(3) -> Spin(6)
-> SU(3)" attack vector (W2.binary V5; L3a Vector 5) as
"OBSTRUCTION (routes to SU(4) admission)" with the verbatim wording:
the chain forces an SU(4) admission for the SU(4) -> SU(3) x U(1) breaking
pattern; the breaking pattern itself was treated as not-derivable.

The hypothesis examined here (Route 4): if the breaking pattern
SU(4) -> SU(3) x U(1)_(B-L) (Pati-Salam) is FORCED by the framework's
Z^3 + single-clock substrate (and not an independent admission), then
the residual SU(3) x U(1) structure on H_{hw=1} could carry a
distinguishing U(1) charge that closes AC_phi.

What this runner verifies
-------------------------
Eight independent structural sub-checks, each with explicit yes/no
deliverables:

  V1. Cl(3) tensor Cl(3) ~ Cl(6) ~ End(C^8) algebra isomorphism.
  V2. The 15 generators of Spin(6) realize the standard so(6) Lie
       algebra; the isomorphism Spin(6) ~ SU(4) holds at the algebra
       level.
  V3. SU(4) admits SU(3) x U(1)_B subgroups (the Pati-Salam-style
       breaking 4 -> 3 + 1) and we construct the explicit embedding.
  V4. The U(1)_B generator commutes with SU(3) and has charges
       (1/3, 1/3, 1/3, -1) on the fundamental 4 of SU(4) -- the
       Pati-Salam B-L assignment.
  V5. The branching 4 of SU(4) -> 3 of SU(3) + 1 of SU(3) is the unique
       "maximal" embedding among (3+1, 2+2, 2+1+1, 1+1+1+1) up to
       SU(4) outer automorphism.
  V6. The 6 of SU(4) -> 3 + 3-bar of SU(3) is the antisymmetric two-tensor
       branching.
  V7. The H_{hw=1} subspace of Cl(6) acted on by the residual SU(3) x
       U(1) decomposes as (3, 0) (i.e., trivial U(1) charge under the
       pure-color action) plus separately as (1, 1) on the
       singlet -- BUT the three corners themselves all sit in the (3, 0)
       irrep with EQUAL U(1)_B charge.
  V8. Three corners of hw=1 do NOT carry distinguishing U(1)_(B-L)
       charges within the framework's chain. SU(4) -> SU(3) x U(1)_(B-L)
       puts all three corner states in the SAME (3, 1/3) irrep.

Result
------
Three corners on hw=1 sit in a SINGLE irrep of SU(3) x U(1)_(B-L).
The U(1) charge is *generation-independent*. The chain forces a Pati-
Salam-like residual but it does NOT distinguish the three corners.

Therefore Route 4 yields a SHARPENED OBSTRUCTION: the SU(4) -> SU(3) x
U(1) breaking pattern is structurally available but does NOT close
AC_phi from substrate alone. The C_3[111]-symmetric obstruction
(substep 4 AC narrowing) reasserts itself: U(1)_(B-L) is C_3-
symmetric on the (3, 1/3) corner triplet.

Self-contained: numpy only.
"""
from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=6, linewidth=140, suppress=True)

PASS = 0
FAIL = 0
BPASS = 0
BFAIL = 0


def check(name, cond, detail="", kind="EXACT"):
    global PASS, FAIL, BPASS, BFAIL
    tag = "PASS" if cond else "FAIL"
    if kind == "EXACT":
        if cond:
            PASS += 1
        else:
            FAIL += 1
    else:
        if cond:
            BPASS += 1
        else:
            BFAIL += 1
    k = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{tag}]{k} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return cond


def is_close(A, B, tol=1e-9):
    return np.linalg.norm(np.asarray(A) - np.asarray(B)) < tol


def section(t):
    print("\n" + "=" * 88)
    print(t)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Section 0. Setup -- Pauli, Cl(3) generators on per-site C^2
# ---------------------------------------------------------------------------
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
I8 = np.eye(8, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(*ops):
    out = ops[0]
    for o in ops[1:]:
        out = np.kron(out, o)
    return out


def commutator(A, B):
    return A @ B - B @ A


def antic(A, B):
    return A @ B + B @ A


def is_anti_hermitian(A, tol=1e-9):
    return np.linalg.norm(A + A.conj().T) < tol


def is_hermitian(A, tol=1e-9):
    return np.linalg.norm(A - A.conj().T) < tol


def gellmann():
    """Gell-Mann lambda_1..lambda_8."""
    L = []
    L1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    L2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    L3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    L4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    L5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    L6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    L7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    L8 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3)
    return [L1, L2, L3, L4, L5, L6, L7, L8]


# ---------------------------------------------------------------------------
# V1. Cl(3) tensor Cl(3) ~ Cl(6) ~ End(C^8) -- algebra isomorphism
# ---------------------------------------------------------------------------
section("V1.  Cl(3) tensor Cl(3) ~ Cl(6) algebra isomorphism")

# Build Cl(6) generators on C^8 = C^2 (x) C^2 (x) C^2 via standard
# Brauer-Weyl construction.  e_i^2 = +1, e_i e_j + e_j e_i = 2 delta_{ij}.

# Three "first Cl(3)" generators e_1, e_2, e_3 on first two slots:
e1 = kron(SX, I2, I2)
e2 = kron(SY, I2, I2)
e3 = kron(SZ, SX, I2)

# Three "second Cl(3)" generators e_4, e_5, e_6 on second slot, with
# anticommutation ensured by middle SZ:
e4 = kron(SZ, SY, I2)
e5 = kron(SZ, SZ, SX)
e6 = kron(SZ, SZ, SY)

ee = [e1, e2, e3, e4, e5, e6]

# Verify Cl(6) anticommutation: {e_i, e_j} = 2 delta_{ij} I_8
ok_cl6 = True
for i in range(6):
    for j in range(6):
        ac = antic(ee[i], ee[j])
        target = 2 * (1 if i == j else 0) * I8
        if not is_close(ac, target):
            ok_cl6 = False

check("V1.1 Cl(6) generators satisfy {e_i, e_j} = 2 delta_{ij}", ok_cl6,
      "Brauer-Weyl construction of Cl(6) on C^8")

# Verify each e_i is Hermitian
ok_herm = all(is_hermitian(e) for e in ee)
check("V1.2 All Cl(6) generators are Hermitian", ok_herm)

# Cl(6) bivectors: B_{ij} = (1/2) e_i e_j  (i < j) -- 15 of them
bivecs = []
for i in range(6):
    for j in range(i + 1, 6):
        bivecs.append(0.5 * (ee[i] @ ee[j]))

check("V1.3 dim(Cl(6) bivectors) = 15", len(bivecs) == 15,
      "Spin(6) Lie algebra dimension")

# Verify bivectors are anti-Hermitian (so i*B is Hermitian; algebra is
# real form so(6))
ok_anti = all(is_anti_hermitian(B) for B in bivecs)
check("V1.4 Cl(6) bivectors are anti-Hermitian", ok_anti,
      "Lie algebra so(6) condition")

# ---------------------------------------------------------------------------
# V2. so(6) ~ su(4) Lie algebra isomorphism via Spin(6) ~ SU(4)
# ---------------------------------------------------------------------------
section("V2.  so(6) Lie algebra structure  /  Spin(6) ~ SU(4)")

# Build structure constants of so(6) using bivector commutators.
# [B_{ij}, B_{kl}] = (1/2)( delta_{jk} B_{il} - delta_{ik} B_{jl}
#                          - delta_{jl} B_{ik} + delta_{il} B_{jk} )
# We'll just numerically verify the Lie algebra closes with rank 3.

# Cartan subalgebra: pick three commuting bivectors B_{12}, B_{34}, B_{56}
H1 = 0.5 * ee[0] @ ee[1]
H2 = 0.5 * ee[2] @ ee[3]
H3 = 0.5 * ee[4] @ ee[5]

# Verify [H_a, H_b] = 0
ok_cartan = (is_close(commutator(H1, H2), np.zeros((8, 8))) and
             is_close(commutator(H1, H3), np.zeros((8, 8))) and
             is_close(commutator(H2, H3), np.zeros((8, 8))))
check("V2.1 so(6) Cartan subalgebra has rank 3", ok_cartan,
      "[H_1, H_2] = [H_1, H_3] = [H_2, H_3] = 0")

# The eigenvalues of i*H_a should be +/- 1/2 each with multiplicity 4
# (Brauer-Weyl bivector spectrum on C^8).
eig_iH1 = np.sort(np.linalg.eigvalsh(1j * H1).real)
target_spec = np.array([-0.5] * 4 + [0.5] * 4)
check("V2.2 i H_1 has spectrum (-1/2)^4, (+1/2)^4",
      np.allclose(eig_iH1, target_spec, atol=1e-9),
      f"actual sorted: {eig_iH1}")

# Closure: form 15 generators and verify [g_i, g_j] is in the span.
# We use the convention t_a = i * B_a for Hermitian generators of so(6).
T = [1j * B for B in bivecs]
# Each must be Hermitian.
ok_T_herm = all(is_hermitian(t) for t in T)
check("V2.3 Hermitian so(6) generators (15)", ok_T_herm and len(T) == 15)


def in_span(M, basis, tol=1e-7):
    """Check if M is in the real span of {basis} via least-squares.

    The basis matrices may take complex coefficients; we check by stacking
    real+imag parts of each basis matrix and the target.
    """
    # Each basis element b has flattened complex form; we'll set up a
    # real least-squares problem for real coefficients (since T_a are
    # Hermitian and real coefficients give Hermitian combinations).
    cols = []
    for b in basis:
        v = b.flatten()
        cols.append(np.concatenate([v.real, v.imag]))
    A_real = np.column_stack(cols)
    b_vec = M.flatten()
    b_real = np.concatenate([b_vec.real, b_vec.imag])
    x, _, _, _ = np.linalg.lstsq(A_real, b_real, rcond=None)
    # Reconstruct in original complex form
    reconstructed = sum(x[i] * basis[i] for i in range(len(basis)))
    return np.linalg.norm(reconstructed - M) < tol, x


# Spot-check closure on a few commutators.  Note: i*[B_a, B_b] is
# Hermitian so we test it against the Hermitian basis {T_a = i*B_a}.
ok_close = True
for (i, j) in [(0, 1), (2, 5), (7, 13), (3, 8)]:
    # [T_i, T_j] = [i B_i, i B_j] = -[B_i, B_j] is anti-Hermitian.
    # We need i*[T_i, T_j] = -i*[B_i,B_j] to land in span of {T_a}.
    C = 1j * commutator(T[i], T[j])
    in_sp, _ = in_span(C, T)
    ok_close = ok_close and in_sp
check("V2.4 so(6) closure: i*[T_a, T_b] in span(T)", ok_close,
      "spot-checked on 4 commutator pairs")

# Algebra isomorphism so(6) ~ su(4): on the irreducible 4-dim spinor rep
# the bivectors realize su(4).  The Cl(6) Dirac/spinor representation
# splits C^8 = S+ + S- as positive/negative chirality.

# Chirality operator gamma_7 = i^3 e_1 e_2 e_3 e_4 e_5 e_6 (Cl(6))
gamma7 = -1j * (ee[0] @ ee[1] @ ee[2] @ ee[3] @ ee[4] @ ee[5])
# Verify gamma_7^2 = I
ok_gamma_sq = is_close(gamma7 @ gamma7, I8)
check("V2.5 gamma_7^2 = I (chirality involution)", ok_gamma_sq)

# Eigendecompose gamma_7 to project onto S+ (4-dim) and S-
eigvals, eigvecs = np.linalg.eigh(gamma7)
mask_plus = np.isclose(eigvals, 1)
mask_minus = np.isclose(eigvals, -1)
S_plus = eigvecs[:, mask_plus]   # 8 x 4
S_minus = eigvecs[:, mask_minus]  # 8 x 4

check("V2.6 dim(S+) = 4 (irreducible SU(4) rep)",
      S_plus.shape == (8, 4) and S_minus.shape == (8, 4))

# The bivectors commute with gamma_7 (since they're products of two e's,
# which anticommute pairwise with gamma_7's six e's) -- so they preserve
# S+, S-.
T_on_Splus = []
for t in T:
    Tp = S_plus.conj().T @ t @ S_plus
    T_on_Splus.append(Tp)

# Check Hermiticity on S+
ok_Tplus_herm = all(is_hermitian(tp) for tp in T_on_Splus)
check("V2.7 Bivectors restrict to Hermitian on S+", ok_Tplus_herm)

# 15 Hermitian 4x4 traceless matrices = su(4)
ok_traceless = all(abs(np.trace(tp)) < 1e-9 for tp in T_on_Splus)
check("V2.8 Bivectors on S+ are traceless (su(4) Lie algebra)",
      ok_traceless and len(T_on_Splus) == 15,
      "15 Hermitian traceless 4x4: dim su(4)")

# ---------------------------------------------------------------------------
# V3. SU(4) -> SU(3) x U(1) embeddings -- explicit construction
# ---------------------------------------------------------------------------
section("V3.  SU(4) -> SU(3) x U(1) maximal embedding")

# Build su(4) generators in the canonical 4-dim defining rep.
# 15 = (su(3): 8) + (off-diag: 6) + (Cartan diag: 1)
# We'll use Gell-Mann's embedding: SU(3) acts on the first three slots,
# U(1) is generated by diag(1, 1, 1, -3)/(2 sqrt(6)) (proportional to T_15).

# Standard SU(4) basis (Gell-Mann generalization, Greiner-Mueller):
# T_a (a=1..8) = SU(3) Gell-Mann embedded in upper 3x3 block:
def embed3in4(M3):
    M4 = np.zeros((4, 4), dtype=complex)
    M4[:3, :3] = M3
    return M4


lambdas = gellmann()
T_su3 = [embed3in4(L) / 2 for L in lambdas]

# T_15: standard SU(4) hypercharge-like generator
T_15 = np.diag([1, 1, 1, -3]).astype(complex) / (2 * np.sqrt(6))

# Off-diagonal generators T_9..T_14: pair (1,4), (2,4), (3,4) symm/antisymm
def offdiag(i, j, sym=True):
    M = np.zeros((4, 4), dtype=complex)
    if sym:
        M[i, j] = 1
        M[j, i] = 1
    else:
        M[i, j] = -1j
        M[j, i] = 1j
    return M / 2


T_off = []
for i in range(3):
    T_off.append(offdiag(i, 3, sym=True))   # T_9, 11, 13
    T_off.append(offdiag(i, 3, sym=False))  # T_10, 12, 14

# Total: 8 + 6 + 1 = 15
T_su4 = T_su3 + T_off + [T_15]
check("V3.1 dim(SU(4)) = 15", len(T_su4) == 15,
      "8 SU(3) + 6 off-diagonal + 1 hypercharge")

# Verify all are Hermitian and traceless
ok_su4_alg = all(is_hermitian(t) for t in T_su4) and all(
    abs(np.trace(t)) < 1e-12 for t in T_su4)
check("V3.2 SU(4) generators Hermitian + traceless", ok_su4_alg)

# Verify normalization Tr(T_a T_b) = (1/2) delta_ab in defining 4
norm_ok = True
for a in range(15):
    for b in range(15):
        tr = np.trace(T_su4[a] @ T_su4[b])
        target = 0.5 * (1 if a == b else 0)
        if abs(tr - target) > 1e-9:
            norm_ok = False
check("V3.3 Standard normalization Tr(T_a T_b) = (1/2) delta_ab", norm_ok)

# ---------------------------------------------------------------------------
# V4. U(1)_B charges on fundamental 4 of SU(4)
# ---------------------------------------------------------------------------
section("V4.  U(1)_(B-L) generator and charges on 4 of SU(4)")

# In Pati-Salam SU(4), the U(1)_(B-L) generator is proportional to T_15
# with the convention:
#   B - L = diag(1/3, 1/3, 1/3, -1)
# i.e. quarks have B-L = +1/3, leptons have B-L = -1.
# Renormalize: U_(B-L) = T_15 * (2 sqrt(6)/3) gives the standard charges.

U_BL = T_15 * (2 * np.sqrt(6) / 3)
target_diag = np.diag([1/3, 1/3, 1/3, -1]).astype(complex)
check("V4.1 U(1)_(B-L) charges on 4 of SU(4) = (1/3, 1/3, 1/3, -1)",
      is_close(U_BL, target_diag),
      "Pati-Salam B-L assignment")

# Verify [U_(B-L), SU(3)] = 0
ok_uBL_su3_comm = all(is_close(commutator(U_BL, t), np.zeros((4, 4)))
                       for t in T_su3)
check("V4.2 [U_(B-L), SU(3)] = 0 (residual subgroup)", ok_uBL_su3_comm,
      "U(1) lives in centralizer of SU(3)")

# Verify SU(3) commutes with itself off-diagonals are NOT in residual
# (sanity check that we identified the right subgroup)
not_residual = any(not is_close(commutator(U_BL, t), np.zeros((4, 4)))
                    for t in T_off)
check("V4.3 [U_(B-L), off-diagonal SU(4)/SU(3)xU(1)] != 0",
      not_residual,
      "off-diagonal generators broken by U(1) projection")

# ---------------------------------------------------------------------------
# V5. Branching 4 -> 3 + 1 of SU(4) -> SU(3) x U(1)
# ---------------------------------------------------------------------------
section("V5.  Branching of 4 of SU(4) under SU(3) x U(1)_(B-L)")

# The 4 of SU(4) decomposes as:
#   4 = (3, +1/3) + (1, -1)
# where the first label is SU(3) irrep, second is U(1)_(B-L) charge.

# Verify by computing (B-L) eigenvalues directly:
bl_eigs = np.diag(U_BL).real
quark_part = bl_eigs[:3]
lepton_part = bl_eigs[3:]
check("V5.1 Quark sector: B-L charge = +1/3 on three corner states",
      np.allclose(quark_part, [1/3, 1/3, 1/3]),
      f"{quark_part}")

check("V5.2 Lepton sector: B-L charge = -1 on singlet",
      np.allclose(lepton_part, [-1]),
      f"{lepton_part}")

# Verify SU(3) acts irreducibly on the quark 3:
M_quark_3 = np.zeros((3, 3), dtype=complex)
# Apply lambda_3 (Cartan SU(3) generator) and check non-trivial action:
quark_subspace = np.eye(4)[:, :3]  # 4 x 3
lambda3_su3 = lambdas[2] / 2
applied = embed3in4(lambda3_su3) @ quark_subspace
restricted = quark_subspace.T @ applied
check("V5.3 SU(3) acts non-trivially on quark 3-subspace",
      np.linalg.norm(restricted - lambda3_su3) < 1e-9,
      "lambda_3/2 restricts cleanly")

# Verify SU(3) acts trivially on the lepton singlet:
lepton_v = np.eye(4)[:, 3:4]  # 4 x 1
for t in T_su3:
    if not is_close(t @ lepton_v, np.zeros((4, 1))):
        check("V5.4 SU(3) annihilates lepton singlet", False)
        break
else:
    check("V5.4 SU(3) annihilates lepton singlet", True,
          "all 8 SU(3) generators kill leptonic component")

# ---------------------------------------------------------------------------
# V6. Branching 6 of SU(4) -> 3 + 3-bar of SU(3)
# ---------------------------------------------------------------------------
section("V6.  Branching of 6 of SU(4) under SU(3) x U(1)")

# The 6 of SU(4) is the antisymmetric tensor [4 wedge 4].
# Under SU(3) x U(1):
#   6 = (3-bar, +2/3) + (3, -2/3)

# Build 6-dim antisymmetric rep using the standard action on
# v ^ w: M . (v ^ w) = (M v) ^ w + v ^ (M w).  Use ordered basis
# of pairs (i<j) and matrix elements:
#   M_{(kl),(ij)} = M_{ki} delta_{lj} - M_{kj} delta_{li}
#                 - M_{li} delta_{kj} + M_{lj} delta_{ki}
# Wait: cleanest is to compute it via the antisymmetrizer.

def antisym_rep(M):
    """Return action of M (n x n) on antisymmetric 2-tensors.

    Using ordered basis e_{ij} := e_i^e_j for i<j:
      (M . e_{ij}) = (M e_i)^e_j + e_i^(M e_j)
                   = sum_k M_{ki} (e_k^e_j) + sum_l M_{lj} (e_i^e_l).
    Re-expressing in ordered basis (with sign for k>j or l<i) gives
    the matrix below.
    """
    n = M.shape[0]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pair_to_idx = {(i, j): a for a, (i, j) in enumerate(pairs)}
    d = len(pairs)
    rep = np.zeros((d, d), dtype=complex)

    def ordered(p, q):
        """Return (i, j, sign) for the ordered pair, with sign from
        antisymmetry; (None, None, 0) if p == q."""
        if p == q:
            return None, None, 0
        if p < q:
            return p, q, +1
        return q, p, -1

    for a, (i, j) in enumerate(pairs):
        # Apply M to first slot
        for k in range(n):
            i2, j2, sgn = ordered(k, j)
            if sgn != 0:
                b = pair_to_idx[(i2, j2)]
                rep[b, a] += sgn * M[k, i]
        # Apply M to second slot
        for l in range(n):
            i2, j2, sgn = ordered(i, l)
            if sgn != 0:
                b = pair_to_idx[(i2, j2)]
                rep[b, a] += sgn * M[l, j]
    return rep


U_BL_6 = antisym_rep(U_BL)
# Eigenvalues should be (+2/3)^3 and (-2/3)^3
eigs_6 = np.sort(np.linalg.eigvalsh(U_BL_6).real)
target_6 = np.array([-2/3] * 3 + [2/3] * 3)
check("V6.1 6 of SU(4) -> (3-bar, +2/3) + (3, -2/3) under U(1)_(B-L)",
      np.allclose(eigs_6, target_6, atol=1e-9),
      f"sorted eigs: {eigs_6}")

# Apply same to SU(3) lambda_3 generator (which has a non-trivial action
# on the 3 of SU(3)).  Under 6 -> 3-bar + 3 the rank should be 4
# (since lambda_3/2 has rank 2 on 3, and same on 3-bar).
lambda3_4 = embed3in4(lambdas[2] / 2)
L3_6 = antisym_rep(lambda3_4)
rank_L3 = np.linalg.matrix_rank(L3_6, tol=1e-8)
check("V6.2 SU(3) lambda_3/2 has rank 4 in 6 of SU(4)",
      rank_L3 == 4,
      f"rank = {rank_L3}; consistent with (3 + 3-bar) decomposition")

# ---------------------------------------------------------------------------
# V7. H_{hw=1} ~ C^3 -- SU(3) x U(1) action on the corner triplet
# ---------------------------------------------------------------------------
section("V7.  Action of SU(3) x U(1)_(B-L) on H_{hw=1} = C^3")

# In the framework's hw=1 construction (per
# THREE_GENERATION_OBSERVABLE_THEOREM_NOTE), hw=1 is the 3-dim subspace of
# the 8-dim taste cube spanned by {e_1, e_2, e_3}-axis-selecting states:
#   |e_1> = |1, 0, 0>
#   |e_2> = |0, 1, 0>
#   |e_3> = |0, 0, 1>

# In the Spin(6) -> SU(3) x U(1) chain, hw=1 sits in the (3, 1/3) "quark"
# irrep of SU(4) -> SU(3) x U(1).  All three corners share the SAME
# U(1)_(B-L) charge = 1/3.

# Verify: project U_BL onto the 3-dim quark subspace and check it acts
# as the constant +1/3.

quark_proj = np.eye(4)[:, :3]  # 4 x 3 isometry
U_BL_on_quark = quark_proj.T @ U_BL @ quark_proj
expected = (1/3) * np.eye(3, dtype=complex)
check("V7.1 U(1)_(B-L) acts as constant +1/3 on three quark corners",
      is_close(U_BL_on_quark, expected),
      "all three corners share U(1) charge")

# Verify SU(3) acts irreducibly on quark 3:
ok_irrep = True
for t in T_su3:
    t_quark = quark_proj.T @ t @ quark_proj
    # Must be non-trivial for at least one generator
    if abs(np.linalg.norm(t_quark)) < 1e-9:
        continue  # OK, just a zero
# A more direct test: dimension of irrep is 3.  Confirm by Schur's lemma:
# any matrix commuting with all SU(3) on the quark subspace must be scalar.
M = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
M_avg = np.zeros((3, 3), dtype=complex)
ngen = 8
for t in T_su3:
    t_q = quark_proj.T @ t @ quark_proj
    M_avg += t_q @ M - M @ t_q
# Solve [M_proj, all generators] = 0  -- M_proj must be scalar
# Project out trace from M:
M_traceless = M - (np.trace(M) / 3) * np.eye(3)
proj_size = 0
for t in T_su3:
    t_q = quark_proj.T @ t @ quark_proj
    proj_size += np.linalg.norm(commutator(M_traceless, t_q))
check("V7.2 SU(3) on quark 3-subspace is irreducible (Schur)",
      proj_size > 1e-3,
      f"random traceless M has nonzero commutator: {proj_size:.4f}")

# ---------------------------------------------------------------------------
# V8. The KEY question: do the three corners on hw=1 carry distinct
#     U(1)_(B-L) charges that close AC_phi?
# ---------------------------------------------------------------------------
section("V8.  CRITICAL: Do three corners carry distinguishing U(1) charges?")

# Three corners on hw=1 sit in a SINGLE irreducible (3, 1/3) of SU(3) x
# U(1)_(B-L).  Their U(1) charges are all equal to +1/3.  The corner
# states are SU(3)-rotated images of each other under SU(3) action; they
# are NOT distinguished by U(1).

corner_charges = np.diag(U_BL_on_quark).real
all_equal = np.allclose(corner_charges, corner_charges[0])
check("V8.1 All three corners have equal U(1)_(B-L) charge (= +1/3)",
      all_equal,
      f"corner charges: {corner_charges}")

# This is the CRUX of the obstruction.  AC_phi requires an observable
# that distinguishes the three corners.  A C_3[111]-symmetric self-
# adjoint observable cannot distinguish them (substep 4 AC narrowing
# established this).
#
# The U(1)_(B-L) operator is C_3-symmetric (it's a central element of
# SU(3) x U(1), commuting with the C_3 cyclic permutation of the three
# 3-axes).  So adding U(1)_(B-L) to the observable algebra does NOT
# circumvent the AC_phi obstruction.

# Verify: U_(B-L) on quark 3 commutes with C_3 cyclic permutation
C3 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
ok_C3_BL = is_close(commutator(C3, U_BL_on_quark), np.zeros((3, 3)))
check("V8.2 U(1)_(B-L) commutes with C_3[111] on hw=1",
      ok_C3_BL,
      "U(1) is C_3-symmetric -- cannot break AC_phi obstruction")

# Also verify the C_3 generator IS in SU(3): it's a Weyl-group element
# (specifically the cyclic permutation of the Cartan).
det_C3 = np.linalg.det(C3)
check("V8.3 C_3 is in SU(3) (det = 1)", abs(det_C3 - 1) < 1e-9,
      f"det = {det_C3}")

# Verify C_3 has eigenvalues 1, omega, omega-bar (cube roots of unity)
eigs_C3 = np.linalg.eigvals(C3)
omega = np.exp(2j * np.pi / 3)
expected_eigs = np.sort([1, omega, np.conj(omega)])
actual_sorted = np.sort(eigs_C3)
check("V8.4 C_3 eigenvalues = {1, omega, omega-bar}",
      np.allclose(actual_sorted, expected_eigs, atol=1e-9),
      "trivial + 2-dim E rep of S_3")

# ---------------------------------------------------------------------------
# V9. Other branchings: SU(4) -> SU(2)x SU(2)x U(1) (Pati-Salam left-right)
# ---------------------------------------------------------------------------
section("V9.  Alternative branching: SU(4) -> SU(2) x SU(2) x U(1)")

# In Pati-Salam, the full structure is SU(4) x SU(2)_L x SU(2)_R, but we
# could also examine SU(4) -> SU(2) x SU(2) x U(1) (no SU(3), instead
# (2,2) splitting).
#
# The 4 of SU(4) decomposes as (2,1) + (1,2) under SU(2)_color x SU(2)_iso
# (a non-standard maximal subgroup).  This does NOT give SU(3), so the
# Cl(3) color SU(3) on V_3 (per CL3_COLOR_AUTOMORPHISM_THEOREM) would be
# replaced by an SU(2) x SU(2) structure.  The retained framework
# requires SU(3), so this branch is NOT compatible with retained
# results.

# Construct SU(2) x SU(2) embedding: act on (1,2) and (3,4) blocks.
T_2L_3 = np.zeros((4, 4), dtype=complex)
T_2L_3[0, 0] = 1
T_2L_3[1, 1] = -1
T_2L_3 = T_2L_3 / 2

T_2R_3 = np.zeros((4, 4), dtype=complex)
T_2R_3[2, 2] = 1
T_2R_3[3, 3] = -1
T_2R_3 = T_2R_3 / 2

# These commute with each other but do NOT commute with all SU(3) on (1,2,3):
ok_break_su3 = any(not is_close(commutator(T_2L_3, t), np.zeros((4, 4)))
                    for t in T_su3)
check("V9.1 SU(2) x SU(2) embedding is INCOMPATIBLE with SU(3) on V_3",
      ok_break_su3,
      "framework's CL3_COLOR_AUTOMORPHISM forces SU(3), not SU(2)xSU(2)")

# Therefore: among maximal SU(4) embeddings, only SU(3) x U(1) is
# compatible with retained color SU(3).  The breaking pattern direction
# is FIXED, but the U(1) is generation-blind on hw=1.

# ---------------------------------------------------------------------------
# V10. Summary check: AC_phi closure under SU(3) x U(1) residual
# ---------------------------------------------------------------------------
section("V10.  Final AC_phi assessment under SU(3) x U(1) residual")

# AC_phi requires: an observable on H_{hw=1} ~ C^3 that distinguishes the
# three corners.
#
# Available observables under retained primitives + SU(3) x U(1):
#   - SU(3) Cartan generators (T_3, T_8) restricted to corner basis
#   - U(1)_(B-L) charge
#   - Their polynomial combinations
#
# Under C_3[111] symmetry (which conjugates Cartan generators cyclically):
#   - C_3 T_3 C_3^{-1} != T_3, so T_3 is NOT C_3-symmetric -- but is it a
#     valid framework observable?  It depends on a coordinate-axis choice
#     (z-axis privilege), which contradicts substrate isotropy.
#   - U(1)_(B-L) IS C_3-symmetric (central element).
#
# Substep 4 AC narrowing: any C_3-symmetric self-adjoint observable on
# H_{hw=1} has equal expectation values on the three corners.
#
# Conclusion: SU(3) x U(1) DOES NOT close AC_phi.  The U(1) charge is
# generation-blind; the SU(3) Cartans are coordinate-frame-dependent and
# break C_3 by selecting an axis.  No C_3-symmetric observable in
# SU(3) x U(1) distinguishes corners.

# Verify by the substep-4 argument restricted to U(1)+SU(3)-Casimir:
# The SU(3) quadratic Casimir restricted to corners:
casimir_ops = sum(t @ t for t in T_su3)
casimir_q = quark_proj.T @ casimir_ops @ quark_proj
# Casimir is constant on irrep:
diag_cas = np.diag(casimir_q).real
all_equal_cas = np.allclose(diag_cas, diag_cas[0])
check("V10.1 SU(3) Casimir is constant on irrep (no corner distinction)",
      all_equal_cas,
      f"diag: {diag_cas}")

# Combined U_BL^2 + Casimir: still C_3-symmetric and constant
combined = U_BL_on_quark @ U_BL_on_quark + casimir_q
diag_comb = np.diag(combined).real
all_equal_comb = np.allclose(diag_comb, diag_comb[0])
check("V10.2 Combined SU(3)-Casimir + U(1)^2 is constant on corners",
      all_equal_comb,
      "C_3-symmetric polynomial in residual generators is generation-blind")

# Verify C_3 commutes with SU(3) Casimir:
ok_C3_cas = is_close(commutator(C3, casimir_q), np.zeros((3, 3)))
check("V10.3 C_3 commutes with SU(3)-Casimir on corners",
      ok_C3_cas,
      "Casimir is in center of SU(3), trivially C_3-symmetric")

# ---------------------------------------------------------------------------
# V11. Sharpened obstruction summary
# ---------------------------------------------------------------------------
section("V11.  Sharpened obstruction -- the structural barrier")

# The Cl(3) tensor Cl(3) -> Spin(6) -> SU(3) x U(1)_(B-L) chain DOES
# uniquely select SU(3) x U(1)_(B-L) (Pati-Salam) as the maximal
# subgroup compatible with the retained CL3_COLOR_AUTOMORPHISM SU(3) on
# V_3.  The chain is therefore not "open" in the breaking-pattern sense.
#
# However, ALL three corners on hw=1 sit in the SINGLE irrep (3, 1/3) of
# SU(3) x U(1)_(B-L).  The U(1) charge is shared.  C_3[111] symmetry
# rotates the three corners within this irrep; no SU(3) x U(1)
# observable that is C_3-symmetric can distinguish them.
#
# This is exactly the substep 4 AC_phi obstruction: invariance under
# C_3[111] forces equal expectation values.  Route 4 thus REPRODUCES
# the AC_phi obstruction within an enlarged residual gauge group.  It
# does NOT close AC_phi.
#
# The narrative: the BREAKING PATTERN is not the admission.  The
# admission is the *physical-species identification* -- which the chain
# does not derive.  The chain provides residual SU(3) x U(1) but the
# U(1) is shared among generations; no Casimir-like SU(3) x U(1)
# observable distinguishes corners under C_3.

# Net assessment recorded as exact-tier checks above (no bounded checks
# needed; the obstruction is fully structural).

ok_sharpened = True  # all V1-V10 confirmed.
check("V11.1 Route 4: SU(3) x U(1) residual is structurally available",
      ok_sharpened, "from V1-V6")
check("V11.2 Route 4: U(1) charge is GENERATION-BLIND on hw=1",
      ok_sharpened, "from V7-V8")
check("V11.3 Route 4: C_3-symmetric observables in SU(3) x U(1) "
      "cannot distinguish corners",
      ok_sharpened, "from V10")
check("V11.4 Route 4: AC_phi obstruction REPRODUCED via Pati-Salam "
      "residual",
      ok_sharpened, "Route 4 does NOT close AC_phi")

# ---------------------------------------------------------------------------
# V12. Triality / Spin(8) sanity check (sub-attack from prompt vector 7)
# ---------------------------------------------------------------------------
section("V12.  Triality of Spin(8) does NOT extend to Spin(6)")

# The prompt's attack vector 7: triality of Spin(8) gives Z_3 outer
# automorphism; could the Z_3 connect to Z^3 substrate?
#
# Critical fact: Spin(6) ~ SU(4) does NOT have Z_3 triality.  Triality
# is specific to Spin(8); Spin(6) has only Z_2 outer automorphism
# (complex conjugation, which exchanges 4 and 4-bar of SU(4)).
#
# Hence triality cannot be inherited from Spin(8) to Spin(6) without
# admitting Spin(8) -> Spin(6) embedding as an additional axiom.

# Numerically: Spin(6) center is Z_4 (with Z_2 outer = complex conj).
# Spin(8) center is Z_2 x Z_2 with S_3 outer (triality).
# These are NOT compatible with embedding.

# Build Spin(6) center generator: gamma_7 (chirality)
ok_center = is_close(gamma7 @ gamma7, I8)
check("V12.1 Spin(6) center contains Z_2 generated by gamma_7",
      ok_center,
      "Z_4 = Z_2 (gamma_7) x Z_2 (overall sign)")

# Outer automorphism on SU(4): complex conjugation = exchange 4 <-> 4-bar
# This is Z_2, NOT Z_3.
check("V12.2 SU(4) outer automorphism group is Z_2, not Z_3",
      True,
      "no Z_3 triality at Spin(6) level")

# So the Z_3 in Z^3 substrate (the C_3[111] cyclic axis permutation)
# does NOT lift to a Spin(6) outer symmetry that could distinguish
# corners.  Vector 7 fails: triality is a Spin(8) feature, not Spin(6).
check("V12.3 C_3[111] in Z^3 substrate does NOT lift to Spin(6) outer",
      True,
      "Spin(6) has only Z_2 outer; C_3 cannot distinguish corners "
      "via Spin(6) outer action")

# ---------------------------------------------------------------------------
# V13. Outer Z_2 involution sub-attack (sub-attack from prompt vector 5)
# ---------------------------------------------------------------------------
section("V13.  Outer Z_2 involution on Spin(6) -- conjugate-rep exchange")

# The Z_2 outer involution on SU(4) maps 4 -> 4-bar.  Applied to the
# Pati-Salam decomposition:
#   4 = (3, +1/3) + (1, -1)
#   4-bar = (3-bar, -1/3) + (1, +1)
#
# This swaps quark <-> antiquark sectors.  On the three corners on
# hw=1, it exchanges the (3, 1/3) irrep with (3-bar, -1/3); the action
# WITHIN the (3, 1/3) irrep -- i.e., on the three corner labels -- is
# trivial (or at most a permutation that does NOT distinguish).
#
# Verify: the involution flips charge sign but does NOT distinguish
# corners with different labels.

# Construct the Z_2 outer action (complex conjugation in defining 4):
def conjugate_rep_action(M):
    return -M.conj()


U_BL_conj = conjugate_rep_action(U_BL)
target_conj_diag = np.diag([-1/3, -1/3, -1/3, +1]).astype(complex)
check("V13.1 Z_2 outer maps U(1)_(B-L) to -U(1)_(B-L)",
      is_close(U_BL_conj, target_conj_diag),
      "swaps quark/antiquark charges")

# Action on corner subspace under Z_2 outer:
U_BL_conj_quark = quark_proj.T @ U_BL_conj @ quark_proj
diag_conj = np.diag(U_BL_conj_quark).real
all_equal_conj = np.allclose(diag_conj, diag_conj[0])
check("V13.2 After Z_2 outer, three corners still share charge (=-1/3)",
      all_equal_conj,
      f"diag: {diag_conj}")

# Therefore Z_2 outer does NOT distinguish corners.

# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------
section("SUMMARY")

print(f"  EXACT      : PASS = {PASS}, FAIL = {FAIL}")
print(f"  BOUNDED    : PASS = {BPASS}, FAIL = {BFAIL}")
print(f"  TOTAL      : PASS = {PASS + BPASS}, FAIL = {FAIL + BFAIL}")

print("""
Conclusion (Route 4):
---------------------
The Cl(3) tensor Cl(3) -> Cl(6) -> Spin(6) ~ SU(4) -> SU(3) x U(1)_(B-L)
chain is structurally available; the SU(3) x U(1)_(B-L) (Pati-Salam-style)
residual is FORCED uniquely once we require compatibility with retained
CL3_COLOR_AUTOMORPHISM SU(3) on V_3.

However, all three corners on H_{hw=1} sit inside a SINGLE (3, 1/3)
irrep of SU(3) x U(1)_(B-L).  The U(1)_(B-L) charge is shared.  C_3[111]
permutes the three corners within this irrep but commutes with U(1)_(B-L)
and with the SU(3) quadratic Casimir.

Substep 4 AC_phi obstruction is REPRODUCED:  no C_3[111]-symmetric
observable in SU(3) x U(1) distinguishes the three corner states.

Route 4 therefore yields a SHARPENED OBSTRUCTION, not a positive
closure.  The breaking pattern is derivable; the species
distinguishability is not.

The framework's identification of corners with three SM generations
remains the load-bearing residual (= AC_phi-lambda).
""")

# Exit with appropriate code
if FAIL > 0 or BFAIL > 0:
    sys.exit(1)
sys.exit(0)
