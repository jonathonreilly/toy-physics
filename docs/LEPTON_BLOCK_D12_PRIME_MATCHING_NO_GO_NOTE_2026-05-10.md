# Lepton Block D12-Prime Matching - Physical-Operator Open Gate

**Date:** 2026-05-10
**Claim type:** open_gate
**Status:** source-note proposal; independent audit owns audit verdict and
pipeline-derived effective status.
**Scope:** current-surface YT-style matching attempt on the lepton `(2,1)`
block.
**Primary runner:** [`scripts/frontier_lepton_block_d12_prime_matching.py`](../scripts/frontier_lepton_block_d12_prime_matching.py)
**Cache:** [`logs/runner-cache/frontier_lepton_block_d12_prime_matching.txt`](../logs/runner-cache/frontier_lepton_block_d12_prime_matching.txt)

## Claim

The YT-style matching argument cannot be reused as a lepton-block Ward
identity on the current source surface unless an additional physical-operator
bridge is supplied.

The reason is narrow. In the quark YT chain, the two sides of the matching
refer to the same composite scalar operator. The relevant source notes define
that scalar through a color-indexed quark bilinear:

- [`YUKAWA_COLOR_PROJECTION_THEOREM.md`](YUKAWA_COLOR_PROJECTION_THEOREM.md)
- [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)

The lepton-block analogy can formally write a hypercharge exchange equation
and, if a unit lepton scalar matrix element is supplied, it algebraically
solves `y_tau = g_1/sqrt(2)`. That formal algebra is not a framework
identity unless the supplied lepton scalar is shown to be the same physical
operator as the scalar used in the matching. The current cited sources do not
provide that bridge.

## Boundary

This note does not use empirical lepton masses, does not predict a lepton
Yukawa, and does not close or permanently rule out Lane 6. It only records a
current-surface gate:

> A YT-style lepton matching needs a theorem identifying a physical lepton
> composite/operator surface, not just a formal unit tensor on the lepton
> block.

Companion branch proposals about lepton tensors or tree-level exchange are
not load-bearing for this landing. If they are later retained by audit, this
gate should be rechecked against those retained inputs.

## Runner Checks

The paired runner verifies:

- the quark YT matching algebra gives `y_t = g_s/sqrt(6)`;
- the formal lepton hypercharge analogy would give `y_tau = g_1/sqrt(2)`
  if a unit lepton scalar operator were supplied;
- the cited YUKAWA source defines the scalar with a color-indexed quark
  bilinear;
- the current cited source text does not define a lepton-composite scalar
  bridge;
- the result remains an open gate, not a retained-grade no-go or mass
  prediction.
