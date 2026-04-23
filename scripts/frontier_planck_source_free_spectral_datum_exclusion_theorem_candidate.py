#!/usr/bin/env python3
"""Audit runner for the source-free spectral-datum exclusion candidate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def pa_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


def packet_light_state() -> np.ndarray:
    p_a = pa_projector()
    ident = np.eye(16)
    return (1.0 / 32.0) * p_a + (7.0 / 96.0) * (ident - p_a)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []
    ident = np.eye(16)
    rho_tr = ident / 16.0
    rho_lt = packet_light_state()
    p_a = pa_projector()

    # Test 1: tracial state has a single eigenvalue.
    evals_tr = np.linalg.eigvalsh(rho_tr)
    checks.append(Check("tracial-single-eigenvalue", np.allclose(evals_tr, evals_tr[0]), f"eval={evals_tr[0]:.6f}"))

    # Test 2: packet-light witness is nontracial.
    evals_lt = np.linalg.eigvalsh(rho_lt)
    distinct_lt = len(np.unique(np.round(evals_lt, 12)))
    checks.append(Check("packet-light-nontracial", distinct_lt > 1, f"distinct={distinct_lt}"))

    # Test 3: max-eigenspace projector is canonically retrievable and proper.
    lam_max = float(evals_lt.max())
    q_max = np.isclose(rho_lt, lam_max).astype(float)
    # q_max built diagonally because rho_lt is diagonal in this witness basis.
    rank_q_max = int(round(np.trace(q_max)))
    checks.append(Check("proper-max-projector", 0 < rank_q_max < 16, f"rank={rank_q_max}"))

    # Test 4: q_max is not scalar.
    checks.append(Check("projector-not-scalar", not np.allclose(q_max, np.eye(16)), "proper projector differs from identity"))

    # Test 5: nontracial witness therefore carries proper spectral datum.
    checks.append(Check("nontracial-carries-datum", rank_q_max in (12, 4), f"rank={rank_q_max}"))

    # Test 6: tracial state has no proper spectral split.
    checks.append(Check("tracial-no-proper-spectral-split", distinct_lt > 1 and len(np.unique(np.round(evals_tr, 12))) == 1, "only one spectral block"))

    # Test 7: direct counting law on tracial state yields quarter.
    coeff_tr = float(np.trace(rho_tr @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff_tr, 0.25), f"coeff={coeff_tr:.6f}"))

    # Test 8: nontracial witness gives a different coefficient.
    coeff_lt = float(np.trace(rho_lt @ p_a))
    checks.append(Check("witness-different-coefficient", not math.isclose(coeff_lt, coeff_tr), f"coeff_lt={coeff_lt:.6f}"))

    # Test 9: normalized positivity of both states.
    ok_norm = math.isclose(np.trace(rho_tr), 1.0) and math.isclose(np.trace(rho_lt), 1.0)
    ok_pos = np.all(np.linalg.eigvalsh(rho_tr) >= -1e-12) and np.all(np.linalg.eigvalsh(rho_lt) >= -1e-12)
    checks.append(Check("state-validity", ok_norm and ok_pos, "both states positive and normalized"))

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
