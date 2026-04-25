#!/usr/bin/env python3
"""Chronology lane probe: local trace-preserving maps preserve record algebra.

This is the finite diagonal-algebra version of the operator statement:

    Tr[(O_R tensor I_L) (id_R tensor Phi_L)(rho)]
      = Tr[(O_R tensor I_L) rho]

for every trace-preserving local map Phi_L.  A non-trace-preserving selected
branch can change conditional statistics only after renormalization, and a map
that acts directly on R is not an operation outside the record algebra.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


PASS = 0
FAIL = 0

Joint = dict[tuple[int, int], Fraction]
Channel = dict[tuple[int, int], Fraction]  # (out_l, in_l) -> probability
Effect = dict[int, Fraction]


@dataclass(frozen=True)
class AuditResult:
    label: str
    record_marginal: dict[int, Fraction]
    trace: Fraction
    classification: str


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fmt_dist(dist: dict[int, Fraction]) -> str:
    return "{" + ", ".join(f"{bit}: {fmt_fraction(dist[bit])}" for bit in sorted(dist)) + "}"


def initial_joint() -> Joint:
    # Correlated but not product, with an asymmetric R marginal so direct
    # operations on R visibly differ from operations outside R.
    return {
        (0, 0): Fraction(1, 2),
        (0, 1): Fraction(1, 6),
        (1, 0): Fraction(1, 12),
        (1, 1): Fraction(1, 4),
    }


def trace_joint(joint: Joint) -> Fraction:
    return sum(joint.values(), Fraction(0))


def record_marginal(joint: Joint) -> dict[int, Fraction]:
    return {
        record: sum(prob for (r, _), prob in joint.items() if r == record)
        for record in (0, 1)
    }


def later_marginal(joint: Joint) -> dict[int, Fraction]:
    return {
        later: sum(prob for (_, l), prob in joint.items() if l == later)
        for later in (0, 1)
    }


def record_expectation(joint: Joint, observable: dict[int, Fraction]) -> Fraction:
    return sum(prob * observable[record] for (record, _), prob in joint.items())


def apply_later_channel(joint: Joint, channel: Channel) -> Joint:
    out: Joint = {(r, l): Fraction(0) for r in (0, 1) for l in (0, 1)}
    for (record, later_in), prob in joint.items():
        for later_out in (0, 1):
            out[(record, later_out)] += channel[(later_out, later_in)] * prob
    return out


def apply_record_flip(joint: Joint) -> Joint:
    out: Joint = {(r, l): Fraction(0) for r in (0, 1) for l in (0, 1)}
    for (record, later), prob in joint.items():
        out[(1 - record, later)] += prob
    return out


def apply_later_effect(joint: Joint, effect: Effect) -> Joint:
    return {(record, later): prob * effect[later] for (record, later), prob in joint.items()}


def normalize(joint: Joint) -> Joint:
    total = trace_joint(joint)
    if total == 0:
        raise ValueError("cannot normalize zero branch")
    return {key: prob / total for key, prob in joint.items()}


def channel_is_trace_preserving(channel: Channel) -> bool:
    return all(sum(channel[(out, incoming)] for out in (0, 1)) == 1 for incoming in (0, 1))


def heisenberg_dual_on_constant_one(channel: Channel) -> dict[int, Fraction]:
    # Phi^*(1)(in) = sum_out P(out | in) * 1(out).
    return {
        incoming: sum(channel[(out, incoming)] for out in (0, 1))
        for incoming in (0, 1)
    }


def audit(label: str, joint: Joint, classification: str) -> AuditResult:
    return AuditResult(label, record_marginal(joint), trace_joint(joint), classification)


def main() -> int:
    print("=" * 88)
    print("OPERATOR-ALGEBRA NO-PAST-SIGNAL PROBE")
    print("  Test: local trace-preserving maps outside R preserve the record marginal.")
    print("=" * 88)
    print()

    rho = initial_joint()
    record_obs = {0: Fraction(-1), 1: Fraction(1)}
    prior_r = record_marginal(rho)
    prior_expectation = record_expectation(rho, record_obs)

    noisy_later_channel: Channel = {
        (0, 0): Fraction(2, 3),
        (1, 0): Fraction(1, 3),
        (0, 1): Fraction(1, 4),
        (1, 1): Fraction(3, 4),
    }
    mixed = apply_later_channel(rho, noisy_later_channel)

    selected_effect = {0: Fraction(1, 5), 1: Fraction(4, 5)}
    selected_raw = apply_later_effect(rho, selected_effect)
    selected_norm = normalize(selected_raw)

    record_flipped = apply_record_flip(rho)

    print("Initial correlated state:")
    print(f"  trace = {fmt_fraction(trace_joint(rho))}")
    print(f"  R marginal = {fmt_dist(prior_r)}")
    print(f"  L marginal = {fmt_dist(later_marginal(rho))}")
    print(f"  <Z_R> = {fmt_fraction(prior_expectation)}")
    print()

    dual_one = heisenberg_dual_on_constant_one(noisy_later_channel)
    print("Later local trace-preserving channel:")
    print(f"  Phi_L^*(1)(0) = {fmt_fraction(dual_one[0])}")
    print(f"  Phi_L^*(1)(1) = {fmt_fraction(dual_one[1])}")
    print(f"  R marginal after id_R tensor Phi_L = {fmt_dist(record_marginal(mixed))}")
    print(f"  <Z_R> after channel = {fmt_fraction(record_expectation(mixed, record_obs))}")
    print()

    print("Selected non-trace-preserving later branch:")
    print(f"  raw branch trace = {fmt_fraction(trace_joint(selected_raw))}")
    print(f"  conditional R marginal = {fmt_dist(record_marginal(selected_norm))}")
    print()

    audits = [
        audit("retained local later channel", mixed, "trace-preserving local operation outside record algebra"),
        audit("postselected branch", selected_norm, "non-trace-preserving selected branch / final-boundary import"),
        audit("direct record flip", record_flipped, "operation acts on record algebra, not outside it"),
    ]
    for result in audits:
        print(
            f"  {result.label:30s} trace={fmt_fraction(result.trace):>4s} "
            f"R={fmt_dist(result.record_marginal):18s} {result.classification}"
        )
    print()

    check("initial state is normalized", trace_joint(rho) == 1)
    check("later channel is trace preserving", channel_is_trace_preserving(noisy_later_channel))
    check("Heisenberg dual preserves identity", dual_one == {0: Fraction(1), 1: Fraction(1)})
    check("later trace-preserving channel preserves record marginal", record_marginal(mixed) == prior_r)
    check(
        "later trace-preserving channel preserves record observable expectation",
        record_expectation(mixed, record_obs) == prior_expectation,
        f"<Z_R>={fmt_fraction(record_expectation(mixed, record_obs))}",
    )
    check(
        "selected non-trace-preserving branch can shift conditional record distribution",
        record_marginal(selected_norm) != prior_r and trace_joint(selected_raw) != 1,
        f"conditional={fmt_dist(record_marginal(selected_norm))}",
    )
    check(
        "direct record operation changes record marginal only by acting on R",
        record_marginal(record_flipped) == {0: prior_r[1], 1: prior_r[0]}
        and record_marginal(record_flipped) != prior_r,
        f"flipped={fmt_dist(record_marginal(record_flipped))}",
    )
    check(
        "classification does not promote selected branch to retained past signaling",
        "final-boundary import" in audits[1].classification,
        audits[1].classification,
    )

    print()
    print("SAFE READ")
    print("  - Local trace-preserving maps outside the record algebra preserve R.")
    print("  - Conditional postselected branches leave that surface.")
    print("  - Directly changing R is future erasure of a carrier, not a t1 operation")
    print("    outside R changing the already-realized t0 record.")
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
