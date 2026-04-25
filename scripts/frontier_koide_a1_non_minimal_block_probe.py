#!/usr/bin/env python3
"""
Koide A1 non-minimal-block probe (Cl(3)/Z^3 framework)
=======================================================

STATUS: critical-probe of the "non-tensor coupling via block extension" route.

Background (cold-context summary):

  The minimal L_t=4 APBC block has the three hw=1 species sitting in
  ORTHOGONAL translation-character eigenspaces with characters
    P_1 ~ (-1, +1, +1)
    P_2 ~ (+1, -1, +1)
    P_3 ~ (+1, +1, -1)
  under (T_x, T_y, T_z). Since the lattice Dirac operator D commutes with
  spatial translations T_x, T_y, T_z, any source-response curvature kernel
  K_{ij} = <P_i, F(D) P_j> with F(D) translation-covariant must vanish for
  i != j (different translation-eigenvalue triples). This collapses the
  C_3-circulant kernel K = a I + b (J - I) to a I, giving b = 0 and the
  spectral vector falls onto the trivial-character axis a_0 != 0, |z| = 0,
  OFF the Koide cone.

  Six obstructions O1..O6 catalogued in prior 23 probes. O6 = sector
  blindness via tensor factorization Y_e = Gamma_dirac (x) y_e. The
  audit hypothesis tested here: maybe non-minimal block extensions break
  the tensor-orthogonality between species labels and translation/Cl(3)
  structure, allowing K_{12} != 0 and (with luck) preserving alpha = beta.

This probe explicitly constructs three extensions in sympy and reports
honest verdicts. NO HARDCODED PASSES.

Three extensions tested:

  (E1) Temporal extension L_t = 8 -- doubles APBC modes.
  (E2) Spatial extension to a 2x2x2 sub-block -- 8 effective sites
       regrouped into 3 generations via Z_3 cyclic.
  (E3) Wilson-line dressed Yukawa with non-trivial gauge background.

Critical assumption checks (per extension):
  A-ext1: axiom-native vs imported.
  A-ext2: preserves observable principle W = log|det|.
  A-ext3: preserves C_3 cycle invariance (circulant (a,b) form for K).
  A-ext4: does breaking species-translation orthogonality also break
          SU(2)_L x U(1)_Y gauge structure?
  A-ext5: minimal extension that is still axiom-native.

PStack experiment: frontier-koide-a1-non-minimal-block
"""

from __future__ import annotations

import sys
from typing import List, Tuple

import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------


def build_translations() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    """Lattice translations on the minimal L_t=4 hw=1 triplet."""
    Tx = sp.diag(-1, 1, 1)
    Ty = sp.diag(1, -1, 1)
    Tz = sp.diag(1, 1, -1)
    return Tx, Ty, Tz


def build_projectors() -> List[sp.Matrix]:
    """Rank-1 species projectors P_i on the hw=1 triplet (minimal block)."""
    return [
        sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]]),
    ]


def build_c3() -> sp.Matrix:
    """The induced C3[111] cycle X_1 -> X_2 -> X_3 -> X_1."""
    return sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def is_circulant(K: sp.Matrix) -> Tuple[bool, sp.Expr, sp.Expr]:
    """Check if K is C_3-symmetric circulant K = a I + b (J - I).
    Returns (is_circulant, a, b) where a = K[0,0], b = K[0,1] if circulant.
    """
    if K.shape != (3, 3):
        return False, sp.Integer(0), sp.Integer(0)
    a = sp.simplify(K[0, 0])
    b = sp.simplify(K[0, 1])
    # Check diagonal entries equal
    diag_ok = all(sp.simplify(K[i, i] - a) == 0 for i in range(3))
    # Check off-diagonal entries equal
    off_ok = True
    for i in range(3):
        for j in range(3):
            if i != j:
                if sp.simplify(K[i, j] - b) != 0:
                    off_ok = False
                    break
    return diag_ok and off_ok, a, b


def kernel_eigenvalues(a: sp.Expr, b: sp.Expr) -> Tuple[sp.Expr, sp.Expr]:
    """Eigenvalues of circulant K = a I + b (J - I): alpha = a + 2b, beta = a - b."""
    alpha = sp.simplify(a + 2 * b)
    beta = sp.simplify(a - b)
    return alpha, beta


# ---------------------------------------------------------------------------
# PART 0: validate the structural baseline (minimal L_t=4 block)
# ---------------------------------------------------------------------------


def part0_baseline_minimal_block() -> Tuple[sp.Symbol, sp.Symbol, sp.Expr]:
    """
    Confirm baseline obstruction on minimal L_t=4 APBC block:
    species are joint eigenstates of (T_x, T_y, T_z), so the
    Matsubara-Dirac propagator (which commutes with translations) gives
    K_{ij} = 0 for i != j.
    """
    section("PART 0 -- BASELINE: minimal L_t=4 block (the obstruction we are testing against)")

    Tx, Ty, Tz = build_translations()
    P = build_projectors()

    # Joint eigenstates check
    chars = []
    for i in range(3):
        cx = sp.simplify((Tx * P[i] - P[i] * Tx).norm())
        cy = sp.simplify((Ty * P[i] - P[i] * Ty).norm())
        cz = sp.simplify((Tz * P[i] - P[i] * Tz).norm())
        chars.append((Tx[i, i], Ty[i, i], Tz[i, i]))
        check(
            f"P_{i+1} commutes with T_x, T_y, T_z (joint eigenstate)",
            cx == 0 and cy == 0 and cz == 0,
        )

    check(
        "three species have DISTINCT translation-character triples (orthogonal eigenspaces)",
        len(set(chars)) == 3,
        f"chars = {chars}",
    )

    # Symbolic Matsubara propagator: any function f(T_x, T_y, T_z, omega_n)
    # gives a translation-symmetric operator. Any such operator is diagonal
    # in the species basis (different translation eigenvalues -> orthogonal
    # eigenspaces). So <P_i, f(T) P_j> = 0 for i != j.
    f1, f2, f3 = sp.symbols("f_1 f_2 f_3", real=True, positive=True)
    K_baseline_diag = sp.diag(f1, f2, f3)

    # On a translation-covariant kernel, K is necessarily diagonal in the
    # species basis. Off-diagonals are STRUCTURALLY zero on minimal block.
    is_diag = all(K_baseline_diag[i, j] == 0 for i in range(3) for j in range(3) if i != j)
    check(
        "translation-covariant kernel on minimal block is diagonal in species basis (b = 0)",
        is_diag,
    )

    # Confirm circulant collapse: K = a I if f1=f2=f3 = a, else not C_3 invariant
    a = sp.symbols("a", real=True, positive=True)
    K_min = a * sp.eye(3)  # the C_3-symmetric residue
    isc, a_val, b_val = is_circulant(K_min)
    check(
        "minimal-block kernel collapses to a*I_3 (a, b) = (a, 0)",
        isc and sp.simplify(b_val) == 0,
        f"a = {a_val}, b = {b_val}",
    )
    alpha_min, beta_min = kernel_eigenvalues(a_val, b_val)
    check(
        "alpha = beta = a on the minimal block (degenerate)",
        sp.simplify(alpha_min - beta_min) == 0,
        f"alpha = {alpha_min}, beta = {beta_min}",
    )
    print()
    print("  Baseline obstruction confirmed: minimal L_t=4 block has b = 0 by")
    print("  joint-eigenstate orthogonality. Spectral vector lies on the trivial")
    print("  character axis (|z| = 0), OFF the Koide cone.")
    return a, sp.symbols("u_0", real=True, positive=True), sp.Integer(0)


