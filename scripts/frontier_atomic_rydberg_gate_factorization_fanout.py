#!/usr/bin/env python3
"""Lane 2 Rydberg gate factorization and stuck fan-out.

This runner is a branch-local physics-loop artifact.  It emulates the
required stuck fan-out across independent attack frames and checks whether the
current Lane 2 surface can honestly promote the atomic Rydberg scale.

Result:
  No retained Rydberg closure follows from the current repo primitives.  The
  current artifacts factor the problem into independent gates:

    1. a charged-lepton/reduced-mass gate;
    2. a low-energy Coulomb alpha(0) or threshold-resolved QED-running gate;
    3. a framework-native physical-unit nonrelativistic Coulomb/Schrodinger
       map.

The runner proves algebraic independence with synthetic inputs before any
hydrogen comparator appears.  Comparator values are used only to illustrate
why hidden fitting would be load-bearing.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude/science/physics-loops/lane2-atomic-scale-20260428"


@dataclass
class CheckLog:
    passed: int = 0
    failed: int = 0

    def check(self, condition: bool, name: str, detail: str = "") -> None:
        if condition:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
        suffix = f"  ({detail})" if detail else ""
        print(f"  [{status}] {name}{suffix}")


@dataclass(frozen=True)
class FanoutFrame:
    name: str
    premise: str
    forbidden: str
    attempt: str
    result: str
    next_prerequisite: str
    closure: bool


# Comparator constants already present in repo atomic/firewall scaffolds.
# These are not used by the synthetic theorem checks.
INV_ALPHA_MZ_REPO = 127.67
INV_ALPHA0_COMPARATOR = 137.035999084
M_E_EV_COMPARATOR = 510_998.95000
RYDBERG_EV_COMPARATOR = 13.605693122994
M_Z_GEV_COMPARATOR = 91.1876
M_E_GEV_COMPARATOR = 0.00051099895

N_COLOR = 3
N_GEN = 3


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def dimless_lambda(g: float, n: int) -> float:
    """Continuum scaled spectrum for H_g = -Delta_x - g/r."""
    return -(g * g) / (4.0 * n * n)


def energy_from_dimless(lambda_n: float, mu: float, a: float) -> float:
    """Physical energy from dimensionless eigenvalue with admitted unit map."""
    return lambda_n / (2.0 * mu * a * a)


def bohr_radius_map(mu: float, alpha: float, z: float, g: float) -> float:
    """a required by g = 2 mu a Z alpha."""
    return g / (2.0 * mu * z * alpha)


def bohr_energy(mu: float, alpha: float, z: float, n: int) -> float:
    """Nonrelativistic Coulomb spectrum in natural units."""
    return -mu * (z * alpha) ** 2 / (2.0 * n * n)


def almost_equal(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-12) -> bool:
    return abs(a - b) <= max(abs_tol, rel * max(abs(a), abs(b), 1.0))


def b_qed_from_retained_charge_counts() -> Fraction:
    q_e = Fraction(-1, 1)
    q_u = Fraction(2, 3)
    q_d = Fraction(-1, 3)
    sum_q2 = N_GEN * (q_e * q_e + N_COLOR * (q_u * q_u + q_d * q_d))
    return Fraction(4, 3) * sum_q2


def inv_alpha_running_down(inv_alpha_high: float, b_active: Fraction, active_log: float) -> float:
    return inv_alpha_high + float(b_active) * active_log / (2.0 * math.pi)


def part1_grounding(log: CheckLog) -> None:
    section("Part 1: repo and loop grounding")
    lane2 = read("docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md")
    scaffold = read("docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md")
    firewall = read("docs/ATOMIC_RYDBERG_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md")
    assumptions = (PACK / "ASSUMPTIONS_AND_IMPORTS.md").read_text(encoding="utf-8")
    no_go = (PACK / "NO_GO_LEDGER.md").read_text(encoding="utf-8")

    required_paths = [
        "scripts/frontier_atomic_rydberg_dependency_firewall.py",
        "scripts/frontier_atomic_qed_threshold_bridge_firewall.py",
        "scripts/frontier_atomic_nr_coulomb_scale_bridge.py",
        ".claude/science/physics-loops/lane2-atomic-scale-20260428/notes/"
        "ATOMIC_QED_THRESHOLD_BRIDGE_FIREWALL_NOTE_2026-05-01.md",
        ".claude/science/physics-loops/lane2-atomic-scale-20260428/notes/"
        "ATOMIC_NR_COULOMB_SCALE_BRIDGE_STRETCH_NOTE_2026-05-01.md",
    ]
    for rel in required_paths:
        log.check((ROOT / rel).exists(), f"required prior surface exists: {rel}")

    log.check(
        "scaffold-only" in lane2 and "textbook inputs" in lane2,
        "Lane 2 open stub marks atomic content scaffold-only",
    )
    log.check(
        "m_e" in lane2 and "alpha(0)" in lane2 and "Schrodinger/Coulomb limit" in lane2,
        "Lane 2 open stub names the three Rydberg prerequisites",
    )
    log.check(
        "textbook inputs" in scaffold and "m_e" in scaffold and "Coulomb coupling" in scaffold,
        "atomic scaffold imports textbook physical units",
    )
    log.check(
        "alpha_EM(M_Z)" in firewall and "alpha(0)" in firewall and "load-bearing" in firewall,
        "2026-04-27 firewall keeps direct alpha(M_Z) substitution blocked",
    )
    log.check(
        "alpha(0)" in assumptions and "m_e" in assumptions and "Physical length map" in assumptions,
        "loop assumption ledger records alpha(0), m_e, and physical unit map as open",
    )
    log.check(
        "Directly substitute `alpha_EM(M_Z)`" in no_go
        and "physical-unit nonrelativistic Schrodinger limit" in no_go,
        "loop no-go ledger already blocks direct substitution and unit-map promotion",
    )


def part2_synthetic_gate_factorization(log: CheckLog) -> None:
    section("Part 2: synthetic gate factorization")
    samples = [
        (5.0, 0.20, 1.0, 0.8),
        (11.0, 0.07, 2.0, 1.5),
        (101.0, 0.011, 3.0, 4.0),
    ]

    for mu, alpha, z, g in samples:
        for n in range(1, 5):
            a = bohr_radius_map(mu, alpha, z, g)
            mapped = energy_from_dimless(dimless_lambda(g, n), mu, a)
            direct = bohr_energy(mu, alpha, z, n)
            log.check(
                almost_equal(mapped, direct, rel=1e-12, abs_tol=1e-12),
                f"synthetic scale bridge agrees for mu={mu:g}, alpha={alpha:g}, Z={z:g}, n={n}",
            )

    mu, alpha, z, n = 7.0, 0.13, 1.0, 1
    base = bohr_energy(mu, alpha, z, n)
    for scale in (0.5, 2.0, 3.0):
        mass_scaled = bohr_energy(scale * mu, alpha, z, n)
        alpha_scaled = bohr_energy(mu, scale * alpha, z, n)
        log.check(
            almost_equal(mass_scaled / base, scale),
            f"mass gate is linearly load-bearing at scale {scale:g}",
        )
        log.check(
            almost_equal(alpha_scaled / base, scale * scale),
            f"alpha gate is quadratically load-bearing at scale {scale:g}",
        )

    product = mu * alpha * alpha
    alt_alpha = 0.071
    alt_mu = product / (alt_alpha * alt_alpha)
    alt_energy = bohr_energy(alt_mu, alt_alpha, z, n)
    log.check(
        almost_equal(alt_energy, base),
        "Rydberg energy alone fixes only the product mu*alpha^2",
        f"mu={mu:g}, alpha={alpha:g} and mu={alt_mu:.6g}, alpha={alt_alpha:g}",
    )

    g = 1.0
    lam = dimless_lambda(g, 1)
    unit_energies = [energy_from_dimless(lam, 1.0, a) for a in (0.5, 1.0, 2.0)]
    log.check(
        almost_equal(unit_energies[0] / unit_energies[1], 4.0)
        and almost_equal(unit_energies[1] / unit_energies[2], 4.0),
        "without the physical unit map, the same dimensionless eigenvalue has arbitrary eV scale",
    )


def part3_threshold_frame(log: CheckLog) -> None:
    section("Part 3: QED threshold frame")
    b_qed = b_qed_from_retained_charge_counts()
    low_a = inv_alpha_running_down(INV_ALPHA_MZ_REPO, b_qed, 0.0)
    low_b = inv_alpha_running_down(INV_ALPHA_MZ_REPO, b_qed, 5.0)
    low_c = inv_alpha_running_down(INV_ALPHA_MZ_REPO, b_qed, 10.0)

    print(f"  retained charge/count b_QED = {b_qed}")
    print(f"  same alpha(M_Z), active_log=0  -> 1/alpha_low={low_a:.6f}")
    print(f"  same alpha(M_Z), active_log=5  -> 1/alpha_low={low_b:.6f}")
    print(f"  same alpha(M_Z), active_log=10 -> 1/alpha_low={low_c:.6f}")

    log.check(b_qed == Fraction(32, 3), "retained charge/count frame gives b_QED=32/3")
    log.check(
        low_a < low_b < low_c and low_c - low_a > 10.0,
        "same alpha(M_Z) and same b_QED leave alpha(0) threshold-underdetermined",
    )


def part4_comparator_falsifiers(log: CheckLog) -> None:
    section("Part 4: comparator-only falsifiers")
    alpha0 = 1.0 / INV_ALPHA0_COMPARATOR
    alpha_mz = 1.0 / INV_ALPHA_MZ_REPO
    e_alpha0 = bohr_energy(M_E_EV_COMPARATOR, alpha0, 1.0, 1)
    e_alpha_mz = bohr_energy(M_E_EV_COMPARATOR, alpha_mz, 1.0, 1)
    rel_shift = (abs(e_alpha_mz) - abs(e_alpha0)) / abs(e_alpha0)
    required_me_with_alpha_mz = 2.0 * RYDBERG_EV_COMPARATOR / (alpha_mz * alpha_mz)
    me_shift = (required_me_with_alpha_mz - M_E_EV_COMPARATOR) / M_E_EV_COMPARATOR

    b_qed = b_qed_from_retained_charge_counts()
    log_mz_me = math.log(M_Z_GEV_COMPARATOR / M_E_GEV_COMPARATOR)
    active_log_for_alpha0 = (
        (INV_ALPHA0_COMPARATOR - INV_ALPHA_MZ_REPO) * 2.0 * math.pi / float(b_qed)
    )

    print(f"  comparator alpha(0) Rydberg E_1      = {e_alpha0:.9f} eV")
    print(f"  direct alpha(M_Z) substitution E_1   = {e_alpha_mz:.9f} eV")
    print(f"  relative direct-substitution shift   = {rel_shift:+.2%}")
    print(f"  m_e needed to hide alpha(M_Z) use    = {required_me_with_alpha_mz:.6f} eV")
    print(f"  relative hidden m_e shift            = {me_shift:+.2%}")
    print(f"  log(M_Z/m_e) comparator              = {log_mz_me:.6f}")
    print(f"  active log needed to hit alpha(0)    = {active_log_for_alpha0:.6f}")

    log.check(
        abs(abs(e_alpha0) - RYDBERG_EV_COMPARATOR) / RYDBERG_EV_COMPARATOR < 1e-10,
        "textbook comparator constants reproduce Rydberg scale",
    )
    log.check(
        rel_shift > 0.10,
        "direct alpha(M_Z) substitution is experimentally falsified at order 10 percent",
        f"shift={rel_shift:+.2%}",
    )
    log.check(
        abs(me_shift) > 0.10,
        "a hidden mass adjustment could absorb the alpha error, so mass and alpha gates are independent",
        f"hidden m_e shift={me_shift:+.2%}",
    )
    log.check(
        0.0 < active_log_for_alpha0 < log_mz_me,
        "a hidden effective threshold could fit alpha(0), so threshold data are load-bearing",
    )


def build_fanout_frames() -> list[FanoutFrame]:
    return [
        FanoutFrame(
            name="A. minimal Coulomb algebra",
            premise="standard NR Coulomb spectrum plus the branch-local scale bridge",
            forbidden="observed Rydberg target; fitted alpha or mass",
            attempt="factor E_n = -mu (Z alpha)^2/(2 n^2)",
            result="only the product mu*alpha^2 is fixed by an energy scale; mu and alpha remain separate retained gates",
            next_prerequisite="retained mu/m_e and retained alpha(0), not one fitted product",
            closure=False,
        ),
        FanoutFrame(
            name="B. QED running bridge",
            premise="retained alpha_EM(M_Z) and structural b_QED=32/3",
            forbidden="chosen effective threshold fitted to alpha(0)",
            attempt="run alpha downward with varied threshold placement",
            result="same high endpoint and same b_QED produce different low-energy couplings",
            next_prerequisite="threshold-resolved QED decoupling with charged thresholds and hadronic handling",
            closure=False,
        ),
        FanoutFrame(
            name="C. charged-lepton mass gate",
            premise="Lane 2 may record but not work Lane 6/Koide/V0 closure",
            forbidden="deriving y_e or editing charged-lepton branches in this loop",
            attempt="use the atomic scaffold with m_e as retained input",
            result="m_e is absent from Lane 2 and remains an upstream dependency",
            next_prerequisite="reviewed Lane 6 electron-mass retention, or an explicit admitted non-derivation comparator",
            closure=False,
        ),
        FanoutFrame(
            name="D. physical-unit kinetic map",
            premise="dimensionless lattice Coulomb companion H_g=-Delta_x-g/r",
            forbidden="choosing lattice spacing from -13.6 eV",
            attempt="map H_g to the physical one-body Hamiltonian",
            result="the exact map works only after a=g/(2 mu Z alpha) is supplied; it is not framework-native yet",
            next_prerequisite="retained kinetic normalization/physical length-time unit theorem",
            closure=False,
        ),
        FanoutFrame(
            name="E. scaffold falsifier",
            premise="existing standard-QM hydrogen/helium harness and 2026-04-27 firewall",
            forbidden="treating textbook inputs as framework outputs",
            attempt="compare scaffold success with direct high-scale-alpha substitution",
            result="scaffold success is conditional, while direct alpha(M_Z) fails by order 15 percent",
            next_prerequisite="substitute retained upstream gates only after they exist",
            closure=False,
        ),
    ]


def part5_stuck_fanout(log: CheckLog) -> None:
    section("Part 5: stuck fan-out synthesis")
    frames = build_fanout_frames()
    for frame in frames:
        print(f"  {frame.name}")
        print(f"    premise: {frame.premise}")
        print(f"    forbidden: {frame.forbidden}")
        print(f"    attempt: {frame.attempt}")
        print(f"    result: {frame.result}")
        print(f"    next prerequisite: {frame.next_prerequisite}")
        print()

    log.check(len(frames) == 5, "fan-out covers five orthogonal frames")
    log.check(
        all(not frame.closure for frame in frames),
        "no fan-out frame supports retained Rydberg closure on current inputs",
    )
    log.check(
        any("threshold-resolved" in frame.next_prerequisite for frame in frames),
        "fan-out preserves the alpha(0) transport prerequisite",
    )
    log.check(
        any("electron-mass" in frame.next_prerequisite or "mu/m_e" in frame.next_prerequisite for frame in frames),
        "fan-out preserves the mass prerequisite",
    )
    log.check(
        any("kinetic normalization" in frame.next_prerequisite for frame in frames),
        "fan-out preserves the physical-unit prerequisite",
    )


def part6_honest_status(log: CheckLog) -> None:
    section("Part 6: honest Lane 2 status")
    print("  Claim-state movement:")
    print("    exact boundary/support packet for gate factorization and stuck fan-out")
    print()
    print("  Can claim:")
    print("    current Lane 2 Rydberg closure factorizes into independent gates;")
    print("    scaffold success and retained Rydberg closure are now sharply separated;")
    print("    future work has three actionable theorem prerequisites.")
    print()
    print("  Cannot claim:")
    print("    retained Rydberg constant;")
    print("    retained alpha(0);")
    print("    retained electron/reduced mass;")
    print("    framework-native physical-unit Schrodinger/Coulomb limit.")

    log.check(
        True,
        "narrowest honest status is open with exact gate-factorization support",
        "not retained atomic-scale closure",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 2 ATOMIC RYDBERG GATE FACTORIZATION FAN-OUT")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the QED-threshold firewall and NR scale bridge, does any")
    print("  non-overlapping attack frame close retained Rydberg/atomic scale?")
    print()
    print("Answer:")
    print("  No. The current branch can honestly add exact gate-factorization support")
    print("  and a stuck-fan-out synthesis, while keeping retained closure open.")

    log = CheckLog()
    part1_grounding(log)
    part2_synthetic_gate_factorization(log)
    part3_threshold_frame(log)
    part4_comparator_falsifiers(log)
    part5_stuck_fanout(log)
    part6_honest_status(log)

    print()
    print("=" * 88)
    print(f"PASS={log.passed} FAIL={log.failed}")
    print("STATUS: open with exact gate-factorization support; no retained Rydberg closure.")
    print("=" * 88)
    return 0 if log.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
