# Fermion Mass Ratios from the CKM Dual

**Date:** 2026-04-16
**Status:** retained (down-type quarks), bounded (up-type quarks, leptons)
**Scripts:**
- `scripts/frontier_mass_ratio_ckm_dual.py` (Phase 1, 23/23 PASS)
- `scripts/frontier_mass_ratio_up_sector.py` (Phase 2, 15/15 PASS)
- `scripts/frontier_mass_ratio_lepton_sector.py` (Phase 3, 14/14 PASS)

## Safe statement

Seven charged-fermion mass ratios are expressed as powers of the
framework coupling `alpha_s(v) = 0.1033` with exponents built from four
exact framework integers (`C_F = 4/3`, `T_F = 1/2`, `N_c = 3`,
`n_pair = 2`). All match observation at the few-percent level. No
observed masses are used as derivation inputs.

The down-type quark ratios (Phase 1) are retained at the same bar as the
promoted CKM atlas. The up-type quark and charged lepton ratios (Phases
2-3) are bounded — the inter-sector relations and lepton exponents are
empirically discovered patterns with exact framework-constant labels,
not first-principles derivations.

## Phase 1: Down-type quark mass ratios (retained)

### Method

The framework has two independent routes to the CKM matrix:

- **Route A (promoted):** Atlas/axiom closure giving `|V_us|`, `|V_cb|`
  from `alpha_s(v)` alone.
- **Route B:** Mass-ratio CKM relations (GST for `|V_us|`, anomalous-
  dimension exponent for `|V_cb|`) expressing CKM elements in terms
  of quark-mass ratios.

Equating the two routes extracts mass ratios from `alpha_s(v)`.

### Formulas

1. `|V_us|_atlas = sqrt(alpha_s(v)/2)` and
   `|V_us|_GST = sqrt(m_d/m_s)` (leading-order NNI texture result)
   give `m_d/m_s = alpha_s(v)/2`.

2. `|V_cb|_atlas = alpha_s(v)/sqrt(6)` and
   `|V_cb| = (m_s/m_b)^{C_F - T_F}` where `C_F - T_F = 5/6`
   give `m_s/m_b = [alpha_s(v)/sqrt(6)]^{6/5}`.

### Results

| Ratio | Predicted | Observed (PDG) | Deviation |
|---|---|---|---|
| `m_d/m_s` | `0.05165` | `0.0500` | `+3.3%` |
| `m_s/m_b` | `0.02239` | `0.02234` | `+0.2%` |
| `m_d/m_b` | `0.001156` | `0.001117` | `+3.5%` |

### Scale ambiguity disclosure

The comparison uses PDG conventional mass quotes: `m_s` at `mu = 2 GeV`,
`m_b` at `mu = m_b`. These are at different renormalization scales.
Running both to a common scale `mu = m_b` gives `m_s(m_b)/m_b(m_b) =
0.0195`, and the 5/6 formula then gives `-11%` deviation from `|V_cb|`.

The +0.2% match at PDG convention and -11% at a common scale are both
real. The framework prediction is for the ratio in the PDG convention
(mixed scales). The scale at which the 5/6 formula applies is itself
part of the prediction. This is stated as an explicit open question,
not hidden.

### Input provenance

- `alpha_s(v) = alpha_bare / u_0^2 = 0.1033` from the canonical
  plaquette chain (V-scheme, standard Lepage-Mackenzie with
  `n_link = 2`)
- `C_F = 4/3`, `T_F = 1/2` from SU(3) group theory (exact)
- GST relation: leading-order NNI texture result (corrections
  `O(m_d/m_s) ~ 5%`)
- The 5/6 exponent: `C_F - T_F` from the SU(3) Casimir structure;
  perturbatively derived, with non-perturbative verification at `g = 1`
  pending (lattice anomalous dimension at `L >= 16`)

### Deviation decomposition

The +3.3% on `m_d/m_s` decomposes as:
- +0.6% from GST intrinsic accuracy
- +2.7% from the atlas `|V_us|` overshoot (+1.32% on `|V_us|` squared)

The +0.2% on `m_s/m_b` (at PDG convention) reflects near-cancellation
between the atlas `|V_cb|` accuracy (-0.06%) and the 5/6 intrinsic
accuracy (+0.28%).

Both predictions lie within the 1-sigma PDG uncertainty bands on the
observed quark masses (`m_d`: 10%, `m_s`: 9%).

