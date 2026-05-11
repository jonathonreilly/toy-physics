# LH-Doublet Traceless Abelian Eigenvalue Ratio (Narrow Theorem)

**Date:** 2026-05-02
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Primary runner:** `scripts/frontier_lh_doublet_traceless_abelian_ratio.py`

## Claim scope (proposed)

> On the graph-first selected-axis surface, the unique traceless U(1)
> direction in the gl(3) ⊕ gl(1) commutant of {SU(2)\_weak, SWAP\_{ν,ρ}}
> has eigenvalue ratio **1 : (−3)** on the Sym²(ℂ²) (6-state) and
> Anti²(ℂ²) (2-state) sub-decompositions of the LH-doublet sector.

This is a structural ratio result. It explicitly **does not** claim:

- specific eigenvalues `+1/3` and `−1` (these require a normalization choice);
- identification with Standard Model hypercharge Y (this is a separate
  renaming step, out of scope here);
- the charge formula `Q = T_3 + Y/2` (out of scope);
- any anomaly-cancellation result (out of scope).

The audit row's previously-stated "claim boundary until fixed" was:
*"the selected-axis surface has a structural 3+1 split with a traceless
abelian direction whose normalized eigenvalues have the left-handed SM
ratio +1/3:−1."* This narrow theorem is the audit's own safe scope made
into a standalone claim with no SM-identification step in its load-bearing
chain.

## Retained dependencies (one-hop)

| Authority | Effective status | Role |
|---|---|---|
| [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | retained_bounded | supplies the 6-dim Sym² and 2-dim Anti² sub-decomposition on the LH-doublet sector |
| [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md) | retained_bounded | supplies the canonical axis selection upstream |

No other authorities are cited as load-bearing.

## Load-bearing step

```text
6 · α + 2 · β = 0       (tracelessness over Sym²+Anti² with multiplicities 6 and 2)
⇒ β = −3 α               (ratio is forced)
⇒ eigenvalue ratio on Sym² : Anti²  =  α : (−3α)  =  1 : (−3).
```

The 6 and 2 multiplicities come from the retained-grade graph-first integration
note's Sym² (3 axes × 2 weak-doublet states = 6 states) and Anti² (1 axis
× 2 weak-doublet states = 2 states) decomposition.

This is class (A) — algebraic identity check on retained-grade inputs. The
conclusion follows from the cited authorities without appeal to anything
else; no new symbol is defined, no external value is read in, no
phenomenological match is performed.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_lh_doublet_traceless_abelian_ratio.py
```

Verifies (at exact rational precision via Python `Fraction`):

1. The structural multiplicities 6 (Sym²) and 2 (Anti²) sum to the LH-
   doublet space dimension 8.
2. The tracelessness condition `6α + 2β = 0` has unique ratio solution
   `β/α = −3`.
3. The ratio is independent of the overall scale (verified for several α
   choices including 1, 2, −5, 7/11).
4. The SM identification step (assigning specific eigenvalues `+1/3` and
   `−1`, identifying with Y, applying `Q = T_3 + Y/2`) is **not** in the
   load-bearing chain and is **not** required for the ratio claim.

## What this note closes

The narrow ratio theorem `1 : (−3)` on Sym² : Anti² as a structural
algebraic consequence of the retained-grade graph-first commutant
decomposition.

## What this note does NOT close

- Specific eigenvalues `+1/3` and `−1` (requires admitted normalization).
- Identification with SM hypercharge Y (admitted renaming).
- The charge formula `Q = T_3 + Y/2` (admitted SM convention).
- Any anomaly cancellation (separate sister theorems).
- LHCM's full claim chain at `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` —
  this note narrows LHCM's safe scope to the ratio only; the SM-Y bridge
  remains an open downstream step.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: bounded_theorem
proposed_claim_scope: |
  exact eigenvalue ratio 1:(-3) on Sym²:Anti² of the LH-doublet sector under
  the graph-first selected-axis commutant decomposition; no specific eigenvalues,
  no SM hypercharge identification, no charge-formula claim.
audit_status_authority: independent audit lane only
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

If the audit lane ratifies a clean theorem verdict, the pipeline can derive a
retained-bounded effective status because both cited authorities are
retained-grade and the load-bearing step is a class (A) algebraic closure.

## Cross-references

- `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` — parent (the audit ledger currently
  records a conditional verdict); this narrow note carves out the audit's named
  safe scope as a standalone claim row.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) — retained-grade primitive supplying
  the commutant decomposition.
- `HYPERCHARGE_IDENTIFICATION_NOTE.md` (currently `audited_renaming`) —
  carries the SM-Y identification step that is **out of scope** here.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
