#!/usr/bin/env python3
"""Route-specific no-go for the EW-current traceless-generator selector.

Authority note:
    docs/EW_CURRENT_TRACELESS_GENERATOR_SELECTOR_NO_GO_NOTE_2026-05-03.md

This runner checks a tempting positive route for the EW current matching gate:

    Tr_internal(Q_EW) = 0  =>  disconnected-current coefficient = 0.

That implication kills ordinary Wick-disconnected one-current loops, but it
does not kill the Fierz singlet color channel S = |Tr_color M|^2 / N_c inside
the connected two-current fermion-line contraction. The missing EW coefficient
`kappa_EW` is attached to that color channel, not to the separate
Wick-disconnected product of one-current traces.

Exit code: 0 on full PASS, 1 on any FAIL.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NOTE = DOCS / "EW_CURRENT_TRACELESS_GENERATOR_SELECTOR_NO_GO_NOTE_2026-05-03.md"
GATE = DOCS / "EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md"
FIERZ = DOCS / "EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md"
NOETHER = DOCS / "AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    suffix = f": {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return passed


def tr_diag(entries: tuple[Fraction, ...]) -> Fraction:
    return sum(entries, Fraction(0))


def tr_diag_square(entries: tuple[Fraction, ...]) -> Fraction:
    return sum((x * x for x in entries), Fraction(0))


def color_singlet_channel(trace_m: Fraction, n_c: int) -> Fraction:
    return trace_m * trace_m / n_c


def color_total_channel(frobenius_norm_sq: Fraction) -> Fraction:
    return frobenius_norm_sq


def color_adjoint_channel(frobenius_norm_sq: Fraction, trace_m: Fraction, n_c: int) -> Fraction:
    return color_total_channel(frobenius_norm_sq) - color_singlet_channel(trace_m, n_c)


def k_ew(n_c: int, kappa: Fraction) -> Fraction:
    f_adj = Fraction(n_c * n_c - 1, n_c * n_c)
    s = Fraction(1, n_c * n_c)
    return Fraction(1, 1) / (f_adj + kappa * s)


def main() -> int:
    print("=" * 84)
    print("EW CURRENT TRACELESS-GENERATOR SELECTOR NO-GO")
    print("=" * 84)

    note = NOTE.read_text(encoding="utf-8") if NOTE.exists() else ""
    gate = GATE.read_text(encoding="utf-8") if GATE.exists() else ""
    fierz = FIERZ.read_text(encoding="utf-8") if FIERZ.exists() else ""
    noether = NOETHER.read_text(encoding="utf-8") if NOETHER.exists() else ""

    check("authority note exists", NOTE.exists(), str(NOTE.relative_to(ROOT)))
    check("gate note exists", GATE.exists(), str(GATE.relative_to(ROOT)))
    check("Fierz note exists", FIERZ.exists(), str(FIERZ.relative_to(ROOT)))
    check("lattice Noether/current note exists", NOETHER.exists(), str(NOETHER.relative_to(ROOT)))
    check("note declares route-specific no-go", "**Type:** no_go" in note)
    check("note does not claim positive closure", "not a positive closure" in note)
    check("gate keeps kappa_EW explicit", "kappa_EW" in gate and "K_EW(kappa_EW)" in gate)
    check("Fierz note defines singlet channel S", "S(x, y)" in fierz and "|Tr G" in fierz)
    check("Noether note supplies bilinear current form", "J^{\u03bc,A}_x" in noether)

    n_c = 3

    # SU(2) T3 in the conventional fundamental normalization:
    # Tr T3 = 0, Tr T3^2 = 1/2.
    t3 = (Fraction(1, 2), Fraction(-1, 2))
    tr_t3 = tr_diag(t3)
    tr_t3_sq = tr_diag_square(t3)
    check("traceless EW generator has Tr(T3)=0", tr_t3 == 0, f"Tr(T3)={tr_t3}")
    check("same generator has nonzero quadratic trace", tr_t3_sq == Fraction(1, 2), f"Tr(T3^2)={tr_t3_sq}")

    # Wick-disconnected current loops carry one internal trace per current.
    wick_disconnected_internal_factor = tr_t3 * tr_t3
    check(
        "tracelessness kills ordinary Wick-disconnected one-current loops",
        wick_disconnected_internal_factor == 0,
        f"(Tr T3)^2={wick_disconnected_internal_factor}",
    )

    # Counterexample to the selector route: take the color propagator matrix
    # M = I_Nc. Its Fierz decomposition is purely singlet, yet the connected
    # two-current contraction with T3 at both vertices is nonzero.
    trace_identity_color = Fraction(n_c)
    frobenius_identity_color = Fraction(n_c)
    singlet_identity = color_singlet_channel(trace_identity_color, n_c)
    adjoint_identity = color_adjoint_channel(frobenius_identity_color, trace_identity_color, n_c)
    total_identity = color_total_channel(frobenius_identity_color)
    check("color identity matrix has total channel N_c", total_identity == n_c, f"T={total_identity}")
    check("color identity matrix is purely Fierz-singlet", singlet_identity == n_c, f"S={singlet_identity}")
    check("color identity matrix has zero adjoint channel", adjoint_identity == 0, f"C={adjoint_identity}")

    same_line_total = total_identity * tr_t3_sq
    same_line_singlet = singlet_identity * tr_t3_sq
    same_line_adjoint = adjoint_identity * tr_t3_sq
    check(
        "connected two-current contraction is nonzero for M=I_color",
        same_line_total == Fraction(3, 2),
        f"Tr_color(I) * Tr(T3^2) = {same_line_total}",
    )
    check(
        "that nonzero contraction is entirely the color Fierz singlet S",
        same_line_singlet == same_line_total and same_line_adjoint == 0,
        f"S_EW={same_line_singlet}, C_EW={same_line_adjoint}",
    )
    check(
        "therefore Tr(Q_EW)=0 does not imply kappa_EW=0",
        same_line_singlet != 0 and wick_disconnected_internal_factor == 0,
        "zero Wick-disconnected loop coexists with nonzero color-singlet channel",
    )

    # A color-adjoint matrix shows the actual selector would have to act on the
    # color matrix M, not on the internal EW generator. Take diag(1/2,-1/2,0).
    color_t3 = (Fraction(1, 2), Fraction(-1, 2), Fraction(0))
    trace_color_t3 = tr_diag(color_t3)
    frob_color_t3 = tr_diag_square(color_t3)
    singlet_color_t3 = color_singlet_channel(trace_color_t3, n_c)
    adjoint_color_t3 = color_adjoint_channel(frob_color_t3, trace_color_t3, n_c)
    check("color-traceless matrix has zero Fierz singlet", singlet_color_t3 == 0, f"S={singlet_color_t3}")
    check("color-traceless matrix has nonzero adjoint channel", adjoint_color_t3 == Fraction(1, 2), f"C={adjoint_color_t3}")

    check("connected selector would give K_EW(0)=9/8", k_ew(n_c, Fraction(0)) == Fraction(9, 8), f"K={k_ew(n_c, Fraction(0))}")
    check("full-trace readout remains algebraically admissible at K_EW(1)=1", k_ew(n_c, Fraction(1)) == 1, f"K={k_ew(n_c, Fraction(1))}")
    check(
        "traceless-generator route cannot distinguish kappa=0 from kappa=1",
        k_ew(n_c, Fraction(0)) != k_ew(n_c, Fraction(1)),
        "additional color-channel selector still required",
    )

    required_note_phrases = [
        "Wick-disconnected",
        "color Fierz singlet",
        "Tr_internal(Q_EW)^2",
        "Tr_internal(Q_EW^2)",
        "kappa_EW",
        "not a positive closure",
    ]
    for phrase in required_note_phrases:
        check(f"note records phrase {phrase!r}", phrase in note)

    print()
    print("=" * 84)
    print(f"RESULT: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 84)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
