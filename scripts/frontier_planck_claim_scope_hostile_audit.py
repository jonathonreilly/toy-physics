#!/usr/bin/env python3
"""Hostile claim-scope scanner for the canonical Planck theorem packet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs/PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md"
AUDIT_DOC = ROOT / "docs/PLANCK_SCALE_CLAIM_SCOPE_HOSTILE_AUDIT_2026-04-23.md"


CLAIM_VERB_RE = re.compile(
    r"\b("
    r"derive[sd]?|derivation|force[sd]?|prove[sd]?|proof|determine[sd]?|"
    r"fixe[sd]?|close[sd]?|give[sn]?"
    r")\b"
)
PLANCK_TARGET_RE = re.compile(
    r"\bplanck\b|a\s*=\s*l\s*[_ -]?\s*p|a\^2\s*=\s*l\s*[_ -]?\s*p\^2"
)
CLZ_RE = re.compile(
    r"cl\s*\(\s*3\s*\)\s*(?:/|on|x|times)?\s*z\s*(?:\^|\*\*)?\s*3"
)
INSUFFICIENT_SURFACE_RE = re.compile(
    r"("
    r"(?:bare\s+)?cl\s*\(\s*3\s*\)\s*(?:/|on|x|times)?\s*z\s*(?:\^|\*\*)?\s*3|"
    r"(?:older\s+|front-door\s+)?minimal\s+(?:ledger|package|stack|surface)|"
    r"bare\s+(?:ledger|package|surface)"
    r")"
    r".{0,90}\b(alone|by itself|in isolation)\b"
    r"|"
    r"\b(alone|by itself|in isolation)\b"
    r".{0,90}"
    r"("
    r"(?:bare\s+)?cl\s*\(\s*3\s*\)\s*(?:/|on|x|times)?\s*z\s*(?:\^|\*\*)?\s*3|"
    r"(?:older\s+|front-door\s+)?minimal\s+(?:ledger|package|stack|surface)|"
    r"bare\s+(?:ledger|package|surface)"
    r")"
)
REQUIRED_SCOPE_RE = re.compile(
    r"axiom extension p1|one-axiom|source-free|locality surface|"
    r"gravitational area/action|area/action normalization|authorized surface|"
    r"authorized physical-lattice package surface|standard gravitational"
)
DROP_REQUIRED_RE = re.compile(
    r"\b(without|drop|dropped|dropping|omit|omitted|remove|removed|no)\b"
    r".{0,80}"
    r"(axiom extension p1|\bp1\b|one-axiom|source-free state law|"
    r"gravitational area/action|area/action normalization)"
)
PROTECTIVE_RE = re.compile(
    r"does not claim|not claim|not claimed|cannot claim|should avoid|"
    r"avoid the stronger|unsafe claim|should not say|not defensible|"
    r"not yet|not already|overclaim|stronger unqualified sentence|"
    r"what this does not claim|non-claim|warning"
)


@dataclass(frozen=True)
class Paragraph:
    line: int
    text: str


@dataclass(frozen=True)
class Finding:
    rule: str
    line: int
    text: str
    reason: str


def normalize(text: str) -> str:
    cleaned = text.lower()
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("*", "")
    cleaned = cleaned.replace("\u00d7", "x")
    cleaned = cleaned.replace("\\times", "times")
    cleaned = cleaned.replace("z\u00b3", "z^3")
    cleaned = cleaned.replace("l\u209a", "l_p")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def paragraphs(text: str) -> list[Paragraph]:
    out: list[Paragraph] = []
    buf: list[str] = []
    start_line = 1

    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.strip():
            if not buf:
                start_line = lineno
            buf.append(line.rstrip())
        elif buf:
            out.append(Paragraph(start_line, "\n".join(buf)))
            buf = []

    if buf:
        out.append(Paragraph(start_line, "\n".join(buf)))

    return out


def has_claim_target(norm: str) -> bool:
    return bool(CLAIM_VERB_RE.search(norm) and PLANCK_TARGET_RE.search(norm))


def is_protected(current: str, previous: str) -> bool:
    context = f"{previous} {current}"
    return bool(PROTECTIVE_RE.search(context))


def scan_packet_text(text: str) -> list[Finding]:
    paras = paragraphs(text)
    findings: list[Finding] = []

    for idx, para in enumerate(paras):
        norm = normalize(para.text)
        prev = normalize(paras[idx - 1].text) if idx > 0 else ""
        protected = is_protected(norm, prev)

        if protected:
            continue

        if has_claim_target(norm) and INSUFFICIENT_SURFACE_RE.search(norm):
            findings.append(
                Finding(
                    "insufficient-surface-alone",
                    para.line,
                    para.text,
                    "Planck derivation language is attached to bare/minimal surface language plus 'alone/by itself/in isolation'.",
                )
            )

        if (
            has_claim_target(norm)
            and CLZ_RE.search(norm)
            and not REQUIRED_SCOPE_RE.search(norm)
        ):
            findings.append(
                Finding(
                    "unscoped-cl3-z3-planck-claim",
                    para.line,
                    para.text,
                    "A Cl(3)/Z^3 Planck claim lacks P1/source-free/area-action scope markers.",
                )
            )

        if PLANCK_TARGET_RE.search(norm) and DROP_REQUIRED_RE.search(norm):
            findings.append(
                Finding(
                    "drops-load-bearing-scope",
                    para.line,
                    para.text,
                    "The paragraph keeps the Planck target while dropping P1, source-free state law, or gravitational area/action normalization.",
                )
            )

    return findings


def expect(name: str, cond: bool, detail: str = "") -> int:
    suffix = f" -- {detail}" if detail else ""
    if cond:
        print(f"PASS: {name}{suffix}")
        return 1
    print(f"FAIL: {name}{suffix}")
    return 0


def fixture_checks() -> tuple[int, int]:
    fixtures = [
        (
            "catches-bare-cl3-z3-alone-forces-planck",
            "Bare Cl(3)/Z^3 alone forces a = l_P.",
            True,
        ),
        (
            "catches-older-minimal-ledger-alone",
            "Planck is already derived by the older minimal ledger alone.",
            True,
        ),
        (
            "catches-dropped-p1",
            "The direct route proves a = l_P without Axiom Extension P1.",
            True,
        ),
        (
            "catches-dropped-area-action",
            "The route derives a = l_P after dropping the gravitational area/action normalization.",
            True,
        ),
        (
            "allows-current-scoped-claim",
            "Planck is derived natively on the physical Cl(3) / Z^3 package plus the explicit Axiom Extension P1 source-free local state law and the standard gravitational area/action normalization.",
            False,
        ),
        (
            "allows-protected-unsafe-example",
            "The branch should avoid the stronger unqualified sentence:\n\n> Planck is already derived by the older minimal ledger alone.",
            False,
        ),
    ]

    passed = 0
    total = 0
    for name, text, should_flag in fixtures:
        total += 1
        findings = scan_packet_text(text)
        passed += expect(
            name,
            bool(findings) is should_flag,
            f"findings={len(findings)}",
        )
    return passed, total


def packet_scope_checks(packet: str, audit_doc: str) -> tuple[int, int]:
    passed = 0
    total = 0

    total += 1
    passed += expect(
        "packet-declares-authorized-surface",
        "## Authorized surface" in packet
        and "Axiom Extension P1" in packet
        and "one-axiom information / Hilbert / locality surface" in packet,
    )

    total += 1
    passed += expect(
        "packet-keeps-minimal-ledger-denial",
        "not claimed on the older minimal ledger in isolation" in packet,
    )

    total += 1
    passed += expect(
        "packet-keeps-area-action-load-bearing",
        "standard gravitational area/action normalization" in packet
        and "area/action normalization can be dropped" in packet
        and "does not claim" in packet,
    )

    total += 1
    passed += expect(
        "packet-has-reviewer-safe-scoped-sentence",
        "physical `Cl(3)` / `Z^3` package plus the" in packet
        and "explicit Axiom Extension P1 source-free local state law" in packet
        and "standard gravitational area/action normalization" in packet,
    )

    total += 1
    passed += expect(
        "audit-doc-documents-can-and-cannot-claim",
        "### Can claim" in audit_doc
        and "### Cannot claim" in audit_doc
        and "bare `Cl(3)` / `Z^3` alone" in audit_doc
        and "standard gravitational area/action normalization" in audit_doc,
    )

    findings = scan_packet_text(packet)
    total += 1
    if findings:
        for finding in findings:
            print(f"FINDING: {finding.rule} line {finding.line}")
            print(f"  reason: {finding.reason}")
            print(f"  text: {finding.text}")
    passed += expect(
        "canonical-packet-has-no-unprotected-overclaims",
        not findings,
        f"findings={len(findings)}",
    )

    return passed, total


def main() -> int:
    packet = PACKET.read_text(encoding="utf-8")
    audit_doc = AUDIT_DOC.read_text(encoding="utf-8")

    print("Planck claim-scope hostile audit")
    print("=" * 78)
    print(f"Target: {PACKET.relative_to(ROOT)}")
    print()

    passed = 0
    total = 0

    fixture_passed, fixture_total = fixture_checks()
    passed += fixture_passed
    total += fixture_total

    print()
    packet_passed, packet_total = packet_scope_checks(packet, audit_doc)
    passed += packet_passed
    total += packet_total

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