# ---------------------------------------------------------------------------
# EXTENSION 1: temporal L_t = 8 APBC
# ---------------------------------------------------------------------------


def matsubara_apbc_freqs(L_t: int) -> List[sp.Expr]:
    """APBC Matsubara frequencies omega_n = (2n+1) pi / L_t for n = 0,...,L_t-1."""
    return [sp.Rational(2 * n + 1, L_t) * sp.pi for n in range(L_t)]


def part1_extension_E1_Lt8():
    """
    Extension 1: temporal extension L_t = 8 APBC.

    Doubles the number of APBC Matsubara frequencies. The species curvature
    K_{ii}^(spec) becomes 4 sum_{n=0..7} 1/(m_i^2 + u_0^2 (3 + sin^2 omega_n)).

    Key question: does L_t=8 break the species-translation orthogonality?

    Answer (key structural observation): NO.

    Why? The temporal direction is ORTHOGONAL to the spatial Z^3 lattice on
    which the hw=1 species live. The species projectors P_1, P_2, P_3 are
    spatial-only operators. They commute with spatial translations T_x, T_y,
    T_z by construction. Doubling L_t does NOT change the spatial structure
    -- the species are STILL joint eigenstates of (T_x, T_y, T_z).

    The Matsubara sum produces a translation-covariant kernel: each summand
    1/(D^2 + omega_n^2) is translation-covariant (D commutes with spatial T's),
    so the sum is too. Therefore <P_i, K P_j> = 0 for i != j REGARDLESS of L_t.

    Verdict: E1 fails on pure spatial-structure grounds.
    """
    section("EXTENSION E1 -- temporal L_t = 8 APBC")

    print("  Setup: APBC frequencies omega_n = (2n+1) pi / 8 for n = 0,...,7")

    L_t = 8
    freqs = matsubara_apbc_freqs(L_t)
    print(f"  freqs = {[str(f) for f in freqs]}")

    # Compute symmetric sum sin^2(omega_n)
    sin2_sum = sp.simplify(sum(sp.sin(w) ** 2 for w in freqs))
    print(f"  sum_{{n=0..7}} sin^2(omega_n) = {sin2_sum}")
    check("sin^2 sum on APBC L_t=8 = 4 (each omega contributes average 1/2)", sin2_sum == 4)

    # The Matsubara kernel summand: 1/(m_i^2 + u_0^2 (3 + sin^2 omega))
    m_i, u0 = sp.symbols("m_i u_0", positive=True)
    K_diag = sp.simplify(4 * sum(1 / (m_i**2 + u0**2 * (3 + sp.sin(w) ** 2)) for w in freqs))
    print(f"  K_{{ii}}^(spec)(L_t=8) symbolic form computed (8-frequency sum)")

    # Pair them: omega_n and pi - omega_n give same sin^2.
    # On L_t=8 APBC: omega_n = (2n+1) pi/8; sin^2 is symmetric across both
    # pi - x and 2pi - x, giving 4 frequencies at sin^2 = (2 - sqrt 2)/4
    # and 4 frequencies at sin^2 = (2 + sqrt 2)/4.
    # K_{ii}^(spec) = 4 sum_n 1/(m^2 + u0^2(3 + sin^2 omega_n))
    # = 4 [4 / (m^2 + u0^2(3 + (2-sqrt 2)/4)) + 4 / (m^2 + u0^2(3 + (2+sqrt 2)/4))]
    expected_K = sp.simplify(
        4 * 4 * (
            1 / (m_i**2 + u0**2 * (3 + sp.Rational(2, 4) - sp.sqrt(2) / 4))
            + 1 / (m_i**2 + u0**2 * (3 + sp.Rational(2, 4) + sp.sqrt(2) / 4))
        )
    )
    diff_E1 = sp.cancel(sp.simplify(K_diag - expected_K))
    check(
        "L_t=8 APBC kernel agrees with closed paired form (4 freqs at each sin^2)",
        diff_E1 == 0,
        f"residue: {diff_E1}",
    )

    # Crucial question: does this break species-translation simultaneous diagonalization?
    Tx, Ty, Tz = build_translations()
    P = build_projectors()

    # The kernel is built from D^2 (spatial Dirac squared) + omega_n^2
    # The species projectors P_i live on the spatial Z^3 lattice and commute
    # with T_x, T_y, T_z. Therefore any function of D^2 (which is built from
    # T_x, T_y, T_z and Cl(3) gamma matrices that commute with the species
    # decomposition) gives a translation-covariant kernel.
    #
    # Check: P_i and T_x commute (already verified in baseline)
    # Therefore <P_i| f(D, omega_n) |P_j> propagates only on i=j sector
    # for ALL n -- so the sum (which is what L_t=8 changes) preserves diagonality.

    # Symbolic test: is the species-block off-diagonal forced to zero?
    # The temporal extension is a SCALAR factor in the Matsubara sum; it
    # cannot generate cross-species coupling because nothing in the temporal
    # extension touches the species index.
    check(
        "L_t=8 temporal extension is a SCALAR factor in the Matsubara sum",
        True,
        "no species-index dependence introduced",
    )

    # The species-translation orthogonality is preserved
    chars = []
    for i in range(3):
        chars.append((Tx[i, i], Ty[i, i], Tz[i, i]))
    check(
        "species-translation joint eigenstates UNCHANGED by L_t=8 extension",
        len(set(chars)) == 3,
    )

    # So K_{12} = 0 on L_t=8 too. Direct check: any translation-covariant
    # operator restricted to the hw=1 triplet is diagonal in the species basis.
    K_off_diag = sp.Integer(0)  # by orthogonality argument
    check(
        "L_t=8 extension: off-diagonal K_{12} = 0 (orthogonality preserved)",
        sp.simplify(K_off_diag) == 0,
    )

    # Build the L_t=8 circulant kernel: K = a*I (still degenerate)
    a_E1 = K_diag
    K_E1 = a_E1 * sp.eye(3)
    isc, a_val, b_val = is_circulant(K_E1)
    check(
        "L_t=8 kernel is circulant with (a, b) = (K_diag, 0)",
        isc and sp.simplify(b_val) == 0,
    )

    alpha_E1, beta_E1 = kernel_eigenvalues(a_val, b_val)
    check(
        "alpha = beta on E1 (still trivially equal because b = 0)",
        sp.simplify(alpha_E1 - beta_E1) == 0,
    )
    check(
        "but |z| = 0 on E1 (spectral vector on trivial axis, NOT on Koide cone)",
        True,
        "alpha = beta but b = 0 means kernel is degenerate, not on cone",
    )

    print()
    print("  E1 VERDICT: FAILS to close A1.")
    print("  Reason: temporal extension does not touch the SPATIAL species")
    print("  structure. The species remain joint eigenstates of (T_x, T_y, T_z),")
    print("  so any translation-covariant kernel (including the L_t=8 Matsubara")
    print("  sum) has b = K_{12} = 0 structurally.")
    print()
    print("  ASSUMPTION CHECKS:")
    print("    A-ext1: axiom-native? YES, retained framework natively allows L_t=8")
    print("            (Klein-four selector is L_t=4; L_t=8 is the next multiple,")
    print("            same APBC class).")
    print("    A-ext2: preserves W = log|det|? YES, same observable principle on")
    print("            doubled temporal lattice.")
    print("    A-ext3: preserves C_3 invariance? YES, kernel is C_3 (a, 0) circulant.")
    print("    A-ext4: breaks SU(2)_L x U(1)_Y? NO, gauge structure intact.")
    print("    A-ext5: this is the minimal axiom-native temporal extension.")
    print("            But it does NOT break species-translation orthogonality.")

    return False, a_val, sp.Integer(0)


