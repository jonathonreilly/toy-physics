#!/usr/bin/env python3
"""
PR #230 color-singlet gauge-zero-mode cancellation theorem.

The previous zero-mode blocks left the massless q=0 gauge mode as a
load-bearing scalar-denominator prescription.  This runner checks the
color-singlet part from first principles: a spatially constant gauge mode
couples to total color charge.  In a q qbar color singlet, the total color
charge annihilates the state, so the zero-mode contribution cancels only after
including quark, antiquark, and exchange pieces together.

This is exact support for removing the q=0 gauge mode in the color-singlet
scalar channel.  It is not retained y_t closure: finite-q IR behavior, the
interacting scalar denominator, the pole derivative, and production evidence
remain open.
"""

from __future__ import annotations

import json
import math

import numpy as np

from frontier_yt_flat_toron_thermodynamic_washout import (
    OUTPUT as FLAT_TORON_WASHOUT,
    ROOT,
)


OUTPUT = ROOT / "outputs" / "yt_color_singlet_zero_mode_cancellation_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def gell_mann_generators() -> list[np.ndarray]:
    zero = 0.0 + 0.0j
    one = 1.0 + 0.0j
    i = 0.0 + 1.0j
    lambdas = [
        np.asarray([[zero, one, zero], [one, zero, zero], [zero, zero, zero]], dtype=complex),
        np.asarray([[zero, -i, zero], [i, zero, zero], [zero, zero, zero]], dtype=complex),
        np.asarray([[one, zero, zero], [zero, -one, zero], [zero, zero, zero]], dtype=complex),
        np.asarray([[zero, zero, one], [zero, zero, zero], [one, zero, zero]], dtype=complex),
        np.asarray([[zero, zero, -i], [zero, zero, zero], [i, zero, zero]], dtype=complex),
        np.asarray([[zero, zero, zero], [zero, zero, one], [zero, one, zero]], dtype=complex),
        np.asarray([[zero, zero, zero], [zero, zero, -i], [zero, i, zero]], dtype=complex),
        (1.0 / math.sqrt(3.0)) * np.asarray([[one, zero, zero], [zero, one, zero], [zero, zero, -2.0 * one]], dtype=complex),
    ]
    return [lam / 2.0 for lam in lambdas]


def singlet_state(nc: int = 3) -> np.ndarray:
    state = np.zeros((nc, nc), dtype=complex)
    for color in range(nc):
        state[color, color] = 1.0 / math.sqrt(nc)
    return state.reshape(nc * nc)


def octet_state(generator: np.ndarray) -> np.ndarray:
    # Normalization: Tr(T^a T^a)=1/2, so sqrt(2) T^a is unit in q qbar space.
    return (math.sqrt(2.0) * generator).reshape(9)


def kron_quark(generator: np.ndarray) -> np.ndarray:
    return np.kron(generator, np.eye(3, dtype=complex))


def kron_antiquark(generator: np.ndarray) -> np.ndarray:
    return np.kron(np.eye(3, dtype=complex), -generator.conjugate())


def expectation(state: np.ndarray, operator: np.ndarray) -> float:
    return float(np.vdot(state, operator @ state).real)


