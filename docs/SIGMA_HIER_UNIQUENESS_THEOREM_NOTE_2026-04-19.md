# σ_hier Uniqueness Theorem

**Date:** 2026-04-19  
**Status:** **conditional support theorem on the open DM gate** — `σ_hier = (2, 1, 0)` is the
unique hierarchy-pairing permutation satisfying the joint 4-observable PMNS
constraint at the pinned chamber point  
**Runner:** `scripts/frontier_sigma_hier_uniqueness_theorem.py` ([scripts/frontier_sigma_hier_uniqueness_theorem.py](../scripts/frontier_sigma_hier_uniqueness_theorem.py))
**Runner result:** `PASS = 24, FAIL = 0`

## What this theorem establishes

At the pinned chamber point `(m_*, δ_*, q_+*) = (0.657061, 0.933806,
0.715042)` (retained by the P3 PMNS-as-f(H) map), the hierarchy pairing
`σ_hier = (2, 1, 0)` is the **unique** element of S_3 satisfying both:

1. **All 9** `|U_PMNS|_{ij}` entries inside the NuFit 5.3 NO 3σ experimental
   ranges.
2. **sin(δ_CP) < 0**, consistent with the T2K/NOvA experimental preference.

This is a conditional support theorem under the observational-promotion
framework. `σ_hier` is not derivable from the `Cl(3)/Z^3` axiom alone, but
the combined 4-observable PMNS constraint (3 angles + CP-phase sign) uniquely
selects it at the pinned chamber point.

## Proof structure

**Step 1 — Magnitude filter (9/9 NuFit check):**

The eigenvector matrix of H(m_*, δ_*, q_+*) has columns V[:,k] sorted
ascending by eigenvalue. For each of the 6 permutations σ ∈ S_3, the PMNS
matrix is P = V[σ, :]. Evaluating all 9 `|U_{ij}|` entries against the
NuFit 5.3 NO 3σ ranges gives:

| σ | NuFit passes | sin(δ_CP) | status |
|---|---:|---:|---|
| (0,1,2) | 4/9 | +0.966 | excluded (5 failures) |
| (0,2,1) | 4/9 | −0.966 | excluded (5 failures) |
| (1,0,2) | 5/9 | −1.000 | excluded (4 failures) |
| (1,2,0) | 5/9 | +1.000 | excluded (4 failures) |
| **(2,0,1)** | **9/9** | **+0.987** | magnitude passes |
| **(2,1,0)** | **9/9** | **−0.987** | magnitude passes |

The magnitude filter reduces S_3 from 6 to 2 admissible permutations.

**Step 2 — CP-phase discriminator:**

The two magnitude-passing permutations (2,0,1) and (2,1,0) differ by a
μ↔τ row swap. A row swap in the PMNS matrix preserves all `|U|` magnitudes
but reverses the sign of the Jarlskog invariant J, hence reversing
sin(δ_CP):

```
σ = (2,0,1):  sin(δ_CP) = +0.9874   (δ_CP ≈ +81°)
σ = (2,1,0):  sin(δ_CP) = −0.9874   (δ_CP ≈ −81°)
```

T2K (2021, Normal Ordering) measures δ_CP in the 1σ range [−200°, −15°]
(central ≈ −108°). NOvA similarly prefers sin(δ_CP) < 0. Both experiments
exclude sin(δ_CP) = +0.987 at ≥ 2σ. Therefore:

- σ = (2,0,1) is **experimentally disfavored** (sin(δ_CP) = +0.987, excluded
  at ≥ 2σ by T2K/NOvA).
- σ = (2,1,0) is **experimentally preferred** (sin(δ_CP) = −0.987, within
  T2K/NOvA 2σ preferred region).

## Theorem statement

**Theorem (σ_hier conditional uniqueness).** At the pinned chamber point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`:

> The unique element σ ∈ S_3 with (1) all 9 `|U_PMNS|_{ij}` inside the
> NuFit 5.3 NO 3σ ranges AND (2) sin(δ_CP) < 0, is σ = (2, 1, 0).

This is exact and verified by the dedicated runner.

## What this closes

The free `σ_hier` ambiguity at the pinned chamber point is resolved under
observational promotion:

- σ_hier was previously listed as an "independent conditional — an S_3
  involution (order 2), not derivable from the retained C_3 order-3 cycle."
- This theorem shows it has **no observational ambiguity**: no other σ ∈ S_3
  passes the joint 4-observable PMNS constraint.
- `σ_hier` is promoted from "free conditional" to "observationally unique at
  the live pin": uniquely selected by observation there, not internally
  derived from the framework alone.

## Consequence for the P3 flagship

With `σ_hier` resolved at the pinned point by this theorem:

- The P3 flagship closure (PMNS-as-f(H) map + chamber pin) depends on:
  1. The imposed branch-choice rule **A-BCC** (physical sheet = `C_base`)
  2. ~~σ_hier = (2,1,0) as an independent conditional~~ → **now closed by
     observational uniqueness at the live pin**
- **A-BCC remains the single named source-side open input on the pinned
  chamber packet.** Broader chamber-wide / all-basin uniqueness is not
  supplied by this theorem.

## Falsifiable prediction

The CP-phase prediction sin(δ_CP) = −0.9874 is a forced geometric
consequence of the uniquely selected σ_hier. It is not a separately imposed
input.

A confirmed >3σ measurement of sin(δ_CP) > +0.5 at DUNE / Hyper-Kamiokande
would falsify the P3 closure (ruling out the only physically consistent
chamber pin under the 4-observable PMNS constraint).

## What this theorem does NOT claim

- Does not derive σ_hier from Cl(3)/Z^3 alone (the C_3 generator cannot
  distinguish S_3 involutions from cyclic elements).
- Does not close A-BCC (the physical-sheet identification is treated
  separately; see `ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md`).
- Does not pin the absolute neutrino mass scale (different carrier).
- Does not determine the solar gap Δm²_21 (different carrier).
- Does not claim chamber-wide or all-basin uniqueness. Other `H`-parameter
  basins, including the documented Basin N neighborhood, may still support
  other internally consistent PMNS fits. A chamber-wide uniqueness statement
  would require a separate basin analysis.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_sigma_hier_uniqueness_theorem.py
```

Expected: `PASS = 24, FAIL = 0`.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [abcc_cp_phase_no_go_theorem_note_2026-04-19](ABCC_CP_PHASE_NO_GO_THEOREM_NOTE_2026-04-19.md)
- [dm_sigma_hier_closure_packet_note_2026-04-20](DM_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md)
- [neutrino_dirac_pmns_retained_lane_packet_2026-04-16](NEUTRINO_DIRAC_PMNS_RETAINED_LANE_PACKET_2026-04-16.md)