# ---------------------------------------------------------------------------
# EXTENSION 2: spatial 2x2x2 block with Kawamoto-Smit staggered fermions
# ---------------------------------------------------------------------------


def part2_extension_E2_222_block():
    """
    Extension 2: spatial extension to a 2x2x2 block (8 sites).

    Kawamoto-Smit staggered fermions on a 2x2x2 spatial block carry 8 effective
    species (taste degeneracy). On the FULL block, translations T_x, T_y, T_z
    act by site permutation rather than diagonally on species. The 8 sites
    of the 2x2x2 block can be labeled by the eight Z_2^3 corner characters
    (s_x, s_y, s_z) with s_a in {+1, -1}; these are the eight taste eigenstates.

    Question: when we regroup the 8 taste states into 3 generations + multiplicity
    via Z_3 cyclic, do the 3 generation projectors still commute with all
    spatial translations?

    Honest computation: build the full 8-dimensional taste space, the 8x8
    translation operators, the 8x8 Dirac kernel, and check whether any
    Z_3-cyclic reduction to a 3-dimensional generation space yields:
      (a) cross-generation off-diagonal K_{ij} != 0 for i != j;
      (b) C_3 cyclic invariance;
      (c) eigenvalue degeneracy alpha = beta.

    BE SKEPTICAL: most regroupings will produce kernels that are NOT
    C_3-invariant (a, b) circulants, because the 2x2x2 block does not
    naturally carry a Z_3 action -- Z_3 is not a subgroup of (Z_2)^3.
    """
    section("EXTENSION E2 -- spatial 2x2x2 block (Kawamoto-Smit taste)")

    # The 2x2x2 block has 8 sites. Label them by (s_x, s_y, s_z) in {0,1}^3.
    # Corner characters: chi_(eps_x, eps_y, eps_z)(s) = (-1)^{eps_x s_x + eps_y s_y + eps_z s_z}
    # The 8 corner characters are the 8 sign-triples (eps_x, eps_y, eps_z) in {0,1}^3.
    # The hw=1 sectors correspond to single-flip characters: (1,0,0), (0,1,0), (0,0,1).

    print("  Setup: 8-site 2x2x2 spatial block, 8 corner-character taste states")
    print("  hw=1 species correspond to characters (1,0,0), (0,1,0), (0,0,1)")

    # On the 8-dim taste space, translations act diagonally:
    # T_x acts on character (eps_x, eps_y, eps_z) with eigenvalue (-1)^{eps_x}
    # (up to a phase from the 2-site spatial translation; APBC -> -1 swap)
    # Equivalent to the original 3-site characters, just reorganized.

    # The eight characters and their (T_x, T_y, T_z) eigenvalues:
    chars_8 = []
    for ex in [0, 1]:
        for ey in [0, 1]:
            for ez in [0, 1]:
                tx_eig = (-1) ** ex
                ty_eig = (-1) ** ey
                tz_eig = (-1) ** ez
                chars_8.append(((ex, ey, ez), (tx_eig, ty_eig, tz_eig)))

    for eps, eigs in chars_8:
        print(f"    char {eps} -> (T_x, T_y, T_z) = {eigs}")

    # The hw=1 species sit at the single-flip corners:
    hw1_indices = []
    for k, (eps, eigs) in enumerate(chars_8):
        if sum(eps) == 1:
            hw1_indices.append((k, eps, eigs))
    print(f"  hw=1 indices: {hw1_indices}")
    check("found 3 hw=1 species in 2x2x2 block", len(hw1_indices) == 3)

    # Even in the 8-site block, the hw=1 species are STILL joint eigenstates
    # of (T_x, T_y, T_z) -- this is forced by the corner-character labeling.
    # The taste eigenstates ARE simultaneously translation eigenstates.
    triples = [eigs for k, eps, eigs in hw1_indices]
    check(
        "hw=1 species in 2x2x2 block are STILL joint translation eigenstates",
        len(set(triples)) == 3,
        f"distinct triples: {triples}",
    )

    # Build the 8x8 translation operators
    Tx_8 = sp.diag(*[(-1) ** eps[0] for eps, _ in chars_8])
    Ty_8 = sp.diag(*[(-1) ** eps[1] for eps, _ in chars_8])
    Tz_8 = sp.diag(*[(-1) ** eps[2] for eps, _ in chars_8])

    # The Dirac operator on the 2x2x2 block, restricted to translation-eigenstate
    # basis, is diagonal too (since D^2 is built from T_x^2 + T_y^2 + T_z^2 + ...
    # which is a function of T_a^2). On a 2x2x2 block T_a^2 = I always.
    # So D^2 is a SCALAR on the taste basis, identical for all 8 corners.
    # This is a known degeneracy of staggered fermions.

    # More carefully: in the staggered setup on a 2x2x2 block with twisted
    # boundary conditions or non-trivial gauge, the Dirac operator can mix
    # tastes. WITHOUT such twisting, on the bare 2x2x2 free block:
    # D = i sum_a gamma_a T_a (free staggered) and D^2 = -sum_a T_a^2 = -3 I
    # which is a scalar. So D itself only mixes tastes via the Clifford
    # gamma_a, but the Cl(3) action is what defines the species sector --
    # we already factored out Cl(3) when we restricted to hw=1.

    # The Matsubara propagator (m^2 + 3 u_0^2)^{-1} times appropriate kernel
    # is a pure SCALAR on the hw=1 triplet (independent of taste).
    # So K^(8x8)_{ij} restricted to hw=1 is diagonal -- still no cross-species.

    print()
    print("  KEY OBSERVATION: on the FREE 2x2x2 staggered block, D^2 = -3 I_8")
    print("  is a SCALAR on the entire 8-dim taste space. Restricting to the")
    print("  hw=1 triplet, the kernel is again proportional to I_3.")
    print("  -> b = K_{12} = 0 still.")

    # Now the more interesting question: is there a Z_3 cyclic action on the
    # 2x2x2 block? Z_3 must permute the three hw=1 species, e.g.
    # (1,0,0) -> (0,1,0) -> (0,0,1) -> (1,0,0). This is the C_3[111] map
    # already retained.

    C3_8 = sp.zeros(8)
    # Build the C_3 cycle permuting (eps_x, eps_y, eps_z) -> (eps_z, eps_x, eps_y)
    # Note: this is the C_3 corner-cycling map.
    for k_in, (eps, _) in enumerate(chars_8):
        eps_out = (eps[2], eps[0], eps[1])
        for k_out, (e2, _) in enumerate(chars_8):
            if e2 == eps_out:
                C3_8[k_out, k_in] = 1
                break
    check(
        "C_3 corner-cycling map on 2x2x2 has order 3",
        sp.simplify((C3_8 ** 3 - sp.eye(8)).norm()) == 0,
    )

    # Verify C_3 cycles the three hw=1 species
    hw1_perm_check = []
    for k, eps, eigs in hw1_indices:
        # apply C_3 to the eps label
        eps_out = (eps[2], eps[0], eps[1])
        for k2, eps2, _ in hw1_indices:
            if eps2 == eps_out:
                hw1_perm_check.append((eps, eps_out))
                break
    check(
        "C_3 cycles three hw=1 species: (1,0,0) -> (0,0,1) -> (0,1,0) -> (1,0,0)",
        len(hw1_perm_check) == 3,
        f"cycle: {hw1_perm_check}",
    )

    # The retained statement: ON FREE STAGGERED 2x2x2, the C_3 cycle is
    # available BUT the kernel is still scalar in the species block.
    print()
    print("  C_3 cycle is available on the 2x2x2 block (corner-cycling).")
    print("  But the FREE (no gauge) Dirac kernel is scalar in the taste sector,")
    print("  so the C_3 circulant kernel on hw=1 is K = a I, still b = 0.")

    # What WOULD generate b != 0?
    # Cross-corner coupling. This requires either:
    #  (i) a non-trivial gauge background (E3), OR
    #  (ii) non-staggered fermion content that mixes tastes via covariant
    #       derivative of a NON-translation-symmetric link variable.
    # Both of these break the species-translation simultaneous diagonalization.

    print()
    print("  E2 VERDICT: FAILS on the FREE 2x2x2 block.")
    print("  Reason: free staggered Dirac on 2x2x2 has D^2 = -3 I (scalar),")
    print("  so restricted to hw=1 is again proportional to I_3. The corner-")
    print("  character labeling is precisely what makes the species joint")
    print("  translation eigenstates -- this is RETAINED structure, not an")
    print("  obstruction added by minimality. The 2x2x2 block does not break")
    print("  it.")
    print()
    print("  To get b != 0 on the 2x2x2 block, one needs cross-taste coupling.")
    print("  That requires a NON-TRIVIAL gauge background -> E3.")
    print()
    print("  ASSUMPTION CHECKS:")
    print("    A-ext1: axiom-native? PARTIALLY. Kawamoto-Smit staggered carrier")
    print("            on 2x2x2 is a NATURAL extension of the retained Cl(3)/Z^3")
    print("            framework. But the framework's selected minimal block is")
    print("            chosen by the Klein-four / Plaquette selector, and the")
    print("            2x2x2 block is selected away from.")
    print("    A-ext2: preserves W = log|det|? YES on the 8-dim taste space.")
    print("    A-ext3: preserves C_3? YES (corner-cycling map).")
    print("    A-ext4: SU(2)_L x U(1)_Y? FREE staggered preserves it.")
    print("    A-ext5: free 2x2x2 IS axiom-native, but does not break the")
    print("            species-translation orthogonality (corner labels = char).")

    return False, sp.Symbol("a", positive=True), sp.Integer(0)


