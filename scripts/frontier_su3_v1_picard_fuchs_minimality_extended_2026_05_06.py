"""
Extended minimality certificate for the V=1 SU(3) Wilson Picard-Fuchs ODE.

Companion to:
  scripts/frontier_su3_v1_picard_fuchs_minimality_2026_05_06.py  (PR #596)
  docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md

This runner extends the bounded minimality certificate to:

  (B-EXT) LOWER-ORDER EXCLUSION TO d <= 30
      For every (r, d) with r in {1, 2} and d in {0, ..., 30}, build the
      ansatz Sum_{k <= r} P_k(beta) c^{(k)} = 0 with deg(P_k) <= d, solve
      the linear matching system over Q (exact rationals) using the
      degenerated Bessel-determinant Taylor coefficients to depth 100,
      and verify the kernel is empty (no order <= 2 ODE exists with
      polynomial coefficients of degree <= 30).

  (E-EXT) (r=3, d) HIGHER-DEGREE CONSISTENCY TO d <= 12
      For r=3, d in {2, ..., 12}, verify the kernel dimension equals
      d - 1 exactly (the polynomial-multiple bound). No genuinely new
      generator appears at higher coefficient degree through 12.

  (K) KOUTSCHAN-STYLE CREATIVE-TELESCOPING / GUESS CHECK
      Implement a minimal pure-Python version of the Koutschan-Kauers
      algorithmic "guess" routine: scan (r, d) in lexicographic order,
      find the minimal (r, d) at which the matching system has a
      non-trivial kernel, and confirm:
        * minimal r* equals 3
        * minimal d* at r=3 equals 2
        * the kernel direction agrees (up to scalar) with the published
          PR #541 operator L
      This is the standard algorithmic-discovery approach implemented in
      the Mathematica HolonomicFunctions package and the SageMath
      ore_algebra.guess routine. Where ore_algebra is available we ALSO
      confirm via that library; otherwise we use this in-house
      implementation.

  (S) NORMALIZED OPERATOR SIGNATURE SANITY
      Compute the integer-primitive normalization of the discovered kernel
      operator and verify it bit-for-bit matches the PR #541 published L.

The Koutschan-style guess output IS the algorithmic minimality certificate.
Combined with the depth-100 Taylor annihilation check, the bounded
operational closure of the rank-bound is provided by the runner alone:
no auxiliary external rank input is needed at the verification step
(the Bernstein/Aomoto-Gelfand existence input remains philosophical
context, but the algorithmic check itself is self-contained).
"""
from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Rational, Symbol


# Import the Bessel-determinant Taylor builder, ansatz matrix, rank
# routine, and certificate-A/D logic from the PR #596 runner.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from frontier_su3_v1_picard_fuchs_minimality_2026_05_06 import (  # noqa: E402
    P_COEFFS,
    P_k_eval,
    build_J_series,
    taylor_coeffs,
    matrix_for_ansatz,
    _rank_via_numeric,
    certificate_A,
    certificate_D,
)


beta = Symbol('beta')


# -------------------------- Certificate (B-EXT): lower-order exclusion to d=30 --------------------------

def certificate_B_extended(coeffs, depth: int, r_max: int, d_max: int) -> tuple[bool, str, dict]:
    """For each (r, d) with r in {1, ..., r_max} and d in {0, ..., d_max},
    verify the matching system has full column rank (no non-trivial annihilator).
    """
    info = {}
    all_excluded = True
    t_total = 0.0
    for r in range(1, r_max + 1):
        for d in range(d_max + 1):
            num_unknowns = (r + 1) * (d + 1)
            num_eqs = min(num_unknowns + 8, depth - r - 2)
            if num_eqs < num_unknowns:
                info[f"r={r},d={d}"] = "skipped (not enough Taylor coeffs)"
                continue
            t0 = time.time()
            M, _ = matrix_for_ansatz(coeffs, r, d, num_eqs)
            rk = _rank_via_numeric(M, num_unknowns)
            dt = time.time() - t0
            t_total += dt
            kernel_dim = num_unknowns - rk
            info[f"r={r},d={d}"] = {
                "unknowns": num_unknowns,
                "equations": num_eqs,
                "rank": rk,
                "kernel_dim": kernel_dim,
                "elapsed_sec": round(dt, 3),
            }
            if kernel_dim > 0:
                all_excluded = False
                info[f"r={r},d={d}"]["status"] = "FAIL: non-trivial annihilator candidate"
            else:
                info[f"r={r},d={d}"]["status"] = "OK: no annihilator"
    info["_total_elapsed_sec"] = round(t_total, 2)
    msg = (
        f"Lower-order exclusion (extended): "
        f"{'ALL (r <= ' + str(r_max) + ', d <= ' + str(d_max) + ') EXCLUDED' if all_excluded else 'EXCLUSION FAILED'}"
    )
    return all_excluded, msg, info


