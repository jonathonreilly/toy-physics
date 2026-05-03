#!/usr/bin/env python3
"""Formal no-go for the gauge-scalar temporal observable bridge.

The runner constructs two completion witnesses that agree on A_min and on the
current retained Wilson plaquette packet, but give different local-response
readouts at beta=6.  That proves the retained packet does not entail the
observable-level bridge <P>_full = R_O(beta_eff).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import hashlib
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel  # noqa: E402
from frontier_gauge_vacuum_plaquette_mixed_cumulant_audit import beta_eff_beta5_coefficient  # noqa: E402
from frontier_scalar_3plus1_temporal_ratio import completion_ratio  # noqa: E402


NOTE = ROOT / "docs" / "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md"
STRETCH = ROOT / "docs" / "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md"

BETA = Fraction(6, 1)
C = Fraction(1, 10_000_000)

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


@dataclass(frozen=True)
class RetainedPacket:
    beta: Fraction
    g_bare: Fraction
    kernel_shape: str
    temporal_ratio_squared: Fraction
    beta5_onset: Fraction
    local_response_name: str
    retained_operator_packet: str

    def fingerprint(self) -> str:
        payload = "|".join(str(getattr(self, field)) for field in self.__dataclass_fields__)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CompletionWitness:
    name: str
    packet: RetainedPacket
    beta6_completion: Fraction

    @property
    def plaquette_readout(self) -> float:
        return plaquette_from_bessel(float(self.beta6_completion))[0]


def beta_eff_minus(beta: Fraction) -> Fraction:
    a = beta_eff_beta5_coefficient()
    return beta + a * beta**5


def beta_eff_plus(beta: Fraction) -> Fraction:
    return beta_eff_minus(beta) + C * beta**6


def invert_local_response(target: float, lo: float, hi: float, steps: int = 80) -> float:
    """Monotone bisection for R_O^{-1}(target) on a bracket."""
    left = lo
    right = hi
    for _ in range(steps):
        mid = 0.5 * (left + right)
        value = plaquette_from_bessel(mid)[0]
        if value < target:
            left = mid
        else:
            right = mid
    return 0.5 * (left + right)


def main() -> int:
    note_text = NOTE.read_text(encoding="utf-8")
    stretch_text = STRETCH.read_text(encoding="utf-8")

    ratio = completion_ratio()
    beta5 = beta_eff_beta5_coefficient()
    packet = RetainedPacket(
        beta=BETA,
        g_bare=Fraction(1, 1),
        kernel_shape="K_O(omega)=3w(3+sin^2 omega)",
        temporal_ratio_squared=Fraction(4, 3),
        beta5_onset=beta5,
        local_response_name="SU3 one-plaquette Bessel response",
        retained_operator_packet="transfer-character-recurrence+mixed-cumulant+underdetermination",
    )

    w_minus = CompletionWitness("minus", packet, beta_eff_minus(BETA))
    w_plus = CompletionWitness("plus", packet, beta_eff_plus(BETA))
    delta_beta = w_plus.beta6_completion - w_minus.beta6_completion
    p_minus = w_minus.plaquette_readout
    p_plus = w_plus.plaquette_readout
    delta_p = p_plus - p_minus

    sample_betas = [
        float(w_minus.beta6_completion)
        + i * (float(w_plus.beta6_completion - w_minus.beta6_completion) / 8.0)
        for i in range(9)
    ]
    sample_ps = [plaquette_from_bessel(beta)[0] for beta in sample_betas]
    monotone = all(a < b for a, b in zip(sample_ps, sample_ps[1:]))

    inv_minus = invert_local_response(p_minus, 6.0, 6.4)
    inv_plus = invert_local_response(p_plus, 6.0, 6.4)

    print("=" * 88)
    print("GAUGE-SCALAR TEMPORAL OBSERVABLE BRIDGE NO-GO")
    print("=" * 88)
    print()
    print("Retained packet")
    print(f"  beta                                  = {packet.beta}")
    print(f"  g_bare                                = {packet.g_bare}")
    print(f"  kernel shape                          = {packet.kernel_shape}")
    print(f"  A_inf/A_2                             = {ratio:.15f}")
    print(f"  beta^5 onset coefficient              = {packet.beta5_onset}")
    print(f"  retained-packet fingerprint           = {packet.fingerprint()}")
    print()
    print("Completion witnesses at beta=6")
    print(f"  beta_eff^-(6)                         = {float(w_minus.beta6_completion):.15f}")
    print(f"  beta_eff^+(6)                         = {float(w_plus.beta6_completion):.15f}")
    print(f"  exact delta beta_eff(6)               = {delta_beta} = {float(delta_beta):.15f}")
    print(f"  R_O(beta_eff^-(6))                    = {p_minus:.15f}")
    print(f"  R_O(beta_eff^+(6))                    = {p_plus:.15f}")
    print(f"  delta R_O                             = {delta_p:.15e}")
    print()

    check(
        "the theorem note declares no_go claim type",
        "**Type:** no_go" in note_text,
        detail="audit seeding can classify the new note as a no-go",
    )
    check(
        "the stretch note's A_min is preserved as the starting packet",
        "Wilson gauge action with" in stretch_text
        and "K_O(omega) = 3w(3 + sin^2 omega)" in note_text
        and "2/sqrt(3)" in note_text,
        detail="beta=6, local source shape, and temporal ratio are present",
    )
    check(
        "the scalar temporal completion ratio remains exactly 2/sqrt(3)",
        abs(ratio - (2.0 / math.sqrt(3.0))) < 1.0e-12,
        detail=f"A_inf/A_2={ratio:.15f}",
    )
    check(
        "the retained beta^5 onset coefficient is exactly 1/26244",
        beta5 == Fraction(1, 26244),
        detail=f"beta5={beta5}",
    )
    check(
        "both witnesses have the same retained primitive fingerprint",
        w_minus.packet.fingerprint() == w_plus.packet.fingerprint(),
        detail=w_minus.packet.fingerprint(),
    )
    check(
        "the witnesses agree through the retained beta^5 onset and differ first by c beta^6",
        delta_beta == C * BETA**6,
        detail=f"delta={delta_beta}",
    )
    check(
        "the local one-plaquette response is strictly increasing on the witness interval",
        monotone,
        detail=f"P interval=[{sample_ps[0]:.15f}, {sample_ps[-1]:.15f}]",
    )
    check(
        "equal retained packet but distinct completion witnesses give distinct BRIDGE readouts",
        delta_p > 1.0e-8,
        detail=f"delta R_O={delta_p:.15e}",
    )
    check(
        "a retained-packet derivation would assign one value, contradicting the two readouts",
        w_minus.packet == w_plus.packet and p_minus != p_plus,
        detail="logical non-entailment by two-model witness",
    )

    check(
        "defining beta_eff by R_O inverse recovers the witness coupling and is therefore tautological",
        abs(inv_minus - float(w_minus.beta6_completion)) < 1.0e-10
        and abs(inv_plus - float(w_plus.beta6_completion)) < 1.0e-10,
        detail=f"inverses=({inv_minus:.15f}, {inv_plus:.15f})",
        bucket="SUPPORT",
    )
    check(
        "the note names the exact objects that would escape the no-go",
        "exact beta-6 Wilson plaquette spectral measure" in note_text
        and "exact independently selected `beta_eff(6)`" in note_text,
        detail="escape hatches are explicit nonperturbative primitives, not fits",
        bucket="SUPPORT",
    )
    check(
        "the note preserves the forbidden-import firewall",
        "No fitted `beta_eff`" in note_text
        and "perturbative beta-function derivation" in note_text
        and "plaquette value remains forbidden" in note_text,
        detail="forbidden inputs appear only as exclusions",
        bucket="SUPPORT",
    )
    check(
        "the audit consequence retires the original open gate as retained_no_go",
        "closure: retained_no_go" in note_text
        and "positive_bridge_status: not_derived" in note_text,
        detail="negative closure, not positive bridge promotion",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