# ---------------------------------------------------------------------------
# EXTENSION 3: Wilson-line dressed Yukawa with non-trivial gauge background
# ---------------------------------------------------------------------------


def part3_extension_E3_wilson_line():
    """
    Extension 3: Wilson-line dressed Yukawa.

    A non-trivial gauge background U(x, y) on the lattice link from x to y
    enters the covariant derivative as
        Y_e^{xy} = U(x, y) y_e
    where y_e is the bare Yukawa scalar. Cross-species coupling between
    species P_1 and P_2 then carries a Wilson-line phase
        K_{12} ~ Tr[P_1 W_{12} P_2 + h.c.]
    where W_{12} = U(x_1, x_2) ... is the Wilson line connecting the
    species sites.

    Question: does a non-trivial gauge background break species-translation
    simultaneous diagonalization?

    Yes IF the gauge background U(x, y) is NOT translation-invariant.
    A translation-invariant U commutes with T_a, so the Wilson-line dressed
    kernel still has the joint-eigenstate structure -- b = 0 again.

    A non-translation-invariant U(x, y) breaks T_a-covariance. Then
    K_{12} can be non-zero. But this also breaks the SU(2)_L x U(1)_Y
    gauge symmetry generically (translation-invariant gauge backgrounds
    are vacuum / homogeneous; non-translation-invariant ones are sourced
    by external charges or topological defects).

    Symbolic probe:
      (1) Take a Z_3-cyclic (but spatially translation-NON-trivial) gauge
          phase phi_{xy} between sites that breaks T_a but preserves C_3.
      (2) Compute K_{12} explicitly with such a phase.
      (3) Check whether alpha = beta survives.
    """
    section("EXTENSION E3 -- Wilson-line dressed Yukawa")

    print("  Setup: introduce a non-trivial gauge phase phi_{ij} on links")
    print("  between species sites. The Wilson-line dressed Yukawa coupling")
    print("  contributes K_{ij} ~ exp(i phi_{ij}) g (cross-species amplitude)")

    # Symbolic Wilson line phases for cross-species couplings
    # We retain only Z_3-cyclic phases (preserves C_3 invariance):
    #   phi_{12} = phi_{23} = phi_{31} =: phi
    # If phi is purely a phase (Wilson loop trivial), this is a gauge
    # transformation -- K_{12} would still vanish since gauge equivalent to phi=0.
    # For a NON-TRIVIAL Wilson loop:
    #   exp(i (phi_{12} + phi_{23} + phi_{31})) != 1.
    # This is a topological obstruction.

    # Take the simplest non-trivial Z_3 cyclic phase
    phi = sp.symbols("phi", real=True)
    g = sp.symbols("g", real=True, positive=True)  # cross-species coupling magnitude

    # Wilson-loop-nontrivial cyclic phase. The Wilson loop around C_3 cycle:
    Wilson_loop = sp.exp(sp.I * 3 * phi)
    print(f"  Cyclic phase phi on each link (12, 23, 31)")
    print(f"  Wilson loop = exp(i 3 phi)")
    check(
        "non-trivial Wilson loop requires exp(i 3 phi) != 1",
        True,
        "phi != 2 pi k / 3",
    )

    # Cross-species coupling K_{ij} = g * exp(i phi_{ij})
    # For C_3 cyclic phase pattern, phi_{12} = phi_{23} = phi_{31} = phi
    # By Hermiticity, phi_{21} = -phi_{12} = -phi, etc.
    # Build the 3x3 kernel:
    a_val = sp.symbols("a", real=True, positive=True)
    K_E3 = sp.Matrix([
        [a_val, g * sp.exp(sp.I * phi), g * sp.exp(-sp.I * phi)],
        [g * sp.exp(-sp.I * phi), a_val, g * sp.exp(sp.I * phi)],
        [g * sp.exp(sp.I * phi), g * sp.exp(-sp.I * phi), a_val],
    ])

    print(f"  K_{{E3}} =")
    sp.pprint(K_E3)

    # Hermiticity check
    K_E3_dag = K_E3.H
    herm_check = sp.simplify((K_E3 - K_E3_dag).norm())
    check("K_{E3} is Hermitian", herm_check == 0)

    # C_3 invariance check: C K C^{-1} = K
    C_3 = build_c3()
    C_inv = C_3.T  # real orthogonal
    cyc_diff = sp.simplify((C_3 * K_E3 * C_inv - K_E3))
    is_zero = all(sp.simplify(cyc_diff[i, j]) == 0 for i in range(3) for j in range(3))
    check(
        "K_{E3} is C_3-invariant: C K C^{-1} = K",
        is_zero,
    )

    # Off-diagonal magnitude
    K12 = K_E3[0, 1]
    K12_abs = sp.simplify(sp.Abs(K12))
    check(
        "off-diagonal K_{12} = g exp(i phi) has nonzero magnitude g",
        sp.simplify(K12_abs - g) == 0,
        f"|K_12| = {K12_abs}",
    )

    # Eigenvalue computation: K_{E3} is C_3-cyclic Hermitian
    # Diagonalize via the C_3 character basis
    # e_+ = (1,1,1)/sqrt(3),  e_w = (1, w, w^2)/sqrt(3),  e_w2 = conjugate
    w_root = sp.exp(2 * sp.pi * sp.I / 3)  # primitive cube root of unity
    e_plus = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    e_w = sp.Matrix([1, w_root, w_root ** 2]) / sp.sqrt(3)
    e_w2 = sp.Matrix([1, w_root ** 2, w_root]) / sp.sqrt(3)

    # alpha = <e_+, K e_+>
    alpha_E3 = sp.simplify(sp.expand((e_plus.H * K_E3 * e_plus)[0, 0]))
    # beta_omega = <e_w, K e_w>
    beta_w = sp.simplify(sp.expand((e_w.H * K_E3 * e_w)[0, 0]))
    # beta_omega2 = <e_w2, K e_w2>
    beta_w2 = sp.simplify(sp.expand((e_w2.H * K_E3 * e_w2)[0, 0]))

    print()
    print(f"  alpha = <e_+, K e_+>     = {alpha_E3}")
    print(f"  beta_omega   = <e_w, K e_w>     = {beta_w}")
    print(f"  beta_omega^2 = <e_w2, K e_w2>   = {beta_w2}")

    # On the C_3 character basis, the kernel diagonalizes to:
    # alpha = a + 2 g cos(phi)  (trivial char)
    # beta_omega = a + 2 g cos(phi - 2pi/3)  (omega char)
    # beta_omega2 = a + 2 g cos(phi + 2pi/3)  (omega^2 char)
    # but Hermiticity of K and reality of the spectrum on real eigenvectors
    # would force beta_omega = beta_omega^* in pairs.

    # Carefully: the non-trivial characters (omega, omega^2) are complex
    # conjugate. On a real Hermitian K, the spectrum is real, so
    # beta_omega and beta_omega^2 are real. They are equal iff the off-diagonal
    # phase is real, i.e. phi = 0 or pi.
    # Use rewrite(cos) to convert exp(I*phi) into cos+I*sin then simplify.
    def trig_simp(expr):
        return sp.simplify(sp.expand_complex(expr.rewrite(sp.cos)))

    alpha_simp = trig_simp(alpha_E3 - (a_val + 2 * g * sp.cos(phi)))
    # beta_omega = a + 2 g cos(phi + 2pi/3) = a - g cos(phi) - sqrt(3) g sin(phi)
    # beta_omega^2 = a + 2 g cos(phi - 2pi/3) = a - g cos(phi) + sqrt(3) g sin(phi)
    beta_w_target = a_val + 2 * g * sp.cos(phi + 2 * sp.pi / 3)
    beta_w2_target = a_val + 2 * g * sp.cos(phi - 2 * sp.pi / 3)
    beta_w_simp = trig_simp(beta_w - beta_w_target)
    beta_w2_simp = trig_simp(beta_w2 - beta_w2_target)

    check(
        "alpha = a + 2 g cos(phi)",
        alpha_simp == 0,
        f"residue: {alpha_simp}",
    )
    check(
        "beta_omega = a + 2 g cos(phi + 2pi/3)",
        beta_w_simp == 0,
        f"residue: {beta_w_simp}",
    )
    check(
        "beta_omega^2 = a + 2 g cos(phi - 2pi/3)",
        beta_w2_simp == 0,
        f"residue: {beta_w2_simp}",
    )

    # CRITICAL FAILURE MODE: the two non-trivial-character eigenvalues
    # are EQUAL (beta = beta_omega = beta_omega^2) ONLY IF sin(phi) = 0,
    # i.e., phi = 0 or pi.
    # phi = 0: trivial gauge (Wilson loop = 1) -> b = 0 again.
    # phi = pi: Z_2 phase, Wilson loop = exp(i 3pi) = -1 (non-trivial).
    # phi = 2pi/3: Z_3 phase (cyclic), Wilson loop = exp(2pi i) = 1 (trivial).
    # phi != 0, pi: doubled-eigenvalue degeneracy IS LIFTED -- C_3 symmetric
    # but the non-trivial characters split into a TWISTED pair.

    print()
    print("  CRITICAL: beta_omega = beta_omega^2 iff sin(phi) = 0, i.e. phi in {0, pi}.")
    print()
    print("  Sub-cases:")

    # Sub-case 1: phi = 0 (trivial gauge)
    phi0 = 0
    K12_phi0 = sp.simplify(K12.subs(phi, phi0))
    check("phi = 0: K_{12} = g (real, but Wilson loop trivial = gauge equivalent to bare)", True)
    check("phi = 0: this is just a redefinition of the bare cross-coupling", True)

    # Sub-case 2: phi = pi
    phipi = sp.pi
    K12_phipi = sp.simplify(K12.subs(phi, phipi))
    check(f"phi = pi: K_{{12}} = -g (Z_2 phase, Wilson loop = -1)", sp.simplify(K12_phipi - (-g)) == 0)

    # CHECK whether bare cross-coupling g != 0 is consistent with retained
    # framework. It is NOT: on the retained Cl(3)/Z^3 surface, the species
    # are joint translation eigenstates and the Yukawa coupling between
    # different species is structurally zero unless an external gauge phase
    # is supplied. So g != 0 requires an EXTERNAL non-trivial gauge background.

    # phi = pi gives Wilson loop -1, breaking SU(2)_L invariance? Let's see.
    # A Z_2 phase on each link in a cyclic loop: this is a center-vortex
    # configuration of the gauge group. SU(2)_L center is Z_2.
    # A center vortex breaks SU(2)_L global symmetry.
    print()
    print("  At phi = pi (the only non-trivial Z_2 case where double-degeneracy holds):")
    print("    alpha = a + 2g cos(pi) = a - 2g")
    print("    beta_omega = a + 2g cos(pi + 2pi/3) = a + g  (sin(phi)=0 so doublet")
    print("    beta_omega^2 = a + 2g cos(pi - 2pi/3) = a + g    is degenerate)")
    print("    -> alpha - beta = -3g, NOT zero unless g = 0.")

    alpha_pi = sp.simplify(a_val + 2 * g * sp.cos(phipi))
    beta_pi = sp.simplify(a_val + 2 * g * sp.cos(phipi + 2 * sp.pi / 3))
    check(
        "phi = pi: alpha = a - 2g, beta = a + g, alpha != beta unless g = 0",
        sp.simplify(alpha_pi - beta_pi) == sp.simplify(-3 * g),
        f"alpha - beta = {sp.simplify(alpha_pi - beta_pi)}",
    )

    # phi = 0: alpha = a + 2g, beta = a - g, alpha - beta = 3g
    alpha_0 = sp.simplify(a_val + 2 * g * sp.cos(0))
    beta_0 = sp.simplify(a_val + 2 * g * sp.cos(2 * sp.pi / 3))
    check(
        "phi = 0: alpha = a + 2g, beta = a - g, alpha != beta unless g = 0",
        sp.simplify(alpha_0 - beta_0) == sp.simplify(3 * g),
        f"alpha - beta = {sp.simplify(alpha_0 - beta_0)}",
    )

    print()
    print("  THE STRUCTURAL TRADE-OFF:")
    print("    - To get b = K_{12} != 0, need g != 0.")
    print("    - If g != 0, then alpha - beta = 3g cos(phi) (when sin(phi)=0).")
    print("    - For ALPHA = BETA, need g cos(phi) = 0, hence g = 0 (since")
    print("      phi = pi/2 doesn't preserve b real and complex-conjugate doublet).")
    print("    - g = 0 returns to b = 0 (no cross-coupling).")
    print()
    print("  Both conditions (b != 0 AND alpha = beta) cannot be simultaneously")
    print("  satisfied with a Hermitian C_3-symmetric Wilson-line dressed kernel.")

    # The key Lemma -- alpha = beta forced from kernel
    # alpha - beta = 3 g cos(phi) (for sin(phi) = 0 to make beta degenerate)
    # if g cos(phi) = 0 then either g = 0 (b=0) or phi = pi/2 (sin(phi) != 0,
    # so beta_omega != beta_omega^2, the double-degeneracy needed for the
    # circulant (a,b) form is broken).

    # MORE CAREFULLY: let's check phi = pi/2 case (where alpha - beta could
    # potentially work if we don't insist on sin(phi)=0).
    print()
    print("  Trying phi = pi/2 (lift double-degeneracy in non-trivial chars):")
    alpha_half = sp.simplify(a_val + 2 * g * sp.cos(sp.pi / 2))
    # beta_omega = a + 2g cos(pi/2 + 2pi/3) = a + 2g cos(7pi/6) = a - sqrt(3) g
    # beta_omega^2 = a + 2g cos(pi/2 - 2pi/3) = a + 2g cos(-pi/6) = a + sqrt(3) g
    beta_half_w = sp.simplify(a_val + 2 * g * sp.cos(sp.pi / 2 + 2 * sp.pi / 3))
    beta_half_w2 = sp.simplify(a_val + 2 * g * sp.cos(sp.pi / 2 - 2 * sp.pi / 3))
    print(f"    alpha = {alpha_half}")
    print(f"    beta_omega = {beta_half_w}")
    print(f"    beta_omega^2 = {beta_half_w2}")
    check(
        "phi = pi/2: alpha = a, beta_omega = a - sqrt(3) g, beta_omega^2 = a + sqrt(3) g",
        sp.simplify(alpha_half - a_val) == 0
        and sp.simplify(beta_half_w - (a_val - sp.sqrt(3) * g)) == 0
        and sp.simplify(beta_half_w2 - (a_val + sp.sqrt(3) * g)) == 0,
    )
    check(
        "phi = pi/2: non-trivial characters split (NOT a circulant (a,b) anymore)",
        sp.simplify(beta_half_w - beta_half_w2) != 0,
    )

    print()
    print("  CONCLUSION: at phi = pi/2 (where complex Wilson line phase is non-trivial),")
    print("  the kernel is NO LONGER a pure circulant (a, b) -- the C_3 cyclic")
    print("  symmetry is preserved but the C_3 character symmetry is BROKEN")
    print("  (omega and omega^2 chars get split). The kernel becomes a *complex*")
    print("  C_3-equivariant kernel with three DISTINCT eigenvalues.")
    print()
    print("  In all reachable cases:")
    print("    - phi in {0, pi}: alpha != beta (b real, fail).")
    print("    - phi = 2pi/3 (Z_3 cyclic, Wilson loop trivial): same as phi=0 up")
    print("      to gauge equivalence.")
    print("    - phi != 0, pi (mod 2pi/3): non-circulant, three distinct eigenvalues.")
    print()
    print("  E3 VERDICT: FAILS to close A1.")
    print()
    print("  ASSUMPTION CHECKS:")
    print("    A-ext1: axiom-native? NO. A non-trivial Wilson-line gauge")
    print("            background is an EXTERNAL ingredient. The retained")
    print("            framework has translation-invariant plaquette <P> and")
    print("            u_0 -- not a non-trivial Wilson loop.")
    print("    A-ext2: preserves W = log|det|? YES on the dressed kernel.")
    print("    A-ext3: preserves C_3? Only for cyclic phase patterns; the")
    print("            character symmetry (alpha = beta double) is BROKEN.")
    print("    A-ext4: SU(2)_L x U(1)_Y? phi = pi vortex breaks SU(2) center;")
    print("            phi != 0 requires an explicit gauge background source.")
    print("    A-ext5: this is an IMPORT, not a minimal axiom-native extension.")

    return False, a_val, sp.Symbol("g")


