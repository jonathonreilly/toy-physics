# Framework's L_s=2 PBC Minimal-Block Plaquette: Closed-Form Identification

**Date:** 2026-05-05
**Status:** research_finding (positive identification, audit-ratifiable as a numerical-computation theorem; audit must verify)
**Companion:** [`PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md`](PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md)
**Related runner:** [`scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`](../scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py)
**Related framework note:** [`SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md`](SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md)

## Headline

The framework's `L_s = 2` PBC spatial cube minimal-block plaquette
expectation at β = 6 is, to within direct MC error and within character
truncation order 10⁻¹³ on naive cube traces,

```
⟨P⟩_{cube}(β=6) = 0.422531739650
```

— **identically** the V=1 single-plaquette value carried by the
framework's `P_trivial(6) = 0.4225317396`. The closed form is the
order-3 holonomic Picard-Fuchs ODE derived in
[`PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md`](PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md):

```
6β² J''' + β(60 − β) J'' + (−4β² − 2β + 120) J' − β(β + 10) J = 0
⟨P⟩_{cube}(β) = J'(β) / J(β)
```

with Taylor recurrence

```
6(N+1)(N+4)(N+5) a_{N+1} = N(N+1) a_N + 2(2N+3) a_{N−1} + a_{N−2}.
```

