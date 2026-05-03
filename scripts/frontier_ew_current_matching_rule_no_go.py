#!/usr/bin/env python3
"""EW current matching-rule no-go runner.

Authority note:
    docs/EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md

The runner checks the formal underdetermination argument:

    F_adj = (N_c^2 - 1) / N_c^2
    K_EW(kappa) = 1 / (F_adj + kappa * (1 - F_adj))

The current retained primitives fix F_adj and CMT color-blind scaling, but
do not fix kappa. Two completions, kappa=0 and kappa=1, satisfy the same
primitive constraints and give different EW matching factors. Therefore the
connected-trace selector kappa=0 is not derivable from those primitives.

Exit code: 0 on full PASS, 1 on any FAIL.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md"
FIERZ = DOCS / "EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def f_adj(n_c: int) -> Fraction:
    return Fraction(n_c * n_c - 1, n_c * n_c)


def singlet_fraction(n_c: int) -> Fraction:
    return Fraction(1, n_c * n_c)


def k_ew(n_c: int, kappa: Fraction) -> Fraction:
    f = f_adj(n_c)
    return Fraction(1, 1) / (f + kappa * (1 - f))


@dataclass(frozen=True)
class Completion:
    n_c: int
    kappa: Fraction
    u0_squared: Fraction

    @property
    def c_v(self) -> Fraction:
        return f_adj(self.n_c)

    @property
    def s_v(self) -> Fraction:
        return singlet_fraction(self.n_c)

    @property
    def t_v(self) -> Fraction:
        return self.c_v + self.s_v

    @property
    def c_u(self) -> Fraction:
        return self.u0_squared * self.c_v

    @property
    def s_u(self) -> Fraction:
        return self.u0_squared * self.s_v

    @property
    def t_u(self) -> Fraction:
        return self.c_u + self.s_u

    @property
    def readout_v(self) -> Fraction:
        return self.c_v + self.kappa * self.s_v

    @property
    def readout_u(self) -> Fraction:
        return self.c_u + self.kappa * self.s_u

    @property
    def matching_v(self) -> Fraction:
        return self.t_v / self.readout_v

    @property
    def matching_u(self) -> Fraction:
        return self.t_u / self.readout_u

    @property
    def ozi_ratio(self) -> Fraction:
        return self.kappa * self.s_v / self.c_v


def primitive_signature(model: Completion) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return the primitive data that the retained packet fixes."""
    return (
        f_adj(model.n_c),
        singlet_fraction(model.n_c),
        model.c_u / model.c_v,
        model.s_u / model.s_v,
    )


def downstream_guard(path: Path, required: list[str], forbidden_windows: list[str]) -> None:
    text = read(path)
    for needle in required:
        check(
            f"{path.relative_to(ROOT)} contains {needle!r}",
            needle in text,
            "downstream conditional wording present",
        )
    for phrase in forbidden_windows:
        check(
            f"{path.relative_to(ROOT)} avoids {phrase!r}",
            phrase not in text,
            "unconditional EW-retention wording absent",
        )


