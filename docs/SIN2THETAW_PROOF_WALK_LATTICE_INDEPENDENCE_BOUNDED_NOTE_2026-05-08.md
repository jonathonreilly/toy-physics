# sin²θ_W^GUT = 3/8 Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_sin2thetaW_proof_walk_lattice_independence.py`](../scripts/frontier_sin2thetaW_proof_walk_lattice_independence.py)

## Claim

The proof that `sin²θ_W^GUT = 3/8` in
[`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)
does not use lattice-action machinery as a load-bearing input. It follows
from `Tr[Y²]` arithmetic + the standard SU(5) Killing-form normalization
+ the GUT-unification physical assumption already cited in the source
note. The proof-walk uses only:

- LHCM-derived hypercharge values fed into a `Tr[Y²]` arithmetic step;
- the standard SU(5) Killing-form normalization
  `Tr[T_a T_b]_5 = (1/2) δ_{ab}` (admitted in the source note §3 row "Y_GUT
  = √(3/5) · Y_SM");
- the GUT-unification physical assumption `g_3 = g_2 = g_1` at the GUT
  scale (admitted in the source note §5 and §5a residual (5));
- the SU(5)-vs-other-GUT-group choice (admitted in the source note §5
  and §5a residual (6));
- exact rational arithmetic in `Fraction` for the trig identity
  `sin²θ = tan²θ / (1 + tan²θ)`.

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim. The two physical admissions (`g_3 = g_2 = g_1`; SU(5) vs SO(10)/E6)
are already on the source note's ledger and are not re-admitted here.

## Proof-Walk

| Step in the cited source note | Load-bearing input | Lattice-action input? |
|---|---|---|
| §0 statement: `tan²θ_W = g'² / g_2²` definition | SM electroweak convention `Q = T_3 + Y/2` | no |
| §0 input (1)+(2): LHCM hypercharges and `Tr[Y²]` per Weyl family | LHCM-derived Y values + multiplicities | no |
| §0 input (3): `g_3 = g_2 = g_1` at GUT scale | admitted GUT-unification physical assumption (source note §5, §5a (5)) | no |
| §0 input (4): `Y_GUT = √(3/5) · Y_SM` rescaling | standard SU(5) Killing-form normalization `Tr[T_a T_b]_5 = (1/2) δ_{ab}` (source note §3 row, §5a (6)) | no |
| Proof step: `g'² = g_2² · (3/5)` at GUT scale | algebraic substitution combining the three admissions | no |
| Proof step: `tan²θ_W^GUT = 3/5` | exact rational arithmetic | no |
| Proof step: `sin²θ = tan²θ / (1 + tan²θ)` | universal trig identity | no |
| Output: `sin²θ_W^GUT = (3/5) / (8/5) = 3/8` | exact `Fraction` arithmetic | no |
| Output: `cos²θ_W^GUT = 5/8`, `tan²θ_W^GUT = 3/5` | algebraic consequences of `sin² + cos² = 1` | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The source note's reduced derivation gives, at the GUT scale,

```text
tan²θ_W^GUT = g'² / g_2² = 3/5,
```

after combining `Y_GUT = √(3/5) · Y_SM` with `g_3 = g_2 = g_1`. The
universal trig identity then yields

```text
sin²θ_W^GUT = tan²θ_W^GUT / (1 + tan²θ_W^GUT)
            = (3/5) / (1 + 3/5)
            = (3/5) / (8/5)
            = 3/8,
```

with `cos²θ_W^GUT = 1 − 3/8 = 5/8`. The runner repeats this calculation
with `fractions.Fraction` and cross-checks the trig consistency
`sin²θ + cos²θ = 1` and `tan²θ = sin²θ / cos²θ`. The runner also checks
the LHCM `Tr[Y²] = 40/3` per generation arithmetic that the source note
§0 input (2) cites as the trace-forced support for the `√(3/5)` rescaling
under the standard Killing-form normalization.

## Dependencies

- [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)
  for the source note being proof-walked.
- [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
  for the `Tr[Y²] = 40/3` arithmetic that the source note's input (2) cites.
- [`LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md`](LHCM_REPAIR_ATLAS_CONSOLIDATION_NOTE_2026-05-02.md)
  for the LHCM hypercharge values that feed `Tr[Y²]`.
- [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
  for the embedding-consistency context that the source note §5a
  cross-references; this proof-walk does not promote that note.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the GUT-unification physical assumption `g_3 = g_2 = g_1` at the GUT
  scale (already admitted in the source note §5 and §5a residual (5));
- the SU(5)-vs-SO(10)/E6 GUT-group choice (already admitted in the
  source note §5 and §5a residual (6));
- the running of `sin²θ_W` from the GUT scale down to `M_Z` (requires
  RG running, not derived in the source note or here);
- the GUT scale value itself (~10^16 GeV is observational/external);
- promotion of `SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`
  to retained status (still unaudited);
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_sin2thetaW_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; sin²θ_W^GUT = 3/8 derivation uses no
lattice-action quantity as a load-bearing input.
```