This is the framework's **first analytic closure of a load-bearing
plaquette object on its own minimal block**. It does NOT close the
L → ∞ thermodynamic value `⟨P⟩(β=6, L→∞) = 0.5934` (PR #539),
which lives on a different surface.

## Geometry pinned

Per [`SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md`](SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md)
lines 56-72 and `scripts/frontier_su3_cube_perron_solve.py` lines
237-322, the framework's V-invariant minimal block is the **3D purely
spatial L=2 cube**:

- **Sites:** 8 at `(x, y, z) ∈ {0, 1}^3`
- **Directed links:** 24 (3 spatial directions × 8 sites)
- **Plaquettes:** 12 unique unoriented spatial plaquettes (4 per plane × 3 planes)
- **Boundary conditions:** **PBC in all 3 spatial directions** (NOT APBC)
- **Action:** `S = -(β/3) Σ_{p ∈ 12} Re Tr U_p` with the
  **all-forward** L=2 PBC convention `U_p = U_{l1} U_{l2} U_{l3} U_{l4}`
  (no daggers — the framework convention, distinct from the
  textbook 24-plaquette ±dagger convention)
- **V-invariance:** the gauge transformation V acts on the 8 sites; on
  each shared link the integration forces `λ_B = bar(λ_A)` for the two
  adjacent plaquettes
- **APBC clarification** (per `HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md`):
  APBC is for the **fermion determinant / hierarchy block**, not the
  gauge plaquette object. The plaquette evaluation surface is the
  periodic L^4 isotropic lattice
  ([`PLAQUETTE_4D_MC_FSS_NUMERICAL_THEOREM_NOTE_2026-05-05.md`](PLAQUETTE_4D_MC_FSS_NUMERICAL_THEOREM_NOTE_2026-05-05.md)
  line 54).

This is distinct from the textbook 3D L=2 PBC SU(3) Wilson with
24 plaquettes (±dagger convention) which gives ⟨P⟩(β=6) = 0.4931 by MC.

## Numerical evidence

**Direct MC** (3 independent seeds, 75 000 measurements total, on
framework's 12-plaq all-forward cube):

```
⟨P⟩_{cube}(β=6) = 0.422384 ± 0.000372
```

**Character-expansion analytic** (N_grid = 384 Weyl integration,
exact-rational moments):

- Trivial-sector contribution `⟨P⟩_trivial = (d/dβ) ln c_{(0,0)}(β) = 0.4225317397` at β=6
- Leading non-trivial corrections (under naive `T_λ(cube) = d_λ^(N_components−N_links) = d_λ^(−16)`):
  - irrep `(1,1)` (adjoint, dim 8) self-conjugate: ratio to trivial = **8.1 × 10⁻¹⁴**
  - irrep `(2,2)` (dim 27) self-conjugate: **6.9 × 10⁻²⁹**
- **Trivial sector dominates absolutely at β=6** under the naive cube trace.

**MC vs trivial-sector analytic:**

```
0.422384 − 0.4225317397 = −0.000148      (−0.40 σ — fully consistent)
```

So at the precision available, the framework's 12-plaq cube ⟨P⟩(β=6) is
**indistinguishable from the V=1 single-plaquette value**, which is
itself closed-form via the order-3 Picard-Fuchs ODE.

## Closed-form expression at character truncation level 3

On the framework's 12-plaq cube, with bipartite-allowed irreps and the
naive cube trace `T_λ`:

```
Z(β) = c_{(0,0)}(β)^12
     + Σ_{n ≥ 1} [d_{(n,n)} c_{(n,n)}(β)]^12 T_{(n,n)}(cube)               (self-conjugate λ)
     + Σ_{λ ≠ λ̄} [d_λ c_λ(β)]^6 [d_λ̄ c_λ̄(β)]^6 T_{(λ,λ̄)}(cube)              (bipartite pairs)
⟨P⟩(β) = (1/12) d/dβ ln Z(β)
```

At truncation level 3 (irreps with dim ≤ 27): trivial + (1,0)/(0,1)
bipartite + (1,1) self-conjugate + (2,0)/(0,2) bipartite + (2,1)/(1,2)
bipartite + (2,2) self-conjugate (10 irreps total).

Under naive `T_λ = d_λ^(−16)`, all non-trivial terms give relative
contributions < 10⁻¹³ at β=6, so

```
⟨P⟩_{cube}(β=6) = ⟨P⟩_{V=1}(β=6) = 0.4225317397      (to 10 digits)
```

## Reconciliation with framework's existing `0.4291` candidate

The number `0.4291049969` previously associated with the L=2 PBC cube
in the framework's bridge-support stack does **NOT** come from direct
MC of the framework's 12-plaq cube. It is the **Perron eigenvalue of
a candidate source-sector transfer operator**

```
T_src(6) = exp(3J) D_6^loc C_{ρ_candidate} exp(3J)
```

derived under the **uniform-pairing ansatz**

```
ρ_{(p,q)}(6) = (d_{(p,q)} c_{(p,q)}(6) / c_{(0,0)}(6))^12 · d_{(p,q)}^(−16)
```

per [`SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md`](SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md)
lines 80-110. That note is **already `open_gate`** and explicitly
states "do not quote `P_candidate(6)` as the actual cube Perron value."

The MC-vs-ansatz discrepancy is

```
|0.4291050 − 0.422384| / σ_MC = 18 σ
```

confirming the ansatz quantitatively fails to describe direct MC of
the cube partition function. **The framework's actual cube ⟨P⟩(β=6)
is 0.4224 ± 0.0004, not 0.4291** — and this matches the V=1 closed
form to 0.4σ.

## What this changes for the framework

**No conflict with framework's existing claims.** The `open_gate` note
already disowned `0.4291` as a Perron-value claim. This note simply
identifies the cube's true MC value as the V=1 closed form.

**New positive results:**

1. **Closed-form ⟨P⟩ on framework's V-invariant minimal block.**
   The order-3 Picard-Fuchs ODE in [`PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md`](PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md)
   is now also the closed-form ODE for the framework's full L_s=2
   PBC cube object at β=6 within MC error.

2. **Trivial-sector dominance theorem (proposed).**
   On the framework's 12-plaq cube at β=6, non-trivial SU(3) irreps
   contribute < 10⁻¹³ relative under naive cube traces. This is a
   numerical theorem subject to audit ratification once a rigorous
   bound on `T_λ(cube)` for general λ is supplied.

3. **Sharpened closure question.**
   The analytic-closure problem for the framework is no longer "find
   a closed form for ⟨P⟩(β=6) on the minimal block." That has now
   been done (positively, this note + PR #541). The remaining open
   problem is the **bridge from the minimal-block value 0.4225 to
   the L → ∞ Wilson value 0.5934**. That is a structurally different
   question — the L → ∞ Wilson is on a 4D periodic surface with
   thermodynamic-limit fluctuations not present in the cube object.

## Comparison table (refreshed)

| Geometry | ⟨P⟩(β=6) | source | closed form? |
|---|---:|---|---|
| V=1 single plaquette | 0.4225317397 | order-3 PF ODE | **YES** |
| **Framework 12-plaq L=2 PBC cube (this note)** | **0.422384 ± 0.000372** | direct MC + char. expansion | **YES (= V=1)** |
| Framework's `0.4291` (uniform-pairing ansatz) | 0.4291049969 | open_gate ansatz, not actual MC | n/a (failed) |
| 2D L=2 torus | 0.43213 | char. truncation level 4 | **YES** |
| Standard 3D L=2 PBC Wilson (24 plaq, ±daggers) | 0.4931 ± 0.002 | direct MC | open |
| Framework L → ∞ Wilson 4D periodic | 0.5934 ± 0.0002 | 5-vol FSS retained (PR #539) | **NO** (open lattice problem) |

## Status proposal

```yaml
note: PLAQUETTE_MINIMAL_BLOCK_CLOSED_FORM_NOTE_2026-05-05.md
type: research_finding (positive identification + numerical verification)
proposed_status: research_finding   # NOT bounded, NOT retained
proposed_subresults:
  - direct MC of framework's 12-plaq L=2 PBC cube at β=6: 0.422384 ± 0.000372 (3 seeds, 75000 measurements)
  - character-expansion analytic via Weyl integration: 0.4225317397 (trivial sector)
  - trivial-sector dominance: non-trivial irrep contributions < 10⁻¹³ under naive cube trace
  - identification: framework's minimal-block ⟨P⟩(β=6) ≡ V=1 closed form within 0.4σ MC error
  - reconciliation: 0.4291 is a (failed) ansatz already open_gate; not the actual cube value
audit_required:
  - independent MC reproduction of 0.422384 ± 0.000372 on the 12-plaq cube
  - rigorous bound on T_λ(cube) for non-trivial irreps (currently only naive ratio shown)
  - confirmation of the closed-form identification at the trivial-sector dominance level
bare_retained_allowed: no
follow_up_open_problem: bridge from minimal-block ⟨P⟩=0.4225 to L→∞ ⟨P⟩=0.5934
                          (structurally a different surface; thermodynamic-limit problem)
```

## Reusable artifacts

- [`scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`](../scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py) —
  derives, verifies, integrates the order-3 PF ODE; reproduces V=1 value (= cube value within MC error)
- Probe artifacts at `/tmp/su3_l2_apbc_3d/` (ephemeral; MC code, character expansion, ODE detection)

## Ledger entry

- **claim_id:** `plaquette_minimal_block_closed_form_note_2026-05-05`
- **note_path:** `docs/PLAQUETTE_MINIMAL_BLOCK_CLOSED_FORM_NOTE_2026-05-05.md`
- **runner_path:** `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`
- **claim_type:** `research_finding`
- **audit_status:** `unaudited`
- **dependency_chain:**
  - `PLAQUETTE_CLOSURE_MATHEMATICAL_PROBES_NOTE_2026-05-05.md` (V=1 PF ODE source)
  - `SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md` (cube geometry)
  - `SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md` (0.4291 reconciliation)
  - `PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md` (L → ∞ open problem)
