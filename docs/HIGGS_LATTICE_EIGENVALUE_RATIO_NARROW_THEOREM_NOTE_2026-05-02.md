# Higgs Lattice Eigenvalue Ratio (Mean-Field) — Narrow Theorem

**Date:** 2026-05-02
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_higgs_lattice_eigenvalue_ratio_narrow.py`

## Claim scope (proposed)

> **Given** the retained graph-first SU(3) gauge surface
> (`graph_first_su3_integration_note`, `retained_bounded`), the
> Wilson canonical convention `g_bare = 1` (admitted; cycle 6 narrow
> theorem), and the Cl(3) Clifford identity `D_taste² = d · I` at
> mean-field factorization with `N_taste = 16` taste eigenvalues, the
> dimensionless lattice generating-functional curvature ratio is
> ```
> R_lattice  ≡  4 / (u_0² · N_taste)  =  1 / (4 u_0²)         at N_taste = 16
> ```
> where `u_0` is the mean-link parameter.

The narrow theorem **explicitly does NOT** claim:

- that `R_lattice` equals the physical ratio `(m_H / v)²` (this is a
  separate physical-matching identification, class (F), and is the
  parent's blocked load-bearing step);
- the value of `u_0` (admitted external lattice mean-field input);
- the full Higgs mass derivation `m_H = v / (2 u_0)`;
- a Standard Model Higgs-mass prediction.

The result is a **pure lattice-side algebraic identity**: the curvature
of the Clifford-Dirac generating functional at mean-field. The physical-
side identification with `(m_H / v)²` is the renaming step the parent's
audit verdict flagged and is excluded here.

## Retained / admitted dependencies (one-hop)

| Authority | Effective status | Role |
|---|---|---|
| `graph_first_su3_integration_note` | retained_bounded | provides SU(N_c=3) gauge structure on Z³ taste surface |
| `g_bare = 1` Wilson canonical convention | admitted (cycle 6 narrow, PR #301) | β = 2 N_c / g_bare² = 6 |
| Cl(3) Clifford identity `D_taste² = d · I` | admitted standard staggered fermion algebra | gives `|λ_k| = sqrt(d) = 2` (in lattice units, d=4) per taste |
| Mean-field factorization `U_{ab} → u_0 δ_{ab}` | admitted standard mean-field convention | scales eigenvalues by `u_0` |

The mean-field factorization is admitted as a standard lattice-gauge
mean-field convention; the result is bounded (conditional) on this
admission.

## Load-bearing step (class A)

```text
Cl(3)/Z^4 APBC minimal block (L = 2):
  N_sites = 2^4 = 16  =  N_taste                                (admitted: minimal block size)
  N_c = 3                                                       (retained: graph_first_su3)
  N_tot = N_c × N_sites = 48                                    (algebraic)

Clifford identity D_taste² = d · I  (admitted standard staggered algebra):
  taste eigenvalues: |λ_k| = sqrt(d) = 2 (in lattice units, d=4 spacetime)

Mean-field factorization U_{ab} → u_0 δ_{ab}  (admitted):
  full eigenvalues: |λ_k|_full = 2 u_0
  pure imaginary (staggered anti-Hermiticity): λ_k = ± 2 i u_0

Generating functional at mean field:
  W(J) = sum_{k=1}^{N_tot} (1/2) log(J² + 4 u_0²)
       = (N_tot / 2) · log(J² + 4 u_0²)

Curvature:
  d²W/dJ² |_{J=0} = N_tot · (1 / (2 u_0²)) · (1 / 2)
                 = N_tot · (1 / (4 u_0²))

Per-taste curvature:
  d²W/dJ² |_{J=0} / N_tot = 1 / (4 u_0²)

Scaled dimensionless ratio:
  R_lattice  ≡  4 / (u_0² · N_taste)
             =  4 / (u_0² · 16)
             =  1 / (4 u_0²)

This matches the per-taste curvature; the ratio R_lattice is an
algebraic combination of admitted mean-field inputs.
```

This is class (A) — algebraic identity from admitted mean-field inputs.
No physical-side identification, no fitted value.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_higgs_lattice_eigenvalue_ratio_narrow.py
```

Verifies, at exact rational precision via Python `Fraction`:

1. `N_tot = N_c × N_sites = 48` from `(N_c, N_sites) = (3, 16)`.
2. Clifford-identity eigenvalue magnitude `2 u_0` (from `D_taste² = d·I` with `d = 4`).
3. Generating functional `W(J)` curvature at mean field.
4. `R_lattice = 4 / (u_0² · 16) = 1 / (4 u_0²)` algebraic identity.
5. Cited authorities (`graph_first_su3_integration_note`,
   cycle-6 g_bare convention) verified retained-grade via live ledger
   lookup.
6. Scope discipline: the physical identification `R_lattice = (m_H/v)²`
   is **not** in the load-bearing chain.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  Pure lattice-side algebraic identity at mean-field on Cl(3)/Z^4 APBC:
  R_lattice = 4/(u_0² N_taste) with N_taste = 16 gives R_lattice = 1/(4 u_0²).
  NO physical Higgs mass identification, NO m_H = v/(2 u_0) claim.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

If ratified, `effective_status = retained_bounded` (bounded_theorem +
audited_clean + retained_bounded dep + admitted mean-field convention).

## What this theorem closes

The lattice-side algebraic content of the parent
`HIGGS_MASS_FROM_AXIOM_NOTE`'s derivation, freed from the conditional
physical-matching identification (which is class (F) and was the parent's
blocking step). The narrow theorem provides a clean retained-bounded
primitive for the lattice-side curvature that downstream rows can cite.

## What this theorem does NOT close

- The physical identification `R_lattice = (m_H/v)²` (separate downstream
  matching theorem; remains in the lattice→physical matching cluster
  obstruction, see prior campaign cycle 13 PR #274).
- The Higgs mass prediction `m_H = v/(2 u_0)` (separate full theorem).
- The value of `u_0` (admitted external lattice input).

## Cross-references

- `HIGGS_MASS_FROM_AXIOM_NOTE.md` — parent (`audit_status: audited_conditional`,
  td=296); this narrow theorem keeps only the lattice-side algebra clean.
- `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` — cycle 6
  sister narrow theorem (PR #301).
- `graph_first_su3_integration_note` — retained_bounded dep.
- Cycles 1-5 (PRs #292, #293, #294, #297, #299) — sister narrow theorems
  / synthesis on different lanes.