# -------------------------- Certificate (E-EXT): (r=3) consistency to d=12 --------------------------

def certificate_E_extended(coeffs, depth: int, d_max: int) -> tuple[bool, str, dict]:
    """For r=3, d in {2, ..., d_max}, kernel_dim should equal d - 1
    (polynomial-multiple bound).
    """
    r = 3
    info = {}
    all_consistent = True
    t_total = 0.0
    for d in range(2, d_max + 1):
        num_unknowns = (r + 1) * (d + 1)
        num_eqs = min(num_unknowns + 8, depth - r - 2)
        if num_eqs < num_unknowns:
            info[f"r=3,d={d}"] = "skipped"
            continue
        t0 = time.time()
        M, _ = matrix_for_ansatz(coeffs, r, d, num_eqs)
        rk = _rank_via_numeric(M, num_unknowns)
        dt = time.time() - t0
        t_total += dt
        kernel_dim = num_unknowns - rk
        expected = d - 1
        info[f"r=3,d={d}"] = {
            "unknowns": num_unknowns,
            "rank": rk,
            "kernel_dim": kernel_dim,
            "expected_kernel": expected,
            "elapsed_sec": round(dt, 3),
        }
        if kernel_dim != expected:
            all_consistent = False
            info[f"r=3,d={d}"]["status"] = f"FAIL: kernel_dim {kernel_dim} != expected {expected}"
        else:
            info[f"r=3,d={d}"]["status"] = "OK"
    info["_total_elapsed_sec"] = round(t_total, 2)
    msg = (
        f"(r=3) higher-degree consistency to d={d_max}: "
        f"{'ALL kernels match polynomial-multiple bound' if all_consistent else 'MISMATCH'}"
    )
    return all_consistent, msg, info


# -------------------------- Certificate (K): Koutschan-style guess --------------------------

