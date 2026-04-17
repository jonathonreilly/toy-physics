#!/usr/bin/env python3
"""Render the current theory-facing next step for the non-unitary frontier.

This is a bounded architecture artifact, not a new experiment sweep. It turns
the latest unitary/non-unitary split into two concrete next-step objects:

1. a reduced phase-valley saturation law for the unitary/gravity side
2. a scalable environment-law proposal for replacing fixed-bin env closures
"""

from __future__ import annotations


def main() -> None:
    print("=" * 92)
    print("NON-UNITARY THEORY FRONTIER CARD")
    print("=" * 92)
    print()
    print("1. Phase-valley saturation law")
    print()
    print("Reduced model:")
    print(
        "  Split the detector-bound path sum into two coarse continuation valleys, "
        "v in {up, down}, with"
    )
    print(
        "    A_v(b) ~= W_v(b) * exp(i phi_v(b)) * exp(-sigma_v(b)^2 / 2)"
    )
    print(
        "  where phi_v is the valley-mean phase/action shift and sigma_v^2 is the "
        "packet-local action spread around each valley's amplitude peak."
    )
    print()
    print(
        "  If the signed field bias enters mainly through the valley means while the "
        "many near-degenerate paths inside each valley self-average, the coarse kick "
        "is controlled less by raw action contrast and more by the normalized valley "
        "bias:"
    )
    print()
    print(
        "    Q_sat(b) = |mu_up(b) - mu_down(b)| / sqrt(sigma_up(b)^2 + sigma_down(b)^2)"
    )
    print()
    print(
        "  with an effective threshold-like response"
    )
    print()
    print(
        "    Delta_k_y(b) ~= Delta_k_sat * tanh(C * Q_sat(b))"
    )
    print()
    print(
        "Interpretation: the raw field/action contrast can still vary with impact "
        "parameter, but once Q_sat is O(1) or larger, the path sum has already chosen "
        "a valley sign. Further growth in the raw contrast changes the kick weakly, "
        "so the response looks like a plateau or threshold instead of a clean power law."
    )
    print()
    print("Retained diagnostic observable:")
    print(
        "  valley saturation ratio"
    )
    print(
        "    Q_sat = signed valley-mean action gap / sqrt(packet-local sigma_up^2 + packet-local sigma_down^2)"
    )
    print(
        "  Unsaturated regime: Q_sat << 1  -> near-linear response"
    )
    print(
        "  Saturating regime: Q_sat >= 1   -> threshold/plateau kick"
    )
    print()
    print("2. Why fixed-bin environments wrong-scale")
    print()
    print(
        "  The growing-DAG sweeps now suggest one shared failure mode: branch-"
        "distinguishing structure gets projected back into a tiny common env label set."
    )
    print(
        "  In mechanism language, the upper and lower slit branches increasingly land "
        "on the same effective env support, so the partial trace stops separating them."
    )
    print()
    print("3. Scalable environment law candidates")
    print()
    print(
        "  Candidate A: multi-local region records"
    )
    print(
        "    E[path] = tensor product over local mass-region cells of small local "
        "records."
    )
    print(
        "    Why it may scale: branch overlap can shrink as more cells differ, instead "
        "of collapsing into one global bin."
    )
    print()
    print(
        "  Candidate B: edge/angle-sector records"
    )
    print(
        "    Each local cell records a coarse signed histogram of incoming/outgoing "
        "edge sectors."
    )
    print(
        "    Why it may scale: different branch geometries can stay distinguishable "
        "even when they hit the same node set."
    )
    print()
    print(
        "  Candidate C: path-history histogram / sequence records"
    )
    print(
        "    Each local region stores a short history sketch or count sketch of recent "
        "mass-region traversals."
    )
    print(
        "    Why it may scale: order information survives, so same-node reuse does not "
        "automatically collapse branches together."
    )
    print()
    print(
        "  Candidate D: genuinely continuous environment field"
    )
    print(
        "    Replace the finite-bin env label by a continuous local record variable "
        "coupled to traversal."
    )
    print(
        "    Why it may scale: branch overlap can decay smoothly with record distance "
        "instead of saturating at a tiny discrete alphabet."
    )
    print()
    print("4. Recommended next implementation target")
    print()
    print(
        "  Keep the unitary/path-sum core fixed and replace only the env law with a "
        "factorized local sector-record model."
    )
    print()
    print(
        "  Toy law:"
    )
    print(
        "    E[path] = tensor product over regions r of |h_r[path]>"
    )
    print(
        "    h_r[path] = coarse signed histogram of angle-sector or edge-sector visits"
    )
    print()
    print(
        "  Then branch overlap is no longer forced through one global bin:"
    )
    print()
    print(
        "    <E[a]|E[b]> ~= product over r of exp(-lambda * ||h_r[a] - h_r[b]||_1)"
    )
    print()
    print(
        "  This is the scaling property we want: if the two branches differ over more "
        "local regions as the graph grows, the env overlap stays small or shrinks, "
        "instead of washing out."
    )
    print()
    print("Bottom line:")
    print(
        "  The unitary core should stay fixed for now. The next theory move is to "
        "derive/measure Q_sat on the gravity side and replace finite-bin env labels "
        "with a local record law whose capacity grows with branch diversity."
    )


if __name__ == "__main__":
    main()
