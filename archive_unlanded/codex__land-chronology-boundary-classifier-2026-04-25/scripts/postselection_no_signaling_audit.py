#!/usr/bin/env python3
"""Chronology lane probe: postselection conditioning versus past editing.

This is a pure-Python probability-table audit. It defines an earlier durable
record R(t0), a later outcome L(t1) correlated with that record, and an
ordinary postselection filter on the later outcome.

The retained distinction is:

    P(R(t0) | L(t1) selected) can differ from P(R(t0)).
    The unconditioned R(t0) marginal and discarded run classes are not edited.

If the later condition is promoted from an ordinary filter to a deterministic
history rule, that is final-boundary import. It is not operational past
signaling on the retained single-clock local-data surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


PASS = 0
FAIL = 0
SELECTED = "selected"
DISCARDED = "discarded"


@dataclass(frozen=True)
class Cell:
    run_class: str
    earlier_record: int
    durable_copy: int
    later_outcome: str
    probability: Fraction


Table = tuple[Cell, ...]
Distribution = dict[int, Fraction]


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


def joint_table() -> Table:
    """Return P(R, L) with L correlated with the earlier durable record."""

    prior = {0: Fraction(1, 2), 1: Fraction(1, 2)}
    selection_rate = {0: Fraction(1, 5), 1: Fraction(4, 5)}
    cells: list[Cell] = []
    for record in (0, 1):
        p_record = prior[record]
        p_selected = p_record * selection_rate[record]
        p_discarded = p_record * (1 - selection_rate[record])
        cells.append(
            Cell(
                run_class=f"R{record}-S",
                earlier_record=record,
                durable_copy=record,
                later_outcome=SELECTED,
                probability=p_selected,
            )
        )
        cells.append(
            Cell(
                run_class=f"R{record}-D",
                earlier_record=record,
                durable_copy=record,
                later_outcome=DISCARDED,
                probability=p_discarded,
            )
        )
    return tuple(cells)


def total_probability(table: Table) -> Fraction:
    return sum((cell.probability for cell in table), Fraction(0))


def filter_outcome(table: Table, later_outcome: str) -> Table:
    return tuple(cell for cell in table if cell.later_outcome == later_outcome)


def normalize(table: Table) -> Table:
    total = total_probability(table)
    if total == 0:
        raise ValueError("cannot condition on a zero-probability event")
    return tuple(
        Cell(
            run_class=cell.run_class,
            earlier_record=cell.earlier_record,
            durable_copy=cell.durable_copy,
            later_outcome=cell.later_outcome,
            probability=cell.probability / total,
        )
        for cell in table
    )


def record_marginal(table: Table) -> Distribution:
    marginal = {0: Fraction(0), 1: Fraction(0)}
    for cell in table:
        marginal[cell.earlier_record] += cell.probability
    return marginal


def conditional_record_distribution(table: Table, later_outcome: str) -> Distribution:
    return record_marginal(normalize(filter_outcome(table, later_outcome)))


def selection_probability_given_record(table: Table, record: int) -> Fraction:
    record_cells = tuple(cell for cell in table if cell.earlier_record == record)
    selected_cells = tuple(
        cell for cell in record_cells if cell.later_outcome == SELECTED
    )
    return total_probability(selected_cells) / total_probability(record_cells)


def weighted_recombine(
    selected_weight: Fraction,
    selected_distribution: Distribution,
    discarded_weight: Fraction,
    discarded_distribution: Distribution,
) -> Distribution:
    return {
        record: (
            selected_weight * selected_distribution[record]
            + discarded_weight * discarded_distribution[record]
        )
        for record in (0, 1)
    }


def table_signature(table: Table, include_probability: bool) -> tuple[tuple[object, ...], ...]:
    rows: list[tuple[object, ...]] = []
    for cell in table:
        base: tuple[object, ...] = (
            cell.run_class,
            cell.earlier_record,
            cell.durable_copy,
            cell.later_outcome,
        )
        if include_probability:
            base = base + (cell.probability,)
        rows.append(base)
    return tuple(sorted(rows))


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fmt_distribution(distribution: Distribution) -> str:
    return (
        "{"
        + ", ".join(
            f"R={record}: {fmt_fraction(distribution[record])}"
            for record in sorted(distribution)
        )
        + "}"
    )


def fmt_cell(cell: Cell) -> str:
    return (
        f"{cell.run_class:5s}  R(t0)={cell.earlier_record}  "
        f"copy={cell.durable_copy}  L(t1)={cell.later_outcome:9s}  "
        f"P={fmt_fraction(cell.probability)}"
    )


def main() -> int:
    print("=" * 88)
    print("POSTSELECTION NO-SIGNALING AUDIT")
    print("  Test: conditional past probabilities are not same-run record edits.")
    print("=" * 88)
    print()

    table = joint_table()
    selected_raw = filter_outcome(table, SELECTED)
    discarded_raw = filter_outcome(table, DISCARDED)
    selected_conditioned = normalize(selected_raw)
    discarded_conditioned = normalize(discarded_raw)

    prior = record_marginal(table)
    selected_distribution = record_marginal(selected_conditioned)
    discarded_distribution = record_marginal(discarded_conditioned)
    p_selected = total_probability(selected_raw)
    p_discarded = total_probability(discarded_raw)
    recombined = weighted_recombine(
        p_selected,
        selected_distribution,
        p_discarded,
        discarded_distribution,
    )

    print("Joint table P(R(t0), L(t1)):")
    for cell in table:
        print(f"  {fmt_cell(cell)}")
    print()

    print("Earlier durable-record distribution:")
    print(f"  P(R(t0))                       = {fmt_distribution(prior)}")
    print(f"  P(L=selected | R=0)            = {fmt_fraction(selection_probability_given_record(table, 0))}")
    print(f"  P(L=selected | R=1)            = {fmt_fraction(selection_probability_given_record(table, 1))}")
    print()

    print("Postselected and discarded subensembles:")
    print(f"  P(L=selected)                  = {fmt_fraction(p_selected)}")
    print(f"  P(R(t0) | L=selected)          = {fmt_distribution(selected_distribution)}")
    print(f"  P(L=discarded)                 = {fmt_fraction(p_discarded)}")
    print(f"  P(R(t0) | L=discarded)         = {fmt_distribution(discarded_distribution)}")
    print(f"  weighted selected+discarded    = {fmt_distribution(recombined)}")
    print()

    check(
        "joint probability table is normalized",
        total_probability(table) == 1,
        f"total={fmt_fraction(total_probability(table))}",
    )
    check(
        "durable copy equals the earlier record in every run class",
        all(cell.durable_copy == cell.earlier_record for cell in table),
    )
    check(
        "later outcome is correlated with the earlier record",
        selection_probability_given_record(table, 1)
        > selection_probability_given_record(table, 0),
        (
            f"P(S|R=1)={fmt_fraction(selection_probability_given_record(table, 1))}, "
            f"P(S|R=0)={fmt_fraction(selection_probability_given_record(table, 0))}"
        ),
    )
    check(
        "selected conditional past distribution shifts",
        selected_distribution[1] == Fraction(4, 5)
        and selected_distribution[1] != prior[1],
        (
            f"P(R=1|S)={fmt_fraction(selected_distribution[1])}, "
            f"P(R=1)={fmt_fraction(prior[1])}"
        ),
    )
    check(
        "discarded conditional past distribution is the complementary filter",
        discarded_distribution[1] == Fraction(1, 5),
        f"P(R=1|D)={fmt_fraction(discarded_distribution[1])}",
    )
    check(
        "unconditioned earlier durable-record distribution is unchanged",
        recombined == prior,
        f"recombined={fmt_distribution(recombined)}",
    )
    check(
        "raw selected plus raw discarded run classes exactly reconstruct the table",
        table_signature(selected_raw + discarded_raw, include_probability=True)
        == table_signature(table, include_probability=True),
    )
    check(
        "conditioning preserves selected run-class record identities",
        table_signature(selected_raw, include_probability=False)
        == table_signature(selected_conditioned, include_probability=False),
    )
    check(
        "discarded run classes remain present and unedited",
        record_marginal(discarded_raw) == {0: Fraction(2, 5), 1: Fraction(1, 10)}
        and all(cell.durable_copy == cell.earlier_record for cell in discarded_raw),
        f"raw discarded marginal={fmt_distribution(record_marginal(discarded_raw))}",
    )

    classification = "conditional subensemble/final-boundary import"
    same_run_past_edit = "NO"
    operational_past_signal = "NO"

    print()
    print("CLASSIFICATION")
    print(f"  chronology label: {classification}")
    print(f"  same-run past record edit: {same_run_past_edit}")
    print(f"  operational past signaling: {operational_past_signal}")
    print()

    check(
        "postselection is classified as a conditional subensemble/final boundary",
        classification == "conditional subensemble/final-boundary import",
        f"classification={classification}",
    )
    check(
        "classification does not promote conditioning to past signaling",
        same_run_past_edit == "NO" and operational_past_signal == "NO",
        (
            f"same_run_past_edit={same_run_past_edit}, "
            f"operational_past_signal={operational_past_signal}"
        ),
    )

    print()
    print("SAFE READ")
    print("  - The later condition changes the accepted subensemble statistics.")
    print("  - The full, unconditioned earlier durable-record marginal is unchanged.")
    print("  - Discarded runs are filtered out of the report, not physically rewritten.")
    print(
        "  - If selected outcomes are imposed as a rule, that is final-boundary"
        " import, not a retained local past-signal channel."
    )
    print()
    print(f"PASS = {PASS}")
    print(f"FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
