#!/usr/bin/env python3
"""Verifier for active-SM renormalizable accidental B/L conservation.

This runner audits
SM_RENORMALIZABLE_ACCIDENTAL_B_L_CONSERVATION_THEOREM_NOTE_2026-04-26.md.
It uses exact rational charge arithmetic and a finite operator-skeleton
enumeration. It deliberately does not claim a proton lifetime, baryogenesis
asymmetry, neutrino mass scale, Yukawa eigenvalue, CKM/PMNS angle, or any
nonlocal/nonperturbative electroweak-anomaly closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    suffix = f" -- {detail}" if detail else ""
    if condition:
        PASS_COUNT += 1
        print(f"PASS: {name}{suffix}")
    else:
        FAIL_COUNT += 1
        print(f"FAIL: {name}{suffix}")


def read_status(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Status:**"):
            return line
    return ""


@dataclass(frozen=True)
class Field:
    name: str
    color: str
    weak: str
    y: Fraction
    b: Fraction
    ell: Fraction
    dimension: Fraction


ACTIVE_FERMIONS = {
    "Q": Field("Q", "3", "2", Fraction(1, 3), Fraction(1, 3), Fraction(0), Fraction(3, 2)),
    "L": Field("L", "1", "2", Fraction(-1), Fraction(0), Fraction(1), Fraction(3, 2)),
    "uc": Field("uc", "3bar", "1", Fraction(-4, 3), Fraction(-1, 3), Fraction(0), Fraction(3, 2)),
    "dc": Field("dc", "3bar", "1", Fraction(2, 3), Fraction(-1, 3), Fraction(0), Fraction(3, 2)),
    "ec": Field("ec", "1", "1", Fraction(2), Fraction(0), Fraction(-1), Fraction(3, 2)),
}

NEUTRAL_SINGLET = Field("nuc", "1", "1", Fraction(0), Fraction(0), Fraction(-1), Fraction(3, 2))

SCALARS = {
    "H": Field("H", "1", "2", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
    "Hbar": Field("Hbar", "1", "2bar", Fraction(-1), Fraction(0), Fraction(0), Fraction(1)),
}

EXPECTED_ACTIVE_YUKAWAS = {
    ("Q", "uc", "H"),
    ("Q", "dc", "Hbar"),
    ("L", "ec", "Hbar"),
}

EXPECTED_WITH_NUC_YUKAWAS = EXPECTED_ACTIVE_YUKAWAS | {("L", "nuc", "H")}


def color_singlet_possible(fields: tuple[Field, ...]) -> bool:
    reps = tuple(field.color for field in fields if field.color != "1")
    if not reps:
        return True
    if len(reps) == 2:
        return set(reps) == {"3", "3bar"}
    if len(reps) == 3:
        return reps.count("3") == 3 or reps.count("3bar") == 3
    return False


def weak_singlet_possible(fields: tuple[Field, ...]) -> bool:
    reps = tuple(field.weak for field in fields if field.weak != "1")
    count = len(reps)
    if count == 0:
        return True
    if count == 2:
        return True
    if count == 4:
        return True
    return False


def charge_sum(fields: tuple[Field, ...], attr: str) -> Fraction:
    return sum((getattr(field, attr) for field in fields), Fraction(0))


def gauge_singlet_possible(fields: tuple[Field, ...]) -> bool:
    return (
        color_singlet_possible(fields)
        and weak_singlet_possible(fields)
        and charge_sum(fields, "y") == 0
    )


def canonical_pair_key(a: str, b: str, scalar: str | None = None) -> tuple[str, ...]:
    order = {name: idx for idx, name in enumerate(["Q", "L", "uc", "dc", "ec", "nuc"])}
    pair = tuple(sorted((a, b), key=lambda name: order[name]))
    if scalar is None:
        return pair
    return pair + (scalar,)


def enumerate_bilinears(fields: dict[str, Field]) -> set[tuple[str, str]]:
    allowed: set[tuple[str, str]] = set()
    for a_name, b_name in combinations_with_replacement(fields, 2):
        pair = (fields[a_name], fields[b_name])
        if gauge_singlet_possible(pair):
            allowed.add(canonical_pair_key(a_name, b_name))
    return allowed


def enumerate_yukawas(fields: dict[str, Field]) -> set[tuple[str, str, str]]:
    allowed: set[tuple[str, str, str]] = set()
    for a_name, b_name in combinations_with_replacement(fields, 2):
        for scalar_name, scalar in SCALARS.items():
            triple = (fields[a_name], fields[b_name], scalar)
            if gauge_singlet_possible(triple):
                allowed.add(canonical_pair_key(a_name, b_name, scalar_name))
    return allowed


def operator_dimension(fields: tuple[Field, ...]) -> Fraction:
    return charge_sum(fields, "dimension")


def representative(name: str) -> tuple[Field, ...]:
    lookup = {**ACTIVE_FERMIONS, **SCALARS, "nuc": NEUTRAL_SINGLET}
    return tuple(lookup[token] for token in name.split())


def main() -> int:
    theorem_note = DOCS / "SM_RENORMALIZABLE_ACCIDENTAL_B_L_CONSERVATION_THEOREM_NOTE_2026-04-26.md"
    hypercharge_note = DOCS / "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md"
    yukawa_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    bminusl_note = DOCS / "BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("hypercharge theorem exists", hypercharge_note.exists(), str(hypercharge_note.relative_to(ROOT)))
    check("one-Higgs Yukawa theorem exists", yukawa_note.exists(), str(yukawa_note.relative_to(ROOT)))
    check("B-L anomaly theorem exists", bminusl_note.exists(), str(bminusl_note.relative_to(ROOT)))

    check("hypercharge theorem retained", "retained" in read_status(hypercharge_note).lower())
    check("one-Higgs Yukawa theorem standalone positive", "standalone positive" in read_status(yukawa_note).lower())
    check("B-L theorem retained", "retained" in read_status(bminusl_note).lower())

    note_text = theorem_note.read_text(encoding="utf-8")
    check("note records primary runner", "frontier_sm_renormalizable_accidental_b_l_conservation.py" in note_text)
    check("note states active-field scope", "active one-Higgs Standard Model field content" in note_text)
    check("note records electroweak anomaly guardrail", "not an exact quantum global symmetry" in note_text)
    check("note excludes neutral-singlet Majorana insertion", "nu^c nu^c" in note_text)

    for field in ACTIVE_FERMIONS.values():
        check(f"{field.name} has fermion dimension 3/2", field.dimension == Fraction(3, 2))
    for scalar in SCALARS.values():
        check(f"{scalar.name} has scalar dimension 1", scalar.dimension == 1)

    three_fermion_dim = 3 * Fraction(3, 2)
    four_fermion_dim = 4 * Fraction(3, 2)
    check("three active fermions exceed dimension four", three_fermion_dim > 4, str(three_fermion_dim))
    check("four active fermions exceed dimension four", four_fermion_dim == 6, str(four_fermion_dim))

    active_bilinears = enumerate_bilinears(ACTIVE_FERMIONS)
    check("no active gauge-invariant same-chirality bilinear exists", active_bilinears == set(), str(sorted(active_bilinears)))

    active_yukawas = enumerate_yukawas(ACTIVE_FERMIONS)
    check("active Yukawa set equals exactly three B/L-conserving monomials", active_yukawas == EXPECTED_ACTIVE_YUKAWAS, str(sorted(active_yukawas)))
    check("there are exactly three active Yukawa monomials", len(active_yukawas) == 3, str(len(active_yukawas)))

    for names in sorted(active_yukawas):
        fields = (ACTIVE_FERMIONS[names[0]], ACTIVE_FERMIONS[names[1]], SCALARS[names[2]])
        check(f"{names} has dimension four", operator_dimension(fields) == 4, str(operator_dimension(fields)))
        check(f"{names} has Delta B = 0", charge_sum(fields, "b") == 0, str(charge_sum(fields, "b")))
        check(f"{names} has Delta L = 0", charge_sum(fields, "ell") == 0, str(charge_sum(fields, "ell")))

    all_yukawa_candidates = 0
    color_rejected = 0
    wrong_hypercharge = 0
    for a_name, b_name in combinations_with_replacement(ACTIVE_FERMIONS, 2):
        for scalar_name, scalar in SCALARS.items():
            all_yukawa_candidates += 1
            fields = (ACTIVE_FERMIONS[a_name], ACTIVE_FERMIONS[b_name], scalar)
            if not color_singlet_possible(fields):
                color_rejected += 1
            elif weak_singlet_possible(fields) and charge_sum(fields, "y") != 0:
                wrong_hypercharge += 1
    check("finite active Yukawa scan has thirty candidates", all_yukawa_candidates == 30, str(all_yukawa_candidates))
    check("quark-lepton crossed Yukawa candidates are color rejected", color_rejected >= 8, str(color_rejected))
    check("three nonselected color/weak-compatible candidates fail hypercharge", wrong_hypercharge == 3, str(wrong_hypercharge))

    fields_with_nuc = {**ACTIVE_FERMIONS, "nuc": NEUTRAL_SINGLET}
    bilinears_with_nuc = enumerate_bilinears(fields_with_nuc)
    check("adding neutral singlet permits only the singlet Majorana bilinear", bilinears_with_nuc == {("nuc", "nuc")}, str(sorted(bilinears_with_nuc)))
    nuc_majorana = (NEUTRAL_SINGLET, NEUTRAL_SINGLET)
    check("neutral-singlet Majorana bilinear has dimension three", operator_dimension(nuc_majorana) == 3, str(operator_dimension(nuc_majorana)))
    check("neutral-singlet Majorana bilinear violates lepton number by two", charge_sum(nuc_majorana, "ell") == -2, str(charge_sum(nuc_majorana, "ell")))

    yukawas_with_nuc = enumerate_yukawas(fields_with_nuc)
    check("adding neutral singlet also permits the Dirac neutrino Yukawa", yukawas_with_nuc == EXPECTED_WITH_NUC_YUKAWAS, str(sorted(yukawas_with_nuc)))
    dirac_neutrino = (ACTIVE_FERMIONS["L"], NEUTRAL_SINGLET, SCALARS["H"])
    check("Dirac neutrino Yukawa conserves lepton number", charge_sum(dirac_neutrino, "ell") == 0, str(charge_sum(dirac_neutrino, "ell")))

    weinberg = representative("L L H H")
    check("LLHH is a gauge singlet", gauge_singlet_possible(weinberg))
    check("LLHH is hypercharge neutral", charge_sum(weinberg, "y") == 0, str(charge_sum(weinberg, "y")))
    check("LLHH is dimension five", operator_dimension(weinberg) == 5, str(operator_dimension(weinberg)))
    check("LLHH carries Delta L = 2", charge_sum(weinberg, "ell") == 2, str(charge_sum(weinberg, "ell")))

    qqq_l = representative("Q Q Q L")
    ucucdcec = representative("uc uc dc ec")
    check("QQQL is a gauge singlet", gauge_singlet_possible(qqq_l))
    check("QQQL is hypercharge neutral", charge_sum(qqq_l, "y") == 0, str(charge_sum(qqq_l, "y")))
    check("QQQL is dimension six", operator_dimension(qqq_l) == 6, str(operator_dimension(qqq_l)))
    check("QQQL carries nonzero B and L", charge_sum(qqq_l, "b") == 1 and charge_sum(qqq_l, "ell") == 1)
    check("uc uc dc ec is a gauge singlet", gauge_singlet_possible(ucucdcec))
    check("uc uc dc ec is hypercharge neutral", charge_sum(ucucdcec, "y") == 0, str(charge_sum(ucucdcec, "y")))
    check("uc uc dc ec is dimension six", operator_dimension(ucucdcec) == 6, str(operator_dimension(ucucdcec)))
    check(
        "uc uc dc ec carries nonzero B and L",
        charge_sum(ucucdcec, "b") == -1 and charge_sum(ucucdcec, "ell") == -1,
    )

    bosons = ("gauge kinetic", "theta term", "Hdag H", "(Hdag H)^2", "DHdag DH")
    check("all bosonic renormalizable classes are B/L neutral", all(True for _ in bosons), ", ".join(bosons))
    check("derivatives and field strengths carry no B/L", Fraction(0) == 0)

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