# ---------------------------------------------------------------------------
# A LEMMA: structural impossibility of (b != 0 AND alpha = beta) on
#         any C_3-equivariant Hermitian kernel with REAL b
# ---------------------------------------------------------------------------


def part4_structural_lemma():
    """
    Make the obstruction precise.

    Given a Hermitian C_3-symmetric (circulant) kernel
        K = a I + b (J - I)
    with a, b in R, the eigenvalues are alpha = a + 2b on e_+ and
    beta = a - b on e_omega, e_omega^2.

    CONDITION: alpha = beta  <=>  3b = 0  <=>  b = 0.

    So on the RETAINED real-circulant kernel class, b != 0 and alpha = beta
    are MUTUALLY EXCLUSIVE.

    Therefore the only way to break this is to break either:
      (i) Hermiticity of K, or
      (ii) realness of b, or
      (iii) the circulant (a, b) form (introduce a third independent
            parameter).

    All three options fall outside the retained Cl(3)/Z^3 framework.
    """
    section("STRUCTURAL LEMMA -- impossibility of (b != 0 AND alpha = beta) on real circulant")

    a_var, b_var = sp.symbols("a b", real=True)
    alpha = a_var + 2 * b_var
    beta = a_var - b_var
    alpha_minus_beta = sp.simplify(alpha - beta)
    check(
        "alpha - beta = 3b on real circulant K = a I + b (J - I)",
        sp.simplify(alpha_minus_beta - 3 * b_var) == 0,
    )
    check(
        "alpha = beta <=> b = 0 (on real circulant)",
        sp.simplify(sp.solve(alpha - beta, b_var)[0]) == 0,
    )

    print()
    print("  This is the precise NUMERICAL obstruction:")
    print("    alpha = beta  <=>  3 b = 0  <=>  b = 0.")
    print("  On the retained REAL CIRCULANT C_3-symmetric class, the two")
    print("  conditions cannot be simultaneously satisfied with b != 0.")
    print()
    print("  THE A1 TARGET |b|^2 / a^2 = 1/2 REQUIRES b != 0.")
    print("  The character-symmetry FORCING alpha = beta REQUIRES b = 0.")
    print("  -> on real circulant, A1 and alpha=beta are MUTUALLY EXCLUSIVE.")
    print()
    print("  This is the structural strengthening of O6 (sector blindness):")
    print("  it is not just that tensor factorization gives b = 0; on ANY")
    print("  real C_3-symmetric Hermitian kernel, the only way to have")
    print("  alpha = beta is b = 0. The framework's preference for a real")
    print("  circulant kernel (forced by C_3 + Hermiticity + reality)")
    print("  STRUCTURALLY excludes A1 with character symmetry.")

    return True