def main() -> int:
    print("=" * 78)
    print("EW CURRENT MATCHING-RULE NO-GO")
    print("=" * 78)

    note = read(NOTE)
    fierz = read(FIERZ)

    check("authority note exists", NOTE.exists(), str(NOTE.relative_to(ROOT)))
    check("Fierz authority exists", FIERZ.exists(), str(FIERZ.relative_to(ROOT)))
    check("note is typed as no_go", "**Type:** no_go" in note, "claim-type hint present")
    check(
        "note registers the primary runner",
        "scripts/frontier_ew_current_matching_rule_no_go.py" in note,
        "runner path present",
    )
    check(
        "note cites retained Fierz/channel authority",
        "EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md" in note,
        "one-hop retained-bounded dependency present",
    )
    check(
        "Fierz authority explicitly leaves matching rule open",
        "The matching rule is **not derived in this note**" in fierz,
        "upstream does not already prove kappa_EW=0",
    )

    nc = 3
    f = f_adj(nc)
    s = singlet_fraction(nc)
    check("F_adj at N_c=3 is exactly 8/9", f == Fraction(8, 9), f"F_adj={f}")
    check("singlet fraction at N_c=3 is exactly 1/9", s == Fraction(1, 9), f"S={s}")
    check("channels sum to the total", f + s == 1, f"F_adj+S={f+s}")

    connected = Completion(n_c=nc, kappa=Fraction(0), u0_squared=Fraction(77, 100))
    full_trace = Completion(n_c=nc, kappa=Fraction(1), u0_squared=Fraction(77, 100))
    half_trace = Completion(n_c=nc, kappa=Fraction(1, 2), u0_squared=Fraction(77, 100))

    check(
        "connected-trace specialization gives K_EW=9/8",
        connected.matching_v == Fraction(9, 8),
        f"K_EW(0)={connected.matching_v}",
    )
    check(
        "full-trace specialization gives K_EW=1",
        full_trace.matching_v == Fraction(1, 1),
        f"K_EW(1)={full_trace.matching_v}",
    )
    check(
        "intermediate kappa gives a distinct admissible coefficient",
        half_trace.matching_v == Fraction(18, 17),
        f"K_EW(1/2)={half_trace.matching_v}",
    )
    check(
        "two completions share all retained primitive data",
        primitive_signature(connected) == primitive_signature(full_trace),
        f"signature={primitive_signature(connected)}",
    )
    check(
        "two completions disagree on EW matching factor",
        connected.matching_v != full_trace.matching_v,
        f"{connected.matching_v} != {full_trace.matching_v}",
    )

    for model in (connected, full_trace, half_trace):
        check(
            f"CMT scaling cancels from K_EW at kappa={model.kappa}",
            model.matching_u == model.matching_v,
            f"K_U={model.matching_u}, K_V={model.matching_v}",
        )
        check(
            f"OZI class is bounded at kappa={model.kappa}",
            abs(model.ozi_ratio) <= Fraction(1, nc * nc - 1),
            f"kappa*S/C={model.ozi_ratio}",
        )

    for other_nc in (2, 3, 4, 5, 10):
        model = Completion(n_c=other_nc, kappa=Fraction(1), u0_squared=Fraction(3, 5))
        bound = Fraction(1, other_nc * other_nc - 1)
        check(
            f"full-trace disconnected ratio is O(1/N_c^2) at N_c={other_nc}",
            model.ozi_ratio == bound,
            f"S/C={model.ozi_ratio}, bound={bound}",
        )

    check(
        "note states the conditional coefficient formula",
        "K_EW(kappa_EW) = 1 / (F_adj + kappa_EW (1 - F_adj))" in note,
        "formula present",
    )
    check(
        "note states 9/8 is special case only",
        "The package-level `9/8` factor is the special case" in note,
        "no unconditional promotion",
    )
    check(
        "note records the two-completion witness",
        "Completion A: kappa_EW = 0" in note and "Completion B: kappa_EW = 1" in note,
        "independence witness present",
    )

    downstream_guard(
        DOCS / "YT_EW_COLOR_PROJECTION_THEOREM.md",
        required=["kappa_EW", "K_EW(kappa_EW)", "audited_conditional / bounded"],
        forbidden_windows=[
            "**Status:** proposed_retained EW normalization lane",
            "The correction 9/8 on the EW couplings is derived from",
        ],
    )
    downstream_guard(
        DOCS / "publication" / "ci3_z3" / "QUANTITATIVE_SUMMARY_TABLE.md",
        required=["matching-rule conditional", "kappa_EW"],
        forbidden_windows=[
            "| `g_1(v)` | `0.4644` | `0.4640` | `+0.08%` | retained |",
            "| `g_2(v)` | `0.6480` | `0.6463` | `+0.26%` | retained |",
        ],
    )
    downstream_guard(
        DOCS / "publication" / "ci3_z3" / "USABLE_DERIVED_VALUES_INDEX.md",
        required=["K_EW(kappa_EW)", "conditional"],
        forbidden_windows=[
            "| `g_1(v)` | `0.4644` | derived |",
            "| `g_2(v)` | `0.6480` | derived |",
        ],
    )
    downstream_guard(
        DOCS / "CANONICAL_HARNESS_INDEX.md",
        required=["EW current matching rule no-go closure", "frontier_ew_current_matching_rule_no_go.py"],
        forbidden_windows=["EW current matching rule open main gate"],
    )

    print()
    print("=" * 78)
    print(f"RESULT: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