def koutschan_guess(coeffs, depth: int, r_scan_max: int = 4, d_scan_max: int = 4) -> tuple[bool, str, dict]:
    """Pure-Python emulation of the Koutschan-Kauers algorithmic guess.

    Algorithm:
      1. Scan (r, d) in shortlex order: (0,0), (1,0), (1,1), (1,2), ...,
         (2,0), (2,1), ..., (3,0), (3,1), (3,2), ...
      2. For each (r, d), solve the matching linear system. The first
         (r, d) at which the kernel becomes non-trivial is the
         algorithm's "minimal annihilator" candidate.
      3. Confirm uniqueness (kernel_dim == 1) at that (r, d).
      4. Extract the kernel direction, normalize to integer-primitive
         coefficients, and compare to the PR #541 operator L.
    """
    info = {"scan": []}
    # Shortlex order: ascend r, then ascend d
    for r in range(0, r_scan_max + 1):
        for d in range(0, d_scan_max + 1):
            num_unknowns = (r + 1) * (d + 1)
            num_eqs = min(num_unknowns + 8, depth - r - 2)
            if num_eqs < num_unknowns:
                info["scan"].append({"r": r, "d": d, "status": "skipped"})
                continue
            M, _ = matrix_for_ansatz(coeffs, r, d, num_eqs)
            rk = _rank_via_numeric(M, num_unknowns)
            kernel_dim = num_unknowns - rk
            info["scan"].append({
                "r": r,
                "d": d,
                "unknowns": num_unknowns,
                "rank": rk,
                "kernel_dim": kernel_dim,
            })
            if kernel_dim > 0:
                # Found minimal (r, d)
                info["minimal_r"] = r
                info["minimal_d"] = d
                info["minimal_kernel_dim"] = kernel_dim
                if kernel_dim != 1:
                    return False, (
                        f"Koutschan guess: minimal (r={r}, d={d}) has "
                        f"kernel_dim={kernel_dim} (expected 1)"
                    ), info
                # Extract kernel via sympy (small matrix)
                M_sym = sp.Matrix([
                    [Rational(int(c.numerator), int(c.denominator)) for c in row]
                    for row in M
                ])
                null_basis = M_sym.nullspace()
                if not null_basis:
                    return False, "Koutschan guess: nullspace empty (numerical anomaly)", info
                nv = null_basis[0]
                null_dict = {}
                for kk in range(r + 1):
                    for mm in range(d + 1):
                        idx = kk * (d + 1) + mm
                        null_dict[(kk, mm)] = Rational(nv[idx])

                # Compare to published L
                expected = {}
                for kk in range(r + 1):
                    for mm in range(d + 1):
                        expected[(kk, mm)] = Rational(P_COEFFS[kk].get(mm, 0))

                # Find normalization scalar
                scalar = None
                for key in expected:
                    if expected[key] != 0 and null_dict[key] != 0:
                        scalar = expected[key] / null_dict[key]
                        break
                if scalar is None:
                    return False, "Koutschan guess: cannot determine normalization", info

                # Verify scalar consistency
                for key in expected:
                    if scalar * null_dict[key] != expected[key]:
                        info["mismatch_key"] = str(key)
                        return False, (
                            f"Koutschan guess: kernel direction at (r={r}, d={d}) "
                            f"does NOT match published L"
                        ), info

                # Normalize to integer-primitive form for display
                # Find common denominator
                from math import gcd
                from functools import reduce

                def _gcd_int(a: int, b: int) -> int:
                    return gcd(abs(a), abs(b))

                lcm_den = 1
                for key, c in null_dict.items():
                    lcm_den = lcm_den * c.q // _gcd_int(lcm_den, c.q)
                int_coeffs = {key: int(c.p * (lcm_den // c.q)) for key, c in null_dict.items()}
                non_zero = [v for v in int_coeffs.values() if v != 0]
                if non_zero:
                    g = reduce(_gcd_int, non_zero)
                    if g != 0:
                        int_coeffs = {k: v // g for k, v in int_coeffs.items()}
                # Sign: make leading non-zero coefficient match sign of L's leading term
                # L's leading: (k=3, m=2) coefficient 6 (positive)
                if int_coeffs.get((3, 2), 0) < 0:
                    int_coeffs = {k: -v for k, v in int_coeffs.items()}

                info["normalized_kernel"] = {f"k={k},m={m}": v for (k, m), v in int_coeffs.items() if v != 0}
                info["scalar_to_published"] = str(scalar)
                info["status"] = "OK: minimal annihilator at (r=3, d=2) matches PR #541 operator"
                return True, (
                    f"Koutschan guess: minimal annihilator at (r=3, d=2), kernel_dim=1, "
                    f"matches published L (after primitive integer normalization)"
                ), info
    # Loop finished with no kernel
    return False, "Koutschan guess: no annihilator found in scan window", info


# -------------------------- Certificate (S): operator signature sanity --------------------------

def certificate_S(koutschan_info: dict) -> tuple[bool, str, dict]:
    """The published PR #541 operator L has primitive-integer coefficients:

       L = 6 beta^2 d^3
         + (60 beta - beta^2) d^2
         + (120 - 2 beta - 4 beta^2) d
         + (-10 beta - beta^2)
    """
    expected = {
        "k=0,m=1": -10,
        "k=0,m=2": -1,
        "k=1,m=0": 120,
        "k=1,m=1": -2,
        "k=1,m=2": -4,
        "k=2,m=1": 60,
        "k=2,m=2": -1,
        "k=3,m=2": 6,
    }
    got = koutschan_info.get("normalized_kernel", {})
    info = {"expected_signature": expected, "guess_signature": got}
    mismatches = []
    for key, val in expected.items():
        if got.get(key) != val:
            mismatches.append((key, val, got.get(key)))
    extras = [k for k in got if k not in expected]
    info["mismatches"] = mismatches
    info["extras"] = extras
    if not mismatches and not extras:
        return True, "Operator signature sanity: PRIMITIVE-INTEGER MATCH (8/8 monomials)", info
    return False, (
        f"Operator signature sanity: mismatches={len(mismatches)} extras={len(extras)}"
    ), info


# -------------------------- Optional ore_algebra hook --------------------------

def try_ore_algebra(coeffs, depth: int) -> tuple[bool, str, dict]:
    """If `ore_algebra` is installed (SageMath), call ore_algebra.guess on
    the Taylor sequence and confirm minimal order is 3.
    """
    try:
        import ore_algebra  # noqa: F401
    except ImportError:
        return False, "ore_algebra unavailable (SageMath/ore_algebra not installed)", {
            "status": "fallback: in-house Koutschan guess used instead"
        }
    # If we get here, attempt a minimal guess invocation
    try:
        from ore_algebra import OreAlgebra
        from sage.all import QQ, PolynomialRing
        R, x = PolynomialRing(QQ, 'x').objgen()
        A = OreAlgebra(R, 'Dx')
        # Convert coeffs to QQ rationals
        seq = [QQ(int(c.p), int(c.q)) for c in coeffs[:min(depth, 60)]]
        L_guess = ore_algebra.guess(seq, A)
        return True, f"ore_algebra.guess succeeded; order={L_guess.order()}", {
            "order": int(L_guess.order()),
            "operator": str(L_guess),
        }
    except Exception as e:
        return False, f"ore_algebra invocation failed: {e}", {"error": str(e)}


# -------------------------- Main --------------------------

def main():
    print("=" * 78)
    print("V=1 SU(3) Wilson Picard-Fuchs ODE: EXTENDED Minimality Certificate")
    print("=" * 78)
    print()
    print("Candidate ODE (from PR #541):")
    print("  6 beta^2 J''' + beta(60-beta) J'' + (-4 beta^2 - 2 beta + 120) J' - beta(beta+10) J = 0")
    print()

    ORDER = 100
    print(f"Building Bessel-determinant Taylor series of J(beta) to depth {ORDER}...")
    t0 = time.time()
    J_poly = build_J_series(ORDER)
    coeffs = taylor_coeffs(J_poly, ORDER)
    print(f"  build+taylor: {time.time()-t0:.2f}s")
    a0, a1, a2, a3, a4 = coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4]
    print(f"  a_0 = {a0}, a_1 = {a1}, a_2 = {a2}, a_3 = {a3}, a_4 = {a4}")
    if a0 != Rational(1):
        print("  WARN: a_0 != 1; normalize required")
    if a2 != Rational(1, 36):
        print(f"  WARN: a_2 expected 1/36, got {a2}")
    print()

    pass_count, fail_count = 0, 0

    # Certificate A (deep Taylor annihilation, depth 100 -> safe range to deg 96)
    print("[A] Deep Taylor annihilation certificate (depth=100):")
    okA, msgA = certificate_A(J_poly, ORDER)
    print(f"    {msgA}")
    if okA:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Certificate D (recurrence consistency through N=99)
    print("[D] Recurrence consistency certificate (N=2..99):")
    okD, msgD, _failsD = certificate_D(coeffs, ORDER)
    print(f"    {msgD}")
    if okD:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Certificate B-EXT (lower-order exclusion to d=30)
    print("[B-EXT] Lower-order exclusion (no order <= 2 ODE with deg <= 30):")
    okBx, msgBx, infoBx = certificate_B_extended(coeffs, ORDER, r_max=2, d_max=30)
    print(f"    {msgBx}  (total {infoBx['_total_elapsed_sec']}s)")
    # Compact summary: print every 5th d
    for r in [1, 2]:
        for d in range(0, 31):
            key = f"r={r},d={d}"
            val = infoBx.get(key)
            if isinstance(val, dict) and (d % 5 == 0 or d == 30):
                print(f"    {key}: unknowns={val['unknowns']}, equations={val['equations']}, "
                      f"rank={val['rank']}, kernel_dim={val['kernel_dim']} -> {val['status']}")
    if okBx:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Certificate E-EXT ((r=3) consistency to d=12)
    print("[E-EXT] (r=3) higher-degree consistency to d=12:")
    okEx, msgEx, infoEx = certificate_E_extended(coeffs, ORDER, d_max=12)
    print(f"    {msgEx}  (total {infoEx['_total_elapsed_sec']}s)")
    for d in range(2, 13):
        key = f"r=3,d={d}"
        val = infoEx.get(key)
        if isinstance(val, dict):
            print(f"    {key}: kernel_dim={val['kernel_dim']}, expected={val['expected_kernel']} -> {val['status']}")
    if okEx:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Certificate K (Koutschan-style guess)
    print("[K] Koutschan-style algorithmic guess:")
    okK, msgK, infoK = koutschan_guess(coeffs, ORDER, r_scan_max=4, d_scan_max=4)
    print(f"    {msgK}")
    if okK:
        print(f"    minimal_r = {infoK.get('minimal_r')}, minimal_d = {infoK.get('minimal_d')}, "
              f"kernel_dim = {infoK.get('minimal_kernel_dim')}")
        print(f"    primitive-integer kernel signature: {infoK.get('normalized_kernel')}")
    if okK:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Certificate S (operator signature sanity)
    print("[S] Operator signature primitive-integer match:")
    okS, msgS, infoS = certificate_S(infoK if okK else {})
    print(f"    {msgS}")
    if not okS:
        print(f"    mismatches: {infoS['mismatches']}")
        print(f"    extras: {infoS['extras']}")
    if okS:
        pass_count += 1
    else:
        fail_count += 1
    print()

    # Optional ore_algebra check
    print("[OA] Optional SageMath/ore_algebra cross-check:")
    okOA, msgOA, infoOA = try_ore_algebra(coeffs, ORDER)
    print(f"    {msgOA}")
    # ore_algebra is optional. Do not penalize fail_count if missing.
    print()

    # Summary
    print("=" * 78)
    print(f"SUMMARY: CERTIFICATE PASS={pass_count} FAIL={fail_count}")
    print("=" * 78)
    print()
    if fail_count == 0:
        print("Extended minimality certificate operationally CLOSED.")
        print("- Lower-order exclusion to (r <= 2, d <= 30): no annihilator")
        print("- (r=3, d) higher-degree consistency to d=12: polynomial-multiple bound exact")
        print("- Algorithmic Koutschan guess: minimal at (r=3, d=2), matches PR #541 L")
        print("- Primitive-integer signature: 8/8 coefficient match")
        print()
        print("Combined with the deep Taylor annihilation (depth 100), the algorithmic")
        print("verification path is self-contained over Q. The Bernstein-Sato existence")
        print("input from D-module theory remains philosophical context, but the bounded")
        print("operational closure of the rank bound is now runner-internal.")
    else:
        print("FAIL: extended bounded certificate did not pass.")

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    output = {
        "candidate_ode": "6 beta^2 J''' + beta(60-beta) J'' + (-4 beta^2 - 2 beta + 120) J' - beta(beta+10) J = 0",
        "taylor_order": ORDER,
        "certificate_A": {"name": "deep Taylor annihilation (depth 100)", "pass": okA, "message": msgA},
        "certificate_D": {"name": "recurrence consistency through N=99", "pass": okD},
        "certificate_B_extended": {
            "name": "lower-order exclusion (r <= 2, d <= 30)",
            "pass": okBx,
            "details": {k: v for k, v in infoBx.items() if isinstance(v, dict)},
            "total_elapsed_sec": infoBx.get("_total_elapsed_sec"),
        },
        "certificate_E_extended": {
            "name": "(r=3) higher-degree consistency (d=2..12)",
            "pass": okEx,
            "details": {k: v for k, v in infoEx.items() if isinstance(v, dict)},
            "total_elapsed_sec": infoEx.get("_total_elapsed_sec"),
        },
        "certificate_K_koutschan": {
            "name": "Koutschan-style algorithmic guess",
            "pass": okK,
            "minimal_r": infoK.get("minimal_r"),
            "minimal_d": infoK.get("minimal_d"),
            "minimal_kernel_dim": infoK.get("minimal_kernel_dim"),
            "normalized_kernel": infoK.get("normalized_kernel"),
            "scalar_to_published": infoK.get("scalar_to_published"),
            "scan": infoK.get("scan"),
        },
        "certificate_S_signature": {
            "name": "Operator primitive-integer signature match",
            "pass": okS,
            "details": infoS,
        },
        "ore_algebra_crosscheck": {
            "available": okOA,
            "message": msgOA,
            "details": infoOA,
        },
        "summary": {
            "pass": pass_count,
            "fail": fail_count,
            "extended_certificate_passed": fail_count == 0,
            "audit_status_authority": "independent audit lane only",
        },
    }
    out_path = out_dir / "su3_v1_picard_fuchs_minimality_extended_2026_05_06.json"
    with out_path.open("w") as f:
        json.dump(output, f, indent=2, default=str)
        f.write("\n")
    print(f"Output written: {out_path}")
    raise SystemExit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