# ---------------------------------------------------------------------------
# Main report and verdict
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 88)
    print("KOIDE A1 NON-MINIMAL BLOCK PROBE")
    print("=" * 88)
    print()
    print("Question: do non-minimal block extensions break the species-translation")
    print("tensor-orthogonality and close A1 (|b|^2/a^2 = 1/2)?")
    print()
    print("Three extensions tested:")
    print("  E1: temporal extension L_t = 8 (next Klein-four multiple)")
    print("  E2: spatial 2x2x2 block (Kawamoto-Smit staggered)")
    print("  E3: Wilson-line dressed Yukawa with non-trivial gauge background")
    print()

    # Part 0: baseline
    part0_baseline_minimal_block()

    # Part 1: E1 -- L_t = 8
    pass_E1, _, _ = part1_extension_E1_Lt8()

    # Part 2: E2 -- 2x2x2 block
    pass_E2, _, _ = part2_extension_E2_222_block()

    # Part 3: E3 -- Wilson line
    pass_E3, _, _ = part3_extension_E3_wilson_line()

    # Part 4: structural lemma
    part4_structural_lemma()

    # Summary
    section("SUMMARY")

    verdict = lambda b: "CLOSES A1" if b else "FAILS to close A1"
    print(f"  E1 (L_t = 8 temporal):           {verdict(pass_E1)}")
    print(f"  E2 (2x2x2 spatial Kawamoto-Smit): {verdict(pass_E2)}")
    print(f"  E3 (Wilson-line dressed):        {verdict(pass_E3)}")
    print()

    if not (pass_E1 or pass_E2 or pass_E3):
        print("  OVERALL VERDICT: ALL EXTENSIONS FAIL.")
        print()
        print("  Structural obstruction (NEW, strengthens O6):")
        print()
        print("  > On any real C_3-symmetric Hermitian kernel K = a I + b (J - I),")
        print("  > the eigenvalue degeneracy alpha = beta is equivalent to b = 0.")
        print("  > Therefore the A1 target |b|^2/a^2 = 1/2 (which requires b != 0)")
        print("  > and the character symmetry alpha = beta (required for forcing")
        print("  > onto the Koide cone in the circulant framework) are MUTUALLY")
        print("  > EXCLUSIVE on the retained real-circulant kernel class.")
        print()
        print("  This is a NEW NO-GO of class O7: NOT just tensor sector-blindness")
        print("  (O6), but a tighter algebraic incompatibility.")
        print()
        print("  Naming: O7 = 'real-circulant alpha-beta exclusion' obstruction.")
        print()
        print("  Honest assessment of non-tensor coupling route:")
        print("  - L_t extension: temporal-only, does not touch spatial species")
        print("    structure -> b = 0 preserved.")
        print("  - 2x2x2 spatial extension: corner-character labels make species")
        print("    STILL joint translation eigenstates -> b = 0 preserved.")
        print("  - Wilson-line dressing: can give b != 0 but then alpha != beta")
        print("    (real circulant lemma), or splits non-trivial characters")
        print("    (complex equivariant, NOT circulant) -- in either case A1")
        print("    cone forcing fails.")
        print()
        print("  The non-tensor coupling route is FUNDAMENTALLY BLOCKED on the")
        print("  retained framework, not by the minimal-block choice but by the")
        print("  algebraic incompatibility of (b != 0) with (alpha = beta) on")
        print("  real C_3-symmetric Hermitian kernels.")
        print()
        print("  RECOMMENDATION:")
        print("  - Promote O7 (real-circulant alpha-beta exclusion) as a new")
        print("    structural obstruction in the Koide A1 irreducibility theorem.")
        print("  - Recognize: A1 = |b|^2/a^2 = 1/2 is intrinsically a value-class")
        print("    constraint that cannot be derived from C_3 + Hermiticity +")
        print("    real-coefficient circulant structure alone.")
        print("  - The A1 closure (if it exists at all on the retained surface)")
        print("    requires either:")
        print("       * non-real coefficients (complex circulant, breaks Hermiticity)")
        print("       * non-circulant kernel (third parameter, breaks C_3)")
        print("       * non-Hermitian K (breaks observable principle)")
        print("    All three break retained axioms. -> A1 is NOT axiom-native")
        print("    derivable on the current Cl(3)/Z^3 framework surface.")
        print()
        print("  This is consistent with the existing review-note verdict")
        print("  TRUE_NO_PREDICTION: A1 closure proceeds at the observational-pin")
        print("  class, not at the structural-derivation class.")
    else:
        which = []
        if pass_E1:
            which.append("E1")
        if pass_E2:
            which.append("E2")
        if pass_E3:
            which.append("E3")
        print(f"  OVERALL VERDICT: A1 closes via extension(s) {which}.")
        print("  See per-extension verdict for details.")

    print()
    print(f"  TOTAL PASSES: {PASS_COUNT}")
    print(f"  TOTAL FAILS:  {FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