def main() -> int:
    print("PR #230 color-singlet gauge-zero-mode cancellation")
    print("=" * 72)

    parent = json.loads(FLAT_TORON_WASHOUT.read_text(encoding="utf-8"))
    generators = gell_mann_generators()
    state_s = singlet_state()
    identity = np.eye(9, dtype=complex)
    cf = 4.0 / 3.0
    ca = 3.0

    generator_norm_errors = [abs(float(np.trace(t @ t).real) - 0.5) for t in generators]
    singlet_charge_norms = []
    singlet_self = 0.0
    singlet_anti_self = 0.0
    singlet_exchange = 0.0
    for t in generators:
        q = kron_quark(t)
        qb = kron_antiquark(t)
        total = q + qb
        singlet_charge_norms.append(float(np.linalg.norm(total @ state_s)))
        singlet_self += expectation(state_s, q @ q)
        singlet_anti_self += expectation(state_s, qb @ qb)
        singlet_exchange += expectation(state_s, q @ qb)

    singlet_total_charge_sq = singlet_self + singlet_anti_self + 2.0 * singlet_exchange

    octet = octet_state(generators[0])
    octet_total_charge_sq = 0.0
    for t in generators:
        total = kron_quark(t) + kron_antiquark(t)
        octet_total_charge_sq += expectation(octet, total @ total)

    naive_exchange_only_zero_mode = singlet_exchange
    full_color_neutral_zero_mode = singlet_total_charge_sq
    cancellation_terms = {
        "quark_self": singlet_self,
        "antiquark_self": singlet_anti_self,
        "twice_exchange": 2.0 * singlet_exchange,
        "sum": singlet_total_charge_sq,
    }

    report(
        "parent-flat-toron-washout-loaded",
        parent.get("proposal_allowed") is False and "flat toron thermodynamic washout" in str(parent.get("actual_current_surface_status", "")),
        str(FLAT_TORON_WASHOUT.relative_to(ROOT)),
    )
    report(
        "su3-generator-normalization",
        max(generator_norm_errors) < 1.0e-12,
        f"max Tr(TaTa)-1/2 error={max(generator_norm_errors):.3e}",
    )
    report(
        "singlet-total-color-charge-vanishes",
        max(singlet_charge_norms) < 1.0e-12,
        f"max ||Qa|S>||={max(singlet_charge_norms):.3e}",
    )
    report(
        "self-and-exchange-pieces-cancel",
        abs(singlet_self - cf) < 1.0e-12
        and abs(singlet_anti_self - cf) < 1.0e-12
        and abs(singlet_exchange + cf) < 1.0e-12
        and abs(singlet_total_charge_sq) < 1.0e-12,
        str(cancellation_terms),
    )
    report(
        "octet-zero-mode-does-not-cancel",
        abs(octet_total_charge_sq - ca) < 1.0e-12,
        f"octet_total_charge_sq={octet_total_charge_sq:.12g}",
    )
    report(
        "exchange-only-zero-mode-is-spurious-for-singlet",
        abs(naive_exchange_only_zero_mode + cf) < 1.0e-12
        and abs(full_color_neutral_zero_mode) < 1.0e-12,
        f"exchange_only={naive_exchange_only_zero_mode:.12g}, full={full_color_neutral_zero_mode:.12g}",
    )
    report(
        "not-retained-closure",
        True,
        "zero-mode cancellation is exact support, but finite-q IR and scalar pole derivative remain open",
    )

    result = {
        "actual_current_surface_status": "exact-support / color-singlet gauge-zero-mode cancellation",
        "verdict": (
            "A spatially constant gauge mode couples to total color charge.  "
            "For the q qbar color singlet, (T_q^a + T_qbar^a)|S>=0 for every "
            "SU(3) generator.  The quark self, antiquark self, and exchange "
            "zero-mode pieces cancel: C_F + C_F - 2 C_F = 0.  Therefore an "
            "exchange-only finite ladder that keeps the q=0 gauge mode is not "
            "a color-neutral scalar denominator.  The q=0 mode is removed by "
            "singlet color neutrality, but PR #230 still needs finite-q IR "
            "control, the interacting scalar pole derivative, and production "
            "evidence before retained y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Color-singlet zero-mode cancellation removes one IR obstruction but does not derive the scalar pole derivative or production evidence.",
        "parent_certificate": str(FLAT_TORON_WASHOUT.relative_to(ROOT)),
        "cancellation_terms": cancellation_terms,
        "witnesses": {
            "C_F": cf,
            "C_A": ca,
            "max_singlet_charge_norm": max(singlet_charge_norms),
            "naive_exchange_only_zero_mode": naive_exchange_only_zero_mode,
            "full_color_neutral_zero_mode": full_color_neutral_zero_mode,
            "octet_total_charge_sq": octet_total_charge_sq,
        },
        "remaining_blockers": [
            "derive finite-q IR and finite-volume behavior of the zero-mode-removed scalar kernel",
            "derive or measure the scalar pole and inverse-propagator derivative",
            "derive projector/source normalization and finite-Nc continuum control",
            "run production FH/LSZ evidence with the color-singlet prescription fixed",
        ],
        "strict_non_claims": [
            "not retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not use H_unit matrix elements or yt_ward_identity as authority",
            "does not use observed top mass or observed y_t as selectors",
            "does not use alpha_LM, plaquette, u0, or reduced pilots as proof inputs",
            "does not set c2 = 1 or Z_match = 1",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
