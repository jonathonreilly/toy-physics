#!/usr/bin/env python3
"""Audit the operational no-past-signaling support theorem.

The theorem is not a chronology-lane closure.  It checks the exact statement
used by the note: on a single-clock ordered circuit, later nonselective CPTP
operations preserve the trace of every earlier record branch, so the earlier
record marginal cannot depend on the later setting.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md"

AUTHORITY_FILES = [
    ROOT / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ROOT / "docs" / "SINGLE_AXIOM_HILBERT_NOTE.md",
    ROOT / "docs" / "SINGLE_AXIOM_INFORMATION_NOTE.md",
    ROOT / "docs" / "LIGHT_CONE_FRAMING_NOTE.md",
    ROOT / "docs" / "CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md",
    ROOT / "docs" / "CPT_EXACT_NOTE.md",
    ROOT / "docs" / "FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md",
]

EPS = 1e-12


passes = 0
fails = 0


def check(name: str, condition: bool) -> None:
    global passes, fails
    if condition:
        passes += 1
        print(f"  [PASS] {name}")
    else:
        fails += 1
        print(f"  [FAIL] {name}")


def section(title: str) -> None:
    print("\n" + "-" * 88)
    print(title)
    print("-" * 88)


def dagger(x: np.ndarray) -> np.ndarray:
    return x.conj().T


def trace(x: np.ndarray) -> complex:
    return complex(np.trace(x))


def close(a: complex, b: complex, eps: float = EPS) -> bool:
    return abs(a - b) <= eps


def kraus_channel(kraus: list[np.ndarray]) -> Callable[[np.ndarray], np.ndarray]:
    return lambda x: sum(k @ x @ dagger(k) for k in kraus)


def is_trace_preserving(kraus: list[np.ndarray]) -> bool:
    dim = kraus[0].shape[1]
    total = sum(dagger(k) @ k for k in kraus)
    return bool(np.allclose(total, np.eye(dim), atol=EPS))


def is_unital_dual(kraus: list[np.ndarray]) -> bool:
    dim = kraus[0].shape[1]
    identity = np.eye(dim, dtype=complex)
    dual_identity = sum(dagger(k) @ identity @ k for k in kraus)
    return bool(np.allclose(dual_identity, identity, atol=EPS))


def density() -> np.ndarray:
    rho = np.array([[0.7, 0.2], [0.2, 0.3]], dtype=complex)
    check("rho is normalized", close(trace(rho), 1.0))
    check("rho is positive semidefinite", np.linalg.eigvalsh(rho).min() >= -EPS)
    return rho


def main() -> int:
    print("=" * 88)
    print("Operational chronology-protection no-past-signaling audit")
    print(f"See {NOTE.relative_to(ROOT)}")
    print("=" * 88)

    section("Authority and scope surface")
    note_text = NOTE.read_text()
    for path in AUTHORITY_FILES:
        check(f"authority/reference exists: {path.relative_to(ROOT)}", path.exists())

    required_boundaries = [
        "does not close it",
        "does not close the lane",
        "postselection",
        "final-boundary",
        "causal cycle",
        "no manuscript promotion or lane closure",
        "no derivation of the retained single-clock surface itself",
    ]
    for phrase in required_boundaries:
        check(f"note states boundary: {phrase}", phrase in note_text)

    forbidden_promotions = [
        "closes the chronology-protection lane",
        "closed chronology-protection lane",
        "therefore time travel is impossible",
        "rules out all possible CTC",
    ]
    for phrase in forbidden_promotions:
        check(f"note avoids overclaim: {phrase}", phrase not in note_text)

    section("Record instrument at t0")
    rho0 = density()
    p0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    p1 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    record_kraus = [p0, p1]
    check("record instrument nonselective sum is trace preserving", is_trace_preserving(record_kraus))

    branches = [p @ rho0 @ p for p in record_kraus]
    base_probs = [trace(branch).real for branch in branches]
    print(f"  P(a at t0) = {base_probs}")
    check("record probabilities sum to one", abs(sum(base_probs) - 1.0) <= EPS)
    check("record branch 0 probability is nonzero", base_probs[0] > 0)
    check("record branch 1 probability is nonzero", base_probs[1] > 0)

    section("Single-clock unitary propagation t0 -> t1")
    theta = 0.37
    u10 = np.array(
        [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]],
        dtype=complex,
    )
    check("U10 is unitary", np.allclose(dagger(u10) @ u10, np.eye(2), atol=EPS))
    sigma = [u10 @ branch @ dagger(u10) for branch in branches]
    for idx, branch in enumerate(branches):
        check(f"unitary preserves trace of record branch {idx}", close(trace(sigma[idx]), trace(branch)))

    section("Later nonselective settings at t1 cannot alter earlier marginal")
    z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    h = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
    reset0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    reset1 = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    settings: dict[str, list[np.ndarray]] = {
        "identity": [np.eye(2, dtype=complex)],
        "future_unitary_H": [h],
        "future_dephasing": [np.sqrt(0.25) * np.eye(2), np.sqrt(0.75) * z],
        "future_reset_memory": [reset0, reset1],
    }

    for name, kraus in settings.items():
        channel = kraus_channel(kraus)
        check(f"{name} is trace preserving", is_trace_preserving(kraus))
        check(f"{name} has unital Heisenberg dual", is_unital_dual(kraus))
        px = [trace(channel(branch)).real for branch in sigma]
        print(f"  {name}: P_x(a) = {px}")
        for idx, value in enumerate(px):
            check(f"{name} preserves earlier branch probability a={idx}", abs(value - base_probs[idx]) <= EPS)

    section("Later measurement: unconditioned no signal, postselected conditioning can bias")
    outcome_kraus = [p0, p1]
    check("future outcome family is trace preserving when summed", is_trace_preserving(outcome_kraus))
    future_outcomes = [kraus_channel([k]) for k in outcome_kraus]
    unconditioned = [
        sum(trace(outcome(sigma[idx])).real for outcome in future_outcomes)
        for idx in range(2)
    ]
    for idx, value in enumerate(unconditioned):
        check(f"summed future outcomes preserve P(a={idx})", abs(value - base_probs[idx]) <= EPS)

    prob_b0 = sum(trace(future_outcomes[0](s)).real for s in sigma)
    conditional_a0_given_b0 = trace(future_outcomes[0](sigma[0])).real / prob_b0
    print(f"  P(a=0) = {base_probs[0]:.12f}")
    print(f"  P(a=0 | future b=0) = {conditional_a0_given_b0:.12f}")
    check("future postselection changes the retrodicted ensemble", abs(conditional_a0_given_b0 - base_probs[0]) > 1e-3)
    check("postselection branch has nonzero probability cost", prob_b0 > 0)

    section("Loschmidt echo is a future state, not past-record alteration")
    echo = dagger(u10) @ sigma[0] @ u10
    check("inverse unitary can reconstruct branch state as a later echo", np.allclose(echo, branches[0], atol=EPS))
    check("echo trace equals original branch probability", close(trace(echo), trace(branches[0])))
    check("echo does not change already computed P(a=0)", abs(trace(echo).real - base_probs[0]) <= EPS)

    section("Summary")
    print("  Certified:")
    print("    ordered single-clock circuit + CPTP later settings imply no change")
    print("    in the unconditioned earlier record marginal P(a).")
    print()
    print("  Not certified:")
    print("    final-boundary theories, postselected subensembles, directed causal")
    print("    cycles, interacting CPT, or a full chronology-protection lane closure.")

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={passes}, FAIL={fails}")
    print("=" * 88)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
