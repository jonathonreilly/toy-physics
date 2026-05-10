# SU(3) Quadratic Casimir on V_3 — Algebraic K1-K3 Narrow Proof-Walk Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/su3_casimir_fundamental_check.py`](../scripts/su3_casimir_fundamental_check.py)

## Why this note exists

The 2026-05-09 audit pass on the parent
[`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
returned `audited_conditional` with the following explicit repair
target:

> missing_bridge_theorem: add a retained bridge deriving the
> identification of V_3 with physical SM quark color and the
> perturbative QCD color-factor readout, or narrow the note to the
> algebraic K1-K3 Casimir statement.

This note pursues the second branch of that repair target: a narrow
proof-walk that scopes the audited claim explicitly to the algebraic
K1-K3 statement (centrality of `C_2`, Schur scalar property, value
`4/3`) on the cited 3-dim symmetric base subspace `V_3`, with
**no** physical-quark color identification load-bearing in the
audited chain. The K4 / C1-C5 physical-quark readouts remain in
the parent note's scope and continue to inherit the upstream
`cl3_color_automorphism_theorem` bound on physical SM color
identification.

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, does not introduce a new repo-wide theory class,
and does not make a retained-status promotion claim.

## Claim (narrow algebraic K1-K3)

Let SU(3) act on the cited 3-dim symmetric base subspace `V_3` (from
[`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md))
via the eight Gell-Mann generators `T^a = lambda^a / 2`, satisfying

```text
Tr[T^a T^b]  =  (1/2) delta^{ab}.
```

Define the quadratic Casimir

```text
C_2  :=  sum_{a=1}^{8} T^a T^a.
```

Then on the irreducible representation `V_3`:

- **(K1) Centrality.** `[C_2, T^b] = 0` for every Lie-algebra
  generator `T^b`.
- **(K2) Schur scalar.** There exists `c_2(3) in R` such that
  `C_2 = c_2(3) * I_3`.
- **(K3) Value.** `c_2(3) = 4/3`.

The narrow proof-walk does **not** claim any of:

- physical SM color identification of `V_3` (this remains the
  upstream bridge gap recorded in the parent note);
- the universal-color-charge K4 readout for physical SM quarks;
- the C1-C5 perturbative-QCD color-factor corollaries (one-gluon
  exchange, quark self-energy, color-singlet bilinears, cross-section
  color factors, lattice string-tension coefficient).

Those K4 / C1-C5 claims remain in the parent note and explicitly
inherit the `audited_conditional` upstream bound on physical SM
color identification.

## Proof-walk

