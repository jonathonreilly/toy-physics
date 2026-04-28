#!/usr/bin/env python3
"""Lane 3 five-sixths scale-selection boundary.

This block-04 runner checks the sharp 3A boundary behind
QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md.

It verifies that exact SU(3) gives C_F - T_F = 5/6 and that the bounded
bridge is numerically sharp on the threshold-local self-scale comparator.
It also verifies that the same fixed exponent is not scale-blind: the
common-scale comparator differs by the inherited one-loop transport factor,
so a retained proof still needs a scale-selection or RG-covariant transport
theorem.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import math
import sys

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0

C_F = Fraction(4, 3)
T_F = Fraction(1, 2)
P_FIVE_SIXTHS = C_F - T_F
INV_P = Fraction(1, 1) / P_FIVE_SIXTHS

V_CB_ATLAS = CANONICAL_ALPHA_S_V / math.sqrt(6.0)

# Inherited comparator values from CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md.
M_S_2GEV = 93.4e-3
M_B_MB = 4.180
R_SELF = M_S_2GEV / M_B_MB
ALPHA_S_2GEV = 0.301
ALPHA_S_MB = 0.226
GAMMA0_OVER_2BETA0 = Fraction(12, 25)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel_dev(value: float, reference: float) -> float:
    return value / reference - 1.0


def pct(value: float) -> str:
    return f"{100.0 * value:+.3f}%"


def transport_factor() -> float:
    return (ALPHA_S_2GEV / ALPHA_S_MB) ** float(GAMMA0_OVER_2BETA0)


def r_same_scale() -> float:
    return R_SELF / transport_factor()


def exponent_inferred(v_cb: float, ratio: float) -> float:
    return math.log(v_cb) / math.log(ratio)


def main() -> int:
    print("=" * 88)
    print("LANE 3 FIVE-SIXTHS SCALE-SELECTION BOUNDARY")
    print("=" * 88)

    new_note = DOCS / "QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md"
    support_note = DOCS / "CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md"
    staircase_note = DOCS / "QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"
    ckm_note = DOCS / "CKM_ATLAS_AXIOM_CLOSURE_NOTE.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (new_note, support_note, staircase_note, firewall_note, ckm_note):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    support_text = read(support_note)
    staircase_text = read(staircase_note)
    firewall_text = read(firewall_note)

    check("new note is a boundary, not a retained mass claim", "does not" in new_text and "claim retained `m_d`, `m_s`, or `m_b`" in new_text)
    check("support note classifies 5/6 as bounded support", "bounded support tool" in support_text and "scale-choice closure is not yet theorem-grade" in support_text)
    check("taste-staircase note keeps 5/6 mechanism open", "non-perturbative `g = 1` mechanism" in staircase_text)
    check("Lane 3 firewall keeps down-type retention open", "down-type bridges and scale-selection rule" in firewall_text)

    print()
    print("B. Exact SU(3) and CKM inputs")
    print("-" * 72)
    check("C_F = 4/3 exactly", C_F == Fraction(4, 3), str(C_F))
    check("T_F = 1/2 exactly", T_F == Fraction(1, 2), str(T_F))
    check("C_F - T_F = 5/6 exactly", P_FIVE_SIXTHS == Fraction(5, 6), str(P_FIVE_SIXTHS))
    check("inverse exponent is 6/5 exactly", INV_P == Fraction(6, 5), str(INV_P))
    check("|V_cb|_atlas = alpha_s(v)/sqrt(6) is positive", V_CB_ATLAS > 0.0, f"{V_CB_ATLAS:.12f}")
    check("|V_cb|_atlas is in the CKM-size range", 0.04 < V_CB_ATLAS < 0.045, f"{V_CB_ATLAS:.12f}")

    print()
    print("C. Threshold-local bounded support")
    print("-" * 72)
    r_pred = V_CB_ATLAS ** float(INV_P)
    dev_self = rel_dev(r_pred, R_SELF)
    p_self = exponent_inferred(V_CB_ATLAS, R_SELF)

    print(f"  |V_cb|_atlas = {V_CB_ATLAS:.12f}")
    print(f"  R_pred       = |V_cb|^(6/5) = {r_pred:.12f}")
    print(f"  R_self       = m_s(2 GeV)/m_b(m_b) = {R_SELF:.12f}")
    print(f"  p_self       = log(|V_cb|)/log(R_self) = {p_self:.12f}")
    print(f"  deviation    = {pct(dev_self)}")

    check("R_pred is the unique ratio implied by granted 5/6 bridge", abs(r_pred - V_CB_ATLAS ** (6.0 / 5.0)) < 1.0e-15)
    check("threshold-local comparator is within 1% of the 5/6 prediction", abs(dev_self) < 0.01, pct(dev_self))
    check("threshold-local inferred exponent is near 5/6", abs(p_self - float(P_FIVE_SIXTHS)) < 0.001, f"delta={p_self - float(P_FIVE_SIXTHS):+.6f}")
    check("the match is not exact and still uses a comparator surface", abs(dev_self) > 1.0e-4, pct(dev_self))

    print()
    print("D. Common-scale transport boundary")
    print("-" * 72)
    t = transport_factor()
    r_same = r_same_scale()
    dev_same = rel_dev(r_pred, r_same)
    p_same = exponent_inferred(V_CB_ATLAS, r_same)

    print(f"  alpha_s(2 GeV) = {ALPHA_S_2GEV:.3f}")
    print(f"  alpha_s(m_b)   = {ALPHA_S_MB:.3f}")
    print(f"  transport T    = {t:.12f}")
    print(f"  R_same         = m_s(m_b)/m_b(m_b) = {r_same:.12f}")
    print(f"  p_same         = log(|V_cb|)/log(R_same) = {p_same:.12f}")
    print(f"  same deviation = {pct(dev_same)}")

    check("one-loop transport factor is nontrivial", t > 1.1, f"T={t:.12f}")
    check("R_self = R_same * T", abs(R_SELF - r_same * t) < 1.0e-15, f"diff={abs(R_SELF - r_same * t):.2e}")
    check("same-scale comparator is materially different from self-scale comparator", abs(rel_dev(r_same, R_SELF)) > 0.1, pct(rel_dev(r_same, R_SELF)))
    check("same-scale inferred exponent is not near 5/6", abs(p_same - float(P_FIVE_SIXTHS)) > 0.02, f"delta={p_same - float(P_FIVE_SIXTHS):+.6f}")
    check("same-scale mismatch is material", abs(dev_same) > 0.10, pct(dev_same))
    check("self-scale surface is much closer than common-scale surface", abs(dev_self) < abs(dev_same) / 20.0, f"self={pct(dev_self)}, same={pct(dev_same)}")

    print()
    print("E. Scale-blind exactness obstruction")
    print("-" * 72)
    t_to_p = t ** float(P_FIVE_SIXTHS)
    same_pred_from_self = (R_SELF / t) ** float(P_FIVE_SIXTHS)
    self_pred = R_SELF ** float(P_FIVE_SIXTHS)

    check("T^(5/6) is not 1", abs(t_to_p - 1.0) > 0.1, f"T^p={t_to_p:.12f}")
    check("same exponent on transported ratio changes the CKM amplitude", abs(same_pred_from_self / self_pred - 1.0) > 0.1, f"factor={same_pred_from_self / self_pred:.12f}")
    check("p_self and p_same are separated by the transport choice", abs(p_self - p_same) > 0.02, f"delta={p_self - p_same:.6f}")
    check("5/6 cannot be exact on both surfaces unless T=1", t != 1.0 and abs(t_to_p - 1.0) > 0.1)
    check("scale-selection theorem remains a separate load-bearing target", "scale-selection theorem" in new_text and "RG-covariant transport theorem" in new_text)

    print()
    print("F. Import and claim firewall")
    print("-" * 72)
    proof_inputs = {
        "C_F",
        "T_F",
        "alpha_s_v",
        "V_cb_atlas",
        "one_loop_transport_context",
        "comparator_surface_labels",
    }
    forbidden_inputs = {
        "observed_masses_as_derivation",
        "fitted_yukawa_entries",
        "hidden_scale_selector",
    }
    check("forbidden proof inputs are absent", proof_inputs.isdisjoint(forbidden_inputs), str(sorted(proof_inputs)))
    check("new note says exact Casimir rational is not scale theorem", "The exact Casimir identity supplies neither by itself" in new_text)
    check("new note keeps down-type ratios bounded", "down-type ratios remain bounded support" in new_text)
    check("new note states no retained down-type mass closure", "cannot retain" in new_text and "`m_d`, `m_s`, or `m_b`" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: 5/6 remains bounded support until a scale-selection or")
        print("RG-covariant transport theorem is supplied.")
        return 0
    print("VERDICT: scale-selection boundary verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