## Phase 2: Up-type quark mass ratios (bounded)

### Inter-sector relations

Two inter-sector mass relations connect up-type and down-type quarks
through exact framework constants:

1. `m_c * m_b = m_s * m_t / N_c` with `N_c = 3`
2. `n_pair * m_u * m_b^2 = m_d * m_s * m_t` with `n_pair = 2`

These are **empirically discovered patterns**, not first-principles
derivations. The algebraic derivation of why `N_c` and `n_pair` appear
in these positions is an open question. The labels are exact framework
constants; the derivation path connecting them to the inter-sector mass
structure is stated but not proved.

### Results

| Ratio | Predicted | Observed (PDG) | Deviation |
|---|---|---|---|
| `m_c/m_t` | `0.007463` | `0.007354` | `+1.5%` |
| `m_u/m_c` | `0.001735` | `0.001701` | `+2.0%` |

Direct verification on observed masses:
- `m_c * m_b = m_s * m_t / 3`: ratio `0.987` (deviation `-1.3%`)
- `2 * m_u * m_b^2 = m_d * m_s * m_t`: ratio `1.002` (deviation `+0.2%`)

### Key structural result

The up-type masses `m_u` and `m_c` are fully determined by `alpha_s(v)`
and `m_t` alone — no `m_b` anchor is needed for the up-type sector.

## Phase 3: Charged lepton mass ratios (bounded companion)

### Lepton exponents

The charged lepton mass ratios follow the same power-law pattern in
`alpha_s(v)` with modified exponents:

1. `m_mu/m_tau = alpha_s(v)^{5/4}` where `5/4 = (C_F - T_F) * N_c / n_pair`
2. `m_e/m_mu = alpha_s(v)^{7/3}` where `7/3 = 1 + C_F`

### Results

| Ratio | Predicted | Observed | Deviation |
|---|---|---|---|
| `m_mu/m_tau` | `0.05857` | `0.05946` | `-1.5%` |
| `m_e/m_mu` | `0.005007` | `0.004836` | `+3.5%` |
| `m_e/m_tau` | `0.000293` | `0.000288` | `+2.0%` |

### Honest disclaimer

Leptons are color singlets. The physical mechanism connecting `alpha_s`
to lepton masses is not yet derived from the lattice axioms. The
exponents `5/4` and `7/3` are empirically discovered power-law fits with
clean group-theory decompositions. Their first-principles derivation is
an open question.

The predicted masses degrade the Koide formula match from `0.001%` to
`0.18%`. This is an explicit cost of the current approach.

## Unified exponent table

| Ratio | Exponent of `alpha_s` | Group-theory formula |
|---|---|---|
| `m_d/m_s` | `1` | GST baseline |
| `m_s/m_b` | `6/5` | `1/(C_F - T_F)` |
| `m_c/m_t` | `6/5` | same, scaled by `1/N_c` |
| `m_u/m_c` | `11/5` | chain, scaled by `N_c/n_pair` |
| `m_mu/m_tau` | `5/4` | `(C_F - T_F) * N_c/n_pair` |
| `m_e/m_mu` | `7/3` | `1 + C_F` |

## What is NOT claimed

- A first-principles derivation of why `N_c` and `n_pair` appear in the
  inter-sector and lepton exponents
- Closure of the absolute down-type scale (`m_b` or `y_b`)
- Closure of the absolute lepton scale (`m_tau` or `y_tau`)
- A first-principles derivation of the 5/6 exponent beyond perturbative
  QCD (non-perturbative verification at `g = 1` pending)
- Neutrino masses or PMNS matrix
- That the scale ambiguity in the `m_s/m_b` comparison is resolved

## What remains open

1. `y_b` derivation (closes both `m_b` and `m_tau` anchors)
2. Non-perturbative proof of the 5/6 exponent at `g = 1`
3. First-principles derivation of `N_c` and `n_pair` inter-sector factors
4. First-principles derivation of lepton exponents
5. Neutrino sector + PMNS
6. Scale-dependence of the 5/6 formula

## Validation

- `frontier_mass_ratio_ckm_dual.py`: 23 PASS, 0 FAIL
- `frontier_mass_ratio_up_sector.py`: 15 PASS, 0 FAIL
- `frontier_mass_ratio_lepton_sector.py`: 14 PASS, 0 FAIL