| Step in the cited Casimir theorem | Load-bearing input | Physical-quark identification load-bearing? |
|---|---|---|
| (CN) Gell-Mann generator basis `T^a = lambda^a / 2` on `V_3` | `cl3_color_automorphism_theorem` (cited) | no |
| (TN) Trace orthonormality `Tr[T^a T^b] = (1/2) delta^{ab}` | standard Gell-Mann normalization (cited) | no |
| (LA) Lie-algebra closure `[T^a, T^b] = i f^{abc} T^c` | standard `su(3)` structure constants (admitted-context) | no |
| (K1) `[C_2, T^b] = i f^{abc} (T^a T^c + T^c T^a)` | (LA) plus standard `f^{abc}` total antisymmetry | no |
| (K1') Antisymmetric `f^{abc}` x symmetric `T^a T^c + T^c T^a` summed = 0 | combinatorial algebra on summation indices | no |
| (K2) Schur scalar `C_2 = c_2(3) * I_3` on irreducible `V_3` | Schur's lemma (admitted-context) | no |
| (K3a) `Tr[C_2] = sum_a Tr[T^a T^a] = 8 * (1/2) = 4` | (TN) plus exact arithmetic | no |
| (K3b) `Tr[c_2(3) * I_3] = c_2(3) * 3` | exact arithmetic | no |
| (K3c) Equating gives `c_2(3) * 3 = 4`, hence `c_2(3) = 4/3` | exact rational arithmetic | no |
| (K3d) Cross-check: `(N^2 - 1) / (2N)` at `N = 3` gives `8/6 = 4/3` | standard SU(N) Casimir formula | no |

The audited chain for K1-K3 uses only:

- the cited algebraic SU(3) embedding on `V_3` from
  `cl3_color_automorphism_theorem`;
- the cited Gell-Mann normalization `Tr[T^a T^b] = (1/2) delta^{ab}`;
- standard `su(3)` Lie-algebra structure constants (admitted-context);
- Schur's lemma (admitted-context);
- exact rational arithmetic.

The audited chain for K1-K3 does **not** use:

- physical SM color identification of `V_3`;
- perturbative QCD color-factor readout;
- one-gluon-exchange / quark self-energy / cross-section context;
- any continuum-limit numerical claim;
- any plaquette / lattice / Wilson-action quantity;
- any fitted observational value.

Promoting K3 to the K4 / C1-C5 physical-quark corollaries requires the
upstream physical SM color identification bridge, which the parent
note explicitly defers to a separate retained bridge dependency
(currently absent in the parent note's dep set, per the audit
ledger as of 2026-05-09).

## Exact arithmetic check

The runner repeats the K3 calculation by:

1. constructing the eight Gell-Mann matrices `lambda^a` explicitly;
2. forming `T^a = lambda^a / 2` and verifying Hermiticity and trace
   orthonormality `Tr[T^a T^b] = (1/2) delta^{ab}`;
3. checking the Lie-algebra closure `[T^a, T^b] = i f^{abc} T^c`;
4. constructing `C_2 = sum_a T^a T^a` and checking
   - all three eigenvalues equal (Schur scalar);
   - the common eigenvalue is `4/3` to floating-point precision;
5. cross-checking against the SU(N) closed-form `(N^2 - 1) / (2N)` at
   `N = 3`, giving `8 / 6 = 4/3`.

The runner is the same one cited by the parent note; this narrow
note does not introduce a new runner because the algebraic K1-K3
checks are already exercised by the parent runner. The new content is
the explicit scope-narrowing in the source note text, which records
the audit-recommended split between algebraic K1-K3 (closes within
the cited authority) and physical-quark K4 / C1-C5 (continues to
inherit the upstream physical SM color identification bound).

## Dependencies

- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
  for the parent theorem note being proof-walked.
- [`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
  for the cited algebraic SU(3) embedding on the 3-dim symmetric
  base subspace `V_3` and the Gell-Mann normalization
  `Tr[T^a T^b] = (1/2) delta^{ab}`.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does **not** show:

- physical SM color identification of `V_3` with physical SM quark
  color — this remains the upstream bridge gap explicitly deferred
  by the parent note;
- the universal-color-charge K4 readout for physical SM quarks —
  this continues to live in the parent note and continues to inherit
  the upstream `cl3_color_automorphism_theorem` bound;
- the C1-C5 perturbative-QCD color-factor corollaries — these
  continue to live in the parent note;
- any retained-status promotion of the parent
  `SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md` surface;
- any continuum-limit numerical claim;
- any follow-on proof-walk for other algebraic bookkeeping notes.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/su3_casimir_fundamental_check.py
```

Expected:

```text
OVERALL: PASS
```

The runner exercises the algebraic K1-K3 chain by checking
Hermiticity of `T^a`, trace orthonormality, `su(3)` Lie-algebra
closure, Schur scalar property of `C_2`, the exact value `4/3`,
and the cross-check against `(N^2 - 1) / (2N)` at `N = 3`.

```yaml
claim_id: su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10
note_path: docs/SU3_CASIMIR_FUNDAMENTAL_ALGEBRAIC_K1_K3_NARROW_PROOF_WALK_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/su3_casimir_fundamental_check.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_casimir_fundamental_theorem_note_2026-05-02
  - cl3_color_automorphism_theorem
audit_authority: independent audit lane only
```
