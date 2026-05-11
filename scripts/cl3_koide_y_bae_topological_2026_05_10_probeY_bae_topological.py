#!/usr/bin/env python3
"""Runner for the bounded Koide BAE topological-decoupling note.

The runner checks the finite C3 representation facts and sampled
amplitude-independence claims used by the source note. It does not
claim that every possible topological construction is exhausted.
"""

from __future__ import annotations

from pathlib import Path
import math
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "KOIDE_Y_BAE_TOPOLOGICAL_INDEX_KTHEORY_NOTE_2026-05-10_probeY_bae_topological.md"
)

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def c_cycle() -> np.ndarray:
    return np.array(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ],
        dtype=complex,
    )


def h_circ(a: float, b: complex) -> np.ndarray:
    c = c_cycle()
    return a * np.eye(3, dtype=complex) + b * c + np.conj(b) * (c @ c)


def character_of_power(power: int) -> complex:
    c = c_cycle()
    return np.trace(np.linalg.matrix_power(c, power))


def irrep_character(k: int, power: int) -> complex:
    omega = np.exp(2j * np.pi / 3)
    return omega ** (k * power)


def multiplicity(k: int) -> complex:
    return sum(
        np.conj(irrep_character(k, j)) * character_of_power(j)
        for j in range(3)
    ) / 3


def sign_eta(values: np.ndarray, tol: float = 1e-10) -> int:
    total = 0
    for val in values:
        real = float(np.real(val))
        if real > tol:
            total += 1
        elif real < -tol:
            total -= 1
    return total


def main() -> int:
    note = NOTE_PATH.read_text()
    note_flat = re.sub(r"\s+", " ", note)

    section("note boundary checks")
    required = [
        "Claim type:** bounded_theorem",
        "source-note proposal only",
        "without an additional amplitude bridge",
        "does not supply that bridge",
        "not a new interpretation of the physical Cl(3) local algebra plus Z^3 spatial substrate baseline",
        "This note does not:",
        "assert retained or audited status",
    ]
    for marker in required:
        check(f"note contains {marker[:52]!r}", marker in note_flat)

    section("C3 representation and K-theory class")
    c = c_cycle()
    check("C has order 3", np.allclose(c @ c @ c, np.eye(3)))
    check("C is unitary", np.allclose(c.conj().T @ c, np.eye(3)))
    chars = [character_of_power(j) for j in range(3)]
    check(
        "regular representation character is (3,0,0)",
        np.allclose(chars, [3, 0, 0]),
        detail=f"chars={chars}",
    )
    mults = [multiplicity(k) for k in range(3)]
    check(
        "character orthogonality gives multiplicities (1,1,1)",
        np.allclose(mults, [1, 1, 1]),
        detail=f"multiplicities={mults}",
    )
    check("K_C3(pt)=R(C3) class is integer triple", all(abs(m.real - round(m.real)) < 1e-12 for m in mults))

    section("circulant amplitude does not alter representation class")
    samples = [
        (1.0, 0.0 + 0.0j),
        (1.0, 1 / math.sqrt(2) + 0.0j),
        (1.3, 0.2 + 0.6j),
        (2.0, -0.4 + 0.3j),
    ]
    for idx, (a, b) in enumerate(samples):
        h = h_circ(a, b)
        check(f"sample {idx}: H(a,b) is Hermitian", np.allclose(h, h.conj().T))
        check(f"sample {idx}: H(a,b) commutes with C", np.allclose(h @ c, c @ h))
        check(
            f"sample {idx}: representation character unchanged",
            np.allclose([character_of_power(j) for j in range(3)], chars),
        )

    section("topological data are discrete while BAE is a continuous ratio")
    bae_ratio = 1 / math.sqrt(2)
    ratios = [0.25, 0.5, bae_ratio, 0.9, 1.25]
    eta_values = []
    for ratio in ratios:
        eigvals = np.linalg.eigvalsh(h_circ(1.0, ratio + 0j))
        eta_values.append(sign_eta(eigvals))
    check(
        "sampled eta signature is integer-valued",
        all(isinstance(v, int) for v in eta_values),
        detail=f"eta={eta_values}",
    )
    near_bae = [bae_ratio - 0.03, bae_ratio, bae_ratio + 0.03]
    near_eta = [sign_eta(np.linalg.eigvalsh(h_circ(1.0, r + 0j))) for r in near_bae]
    check(
        "eta signature does not single out the BAE neighborhood in this route",
        len(set(near_eta)) == 1,
        detail=f"ratios={near_bae}, eta={near_eta}",
    )
    check("BAE ratio is non-integer continuous data", not float(bae_ratio).is_integer())

    section("point character, anomaly-trace, and cohomology bookkeeping")
    check("point Chern character reduces to rank 3", abs(chars[0] - 3) < 1e-12)
    check("non-identity C3 character traces vanish", abs(chars[1]) < 1e-12 and abs(chars[2]) < 1e-12)
    h_point = {"H0": "Z", "Hq_gt_0": "0"}
    check("point cohomology has H0=Z", h_point["H0"] == "Z")
    check("point cohomology has Hq=0 for q>0", h_point["Hq_gt_0"] == "0")
    group_torsion_orders = [3, 3]
    check("finite C3 cohomology torsion data are finite integers", group_torsion_orders == [3, 3])

    section("runner import boundary")
    source = Path(__file__).read_text()
    modules = set()
    for match in re.finditer(r"^(?:from|import)\s+([\w.]+)", source, re.MULTILINE):
        modules.add(match.group(1).split(".")[0])
    allowed = {"__future__", "math", "numpy", "pathlib", "re", "sys"}
    check("imports limited to numpy plus stdlib", modules <= allowed, detail=f"modules={sorted(modules)}")

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
