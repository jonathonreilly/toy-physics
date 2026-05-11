# Gauge-Vacuum Plaquette First Symmetric Three-Sample Minimal Positive Completion

**Date:** 2026-04-19  
**Status:** support - structural or confirmatory support note
three-sample seam; the local Wilson triple still fails the retained positive
cone, but there is one unique smallest adjoint-only positive completion  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py`

**Audit-conditional perimeter (2026-05-05):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing
step class `B`. The audit chain-closure explanation is exact: "the
adjoint-only half-line argument closes algebraically once Z^loc, F,
and the retained cone coordinates are accepted. The restricted packet
does not provide the upstream derivation of those inputs, and the
runner imports them from an unprovided prior module." The audit-stated
repair target is: "missing_dependency_edge: provide the upstream
local-Wilson obstruction note or runner source in the restricted
packet, or inline an independent derivation of radical_entries,
sample_matrix, and su3_partition_sum." This rigorization edit only
sharpens the boundary of the conditional perimeter; nothing here
promotes audit status, and the runner sha256 remains
`a48d33ae347b8d41003099301bb36c6704ea4dfd82cadb0d8c90ef8a4a8ddc22`.

## Question

Given the exact local Wilson three-sample triple on `W_A, W_B, W_C`, the exact
radical reconstruction map, and the exact first symmetric retained positive
cone, is there any constructive theorem stronger than “the current local triple
fails positivity”?

## Answer

Yes.

There is one exact constructive upgrade beyond the current no-go:

1. reconstruct the explicit local Wilson sample triple
   `Z^loc = [Z^loc_A, Z^loc_B, Z^loc_C]^T`
   through the exact inverse radical map
   `a^loc = F^(-1) Z^loc`;
2. observe that only the adjoint retained coordinate fails positivity:
   `a^loc_(1,1) < 0`, while `a^loc_(0,0) > 0` and `a^loc_(1,0) > 0`;
3. add exactly the minimal adjoint repair `-a^loc_(1,1)` and leave the other
   retained coordinates unchanged.

This produces the unique **explicit first-sector positive completion candidate**

`a^min = (a^loc_(0,0), a^loc_(1,0), 0)`

and the corresponding exact **completed sample triple**

`Z^min = F a^min`.

So the branch is no longer only a no-go at the first symmetric retained seam.
It now has one explicit constructive first-sector positive completion
candidate.

## Exact data

From the local-Wilson obstruction theorem:

`a^loc_(0,0) =  0.34960695245840506...`,

`a^loc_(1,0) =  0.09339384931083795...`,

`a^loc_(1,1) = -0.03190961277002444...`.

Therefore the unique minimal adjoint repair is

`r_min = -a^loc_(1,1) = 0.03190961277002444...`.

So

`a^min = (0.34960695245840506..., 0.09339384931083795..., 0)`.

Evaluating `Z^min = F a^min` gives the exact completed sample triple

`Z^min(W_A) = 0.1351652795620484...`,

`Z^min(W_B) = 0.3740128800091385...`,

`Z^min(W_C) = 0.5438438585441973...`.

The completion changes only the adjoint sample ray:

- `W_A` stays fixed because the adjoint orbit vanishes exactly there,
- `W_B` increases,
- `W_C` decreases.

## Theorem 1: unique adjoint-only minimal positive completion

Let `C = Cone(r_0, r_1, r_2)` be the exact first symmetric retained positive
cone with coordinates `a = F^(-1) Z`.

For the explicit local Wilson triple `Z^loc`, the first two coordinates of
`a^loc = F^(-1) Z^loc` are already nonnegative and the third is strictly
negative.

Hence among all adjoint-only repairs of the form

`a = (a^loc_(0,0), a^loc_(1,0), a^loc_(1,1) + t)`,

cone membership is equivalent to `t >= -a^loc_(1,1)`.

Therefore the unique minimal adjoint-only positive repair is

`t = -a^loc_(1,1)`,

equivalently `a = a^min`.

## What this closes

- one exact constructive upgrade beyond the local-Wilson positive-cone no-go
- one exact explicit first-sector positive completion candidate
- one exact completed sample triple on the named `W_A, W_B, W_C` seam
- one exact statement that the smallest positive repair is purely adjoint and
  unique along the adjoint-only route

## What this does not close

- the true full `beta = 6` spatial-environment transfer / boundary realization
- the actual framework-point Perron/Jacobi packet
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Meaning

This is the first genuinely constructive reopening on the plaquette branch
after the current-bank no-go theorems.

The branch can now say:

- the local Wilson triple is not itself the retained positive answer,
- but it canonically generates one explicit first-sector positive completion
  candidate,
- so the remaining seam is no longer “find any positive first-sector object,”
  but “realize or extend this candidate inside the true `beta = 6`
  spatial-environment packet.”

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py
```

## Imported authorities (audit-conditional perimeter register)

The runner [`scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py`](../scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py)
imports three names from the upstream local-Wilson obstruction module
[`scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py`](../scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py):

| Imported name | Provides | Used in this note for |
|---|---|---|
| `radical_entries` | exact symbolic radical entries `r_0`, `r_1`, `r_2` for the first symmetric retained cone | reconstructing the cone coordinates via `F = sample_matrix(radical_entries)` |
| `sample_matrix` | exact `3 x 3` radical sample matrix `F` | the `a^loc = F^(-1) Z^loc` reconstruction step in Theorem 1 |
| `su3_partition_sum` | exact one-plaquette `SU(3)` partition sum `Z_(1plaq)(6)` at `beta = 6` | the normalized local Wilson sample triple `Z^loc = [w_6(W_A), w_6(W_B), w_6(W_C)] / Z_(1plaq)(6)` |

The corresponding source note is
[`GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md),
which on the current ledger carries `claim_type: no_go` and
`effective_status: unaudited`. That parent note is exactly the upstream
authority whose absence the audit verdict flags: it derives the local
Wilson sample triple, the radical reconstruction map `F`, and the
first-symmetric retained positive cone coordinates that this note
imports.

The conditional perimeter of this row is therefore precisely the
unaudited status of the upstream parent note. The adjoint-only
half-line argument (Theorem 1) is itself algebraic: along
`a(t) = (a^loc_(0,0), a^loc_(1,0), a^loc_(1,1) + t)`, cone membership
is equivalent to coordinatewise nonnegativity, and the third coordinate
gives the half-line condition `t >= -a^loc_(1,1)` with unique minimum
at `t = -a^loc_(1,1)`. That algebraic step is not part of the
conditional perimeter at the stated scope; only the inputs `Z^loc`,
`F`, and the retained cone coordinates are.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for this row, the
audit-stated repair target is:

> missing_dependency_edge: provide the upstream local-Wilson
> obstruction note or runner source in the restricted packet, or
> inline an independent derivation of radical_entries, sample_matrix,
> and su3_partition_sum.

Two repair paths follow directly:

1. **Promote the upstream obstruction note.** Land an audited verdict
   on
   [`GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md`](GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md).
   That note already records the exact `a^loc` values, the radical
   reconstruction map, and the local-Wilson positive-cone obstruction
   theorem. Once it is retained-grade, this row's restricted-packet
   audit can pick up the upstream derivation by reference.

2. **Inline the upstream derivations into this runner.** Replace the
   three module-level imports with inline derivations of
   `radical_entries`, `sample_matrix`, and `su3_partition_sum` directly
   in [`frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py`](../scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py).
   This makes the runner self-contained but duplicates work that is
   more naturally factored into the parent local-Wilson obstruction
   module.

Either repair narrows the conditional perimeter; this rigorization edit
only sharpens the boundary register without changing audit status.
