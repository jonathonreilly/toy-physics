#!/usr/bin/env python3
"""Check the BAE-rename meta clarification note.

This runner is a review-hygiene check, not a physics proof. It verifies
that the rename note:
  - is classified as meta;
  - does not promote any audit row;
  - keeps the framework axiom set (A1, A2) unchanged;
  - introduces "BAE" / "Brannen Amplitude Equipartition" as the primary
    name and acknowledges legacy "A1-condition" alias;
  - cross-references all 18 campaign PRs (Routes F/E/A/D + Probes 1-7 +
    Synthesis + Probes 12-17);
  - establishes a forward-looking review-loop rule for future
    BAE-related branches.

Companion to:
  - docs/PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md
  - docs/C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md
  - docs/KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"

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
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    if not NOTE.exists():
        print(f"missing rename note: {NOTE}")
        return 1
    if not MINIMAL_AXIOMS.exists():
        print(f"missing minimal-axioms note: {MINIMAL_AXIOMS}")
        return 1

    note = NOTE.read_text()
    minimal = MINIMAL_AXIOMS.read_text()

    print("BAE-rename meta clarification check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("rename note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    check(
        "does not declare pipeline status",
        effective_token not in note and audit_clean_token not in note,
    )

    # ---- BAE name introduced ----
    check(
        "BAE name introduced as primary",
        "Brannen Amplitude Equipartition" in note and "BAE" in note,
    )
    check(
        "structural content stated (3a² = 6|b|²)",
        "3a²" in note and "6|b|²" in note,
    )

    # ---- Legacy alias acknowledged ----
    for legacy_alias in ["A1-condition", "Brannen-Rivero", "Frobenius equipartition"]:
        check(
            f"legacy alias acknowledged: '{legacy_alias}'",
            legacy_alias in note,
        )

    # ---- Naming collision documented ----
    check(
        "framework-A1 vs BAE collision documented",
        "framework axiom A1" in note and "Cl(3)" in note,
    )
    check(
        "Brannen-Rivero literature attribution present",
        "KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18" in note,
    )

    # ---- 18 campaign PRs cross-referenced ----
    expected_prs = [
        "#727", "#730", "#731", "#732",  # Routes F/E/A/D
        "#735", "#733", "#736", "#734",  # Probes 1-4
        "#738", "#737", "#740",          # Probes 5-7
        "#751",                          # 11-probe synthesis
        "#755", "#763", "#784",          # Probes 12-14
        "#788", "#789", "#787",          # Probes 15-17
    ]
    for pr in expected_prs:
        check(f"PR cross-reference: {pr}", pr in note)

    # ---- Review-loop rule ----
    check(
        "review-loop rule for future branches present",
        "Review-loop rule" in note,
    )
    check(
        "filename convention KOIDE_BAE_* established",
        "KOIDE_BAE_" in note,
    )

    # ---- File-immutability principle preserved ----
    check(
        "file-immutability for landed PRs preserved",
        "grandfathered" in note or "file immutability" in note.lower(),
    )

    # ---- Framework axioms unchanged ----
    check(
        "framework axioms A1+A2 declared unchanged",
        "remain the only mathematical axioms" in note
        or "axiom set" in note and "unchanged" in note.lower(),
    )
    check(
        "minimal-axioms note still has Cl(3) A1",
        "the physical local algebra is `Cl(3)`" in minimal,
    )
    check(
        "minimal-axioms note still has Z³ A2",
        "the physical spatial substrate is the cubic" in minimal,
    )

    # ---- No theorem promotion ----
    check(
        "rename does not promote any audit row",
        "does not promote" in note,
    )
    check(
        "rename does not modify retained theorems",
        "does not" in note and "retained theorem" in note,
    )

    # ---- Forward-only application ----
    check(
        "rename applies prospectively (forward-only)",
        "prospectively" in note or "forward" in note.lower(),
    )

    # ---- Structural-content layers acknowledged ----
    structural_layers = [
        "Brannen-Rivero original",
        "Frobenius level",
        "ℝ-isotype level",
        "Continuous-symmetry level",
    ]
    for layer in structural_layers:
        check(
            f"structural-content layer acknowledged: '{layer}'",
            layer in note,
        )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "BAE rename meta check passed: "
        "name 'A1-condition' renamed to 'Brannen Amplitude Equipartition (BAE)' "
        "going forward, framework axioms unchanged, "
        "file-immutability preserved for landed PRs, no theorem promotion."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
