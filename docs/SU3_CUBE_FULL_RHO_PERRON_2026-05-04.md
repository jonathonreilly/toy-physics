# SU(3) L_s=2 APBC Cube Full-ρ Perron Solve: APBC ≡ PBC Under Existing Implementation

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — closes the L_s=2 cube full-ρ Perron computation, unaudited.
**Primary runner:** `scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py`
**Load-bearing predecessor:** [`SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md)

## 0. Headline

This note evaluates the L_s=2 APBC cube full-ρ Perron computation under
the existing-runner implementation:

```text
P_cube(L_s=2 APBC, β=6, full-ρ NMAX=4..8) = 0.4291049969
```

This **matches PR #501 Block 5's candidate value exactly** (difference 4.7e-11) — confirming that under the existing implementation (which uses all-forward link convention at L_s=2 with no APBC-specific phase factors), **APBC and PBC are numerically equivalent** at L_s=2.

The gap to the bridge support upper candidate (`0.5935306800`) is
`0.164` = `543× ε_witness` — stable across the tested NMAX_rho values
from 3 to 8.

Two interpretations:

- **(a)** APBC ≡ PBC at L_s=2 numerically; framework's existing runner [`frontier_su3_cube_perron_solve.py`](scripts/frontier_su3_cube_perron_solve.py) blurs the distinction correctly. The campaign's L≥3 verdict stands.
- **(open)** APBC has phase factors (Z_3 center twists for non-self-conjugate sectors) that the existing runner does not implement. The implementation gap, not the geometry choice, is the actual missing piece.

## 1. What this PR delivers

### 1.1 Full candidate-ρ Perron solve

Per Block 5 (PR #501), the candidate ansatz at L_s=2 cube is:

```text
ρ_(p,q)(6) = (d_(p,q) × c_(p,q)(6) / c_(0,0)(6))^12 × d_(p,q)^(-16)
```

where the `d^(-16)` factor encodes the cube's index-graph topology (`N_components = 8` on 24 directed links, all-forward convention). This formula was verified by Block 5 to give the candidate value `0.4291049969` reported by the framework's existing index-graph open-gate runner.

This PR applies the FULL ρ (not just trivial sector as the existing `frontier_su3_cube_perron_solve.py` did) in the source-sector Perron solve:

```text
T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)
```

with `C_(Z_6^env) = diag(ρ_(p,q)(6))`.

### 1.2 NMAX_rho convergence

P(6) is **stable to 12 decimal places** across NMAX_rho = 3, 4, 5, 6, 7, 8:

```text
NMAX_rho =  3: P(6) = 0.429104996947
NMAX_rho =  4: P(6) = 0.429104996947
NMAX_rho =  5: P(6) = 0.429104996947
NMAX_rho =  6: P(6) = 0.429104996947
NMAX_rho =  7: P(6) = 0.429104996947
NMAX_rho =  8: P(6) = 0.429104996947
```

The Perron value is dominated by low-(p,q) contributions; high-(p,q) sectors are suppressed by `d^(-16)` and irrelevant.

### 1.3 Bridge comparison

| Quantity | Value |
|---|---:|
| `P_triv` (ρ = δ) | `0.4225317396` |
| `P_loc` (ρ = 1) | `0.4524071590` |
| **`P_cube` (full candidate-ρ, this PR)** | **`0.4291049969`** |
| Bridge support upper | `0.5935306800` |
| Gap to upper | `0.164426` |
| `ε_witness` | `3.030 × 10⁻⁴` |
| Gap factor | **`543× ε_witness`** |

The L_s=2 APBC cube under the existing implementation **does not close** the no-go witness scale.

## 2. APBC ≡ PBC under existing implementation

The framework's existing runner `frontier_su3_cube_perron_solve.py` is titled "L_s=2 APBC cube Perron solve" but its geometry encoder (Section B) uses 12 plaquettes / 24 links / all-forward convention — identical to L_s=2 PBC. PR #501 Block 5 verified the all-forward convention is consistent with the candidate ansatz `T_λ = d^(N_components - N_links)` with `N_components = 8`.

This PR computes the same ρ formula under the same convention and gets the same value. **APBC vs PBC distinction is not numerical at this implementation level**.

The framework's roadmap and staging gate explicitly say "L_s=2 APBC", suggesting APBC matters. Two possibilities:

1. The existing runner is correct: APBC at L_s=2 reduces to PBC under the all-forward convention, and the difference between APBC and PBC is conceptual (boundary identification language) but not numerical.
2. APBC has phase factors (Z_3 center twists for non-self-conjugate λ where character has non-trivial Z_3 charge) that the existing runner does not implement. These would modify ρ_(λ)(6) for `(p, q)` with `p ≠ q` mod 3.

**Resolution requires framework documentation** specifying the APBC implementation. Without it, the conservative reading is (1).

## 3. Theorem statement

**Bounded theorem (L_s=2 cube full-ρ Perron value).** Under the existing-runner all-forward convention, the L_s=2 APBC cube source-sector Perron solve with the FULL candidate-ansatz ρ_(p,q)(6) = (d c/c_(0,0))^12 × d^(-16) gives:

```text
P_cube(L_s=2, β=6) = 0.4291049969
```

stable to 12 decimal places across NMAX_rho ∈ {3, 4, 5, 6, 7, 8}, matching PR #501 Block 5's candidate value.

The gap to the bridge support upper candidate `0.5935306800` is `0.164` = `543× ε_witness`, structurally fixed at all NMAX_rho. The L_s=2 cube alone (under the existing implementation) cannot close the no-go witness scale.

## 4. Scope

### 4.1 In scope

- Full candidate-ρ Perron solve at L_s=2 cube, NMAX_rho ∈ {3..8}.
- Confirmation that the L_s=2 APBC label gives the SAME numerical value
  as the all-forward L_s=2 PBC candidate under the existing
  implementation.
- Identification of the open question: does APBC have unimplemented phase factors?

### 4.2 Out of scope

- APBC-specific phase-factor implementation (requires framework documentation).
- Larger blocks (L_s ≥ 3 APBC).
- Closure of the gauge-scalar bridge.

### 4.3 Not making the following claims

- Does NOT promote the bridge parent chain.
- Does NOT compute or constrain `<P>(β=6)` beyond confirming the L_s=2 cube candidate value.
- Does NOT prove APBC ≡ PBC at L_s=2 — only confirms the existing runner's implementation gives the same value.

## 5. Audit consequence

```yaml
claim_id: su3_cube_full_rho_perron_2026-05-04
note_path: docs/SU3_CUBE_FULL_RHO_PERRON_2026-05-04.md
runner_path: scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03
verdict_rationale_template: |
  Bounded support theorem: L_s=2 APBC cube full-candidate-ρ Perron
  solve gives P(6) = 0.4291049969, stable to 12 decimal places across
  NMAX_rho ∈ {3..8}. Matches PR #501 Block 5 candidate to 1e-11.

  Shows that under the existing implementation (all-forward convention,
  no APBC-specific phase factors), the L_s=2 APBC label is numerically
  equivalent to the all-forward L_s=2 PBC candidate.

  Gap to bridge support upper (0.5935) is 0.164 = 543× ε_witness,
  structurally fixed. L_s=2 cube alone does not close the no-go
  witness scale.

  Open question: does framework's APBC have Z_3 center-twist phase
  factors that the existing runner does not implement? Resolution
  requires framework documentation specifying APBC implementation.

  Does not promote bridge parent chain. No forbidden imports.
```

## 6. Cross-references

- Counterfactual context, not a load-bearing dependency:
  `SU3_BRIDGE_COUNTERFACTUAL_PASS_2026-05-04.md`.
- Block 5 (L_s=2 verdict):
  [`SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md).
- Existing cube Perron runner (trivial sector only): `scripts/frontier_su3_cube_perron_solve.py`.
- Native staging gate (where APBC is named): `docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`.

## 7. Command

```bash
python3 scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py
```

Expected runtime: ~15 seconds. Expected summary:

```text
SUMMARY: THEOREM PASS=1 SUPPORT=1 FAIL=0
```
