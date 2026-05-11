#!/usr/bin/env python3
"""Runner for the Connes-Kreimer partial-sum RB bounded note."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    print("FAIL: sympy required for symbolic checks")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "CONNES_KREIMER_PARTIAL_SUM_RB_B4_EXTERNAL_BOUNDED_NOTE_2026-05-10.md"

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


def seq_mul(left, right):
    return tuple(a * b for a, b in zip(left, right))


def seq_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def strict_prefix(seq):
    out = []
    total = sp.Integer(0)
    for item in seq:
        out.append(total)
        total += item
    return tuple(out)


def seq_equal(left, right) -> bool:
    return len(left) == len(right) and all(
        sp.simplify(a - b) == 0 for a, b in zip(left, right)
    )


def make_binary_tree(depth):
    if depth == 0:
        return ("o",)
    child = make_binary_tree(depth - 1)
    return ("o", child, child)


def count_leaves(tree) -> int:
    if len(tree) == 1:
        return 1
    return count_leaves(tree[1]) + count_leaves(tree[2])


def count_nodes(tree) -> int:
    if len(tree) == 1:
        return 1
    return 1 + count_nodes(tree[1]) + count_nodes(tree[2])


def cut_count(depth: int) -> int:
    count = 1
    for _ in range(depth):
        count = (count + 1) ** 2
    return count


def main() -> int:
    print("=" * 76)
    print("CONNES-KREIMER PARTIAL-SUM RB B4 BOUNDED RUNNER")
    print("=" * 76)

    size = 8
    a = tuple(sp.Symbol(f"a{i}") for i in range(size))
    b = tuple(sp.Symbol(f"b{i}") for i in range(size))

    left = seq_mul(strict_prefix(a), strict_prefix(b))
    right = strict_prefix(
        seq_add(seq_add(seq_mul(strict_prefix(a), b), seq_mul(a, strict_prefix(b))), seq_mul(a, b))
    )
    check("strict prefix sum satisfies Rota-Baxter weight +1", seq_equal(left, right))

    wrong_weight = strict_prefix(
        seq_add(seq_add(seq_mul(strict_prefix(a), b), seq_mul(a, strict_prefix(b))), tuple(-x for x in seq_mul(a, b)))
    )
    check("strict prefix sum does not satisfy weight -1", not seq_equal(left, wrong_weight))

    check("strict prefix sum is not idempotent", not seq_equal(strict_prefix(a), strict_prefix(strict_prefix(a))))

    b4 = make_binary_tree(4)
    check("B4 has 16 leaves", count_leaves(b4) == 16)
    check("B4 has 31 nodes", count_nodes(b4) == 31)
    check("B4 has 30 edges", count_nodes(b4) - 1 == 30)
    check("B4 admissible-cut recursion gives 458329", cut_count(4) == 458329)

    alpha = sp.Symbol("alpha")
    prepared_first_slot = alpha ** 16
    regular_first_slot = prepared_first_slot - strict_prefix((prepared_first_slot, sp.Integer(0)))[0]
    check(
        "first regular slot reads the imported character value tautologically",
        sp.simplify(regular_first_slot - alpha ** 16) == 0,
    )

    if NOTE.exists():
        body = NOTE.read_text()
        forbidden = [
            "closes the hierarchy formula",
            "derives alpha_LM",
        ]
        bare_admission_labels = tuple("A" + str(index) for index in range(1, 5))
        check(
            "note avoids promotion language and bare admission labels",
            all(item not in body for item in forbidden)
            and all(label not in body for label in bare_admission_labels),
        )
    else:
        check("companion note exists", False, str(NOTE))

    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print("VERDICT: external bounded algebra only; no framework bridge")
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
